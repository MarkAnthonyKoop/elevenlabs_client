# CLAUDE.md — elevenlabs_client

Read `README.md` first. Universal rules: `~/CLAUDE.md`. Machine notes:
`~/claude/CLAUDE.md`.

## Single purpose

`elevenlabs_client` does **one thing**: text → MP3 via the ElevenLabs HTTP
API. Voice listing and voice lookup support that one thing. Anything else
(post-processing, mixing, lip-sync) belongs in a sibling.

## Available state

API key resolution: `ELEVENLABS_API_KEY` env var first, then
`~/.cache/elevenlabs_client/api_key` (chmod 600). Both paths are checked by
`auth.get_api_key()`. **Do not** add a third location without updating the
README.

If you find the file missing on a fresh setup, prompt the user with the
exact path to drop it — don't try to OAuth-flow your way into ElevenLabs.

## Files stay under 150 lines

If `tts.py` grows past that — likely because we add streaming or websockets
— split into `tts_stream.py` or similar. Don't branch inside `tts.py`.

## Don't use the `elevenlabs` SDK

The official SDK pulls ~30MB of transitive deps (pydantic v2, httpx,
websockets) for what is fundamentally three REST endpoints. `requests`
covers our needs. Revisit only when we need bidirectional streaming.

## Cost discipline

ElevenLabs bills per character. A 5-minute narration at ~150 wpm is ~7500
chars — a notable fraction of the Free tier. When invoked from `edit_suite`,
the caller logs cost via `edit_suite/telemetry.py`. **Always** return
`chars_used` from `tts()` so telemetry can capture the actual bill.

If a workflow loops `tts()` many times (e.g., per-paragraph synthesis for a
documentary), the caller should batch by reading the script file once and
either using `tts-batch` or hitting the API in one call where possible.

## When something is broken, fix the root cause

If the API returns 4xx, surface the body directly (it's almost always a
useful error). Don't retry silently. Don't catch and swallow.

If the API returns 5xx, one retry with backoff is acceptable. Beyond that,
fail and let the caller decide.

## Smoke test before declaring done

```bash
# 1. CLI loads, subcommands listed
python3 -m elevenlabs_client --help | grep -E "voices|tts|tts-batch"

# 2. key resolves (will error meaningfully if not set)
python3 -c "from elevenlabs_client.auth import get_api_key; print(get_api_key()[:8] + '...')"

# 3. real round-trip (requires a working key + free-tier headroom)
python3 -m elevenlabs_client tts \
    --text "smoke test, one two three" \
    --out /tmp/_es_smoke.mp3
file /tmp/_es_smoke.mp3
# expect: ISO Media or MPEG ADTS / audio
rm /tmp/_es_smoke.mp3
```
