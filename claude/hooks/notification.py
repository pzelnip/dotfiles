#!/usr/bin/env python3
"""
Text-to-speech notification hook for Claude Code.

Provides context-aware notifications with OpenAI TTS and macOS fallback.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.notifications import speak_text, generate_notification_message
from core.config import is_notifications_enabled
from core.hooks import run_hook_safely
from core.transcript import (
    parse_recent_messages,
    parse_last_tool_use,
    format_recent_context,
    generate_specific_message
)


def generate_and_speak_notification(data):
    """Generate and speak notification message."""
    with open('/tmp/hook_debug.log', 'a') as f:
        f.write(f"\n=== HOOK DATA ===\n")
        f.write(f"Keys: {list(data.keys())}\n")
        for key, value in data.items():
            if key != 'transcript_path':
                f.write(f"{key}: {value}\n")

    if not is_notifications_enabled():
        return "Notifications disabled"

    message = None

    try:
        transcript_path = data.get('transcript_path')

        if transcript_path:
            recent_messages = parse_recent_messages(transcript_path)
            tool_name, tool_input = parse_last_tool_use(transcript_path)

            if tool_name and tool_input:
                recent_context = format_recent_context(recent_messages)
                message = generate_specific_message('tool_use', tool_name, tool_input, recent_context)
    except Exception:
        pass

    if not message:
        message = generate_notification_message(data)

    speak_text(message)

    return message


def main():
    run_hook_safely("notification", generate_and_speak_notification)


if __name__ == "__main__":
    main()
