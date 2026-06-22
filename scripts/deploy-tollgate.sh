#!/bin/bash
# deploy-tollgate.sh — automated Cashu Tollgate deployment on a fresh Ubuntu VM.
# Pushed via SSH: ssh ubuntu@<ip> 'sudo bash -s' < deploy-tollgate.sh
#
# Prerequisites: the tollgate binary must already be at /tmp/cashu-tollgate
# (SCP'd before running this script).

set -euo pipefail

BINARY_SRC="/tmp/cashu-tollgate"
INSTALL_DIR="/opt/cashu-tollgate"
WALLET_USER="cashu-wallet"
WALLET_HOME="/var/lib/cashu-wallet"
CDK_VERSION="0.17.1"

echo "=== 1. Install cdk-cli ==="
if ! command -v cdk-cli >/dev/null 2>&1; then
    curl -sL -o /usr/local/bin/cdk-cli \
        "https://github.com/cashubtc/cdk/releases/download/v${CDK_VERSION}/cdk-cli-${CDK_VERSION}-x86_64"
    chmod +x /usr/local/bin/cdk-cli
    echo "  installed cdk-cli ${CDK_VERSION}"
else
    echo "  cdk-cli already installed"
fi

echo "=== 2. Create wallet user ==="
if ! id "$WALLET_USER" >/dev/null 2>&1; then
    useradd -r -m -d "$WALLET_HOME" -s /usr/sbin/nologin "$WALLET_USER"
    chmod 700 "$WALLET_HOME"
    echo "  created $WALLET_USER"
else
    echo "  $WALLET_USER already exists"
fi

# Initialize wallet if not already done
if [ ! -f "$WALLET_HOME/seed" ]; then
    sudo -u "$WALLET_USER" cdk-cli --work-dir "$WALLET_HOME" balance >/dev/null 2>&1 || true
    echo "  wallet initialized"
fi

echo "=== 3. Install tollgate binary ==="
mkdir -p "$INSTALL_DIR"
cp "$BINARY_SRC" "$INSTALL_DIR/cashu-tollgate"
chmod +x "$INSTALL_DIR/cashu-tollgate"
echo "  binary installed at $INSTALL_DIR/cashu-tollgate"

echo "=== 4. Deploy timeleft command ==="
cat > /usr/local/bin/timeleft << 'TIMELEOF'
#!/bin/bash
META="$HOME/.tollgate"
if [ ! -f "$META" ]; then
    echo "Not in a tollgate session"
    exit 1
fi
STARTED=$(python3 -c "import json; print(int(json.load(open('$META'))['started']))")
DURATION=$(python3 -c "import json; print(int(json.load(open('$META'))['duration']))")
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
echo "  Time remaining: ${MINS}m ${SECS}s (${REMAINING}s)"
echo "  Paid for:       ${AMOUNT} minutes"
TIMELEOF
chmod +x /usr/local/bin/timeleft

echo "=== 5. Move admin SSH to port 2222 ==="
CURRENT_PORT=$(grep -E "^#?Port " /etc/ssh/sshd_config | head -1 | awk '{print $2}')
if [ "$CURRENT_PORT" != "2222" ]; then
    sed -i 's/^#\?Port .*/Port 2222/' /etc/ssh/sshd_config

    # Ubuntu 24.04 uses socket activation — disable it so the Port directive takes effect
    if systemctl list-unit-files | grep -q ssh.socket; then
        systemctl disable --now ssh.socket 2>/dev/null || true
        mkdir -p /etc/systemd/system/ssh.socket.d
        cat > /etc/systemd/system/ssh.socket.d/override.conf << 'SOCKEOF'
[Socket]
ListenStream=
ListenStream=2222
SOCKEOF
    fi

    systemctl daemon-reload
    systemctl restart ssh 2>/dev/null || systemctl restart sshd 2>/dev/null
    echo "  admin SSH now on port 2222 (connect: ssh -p 2222 <user>@<ip>)"
else
    echo "  admin SSH already on port 2222"
fi

echo "=== 6. Create systemd service ==="
cat > /etc/systemd/system/cashu-tollgate.service << SVCEOF
[Unit]
Description=Cashu Tollgate SSH Server
After=network.target

[Service]
Type=simple
ExecStart=${INSTALL_DIR}/cashu-tollgate
Restart=on-failure
RestartSec=5
WorkingDirectory=${INSTALL_DIR}

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable --now cashu-tollgate
echo "  tollgate service started (port 22)"

echo "=== 7. Verify ==="
sleep 2
if systemctl is-active --quiet cashu-tollgate; then
    echo "  service: ACTIVE"
else
    echo "  service: FAILED"
    journalctl -u cashu-tollgate --no-pager -n 20
    exit 1
fi

# Check port 22 is bound by tollgate
if ss -tlnp | grep -q ':22 '; then
    echo "  port 22: LISTENING"
else
    echo "  port 22: NOT LISTENING (check service logs)"
    exit 1
fi

echo ""
echo "=== DEPLOY COMPLETE ==="
echo "Tollgate SSH: port 22 (Cashu token auth)"
echo "Admin SSH:    port 2222 (key auth)"
echo "Wallet:       $WALLET_HOME"
echo ""
echo "Test: mint a token at https://testnut.cashu.exchange, then:"
echo "  ssh -t cashuB...@$(hostname -I | awk '{print $1}')"
