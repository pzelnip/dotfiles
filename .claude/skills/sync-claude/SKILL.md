---
name: sync-claude
description: Two-way sync of Claude Code config between ~/.claude and this repo's claude/ dir — report what differs, prompt for what to copy each way, apply, then commit and push. Use when the user runs /sync-claude or asks to sync Claude skills/hooks/commands/statusline with the dotfiles repo.
---

# Sync Claude

## Overview

`claude/` in this repo is a portable library of Claude Code skills, hooks, commands,
and config (see [claude/README.md](../../../claude/README.md)). Nothing is symlinked —
Claude Code reads `~/.claude`, so the two copies drift. This skill reconciles them in
both directions, then commits and pushes the repo side.

Copying is **always opt-in per item**. Never sync anything the user did not pick.

## Sync unit

One item = one entry under `skills/`, `commands/`, or `agents/` (e.g.
`skills/test-improver`), or one top-level entry otherwise (e.g. `core`, `hooks`,
`statusline.sh`, `settings.json`).

Runtime state is never a candidate — `scripts/compare.sh` already excludes
`projects/`, `sessions/`, `history.jsonl`, `cache/`, `plugins/`, `file-history/`,
`__pycache__`, `.DS_Store`, and friends. Do not hand-copy anything it filtered out.

Work-specific items are never a candidate either. `claude/` holds **general**,
portable content, so items wired to internal Zapier tooling are listed in
[scripts/ignore.txt](scripts/ignore.txt) and dropped from the comparison in both
directions; `compare.sh` reports the count on stderr. If the user asks to sync
something the ignore list is holding back, or wants a new item permanently
excluded, edit that file rather than working around it.

## Workflow

### 1. Preflight

From the repo root (`/Users/adamparkin/dotfiles` — `cd` there, never use `git -C`):

```shell
git status --short
git pull --rebase --autostash origin main
```

If the working tree has uncommitted changes under `claude/`, show them and ask whether
to continue — the commit at the end would otherwise sweep them in. Untracked files
elsewhere in the repo are fine and must be left alone.

### 2. Compare

```shell
bash .claude/skills/sync-claude/scripts/compare.sh claude "$HOME/.claude"
```

Each output line is `STATUS<TAB>item`:

| Status      | Meaning                | Direction to offer          |
| ----------- | ---------------------- | --------------------------- |
| `HOME_ONLY` | only in `~/.claude`    | home → repo                 |
| `REPO_ONLY` | only in repo `claude/` | repo → home                 |
| `DIFFERENT` | in both, contents vary | ask which side wins         |
| `SAME`      | identical              | nothing — just count it     |

For any `DIFFERENT` item, read the actual diff before presenting it so the summary
says what changed, not just that something did:

```shell
diff -ru --exclude=__pycache__ --exclude='*.pyc' --exclude=.DS_Store \
  claude/<item> "$HOME/.claude/<item>"
```

### 3. Present and prompt

Two numbered lists, one per direction. For each item give a one-line description
(read the skill's `description` frontmatter or the file's first lines — do not guess
from the name), and for `DIFFERENT` items a one-line summary of the delta.

Mark `[review first]` inline on **plugin- or marketplace-installed** items, and on
items containing secrets, absolute home paths, or machine-local settings
(`settings.json`, `CLAUDE.md`). Flagging is advice, not a veto; the user decides.

If a candidate looks work-specific but `compare.sh` still surfaced it, say so and
offer to add it to [scripts/ignore.txt](scripts/ignore.txt).

Also report the ignored count `compare.sh` printed on stderr, so the user can see
the comparison was not exhaustive.

Ask for the selection as numbers, since there are usually more than four candidates:

> Reply with numbers (`1,3,5`), ranges (`1-4`), `all`, or `none` for each list.

Use `AskUserQuestion` only when it genuinely fits: a direction decision per
`DIFFERENT` item (options: `repo → home`, `home → repo`, `skip`), batching up to four
items per call. Never use it to page through a long candidate list.

If both lists are empty, say everything is already in sync, and stop — no commit,
no push.

### 4. Apply

Copy with `rsync` so excluded noise never lands in the repo. Directory items need the
trailing slashes exactly as shown:

```shell
# home -> repo
rsync -a --delete --exclude=__pycache__ --exclude='*.pyc' --exclude=.DS_Store \
  "$HOME/.claude/skills/<name>/" "claude/skills/<name>/"

# repo -> home
rsync -a --exclude=__pycache__ --exclude='*.pyc' --exclude=.DS_Store \
  "claude/skills/<name>/" "$HOME/.claude/skills/<name>/"

# single files, either direction
cp "$HOME/.claude/commands/<name>.md" "claude/commands/<name>.md"
```

Rules:

- `--delete` only on the home → repo direction, and only for a directory item the user
  explicitly picked. Never `--delete` into `~/.claude`.
- `hooks/` and `core/` travel together — the hooks import `core` via a relative
  `sys.path` entry. If the user picks one and the other also differs, say so and offer
  both.
- Copying into `~/.claude` does not wire anything up. If a synced hook or statusline
  is not referenced in `~/.claude/settings.json`, tell the user and show the JSON from
  [claude/README.md](../../../claude/README.md) rather than editing settings yourself.
- If a synced item introduces a new top-level category in `claude/` (e.g. the first
  `agents/` entry), add it to the Structure and install sections of
  [claude/README.md](../../../claude/README.md).

Re-run `compare.sh` afterward to confirm each picked item now reports `SAME`.

### 5. Commit and push

Only when the repo side actually changed. Stage by path — the repo carries unrelated
untracked files, so never `git add -A` or `git add .`:

```shell
git add claude/
git status --short
git pull --rebase --autostash origin main
git commit -m "$(cat <<'EOF'
Synced claude data

Into repo from ~/.claude:
* Add skills/<name> — <one-line what it does>
* Update core/ — <what changed>

Into ~/.claude from repo (no repo diff):
* Install commands/<name>.md
EOF
)"
git push origin main
```

Drop either section if that direction synced nothing. Keep the bullets specific —
name every item, and for updates say what changed. End the message with the
`Co-Authored-By` trailer.

If the push is rejected, `git pull --rebase --autostash origin main` and push again.

Finally, report to the user: what went each way, what was skipped, anything still
`DIFFERENT` by choice, and the pushed commit SHA.
