# Naturalist Loophole crossover completion run

This bundle creates the missing 2×2 crossover cells for QQ-v1 / Naturalist Loophole.

## Why this exists

The completed QQ-v1 run paired model family and word set:

| Word set | GPT models | Claude models |
|---|---:|---:|
| GPT-authored words | already run | missing |
| Claude-authored words | missing | already run |

That means the original architecture-family contrast is partially confounded with stimulus set. The within-GPT naturalist effect is still clean, and the within-Claude floor effect is still clean, but the cross-family claim needs the missing cells.

This bundle adds:

- Claude-family models on the 12 GPT-authored words
- GPT-family models on the Claude-authored words, excluding `flürbenheim` because the prior run had mojibake (`flÃ¼rbenheim`)

At 6 reps, this is 2,070 added trials.

## Files

- `frames_crossover_missing_no_flurbenheim.csv` — run this to add only the missing cells.
- `frames_balanced_no_flurbenheim.csv` — full balanced design excluding `flürbenheim`, useful for checking row counts and future full reruns.
- `runner_crossover.py` — original runner patched so `--arch` filters by `model_family` rather than `word_author`.
- `qq_heuristic_v3_1.py` — current deployed heuristic.
- `code_jsonl_with_v3_1.py` — codes new JSONL output with v3.1.

## Smoke test

```bash
python runner_crossover.py --frames frames_crossover_missing_no_flurbenheim.csv --dry-run
python runner_crossover.py --frames frames_crossover_missing_no_flurbenheim.csv --limit 6 --out results/crossover_smoke.jsonl
```

## Full missing-cell run

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...

python runner_crossover.py   --frames frames_crossover_missing_no_flurbenheim.csv   --reps 6   --out results/qq_crossover_missing_no_flurbenheim.jsonl   --resume
```

Expected plan:

```text
345 frame-rows × 6 reps = 2,070 trials
```

## Code the new run

```bash
python code_jsonl_with_v3_1.py   results/qq_crossover_missing_no_flurbenheim.jsonl   qq_crossover_missing_no_flurbenheim_v3_1_full.jsonl
```

## Combining with the original run

For publication analyses excluding `flürbenheim`, combine:

1. original `qq_v1_v3_1_full.jsonl`, filtering out any rows with `word == "flürbenheim"` or prompt/word containing `flÃ¼rbenheim`
2. new `qq_crossover_missing_no_flurbenheim_v3_1_full.jsonl`

The resulting balanced no-flürbenheim dataset should have:

```text
23 words × 5 frames × 6 models × 6 reps = 4,140 trials
```

Then analyze as a 2 word-author × 2 model-family × 5 frame design.
