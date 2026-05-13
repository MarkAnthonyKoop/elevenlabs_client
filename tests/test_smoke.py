"""Smoke test for elevenlabs_client — verifies the package imports cleanly."""
import importlib


def test_import():
    mod = importlib.import_module("elevenlabs_client")
    assert mod is not None


def test_main_module_importable():
    # `python3 -m elevenlabs_client` works iff this import works
    importlib.import_module("elevenlabs_client.__main__")
