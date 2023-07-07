#!/usr/bin/env python3

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from src.schema import Example, OriginalInfo, Source, Utterance


def operation(
    *,
    path_in: Path,
    path_out: Path,
    path_id2src: Path,
) -> None:
    path_out.mkdir(exist_ok=True, parents=True)

    id2srcs: dict[int, list[Source]] = {}
    with path_id2src.open() as inf:
        for items in csv.reader(inf, delimiter="\t"):
            _id = int(items[0])
            srcs: list[str] = json.loads(items[1])
            if srcs is None:
                continue
            id2srcs[_id] = []
            for s in srcs:
                kv = s.split("@")
                id2srcs[_id].append(
                    Source(
                        path=kv[1],
                        line_index=int(kv[0]),
                    )
                )

    with path_in.open() as inf, path_out.joinpath("data.jsonl").open("w") as okf, path_out.joinpath(
        "skipped.jsonl"
    ).open("w") as skipf:
        ok_ids = set()
        r = csv.reader(inf)
        header = next(r)
        idx_q = header.index("日本語Q")
        idx_a = header.index("日本語A")
        idx_en_q = header.index("instruction_en")
        idx_en_a = header.index("output_en")
        idx_q_org = header.index("(original)日本語Q")
        idx_a_org = header.index("(original)日本語A")
        idx_memo = header.index("メモ")

        out_exs = []
        for items in r:
            ok: bool = items[3] == "o" and items[4] == "o"
            skip: bool = items[3] == "x"
            if not ok and not skip:
                continue

            q: str = items[idx_q].strip()
            a: str = items[idx_a].strip()
            ctx = [
                Utterance(name="user", text=q),
                Utterance(name="agent", text=a),
            ]

            en_q: str = items[idx_en_q]
            en_a: str = items[idx_en_a]
            en_ctx = [
                Utterance(name="user", text=en_q),
                Utterance(name="agent", text=en_a),
            ]

            ja_q: str = items[idx_q_org]
            ja_a: str = items[idx_a_org]
            org_ja_ctx = [
                Utterance(name="user", text=ja_q),
                Utterance(name="agent", text=ja_a),
            ]

            _idx: int = int(items[0])
            myid: str = f"instruction_ja.{_idx:06}"
            if ok:
                ok_ids.add(myid)

            meta: dict[str, Any] = {
                "original_id": _idx,
            }
            memo: str = items[idx_memo].strip().rstrip("。")
            if len(memo) > 0:
                meta["memo"] = memo

            src = id2srcs.get(_idx)
            if src is None:
                print(f"skip (no source id): {_idx}")
                continue
            ex = Example(
                id=myid,
                utterances=ctx,
                original_info=OriginalInfo(
                    utterances={
                        "en": en_ctx,
                        "machine_translated_ja": org_ja_ctx,
                    },
                    sources=src,
                ),
                meta=meta,
            )
            out_exs.append(ex)

        for ex in sorted(out_exs, key=lambda x: x.id):
            _outf = okf
            if ex.id not in ok_ids:
                _outf = skipf
                ex.utterances = []  # clear
            _outf.write(json.dumps(ex.model_dump(), ensure_ascii=False))
            _outf.write("\n")


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", type=Path, default="/dev/stdin", required=False)
    oparser.add_argument("--output", "-o", type=Path, default="/dev/stdout", required=False)
    oparser.add_argument("--id2src", type=Path, required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        path_in=opts.input,
        path_out=opts.output,
        path_id2src=opts.id2src,
    )


if __name__ == "__main__":
    main()
