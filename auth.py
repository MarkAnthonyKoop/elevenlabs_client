"""API key resolution. Order: env var, then cache file, then error."""
from __future__ import annotations

import os
from pathlib import Path

KEY_PATH = Path(os.path.expanduser("~/.cache/elevenlabs_client/api_key"))


class ElevenLabsError(RuntimeError):
    pass


def get_api_key() -> str:
    env = os.environ.get("ELEVENLABS_API_KEY")
    if env:
        return env.strip()
    if KEY_PATH.exists():
        key = KEY_PATH.read_text().strip()
        if key:
            return key
    raise ElevenLabsError(
        f"No ElevenLabs API key found.\n"
        f"  Set ELEVENLABS_API_KEY env var, OR\n"
        f"  Write the key to {KEY_PATH} (chmod 600)."
    )


def save_api_key(key: str) -> None:
    """Persist the key to KEY_PATH with restrictive perms."""
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    KEY_PATH.write_text(key.strip())
    KEY_PATH.chmod(0o600)
