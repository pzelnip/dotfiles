# Claude Code Stuff

This directory is a personal library of [Claude Code](https://claude.com/claude-code)
skills, hooks, and config that I use across machines. Unlike `/dotfiles`, nothing
here is symlinked automatically — Claude Code reads from `~/.claude`, so on a new
machine just copy what you need.

Everything here is intended to be **general** (not tied to work-specific tooling).

## Structure

* `/skills` — custom skills, one directory per skill (each containing a
  `SKILL.md`).
* `/hooks` — event hooks (`notification.py`, `stop.py`) that provide spoken
  notifications when Claude needs attention or finishes.
* `/core` — Python support package the hooks import (TTS, transcript parsing,
  config, logging). The hooks add `..` to `sys.path`, so `core/` must sit
  directly alongside `hooks/` under `~/.claude`.
* `statusline.sh` — status line script (model, cwd, project, session, cost).

## Installing on a new machine

### Skills

```shell
cp -r claude/skills/<skill-name> ~/.claude/skills/
```

### Hooks + core + statusline

Copy the bundle (keep `hooks/` and `core/` as siblings — the hooks import
`core` via a relative `sys.path` entry):

```shell
cp -r claude/hooks     ~/.claude/hooks
cp -r claude/core      ~/.claude/core
cp    claude/statusline.sh ~/.claude/statusline.sh
```

Then wire them into `~/.claude/settings.json`:

```jsonc
{
  "hooks": {
    "Notification": [
      { "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/notification.py" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/stop.py" }] }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline.sh"
  }
}
```

**Dependencies / config:**

* Requires the `requests` Python package.
* TTS prefers the OpenAI API when `OPENAI_API_KEY` is set, and falls back to the
  macOS `say` command otherwise.
* `statusline.sh` requires `jq`.
