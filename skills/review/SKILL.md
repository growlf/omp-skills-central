---
name: review
description: Critical code-review pass for one unit of change — a GitHub PR, a branch, or the uncommitted working tree. Reviews correctness, security, tests, conventions, and scope; posts explicit findings as review comments with severity labels; ends with one clear verdict (approve / comment / request-changes). Use when the user says "/review", "review this", "code review", "review PR #n", or when another workflow (e.g. grind) delegates its review phase here.
metadata:
  version: "0.0.0"
  mode: skill
---
# Review

A disciplined review pass for one unit of change. Produces **posted findings**
and a **verdict** — a change is never "reviewed" by assertion alone.

## Invocation contract

- **Standalone:** the target comes from arguments — a PR number, branch name,
  or "working tree". If none given, use the PR or branch tied to the current
  checkout; if still ambiguous, stop and ask.
- **Composed:** invoked by another workflow (e.g. grind). The target is already
  established — do not ask, do not re-derive it. Findings return into the
  caller's flow; fixing and merging remain the caller's decisions.

## Prerequisites

- `gh` CLI authenticated (for PR reviews); plain `git` otherwise
- The diff available locally (`git fetch --all --prune` first)

## Procedure

1. **Orient.** Read the PR description, commit messages, and linked issues;
   list changed files (`gh pr view`, `gh pr diff --name-only`). Establish the
   stated intent — review against intent, not imagination.
2. **Read the full diff**, then open enough surrounding code to judge each hunk
   in context. Check, in priority order:
   - **Correctness:** logic errors, unhandled edge cases, swallowed error
     paths, concurrency issues
   - **Security:** secrets in diffs, injection, unsafe input handling, authz
     gaps. Plausible vulnerabilities are reported through `SECURITY.md` —
     never as a public comment.
   - **Tests:** do behavior changes ship with tests? Do tests assert behavior
     rather than implementation? Does the suite actually pass?
   - **Conventions:** matches neighboring code style and `AGENTS.md` rules;
     governance files untouched without cause
   - **Scope:** changes beyond stated intent — flag it, don't block on it
3. **Verify by running, not reading.** If a finding hinges on runtime behavior,
   run the relevant test or command before asserting it.
4. **Post the review.**
   - PR: inline comments on specific lines plus an overall review body via
     `gh pr review --comment` / `--request-changes`
   - Local diff: present findings in the conversation instead
5. **Label every finding** with `file:line`, why it matters, and a concrete fix:
   - `blocking` — broken, insecure, or untested behavior change
   - `should-fix` — real issue, not fatal
   - `nit` — polish; batch these together
6. **Verdict.** End with exactly one:
   - ✅ **APPROVE** — no blocking findings
   - ⚠️ **COMMENT** — should-fixes / nits only
   - ❌ **REQUEST_CHANGES** — at least one blocking finding
7. **Offer next step (standalone only).** Ask whether to apply the blocking /
   should-fix items now. When composed, stop after the verdict.

## Rules

- Post real comments. A silent approval is not a review.
- Never approve your own work; disclose authorship conflicts and still run the pass.
- Never merge. Review grants no merge authority — callers decide.
- Report, don't fix — unless standalone and the user accepted step 7's offer.
- Every finding cites `file:line`. No vague feedback.
