# Development Skill Comparison

## Sources

| Source | Path |
|--------|------|
| AI | `~/Projects/AI/agents/development/SKILL.md` (84 lines) |
| LFNW | `~/Projects/lfnw/lfnw-django/.agents/skills/development/SKILL.md` (84 lines) |
| OMP | `~/Projects/omp-skills-central/skills/development/SKILL.md` (73 lines) |

## Scores

| Criterion | Score (AI) | Score (OMP) | Notes |
|-----------|-----------|-------------|-------|
| Completeness | 9/10 | 7/10 | AI has reconcile-issues sub-agent, triggers metadata, more detailed delegation guidance |
| Clarity | 9/10 | 8/10 | AI's "When to Use" includes delegation targets, making routing clearer |
| Usefulness | 9/10 | 7/10 | AI's trigger patterns and reconciliation coverage add significant utility |

## Unique Sections

### In AI/LFNW (not in OMP):
1. **`triggers` metadata** — comprehensive trigger pattern list for auto-routing (cleanup, triage, grind, review, openspec, etc.)
2. **`reconcile-issues` sub-agent** — cross-references open issues with roadmap/plan files, detects stale/orphan/inconsistent items
3. **`Reconcile issues` in Scope** — listed alongside Cleanup, Triage, Code grinding, Code review, OpenSpec
4. **Detailed "When to Use"** — each line includes delegation target (e.g., `→ delegate to cleanup`), and covers more trigger phrases
5. **Duplicate "When to Use" line** — line 76 repeats reconcile issues check (minor bug, not harmful)

### In OMP (not in AI/LFNW):
1. None — OMP is a strict subset of AI/LFNW

## Differences

OMP version is missing:
- `triggers` YAML metadata block
- `reconcile-issues` sub-agent section
- `Reconcile issues` scope item
- Delegation targets in "When to Use" section (just lists triggers, not where to route)
- Several trigger phrase patterns

AI and LFNW versions are **identical**.

## Verdict

Merge: **Use AI/LFNW version** (it is the superset). OMP is a degraded copy missing features that exist in both AI and LFNW.
