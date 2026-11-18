---
name: bitwarden
description: "Manage Bitwarden vault items for BMS IT automation - search, create, update, delete credentials, generate passwords, manage organizations. Use for: bitwarden, vault, credential, password, secret, organization, collection, folder"
mode: skill
triggers: bitwarden,vault,credential,password,secret,organization,collection,folder,lookup,search vault
---

# Bitwarden Vault Management

Use the **bitwarden MCP server** (`mcp__bitwarden__*` tools) for all vault operations. This skill provides the workflow for BMS IT credential management.

## Quick Reference

| Tool | Purpose |
|---|---|
| `mcp__bitwarden__list` | Search/list vault items |
| `mcp__bitwarden__get` | Get item details (by ID or search) |
| `mcp__bitwarden__create_item` | Create new vault item |
| `mcp__bitwarden__edit_item` | Update existing item |
| `mcp__bitwarden__delete` | Remove item |
| `mcp__bitwarden__generate` | Generate secure passwords/passphrases |
| `mcp__bitwarden__sync` | Sync vault from server |

## Common Workflows

### Search for a vault item
```
mcp__bitwarden__list(type="items", search="<search term>")
```

### Get item details
```
mcp__bitwarden__get(object="item", id="<item ID or search term>")
```

### Create a login item
```
mcp__bitwarden__create_item(
  name="<name>",
  type=1,
  login={
    username="<username>",
    password="<password>",
    uris=[{uri: "https://example.com"}]
  },
  notes="<notes>",
  folderId="<folder-id>",
  organizationId="<org-id>",
  collectionIds=["<collection-id>"]
)
```

### Generate a secure password
```
mcp__bitwarden__generate(
  length=24,
  uppercase=true,
  lowercase=true,
  number=true,
  special=true
)
```

### Update an item's password
```
mcp__bitwarden__edit_item(
  id="<item-id>",
  login={password: "<new-password>"}
)
```

## BMS IT Organization

- **Org ID**: `f8a8b00f-496a-44d3-b9d6-5ed28ecd95a3` (BMS)
- **Collection (Critical Infra/High Sec)**: `70868edb-2554-4e54-aeb1-8aa840217501`
- **Folder (automation-only)**: `6e373864-9fe4-4052-8874-73debb260f42`

## Session Management

The session is auto-resolved from `~/.cache/opskit/bw-session`. If locked:
1. Run `bwunlock.sh` to refresh
2. Or manually: `bw unlock --raw > ~/.cache/opskit/bw-session`

## Do NOT

- Store vault session tokens in output or logs
- Hardcode passwords from vault lookups - use MCP tools
- Modify the session file directly
