"""Notification system for Claude Code."""

from .tts import TTSManager, speak_text
from .messages import NotificationMessages, generate_notification_message, generate_completion_message

__all__ = ['TTSManager', 'speak_text', 'NotificationMessages', 'generate_notification_message', 'generate_completion_message']