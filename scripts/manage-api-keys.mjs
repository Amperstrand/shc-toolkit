#!/usr/bin/env node
/**
 * SHC API Key Manager — Playwright script for creating/revoking API keys.
 *
 * Usage:
 *   node scripts/manage-api-keys.mjs --create --name "tollgate-ci" --scope full --days 90
 *   node scripts/manage-api-keys.mjs --list
 *   node scripts/manage-api-keys.mjs --revoke 106
 *
 * Requires PLAYWRIGHT_SHC_EMAIL and PLAYWRIGHT_SHC_PASSWORD env vars.
 * Uses Playwright to drive the SHC web UI (Blesta) since API key creation
 * via the API itself requires Basic auth + OTP.
 *
 * Run: npx playwright test --config=scripts/pw-config.mjs scripts/manage-api-keys.mjs
 * Or:  node scripts/manage-api-keys.mjs (if playwright is installed globally)
 */

import { chromium } from 'playwright';

const BASE = 'https://blesta.sovereignhybridcompute.com';
const EMAIL = process.env.SHC_PLAYWRIGHT_EMAIL || process.env.SHC_EMAIL;
const PASSWORD = process.env.SHC_PLAYWRIGHT_PASSWORD || process.env.SHC_PASSWORD;

async function login(page) {
  if (!EMAIL || !PASSWORD) {
    console.error('Set SHC_PLAYWRIGHT_EMAIL and SHC_PLAYWRIGHT_PASSWORD');
    process.exit(1);
  }
  await page.goto(`${BASE}/client/login/`);
  await page.fill('input[name="email"]', EMAIL);
  await page.fill('input[name="password"]', PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/client/**', { timeout: 10000 });
}

async function listKeys(page) {
  await page.goto(`${BASE}/client/apikeys/`);
  const rows = await page.$$eval('table tbody tr', rows => rows.map(r => {
    const cells = r.querySelectorAll('td');
    return {
      name: cells[0]?.textContent?.trim(),
      scope: cells[1]?.textContent?.trim(),
      areas: cells[2]?.textContent?.trim()?.slice(0, 60),
      prefix: cells[3]?.querySelector('code')?.textContent?.trim(),
      created: cells[4]?.textContent?.trim(),
      expires: cells[5]?.textContent?.trim(),
      lastUsed: cells[6]?.textContent?.trim(),
      revokeUrl: cells[7]?.querySelector('a')?.href,
    };
  }));
  console.log(JSON.stringify(rows, null, 2));
}

async function createKey(page, name, scope, days, areas = []) {
  await page.goto(`${BASE}/client/apikeys/`);

  await page.fill('input[name="name"]', name);

  const scopeMap = { read: 'Read', operate: 'Operate', full: 'Full' };
  await page.selectOption('select[name="scope"]', { label: scopeMap[scope] || 'Full' });

  await page.fill('input[name="expires"]', String(days));

  if (areas.length > 0) {
    for (const area of areas) {
      const labels = {
        billing: 'Invoices & Billing',
        services: 'Services (VMs)',
        transactions: 'Transactions',
        contacts: 'Contacts',
        account: 'Account & Payment Methods',
        emails: 'Email History',
        managers: 'Account Managers',
        credit: 'Account Credit',
        support: 'Support & Knowledge Base',
        quotations: 'Quotations',
      };
      const label = labels[area] || area;
      await page.check(`label:has-text("${label}") input[type="checkbox"]`);
    }
  }

  const responsePromise = page.waitForResponse(r => r.url().includes('/apikeys/') && r.request().method() === 'POST');
  await page.click('button:has-text("Create API Key")');
  const response = await responsePromise;

  const result = await page.evaluate(() => {
    const alert = document.querySelector('.alert');
    const keyEl = document.querySelector('code, .api-key, [class*="key"]');
    return {
      alert: alert?.textContent?.trim(),
      key: keyEl?.textContent?.trim(),
      body: document.body.textContent,
    };
  });

  const keyMatch = result.body.match(/shc_live_[A-Za-z0-9]{20,}/);
  const newKey = keyMatch ? keyMatch[0] : null;

  if (newKey) {
    console.log(JSON.stringify({ name, scope, days, areas, key: newKey, warning: 'Save this key — it will not be shown again' }, null, 2));
  } else {
    console.log(JSON.stringify({ name, scope, days, areas, key: null, pageAlert: result.alert, error: 'Could not extract key from page' }, null, 2));
    await page.screenshot({ path: '/tmp/shc-apikey-create.png' });
    console.error('Screenshot saved to /tmp/shc-apikey-create.png');
  }
}

async function revokeKey(page, keyIdOrPrefix) {
  await page.goto(`${BASE}/client/apikeys/`);

  const revokeLink = await page.$(`a[href*="/apikeys/delete/"]`);
  if (!revokeLink) {
    console.error(`No revoke link found for ${keyIdOrPrefix}`);
    return;
  }

  const allLinks = await page.$$eval('a[href*="/apikeys/delete/"]', links =>
    links.map(l => ({ href: l.href, text: l.closest('tr')?.textContent?.trim()?.slice(0, 80) }))
  );

  const target = allLinks.find(l =>
    l.text?.includes(keyIdOrPrefix) || l.href.includes(keyIdOrPrefix)
  );

  if (!target) {
    console.error(`Key ${keyIdOrPrefix} not found. Available:`);
    console.log(JSON.stringify(allLinks, null, 2));
    return;
  }

  console.log(`Revoking: ${target.text}`);
  await page.goto(target.href);
  const confirmBtn = await page.$('button:has-text("Delete"), button:has-text("Revoke"), input[type="submit"]');
  if (confirmBtn) {
    await confirmBtn.click();
    await page.waitForTimeout(2000);
    console.log('Revoked.');
  }
}

const args = process.argv.slice(2);
const action = args[0];

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await login(page);

    if (action === '--list' || action === 'list') {
      await listKeys(page);
    } else if (action === '--create') {
      const name = args[args.indexOf('--name') + 1] || 'playwright-key';
      const scope = args[args.indexOf('--scope') + 1] || 'full';
      const days = parseInt(args[args.indexOf('--days') + 1] || '90');
      const areasArg = args[args.indexOf('--areas') + 1];
      const areas = areasArg ? areasArg.split(',') : [];
      await createKey(page, name, scope, days, areas);
    } else if (action === '--revoke') {
      const id = args[args.indexOf('--revoke') + 1] || args[1];
      await revokeKey(page, id);
    } else {
      console.log(`Usage:
  node manage-api-keys.mjs --list
  node manage-api-keys.mjs --create --name "tollgate-ci" --scope full --days 90 [--areas services,billing,credit]
  node manage-api-keys.mjs --revoke <prefix-or-id>

Scopes: read, operate, full
Areas: billing, services, transactions, contacts, account, emails, managers, credit, support, quotations`);
    }
  } finally {
    await browser.close();
  }
})();
