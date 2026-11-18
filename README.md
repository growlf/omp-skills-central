# OMP Skills Central

Central skills repo for the team. Includes:
- **Team-created skills** (skills/)
- **Curated community skills** (skills/)
- **Plugins with code** (plugins/)
- **Community skill sources** (curated/)

## Quick Install

```bash
# Run once per machine
git clone <repo-url> ~/.omp/central-skills
cd ~/.omp/central-skills
./setup.sh
```

## Skills

| Skill | Source | Description |
|-------|--------|-------------|
| bitwarden | Team | Bitwarden vault management via MCP tools |
| credential-mgmt | Team | Vault session management and credential lifecycle |

## Adding Skills

1. Add a new directory under `skills/<name>/SKILL.md`
2. Commit and push
3. Team members run `./setup.sh`

## Adding Community Skills

Copy from the internet → add to `skills/` → commit. Document sources in `curated/`.
