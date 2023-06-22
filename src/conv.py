#!/usr/bin/env python3

import argparse
import csv
import json
import random
from pathlib import Path


def operation(
    *,
    path_in: Path,
    path_out: Path,
    path_done: Path,
    path_id2src: Path,
    num: int,
) -> None:
    random.seed(42)
    done = set()
    with path_done.open() as inf:
        for line in inf:
            done.add(line.strip())

    id2src = {}
    with path_id2src.open() as inf:
        for row in csv.reader(inf, delimiter="\t"):
            id2src[row[0]] = row[1]

    with path_in.open() as inf, path_out.open("w") as outf:
        d = json.load(inf)
        w = csv.writer(outf)
        z = []
        for v in d:
            tmp = [_v.strip() for _v in v.values()]
            if tmp[0] in done:
                continue
            tmp.append(id2src[tmp[0]])
            z.append(tmp)

        random.shuffle(z)
        out: int = 0
        for tmp in z:
            w.writerow(tmp)
            out += 1
            if out == num:
                break


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    oparser.add_argument("--output", "-o", type=Path, default="/dev/stdout", required=False)
    oparser.add_argument("--done", type=Path, required=True)
    oparser.add_argument("--id2src", type=Path, required=True)
    oparser.add_argument("--num", type=int, required=True, default=3000)

    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        path_done=opts.done,
        path_id2src=opts.id2src,
        num=opts.num,
    )


if __name__ == "__main__":
    main()
