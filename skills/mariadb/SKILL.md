---
name: mariadb
description: "MariaDB/MySQL database operations for WordPress sites: backup/restore, repair, optimization, schema changes, query tuning, and user management. Use for database health checks, import/export, table optimization, and troubleshooting slow queries. Triggers: database, db, mariadb, mysql, wp-db, database-operations, db-repair, db-backup, db-restore."
metadata:
  version: "0.0.0"
  mode: skill
---
# MariaDB/MySQL Database Operations

## Running MySQL/MariaDB

**Via Docker (BMS):**
```bash
docker compose exec mariadb mariadb -u root -e "SHOW DATABASES;"
docker compose exec mariadb mysqldump -u root bms_members > /tmp/backup.sql
```

## Core Workflows

### Backup and Restore
```bash
# Full DB backup (compressed)
docker compose exec mariadb mysqldump -u root bms_members | gzip > /tmp/bms_members_$(date +%Y%m%d).sql.gz

# Restore
gunzip -c /tmp/bms_members_*.sql.gz | docker compose exec -T mariadb mariadb -u root bms_members
```

### Repair and Optimization
```bash
docker compose exec mariadb mariadb -u root -e "CHECK TABLE bms_members.wp_posts;"
docker compose exec mariadb mariadb -u root -e "REPAIR TABLE bms_members.wp_posts;"
```

### Large Table Analysis (BMS members has ~150 tables, 69MB)
```bash
# Find largest tables
docker compose exec mariadb mariadb -u root -e "SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb FROM information_schema.tables WHERE table_schema = 'bms_members' ORDER BY total DESC LIMIT 20;"

# Count orphaned post meta
docker compose exec mariadb mariadb -u root -e "SELECT COUNT(*) FROM bms_members.wp_postmeta pm LEFT JOIN bms_members.wp_posts p ON pm.post_id = p.ID WHERE p.ID IS NULL;"
```

## BMS-Specific

| Database | Tables | Size | Purpose |
|----------|--------|------|---------|
| `bms_main` | ~27 | ~5 MB | Main site |
| `bms_members` | ~150 | ~69 MB | Members (MemberPress + WooCommerce + Wordfence + Ninja Forms) |

## Gotchas

- Always use `--single-transaction` for InnoDB backups
- Never delete from `wp_options` — contains critical configuration
- MariaDB 11.4 default engine is InnoDB (supports transactions)
