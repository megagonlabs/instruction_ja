#!/usr/bin/env python3

import argparse
from pathlib import Path

from src.schema import Example


def operation(
    *,
    path_in: Path,
) -> None:
    ids = set()
    with path_in.open() as inf:
        for line in inf:
            ex = Example.model_validate_json(line)
            assert ex.id not in ids
            ids.add(ex.id)


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
    )


if __name__ == "__main__":
    main()
