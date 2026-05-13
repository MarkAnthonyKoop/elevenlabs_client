"""elevenlabs_client CLI. `python3 -m elevenlabs_client <subcommand>`."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .tts import DEFAULT_MODEL, tts
from .voices import DEFAULT_VOICE_ID, list_voices


def _cmd_voices(args: argparse.Namespace) -> int:
    for v in list_voices():
        print(f"{v['voice_id']}\t{v['name']}\t{v['category']}")
    return 0


def _cmd_tts(args: argparse.Namespace) -> int:
    res = tts(
        args.text,
        out=args.out,
        voice=args.voice,
        model=args.model,
    )
    print(json.dumps({
        "out": str(res.out_path),
        "chars_used": res.chars_used,
        "voice_id": res.voice_id,
        "model": res.model,
    }))
    return 0


def _cmd_tts_batch(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [l.strip() for l in Path(args.in_path).read_text().splitlines() if l.strip()]
    total_chars = 0
    for i, line in enumerate(lines, 1):
        target = out_dir / f"line_{i:03d}.mp3"
        res = tts(line, out=target, voice=args.voice, model=args.model)
        total_chars += res.chars_used
        print(f"{i}/{len(lines)} -> {target}", flush=True)
    print(f"done. {total_chars} chars across {len(lines)} files")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="elevenlabs_client")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("voices", help="list voices on the account")
    sp.set_defaults(func=_cmd_voices)

    sp = sub.add_parser("tts", help="text -> MP3")
    sp.add_argument("--text", required=True)
    sp.add_argument("--out", required=True)
    sp.add_argument("--voice", default=DEFAULT_VOICE_ID)
    sp.add_argument("--model", default=DEFAULT_MODEL)
    sp.set_defaults(func=_cmd_tts)

    sp = sub.add_parser("tts-batch", help="one MP3 per line in --in file")
    sp.add_argument("--in", dest="in_path", required=True)
    sp.add_argument("--out-dir", required=True)
    sp.add_argument("--voice", default=DEFAULT_VOICE_ID)
    sp.add_argument("--model", default=DEFAULT_MODEL)
    sp.set_defaults(func=_cmd_tts_batch)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
