---
name: extensions
description: "Pi extensions for the Agent Library. Provides capability discovery, extension management, agent wiring, and debugging features."
metadata:
  version: "0.0.0"
  mode: agent
---
# Extensions Directory

This directory contains Pi extensions that enhance the Agent Library experience.

## Available Extensions

- **agent-aiyama** — Global agent session overseer: auto-detects project tech stack (40+ signatures), queries the agent library for matching specialists, and injects suggestions into every session. Provides `/agent-aiyama`, `/agents`, `/discover`, `/wire`, `/unwire` commands and `agent-aiyama-discover`, `agent-aiyama-wire` tools. Replaces `enhance.ts`, `capability-discovery`, and `ext-manager`.

- **capability-discovery** — Legacy: automatically detects project capabilities and injects agent recommendations. Provides `/agents`, `/discover`, `/wire`, `/unwire` commands. **Superseded by agent-aiyama**.

- **ext-manager** — Legacy: extension debugger. Provides `/ext` commands and `ext-manager-*` tools. **Superseded by agent-aiyama**.

- **compact-header** — Shortens conversation headers automatically.

- **custom-footer** — Adds custom footer to responses automatically.

- **git-guard** — Prevents dangerous git operations automatically.

- **tool-metadata** — Adds metadata to tool calls automatically.

- **worktree-enforcement** — Enforces worktree-only rule automatically.

## Installation

Install globally (available in all projects):

```bash
cp agents/extensions/<name> ~/.pi/agent/extensions/
```

Or per-project:

```bash
cp agents/extensions/<name> <project>/.pi/extensions/
```

Extensions are loaded automatically by Pi when the session starts.

## Migration

### From enhance.ts → agent-aiyama

agent-aiyama replaces enhance.ts with all its features:
- `/pi` → `/agent-aiyama`
- `/pi list` → `/agent-aiyama list`
- `/pi discover` → `/agent-aiyama discover`
- `/agents`, `/discover`, `/wire`, `/unwire` — all work as aliases
- `agent-discover` tool → `agent-aiyama-discover`

```bash
# Install agent-aiyama
cp agents/extensions/agent-aiyama ~/.pi/agent/extensions/agent-aiyama
# Remove old extensions
rm ~/.pi/agent/extensions/enhance.ts 2>/dev/null
rm ~/.pi/agent/extensions/capability-discovery.ts 2>/dev/null
rm ~/.pi/agent/extensions/ext-manager.ts 2>/dev/null
```

### From capability-discovery + ext-manager → agent-aiyama

agent-aiyama supersedes both. All commands and tools are included.

```bash
# Just install agent-aiyama, remove the old ones
cp agents/extensions/agent-aiyama ~/.pi/agent/extensions/agent-aiyama
rm ~/.pi/agent/extensions/capability-discovery.ts 2>/dev/null
rm ~/.pi/agent/extensions/ext-manager.ts 2>/dev/null
```
