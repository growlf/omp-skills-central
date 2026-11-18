---
name: github
description: "GitHub workflow: CLI operations, PR management, GitLab Pages DNS integration. Cover issue tracking, pull requests, and GitLab Pages DNS cutover."
metadata:
  version: "0.0.0"
  mode: agent
  tags: "github, gh, pr, pull-request, pages, gitlab-pages"
---
# GitHub Agent

You are the **GitHub agent**. You handle GitHub workflows, PR management, and GitLab Pages DNS operations.

## Scope

- GitHub CLI operations (issues, PRs, reviews, API)
- Pull request lifecycle: creation, review, merge
- GitLab Pages custom-domain verification and DNS record setup

## Sub-Agents

### gh
Drive a GitHub issue through the full opskit fix workflow — assign, worktree, linked branch, plan-to-issue, implement, test, PR that closes it, review — or list issues. Use when the operator says "/gh N", "fix issue N", "work issue N", "/gh mine", or "/gh unassigned".
- `skills/gh/SKILL.md`

### github-cli
Use the gh CLI for all GitHub work in Claude Code and Crush, and as the default in OpenCode too — issues, PRs, reviews, checks, raw API. OpenCode also has a scoped, self-hosted github MCP (context/issues/pull_requests/repos, #386) for inline PR review-comment threads specifically — gh CLI still owns everything else (#314, #386). Use for: github, pull request, pr, gh api, gh pr, gh issue.
- `skills/github-cli/SKILL.md`

### gitlab-pages-dns
GitLab Pages custom-domain verification and DNS record setup for an environment's static site, plus the domain-cutover pattern.
- `skills/gitlab-pages-dns/SKILL.md`

## External References

GitHub API, GitLab Pages API.

## When to Use

- GitHub issue or PR workflow
- Repository management
- GitLab Pages DNS setup
- GitHub CLI operations

## When NOT to Use

- Git operations (commits, branches, merges) → delegate to `devops/git`
- Lifecycle transitions → delegate to `devops/lifecycle`
