"""Centralized logging for Claude Code hooks."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class HookLogger:
    """Centralized logging for Claude Code hooks."""
    
    def __init__(self, log_dir: str = "~/.claude/.hook-logs", enabled: bool = True):
        self.log_dir = Path(log_dir).expanduser()
        self.enabled = enabled
    
    def log_event(self, hook_name: str, event_type: str, data: Dict[str, Any]) -> None:
        """Log a hook event with structured data."""
        if not self.enabled:
            return
        
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                "event_type": event_type,
                "data": data
            }
            
            log_file = self.log_dir / f"{hook_name}.jsonl"
            with open(log_file, "a") as f:
                json.dump(log_entry, f)
                f.write("\n")
        except Exception:
            # Silent failure to avoid breaking hooks
            pass
    
    def log_error(self, hook_name: str, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """Log hook errors with context."""
        if not self.enabled:
            return
        
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            error_entry = {
                "hook": hook_name,
                "error": error,
                "context": context
            }
            
            log_file = self.log_dir / "errors.jsonl"
            with open(log_file, "a") as f:
                json.dump(error_entry, f)
                f.write("\n")
        except Exception:
            pass


# Global logger instance
_logger = HookLogger(enabled=False)


def log_hook_event(hook_name: str, event_type: str, data: Dict[str, Any]) -> None:
    """Log a hook event using the global logger."""
    _logger.log_event(hook_name, event_type, data)


def log_hook_error(hook_name: str, error: str, context: Optional[Dict[str, Any]] = None) -> None:
    """Log a hook error using the global logger."""
    _logger.log_error(hook_name, error, context)