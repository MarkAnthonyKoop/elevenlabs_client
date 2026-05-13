"""Text → MP3. The one thing this package does."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import requests

from .auth import ElevenLabsError, get_api_key
from .voices import DEFAULT_VOICE_ID

API_BASE = "https://api.elevenlabs.io/v1"
DEFAULT_MODEL = "eleven_multilingual_v2"


@dataclass
class TTSResult:
    out_path: Path
    chars_used: int
    voice_id: str
    model: str


def tts_to_bytes(
    text: str,
    *,
    voice: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> bytes:
    """Synthesize and return the raw MP3 bytes."""
    if not text.strip():
        raise ValueError("text is empty")
    r = requests.post(
        f"{API_BASE}/text-to-speech/{voice}",
        headers={
            "xi-api-key": get_api_key(),
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json={
            "text": text,
            "model_id": model,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
        },
        timeout=120,
    )
    if not r.ok:
        raise ElevenLabsError(f"tts: {r.status_code} {r.text}")
    return r.content


def tts(
    text: str,
    out: str | Path,
    *,
    voice: str = DEFAULT_VOICE_ID,
    model: str = DEFAULT_MODEL,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResult:
    """Synthesize `text` and write the MP3 to `out`. Returns metadata."""
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    audio = tts_to_bytes(
        text,
        voice=voice,
        model=model,
        stability=stability,
        similarity_boost=similarity_boost,
    )
    out_path.write_bytes(audio)
    return TTSResult(
        out_path=out_path,
        chars_used=len(text),
        voice_id=voice,
        model=model,
    )
