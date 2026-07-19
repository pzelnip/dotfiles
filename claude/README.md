# Claude Code Stuff

This directory is a personal library of [Claude Code](https://claude.com/claude-code)
skills (and, eventually, slash commands) that I use across machines. Unlike
`/dotfiles`, nothing here is symlinked automatically — Claude Code reads skills
from `~/.claude/skills` and commands from `~/.claude/commands`, so on a new
machine just copy what you need:

```shell
cp -r claude/skills/<skill-name> ~/.claude/skills/
```

## Structure

* `/skills` - custom skills, one directory per skill (each containing a
  `SKILL.md`).
