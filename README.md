# OMP Skills Central

Central skills repo for the team. Consolidated from:
- ~/Projects/AI (main AI project)
- ~/Projects/lfnw (LFNW event site project)
- ~/Projects/opskit (Opskit tooling)

## Quick Install

```bash
git clone git@github.com:growlf/omp-skills-central ~/.omp/central-skills
cd ~/.omp/central-skills
./setup.sh
```

## Skills (97 total)

### Security & Secrets
| Skill | Source | Description |
|-------|--------|-------------|
| bitwarden | AI | Bitwarden vault management via MCP tools |
| bwunlock | AI | Bitwarden unlock and session management |
| credential-mgmt | AI | Vault session management and credential lifecycle |
| security | AI | Security auditing and vulnerability scanning |

### Dev & Code
| Skill | Source | Description |
|-------|--------|-------------|
| ai-framework | AI | Azure AI Foundry platform integration |
| development | AI+LFNW | General code helpers, cleanup, triage, code review |
| django | AI+LFNW | Django web development and deployment |
| django-dev-env | AI | Django development environment setup |
| django-expert | AI | Django expert-level guidance |
| djangocms-agent | AI | DjangoCMS agent workflow |
| djangocms-reviewer | AI | DjangoCMS code review |
| openspec-* | AI | OpenSpec workflow (8 skills: apply, archive, bulk-archive, continue, explore, ff, new, onboard, sync-specs, verify) |
| cleanup | AI | Branch and worktree cleanup |
| grind | AI | Code grinding and refactoring |
| triage | AI | Issue triage and prioritization |
| review | AI | Code review workflows |
| mr-review | AI | Merge request review |
| cmake | AI | CMake build system |
| docker-compose | AI | Docker Compose management |

### DevOps & Infra
| Skill | Source | Description |
|-------|--------|-------------|
| devops | AI+LFNW | CI/CD, Git workflows, project lifecycle |
| infra | AI+LFNW | Infrastructure operations, Proxmox VE |
| ops | AI+LFNW | Operations and monitoring |
| ansible | AI | Ansible automation |
| backup | AI | Backup schedules and recovery |
| baseline | AI | System baseline capture |
| check-connectivity | AI | Network connectivity probing |
| infra-placement | AI | Infrastructure placement planning |
| proxmox | AI | Proxmox VM management |
| proxmox-cli | AI | Proxmox CLI operations |
| routeros | AI | MikroTik RouterOS management |
| mikrotik | AI | MikroTik network management |
| technitium | AI | Technitium DNS management |
| zabbix | AI | Zabbix monitoring |
| lifecycle | AI | System lifecycle management |
| mail-auth-check | AI | Email authentication checking |
| grouchys-diner-monitor | OPCODE | Grouchys Diner infrastructure monitoring |

### Documentation
| Skill | Source | Description |
|-------|--------|-------------|
| documentation | AI+LFNW | Documentation workflows, KB management |
| documents | AI | Document file format creation/editing |
| doc-coauthoring | AI | Collaborative document creation |
| knowledge-base | AI | Knowledge base management |
| handoff | AI | Task state handoff |
| templates | AI | Documentation templates |
| release | AI | Release documentation |
| docx | AI | Microsoft Word documents |
| xlsx | AI | Microsoft Excel spreadsheets |
| pptx | AI | Microsoft PowerPoint presentations |
| pdf | AI | PDF processing |
| google-workspace | AI | Google Workspace documents |

### GitHub & Git
| Skill | Source | Description |
|-------|--------|-------------|
| github | AI+LFNW | GitHub workflow, PR management |
| gh | AI | GitHub CLI operations |
| github-cli | AI | GitHub CLI for all GitHub work |
| git | AI | Git workflow |
| gitlab-pages-dns | AI | GitLab Pages DNS integration |
| reconcile-issues | AI | Issue reconciliation workflows |

### Project Management
| Skill | Source | Description |
|-------|--------|-------------|
| manager | AI | Project management and coordination |
| task-mgmt | AI+LFNW | Task management and delegation |
| project-lifecycle | AI | Project lifecycle management |
| discovery | AI | Project discovery and scoping |
| startsession | AI | Session lifecycle start |
| endsession | AI | Session lifecycle end |
| dogfood-cycle | AI | Internal testing cycles |
| vikunja-ticket | AI | Vikunja ticket management |
| vikunja-user | AI | Vikunja user management |

### Research & Search
| Skill | Source | Description |
|-------|--------|-------------|
| researcher | AI | Agent/skill research and evaluation |
| research | AI | General research workflows |
| search | AI | Web search and information retrieval |
| find-skills | AI | Skill discovery and management |

### Data & Files
| Skill | Source | Description |
|-------|--------|-------------|
| data | AI | Data management, pipelines, databases |
| mariadb | AI | MariaDB database management |

### Media & Web
| Skill | Source | Description |
|-------|--------|-------------|
| web | AI+LFNW | Web application development |
| media | AI | Media processing and generation |
| web-preview | AI | Web preview and testing |
| websearch | AI | Web search integration |
| visual-regression | LFNW | Visual regression testing |
| lfnw-linkedin-photo | LFNW | LinkedIn photo management for LFNW |
| venue | LFNW | Event venue management |
| sponsors | LFNW | Event sponsor management |
| homepage-ctas | LFNW | Homepage call-to-action management |
| featured-speakers | LFNW | Event speaker management |

### AI & ML
| Skill | Source | Description |
|-------|--------|-------------|
| microsoft-foundry | AI | Microsoft Foundry integration |

### Extensions
| Skill | Source | Description |
|-------|--------|-------------|
| extensions | AI | Extension management and wiring |
| selector | AI | Agent recommendation for projects |
| shared-browser | AI | Collaborative browser control |

### Utilities
| Skill | Source | Description |
|-------|--------|-------------|
| skills | AI | Skills reference and management |
| tools | AI | General utility tools |
| luanti | AI | Luanti (Minecraft-like) game server management |

## Adding Skills

1. Add a new directory under `skills/<name>/SKILL.md`
2. Commit and push
3. Team members run `./setup.sh`

## Merge Notes

Skills that exist in multiple sources are merged to combine the best content from each source. See `merges/` for comparison reports.

## Inventory

See `inventory.md` for the full skill inventory with sources and status.
