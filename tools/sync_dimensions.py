"""Add leagues that exist in sportyR's surface-dimensions.json but not here.

Usage:
    python tools/sync_dimensions.py PATH/TO/sportyR/data-raw/surface-dimensions.json
    python tools/sync_dimensions.py PATH/TO/surface-dimensions.json --check

The sportyR entry text is copied verbatim (same hand-formatted layout), so
values are never retyped. Existing leagues are left alone (sportypy's classes
may depend on their current values); differences are only reported.
Keys keep sportypy's convention: sportyR's "little league" is "little_league"
here, so keys are compared with "_" and " " treated as equal. "custom" is a
sportyR-only template and is skipped.
"""
import argparse
import json
import sys
from pathlib import Path

NL = chr(10)
TARGET = Path(__file__).resolve().parents[1] / "sportypy/data/surface_dimensions.json"


def norm(key):
    return key.replace("_", " ")


def entry_text(text, sport, league):
    """Return the verbatim league block, re-indented to this file's 4-space style."""
    lines = text.split(NL)
    s = next(k for k, ln in enumerate(lines) if ln.strip() == f'"{sport}": {{')
    i = next(k for k in range(s, len(lines)) if lines[k].strip() == f'"{league}": {{')
    ind = len(lines[i]) - len(lines[i].lstrip())
    j = next(k for k in range(i, len(lines))
             if lines[k].rstrip(",") == " " * ind + "}")
    step = ind // 3  # sportyR nests league at 3 levels (root>sport>league)
    out = []
    for ln in lines[i:j + 1]:
        pad = len(ln) - len(ln.lstrip())
        out.append(" " * (8 + (pad - ind) * 4 // step) + ln.lstrip() if ln.strip() else "")
    return NL.join(out).rstrip(",")


def missing(source, target):
    return {
        sport: [lg for lg in leagues if lg != "custom"
                and norm(lg) not in {norm(k) for k in target.get(sport, {})}]
        for sport, leagues in source.items() if sport in target
    }


def add_entry(text, sport, block):
    lines = text.split("\n")
    s = lines.index(f'    "{sport}": {{')
    end = next(k for k in range(s, len(lines)) if lines[k] in ("    }", "    },"))
    prev = end - 1
    while not lines[prev].strip():
        prev -= 1
    lines[prev] = lines[prev].rstrip(",") + ","
    lines[end:end] = ["", *block.split("\n")]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sportyr_json")
    ap.add_argument("--check", action="store_true", help="exit 1 if leagues are missing; write nothing")
    args = ap.parse_args(argv)

    src_text = Path(args.sportyr_json).read_text(encoding="utf-8")
    tgt_text = TARGET.read_text(encoding="utf-8")
    source, target = json.loads(src_text), json.loads(tgt_text)

    todo = {sp: lgs for sp, lgs in missing(source, target).items() if lgs}
    for sport, leagues in todo.items():
        for lg in leagues:
            print(f"{'missing' if args.check else 'adding'}: {sport}/{lg}")
            if not args.check:
                tgt_text = add_entry(tgt_text, sport, entry_text(src_text, sport, lg))
    if args.check:
        return 1 if todo else 0
    json.loads(tgt_text)  # must still parse
    TARGET.write_text(tgt_text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
