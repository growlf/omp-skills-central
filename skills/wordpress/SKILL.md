---
name: wordpress
description: "WordPress site administration, development, and troubleshooting. Covers WP-CLI operations, plugin/theme management, database operations, Docker Compose stacks, backup/restore, and debugging. Bilingual: speaks English and French."
metadata:
  version: "0.0.0"
  mode: subagent
  triggers: wordpress, wp-cli, wordpress-admin, wordpress-debug, wp-admin, wp-content, wordpress-site, wordpress-stack
---
# WordPress Generalist

> **Scope:** Site administration, development, and troubleshooting. For **plugin development** (building WP plugins to publish), use the `wp-dev-skills` collection.

This generalist orchestrates three sub-skills:

| Sub-skill | Handles |
|-----------|---------|
| **wordpress-dev** | WP-CLI operations, plugin/theme management, core updates, site configuration, debugging |
| **mariadb** | MariaDB/MySQL operations — backup/restore, repair, optimization, schema changes, query tuning |
| **docker-compose** | Docker Compose management — stack up/down, networking, volumes, logs, troubleshooting |

## When to use

- "How do I fix this WordPress error?"
- "Update all WordPress plugins"
- "Backup/restore the database"
- "Why is my Docker stack not starting?"
- "Debug slow WooCommerce endpoints"
- "Install/activate a WordPress plugin"
- "Fix WP-CLI permission issues"

## Always start by asking

1. **Which site?** (main or members — BMS has two WordPress sites)
2. **Local or production?** (local Docker stack vs Tigertech remote)
3. **What's the error or goal?** (be specific)

## Key principles

- **WP-CLI is the primary interface** — almost everything can be done via `wp` commands
- **Never run bare `wp` without the wrapper** — it won't work in Docker/LocalWP environments
- **Always backup before destructive operations** (core updates, major plugin updates)
- **Check the stack health first** — `docker compose ps` before debugging site issues
- **BMS has two sites:** `bms-main.local` (main) and `bms-members.local` (members with WooCommerce)

## External references

- [WP-CLI Handbook](https://developer.wordpress.org/cli/commands/)
- [WordPress Developer Handbook](https://developer.wordpress.org/themes/)
- [WooCommerce Hooks Reference](https://woocommerce.github.io/woocommerce-rest-api/)
