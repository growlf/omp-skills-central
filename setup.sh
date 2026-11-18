#!/bin/bash
# setup.sh — Install central skills for all team members
# Run this once per machine, or after pulling updates

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CENTRAL="$HOME/.omp/central-skills"
SKILLS="$HOME/.omp/agent/skills"

# Clone or update the central repo
if [ -d "$CENTRAL" ]; then
  echo "Updating existing central skills repo..."
  cd "$CENTRAL"
  git pull
else
  echo "Cloning central skills repo..."
  mkdir -p "$(dirname "$CENTRAL")"
  git clone "$(git -C "$SCRIPT_DIR" remote get-url origin 2>/dev/null || echo "$SCRIPT_DIR")" "$CENTRAL"
fi

# Symlink skills
mkdir -p "$SKILLS"
SKILL_COUNT=0
for skill in "$CENTRAL/skills/"*/; do
  [ -d "$skill" ] || continue
  SKILL_NAME=$(basename "$skill")
  ln -sfn "$skill" "$SKILLS/$SKILL_NAME"
  SKILL_COUNT=$((SKILL_COUNT + 1))
  echo "  → $SKILL_NAME"
done

# Optional: setup marketplace (uncomment to enable)
# echo ""
# echo "Setting up OMP marketplace..."
# omp plugin marketplace add your-org/omp-skills-central
# for plugin in "$CENTRAL/plugins/"*/; do
#   [ -d "$plugin" ] || continue
#   PLUGIN_NAME=$(basename "$plugin")
#   echo "  Installing: $PLUGIN_NAME@skills-central"
#   omp plugin install "$PLUGIN_NAME"@skills-central
# done

echo ""
echo "Installed $SKILL_COUNT skill(s) into $SKILLS"
echo "Restart OMP to pick up new skills."
echo ""
echo "To update later: cd $CENTRAL && git pull && ./setup.sh"
