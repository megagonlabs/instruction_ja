
# Conversion

```bash
git submodule update --init

# Get data source
poetry run python ./src/hh-rlhf-49k-ja-add.py \
    --ref ./src/hh-rlhf \
    -i ./src/hh-rlhf-49k-ja/mpt_hhrlhf_49k_ja.json \
    -o ./src/id2src.tsv

# Make worksheet 
python ./src/conv.py \
    -i ./src/hh-rlhf-49k-ja/mpt_hhrlhf_49k_ja.json \
    --done ./_done.txt \
    --id2src ./src/id2src.tsv \
    -o sheet.csv \
    -num 3000

# Make annotion :-D

# Convert to json
poetry run python -m src.generate -i ./sheet.csv -o data --id2src ./src/id2src.tsv
```

## Optional

We do not use this part.

```bash
poetry run python ./dolly_hhrlhf_convert.py \
    -i ./dolly_hhrlhf/data/ \
    -o ./dolly_hhrlhf.jsonl
```
