# Skill Inventory

This file documents all skills found across the three project sources,
their locations, and merge decisions.

## Source Locations

| Source | Path | Description |
|--------|------|-------------|
| AI | ~/Projects/AI | Main AI project (non-worktrees) |
| AI-WT | ~/Projects/AI/.wt/* | Worktree clones (duplicates) |
| LFNW | ~/Projects/lfnw | LFNW event site project |
| OPCODE | ~/Projects/opskit | Opskit tooling project |
| Central | ~/Projects/omp-skills-central | Our central repo (target) |

## Skill Catalog

| # | Name | Source(s) | Best Source | Status |
|---|------|-----------|-------------|--------|
| 1 | ai-framework | AI, Central | AI | ✓ In Central |
| 2 | ansible | AI | AI | New |
| 3 | backup | AI | AI | New |
| 4 | baseline | AI | AI | New |
| 5 | bitwarden | AI, Central | AI | ✓ In Central |
| 6 | bwunlock | AI | AI | New |
| 7 | check-connectivity | AI | AI | New |
| 8 | cleanup | AI | AI | New |
| 9 | cmake | AI | AI | New |
| 10 | data | AI, Central | AI | ✓ In Central |
| 11 | devops | AI, LFNW, Central | AI | ✓ In Central |
| 12 | development | AI, LFNW, Central | AI | ✓ In Central |
| 13 | discovery | AI | AI | New |
| 14 | doc-coauthoring | AI | AI | New |
| 15 | docx | AI | AI | New |
| 16 | docker-compose | AI | AI | New |
| 17 | dogfood-cycle | AI | AI | New |
| 18 | djangocms-agent | AI | AI | New |
| 19 | djangocms-reviewer | AI | AI | New |
| 20 | django | AI | AI | New |
| 21 | django-dev-env | AI | AI | New |
| 22 | django-expert | AI | AI | New |
| 23 | documentation | AI, Central | AI | ✓ In Central |
| 24 | documents | AI, Central | AI | ✓ In Central |
| 25 | endsession | AI | AI | New |
| 26 | extensions | AI, Central | AI | ✓ In Central |
| 27 | find-skills | AI | AI | New |
| 28 | gh | AI | AI | New |
| 29 | github | AI, Central | AI | ✓ In Central |
| 30 | github-cli | AI | AI | New |
| 31 | git | AI | AI | New |
| 32 | gitlab-pages-dns | AI | AI | New |
| 33 | google-workspace | AI | AI | New |
| 34 | grind | AI | AI | New |
| 35 | handoff | AI | AI | New |
| 36 | infra | AI, LFNW, Central | AI | ✓ In Central |
| 37 | infra-placement | AI | AI | New |
| 38 | knowledge-base | AI | AI | New |
| 39 | lifecycle | AI | AI | New |
| 40 | mail-auth-check | AI | AI | New |
| 41 | manager | AI, Central | AI | ✓ In Central |
| 42 | mariadb | AI | AI | New |
| 43 | media | AI, Central | AI | ✓ In Central |
| 44 | microsoft-foundry | AI | AI | New |
| 45 | mikrotik | AI | AI | New |
| 46 | mr-review | AI | AI | New |
| 47 | openspec-apply-change | AI | AI | New |
| 48 | openspec-archive-change | AI | AI | New |
| 49 | openspec-bulk-archive-change | AI | AI | New |
| 50 | openspec-continue-change | AI | AI | New |
| 51 | openspec-explore | AI | AI | New |
| 52 | openspec-ff-change | AI | AI | New |
| 53 | openspec-new-change | AI | AI | New |
| 54 | openspec-onboard | AI | AI | New |
| 55 | openspec-sync-specs | AI | AI | New |
| 56 | openspec-verify-change | AI | AI | New |
| 57 | ops | AI, LFNW, Central | AI | ✓ In Central |
| 58 | pdf | AI | AI | New |
| 59 | pptx | AI | AI | New |
| 60 | proxmox | AI | AI | New |
| 61 | proxmox-cli | AI | AI | New |
| 62 | release | AI | AI | New |
| 63 | reconcile-issues | AI, Central | AI | ✓ In Central |
| 64 | researcher | AI, Central | AI | ✓ In Central |
| 65 | review | AI | AI | New |
| 66 | routeros | AI | AI | New |
| 67 | search | AI, Central | AI | ✓ In Central |
| 68 | security | AI | AI | New |
| 69 | selector | AI, Central | AI | ✓ In Central |
| 70 | shared-browser | AI | AI | New |
| 71 | skills | AI | AI | New |
| 72 | skills-reference | AI | AI | New |
| 73 | startsession | AI | AI | New |
| 74 | task-mgmt | AI, LFNW, Central | AI | ✓ In Central |
| 75 | templates | AI | AI | New |
| 76 | technitium | AI | AI | New |
| 77 | triage | AI | AI | New |
| 78 | tools | AI | AI | New |
| 79 | vikunja-ticket | AI | AI | New |
| 80 | vikunja-user | AI | AI | New |
| 81 | web | AI, LFNW, Central | AI | ✓ In Central |
| 82 | web-preview | AI | AI | New |
| 83 | websearch | AI | AI | New |
| 84 | wordpress | AI | AI | New |
| 85 | wordpress-dev | AI | AI | New |
| 86 | xlsx | AI | AI | New |
| 87 | zabbix | AI | AI | New |
| 88 | lfnw-linkedin-photo | LFNW | LFNW | New |
| 89 | venue | LFNW | LFNW | New |
| 90 | sponsors | LFNW | LFNW | New |
| 91 | homepage-ctas | LFNW | LFNW | New |
| 92 | featured-speakers | LFNW | LFNW | New |
| 93 | visual-regression | LFNW | LFNW | New |
| 94 | grouchys-diner-monitor | OPCODE | OPCODE | New |

## Merge Notes

### Skills with duplicates across sources:
- **github**: AI + Central (already in Central)
- **documentation**: AI + Central (already in Central)
- **credential-mgmt**: AI + Central (already in Central)
- **devops**: AI + LFNW + Central (already in Central)
- **development**: AI + LFNW + Central (already in Central)
- **infra**: AI + LFNW + Central (already in Central)
- **ops**: AI + LFNW + Central (already in Central)
- **task-mgmt**: AI + LFNW + Central (already in Central)
- **web**: AI + LFNW + Central (already in Central)
- **ai-framework**: AI + Central (already in Central)
- **bitwarden**: AI + Central (already in Central)
- **data**: AI + Central (already in Central)
- **documents**: AI + Central (already in Central)
- **extensions**: AI + Central (already in Central)
- **manager**: AI + Central (already in Central)
- **media**: AI + Central (already in Central)
- **project-lifecycle**: AI + Central (already in Central)
- **researcher**: AI + Central (already in Central)
- **search**: AI + Central (already in Central)
- **selector**: AI + Central (already in Central)

## Next Steps

1. Compare duplicate skills (github, documentation, credential-mgmt, devops, development, infra, ops, task-mgmt, web)
2. Merge the best content from each source
3. Add all new skills to the central repo
4. Update README.md and setup.sh
5. Push to GitHub

