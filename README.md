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
| ai-framework | Community | AI framework integration and scaffolding |
| bitwarden | Team | Bitwarden vault management via MCP tools |
| credential-mgmt | Team | Vault session management and credential lifecycle |
| data | Community | Data processing and analysis workflows |
| development | Community | Development workflow and coding patterns |
| devops | Community | DevOps automation and infrastructure |
| documentation | Community | Documentation workflows, KB management |
| documents | Community | Document generation and management |
| extensions | Community | Extension development and configuration |
| github | Community | GitHub workflow: CLI, PRs, issue tracking |
| infra | Community | Infrastructure management and deployment |
| luanti | Community | Luanti (Minecraft-like) game development |
| manager | Community | Project management and coordination |
| media | Community | Media processing and generation |
| ops | Community | Operations and monitoring |
| project-lifecycle | Community | Project lifecycle management |
| reconcile-issues | Community | Issue reconciliation workflows |
| researcher | Community | Research and investigation workflows |
| search | Community | Search and discovery patterns |
| selector | Community | Selection and filtering patterns |
| task-mgmt | Community | Task management and delegation |
| web | Community | Web development and deployment |

## Adding Skills

1. Add a new directory under `skills/<name>/SKILL.md`
2. Commit and push
3. Team members run `./setup.sh`

## Adding Community Skills

Copy from the internet → add to `skills/` → commit. Document sources in `curated/`.
