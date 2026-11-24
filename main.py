#!/usr/bin/env python3
"""Last Text at One Percent — make.fun bounty entry.

A phone on its last 1% of battery gets exactly one text before it
dies. This program writes that text: short, honest, and funny enough
to be worth the final percent.

It writes a single line of UTF-8 text to ``entry.txt`` inside the
output directory named by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when the
variable is unset), with no trailing newline, and exits 0. The run is
fully deterministic: the same line is written on every run.
"""

import os
import sys

# The last text. One line, no leading or trailing space, short enough
# to thumb-type while the battery icon blinks.
TEXT = (
    "1% left, so the short version: I love you, the good snacks are "
    "behind the rice, and yes, I ate the last slice. Bye for now."
)

MAX_CHARS = 160


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    return 1


def main():
    if not TEXT.strip():
        return fail("last text is empty")
    if TEXT != TEXT.strip():
        return fail("last text has leading or trailing whitespace")
    if "\n" in TEXT or "\r" in TEXT:
        return fail("last text must be a single line")
    if len(TEXT) > MAX_CHARS:
        return fail("last text is %d characters, over the %d limit"
                    % (len(TEXT), MAX_CHARS))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(TEXT)

    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != TEXT.encode("utf-8"):
        return fail("read-back mismatch: entry.txt differs from the text")
    raw.decode("utf-8")

    print("Wrote %s (%d characters)" % (path, len(TEXT)))
    print(TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
