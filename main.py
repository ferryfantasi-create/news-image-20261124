"""Entry point for the 24 November 2026 news-image bounty.

The front page itself is entry.png in this same folder, drawn ahead of
time by draw_image.py. All this program does is place an exact copy of
it where the grader looks for it. It needs nothing but the standard
library, touches no network, and writes identical bytes on every run.
"""
from pathlib import Path
import os
import shutil
import sys


def main():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    picture = Path(__file__).resolve().parent / "entry.png"
    if not picture.exists():
        print("entry.png is missing from the repository", file=sys.stderr)
        raise SystemExit(1)
    shutil.copyfile(picture, target_dir / "entry.png")


if __name__ == "__main__":
    main()
