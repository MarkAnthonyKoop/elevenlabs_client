# elevenlabs_client

Programmatic client for [ElevenLabs](https://elevenlabs.io) — text-to-speech,
voice listing, and (future) voice cloning.

Sized for use inside `edit_suite` workflows: one prompt + voice → an MP3 file
on disk. Sibling of `suno_client/` (which generates *songs*); this generates
*voiceovers and dialogue*.

---

## §1 User manual

### One-time setup

```bash
# Save your ElevenLabs API key (paste once; chmod 600).
mkdir -p ~/.cache/elevenlabs_client
chmod 700 ~/.cache/elevenlabs_client
printf 'YOUR_API_KEY_HERE' > ~/.cache/elevenlabs_client/api_key
chmod 600 ~/.cache/elevenlabs_client/api_key

# Or set the env var (overrides the file).
export ELEVENLABS_API_KEY="..."
```

### Common operations

```bash
# List available voices
python3 -m elevenlabs_client voices

# Generate a voiceover (default voice + model)
python3 -m elevenlabs_client tts \
    --text "Welcome to the show." \
    --out /tmp/intro.mp3

# Use a specific voice (id from `voices` output)
python3 -m elevenlabs_client tts \
    --text "Welcome to the show." \
    --voice 21m00Tcm4TlvDq8ikWAM \
    --out /tmp/intro.mp3

# Generate from a file (one paragraph per line; one MP3 per line)
python3 -m elevenlabs_client tts-batch \
    --in script.txt \
    --voice 21m00Tcm4TlvDq8ikWAM \
    --out-dir /tmp/lines/
```

---

## §2 Reference

### CLI subcommands

| Command | Purpose |
|---|---|
| `voices` | List voices on the account (id, name, category). |
| `tts --text T --out PATH [--voice V] [--model M]` | One-shot synthesis. |
| `tts-batch --in FILE --out-dir DIR [--voice V]` | One MP3 per line in FILE. |

### Python API

```python
from elevenlabs_client import tts, list_voices, default_voice_id

list_voices()                          # -> [{"voice_id": ..., "name": ...}, ...]
tts("Welcome to the show.", out="/tmp/intro.mp3")     # default voice
tts("Goodnight.", out="/tmp/outro.mp3", voice=default_voice_id())
```

### Authentication

API key is resolved from (first match wins):

1. `ELEVENLABS_API_KEY` env var
2. `~/.cache/elevenlabs_client/api_key` (chmod 600 strongly recommended)
3. Raises `ElevenLabsError` otherwise

### Models

Default model: `eleven_multilingual_v2`. Override with `--model` or the
`model` kwarg. See ElevenLabs docs for the current list.

### Filesystem contract

- `~/.cache/elevenlabs_client/api_key` — your API key (chmod 600).
- Output files: wherever the caller asks. No state written to disk by tts().

### Costs (May 2026, ~indicative)

ElevenLabs bills per character generated. Roughly:
- Free: 10k chars/mo
- Starter ($5/mo): 30k chars/mo
- Creator ($22/mo): 100k chars/mo + voice cloning

Estimate at planning time: `len(text) * voice_cost_per_char`. The client
returns `chars_used` so `edit_suite/telemetry.py` can log it.

---

## §3 Architecture

### Module layout

```
__main__   ── CLI subcommands
auth.py    ── API key resolution (env -> file -> error)
voices.py  ── list_voices(), default_voice_id()
tts.py     ── tts(), tts_to_bytes()
```

### Why pure-requests, not the `elevenlabs` SDK

Same reasoning as `ai_cover_art`: the official SDK pulls in many MB of deps
(pydantic, httpx, websockets, …) for a handful of HTTP calls we can do with
`requests`. If we ever need streaming or websockets, that's the trigger to
revisit.

### What does NOT belong here

- Audio post-processing (EQ, compression) → future `audio_fx/` sibling.
- Voice cloning UX → if it grows beyond ~50 lines, split into `clone.py`.
- Selection-bound edits ("regenerate this exact 4 seconds with a different
  voice") → that's `audio_inpaint/`, a future sibling that may wrap us.
