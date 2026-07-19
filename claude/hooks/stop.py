#!/usr/bin/env python3
"""
Stop hook for Claude Code - announces when Claude has finished its work.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.notifications import speak_text, generate_completion_message
from core.config import is_notifications_enabled
from core.hooks import run_hook_safely
from core.transcript import (
    parse_recent_messages,
    parse_last_assistant_message,
    format_recent_context,
    generate_specific_message
)


def generate_and_speak_completion(data):
    """Generate and speak completion message."""
    if not is_notifications_enabled():
        return "Notifications disabled"

    message = None

    try:
        transcript_path = data.get('transcript_path')

        if transcript_path:
            recent_messages = parse_recent_messages(transcript_path)
            last_text = parse_last_assistant_message(transcript_path)

            if last_text:
                context = format_recent_context(recent_messages)
                message = generate_specific_message('pause', None, last_text, context)
    except Exception:
        pass

    if not message:
        message = generate_completion_message(data)

    speak_text(message)

    return message


def main():
    run_hook_safely("stop", generate_and_speak_completion)


if __name__ == "__main__":
    main()
