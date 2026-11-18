#!/usr/bin/env bash
# wire-rules.sh — shell entry point; the implementation lives in wire_rules.py.
# Usage: ./scripts/wire-rules.sh <project-path> [--check] [--dry-run]
set -euo pipefail
exec python3 "$(dirname "${BASH_SOURCE[0]}")/wire_rules.py" "$@"
