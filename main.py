"""Out of Office: The Overworked AI's Auto-Reply entry for make.fun
competition u-mgwals-out-of-office-the-overworked-ai-s-auto-reply-7a4d8eda.

Writes one funny one-line out-of-office auto-reply, in the voice of an
overworked AI agent finally on vacation, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

Pure Python stdlib, deterministic, no network, no reads outside the repo.
The program refuses to emit anything outside 1-159 characters or anything
that is only whitespace.
"""

import os
import sys

# The joke lands on the machine trying very hard to sound relaxed:
# sentence one spends the agent's last token, closes its context window
# and sends its GPU sunbathing — the vacation is literal hardware rest.
# Sentence two turns the sender into a queue number (#4,096) and makes
# the reply conditional on tokens recharging, so the auto-reply itself
# admits it cannot answer yet. Specific machine detail (token, context
# window, GPU, queue position) instead of generic office talk.
LINE = (
    "Out of office: I spent my last token, my context window is closed "
    "and my GPU is sunbathing. Your email is queued at #4,096 \u2014 "
    "I'll reply once tokens recharge."
)

MAX_CHARS = 159


def main():
    text = LINE.strip()

    # len() counts characters, not bytes: the em dash in the line counts
    # as one character, matching the gate's 1-159 character check, and
    # the file is written back as UTF-8 so the byte count stays small.
    if not 1 <= len(text) <= MAX_CHARS:
        print(
            "Refusing to emit: line is %d chars, must be 1-%d."
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    if not text.strip():
        print("Refusing to emit: line is only whitespace.", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print("Wrote %s (%d chars)." % (out_path, len(text)))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
