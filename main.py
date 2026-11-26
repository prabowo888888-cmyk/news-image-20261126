#!/usr/bin/env python3
"""Entry point for the 26 November 2026 world-news image.

Copies the bundled entry.png (drawn by gen_image.py) into the output
directory the platform provides. Pure standard library, no network, and
fully deterministic: the same input file always produces the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a valid PNG")
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
