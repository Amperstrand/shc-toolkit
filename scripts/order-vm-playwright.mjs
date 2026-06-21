#!/usr/bin/env node
/**
 * SHC VM Ordering via Playwright — workaround for API ordering 500 bug.
 *
 * The SHC User API POST /ordering/submit returns 500 internal_error
 * after confirmation on ALL plans (confirmed June 2026, ticket #214).
 * This script drives the Blesta web UI to place orders instead.
 *
 * Usage:
 *   node scripts/order-vm-playwright.mjs \
 *     --form dev-vps --plan standard --period day \
 *     --hostname my-vm --ssh-key ~/.ssh/id_ed25519.pub \
 *     --os "Debian 13" --apply-credit --agree-terms
 *
 *   # List available forms
 *   node scripts/order-vm-playwright.mjs --forms
 *
 *   # List plans in a form
 *   node scripts/order-vm-playwright.mjs --form dev-vps --plans
 *
 *   # Cancel a VM (uses API, not Playwright)
 *   node scripts/order-vm-playwright.mjs --cancel 602
 *
 * Requires:
 *   - SHC_PLAYWRIGHT_EMAIL / SHC_PLAYWRIGHT_PASSWORD env vars
 *   - playwright installed (npm install playwright)
 *
 * CSRF NOTE: Blesta form tokens expire after ~15 min of inactivity.
 * This script completes the full flow (login → plan → config → checkout)
 * in under 60 seconds to avoid token expiry.
 */

import { chromium } from 'playwright';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

const BASE = 'https://blesta.sovereignhybridcompute.com';
const EMAIL = process.env.SHC_PLAYWRIGHT_EMAIL || process.env.SHC_EMAIL;
const PASSWORD = process.env.SHC_PLAYWRIGHT_PASSWORD || process.env.SHC_PASSWORD;

// ─── CLI Parsing ─────────────────────────────────────────────

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    } else {
      args._.push(arg);
    }
  }
  return args;
}

// ─── Helpers ─────────────────────────────────────────────────

function readSshKey(path) {
  const resolved = resolve(path.replace('~', process.env.HOME));
  if (!existsSync(resolved)) {
    console.error(`SSH key not found: ${resolved}`);
    process.exit(1);
  }
  return readFileSync(resolved, 'utf-8').trim();
}

async function login(page) {
  if (!EMAIL || !PASSWORD) {
    console.error('Set SHC_PLAYWRIGHT_EMAIL and SHC_PLAYWRIGHT_PASSWORD');
    process.exit(1);
  }
  process.stderr.write('Logging in... ');
  await page.goto(`${BASE}/client/login/`);
  await page.fill('input[name="email"]', EMAIL);
  await page.fill('input[name="password"]', PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/client/', { timeout: 10000 });
  process.stderr.write('OK\n');
}

// ─── Order Flow ──────────────────────────────────────────────

/**
 * Map plan name to index in the plan list.
 * dev-vps: 0=Starter, 1=Standard, 2=Professional, 3=Business, 4=Enterprise
 * NVME: same order
 * kansas-vps: same order
 */
const PLAN_INDEX = {
  starter: 0, standard: 1, professional: 2, pro: 2, business: 3, enterprise: 4,
};

/**
 * Map period name to option label fragment.
 */
const PERIOD_MAP = {
  day: '1 Day',
  week: '1 Week',
  month: '1 Month',
  year: '1 Year',
};

async function orderVM(page, opts) {
  const {
    form = 'dev-vps',
    plan = 'standard',
    period = 'day',
    hostname,
    sshKey,
    os = 'Debian 13',
    applyCredit = true,
    agreeTerms = true,
    ram, cpu, disk, ipv4, desktop,
  } = opts;

  if (!hostname) {
    console.error('--hostname is required');
    process.exit(1);
  }

  const planIdx = PLAN_INDEX[plan.toLowerCase()];
  if (planIdx === undefined) {
    console.error(`Unknown plan: ${plan}. Valid: ${Object.keys(PLAN_INDEX).join(', ')}`);
    process.exit(1);
  }

  const periodLabel = PERIOD_MAP[period.toLowerCase()];
  if (!periodLabel) {
    console.error(`Unknown period: ${period}. Valid: ${Object.keys(PERIOD_MAP).join(', ')}`);
    process.exit(1);
  }

  // Step 1: Navigate to order form and select plan
  process.stderr.write(`Selecting ${plan} (${periodLabel}) from ${form}... `);
  await page.goto(`${BASE}/order/main/index/${form}/`);
  await page.waitForURL(`**/order/main/packages/${form}**`, { timeout: 10000 });

  const planForms = page.locator('form:has(button:has-text("Add to Cart"))');
  const count = await planForms.count();
  if (planIdx >= count) {
    console.error(`Plan index ${planIdx} out of range (only ${count} plans available)`);
    process.exit(1);
  }

  const targetForm = planForms.nth(planIdx);
  await targetForm.locator('select').selectOption(new RegExp(periodLabel));
  await targetForm.getByRole('button').click();
  await page.waitForURL('**/order/config/index/**', { timeout: 10000 });
  process.stderr.write('OK\n');

  // Step 2: Fill config RAPIDLY (CSRF token expires!)
  process.stderr.write('Filling configuration... ');

  await page.getByRole('textbox', { name: 'Hostname' }).fill(hostname);

  if (sshKey) {
    const keyContent = sshKey.startsWith('ssh-') ? sshKey : readSshKey(sshKey);
    await page.getByRole('textbox', { name: 'SSH Public Key' }).fill(keyContent);
  }

  // Select OS if specified
  const osSelect = page.getByRole('combobox', { name: 'Operating System' });
  if (await osSelect.count() > 0) {
    await osSelect.selectOption(os);
  }

  // Optional config overrides
  if (ram) {
    const ramSelect = page.getByRole('combobox', { name: 'Total RAM' });
    if (await ramSelect.count() > 0) await ramSelect.selectOption(new RegExp(ram));
  }
  if (cpu) {
    const cpuSelect = page.getByRole('combobox', { name: 'vCPU Cores' });
    if (await cpuSelect.count() > 0) await cpuSelect.selectOption(new RegExp(cpu));
  }
  if (disk) {
    const diskSelect = page.getByRole('combobox', { name: 'SSD Storage' });
    if (await diskSelect.count() > 0) await diskSelect.selectOption(new RegExp(disk));
  }
  if (ipv4) {
    const ipSelect = page.getByRole('combobox', { name: 'Total IPv4 Addresses' });
    if (await ipSelect.count() > 0) await ipSelect.selectOption(new RegExp(ipv4));
  }
  if (desktop) {
    const deskSelect = page.getByRole('combobox', { name: 'Desktop Environment' });
    if (await deskSelect.count() > 0) await deskSelect.selectOption(new RegExp(desktop));
  }

  // Click Continue immediately
  await page.getByRole('button', { name: 'Continue' }).click();
  process.stderr.write('OK\n');

  // Step 3: Review page — just click Checkout
  process.stderr.write('Reviewing order... ');
  await page.waitForURL('**/order/cart/index/**', { timeout: 10000 });

  // Verify the order looks right
  const orderText = await page.locator('table').first().textContent();
  if (!orderText.includes(hostname)) {
    console.error(`Warning: hostname "${hostname}" not found in order review!`);
    console.error(orderText.substring(0, 500));
  }

  // Click Checkout
  await page.getByRole('link', { name: 'Checkout' }).click();
  await page.waitForURL('**/order/checkout/index/**', { timeout: 10000 });
  process.stderr.write('OK\n');

  // Step 4: Checkout
  process.stderr.write('Checking out... ');

  if (applyCredit) {
    const creditCheckbox = page.getByRole('checkbox', { name: /Apply Credit/ });
    if (await creditCheckbox.count() > 0) {
      await creditCheckbox.check();
    }
  }

  if (agreeTerms) {
    const termsCheckbox = page.getByRole('checkbox', { name: /Terms/ });
    if (await termsCheckbox.count() > 0) {
      await termsCheckbox.check();
    }
  }

  // Submit order
  await page.getByRole('button', { name: 'Submit Order' }).click();

  // Wait for completion page
  await page.waitForURL('**/order/checkout/complete/**', { timeout: 30000 });
  process.stderr.write('OK\n');

  // Extract order ID from URL
  const url = page.url();
  const orderIdMatch = url.match(/complete\/[^/]+\/([a-f0-9]+)/);
  const orderId = orderIdMatch ? orderIdMatch[1] : 'unknown';

  // Extract details from completion page
  const bodyText = await page.textContent('body');
  const priceMatch = bodyText.match(/\$(\d+\.\d{4})/);
  const price = priceMatch ? priceMatch[1] : '?';

  const result = {
    order_id: orderId,
    hostname,
    plan: `${form}/${plan}`,
    period,
    price: `$${price}`,
    status: 'ordered',
    url,
  };

  console.log(JSON.stringify(result, null, 2));
  return result;
}

// ─── List Forms ──────────────────────────────────────────────

async function listForms(page) {
  await page.goto(`${BASE}/order/forms/`);
  const forms = await page.$$eval('h3 + a, h3', (els) => {
    return els.map(e => e.textContent?.trim()).filter(t => t);
  });
  // Better: extract from the order page cards
  const cards = await page.$$eval('[class*="card"], [class*="package"]', (els) => {
    return els.map(e => {
      const heading = e.querySelector('h3')?.textContent?.trim();
      const link = e.querySelector('a[href*="/order/main/index/"]')?.getAttribute('href');
      const desc = e.querySelector('p')?.textContent?.trim()?.substring(0, 100);
      return { heading, link, desc };
    }).filter(c => c.heading && c.link);
  });

  if (cards.length > 0) {
    console.log('Available order forms:\n');
    for (const c of cards) {
      const formId = c.link?.match(/index\/([^/]+)/)?.[1] || '?';
      console.log(`  ${formId.padEnd(15)} ${c.heading}`);
      if (c.desc) console.log(`  ${' '.repeat(15)} ${c.desc}...\n`);
    }
  } else {
    // Fallback: just list known forms
    console.log('Known order forms:');
    console.log('  dev-vps       Dev VPS (Nested KVM) — Cherryvale, Kansas');
    console.log('  NVME          NVMe Cloud VPS — Katy, Texas');
    console.log('  kansas-vps    SSD Cloud VPS — Cherryvale, Kansas');
    console.log('  HDD           HDD Cloud VPS — Katy, Texas');
  }
}

// ─── List Plans ──────────────────────────────────────────────

async function listPlans(page, form) {
  await page.goto(`${BASE}/order/main/index/${form}/`);
  await page.waitForURL(`**/order/main/packages/${form}**`, { timeout: 10000 });

  const plans = await page.$$eval('form:has(button:has-text("Add to Cart"))', (forms, formId) => {
    return forms.map((f, i) => {
      // Find the plan name — it's the <strong> before the form
      let prev = f.previousElementSibling;
      while (prev && !prev.querySelector('strong') && prev.previousElementSibling) {
        prev = prev.previousElementSibling;
      }
      const name = prev?.querySelector('strong')?.textContent?.trim() || `Plan ${i}`;
      const desc = prev?.querySelector('p')?.textContent?.trim()?.substring(0, 120);
      const options = Array.from(f.querySelectorAll('option')).map(o => o.textContent?.trim());
      return { index: i, name, desc, pricing: options };
    });
  }, form);

  console.log(`Plans in ${form}:\n`);
  for (const p of plans) {
    console.log(`  [${p.index}] ${p.name}`);
    if (p.desc) console.log(`      ${p.desc.substring(0, 100)}`);
    console.log(`      Pricing: ${p.pricing.join(' | ')}`);
    console.log();
  }
}

// ─── Cancel VM ───────────────────────────────────────────────

async function cancelVM(serviceId) {
  // Use the API for cancellation (it works)
  const apiKey = process.env.SHC_API_KEY;
  if (!apiKey) {
    console.error('SHC_API_KEY required for --cancel');
    process.exit(1);
  }

  const resp = await fetch(`${BASE.replace('blesta.', 'blesta.')}/user-api/v2/vm/${serviceId}/cancel`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  });
  const body = await resp.json();
  if (resp.ok) {
    console.log(`Cancelled VM ${serviceId}: ${JSON.stringify(body)}`);
  } else {
    console.error(`Failed to cancel: ${JSON.stringify(body)}`);
    process.exit(1);
  }
}

// ─── Wait for SSH ────────────────────────────────────────────

async function waitForSSH(ip, maxWaitSec = 300) {
  const { execSync } = await import('child_process');
  const deadline = Date.now() + maxWaitSec * 1000;
  process.stderr.write(`Waiting for SSH at ${ip}...`);

  while (Date.now() < deadline) {
    process.stderr.write('.');
    try {
      const result = execSync(
        `ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o BatchMode=yes debian@${ip} "hostname" 2>/dev/null`,
        { timeout: 10000, encoding: 'utf-8' }
      ).trim();
      if (result) {
        process.stderr.write(` OK (${result})\n`);
        return true;
      }
    } catch {
      // Not ready yet
    }
    await new Promise(r => setTimeout(r, 10000));
  }
  process.stderr.write(' TIMEOUT\n');
  return false;
}

// ─── Main ────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);

  // Non-Playwright commands
  if (args.cancel) {
    await cancelVM(args.cancel);
    return;
  }

  // Launch browser
  const browser = await chromium.launch({
    headless: !args['show-browser'],
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
  });
  const page = await context.newPage();

  try {
    await login(page);

    if (args.forms) {
      await listForms(page);
    } else if (args.plans) {
      await listPlans(page, args.form || 'dev-vps');
    } else if (args.order || args.hostname) {
      const sshKey = args['ssh-key'] || args.sshKey;
      const result = await orderVM(page, {
        form: args.form || 'dev-vps',
        plan: args.plan || 'standard',
        period: args.period || 'day',
        hostname: args.hostname,
        sshKey,
        os: args.os,
        applyCredit: args['apply-credit'] !== false,
        agreeTerms: args['agree-terms'] !== false,
        ram: args.ram,
        cpu: args.cpu,
        disk: args.disk,
        ipv4: args.ipv4 || args.ip,
        desktop: args.desktop,
      });

      // Optionally wait for SSH
      if (args.wait || args.ssh) {
        process.stderr.write('\n');
        // Get IP from API
        const apiKey = process.env.SHC_API_KEY;
        if (apiKey) {
          const resp = await fetch(`${BASE}/user-api/v2/vm`, {
            headers: { 'Authorization': `Bearer ${apiKey}` },
          });
          const vms = await resp.json();
          const vm = vms.items?.find(v => v.hostname === args.hostname);
          if (vm) {
            const ip = vm.ips?.[0]?.ip;
            if (ip) {
              console.log(`VM IP: ${ip} (service_id: ${vm.id})`);
              await waitForSSH(ip, args['ssh-timeout'] || 300);
            }
          }
        }
      }
    } else {
      console.log(`SHC VM Ordering Script

Usage:
  node scripts/order-vm-playwright.mjs --forms                    List order forms
  node scripts/order-vm-playwright.mjs --form dev-vps --plans     List plans in a form
  node scripts/order-vm-playwright.mjs --order \\
    --form dev-vps --plan standard --period day \\
    --hostname my-vm --ssh-key ~/.ssh/id_ed25519.pub \\
    --os "Debian 13" --apply-credit --agree-terms [--wait]

  node scripts/order-vm-playwright.mjs --cancel 602               Cancel a VM

Options:
  --form          Order form: dev-vps, NVME, kansas-vps, HDD (default: dev-vps)
  --plan          Plan: starter, standard, professional, business, enterprise
  --period        Billing: day, week, month, year (default: day)
  --hostname      VM hostname (required for --order)
  --ssh-key       Path to SSH public key or inline key
  --os            OS template name (default: "Debian 13")
  --apply-credit  Use account credit for payment (default: true)
  --agree-terms   Agree to ToS automatically (default: true)
  --ram           Override RAM (e.g., "16 GB")
  --cpu           Override CPU cores (e.g., "4 Cores")
  --disk          Override disk (e.g., "32 GB")
  --ipv4          Override IPv4 count (e.g., "2 IPs")
  --desktop       Desktop environment (e.g., "GNOME Desktop")
  --wait          Wait for SSH after ordering
  --ssh-timeout   Max seconds to wait for SSH (default: 300)
  --show-browser  Show browser window (for debugging)
  --forms         List available order forms
  --plans         List plans in --form

Env:
  SHC_PLAYWRIGHT_EMAIL     Blesta login email
  SHC_PLAYWRIGHT_PASSWORD  Blesta login password
  SHC_API_KEY              API key (for --wait and --cancel)
`);
    }
  } finally {
    await browser.close();
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
