---
name: discovery
description: "Search for and load new capabilities (agents, tools, packages) when you don't have what you need."
metadata:
  mode: skill
  version: "0.0.0"
---
# Discovery Skill

Use this skill when you encounter a task where you don't have the right capability, tool, or knowledge.

## When to use

- You recognize you need something you don't currently have
- You're stuck or circling on a problem that a specialized agent might solve
- A task could be done faster with a tool you haven't loaded yet
- You're unsure how to proceed and might benefit from external expertise

## Discovery procedure

### Step 1: Identify the gap

State clearly: "I need [capability] to do [task], but I don't have it."

Be specific about what you're missing — not just "a tool" but "browser automation" or "Django template debugging."

### Step 2: Search sources (in order)

Search sources in this order:

1. **Agent library** — `./scripts/` (bundled)
   - Run: `AGENTS_HOME=. python3 scripts/recommend.py "<what you need>"`
   - Returns matching agents from the registry
   - These are specialized sub-agents you can delegate to

2. **Pi packages** — `~/.pi/agent/npm/node_modules/` and `~/.pi/packages/`
   - **npm-installed packages**: `~/.pi/agent/npm/node_modules/*/skills/*/SKILL.md`
   - **Pi extension packages**: `~/.pi/packages/*/skills/*/SKILL.md`
   - List available packages: `find ~/.pi/agent/npm/node_modules -name "SKILL.md"` or `find ~/.pi/packages -name "SKILL.md"`
   - Read SKILL.md files to understand each package's capabilities

3. **MCP servers** — `mcp_status()`
   - Check if the capability exists as an MCP tool
   - `mcp_list_resources()` to see available tools
   - `mcp_connect("<server-name>")` to connect

4. **External sources** — web search
   - Search for tools, packages, or agents that solve the problem
   - GitHub, npm, PyPI, etc.
   - Use `web_search()` or `fetch_content()`

### Step 3: Evaluate candidates

For each candidate found, assess:
- **Relevance**: Does it directly address the gap?
- **Maturity**: Is it stable and well-documented?
- **Fit**: Does it match your project's stack/requirements?
- **Cost**: How much does it add to context or complexity?

### Step 4: Recommend

Present your findings to the user:

```
I found the following options for [capability]:

1. [Name] — [brief description]
   - Source: [agent library / Pi package / MCP / external]
   - Pros: [why it's a good fit]
   - Cons: [trade-offs]

2. [Name] — [brief description]
   - Source: ...

Would you like me to:
- Install [preferred option]?
- Load it into this session only?
- Continue with what I have?
- Something else?
```

### Step 5: Load (after user approval)

If the user approves:

**For agent library agents:**
- Wire the agent into the project: `bash scripts/wire-rules.sh <project-path>`
- The agent's SKILL.md will now be loaded

**For Pi packages:**
- Install via npm: `cd ~/.pi/agent/npm && npm install <package-name>` (global) or `npm install --save <package-name>` (local)
- Pi packages are loaded automatically from `~/.pi/agent/npm/node_modules/` and `~/.pi/packages/`
- Restart session to load the package

**For MCP servers:**
- Connect via: `mcp_connect("<server-name>")`
- Or add to Pi config for persistence

**For external tools:**
- Provide installation instructions
- Offer to add to your package manager

## Key principles

- **Ask, don't install** — always present options and get user approval
- **Be specific** — describe what the capability does, not just its name
- **Respect context** — don't load more than necessary for the task
- **One at a time** — load one capability, test it, then decide if you need more
- **Fail gracefully** — if no good match is found, continue with what you have and note the gap

## Examples

```
User: "Help me debug this Django template error"

I need Django template debugging knowledge but don't have it.
Searching agent library...
Found: django agent (generalist: web)
Recommend: "I found a Django specialist in the agent library. Wire it in?"

User: "Write a browser test for this form"

I need browser automation but don't have it.
Searching Pi packages...
Found: pi-playwright
Recommend: "I found pi-playwright in Pi packages. Install it?"
```
