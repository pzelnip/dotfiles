"""Configuration scope definitions for Claude Code."""

from enum import Enum
from pathlib import Path


class ConfigScope(Enum):
    """Configuration scopes in precedence order (highest to lowest)."""
    LOCAL = "local"      # .claude/settings.local.json (highest precedence)
    PROJECT = "project"  # .claude/settings.json 
    USER = "user"        # ~/.claude/settings.json (lowest precedence)


def get_config_path(scope: ConfigScope, repo_root: Path = None) -> Path:
    """Get the configuration file path for a given scope."""
    if scope == ConfigScope.LOCAL and repo_root:
        return repo_root / ".claude" / "settings.local.json"
    elif scope == ConfigScope.PROJECT and repo_root:
        return repo_root / ".claude" / "settings.json"
    elif scope == ConfigScope.USER:
        return Path.home() / ".claude" / "settings.json"
    else:
        raise ValueError(f"Invalid scope or missing repo_root: {scope}")


def find_repo_root(start_path: Path = None) -> Path:
    """Find the repository root by looking for .claude directory."""
    current = start_path or Path.cwd()
    
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    
    return None