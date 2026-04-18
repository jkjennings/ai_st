#!/usr/bin/env python3
"""
Download an AI-generated image from Pollinations.ai and save locally.
Free, no API key required.

Usage:
    python3 generate_image.py "prompt text" output_path [--width N] [--height N]

Output (stdout): JSON — {"path": "...", "url": "...", "status": "ok"}
                      or {"status": "error", "reason": "..."}
Exit: 0 on success, 1 on any failure (caller should always continue without the image)
"""
import sys
import json
import argparse
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import URLError

BASE_URL = "https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&nologo=true"


def generate(prompt: str, output_path: str, width: int, height: int) -> dict:
    encoded = quote(prompt, safe="")
    url = BASE_URL.format(prompt=encoded, w=width, h=height)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as resp:
        out.write_bytes(resp.read())
    return {"status": "ok", "path": str(out), "url": url}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="Image description prompt")
    parser.add_argument("output_path", help="Where to save the image (jpg/png)")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    args = parser.parse_args()

    try:
        result = generate(args.prompt, args.output_path, args.width, args.height)
        print(json.dumps(result))
    except URLError as e:
        print(json.dumps({"status": "error", "reason": f"Network error: {e.reason}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "reason": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
