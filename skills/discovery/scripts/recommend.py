#!/usr/bin/env python3
"""recommend.py — Recommend agents for a project, or say there are none.

Usage:
  python3 recommend.py "Django CMS project"
  python3 recommend.py --search django,ops,git
  python3 recommend.py --list
  python3 recommend.py --info <agent-name>
  python3 recommend.py --compare agent1 agent2
  python3 recommend.py --search "dns"

Exit codes:
  0  one or more agents cleared the relevance gate
  3  the query was understood but nothing in the registry matched — this is a
     useful answer, not a failure, and scripts should branch on it
  2  the registry is missing, empty, or has no search index
  1  usage error (no arguments, unknown agent, ...)

Scoring lives in ../../lib/scoring.py and is shared with agent-research.py.
"""

import argparse
import json
import os
import sys
from pathlib import Path
_RECOMMEND_DEBUG = os.environ.get("RECOMMEND_DEBUG") == "1"

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import db as registry_db  # noqa: E402
from lib import scoring  # noqa: E402
from lib.db import RegistryUnavailable  # noqa: E402

EXIT_OK = 0
EXIT_NO_MATCH = 3


class UsageParser(argparse.ArgumentParser):
    """argparse exits 2 on a usage error, colliding with "registry unavailable".

    A caller that cannot tell a typo from a broken database will page someone
    over `--limit 0` or ignore a real registry failure. Usage errors exit 1.
    """

    def error(self, message: str):  # noqa: D401 — argparse API
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def _use_new_db() -> bool:
    """Backend selection lives in lib/db so both CLIs always agree."""
    return registry_db.use_new_db()


def recommend(query: str, limit: int = 5, include_catalog: bool = False) -> dict:
    """Scored, gated recommendations. See lib/scoring.py for the algorithm.

    Args:
        query: Search query / project description
        limit: Maximum matches to return
        include_catalog: If True, include non-installed catalog entries
                         for discovery. Default False (installed only).
    """
    if _use_new_db():
        return _recommend_new(query, limit, include_catalog)
    return _recommend_old(query, limit)


def _recommend_old(query: str, limit: int) -> dict:
    """Old path: use agents.db directly."""
    conn = registry_db.connect()
    try:
        result = scoring.search(conn, query, limit=limit)
        return _enrich(conn, result)
    finally:
        conn.close()


def _recommend_new(query: str, limit: int, include_catalog: bool = False) -> dict:
    """New path: use state.db + catalog.db.

    Args:
        query: Search query
        limit: Maximum matches to return
        include_catalog: If True, include non-installed catalog entries
                         for discovery mode.
    """
    catalog = registry_db.connect_catalog()
    state = registry_db.connect_state()
    try:
        # Request more than limit to compensate for external agents that may
        # appear in the top-N but get filtered out by recommend.py.
        expanded_limit = min(limit * 3, 30)
        # Search WITHOUT kinds filter so skill hits are available for
        # parent promotion (H2).  Skills never appear in the final output;
        # only their parent agents do.
        result = scoring.search(catalog, query, limit=expanded_limit)
        # The selector answers "which agent?", so only installed agents
        # may appear. Scripts and references are catalog skills and must
        # never be recommended as agents.
        installed = {r[0] for r in state.cursor().execute(
            "SELECT ident FROM installed WHERE kind = 'agent'").fetchall()}
        source_idents = {r[0] for r in catalog.cursor().execute(
            "SELECT ident FROM entries").fetchall()}

        # Enrich all catalog entries with installed/edge data
        for match in result["matches"]:
            dn = match["name"]
            row = None
            lookup = dn  # default fallback
            # Try: local/{dn} → {dn} → ends with /{dn} (external entries)
            for candidate in (f"{dn}/{dn}" if '/' not in dn else dn,
                              dn if '/' not in dn else None,
                              f"%/{dn}" if '/' not in dn else None):
                if not candidate:
                    continue
                if candidate.startswith('%'):
                    row = catalog.cursor().execute(
                        "SELECT entry_id, ident, description, kind FROM entries WHERE ident LIKE ?",
                        (candidate,) ).fetchone()
                    if row:
                        lookup = row[1]  # ident
                        break
                else:
                    row = catalog.cursor().execute(
                        "SELECT entry_id, ident, description, kind FROM entries WHERE ident = ?",
                        (candidate,)).fetchone()
                    if row:
                        lookup = row[1]  # ident
                        break
            desc = row[2] if row else None  # description
            kind = row[3] if row else None  # kind
            tags = [r[0] for r in catalog.cursor().execute("""
                SELECT et.tag FROM entries e
                JOIN entry_tags et ON et.entry_id = e.entry_id
                WHERE e.ident = ?
            """, (lookup,)).fetchall()]
            skills = [r[0] for r in state.cursor().execute("""
                SELECT i2.ident FROM edges e
                JOIN installed i2 ON i2.ident = e.child
                WHERE e.parent = ? AND i2.kind = 'skill'
            """, (lookup,)).fetchall()]
            match.update({
                "ident": lookup,
                "description": (desc if desc else "No description"),
                "type": "agent" if kind == "agent" else "skill",
                "tags": tags,
                "skills": [s.rsplit("/", 1)[-1] for s in skills],
                "usage_projects": len(state.cursor().execute(
                            "SELECT project_path FROM agent_usage WHERE agent_name = ?", (lookup,)).fetchall()),
            })

        # --- H2: promote skill hits to their parent agent ---
        # After enrichment we know each match's ident and type.  When a query
        # matches only a skill (not its parent agent), the skill alone is not
        # a valid answer, but its parent is.  Promote the parent with
        # "skill:<child>" evidence so callers see *why* it was recommended.
        promoted: set[str] = set()  # parent idents we've already injected
        # Collect existing agent idents so we don't promote a parent that
        # is already in the result set (e.g. via an alias).
        existing_agents: set[str] = {
            m["ident"] for m in result["matches"]
            if m.get("type") == "agent" and m.get("ident") in installed
        }
        for match in result["matches"]:
            ident = match.get("ident")
            kind = match.get("type")
            if kind != "skill" or not ident or ident in installed:
                # Already a valid installed agent; nothing to promote.
                continue
            # Look up this skill's parent in the edges table.
            parent_row = state.cursor().execute(
                "SELECT parent FROM edges WHERE child = ?",
                (ident,),
            ).fetchone()
            if parent_row:
                parent_ident = parent_row[0]
                if parent_ident not in installed:
                    # Parent is not installed; skip promotion.
                    continue
                if parent_ident in existing_agents or parent_ident in promoted:
                    # Parent is already a candidate (alias hit or earlier
                    # promotion); no need to add a duplicate.
                    continue
                promoted.add(parent_ident)
                # Build evidence string from the skill's display name.
                child_name = match["name"]
                evidence = [f"skill:{child_name}"]
                evidence.extend(match.get("matched_on", []))
                # Look up the parent's own description and tags.
                p_row = catalog.cursor().execute(
                    "SELECT description FROM entries WHERE ident = ?",
                    (parent_ident,),
                ).fetchone()
                p_desc = p_row[0] if p_row else "No description"
                p_tags = [r[0] for r in catalog.cursor().execute("""
                    SELECT et.tag FROM entries e
                    JOIN entry_tags et ON et.entry_id = e.entry_id
                    WHERE e.ident = ?
                """, (parent_ident,)).fetchall()]
                # Add as a match with a tiny score penalty so it ranks
                # below any real FTS hit on the agent itself.
                result["matches"].append({
                    "name": scoring._get_name(parent_ident),
                    "score": round(match.get("score", 0.0) + 0.001, 6),
                    "matched_on": evidence,
                    "confidence": "high",
                    "ident": parent_ident,
                    "description": p_desc if p_desc else "No description",
                    "type": "agent",
                    "tags": p_tags,
                    "skills": [],
                    "usage_projects": len(state.cursor().execute(
                            "SELECT project_path FROM agent_usage WHERE agent_name = ?", (parent_ident,)).fetchall()),
                })

        # --- Promote model sub-agents (.md files) → their parent agent ---
        # Model sub-agents (kind='agent' with .md name) are children of a
        # generalist.  They should never rank above their parent.  Promote
        # the parent when a model sub-agent matches (M1 + H2 interaction).
        for match in list(result["matches"]):
            if match.get("type") != "agent" or match.get("ident") not in installed:
                continue
            ident = match["ident"]
            # Only promote for model sub-agents (.md files)
            if ".md" not in ident:
                continue
            # Skip if already a top-level generalist (no parent in edges)
            parent_row = state.cursor().execute(
                "SELECT parent FROM edges WHERE child = ?",
                (ident,),
            ).fetchone()
            if not parent_row:
                continue
            parent_ident = parent_row[0]
            if parent_ident not in installed:
                continue
            # Skip if parent is already in results
            if any(m.get("ident") == parent_ident for m in result["matches"]):
                continue
            # Look up parent description and tags.
            p_row = catalog.cursor().execute(
                "SELECT description FROM entries WHERE ident = ?",
                (parent_ident,),
            ).fetchone()
            p_desc = p_row[0] if p_row else "No description"
            p_tags = [r[0] for r in catalog.cursor().execute("""
                SELECT et.tag FROM entries e
                JOIN entry_tags et ON et.entry_id = e.entry_id
                WHERE e.ident = ?
            """, (parent_ident,)).fetchall()]
            evidence = [match["name"]] + match.get("matched_on", [])
            result["matches"].append({
                "name": scoring._get_name(parent_ident),
                "score": round(match.get("score", 0.0) + 0.001, 6),
                "matched_on": evidence,
                "confidence": "high",
                "ident": parent_ident,
                "description": p_desc if p_desc else "No description",
                "type": "agent",
                "tags": p_tags,
                "skills": [],
                "usage_projects": len(state.cursor().execute(
                            "SELECT project_path FROM agent_usage WHERE agent_name = ?", (parent_ident,)).fetchall()),
            })

        # Filter matches: in normal mode, only installed agents.
        # In catalog mode, include non-installed entries with source info.
        # Sort by score ascending (BM25: lower is better) before filtering.
        # Parent promotions get +0.001 so they rank below their children,
        # but skills are filtered out later anyway.
        result["matches"].sort(key=lambda m: m.get("score", 0.0), reverse=False)
        filtered = []
        for m in result["matches"]:
            if include_catalog:
                # Include everything, mark source
                ident = m.get("ident", "")
                entry_row = catalog.cursor().execute(
                    "SELECT source_id FROM entries WHERE ident = ?",
                    (ident,),
                ).fetchone()
                m["source"] = entry_row[0] if entry_row else "unknown"
                m["installed"] = ident in installed
                filtered.append(m)
            else:
                # Normal mode: installed agents only
                if m.get("ident") in installed and m.get("type") == "agent":
                    filtered.append(m)
        result["matches"] = filtered

        # After filtering+sorting, remove model sub-agents that rank above
        # their parent.  A model sub-agent should never appear before its
        # generalist parent (M1 + H2 interaction).
        for m in list(result["matches"]):
            if ".md" not in m.get("ident", ""):
                # Only model sub-agents (.md files) get removed — regular
                # child agents (django, infra, etc.) rank normally by BM25.
                continue
            parent_row = state.cursor().execute(
                "SELECT parent FROM edges WHERE child = ?",
                (m["ident"],),
            ).fetchone()
            if not parent_row:
                continue
            parent_ident = parent_row[0]
            # Find parent rank
            parent_idx = next(
                (i for i, p in enumerate(result["matches"]) if p["ident"] == parent_ident),
                None,
            )
            child_idx = result["matches"].index(m)
            if parent_idx is not None and parent_idx > child_idx:
                # Parent ranks below child — remove the child.
                result["matches"].pop(child_idx)

        result["no_match"] = not result["matches"]
        # Re-evaluate ambiguity after filtering/promotion.  The original
        # scoring.search() ambiguity flag is computed on the full catalog
        # ranking (skills + external entries), which changes after we filter
        # to installed agents only and apply H2 promotion.
        #
        # Strategy:
        #  - If scoring.search() already said ambiguous=True, keep it
        #    (the original detection covered the right cases before my
        #    scoring changes).
        #  - Only re-evaluate when the original was False — to catch cases
        #    where filtering/promotion made two previously-distant agents
        #    appear close (e.g. "security hardening" where the top skill
        #    match was filtered out).
        #
        # Use a relative threshold matching the original AMBIGUITY_RATIO for
        # post-filter re-evaluation.  This catches cases where filtering
        # made previously-distant agents appear close (e.g. "security
        # hardening") without over-flagging cases like "pr review".
        # to avoid false positives from BM25 score scale changes.
        _POST_FILTER_AMBIGUITY = 0.10
        if not result.get("ambiguous") and len(result["matches"]) >= 2:
            s0 = abs(result["matches"][0]["score"])
            s1 = abs(result["matches"][1]["score"])
            rel_diff = abs(s0 - s1) / max(s0, s1, 1e-12)
            if rel_diff <= _POST_FILTER_AMBIGUITY:
                result["ambiguous"] = True
        # Fix confidence after filtering/promotion:
        #  - If not ambiguous, the top match must have "high" confidence
        #  - If ambiguous, the top 2 matches should have "ambiguous"
        if result["matches"]:
            if not result.get("ambiguous"):
                result["matches"][0]["confidence"] = "high"
            elif len(result["matches"]) >= 2:
                result["matches"][0]["confidence"] = "ambiguous"
                result["matches"][1]["confidence"] = "ambiguous"
        return result
    finally:
        state.close()
        catalog.close()


def _enrich(conn, result: dict) -> dict:
    """Attach the descriptive fields a caller needs to act on a match."""
    for match in result["matches"]:
        row = conn.cursor().execute(
            "SELECT description, type FROM agents WHERE name = ?", (match["name"],)
        ).fetchone()
        tags = [r[0] for r in conn.cursor().execute(
            "SELECT tag FROM agent_tags WHERE agent_name = ? ORDER BY tag", (match["name"],)
        )]
        skills = [r[0] for r in conn.cursor().execute(
            "SELECT skill_name FROM agent_skills WHERE agent_name = ? ORDER BY skill_name",
            (match["name"],),
        )]
        usage = conn.cursor().execute(
            "SELECT COUNT(*) FROM agent_usage WHERE agent_name = ?", (match["name"],)
        ).fetchone()[0]
        match.update({
            "ident": match["name"],
            "description": (row["description"] if row else "") or "No description",
            "type": (row["type"] if row else "") or "agent",
            "tags": tags,
            "skills": skills,
            "usage_projects": usage,
        })
    return result


def _display_name(ident: str) -> str:
    """ops/ops -> ops; owner/name -> name."""
    return ident.split("/", 1)[-1]


def _summary_new(catalog, state, ident: str) -> dict:
    """A list/info-shaped agent record from state.db + catalog.db."""
    entry = catalog.cursor().execute(
        "SELECT entry_id, description FROM entries WHERE ident = ?", (ident,)
    ).fetchone()
    tags: list[str] = []
    if entry:
        tags = [r[0] for r in catalog.cursor().execute(
            "SELECT tag FROM entry_tags WHERE entry_id = ? ORDER BY tag",
            (entry["entry_id"],),
        )]
    skills = state.cursor().execute("""
        SELECT i.ident AS skill_name, i.path AS skill_path, i.kind AS type
        FROM edges e
        JOIN installed i ON i.ident = e.child
        WHERE e.parent = ? AND i.kind = 'skill'
        ORDER BY i.ident
    """, (ident,)).fetchall()
    path = state.cursor().execute(
        "SELECT path FROM installed WHERE ident = ?", (ident,)
    ).fetchone()
    return {
        "name": _display_name(ident),
        "ident": ident,
        "description": (entry["description"] if entry else "") or "No description",
        "type": "agent",
        "status": "active",
        "path": path["path"] if path else "",
        "tags": tags,
        "skills": [dict(s) for s in skills],
        "usage_projects": len(state.cursor().execute(
                            "SELECT project_path FROM agent_usage WHERE agent_name = ?", (ident,)).fetchall()),
    }


def _list_agents_new() -> list[dict]:
    """List installed agents from state.db + catalog.db."""
    catalog = registry_db.connect_catalog()
    state = registry_db.connect_state()
    try:
        idents = [r[0] for r in state.cursor().execute(
            "SELECT ident FROM installed WHERE kind = 'agent' ORDER BY ident")]
        return [_summary_new(catalog, state, ident) for ident in idents]
    finally:
        state.close()
        catalog.close()


def _resolve_ident_new(state, name: str) -> str | None:
    """Accept 'ops', 'ops/ops' or an external 'owner/name'."""
    candidates = [name] if "/" in name else [f"{name}/{name}", name]
    for candidate in candidates:
        row = state.cursor().execute(
            "SELECT ident FROM installed WHERE ident = ? AND kind = 'agent'",
            (candidate,),
        ).fetchone()
        if row:
            return row[0]
    if "/" not in name:
        row = state.cursor().execute(
            "SELECT ident FROM installed WHERE ident LIKE ? AND kind = 'agent'",
            (f"%/{name}",),
        ).fetchone()
        if row:
            return row[0]
    return None


def _agent_info_new(name: str) -> dict | None:
    """Detailed agent record from state.db + catalog.db."""
    catalog = registry_db.connect_catalog()
    state = registry_db.connect_state()
    try:
        ident = _resolve_ident_new(state, name)
        if ident is None:
            return None
        info = _summary_new(catalog, state, ident)
        info["usage"] = []
        info["requires"] = [
            dict(r) for r in state.cursor().execute(
                "SELECT requires_ident, op, version FROM requires "
                "WHERE ident = ? ORDER BY requires_ident", (ident,))
        ]
        return info
    finally:
        state.close()
        catalog.close()


def list_agents() -> list[dict]:
    """List all active agents."""
    if _use_new_db():
        return _list_agents_new()
    conn = registry_db.connect()
    try:
        agents = conn.cursor().execute("""
            SELECT a.name, a.description, a.type,
                   GROUP_CONCAT(DISTINCT t.tag) as tags,
                   COUNT(DISTINCT s.skill_name) as skill_count
            FROM agents a
            LEFT JOIN agent_tags t ON a.name = t.agent_name
            LEFT JOIN agent_skills s ON a.name = s.agent_name
            WHERE a.status = 'active'
            GROUP BY a.name
            ORDER BY a.name
        """).fetchall()
        return [dict(a) for a in agents]
    finally:
        conn.close()


def agent_info(name: str) -> dict | None:
    """Get detailed info about an agent."""
    if _use_new_db():
        return _agent_info_new(name)
    conn = registry_db.connect()
    try:
        agent = conn.cursor().execute("SELECT * FROM agents WHERE name = ?", (name,)).fetchone()
        if not agent:
            return None
        tags = [r[0] for r in conn.cursor().execute(
            "SELECT tag FROM agent_tags WHERE agent_name = ?", (name,)
        ).fetchall()]
        skills = conn.cursor().execute(
            "SELECT skill_name, skill_path, type FROM agent_skills WHERE agent_name = ?", (name,)
        ).fetchall()
        usage = conn.cursor().execute(
            "SELECT project_path, linked_from FROM agent_usage WHERE agent_name = ?", (name,)
        ).fetchall()
        return {
            **dict(agent),
            "tags": tags,
            "skills": [dict(s) for s in skills],
            "usage": [dict(u) for u in usage],
        }
    finally:
        conn.close()


def compare_agents(names: list[str]) -> list[dict]:
    """Compare multiple agents side-by-side."""
    results = []
    for name in names:
        info = agent_info(name)
        if info:
            results.append(info)
    return results


def search_tags(term: str) -> list[dict]:
    """Find agents by exact tag or alias, e.g. --search review / --search dns."""
    term = term.strip().lower()
    if _use_new_db():
        return _search_tags_new(term)
    return _search_tags_old(term)


def _search_tags_old(term: str) -> list[dict]:
    """Old path: agents.db."""
    conn = registry_db.connect()
    try:
        names = {r[0] for r in conn.cursor().execute("""
            SELECT DISTINCT a.name
            FROM agents a
            JOIN agent_tags t ON a.name = t.agent_name
            WHERE a.status = 'active' AND LOWER(t.tag) = ?
        """, (term,))}
        names |= {
            agent for agent, words in scoring.load_aliases().items()
            if term in {w.lower() for w in words}
        }
        if not names:
            return []
        placeholders = ",".join("?" for _ in names)
        rows = conn.cursor().execute(
            f"SELECT name, description FROM agents WHERE name IN ({placeholders}) ORDER BY name",
            sorted(names),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def _search_tags_new(term: str) -> list[dict]:
    """New path: catalog.db + state.db."""
    catalog = registry_db.connect_catalog()
    state = registry_db.connect_state()
    try:
        entries = catalog.cursor().execute("""
            SELECT DISTINCT e.ident
            FROM entries e
            JOIN entry_tags et ON et.entry_id = e.entry_id
            WHERE LOWER(et.tag) = ? AND e.kind = 'agent'
        """, (term,)).fetchall()
        names = {r[0] for r in entries}
        term_tokens = set(scoring.query_tokens(term))
        aliases = scoring.load_aliases()
        for ident, words in aliases.items():
            alias_tokens: set[str] = set()
            for word in words:
                alias_tokens.update(scoring.query_tokens(word))
            if term_tokens & alias_tokens:
                names.add(scoring._normalize_alias_key(ident))
        if not names:
            return []
        installed = {r[0] for r in state.cursor().execute(
            "SELECT ident FROM installed WHERE kind = 'agent'").fetchall()}
        names = names & installed
        if not names:
            return []
        placeholders = ",".join("?" for _ in names)
        rows = catalog.cursor().execute(
            f"SELECT ident FROM entries WHERE ident IN ({placeholders}) ORDER BY ident",
            sorted(names),
        ).fetchall()
        # Callers (and the printer) expect the same shape as list/info:
        # `name` for display, `ident` for the canonical key.
        return [_summary_new(catalog, state, r["ident"]) for r in rows]
    finally:
        catalog.close()
        state.close()


def print_matches(result: dict) -> None:
    if result["ambiguous"]:
        print(f"Note: {len(result['matches'])} agents match about equally on this query"
              f" — that is a real ambiguity, not a ranking.")
    for i, match in enumerate(result["matches"], 1):
        installed_marker = " [installed]" if match.get("installed") else ""
        if not match.get("installed", True):
            installed_marker = " [not-installed]"  # catalog mode: not installed
        marker = " [ambiguous]" if match.get("confidence") == "ambiguous" else ""
        print(f"\n{i}. {match['name']} ({match['type']}){installed_marker}{marker}")
        print(f"   {match['description']}")
        if match.get("source"):
            print(f"   Source: {match['source']}")
        if match["tags"]:
            print(f"   Tags: {', '.join(match['tags'])}")
        print(f"   Matched: {', '.join(match['matched_on'])}")
        if match.get("skills"):
            shown = ', '.join(match["skills"][:5])
            more = "..." if len(match["skills"]) > 5 else ""
            print(f"   Skills: {len(match['skills'])} ({shown}{more})")
        if match.get("usage_projects"):
            print(f"   Used by: {match['usage_projects']} project(s)")


def print_refusal(result: dict) -> None:
    print(f"No agent matches {result['query']!r}.")
    if result["tokens"]:
        print(f"Tried: {', '.join(result['tokens'])}.")
    print("The registry has nothing for this. Either rephrase with a domain word"
          " (dns, django, git, review, docs) or create an agent — see manager/.")


def main() -> int:
    parser = UsageParser(description="Recommend agents for a project")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("query", nargs="?", help="Search query / project description")
    group.add_argument("--list", action="store_true", help="List all active agents")
    group.add_argument("--info", metavar="NAME", help="Show agent details")
    group.add_argument("--compare", nargs="+", metavar="NAME", help="Compare agents")
    group.add_argument("--search", metavar="TERM", help="Find agents by tag or alias")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--limit", type=int, default=5, help="Maximum matches (default 5)")
    parser.add_argument("--catalog", action="store_true",
                        help="Include non-installed catalog entries for discovery")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error(f"--limit must be at least 1 (got {args.limit})")

    try:
        if args.query is not None:
            result = recommend(args.query, limit=args.limit,
                               include_catalog=args.catalog)
            if args.json:
                print(json.dumps(result, indent=2))
            elif result["no_match"]:
                print_refusal(result)
            else:
                print_matches(result)
            return EXIT_NO_MATCH if result["no_match"] else EXIT_OK

        if args.list:
            agents = list_agents()
        elif args.info:
            info = agent_info(args.info)
            if info is None:
                print(f"recommend: no such agent: {args.info}", file=sys.stderr)
                return 1
            agents = [info]
        elif args.compare:
            agents = compare_agents(args.compare)
        else:
            agents = search_tags(args.search)
    except RegistryUnavailable as exc:
        print(f"recommend: {exc}", file=sys.stderr)
        return 2

    if not agents:
        print("No agents found.")
        return 1

    if args.json:
        print(json.dumps(agents, indent=2))
        return EXIT_OK

    for i, agent in enumerate(agents, 1):
        print(f"\n{i}. {agent['name']} ({agent.get('type', 'agent')})")
        print(f"   {agent.get('description') or 'No description'}")
        if agent.get("tags"):
            tags = agent["tags"]
            if isinstance(tags, str):
                tags = [t for t in tags.split(",") if t]
            if tags:
                print(f"   Tags: {', '.join(tags)}")
        skills = agent.get("skills") or []
        if skills:
            print(f"   Skills: {len(skills)}")
        if agent.get("usage_projects"):
            print(f"   Used by: {agent['usage_projects']} project(s)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
