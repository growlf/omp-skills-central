# Web Skill Comparison

## Sources

| Source | Path |
|--------|------|
| AI | `~/Projects/AI/agents/web/SKILL.md` |
| LFNW | `~/Projects/lfnw/lfnw-django/.agents/skills/web/SKILL.md` |
| OMP | `~/Projects/omp-skills-central/skills/web/SKILL.md` |

## Scores

| Criterion | Score (AI) | Score (OMP) | Notes |
|-----------|-----------|-------------|-------|
| Completeness | 8/10 | 8/10 | 2 sub-agents + 2 leaf skills, good scope |
| Clarity | 9/10 | 9/10 | Well-structured with Leaf Skills section |
| Usefulness | 8/10 | 8/10 | Practical delegation to django/wordpress/shared-browser |

## Unique Sections

### In AI (not in OMP):
1. **`shared-browser` path** — uses relative path `shared-browser/SKILL.md`

### In OMP (not in AI):
1. **`shared-browser` path** — uses `skills/shared-browser/SKILL.md` (absolute-style)

### In LFNW:
- Identical to AI (uses `shared-browser/SKILL.md`)

## Differences

Single line difference: the `shared-browser` skill reference path.
- **AI/LFNW**: `shared-browser/SKILL.md` (relative, works within agent context)
- **OMP**: `skills/shared-browser/SKILL.md` (absolute-style, may not resolve correctly)

AI/LFNW path is correct because `shared-browser` lives at `skills/shared-browser/SKILL.md` relative to the agents directory root, and the skill reference in AI/agents/web/ is already at that level.

## Verdict

Merge: **Use AI/LFNW version** (correct relative path). OMP has a broken path that won't resolve.
