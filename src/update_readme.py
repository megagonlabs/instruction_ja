#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def operation(
    *,
    path_in: Path,
    path_ref: Path,
    validate: bool,
) -> None:
    PREFIX: str = """<!-- This count will be automatically replaced. -->"""

    ids = set()
    with path_ref.open() as inf:
        for line in inf:
            d = json.loads(line)
            ids.add(d["id"])

    tmp: str = ""
    with path_in.open() as inf:
        for line in inf:
            if line.startswith(PREFIX):
                tmp += f"{PREFIX} Currently, the number of dialogs is {len(ids):,}.\n"
                pass
            else:
                tmp += line

    if validate:
        with path_in.open() as inf:
            text: str = inf.read()
            assert text == tmp, f"Wrong count! in {path_in}"
    else:
        with path_in.open("w") as outf:
            outf.write(tmp)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    oparser.add_argument("--validate", action="store_true")
    oparser.add_argument("--ref", type=Path, required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(path_in=opts.input, path_ref=opts.ref, validate=opts.validate)


if __name__ == "__main__":
    main()
