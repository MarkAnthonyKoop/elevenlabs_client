"""List voices, look up the default."""
from __future__ import annotations

import requests

from .auth import ElevenLabsError, get_api_key

API_BASE = "https://api.elevenlabs.io/v1"

# Rachel — ElevenLabs' canonical demo voice. Available on all accounts.
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def default_voice_id() -> str:
    return DEFAULT_VOICE_ID


def list_voices() -> list[dict]:
    """Return [{voice_id, name, category, preview_url}, ...]."""
    r = requests.get(
        f"{API_BASE}/voices",
        headers={"xi-api-key": get_api_key()},
        timeout=30,
    )
    if not r.ok:
        raise ElevenLabsError(f"voices: {r.status_code} {r.text}")
    data = r.json().get("voices", [])
    return [
        {
            "voice_id": v["voice_id"],
            "name": v.get("name", ""),
            "category": v.get("category", ""),
            "preview_url": v.get("preview_url", ""),
        }
        for v in data
    ]
