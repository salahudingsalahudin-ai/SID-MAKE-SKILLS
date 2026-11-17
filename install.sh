#!/usr/bin/env bash
# Sid Agent Skills — layout check.
# Verifies every skill folder has a readable SKILL.md and prints the list.
# Usage: ./install.sh
set -e
cd "$(dirname "$0")"

echo "Sid Agent Skills — layout check"
echo "================================"

count=0
missing=0
for dir in skills/*/; do
  name=$(basename "$dir")
  if [ -f "$dir/SKILL.md" ]; then
    desc=$(awk 'BEGIN{p=0} /^---$/{p++; next} p==1 && /^description:/{sub(/^description: */,""); if ($0=="|-" || $0=="|") {getline; sub(/^  */,"")}; print substr($0,1,100); exit}' "$dir/SKILL.md")
    printf '%-28s %s\n' "$name" "${desc}"
    count=$((count + 1))
  else
    echo "MISSING SKILL.md: $name"
    missing=$((missing + 1))
  fi
done

echo "--------------------------------"
echo "Skills found: $count"
if [ "$missing" -gt 0 ]; then
  echo "Missing SKILL.md: $missing"
  exit 1
fi
echo "Layout OK: README.md, AGENTS.md, install.sh, skills/ ($count skills)"
echo
echo "To use: copy skills/ into your agent's skills folder,"
echo "e.g. ~/.claude/skills/ or .claude/skills/ — see README.md."
