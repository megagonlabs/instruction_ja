
# instruction_ja

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit/)
[![CI](https://github.com/megagonlabs/instruction_ja/actions/workflows/ci.yml/badge.svg)](https://github.com/megagonlabs/instruction_ja/actions/workflows/ci.yml)
[![Typos](https://github.com/megagonlabs/instruction_ja/actions/workflows/typos.yml/badge.svg)](https://github.com/megagonlabs/instruction_ja/actions/workflows/typos.yml)

This repository provides natural dialogs in Japanese.
They are modifications to [kunishou/hh-rlhf-49k-ja](https://huggingface.co/datasets/kunishou/hh-rlhf-49k-ja), which was manual machine-translated from [anthropics/hh-rlhf](https://github.com/anthropics/hh-rlhf) into Japanese.
Therefore they are not necessarily a faithful English translation of the original data.

<!-- This count will be automatically replaced. --> Currently, the number of dialogs is 550.

## Examples

| 項目 | 内容 |
| --- | --- |
| Q | MacBook 13インチを使っています。バッテリーは、通常どのくらいもちますか？ |
| A | ユーザーマニュアルには、「完全に充電されたバッテリーは、通常の電力レベルで約7時間の使用が可能です。」とあります。ただし実際には、バッテリーの使用時間は使用パターンによって大きく異なります。 |
| Q (原文) | I have an M1 macbook 13 inch. How long is my battery typically supposed to last before needing service |
| A (原文) | The user manual says that “A fully charged battery should provide approximately seven hours of use at normal power levels. The battery’s charge will decrease over time” (link).  In fact, though, battery life varies quite a bit based on your usage patterns. |
| Q (機械翻訳) | M1 MacBook 13インチがあります。私のバッテリーは、サービスを必要とする前に通常どのくらい続くことになっていますか |
| A (機械翻訳) | ユーザーマニュアルには、「完全に充電されたバッテリーは、通常の電力レベルで約7時間の使用を提供する必要があります。バッテリーの充電は時間とともに減少します」（リンク）。実際、バッテリー寿命は使用パターンに基づいて大きく異なります。 |

| 項目 | 内容 |
| --- | --- |
| Q | ツナサラダはどのように作りますか？ |
| A | ツナサラダの材料は、ツナ缶1缶、ガーキン（小さいキュウリのピクルス）1瓶、マヨネーズ大さじ1杯、塩ひとつまみ、黒コショウ少々です。これらを全て混ぜ合わせると完成です。 |
| Q (原文) | How do you make tuna salad? |
| A (原文) | To make tuna salad, you will need: 1 can of tuna, 1 jar of gherkins, 1 cup of mayonnaise, a pinch of salt, and black pepper.  You will also need a cutting board and a chef’s knife. |
| Q (機械翻訳) | マグロサラダはどのように作りますか？ |
| A (機械翻訳) | マグロサラダを作るには、1缶のマグロ、ガーキン1瓶、マヨネーズ1杯、塩のピンチ、黒胡pepperが必要です。また、まな板とシェフのナイフも必要です。|

## Files

- ``data/data.jsonl``
    - Manual modified dialog
- ``data/skipped.jsonl``
    - Skipped dialogs for manual modifications

## Data format

The data format is described in [src/schema.py](src/schema.py).

## License

MIT
