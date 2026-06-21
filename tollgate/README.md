# Cashu Tollgate

Pay-per-minute SSH shell access with [Cashu](https://cashu.space) ecash tokens.

Users paste a Cashu token as their SSH username, the server redeems it into its own wallet, creates a throwaway guest account, and gives them an interactive bash shell for as many minutes as the token is worth (1 sat = 1 minute). When time runs out or they disconnect, the account is destroyed.

```
$ ssh -t cashuBo2FteB5odH...@tollgate.example.com

  +======================================+
  |        CASHU TOLLGATE                |
  +======================================+
  |  Mint:   https://testnut.cashu.exchange |
  |  Amount:    8 sat                     |
  |  Time:      8 min (  480 sec)       |
  |  User:   g-c3aa7bfb                   |
  +======================================+
  |  Run 'timeleft' to see remaining time|
  |  Session self-destructs on timeout.  |
  +======================================+

g-c3aa7bfb@tollgate:~$ whoami
g-c3aa7bfb
g-c3aa7bfb@tollgate:~$ timeleft
  Time remaining: 7m 39s (459s)
  Paid for:       8 minutes
  [############################--]
```

## Architecture

```
User
  └── ssh -t <cashu_token>@<host>
        │
        ▼
  Tollgate SSH Server (Go, port 22)
    ├── 1. Decode Cashu token (V3 JSON / V4 CBOR)
    ├── 2. Check replay (spent hash list)
    ├── 3. Verify unspent with mint API
    ├── 4. Redeem to CDK wallet (cdk-cli receive)
    ├── 5. Create JIT guest user (useradd)
    ├── 6. Spawn bash -i inside PTY (creack/pty)
    ├── 7. Timer kills session after N minutes
    └── 8. Cleanup (userdel -r -f) on disconnect/timeout

  Wallet (isolated cashu-wallet user)
    └── /var/lib/cashu-wallet/ (cdk-cli sqlite + seed)
          └── Balance accumulates, melt to Lightning later
```

## Components

| File | Purpose |
|---|---|
| `main.go` | Go SSH server — token decoding, verification, guest management, PTY shell |
| `faucet/index.html` | Static web page — mints free test tokens from testnut, shows copy-paste SSH command |
| `timeleft` | Shell script deployed to `/usr/local/bin/timeleft` — shows remaining session time |

## Requirements

- Debian 12 (or any Linux with `useradd`/`userdel`)
- [Go 1.22+](https://go.dev/) (for building)
- [cdk-cli](https://github.com/cashubtc/cdk/releases) (for token redemption)
- SSH host keys (`/etc/ssh/ssh_host_ed25519_key`, `ssh_host_rsa_key`)

## Install

### 1. Build the server

```bash
cd tollgate/
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o cashu-tollgate .
```

### 2. Deploy to your VPS

```bash
scp cashu-tollgate your-vps:/opt/cashu-tollgate/
scp faucet/index.html your-vps:/var/www/faucet/  # optional
```

### 3. Install cdk-cli

```bash
# Download latest release
curl -sL -o /usr/local/bin/cdk-cli \
  https://github.com/cashubtc/cdk/releases/latest/download/cdk-cli-$(uname -m)
chmod +x /usr/local/bin/cdk-cli
```

### 4. Create the wallet user

```bash
useradd -r -m -d /var/lib/cashu-wallet -s /usr/sbin/nologin cashu-wallet
chmod 700 /var/lib/cashu-wallet

# Initialize wallet (creates seed + sqlite db)
sudo -u cashu-wallet cdk-cli --work-dir /var/lib/cashu-wallet balance
```

### 5. Deploy timeleft command

```bash
cat > /usr/local/bin/timeleft << 'EOF'
#!/bin/bash
# Cashu Tollgate - show remaining session time
META="$HOME/.tollgate"
if [ ! -f "$META" ]; then
    echo "Not in a tollgate session"
    exit 1
fi
STARTED=$(python3 -c "import json; print(json.load(open('$META'))['started'])")
DURATION=$(python3 -c "import json; print(json.load(open('$META'))['duration'])")
AMOUNT=$(python3 -c "import json; print(json.load(open('$META'))['amount'])")
NOW=$(date +%s)
ELAPSED=$((NOW - STARTED))
REMAINING=$((DURATION - ELAPSED))
if [ $REMAINING -le 0 ]; then
    echo "Time's up!"
    exit 0
fi
MINS=$((REMAINING / 60))
SECS=$((REMAINING % 60))
FILLED=$((REMAINING * 30 / DURATION))
BAR=$(printf '█%.0s' $(seq 1 $FILLED))$(printf '░%.0s' $(seq $((FILLED+1)) 30))
echo "  Time remaining: ${MINS}m ${SECS}s (${REMAINING}s)"
echo "  Paid for:       ${AMOUNT} minutes"
echo "  [${BAR}]"
echo "  Session ends automatically. No refund for unused time."
EOF
chmod +x /usr/local/bin/timeleft
```

### 6. Move admin SSH to port 2222

```bash
# Edit /etc/ssh/sshd_config
Port 2222
systemctl restart sshd
```

### 7. Create systemd service

```bash
cat > /etc/systemd/system/cashu-tollgate.service << 'EOF'
[Unit]
Description=Cashu Tollgate SSH Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/cashu-tollgate/cashu-tollgate
Restart=on-failure
RestartSec=5
WorkingDirectory=/opt/cashu-tollgate

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now cashu-tollgate
```

### 8. Verify

```bash
systemctl status cashu-tollgate
# Should show: "Cashu Tollgate listening on port 22"
```

## Faucet (for testing)

The `faucet/index.html` is a single-page app that:
1. Connects to [testnut](https://testnut.cashu.exchange) (fake Lightning wallet — all invoices auto-pay)
2. Mints an 8-sat token using [cashu-ts](https://github.com/cashubtc/cashu-ts)
3. Shows the token + a ready-to-copy `ssh -t <token>@<host>` command

Deploy it anywhere that serves static files (GitHub Pages, Netlify, Caddy, nginx). Update `TOLLGATE_HOST` in the HTML to point to your server.

## Wallet Management

**Check balance:**
```bash
sudo -u cashu-wallet cdk-cli --work-dir /var/lib/cashu-wallet balance
```

**Cash out to Lightning:**
```bash
sudo -u cashu-wallet cdk-cli --work-dir /var/lib/cashu-wallet melt
# Enter a BOLT11 invoice from your Lightning wallet
```

**Transfer to another mint:**
```bash
sudo -u cashu-wallet cdk-cli --work-dir /var/lib/cashu-wallet transfer \
  --source-mint https://testnut.cashu.exchange \
  --target-mint <your-mint-url> \
  --full-balance
```

**Backup the seed:**
```bash
sudo cat /var/lib/cashu-wallet/seed > ~/cashu-wallet-seed-backup.txt
```
Anyone with this seed can spend your tokens. Keep it safe.

## Configuration

All config is at the top of `main.go`:

| Constant | Default | Description |
|---|---|---|
| `Port` | `22` | SSH listener port |
| `RateSecPerSat` | `60` | Seconds of shell time per sat (1 sat = 1 min) |
| `BaseDir` | `/opt/cashu-tollgate` | Directory for logs, spent hashes |
| `SpentHashesFile` | `spent.txt` | SHA256 hashes of used tokens (replay protection) |
| `TokensLogFile` | `tokens.log` | JSONL log of all token attempts |
| `WalletFile` | `wallet.jsonl` | Legacy wallet file (not used when cdk-cli handles redemption) |

## Security Model

### What guests CAN do
- Write to their home directory
- Use compilers, interpreters, network tools
- Run `timeleft` to check remaining time
- Use network (curl, wget, ssh outbound)

### What guests CANNOT do
- Access root or sudo
- See or access other users' home directories
- Read the Cashu wallet (`/var/lib/cashu-wallet/` is `chmod 700 cashu-wallet:cashu-wallet`)
- Access the tollgate server process or logs
- Survive disconnect (user is deleted on session end)

### What the server does
- Runs as root (needed for `useradd`/`userdel`)
- Redeems tokens via `sudo -u cashu-wallet cdk-cli receive` before granting access
- Tokens that fail redemption are rejected — no shell is given
- Guest usernames are deterministic: `g-` + `sha256(token)[:8]`
- PTY is allocated via `creack/pty` with `io.Copy` bridging to the SSH channel
- Timer goroutine sends SIGTERM + closes PTY + closes SSH session on timeout

### ⚠️ Security Disclaimer

**This software creates ephemeral user accounts with shell access on your server.** This has obvious security implications:

- **Guests can run arbitrary code** on your infrastructure. While they can't sudo, they can compile and execute programs, make network connections, and consume resources.
- **The Cashu token is the only authentication.** There is no password, no public key check. Anyone with a valid token gets a shell. Rate limiting and abuse prevention are not implemented.
- **The server runs as root** because it needs to create/delete system users. A vulnerability in the Go SSH server or PTY handling could be catastrophic.
- **Resource exhaustion** is trivial — a user could fork-bomb, fill disk, or consume all memory within their session.
- **Network access is unrestricted** — guests can use your server as a jump host, run port scans, or attack other systems. Your ISP/cloud provider may not appreciate this.

**Do not run this on a production server, a server with sensitive data, or any system you care about without understanding the risks.** If you're thinking about running this at work, **consult your IT/security team first.** This is a proof of concept for educational and experimental purposes.

## How It Works (deep dive)

### Token flow

1. **User connects:** `ssh -t cashuB...@host` — the Cashu token is the entire SSH username (can be 378+ characters)
2. **Decode:** Server parses V3 (`cashuA`, JSON/base64) or V4 (`cashuB`, CBOR) format, extracts mint URL, amount, and cryptographic proofs
3. **Replay check:** SHA256 of the token string is checked against `spent.txt`
4. **Mint verification:** Server calls `POST /v1/checkstate` on the mint to verify proofs are unspent
5. **Redeem:** Server calls `sudo -u cashu-wallet cdk-cli receive --allow-untrusted <token>` — this does a NUT-03 swap (invalidates user's proofs, mints new ones to the wallet). If this fails, the user gets nothing.
6. **User creation:** `useradd -m -s /bin/bash g-<hash>` with `chmod 700` home dir and custom `.bashrc`
7. **Shell:** `exec.Command("sudo", "-u", guest, "-H", "bash", "-i")` started inside a PTY via `creack/pty.Start()`. I/O bridged with `io.Copy` between SSH channel and PTY master fd.
8. **Timer:** Goroutine sleeps for `amount * 60` seconds, then SIGTERM → close PTY → close SSH → cleanup
9. **Cleanup:** `pkill -u <guest>` + `userdel -r -f <guest>` — user ceases to exist

### Why Go

We started with Python asyncssh. The PTY handling was fundamentally broken — `asyncio.create_subprocess_exec` creates pipes, not PTYs, so bash gets EOF and dies. The `pty.openpty()` + manual master/slave bridge also failed (master_fd returned EOF). Go's `gliderlabs/ssh` + `creack/pty` handles this cleanly:

```go
cmd := exec.Command("sudo", "-u", guest, "-H", "bash", "-i")
ptmx, _ := pty.Start(cmd)
go io.Copy(ptmx, s)   // stdin: SSH → PTY
io.Copy(s, ptmx)       // stdout: PTY → SSH
```

Three lines, battle-tested, works.

## Future Work

- **Rust rewrite** — [CDK](https://github.com/cashubtc/cdk) has no Go bindings. Currently shelling out to `cdk-cli`. A Rust rewrite with CDK + [russh](https://github.com/Eugeny/russh) would give native Cashu wallet operations in a single binary.
- **Rate limiting** — no protection against token brute-forcing or resource abuse
- **Real Bitcoin** — currently test-mint only. Accepting real sats requires trust decisions about which mints to accept and how to handle fees.
- **Monitoring** — basic structured logs, no metrics or alerting

## License

MIT
