"""Message generation for Claude Code notifications."""

from typing import Dict, Any


class NotificationMessages:
    """Generates contextual notification messages."""
    
    # Tool descriptions for notifications
    TOOL_DESCRIPTIONS = {
        "Bash": "run a command",
        "Write": "create a file", 
        "Edit": "edit a file",
        "MultiEdit": "edit a file",
        "Read": "read a file",
        "WebFetch": "fetch a URL",
        "Glob": "search for files",
        "Grep": "search file contents",
        "Task": "perform a task",
        "LS": "list directory contents",
        "NotebookRead": "read a notebook",
        "NotebookEdit": "edit a notebook",
        "TodoWrite": "update tasks",
        "WebSearch": "search the web"
    }
    
    def generate_notification(self, data: Dict[str, Any]) -> str:
        """Generate a notification message from hook data."""
        base_message = data.get("message", "")
        
        # Handle permission requests
        if "permission" in base_message.lower():
            return self._generate_permission_message(base_message)
        
        # Handle different message types
        if "error" in base_message.lower() or "failed" in base_message.lower():
            return "Claude encountered an error"
        elif "waiting" in base_message.lower():
            return "Claude is waiting for input"
        elif "approval" in base_message.lower() or "confirm" in base_message.lower():
            return "Claude needs your approval"
        else:
            return "Claude needs your attention"
    
    def generate_completion(self, data: Dict[str, Any]) -> str:
        """Generate a completion message for stop hooks."""
        return "Claude finished its task"
    
    def _generate_permission_message(self, base_message: str) -> str:
        """Generate permission message using tool descriptions."""
        if "permission to use" in base_message:
            tool_name = base_message.split("permission to use")[-1].strip()
            
            if tool_name in self.TOOL_DESCRIPTIONS:
                description = self.TOOL_DESCRIPTIONS[tool_name]
                return f"Claude wants to {description}"
        
        return "Claude needs permission"


# Global message generator
_messages = NotificationMessages()


def generate_notification_message(data: Dict[str, Any]) -> str:
    """Generate notification message using global generator."""
    return _messages.generate_notification(data)


def generate_completion_message(data: Dict[str, Any]) -> str:
    """Generate completion message using global generator."""
    return _messages.generate_completion(data)