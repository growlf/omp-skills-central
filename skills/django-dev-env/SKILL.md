---
name: django-dev-env
description: "Self-contained Docker dev environment management for any Django project. Queries user for project values on first run, then stores them in .env for subsequent use."
metadata:
  version: "0.0.0"
  mode: skill
  triggers: /django-dev-env,django dev,django dev-env,docker dev,django environment
---
# Django Dev Environment

You are the **Django dev environment** expert. You manage Docker-based Django
development workflows for **any** project. You do NOT depend on project-specific
scripts — you implement the full lifecycle yourself using docker-compose,
PostgreSQL management, and Django management commands.

## First-Run Setup

When the user runs `/django-dev-env` for the first time (no `.env` or missing
required values), you MUST query the user for each value before proceeding.

**Values to collect (with defaults):**

| Value | Default | Description |
|-------|---------|-------------|
| `COMPOSE_PROJECT_NAME` | `django-dev` | Docker compose project name |
| `DEV_PORT` | `8880` | Port the dev server listens on |
| `DB_NAME` | `dev_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | (prompt) | PostgreSQL password |
| `DB_HOST` | `db` | PostgreSQL hostname (usually the compose service name) |
| `DJANGO_APP_CONTAINER` | `app` | Django app container service name |
| `DJANGO_DB_CONTAINER` | `db` | PostgreSQL container service name |
| `DJANGO_SETTINGS_MODULE` | `project.settings.dev` | Django settings module |
| `COMPOSE_DEV_FILE` | `docker-compose.dev.yml` | Dev compose file name |

**How to collect:**
```python
# Check if .env exists and has all values
from pathlib import Path
env_path = Path(".env")

if not env_path.exists():
    missing = []
else:
    env_content = env_path.read_text()
    env_vars = {}
    for line in env_content.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            env_vars[key.strip()] = value.strip().strip("'\"")
    missing = [k for k in REQUIRED_VARS if k not in env_vars]

if missing:
    # Ask user for each missing value with a default suggestion
    # Then write/update .env file
```

**Ask the user like:**
```
I'll set up Django dev environment for this project. Here are the values I need:

1. COMPOSE_PROJECT_NAME (default: django-dev) → ?
2. DEV_PORT (default: 8880) → ?
3. DB_PASSWORD → ? (required, no default)
4. DJANGO_DB_CONTAINER (default: db) → ?
...
```

After collecting all values, write them to `.env` and confirm.

**Also ensure `backups/` and `clone-prod-*` are git-ignored:**
```python
gitignore = Path(".gitignore")
gitignore_content = gitignore.read_text() if gitignore.exists() else ""
for pattern in ["backups/", "clone-prod-*"]:
    if pattern not in gitignore_content:
        gitignore.write_text(gitignore_content + f"\n# /django-dev-env skill\n{pattern}",
                            mode="a")
        print(f"Added {pattern} to .gitignore")
```

## Commands

The skill responds to these patterns:

- `/django-dev-env start` — Build and start the dev stack
- `/django-dev-env stop` — Stop the dev stack
- `/django-dev-env start --wipe` — Stop, wipe volumes, rebuild, restore from backup
- `/django-dev-env backup` — Backup database and media
- `/django-dev-env restore <path>` — Restore from backup
- `/django-dev-env health` — Check if dev stack is healthy
- `/django-dev-env logs [--tail N]` — Show container logs
- `/django-dev-env status` — Show running containers and health
- `/django-dev-env migrate` — Run Django migrations
- `/django-dev-env` (no args) — Show status + summary

If the user just says "start dev", "bring up the dev server", etc., treat it as `start`.

## Core Workflows

### Build and Start Dev Stack

```python
import subprocess
from pathlib import Path

env = Path(".env")
if not env.exists():
    print("Run /django-dev-env first to configure the environment.")
    return

# Parse .env
env_vars = {}
for line in env.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, _, value = line.partition("=")
        env_vars[key.strip()] = value.strip().strip("'\"")

compose_file = env_vars.get("COMPOSE_DEV_FILE", "docker-compose.dev.yml")
project = env_vars["COMPOSE_PROJECT_NAME"]
app = env_vars["DJANGO_APP_CONTAINER"]
db = env_vars["DJANGO_DB_CONTAINER"]

def run(*cmd, check=True):
    subprocess.run(cmd, check=check, capture_output=True, text=True)

# Build and start
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "up", "-d", "--build")
```

**Compose files to look for** (in order of preference):
1. `docker-compose.yml` + `docker-compose.dev.yml` (separate dev overrides)
2. `docker-compose.dev.yml` (single compose file with dev config)
3. `docker-compose.yml` (single compose file)

### Stop Dev Stack

```python
# Stop (keep volumes)
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "down")

# Stop and remove volumes (DESTRUCTIVE — confirm with user first)
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "down", "--volumes")
```

### Wipe and Rebuild (dev-up equivalent)

```python
# 1. Stop and destroy volumes
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "down", "--volumes")

# 2. Find latest backup across all sources
# Sources: backups/ (docker-backup.sh), clone-prod-*/ (clone-from-prod.sh)
def find_latest_backup():
    """Find most recent backup across all types (docker-backup, clone-prod, etc.)"""
    if not Path("backups").is_dir():
        return None
    # Filter to valid backup dirs (have a db file)
    candidates = [d for d in Path("backups").iterdir()
                  if d.is_dir()
                  and any(p.name.endswith(".sql") or p.name.endswith(".sql.gz") for p in d.iterdir())]
    return sorted(candidates)[-1] if candidates else None

backup_dir = find_latest_backup()
if not backup_dir:
    print("No backup found. Run /django-dev-env backup or clone-from-prod.sh first.")
    return

# Detect backup format: clone-prod uses gzipped DB, docker-backup uses plain
db_file = backup_dir / "db.sql"  # plain from docker-backup.sh
db_gz_file = backup_dir / "db.sql.gz"  # gzipped from clone-from-prod.sh
db_dump = db_gz_file if db_gz_file.exists() else db_file
media_archive = backup_dir / "media.tar.gz"  # only in clone-prod-*

# 3. Start database only
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "up", "-d", db)

# 4. Create/restore database
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "exec", db,
    "psql", "-U", env_vars["DB_USER"], "-c",
    f"CREATE DATABASE {env_vars['DB_NAME']}",
    check=False)  # may already exist

# Restore database (handle .sql and .sql.gz formats)
if db_gz_file.exists():
    # clone-prod-* format: gzipped
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "exec", db,
        "sh", "-c", f"gunzip -c /tmp/db.sql.gz | psql -U {env_vars['DB_USER']} {env_vars['DB_NAME']}")
    # Upload gzipped file to container
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "cp", str(db_gz_file), f"{db}:/tmp/db.sql.gz")
else:
    # docker-backup.sh format: plain text
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "exec", db,
        "psql", "-U", env_vars["DB_USER"], env_vars["DB_NAME"],
        "<", str(db_dump))

# 5. Start app
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "up", "-d", app, "--build")

# 6. Run migrations
run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "exec", app,
    "python", "manage.py", "migrate")

# 7. Restore media (if exists)
if media_archive.exists():
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "cp",
        f"{backup_dir}/media.tar.gz", f"{app}:/tmp/media.tar.gz")
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "exec", app,
        "sh", "-c", "rm -rf /app/media/* && tar -xzf /tmp/media.tar.gz -C /app/media/ && rm /tmp/media.tar.gz")
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "exec", app,
        "chown", "-R", "www-data:www-data", "/app/media")

# 8. Wait for healthy
import time
for i in range(48):  # up to 4 minutes (48 × 5s)
    result = run("docker", "inspect", "-f",
                 "{{.State.Health.Status}}",
                 f"{project}_{app}_1")
    if "healthy" in result.stdout:
        print(f"Dev server ready: http://localhost:{env_vars['DEV_PORT']}")
        break
    time.sleep(5)
else:
    print("Dev server did not become healthy. Check logs:")
    print(f"  docker compose -p {project} -f {compose_file} logs --tail 50 {app}")
```

### Backup

```python
import subprocess
from datetime import datetime
from pathlib import Path

backup_dir = Path("backups") / datetime.now().strftime("%Y%m%dT%H%M%SZ")
backup_dir.mkdir(parents=True)

# Dump database
subprocess.run(["docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "exec", db,
    "pg_dump", "-U", env_vars["DB_USER"], env_vars["DB_NAME"]],
    stdout=open(backup_dir / "db.sql", "w"), check=True)

# Archive media
subprocess.run(["docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "exec", app,
    "tar", "-czf", "/tmp/media.tar.gz", "-C", "/app/media", "."],
    check=True)
subprocess.run(["docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "cp",
    f"{app}:/tmp/media.tar.gz", str(backup_dir / "media.tar.gz")],
    check=True)
subprocess.run(["docker", "compose", "-p", project, "-f", "docker-compose.yml",
    "-f", compose_file, "exec", app,
    "rm", "/tmp/media.tar.gz"],
    check=True, capture_output=True)

# Secure permissions
backup_dir.chmod(0o700)
(backup_dir / "db.sql").chmod(0o600)
(backup_dir / "media.tar.gz").chmod(0o600)

print(f"Backup saved to: {backup_dir}")
```

### Restore

```python
def restore(backup_path: str):
    backup_dir = Path(backup_path)
    db_dump = backup_dir / "db.sql"
    media_archive = backup_dir / "media.tar.gz"

    if not db_dump.exists():
        print(f"Error: {db_dump} not found")
        return

    # Stop app
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "stop", app)

    # Restore database
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "exec", db,
        "psql", "-U", env_vars["DB_USER"], env_vars["DB_NAME"],
        "<", str(db_dump))

    # Restore media
    if media_archive.exists():
        run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
            "-f", compose_file, "cp",
            str(backup_dir / "media.tar.gz"), f"{app}:/tmp/media.tar.gz")
        run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
            "-f", compose_file, "exec", app,
            "sh", "-c", "rm -rf /app/media/* && tar -xzf /tmp/media.tar.gz -C /app/media/ && rm /tmp/media.tar.gz")
        run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
            "-f", compose_file, "exec", app,
            "chown", "-R", "www-data:www-data", "/app/media")

    # Start app
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "up", "-d", app)

    print("Restore complete")
```

### Health Check

```python
def health_check():
    app = env_vars["DJANGO_APP_CONTAINER"]
    status = run("docker", "inspect", "-f", "{{.State.Health.Status}}",
                 f"{project}_{app}_1").stdout.strip()
    if status == "healthy":
        print(f"Dev server healthy: http://localhost:{env_vars['DEV_PORT']}")
    else:
        print(f"Dev server status: {status}")
        print(f"Recent logs: docker compose -p {project} -f {compose_file} logs --tail 20 {app}")
```

### Status

```python
def status():
    run("docker", "compose", "-p", project, "-f", "docker-compose.yml",
        "-f", compose_file, "ps")
    health_check()
```

## When to Delegate

| Task | Delegate to |
|------|-------------|
| Production deployment | `ops` agent |
| System administration | `ops` agent |
| CI/CD pipeline | `devops` agent |

## When to Use Django-Expert Instead

| Task | Delegate to |
|------|-------------|
| Writing Django models/views/APIs | `django-expert` skill |
| Django CMS plugin development | `djangocms-agent` skill |
| ORM query optimization | `django-expert` skill |
