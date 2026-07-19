"""Simplified configuration manager for Claude Code."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .scope import ConfigScope, get_config_path, find_repo_root


class ConfigManager:
    """Manages configuration across Claude's scope hierarchy."""
    
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or find_repo_root()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using scope precedence."""
        env_key = f"CLAUDE_CUSTOM_{key.upper().replace('.', '_')}"
        
        # Check all scopes in precedence order
        for scope in ConfigScope:
            try:
                config_path = get_config_path(scope, self.repo_root)
                if config_path and config_path.exists():
                    settings = self._load_config(config_path)
                    env_vars = settings.get("env", {})
                    
                    if env_key in env_vars:
                        return self._parse_value(env_vars[env_key])
            except (ValueError, FileNotFoundError):
                continue
        
        return default
    
    def set(self, key: str, value: Any, scope: ConfigScope = ConfigScope.LOCAL) -> bool:
        """Set configuration value in specified scope."""
        try:
            config_path = get_config_path(scope, self.repo_root)
            env_key = f"CLAUDE_CUSTOM_{key.upper().replace('.', '_')}"
            
            # Load existing settings
            settings = self._load_config(config_path)
            
            # Ensure env section exists
            if "env" not in settings:
                settings["env"] = {}
            
            # Set the value
            settings["env"][env_key] = str(value)
            
            # Save back to file
            return self._save_config(config_path, settings)
        except Exception:
            return False
    
    def unset(self, key: str, scope: ConfigScope = ConfigScope.LOCAL) -> bool:
        """Remove configuration value from specified scope."""
        try:
            config_path = get_config_path(scope, self.repo_root)
            env_key = f"CLAUDE_CUSTOM_{key.upper().replace('.', '_')}"
            
            settings = self._load_config(config_path)
            env_vars = settings.get("env", {})
            
            if env_key in env_vars:
                del env_vars[env_key]
                return self._save_config(config_path, settings)
            
            return False
        except Exception:
            return False
    
    def list_all(self, prefix: str = "") -> Dict[str, Any]:
        """List all configuration values with optional prefix filter."""
        result = {}
        
        # Collect from all scopes (later scopes override earlier ones)
        for scope in reversed(list(ConfigScope)):
            try:
                config_path = get_config_path(scope, self.repo_root)
                if config_path and config_path.exists():
                    settings = self._load_config(config_path)
                    env_vars = settings.get("env", {})
                    
                    for env_key, value in env_vars.items():
                        if env_key.startswith("CLAUDE_CUSTOM_"):
                            config_key = env_key[14:].lower().replace('_', '.')
                            
                            if not prefix or config_key.startswith(prefix):
                                result[config_key] = self._parse_value(value)
            except Exception:
                continue
        
        return result
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file."""
        if not config_path.exists():
            return {}
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_config(self, config_path: Path, settings: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception:
            return False
    
    def _parse_value(self, value: str) -> Any:
        """Parse environment variable value back to appropriate type."""
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '').replace('-', '').isdigit():
            try:
                return float(value)
            except ValueError:
                return value
        else:
            return value


# Convenience functions
def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value (convenience function)."""
    return ConfigManager().get(key, default)


def is_notifications_enabled() -> bool:
    """Check if notifications are enabled."""
    return get_config("notifications.enabled", True)


def get_ide_command() -> str:
    """Get the configured IDE command."""
    return get_config("ide.command", None)