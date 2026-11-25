"""Two Lines to Your Past Self.

Writes exactly two lines to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR):

  Line 1: a warning about one specific moment, in a single sentence.
  Line 2: one sentence on why that moment mattered and what changed.

The moment is hyper-specific on purpose: a clock time, a named
recipient, and the exact words almost sent. The second line traces
the cause and effect instead of restating the warning: the text
stays unsent, pride survives the night, and the concrete change is
the first morning in months without checking her replies — the
habit breaking is the proof the moment mattered.

Stdlib only. No network, no temp files, no deletion of the output
directory. The output file is written directly and chmodded 0644
so the grader's collector (a different user) can read it.
"""

import os
import sys


# The entry itself: two lines, each exactly one sentence.
LINE_ONE = (
    "Don't send the 1:12 a.m. text to Sara that says 'I miss us' "
    "- lock the phone and let the night end."
)

LINE_TWO = (
    "Leaving it unsent meant you woke up with your pride intact, "
    "and that was the first morning in months you did not check her replies."
)

MAX_CHARS = 280


def build_entry() -> str:
    """Join the two lines with a single newline, no trailing blank line."""
    return LINE_ONE + "\n" + LINE_TWO + "\n"


def count_sentences(line: str) -> int:
    """Count sentence-ending marks, ignoring the dots in a clock time.

    "1:12 a.m." contains periods that are not sentence ends, so a
    naive count would over-count. Strip the clock abbreviation first,
    then count the remaining terminal punctuation.
    """
    cleaned = line.replace("a.m.", "am").replace("p.m.", "pm")
    return sum(1 for ch in cleaned if ch in ".!?")


def validate_entry(text: str) -> list:
    """Check the entry against the sealed gate, returning problems."""
    problems = []
    if not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    body = text.rstrip("\n")
    lines = body.split("\n")
    if len(lines) != 2:
        problems.append("entry has %d lines, expected exactly 2" % len(lines))
        return problems
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            problems.append("line %d is blank" % index)
        if count_sentences(line) != 1:
            problems.append(
                "line %d has %d sentences, expected exactly 1"
                % (index, count_sentences(line))
            )
    if lines[0].strip() == lines[1].strip():
        problems.append("the two lines must not repeat each other")
    return problems


def output_path() -> str:
    """Resolve the output directory the grader provides, default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = build_entry()
    problems = validate_entry(text)
    if problems:
        for problem in problems:
            print("invalid entry: %s" % problem, file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
    os.chmod(path, 0o644)
    print("wrote %s (%d characters, 2 lines)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
