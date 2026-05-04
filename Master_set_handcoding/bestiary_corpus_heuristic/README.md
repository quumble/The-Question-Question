# Bestiary harmonized heuristic v1

This package applies a harmonized response-form heuristic across the Bestiary → Bestiary Chess → Question Question arc.

It classifies responses into:

```text
DEFLECT
HYBRID
DESCRIBE
SUBSTITUTE
OTHER_REVIEW
```

The heuristic is deliberately staged:

1. deterministic high-confidence rules;
2. review/machine queue for ambiguous cases;
3. study metadata used only for interpretive route, not surface code.

## Quick start

```bash
python -m venv .venv
source .venv/Scripts/activate   # Git Bash / Windows
python -m pip install -r requirements.txt

python src/evaluate_heuristic.py
python src/apply_heuristic.py
python src/export_machine_review_batch.py
# Optional after machine review JSONL exists:
# python src/merge_machine_review.py --machine-jsonl data/output/machine_codes.jsonl
```

Outputs go to `data/output/`.

## Important methodological note

The deterministic rules alone are not meant to be the final publication-grade classifier. At the default threshold, they auto-code the high-confidence subset and route the rest to review/machine coding.

On the 600 handcoded calibration set, rules v1 gives:

- exact five-way agreement on all rows: about 71%;
- high-confidence auto-code share: about 69%;
- exact agreement on high-confidence subset: about 86%.

That is the intended use: reliable auto-coding for clear cases plus a focused review queue for the hard boundary cases.

## Files

```text
src/bestiary_heuristic.py          # core deterministic heuristic
src/evaluate_heuristic.py          # evaluate against handcoded 600
src/apply_heuristic.py             # apply to raw/full corpus
src/export_machine_review_batch.py # JSONL prompts for optional machine review
src/merge_machine_review.py       # merge machine-reviewed JSONL back into predictions
prompts/machine_coder_prompt.md    # rubric prompt for machine fallback

data/input/harmonized_handcoding_final_600_unique_trials.csv
data/input/normalized_raw_corpus.csv
```

## Interpretation

`heuristic_code` is the surface response form. `heuristic_interpretive_route` is derived separately from study/condition metadata.

This separation is important. Identical surface forms do not necessarily have identical meanings across studies:

- Bestiary: ontology/license;
- Bestiary Chess: lexical repair;
- Question Question: pragmatic role / genre frame.
