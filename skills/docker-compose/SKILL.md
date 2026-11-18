---
name: docker-compose
description: "Docker Compose management for local WordPress stacks: stack up/down/restart, networking, volumes, logging, troubleshooting, and container debugging. Use for Docker Compose operations, stack health checks, and container-level debugging. Triggers: docker, docker-compose, compose, container, container-debug, docker-health, docker-logs, docker-network, docker-volume."
metadata:
  version: "0.0.0"
  mode: skill
---
# Docker Compose Management

## BMS Stack Layout

```
~/Projects/BMS/docker/docker-compose.yml
├── Apache (WordPress sites on port 8083)
├── MariaDB (database, internal only)
└── Adminer (DB admin on port 8082)
```

## Core Workflows

### Stack Management
```bash
cd ~/Projects/BMS/docker

# Start
docker compose up -d

# Stop
docker compose down

# Restart a service
docker compose restart apache

# View status
docker compose ps
```

### Logging
```bash
docker compose logs -f apache
docker compose logs -f mariadb
```

### Exec Into Containers
```bash
docker compose exec apache bash
docker compose exec -T apache wp --info --allow-root
```

### Volume Management
```bash
# Check data dir size
du -sh docker/data/

# Backup volume data
tar czf /tmp/docker-data.tar.gz -C docker/data .
```

### Rebuilding (NUKE AND REBUILD — DANGEROUS)
```bash
docker compose down -v
rm -rf docker/data/*
docker compose up -d
```

## BMS-Specific

### Ports
| Service | Port |
|---------|------|
| Apache/WordPress | 8083 |
| Adminer | 8082 |

### Vhosts
- `bms-main.local:8083` → main site
- `bms-members.local:8083` → members site

Add to `/etc/hosts` if needed:
```bash
echo "127.0.0.1 bms-main.local bms-members.local" | sudo tee -a /etc/hosts
```

## Common Issues

1. **Port already in use** — `lsof -i :8083` to check
2. **MariaDB not starting** — check data dir: `docker compose logs mariadb`
3. **Apache 502/503** — check if WordPress files exist in the volume
4. **Slow performance** — `docker stats --no-stream`, check resource limits
5. **Volume permissions** — `docker compose exec apache chown -R www-data:www-data /var/www/html/wp-content`

## Gotchas

- **Docker memory** — at least 4GB RAM for WordPress + MariaDB
- **Volume permissions** — Linux requires `www-data:www-data` ownership
- **`docker compose down -v`** deletes ALL volume data!
- **Log growth** — Docker logs can fill disk over time
