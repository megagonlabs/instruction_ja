#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import pandas as pd


def operation(
    *,
    path_in: Path,
    path_out: Path,
) -> None:
    for f in path_in.glob("**/*.parquet"):
        df = pd.read_parquet(f)
        with path_out.open("w") as outf:
            for index, row in df.iterrows():
                d = {
                    "prompt": str(row[0]),
                    "response": str(row[1]),
                    "source": f"{index}@{f}",
                }
                outf.write(json.dumps(d, ensure_ascii=False))
                outf.write("\n")


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    oparser.add_argument("--output", "-o", type=Path, default="/dev/stdout", required=False)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
    )


if __name__ == "__main__":
    main()
