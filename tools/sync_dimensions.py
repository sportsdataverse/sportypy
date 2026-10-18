"""Add leagues that exist in sportyR's surface-dimensions.json but not here.

Usage:
    python tools/sync_dimensions.py PATH/TO/sportyR/data-raw/surface-dimensions.json
    python tools/sync_dimensions.py PATH/TO/surface-dimensions.json --check

The sportyR entry text is copied verbatim (same hand-formatted layout), so
values are never retyped. Existing leagues are left alone (sportypy's classes
may depend on their current values); for leagues present in both, every key
whose value differs is printed as "drift: sport/league/key: sportypy vs
sportyR" (information only; the exit code is unchanged). A sport absent from
sportypy is warned about and skipped.
Keys keep sportypy's convention: sportyR's "little league" is "little_league"
here, so keys are compared with "_" and " " treated as equal. "custom" is a
sportyR-only template and is skipped. ``--add-sport SPORT`` creates a sport
sportypy lacks (first league written there, the rest by the normal path).
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
    nxt = next(ln for ln in lines[i + 1:j] if ln.strip())
    step = len(nxt) - len(nxt.lstrip()) - ind  # sportyR's indent width varies by sport
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


def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(flat(v, f"{prefix}{k}/"))
        else:
            out[f"{prefix}{k}"] = v
    return out


def drift(source, target):
    """Yield (sport, league, key, sportypy_value, sportyr_value) differences."""
    for sport, leagues in source.items():
        if sport not in target:
            continue
        mine = {norm(k): v for k, v in target[sport].items()}
        for lg, entry in leagues.items():
            if norm(lg) not in mine:
                continue
            a, b = flat(mine[norm(lg)]), flat(entry)
            for key in sorted(set(a) | set(b)):
                if a.get(key, "<absent>") != b.get(key, "<absent>"):
                    yield sport, lg, key, a.get(key, "<absent>"), b.get(key, "<absent>")


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


def add_sport(text, sport, block):
    """Append a new sport holding one league block (the file ends in a closing brace)."""
    body = text.rstrip()
    assert body.endswith("}")
    return body[:-1].rstrip() + f',{NL}{NL}    "{sport}": {{{NL}{block}{NL}    }}{NL}}}'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sportyr_json")
    ap.add_argument("--check", action="store_true", help="exit 1 if leagues are missing; write nothing")
    ap.add_argument("--add-sport", action="append", default=[], metavar="SPORT",
                    help="also create this sport (absent from sportypy) from sportyR; write mode only")
    args = ap.parse_args(argv)
    if args.add_sport and args.check:
        ap.error("--add-sport cannot be combined with --check")

    src_text = Path(args.sportyr_json).read_text(encoding="utf-8")
    tgt_text = TARGET.read_text(encoding="utf-8")
    source, target = json.loads(src_text), json.loads(tgt_text)

    for sport in args.add_sport:
        if sport not in source:
            ap.error(f"sport '{sport}' is not in {args.sportyr_json}")
        leagues = [lg for lg in source[sport] if lg != "custom"]
        if sport in target or not leagues:
            continue
        print(f"adding sport: {sport}/{leagues[0]}")
        tgt_text = add_sport(tgt_text, sport, entry_text(src_text, sport, leagues[0]))
        target = json.loads(tgt_text)

    for sport in source:
        if sport not in target:
            print(f"warning: sport '{sport}' absent from sportypy; skipped")
    for sport, lg, key, mine, theirs in drift(source, target):
        print(f"drift: {sport}/{lg}/{key}: {mine!r} vs {theirs!r}")

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
