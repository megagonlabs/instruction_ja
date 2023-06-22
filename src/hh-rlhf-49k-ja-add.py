#!/usr/bin/env python3

import argparse
import gzip
import json
from collections import defaultdict
from pathlib import Path
from typing import Optional


def operation(
    *,
    path_in: Path,
    path_ref: Path,
    path_dolly: Optional[Path],
    path_out: Path,
) -> None:
    key2id = defaultdict(list)
    if path_dolly:
        with path_dolly.open() as inf:
            for line in inf:
                d = json.loads(line)
                prefix: str = (
                    "Below is an instruction that describes a task."
                    + " Write a response that appropriately completes the request.\n\n### Instruction:\n"
                )
                assert d["prompt"].startswith(prefix), d["prompt"]
                q: str = d["prompt"].replace(prefix, "").split("###")[0].strip().replace("\n", "")
                a: str = d["response"].strip().replace("\n", "")
                key = (q, a)
                # assert key not in key2id, line
                key2id[key].append(d["source"])

    for en_f in path_ref.glob("**/*.gz"):
        if en_f.parent.name == "red-team-attempts":
            continue
        with gzip.open(en_f) as rf:
            fname: str = str(en_f).replace("src/", "")
            for lid, line in enumerate(rf):
                c: str = json.loads(line)["chosen"].strip().split("Human: ")
                q = c[1].split("Assistant:")[0].strip().replace("\n", "")
                a = c[1].split("Assistant:")[1].strip().replace("\n", "")
                key = (q, a)
                _id: str = f"{lid+1}@{fname}"
                #                     assert key not in key2id
                key2id[key].append(_id)

    with path_in.open() as inf, path_out.open("w") as outf:
        ja_ds = json.load(inf)
        for item in ja_ds:
            q = item["instruction_en"].strip().replace("\n", "")
            a = item["output_en"].strip().replace("\n", "")
            key = (q, a)
            _ids = key2id.get(key, None)
            _ids_str = json.dumps(_ids)
            outf.write(f'{item["index"]}\t{_ids_str}\n')


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, required=True)
    oparser.add_argument("--ref", "-r", type=Path, required=True)
    oparser.add_argument("--dolly", "-d", type=Path, required=False)
    oparser.add_argument("--output", "-o", type=Path, default="/dev/stdout", required=False)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_ref=opts.ref,
        path_dolly=opts.dolly,
        path_out=opts.output,
    )


if __name__ == "__main__":
    main()
