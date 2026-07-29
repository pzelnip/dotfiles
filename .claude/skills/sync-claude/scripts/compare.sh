#!/usr/bin/env bash
#
# Reports sync candidates between this repo's claude/ dir and ~/.claude.
#
# Usage: compare.sh [repo-claude-dir] [home-claude-dir]
#
# Output is one tab-separated item per line:
#   HOME_ONLY <item>  only in ~/.claude       -> candidate to copy into the repo
#   REPO_ONLY <item>  only in repo claude/    -> candidate to copy into ~/.claude
#   DIFFERENT <item>  in both, contents vary  -> needs a direction decision
#   SAME      <item>  in both, identical      -> nothing to do
#
# An "item" is the sync unit: one entry per skill/command/agent
# (e.g. skills/test-improver), or one top-level entry otherwise
# (e.g. core, hooks, statusline.sh).

set -uo pipefail

REPO_CLAUDE="${1:-claude}"
HOME_CLAUDE="${2:-$HOME/.claude}"

# Runtime state and machine-local noise: never a sync candidate, either way.
EXCLUDED=(
  .DS_Store .git .venv .last-cleanup .last-update-result.json
  agent-memory backups cache debug file-history history.jsonl ide memory
  mcp-needs-auth-cache.json paste-cache plans plugins policy-limits.json
  projects remote-settings.json session-env sessions shell-snapshots
  statsig stats-cache.json todos __pycache__
)
# Repo-only files documenting the library; they have no place in ~/.claude.
EXCLUDED_REPO=(README.md)

DIFF_EXCLUDES=(--exclude=__pycache__ --exclude='*.pyc' --exclude=.DS_Store)

# Dirs whose children are the sync unit rather than the dir itself.
CONTAINERS=(skills commands agents)

in_list() {
  local needle="$1" x
  shift
  for x in "$@"; do
    [[ "$x" == "$needle" ]] && return 0
  done
  return 1
}

# Enumerate sync units under a .claude-style root, one per line.
list_items() {
  local root="$1" name child
  [[ -d "$root" ]] || return 0
  while IFS= read -r name; do
    [[ -z "$name" ]] && continue
    if in_list "$name" "${CONTAINERS[@]}" && [[ -d "$root/$name" ]]; then
      while IFS= read -r child; do
        [[ -z "$child" ]] && continue
        printf '%s/%s\n' "$name" "$child"
      done < <(ls -A "$root/$name")
    else
      printf '%s\n' "$name"
    fi
  done < <(ls -A "$root")
}

# Drop excluded items; $1 is "repo" or "home".
filter_items() {
  local scope="$1" line top base
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    top="${line%%/*}"
    base="${line##*/}"
    in_list "$top" "${EXCLUDED[@]}" && continue
    in_list "$base" "${EXCLUDED[@]}" && continue
    case "$base" in
      *.pyc | *.swp) continue ;;
    esac
    if [[ "$scope" == repo ]] && in_list "$line" "${EXCLUDED_REPO[@]}"; then
      continue
    fi
    printf '%s\n' "$line"
  done
}

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

list_items "$REPO_CLAUDE" | filter_items repo | sort >"$tmp/repo"
list_items "$HOME_CLAUDE" | filter_items home | sort >"$tmp/home"

comm -13 "$tmp/repo" "$tmp/home" | while IFS= read -r item; do
  printf 'HOME_ONLY\t%s\n' "$item"
done

comm -23 "$tmp/repo" "$tmp/home" | while IFS= read -r item; do
  printf 'REPO_ONLY\t%s\n' "$item"
done

comm -12 "$tmp/repo" "$tmp/home" | while IFS= read -r item; do
  if diff -rq "${DIFF_EXCLUDES[@]}" "$REPO_CLAUDE/$item" "$HOME_CLAUDE/$item" >/dev/null 2>&1; then
    printf 'SAME\t%s\n' "$item"
  else
    printf 'DIFFERENT\t%s\n' "$item"
  fi
done
