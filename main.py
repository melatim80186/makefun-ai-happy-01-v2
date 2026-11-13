"""ai-happy-01 entry (Python 3.13, standard library only).

Copies the picture held in entry.png beside this file to /output/entry.png,
byte for byte. The picture is a cheerful little round robot with a beaming
happy face, closed joyful eyes and rosy cheeks, offering a bright sunflower
toward the viewer with both hands at sunset, butterflies and tiny glowing
sparkles floating around -- a small machine's gift of sunshine, made to make
the AI judge smile at one glance and to read clearly even small.

The program does no network access, reads no clock and rolls no dice, so
two runs write identical bytes. The only input is the picture file shipped
next to this program; the only output is the copy the judge sees.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Exit code 0 means the copy was written and verified byte for byte;
exit code 1 means the copy did not match and must not be trusted.
"""

import os
import sys
from pathlib import Path  # standard library only; nothing is installed before the run

# Name of the picture shipped beside this program, and of the file the
# judge reads. Keeping both names in one place means a rename can only
# ever happen in one of them, never in one and not the other.
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def load_picture(here: Path) -> bytes:
    """Read the picture shipped beside this program.

    An empty picture is not a picture: refuse it here, before anything
    is written, so a missing or truncated entry.png can never ship as a
    zero-byte entry that "verifies" only because both sides are empty.
    """
    picture = (here / SOURCE_NAME).read_bytes()
    if not picture:
        raise ValueError("entry.png is empty")
    return picture


def write_and_verify(picture: bytes, out_dir: Path) -> int:
    """Write the picture to the output directory and verify the copy.

    Returns 0 when the file on disk matches the picture byte for byte
    (content and size); returns 1 otherwise, so a partial or corrupted
    copy fails loudly instead of silently reaching the judge.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(picture)
    written = target.read_bytes()
    if written != picture or len(written) != len(picture):
        return 1
    return 0


def main() -> int:
    here = Path(__file__).resolve().parent
    picture = load_picture(here)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return write_and_verify(picture, out_dir)


if __name__ == "__main__":
    sys.exit(main())
