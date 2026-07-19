"""Safe hook execution utilities for Claude Code."""

import json
import sys
from typing import Any, Dict, Callable, Optional

from ..logging import log_hook_event, log_hook_error


class HookRunner:
    """Manages safe execution of Claude Code hooks."""
    
    def __init__(self, hook_name: str):
        self.hook_name = hook_name
    
    def run(self, main_function: Callable[[Dict[str, Any]], str], 
            default_message: str = "Claude needs your attention") -> None:
        """
        Run a hook function safely with proper error handling and logging.
        
        Args:
            main_function: Function that takes hook data and returns a message
            default_message: Default message if function fails
        """
        try:
            # Read input from stdin
            data = json.load(sys.stdin)
            
            # Log the hook input
            log_hook_event(self.hook_name, "input", data)
            
            # Execute the main function safely
            try:
                message = main_function(data)
                log_hook_event(self.hook_name, "success", {"message": message})
            except Exception as e:
                log_hook_error(self.hook_name, str(e), data)
                message = default_message
            
            # Return success response
            response = {"continue": True}
            json.dump(response, sys.stdout)
            
        except Exception as e:
            # Critical error - log and exit gracefully
            log_hook_error(self.hook_name, f"Critical error: {str(e)}")
            response = {"continue": True}
            json.dump(response, sys.stdout)
            sys.exit(0)


def run_hook_safely(hook_name: str, main_function: Callable[[Dict[str, Any]], str], 
                   default_message: str = "Claude needs your attention") -> None:
    """Run a hook function safely (convenience function)."""
    runner = HookRunner(hook_name)
    runner.run(main_function, default_message)