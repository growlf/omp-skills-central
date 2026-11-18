---
name: mr-review
description: "Iterative PR/MR review-and-fix cycle — reviews a PR/MR, posts findings, fixes them in a worktree branch, re-reviews until all real items are resolved, then stops for human merge approval. Works with GitHub (gh) or GitLab (glab)."
metadata:
  version: "0.0.0"
  mode: skill
  triggers: /mr-review,/pr-review,/review-and-fix,/review-fix,/dev-review,/code-review-and-fix,review-and-fix,review-fix,dev-review
---
# MR Review — Iterative PR/MR Review & Fix

A disciplined review-and-fix cycle for any PR or merge request. Reviews fully, fixes every real finding in a worktree, re-reviews, and repeats until only nits/comments remain. Then stops for human merge approval.

## Invocation contract

- **Standalone:** target from args — PR number, branch name, or current worktree.
- **Composed:** invoked by another workflow (grind). Target already established.
- **Auto-detect:** if no target given, try current branch → linked PR/MR → working tree.

## Prerequisites

- `gh` (GitHub) **or** `glab` (GitLab) CLI — auto-detected
- `git` with remote pointing to canonical repo
- Working tree clean (or work in isolated worktree)

## Workflow

### Phase 1: Triage

1. **Orient.** Read the MR/PR description, linked issues, commit messages. List changed files.
2. **Fetch.** `git fetch --all --prune`
3. **Create worktree.** `git worktree add -b mr-review/<mr-id> worktree/mr-review/<mr-id> origin/<target-branch>`
4. **Checkout worktree.** All work happens here.

### Phase 2: Review

Review the diff in full context, checking:
- **Correctness** — logic errors, edge cases, swallowed errors
- **Security** — secrets, injection, authz gaps (flag via SECURITY.md if critical)
- **Tests** — do changes ship with tests? Do tests pass?
- **Conventions** — AGENTS.md rules, neighboring code style
- **Scope** — changes beyond stated intent

### Phase 3: Findings

Label every finding:
- `blocking` — broken, insecure, untested behavior change
- `should-fix` — real issue, not fatal
- `nit` — polish only

Post real comments on the MR/PR for `blocking` and `should-fix` items.

### Phase 4: Fix

For every `blocking` and `should-fix` finding:
1. Apply the fix in the worktree
2. Run tests after each meaningful change
3. If fix is ambiguous, stop and report to human
4. Commit with conventional commit message

### Phase 5: Push & Re-Review

1. **Push.** `git push origin mr-review/<mr-id>`
2. **Update PR.** Push a new commit with fixes to trigger CI/review
3. **Re-review.** Run the full review pass again on the updated diff
4. **Repeat.** Go back to Phase 3 with the new state

### Phase 6: Final Verdict

When no more `blocking` or `should-fix` items remain:
- `✅ APPROVE` — no blocking findings
- `⚠️ COMMENT` — nits only (human decides)
- `❌ REQUEST_CHANGES` — unresolvable issue

Then **stop** and present the final verdict to the human with:
- Summary of all findings and fixes applied
- Final verdict
- Link to the branch and MR/PR
- Question: "Shall I merge this?"

## GitLab vs GitHub

| Action | GitHub | GitLab |
|--------|--------|--------|
| Fetch diff | `gh pr view --diff` | `glab mr diff <id>` |
| List files | `gh pr view --files` | `glab mr show <id>` |
| Post comment | `gh pr review --comment` | `glab mr note <id> --message` |
| Request changes | `gh pr review --request-changes` | `glab mr edit <id> --reviewer <user>` |
| Push branch | `git push origin <branch>` | `git push origin <branch>` |

## Rules

- Post real comments. A silent approval is not a review.
- Never merge. Review grants no merge authority.
- Every finding cites `file:line`. No vague feedback.
- Always test fixes before committing.
- One worktree per MR/PR. Never touch main.
- If CI fails after fixes, diagnose and retry (up to 2× for flakes).
- If the MR author is us (the agent), still run the pass — disclose and proceed.
- Report scope creep as a finding, not a blocker.
