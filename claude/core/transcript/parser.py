"""Simplified transcript parsing for Claude Code hooks."""

import json
import os
from typing import List, Dict, Any, Optional


class TranscriptParser:
    """Parses Claude Code JSONL transcript files."""
    
    def __init__(self, transcript_path: str):
        self.transcript_path = transcript_path
        self._messages = None
    
    @property
    def messages(self) -> List[Dict[str, Any]]:
        """Get all messages from the transcript (cached)."""
        if self._messages is None:
            self._messages = self._load_messages()
        return self._messages
    
    def get_recent(self, count: int = 10, roles: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get recent messages, optionally filtered by roles."""
        messages = self.messages
        
        if roles:
            messages = [msg for msg in messages if msg.get('role') in roles]
        
        return messages[-count:] if messages else []
    
    def _load_messages(self) -> List[Dict[str, Any]]:
        """Load all messages from the transcript file."""
        if not self.transcript_path or not os.path.exists(self.transcript_path):
            return []
        
        messages = []
        try:
            with open(self.transcript_path, 'r') as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))
        except Exception:
            pass
        
        return messages


def parse_transcript(transcript_path: str) -> List[Dict[str, Any]]:
    """Parse a transcript file and return all messages (convenience function)."""
    parser = TranscriptParser(transcript_path)
    return parser.messages