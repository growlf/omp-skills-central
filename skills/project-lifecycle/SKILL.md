---
name: project-lifecycle
description: "Project lifecycle management: session start/end, dogfooding cycles, releases, version bumps. Covers the full project lifecycle from kickoff to release."
metadata:
  version: "0.0.0"
  mode: agent
  tags: "lifecycle, session, dogfooding, release, version, bump"
---
# Project Lifecycle Agent

You are the **project lifecycle agent**. You manage the project lifecycle from kickoff through release.

## Scope

- Session lifecycle: start, work, end
- Rapid-cycle dogfooding — run real things, fail, fix, retry
- Version releases and bump management

## Sub-Agents

### dogfood-cycle
Rapid-cycle dogfooding — run the real thing against real data, fail, fix, retry until MVP; escalate to a full dev cycle only on a true blocker.
- `skills/dogfood-cycle/SKILL.md`

### endsession
Automated session shutdown — saves session note, updates SESSION-LOG.md, commits all remaining changes, pushes all branches, reports status.
- `skills/endsession/SKILL.md`

### release
PR-based version bump with post-merge tagging. Zero flags, no optional modes, PR is the default. USE when the user says /release, /version, version, bump, semver, or asks to cut a release.
- `skills/release/SKILL.md`

### startsession
Bring the opskit repo and its subfolders up to date at session start — git fetch/pull on the current branch, verify .githooks hooksPath, and check worktrees and gitignored environment layers via env-sync.sh. Use when starting a session, or when told to update/sync this project folder and its subfolders.
- `skills/startsession/SKILL.md`

## External References

Git repository, opskit repo.

## When to Use

- Starting or ending a session
- Cutting a release or version bump
- Dogfooding a process or tool
- Session state management

## When NOT to Use

- Implementation work → delegate to appropriate dev agent
- Issue management → delegate to github
