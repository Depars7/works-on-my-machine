"""Write one funny developer excuse to /output/entry.txt.

Standard library only. The file's content is exactly the excuse's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be a single line of 1-200
characters, so the excuse is validated before it is written.
"""

import os

EXCUSE = (
    "Don't blame the deploy \u2014 the bug was already in production; "
    "I just finally gave it users."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line):
    """The bounty gate: one line, 1-200 characters, non-blank."""
    if not 1 <= len(line) <= 200:
        raise ValueError("entry must be 1-200 characters")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    # Exactly one line: no newline or carriage return anywhere, and
    # no leading/trailing whitespace the gate would count against
    # the line as written.
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    return line


def write_entry(line):
    """Write the line's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(line.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(EXCUSE)
    write_entry(line)


if __name__ == "__main__":
    main()
