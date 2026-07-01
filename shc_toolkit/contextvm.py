"""ContextVM bootstrap — turn SHC VMs into discoverable MCP servers on Nostr.

Installs the ContextVM TS SDK on a VM, generates a Nostr keypair, deploys a
minimal MCP gateway server, and starts it as a systemd service.

Requires: VM must be running with SSH access (debian user, key-based auth).

Usage:
    from shc_toolkit.contextvm import install_contextvm, generate_server_script

    # Deploy to a VM
    install_contextvm("1.2.3.4", user="debian")

    # Or generate the server script to inspect/customize
    script = generate_server_script(name="my-vm-server")
"""

from __future__ import annotations

import logging
from typing import Any

from .provision import ssh_cmd

log = logging.getLogger(__name__)

DEFAULT_RELAY = "wss://relay.contextvm.org"
REMOTE_DIR = "/home/debian/contextvm"


def generate_server_script(
    name: str = "shc-vm",
    relay: str = DEFAULT_RELAY,
    about: str = "",
    user: str = "debian",
) -> str:
    """Generate a ContextVM MCP gateway server script (TypeScript/Bun).

    This script wraps a mock MCP server and exposes it over Nostr via the
    ContextVM Gateway. The VM becomes discoverable by its Nostr pubkey.

    Args:
        name: Server name shown in ContextVM discovery.
        relay: Nostr relay URL for ContextVM communication.
        about: Optional description text.

    Returns:
        TypeScript source code for the server script.
    """
    bun_bin = f"/home/{user}/.bun/bin/bun" if user else "/root/.bun/bin/bun"
    return f'''import {{
  NostrMCPGateway,
}} from "@contextvm/sdk";
import {{ PrivateKeySigner }} from "@contextvm/sdk/signer";
import {{ generateSecretKey, getPublicKey }} from "nostr-tools";
import {{ StdioClientTransport }} from "@modelcontextprotocol/sdk/client/stdio.js";
import {{ Client }} from "@modelcontextprotocol/sdk/client/index.js";
import {{ writeFileSync, readFileSync }} from "fs";

// Generate or load Nostr identity (stored as hex)
let skHex: string;
try {{
  skHex = readFileSync("{REMOTE_DIR}/secret.key", "utf8").trim();
  console.log("Loaded existing Nostr identity");
}} catch {{
  skHex = Buffer.from(generateSecretKey()).toString("hex");
  writeFileSync("{REMOTE_DIR}/secret.key", skHex);
  console.log("Generated new Nostr identity");
}}

const pk = getPublicKey(Buffer.from(skHex, "hex"));
console.log("Server pubkey:", pk);

// Connect to a mock MCP server (echo) via stdio.
// Replace this with your actual MCP server.
const mcpClient = new Client(
  {{ name: "{name}", version: "1.0.0" }},
  {{ capabilities: {{}} }},
);

const transport = new StdioClientTransport({{
  command: "{bun_bin}",
  args: ["{REMOTE_DIR}/echo-server.ts"],
}});

const signer = new PrivateKeySigner(skHex);

const gateway = new NostrMCPGateway({{
  mcpClientTransport: transport,
  nostrTransportOptions: {{
    signer,
    relayHandler: ["{relay}"],
    isPublicServer: true,
    publishRelayList: true,
    serverInfo: {{
      name: "{name}",
      about: "{about}",
      website: "",
    }},
  }},
}});

console.log("Starting ContextVM gateway...");
console.log("Relay: {relay}");
console.log("Discover me at pubkey:", pk);

await gateway.start();
console.log("Gateway started. Waiting for connections...");

// Keep alive
process.on("SIGINT", async () => {{
  console.log("Shutting down...");
  await gateway.stop();
  process.exit(0);
}});

await new Promise(() => {{}}); // run forever
'''


def generate_echo_server() -> str:
    """Generate a minimal MCP echo server (TypeScript/Bun).

    This is a placeholder MCP server that echoes messages.
    Replace with your actual tools/capabilities.
    """
    return '''import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "echo", version: "1.0.0" },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "echo",
    description: "Echo a message back",
    inputSchema: {
      type: "object",
      properties: { message: { type: "string" } },
      required: ["message"],
    },
  }],
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  if (req.params.name === "echo") {
    return {
      content: [{ type: "text", text: `Echo: ${{req.params.arguments?.message}}` }],
    };
  }
  return { content: [{ type: "text", text: "Unknown tool" }], isError: true };
});

const transport = new StdioServerTransport();
await server.connect(transport);
'''


def generate_systemd_service(user: str = "debian") -> str:
    """Generate a systemd unit file for the ContextVM gateway."""
    return f"""[Unit]
Description=ContextVM MCP Gateway
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={REMOTE_DIR}
ExecStart=/home/{user}/.bun/bin/bun run {REMOTE_DIR}/gateway.ts
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PATH=/home/{user}/.bun/bin:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
"""


def install_contextvm(
    host: str,
    user: str = "debian",
    server_name: str = "shc-vm",
    relay: str = DEFAULT_RELAY,
    port: int | None = None,
) -> dict[str, Any]:
    """Install ContextVM on a VM via SSH.

    Installs Bun runtime, @contextvm/sdk, deploys server scripts, and starts
    a systemd service. The VM becomes a discoverable MCP server on Nostr.

    Args:
        host: VM IP address.
        user: SSH username.
        server_name: Name shown in ContextVM discovery.
        relay: Nostr relay for ContextVM communication.
        port: Unused (ContextVM uses Nostr, not direct TCP). Kept for API compat.

    Returns:
        Dict with installation status and VM's Nostr pubkey (if available).
    """
    result: dict[str, Any] = {"host": host, "server_name": server_name}

    log.info("Installing ContextVM on %s@%s", user, host)

    # 1. Create working directory
    ssh_cmd(host, f"mkdir -p {REMOTE_DIR}", user=user, timeout=15)

    # 2. Install unzip (required by Bun installer, not on fresh Debian cloud images)
    log.info("Installing unzip (wait for cloud-init dpkg lock to release)...")
    ssh_cmd(
        host,
        f"sudo bash -c 'for i in $(seq 1 30); do "
        f"apt-get update -qq && apt-get install -y -qq unzip && break "
        f"|| sleep 5; done'",
        user=user,
        timeout=300,
    )

    # 3. Install Bun
    log.info("Installing Bun runtime...")
    ssh_cmd(host, "curl -fsSL https://bun.sh/install | bash", user=user, timeout=60)

    # 4. Initialize project + install SDK
    log.info("Installing @contextvm/sdk...")
    ssh_cmd(
        host,
        f"cd {REMOTE_DIR} && "
        f'/home/{user}/.bun/bin/bun init -y && '
        f"/home/{user}/.bun/bin/bun add @contextvm/sdk nostr-tools "
        f"@modelcontextprotocol/sdk",
        user=user,
        timeout=120,
    )

    # 5. Deploy server scripts
    log.info("Deploying server scripts...")
    gateway_script = generate_server_script(name=server_name, relay=relay, user=user)
    echo_script = generate_echo_server()
    systemd_unit = generate_systemd_service(user=user)

    import subprocess
    for filename, content in [
        ("gateway.ts", gateway_script),
        ("echo-server.ts", echo_script),
    ]:
        subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             f"{user}@{host}", f"cat > {REMOTE_DIR}/{filename}"],
            input=content, text=True, timeout=30,
        )

    # 6. Install systemd service
    log.info("Setting up systemd service...")
    subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no",
         f"{user}@{host}", f"sudo tee /etc/systemd/system/contextvm.service"],
        input=systemd_unit, text=True, timeout=30,
    )
    ssh_cmd(host, "sudo systemctl daemon-reload && "
             "sudo systemctl enable contextvm && "
             "sudo systemctl start contextvm", user=user, timeout=30)

    # 7. Wait and check status
    import time
    time.sleep(3)
    try:
        status = ssh_cmd(host, "sudo systemctl is-active contextvm", user=user, timeout=10)
        result["service_active"] = "active" in status
    except Exception:
        result["service_active"] = False

    # 8. Try to get the pubkey from logs
    try:
        logs = ssh_cmd(host, "sudo journalctl -u contextvm --no-pager -n 10",
                       user=user, timeout=10)
        for line in logs.split("\n"):
            if "pubkey:" in line.lower():
                pk = line.split("pubkey:")[-1].strip()
                result["pubkey"] = pk
                break
    except Exception:
        pass

    result["relay"] = relay
    result["discoverable"] = result.get("service_active", False)

    if result.get("service_active"):
        log.info("ContextVM running on %s. Pubkey: %s", host, result.get("pubkey", "unknown"))
    else:
        log.warning("ContextVM service may not have started. Check: ssh %s@%s journalctl -u contextvm",
                    user, host)

    return result
