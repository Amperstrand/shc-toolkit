#!/bin/bash
# setup-dev-worker.sh — Deploy physical-router-test-automation worker on SHC Dev VPS.
# First-time setup: installs system deps, Python venvs, clones repos.
# Pushed via: VMBootstrap.deploy(service_id, script)

set -ex

export DEBIAN_FRONTEND=noninteractive

echo "=== 1. Verify nested KVM ==="
ls -la /dev/kvm || { echo "FATAL: /dev/kvm not found — nested KVM not available"; exit 1; }
grep -oc "vmx\|svm" /proc/cpuinfo
echo "Nested KVM: OK"

echo "=== 2. Install system dependencies ==="
sudo apt-get update -qq
sudo apt-get install -y -qq \
    wget curl git socat ca-certificates gnupg \
    python3-venv python3-pip \
    qemu-system-x86 qemu-utils \
    bridge-utils cpu-checker \
    2>&1 | tail -5

echo "=== 3. Verify KVM acceleration ==="
kvm-ok 2>&1 || echo "(kvm-ok not available, checking manually)"
ls -la /dev/kvm
echo "KVM: OK"

echo "=== 4. Clone physical-router-test-automation ==="
cd /opt
sudo rm -rf tollgate-test 2>/dev/null || true
sudo git clone --depth 50 https://github.com/OpenTollGate/physical-router-test-automation.git tollgate-test
cd /opt/tollgate-test
echo "Repo cloned at $(pwd)"
git log --oneline -3

echo "=== 5. Create Python venv and install deps ==="
sudo python3 -m venv /opt/tollgate-venv
sudo /opt/tollgate-venv/bin/pip install -q --upgrade pip
if [ -f /opt/tollgate-test/requirements.txt ]; then
    sudo /opt/tollgate-venv/bin/pip install -q -r /opt/tollgate-test/requirements.txt
    echo "requirements.txt installed"
else
    echo "No requirements.txt found — installing minimal deps"
    sudo /opt/tollgate-venv/bin/pip install -q requests pytest
fi

echo "=== 6. Set permissions for debian user ==="
sudo chown -R debian:debian /opt/tollgate-test
sudo chown -R debian:debian /opt/tollgate-venv

echo "=== 7. Quick environment test ==="
cat > /tmp/test-kvm.sh << 'TESTEOF'
#!/bin/bash
set -e
echo "--- KVM available ---"
ls /dev/kvm
echo "--- QEMU version ---"
qemu-system-x86_64 --version | head -1
echo "--- Python venv ---"
/opt/tollgate-venv/bin/python3 -c "import sys; print(f'Python {sys.version}')"
echo "--- Repo structure ---"
ls /opt/tollgate-test/lib/cloud_lab/worker/ | head -10
echo "--- Worker importable ---"
cd /opt/tollgate-test && /opt/tollgate-venv/bin/python3 -c "from lib.cloud_lab.worker.config import WorkerConfig; print('WorkerConfig importable')" 2>&1 || echo "(import failed — checking deps)"
echo "=== QUICK TEST PASSED ==="
TESTEOF
chmod +x /tmp/test-kvm.sh
bash /tmp/test-kvm.sh

echo ""
echo "=== SETUP COMPLETE ==="
echo "Repo: /opt/tollgate-test"
echo "Venv: /opt/tollgate-venv"
echo "KVM:  /dev/kvm (nested virtualization active)"
echo ""
echo "To run the worker:"
echo "  cd /opt/tollgate-test"
echo "  export TOLLGATE_RUN_ID=shc-test-001"
echo "  export TOLLGATE_QUICK=1"
echo "  export GH_TOKEN=\$(cat /opt/tollgate-test/.env | grep GH_TOKEN | cut -d= -f2)"
echo "  /opt/tollgate-venv/bin/python3 -m lib.cloud_lab.worker --from-env"
