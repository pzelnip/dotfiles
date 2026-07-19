"""Text-to-Speech manager for Claude Code notifications."""

import os
import subprocess
import tempfile
import requests
from typing import Optional


class TTSManager:
    """Manages text-to-speech functionality with multiple backends."""
    
    def __init__(self, prefer_openai: bool = True):
        self.prefer_openai = prefer_openai
    
    def speak(self, text: str, voice: str = "alloy") -> bool:
        """Speak text using the best available TTS method."""
        if self.prefer_openai and self._has_openai_key():
            if self._speak_openai(text, voice):
                return True
        
        return self._speak_macos(text)
    
    def _speak_openai(self, text: str, voice: str) -> bool:
        """Use OpenAI TTS API."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return False
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": voice,
                    "response_format": "mp3"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                
                subprocess.run(["afplay", tmp_file_path], check=True)
                os.unlink(tmp_file_path)
                return True
            
            return False
        except Exception:
            return False
    
    def _speak_macos(self, text: str) -> bool:
        """Use macOS built-in TTS."""
        try:
            subprocess.run(["say", text], check=True)
            return True
        except Exception:
            return False
    
    def _has_openai_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(os.getenv("OPENAI_API_KEY"))
    
    def is_available(self) -> bool:
        """Check if any TTS backend is available."""
        return self._has_openai_key() or self._has_macos_tts()
    
    def _has_macos_tts(self) -> bool:
        """Check if macOS TTS is available."""
        try:
            subprocess.run(["which", "say"], capture_output=True, check=True)
            return True
        except Exception:
            return False


# Global TTS manager instance
_tts_manager = TTSManager()


def speak_text(text: str, voice: str = "alloy") -> bool:
    """Speak text using the global TTS manager."""
    return _tts_manager.speak(text, voice)