#!/usr/bin/env python3
"""Genera locales/es.json traduciendo desde en.json (requiere deep-translator en backend venv)."""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "locales" / "en.json"
ES_PATH = ROOT / "locales" / "es.json"

_PH = re.compile(r"\{[^{}]+\}")


def translate_one(translator, text: str) -> str:
    if not text or not text.strip():
        return text
    placeholders: list[str] = []

    def mask(m):
        placeholders.append(m.group(0))
        return f"<<{len(placeholders) - 1}>>"

    masked = _PH.sub(mask, text)
    try:
        out = translator.translate(masked)
    except Exception as e:
        print(f"WARN translate: {e!r} :: {text[:80]}...", file=sys.stderr)
        return text
    if not out:
        return text
    for i, ph in enumerate(placeholders):
        out = out.replace(f"<<{i}>>", ph)
    return out


def walk(obj, translator, cache: dict):
    if isinstance(obj, dict):
        return {k: walk(v, translator, cache) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(i, translator, cache) for i in obj]
    if isinstance(obj, str):
        if obj in cache:
            return cache[obj]
        t = translate_one(translator, obj)
        cache[obj] = t
        time.sleep(0.08)
        return t
    return obj


def main():
    from deep_translator import GoogleTranslator

    translator = GoogleTranslator(source="en", target="es")
    data = json.loads(EN_PATH.read_text(encoding="utf-8"))
    cache: dict[str, str] = {}
    out = walk(data, translator, cache)
    ES_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {ES_PATH} ({len(cache)} unique strings)")


if __name__ == "__main__":
    main()
