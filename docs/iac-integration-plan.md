# SHC IaC Integration — Implementation Plan

## Overview
Three phases: backup CLI → Pulumi provider → Terraform provider. Each phase is independently testable and deployable.

---

## Phase 1: Backup CLI Commands (30 min)

### Files to modify
- `shc_toolkit/cli.py` — Add 6 new command functions + subparsers
- `shc_toolkit/client.py` — Add `verify_backup` method (API endpoint exists, not wrapped)

### Commands to add
```
shc backup list <service_id>
    → client.list_backups(service_id)
    → Print table: id, name, created_at, protected, size

shc backup create <service_id> [--name=<name>]
    → client.create_backup(service_id, name)
    → Print backup ID + status

shc backup restore <service_id> <backup_id>
    → client.restore_backup(service_id, backup_id)
    → Print job status

shc backup delete <service_id> <backup_id>
    → client.delete_backup(service_id, backup_id)
    → Print confirmation

shc backup protect <service_id> <backup_id> [--off]
    → client.set_backup_protection(service_id, backup_id, not args.off)
    → Print new protection status

shc backup verify <service_id> <backup_id>
    → client.verify_backup(service_id, backup_id)  [NEW METHOD]
    → POST /vm/{id}/backups/verify
    → Print verification result
```

### Also add missing CLI commands
```
shc snapshot-delete <service_id> <snapshot_id>
    → client.delete_snapshot(service_id, snapshot_id)
    (Currently missing from CLI — method exists in client.py)
```

### E2E Test Procedure
```bash
# 1. Order a test VM (with options → 64s provisioning)
shc order --hostname backup-test --package-id 81 --pricing-id 245 --pay

# 2. Wait for ready
shc list  # Note the service_id

# 3. Create a backup
shc backup create <service_id> --name "pre-test"
# EXPECTED: backup_id returned, status=READY

# 4. List backups
shc backup list <service_id>
# EXPECTED: backup appears with name="pre-test"

# 5. Protect the backup
shc backup protect <service_id> <backup_id>
# EXPECTED: protected=true

# 6. Verify the backup
shc backup verify <service_id> <backup_id>
# EXPECTED: verification result

# 7. Delete the backup
shc backup delete <service_id> <backup_id>
# EXPECTED: deleted confirmation

# 8. Confirm deletion
shc backup list <service_id>
# EXPECTED: empty list

# 9. Cleanup
shc cancel <service_id>
```

### Success Criteria
- All 6 backup commands work against live SHC API
- `shc backup list` output is human-readable table
- `--format=json` flag outputs machine-readable JSON
- Confirmation flow handled automatically (client._confirmed_request)

---

## Phase 2: Pulumi Dynamic Provider (1-2 days)

### Directory structure
```
/Users/macbook/src/shc-pulumi/
    __init__.py
    provider.py          — Pulumi dynamic provider classes
    vm_resource.py       — SHCVMResource (CRUD)
    snapshot_resource.py — SHCSnapshotResource (create, delete)
    backup_resource.py   — SHCBackupResource (create, delete)
    pyproject.toml       — Package metadata
    tests/
        test_vm.py       — E2E: pulumi up → verify → destroy
        test_snapshot.py — E2E: create VM → snapshot → destroy
        test_backup.py   — E2E: create VM → backup → destroy
    examples/
        main.py          — Example Pulumi program
        Pulumi.yaml      — Project config
```

### Provider implementation (`provider.py`)
```python
import pulumi
from shc_toolkit.client import SHCClient

class SHCProviderConfig:
    """Shared config passed to all resource providers."""
    api_key: str
    base_url: str = "https://blesta.sovereignhybridcompute.com/user-api/v2"

class SHCVMProvider(pulumi.dynamic.ResourceProvider):
    """Manages a SHC VPS instance."""

    def __init__(self, config: SHCProviderConfig):
        self._client = SHCClient(api_key=config.api_key)

    def create(self, inputs):
        # submit_order with auto-injected options
        result = self._client.submit_order(
            hostname=inputs["hostname"],
            package_id=inputs["package_id"],
            pricing_id=inputs["pricing_id"],
        )
        service_id = result["service_ids"][0]

        # Wait for provisioning (poll get_vm until ready)
        import time
        for _ in range(60):
            vm = self._client.get_vm(service_id)
            if vm.get("provisioning_state") == "ready":
                break
            time.sleep(5)

        # Apply SSH key if provided
        if inputs.get("ssh_key"):
            self._client.apply_ssh_key_live(service_id, inputs["ssh_key"])

        # Schedule end-of-term cancel if auto_cancel
        if inputs.get("auto_cancel", True):
            self._client.cancel_vm(service_id, immediate=False)

        return pulumi.dynamic.CreateResult(
            id=str(service_id),
            outs={
                "service_id": service_id,
                "hostname": inputs["hostname"],
                "ip": vm.get("ips", [{}])[0].get("ip", ""),
                "os_user": vm.get("os_user", "debian"),
                "status": vm.get("service_status", ""),
            }
        )

    def read(self, id, props):
        service_id = int(id)
        try:
            vm = self._client.get_vm(service_id)
            return pulumi.dynamic.ReadResult(
                id=id,
                props={**props, "ip": vm.get("ips", [{}])[0].get("ip", "")}
            )
        except Exception:
            return pulumi.dynamic.ReadResponse(id=id, props=props)

    def delete(self, id, props):
        self._client.cancel_vm(int(id), immediate=True)

class SHCSnapshotProvider(pulumi.dynamic.ResourceProvider):
    def __init__(self, config: SHCProviderConfig):
        self._client = SHCClient(api_key=config.api_key)

    def create(self, inputs):
        result = self._client.create_snapshot(
            inputs["service_id"],
            name=inputs.get("name")
        )
        return pulumi.dynamic.CreateResult(
            id=result.get("id", result.get("backup_id", "")),
            outs={"service_id": inputs["service_id"], **result}
        )

    def delete(self, id, props):
        self._client.delete_snapshot(props["service_id"], id)
```

### Example Pulumi program (`examples/main.py`)
```python
import pulumi
from shc_pulumi import SHCVMProvider, SHCSnapshotProvider

config = pulumi.Config()
api_key = config.require_secret("shc_api_key")

# Create a VM
vm = pulumi.dynamic.Resource(
    "shc-pulumi-test",
    SHCVMProvider(api_key=api_key),
    pulumi.Output.api_key.apply(lambda k: {
        "hostname": "pulumi-test",
        "package_id": 81,
        "pricing_id": 245,
        "ssh_key": open("/Users/macbook/.ssh/id_rsa.pub").read().strip(),
        "auto_cancel": True,
    }),
)

pulumi.export("vm_ip", vm["ip"])
pulumi.export("vm_hostname", vm["hostname"])
```

### E2E Test Procedure
```bash
# 1. Install Pulumi
brew install pulumi

# 2. Configure secrets
pulumi config set shc_api_key $SHC_API_KEY --secret

# 3. Preview
pulumi preview
# EXPECTED: shows 1 resource to create (shc-pulumi-test)

# 4. Deploy
pulumi up --yes
# EXPECTED: VM provisions in ~64s, outputs show IP + hostname

# 5. Verify the VM exists
shc list
# EXPECTED: pulumi-test VM visible

# 6. Verify SSH works
ssh debian@$(pulumi stack output vm_ip)
# EXPECTED: shell access

# 7. Destroy
pulumi destroy --yes
# EXPECTED: VM cancelled (immediate), credit refunded

# 8. Verify cleanup
shc list
# EXPECTED: VM gone
```

### Success Criteria
- `pulumi up` creates a VM that provisions in <90s
- `pulumi destroy` cancels the VM and gets refund
- Stack outputs include IP, hostname, service_id
- SSH access verified after pulumi up
- VM gone after pulumi destroy
- Works from any Python Pulumi program

---

## Phase 3: Terraform Provider (2-3 days)

### Directory structure
```
/Users/macbook/src/terraform-provider-shc/
    main.go                    — Provider server entry point
    go.mod                     — Go module definition
    provider/
        provider.go            — Provider implementation (schema, configure)
    resources/
        vm_resource.go         — shc_vm resource (Create/Read/Update/Delete)
        snapshot_resource.go   — shc_snapshot resource
        backup_resource.go     — shc_backup resource
    client/
        client.go              — Go HTTP client wrapping SHC API
        types.go               — Go structs for API responses
    docs/
        index.md               — Provider docs
        resources/
            vm.md              — shc_vm docs
            snapshot.md        — shc_snapshot docs
            backup.md          — shc_backup docs
    examples/
        main.tf                — Example Terraform config
    Makefile                   — Build + install targets
    .github/workflows/ci.yml   — CI: build + test + lint
```

### Provider schema
```go
func (p *shcProvider) Schema(ctx context.Context, req provider.SchemaRequest, resp *provider.SchemaResponse) {
    resp.Schema = schema.Schema{
        Attributes: map[string]schema.Attribute{
            "api_key": schema.StringAttribute{Required: true, Sensitive: true},
            "endpoint": schema.StringAttribute{Optional: true},
        },
    }
}
```

### Resource: shc_vm
```hcl
resource "shc_vm" "web" {
  hostname    = "web-prod"
  package_id  = 81
  pricing_id  = 245
  ssh_key     = file("~/.ssh/id_ed25519.pub")
  auto_cancel = true

  # Computed outputs
  # ip          = "66.92.204.236"
  # os_user     = "debian"
  # service_id  = 625
}
```

Go implementation maps to SHC API:
- **Create**: `POST /ordering/submit` → poll `GET /vm/{id}` until ready
- **Read**: `GET /vm/{id}` → extract ip, status, hostname
- **Update**: `PATCH /vm/{id}/upgrade` (machine type change only)
- **Delete**: `POST /vm/{id}/cancel {"immediate": true}`

### Resource: shc_snapshot
```hcl
resource "shc_snapshot" "pre_deploy" {
  service_id = shc_vm.web.service_id
  name       = "pre-deploy-baseline"
}
```

### Resource: shc_backup
```hcl
resource "shc_backup" "daily" {
  service_id = shc_vm.web.service_id
  name       = "daily-backup"
  protected  = true
}
```

### E2E Test Procedure
```bash
# 1. Build the provider
cd /Users/macbook/src/terraform-provider-shc
make install  # installs to ~/.terraform.d/plugins/

# 2. Configure terraform to use local provider
cat > ~/.terraformrc << 'EOF'
provider_installation {
  filesystem_mirror { path = "~/.terraform.d/plugins" }
}
EOF

# 3. Write test config
cat > /tmp/test_shc.tf << 'EOF'
terraform {
  required_providers { shc = { source = "sovereignhybridcompute/shc" } }
}

provider "shc" { api_key = var.shc_api_key }

resource "shc_vm" "test" {
  hostname   = "tf-test"
  package_id = 81
  pricing_id = 245
  auto_cancel = true
}

output "vm_ip"   { value = shc_vm.test.ip }
output "vm_id"   { value = shc_vm.test.service_id }
EOF

# 4. Init + Plan
terraform -chdir=/tmp init
terraform -chdir=/tmp plan -var shc_api_key=$SHC_API_KEY
# EXPECTED: plan shows 1 resource to create

# 5. Apply
terraform -chdir=/tmp apply -var shc_api_key=$SHC_API_KEY -auto-approve
# EXPECTED: VM created, IP output shown

# 6. Verify
shc list
ssh debian@$(terraform -chdir=/tmp output -raw vm_ip)
# EXPECTED: shell access

# 7. Take a snapshot via Terraform
# (add shc_snapshot resource, apply again)

# 8. Destroy
terraform -chdir=/tmp destroy -var shc_api_key=$SHC_API_KEY -auto-approve
# EXPECTED: VM cancelled, snapshot deleted

# 9. Verify cleanup
shc list
# EXPECTED: no VMs
```

### CI Pipeline (`.github/workflows/ci.yml`)
```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - uses: actions/setup-go@v5
      - run: go build ./...
      - run: go vet ./...
      - run: go test ./... -v
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - run: gofmt -l . && [ -z "$(gofmt -l .)" ]
```

### Success Criteria
- `terraform plan` shows VM creation without errors
- `terraform apply` creates a VM that provisions in <90s
- `terraform destroy` cancels VM + deletes snapshots/backups
- State file correctly tracks VM service_id, IP, hostname
- `terraform refresh` updates IP from API
- Works with `terraform import shc_vm.test 625`
- Published to Terraform Registry (optional, requires namespace)

---

## Cross-Phase Documentation Deliverables

### `docs/backup-cli.md`
- Command reference for all 6 backup commands
- Examples for each
- Confirmation flow notes

### `docs/pulumi-provider.md`
- Installation: `pip install shc-pulumi`
- Quick start example
- Resource reference (vm, snapshot, backup)
- Configuration (api_key, endpoint)

### `docs/terraform-provider.md`
- Installation: Registry or local filesystem
- Quick start example
- Resource reference with all attributes
- Import syntax
- State management notes

### `HANDOVER.md` update
- Add IaC integration section
- Document which tools are available for which use cases:
  - CLI users: `shc` / `shc-compute`
  - Python users: `shc_toolkit.client.SHCClient`
  - Pulumi users: `shc-pulumi` package
  - Terraform users: `terraform-provider-shc`
  - gcloud users: `shc-compute compute instances ...`

---

## Execution Order

```
Phase 1 (30 min): Backup CLI
  → Code, test against live VM, commit
  → Deliverable: 6 new CLI commands + snapshot-delete

Phase 2 (1-2 days): Pulumi Provider
  → Depends on: Phase 1 complete (backup methods verified)
  → Code provider.py + vm_resource.py first
  → E2E test: pulumi up → SSH → destroy
  → Add snapshot + backup resources
  → Deliverable: pip-installable shc-pulumi package

Phase 3 (2-3 days): Terraform Provider
  → Depends on: Phase 1+2 complete (API surface fully tested)
  → Code Go HTTP client first (port of Python client)
  → Code provider + vm_resource
  → E2E test: terraform apply → SSH → destroy
  → Add snapshot + backup resources
  → Deliverable: terraform-provider-shc binary + Registry submission
```

Total estimated effort: 3-5 days. Each phase independently useful.
