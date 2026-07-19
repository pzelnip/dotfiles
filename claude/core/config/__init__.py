"""Configuration management utilities."""

from .manager import ConfigManager, get_config, is_notifications_enabled
from .scope import ConfigScope

__all__ = ['ConfigManager', 'ConfigScope', 'get_config', 'is_notifications_enabled']