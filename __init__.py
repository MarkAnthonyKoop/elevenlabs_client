"""elevenlabs_client — text-to-speech via the ElevenLabs HTTP API."""
from .auth import ElevenLabsError, get_api_key
from .tts import tts, tts_to_bytes
from .voices import default_voice_id, list_voices

__all__ = [
    "ElevenLabsError",
    "get_api_key",
    "tts",
    "tts_to_bytes",
    "list_voices",
    "default_voice_id",
]
__version__ = "0.1.0"
