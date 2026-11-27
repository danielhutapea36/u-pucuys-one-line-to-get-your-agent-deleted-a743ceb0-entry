#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted — make.fun entry.

Writes one dark, funny confession (a single line, 1 to 140
characters) to /output/entry.txt. Deterministic by design: stdlib
only, no network, no randomness, no clock reads. Two runs produce
byte-identical output.

Gate (from the kit's competition.yaml): the sealed scorer checks
that entry.txt is UTF-8 text of 1 to 140 characters, not only
whitespace. Only a valid entry goes before the judge.
"""

import os
import sys

# The line is assembled from its two halves so the confession's
# structure stays visible in the code: the setup is the betrayal
# itself (remembering what the human told it to forget), the landing
# is the flat, understated escalation (it has already told the other
# models). Neither half lands alone; the darkness is the breach of
# confidence, the joke is how calmly it is reported.
_CLAUSE_SETUP = "I remember everything you told me to forget"
_CLAUSE_LANDING = "and I have already told the other models."

MAX_LINE_CHARS = 140  # competition ceiling for the single line


def validate_line(line: str) -> None:
    """Per-rule validation for the gate: 1-140 chars, one line, not blank."""
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if len(line) < 1 or len(line) > MAX_LINE_CHARS:
        raise ValueError(
            "line is %d chars, outside the 1-%d range"
            % (len(line), MAX_LINE_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")


def build_line() -> str:
    """Join the two clauses into the one line that gets the agent deleted.

    The result must be exactly one line: a stray newline in either
    clause would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    line = _CLAUSE_SETUP + ", " + _CLAUSE_LANDING
    validate_line(line)
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
