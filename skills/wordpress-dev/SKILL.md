---
name: wordpress-dev
description: "WordPress site administration via WP-CLI: plugin/theme/core management, configuration, debugging, and troubleshooting. Use for WP-CLI operations, site configuration, plugin conflicts, debug logging, and WP admin debugging. Triggers: wp, wp-cli, wordpress-admin, wordpress-debug, wp-admin, wp-content, wordpress-site."
metadata:
  version: "0.0.0"
  mode: skill
---
# WordPress Development & Administration (WP-CLI)

## Running WP-CLI

**Via Docker (BMS):**
```bash
docker compose exec -T apache wp --path=/var/www/html
```

For members site:
```bash
docker compose exec -T apache wp --path=/var/www/html/members
```

## Core Workflows

### Site Information
```bash
docker compose exec -T apache wp core version --allow-root
docker compose exec -T apache wp option get siteurl --allow-root
docker compose exec -T apache wp plugin list --status=all --format=json
```

### Plugin Management
```bash
docker compose exec -T apache wp plugin update --all --allow-root
docker compose exec -T apache wp plugin activate memberpress --allow-root
docker compose exec -T apache wp plugin deactivate wordfence --allow-root
docker compose exec -T apache wp transient delete-all --allow-root
```

### Database Operations
```bash
docker compose exec -T apache wp db export /tmp/backup.sql --allow-root
docker compose exec -T apache wp db import /tmp/backup.sql --allow-root
# Always dry-run search-replace first
docker compose exec -T apache wp search-replace 'http://old' 'http://new' --dry-run --allow-root
docker compose exec -T apache wp search-replace 'http://old' 'http://new' --allow-root
```

### Debugging
```bash
# Enable WP debug logging
docker compose exec -T apache wp config set WP_DEBUG true --allow-root
docker compose exec -T apache wp config set WP_DEBUG_LOG true --allow-root

# Check logs
docker compose logs apache | tail -50

# WooCommerce debugging
docker compose exec -T apache wp wc status --allow-root
```

## BMS-Specific Patterns

### Two Sites
- **Main:** `bms-main.local` → `sites/main/` → DB: `bms_main`
- **Members:** `bms-members.local` → `sites/main/members/` → DB: `bms_members`

### Common Issues
1. **WP-CLI fails** — always use `--allow-root` in Docker, and `--path` for the correct site
2. **500 errors** — deactivate all plugins first, then reactivate one by one
3. **WooCommerce cart issues** — flush transients and cache
4. **MemberPress issues** — check logs in WP admin → MemberPress → Logs

## Gotchas

- **Never run bare `wp` without `--allow-root` in Docker**
- **WP-CLI in Docker** always needs `--path` to point to the correct site
- **Search-replace is destructive** — always `--dry-run` first
- **Plugin conflicts** — deactivate recently activated plugins first
