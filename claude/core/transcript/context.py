"""Context-aware message generation for notification hooks."""

import json
import os
import subprocess
from typing import List, Dict, Any, Optional, Tuple

CONTEXT_MESSAGE_COUNT = 10


def parse_recent_messages(transcript_path: str) -> List[Dict[str, Any]]:
    """Parse recent messages from transcript file.

    Returns list of message dicts with type, role, and content,
    or empty list on any error.
    """
    try:
        if not transcript_path or not os.path.exists(transcript_path):
            return []

        messages = []
        with open(transcript_path, 'r') as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))

        recent = messages[-CONTEXT_MESSAGE_COUNT:] if messages else []

        filtered = []
        for msg in recent:
            if msg.get('type') in ['user', 'assistant']:
                message_data = msg.get('message', {})
                role = message_data.get('role')
                if role in ['user', 'assistant']:
                    filtered.append({
                        'type': msg.get('type'),
                        'role': role,
                        'content': message_data.get('content', [])
                    })

        return filtered
    except Exception:
        return []


def parse_last_tool_use(transcript_path: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Find most recent tool_use block without a result.

    Returns tuple: (tool_name, tool_input_dict) or (None, None) on error.
    """
    try:
        messages = parse_recent_messages(transcript_path)

        tool_result_ids = set()
        for msg in messages:
            if msg.get('role') == 'user':
                content = msg.get('content', [])
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'tool_result':
                        tool_use_id = block.get('tool_use_id')
                        if tool_use_id:
                            tool_result_ids.add(tool_use_id)

        for msg in messages:
            if msg.get('role') == 'assistant':
                content = msg.get('content', [])
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'tool_use':
                        tool_id = block.get('id')
                        if tool_id and tool_id not in tool_result_ids:
                            tool_name = block.get('name')
                            tool_input = block.get('input', {})
                            return (tool_name, tool_input)

        return (None, None)
    except Exception:
        return (None, None)


def parse_last_assistant_message(transcript_path: str) -> Optional[str]:
    """Find most recent assistant text message in transcript.

    Returns text string or None on error.
    """
    try:
        messages = parse_recent_messages(transcript_path)

        for msg in reversed(messages):
            if msg.get('role') == 'assistant':
                content = msg.get('content', [])
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        return block.get('text')

        return None
    except Exception:
        return None


def format_recent_context(recent_messages: List[Dict[str, Any]]) -> str:
    """Format recent messages for claude CLI prompt.

    Returns formatted string or empty string on error.
    """
    try:
        if not recent_messages:
            return ''

        formatted_lines = []
        for msg in recent_messages:
            role = msg.get('role', '')
            content = msg.get('content', [])

            text_parts = []
            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        text_parts.append(block.get('text', ''))

            if text_parts:
                role_label = 'User' if role == 'user' else 'Assistant'
                text = ' '.join(text_parts)
                formatted_lines.append(f"{role_label}: {text}")

        formatted = '\n'.join(formatted_lines)

        if len(formatted) > 500:
            return formatted[:497] + '...'

        return formatted
    except Exception:
        return ''


def generate_specific_message(
    context_type: str,
    tool_name: Optional[str],
    tool_input: Any,
    recent_context: str,
    debug: bool = True
) -> Optional[str]:
    """Generate contextual notification message using claude CLI.

    Args:
        context_type: Either 'tool_use' or 'pause'
        tool_name: Name of the tool being used (for tool_use)
        tool_input: Tool input dict or message text (for pause)
        recent_context: Formatted recent conversation context
        debug: Whether to write debug logs

    Returns:
        Generated message string or None on error
    """
    try:
        if context_type == 'tool_use':
            prompt = f"""You are a notification system. Say ONLY what Claude wants to do, nothing else. No explanations, no markdown, no preamble. Just the plain spoken notification.

Recent conversation: {recent_context}
Claude is asking permission to: use {tool_name} tool with {tool_input}

Notification (must start with "Claude wants to", 5-10 words, plain text only):"""
        elif context_type == 'pause':
            prompt = f"""You are a notification system. Say ONLY why Claude paused, nothing else. No explanations, no markdown, no preamble. Just the plain spoken notification.

Recent conversation: {recent_context}
Claude just said: {tool_input}

Notification (must start with "Claude", 5-10 words, plain text only):"""
        else:
            return None

        if debug:
            hook_type = "NOTIFICATION HOOK" if context_type == 'tool_use' else "STOP HOOK"
            with open('/tmp/hook_debug.log', 'a') as f:
                f.write(f"\n=== {hook_type} ===\n")
                f.write(f"Prompt: {prompt[:200]}...\n")

        result = subprocess.run(
            ['claude', '-p', '--settings', '{"hooks":{}}', '--setting-sources', '', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if debug:
            with open('/tmp/hook_debug.log', 'a') as f:
                f.write(f"Generated: {result.stdout.strip()}\n")

        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return None
    except Exception:
        return None
