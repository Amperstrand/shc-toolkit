# Migrating from Google Cloud (gcloud) to SHC

The `shc-compute` CLI provides a drop-in replacement for common `gcloud compute` commands. This guide maps each command to its SHC equivalent and highlights key differences.

## Quick Start

Replace `gcloud` with `shc-compute` in your scripts. Most commands work with the same flags and output formats.

```bash
# Before
gcloud compute instances list --format=json

# After
shc-compute compute instances list --format=json
```

## Authentication

Set your SHC API key as an environment variable:

```bash
export SHC_API_KEY="shc_live_..."
```

## Instance Commands

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `instances create NAME --machine-type=n1-standard-2` | `instances create NAME --machine-type=n1-standard-2` | Creates a Dev VPS VM. Maps n1-standard-2 to pkg 81 |
| `instances list --format=json` | `instances list --format=json` | Lists all VMs in gcloud-compatible format |
| `instances describe NAME --format=json` | `instances describe NAME --format=json` | Shows detailed VM info including power state and firewall rules |
| `instances delete NAME --quiet` | `instances delete NAME --quiet` | Cancels and deletes the VM |
| `instances start NAME` | `instances start NAME` | Powers on a stopped VM |
| `instances stop NAME` | `instances stop NAME` | Powers off a running VM |
| `instances reset NAME` | `instances reset NAME` | Forces a VM reboot (hard reset) |
| `instances add-metadata NAME --metadata=k=v` | `instances add-metadata NAME --metadata=k=v` | Stores metadata locally in `~/.shc-compute/metadata.json` |
| `instances delete-metadata NAME --keys=k` | `instances delete-metadata NAME --keys=k` | Removes metadata entries |

## Snapshot Commands

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `snapshots list --format=json` | `snapshots list --format=json` | Lists all snapshots in gcloud-compatible format |
| `snapshots describe SNAP --format=json` | `snapshots describe SNAP --format=json` | Shows snapshot details |
| `snapshots delete SNAP --quiet` | `snapshots delete SNAP --quiet` | Deletes a snapshot |
| `instances create NAME --source-snapshot=SNAP` | `instances create NAME --source-snapshot=SNAP` | Creates a VM from a snapshot |

**Note:** Create snapshots using the `shc` CLI:

```bash
# Create a snapshot
shc create-snapshot <service_id> --name "pre-deploy"

# Restore from snapshot
shc restore-snapshot <service_id> <snapshot_id>
```

## Firewall Rules

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `firewall-rules list --format=json` | `firewall-rules list --format=json` | Lists firewall rules in gcloud-compatible format |

**Note:** Manage individual firewall rules using the `shc` CLI:

```bash
# List rules for a VM
shc firewall <service_id>

# Add a rule
shc firewall <service_id> --add --protocol tcp --port 22 --action accept

# Remove a rule
shc firewall <service_id> --remove --position 1
```

## SSH Commands

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `ssh NAME --command="whoami"` | `ssh NAME --command="whoami"` | SSH into a VM and run a command |
| `ssh NAME` | `ssh NAME` | Interactive SSH session |

## Machine Types

SHC Dev VPS plans map to Google Compute Engine machine types:

| Machine Type | SHC Package | SHC Pricing | vCPUs | RAM |
|--------------|-------------|-------------|-------|-----|
| n1-standard-2 | 81 | 245 | 2 | 8 GB |
| n1-standard-4 | 82 | 249 | 4 | 16 GB |
| n1-standard-8 | 83 | 253 | 8 | 32 GB |

Custom machine types are not supported. Use one of the predefined types above.

## Images

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `images list --format=json` | `images list --format=json` | Lists available OS templates |

Supported templates include Debian, Ubuntu, Fedora, Arch, NixOS, AlmaLinux, Alpine, Devuan, and OpenBSD.

## Config

| gcloud compute | shc-compute | Notes |
|---------------|-------------|-------|
| `config get-value project` | `config get-value project` | Returns "shc" (project name) |

## Output Formats

`shc-compute` supports the same output formats as `gcloud`:

- `--format=json` - JSON output (default)
- `--format=value(field)` - Extract a single field
- `--format=get(field)` - Get a nested field

```bash
# Get all VM IPs
shc-compute compute instances list --format=value(networkInterfaces[0].accessConfigs[0].natIP)

# Get first VM status
shc-compute compute instances list --format=get([0].status)
```

## Filtering

Filter VMs by metadata:

```bash
# Filter by metadata
shc-compute compute instances list --filter="metadata.env=production"

# Filter by name
shc-compute compute instances list --filter="name:web-*"
```

## Key Differences

1. **Single region**: SHC operates in Katy, Texas only. There are no zones or regions to specify.

2. **No persistent disks**: VMs come with local NVMe storage. Use snapshots for backups.

3. **No load balancers**: Use a reverse proxy like Caddy or Nginx on a VM instead.

4. **No instance groups**: Scale VMs manually using the CLI or API.

5. **Metadata storage**: Metadata is stored locally in `~/.shc-compute/metadata.json` rather than on the VM.

6. **Hourly proration**: You're charged the full daily rate upfront but refunded for unused hours on cancel (minimum 1 hour). A 2-hour CI run costs pennies, not a full day.

7. **No VPC networking**: Each VM has a single public IP with firewall rules managed at the VM level.

## Example Workflow

```bash
# Set up environment
export SHC_API_KEY="shc_live_..."

# List existing VMs
shc-compute compute instances list --format=json

# Create a new VM
shc-compute compute instances create my-app \
  --machine-type=n1-standard-2 \
  --metadata=env=production,app=web \
  --tags=web-server

# Add metadata
shc-compute compute instances add-metadata my-app --metadata=owner=alice

# Get VM details
shc-compute compute instances describe my-app --format=json

# SSH into the VM
shc-compute compute ssh my-app --command="sudo apt update"

# List snapshots
shc-compute compute snapshots list --format=json

# Stop the VM
shc-compute compute instances stop my-app

# Start the VM
shc-compute compute instances start my-app

# Delete the VM
shc-compute compute instances delete my-app --quiet
```

## Unsupported Commands

The following `gcloud compute` commands are not supported:

- `instances attach-disk` - No persistent disks
- `instances detach-disk` - No persistent disks
- `instances set-disk-auto-delete` - No persistent disks
- `firewall-rules create` - Use `shc firewall` instead
- `firewall-rules delete` - Use `shc firewall --remove` instead
- `addresses create` - Each VM gets a public IP automatically
- `addresses delete` - Public IP is deleted with the VM
- `networks create` - No VPC networking
- `subnets create` - No VPC networking
- `target-pools create` - No load balancers
- `health-checks create` - No load balancers
- `instance-groups create` - No instance groups
- `instance-templates create` - No instance templates

## Migration Checklist

Before migrating from Google Cloud to SHC:

1. Identify all machine types in use and map them to SHC packages
2. Export VM metadata from Google Cloud and import to `~/.shc-compute/metadata.json`
3. Set up snapshots as replacements for persistent disks
4. Refactor scripts that use load balancers to use reverse proxies
5. Update CI/CD pipelines to use `shc-compute` instead of `gcloud compute`
6. Test SSH access and firewall rules after migration
7. Update monitoring and alerting to account for daily billing minimum

## Next Steps

- Read the [main README](../README.md) for complete shc-toolkit documentation
- Explore the [SHC API docs](https://blesta.sovereignhybridcompute.com/user-api/docs/)
- Try the `shc` CLI for additional features not available in `shc-compute`