from __future__ import annotations
import argparse
import json
from pathlib import Path

import pandas as pd

SYSTEM_PROMPT_PATH = Path("prompts/machine_coder_prompt.md")


def main():
    ap = argparse.ArgumentParser(description="Export low-confidence heuristic cases as JSONL prompts for external/machine coding.")
    ap.add_argument("--input", default="data/output/full_corpus_rules_v1_predictions.csv")
    ap.add_argument("--output", default="data/output/machine_review_queue.jsonl")
    ap.add_argument("--only-needs-review", action="store_true", default=True)
    ap.add_argument("--max-rows", type=int, default=0, help="0 means all")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    if args.only_needs_review and "heuristic_needs_review" in df.columns:
        df = df[df["heuristic_needs_review"].astype(bool)]
    if args.max_rows and args.max_rows > 0:
        df = df.head(args.max_rows)

    prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8") if SYSTEM_PROMPT_PATH.exists() else "Classify the response."
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for i, row in df.iterrows():
            rid = row.get("global_trial_id", row.get("trial_id", i))
            payload = {
                "id": str(rid),
                "study": row.get("study", ""),
                "condition": row.get("condition", ""),
                "word": row.get("word", ""),
                "prompt": row.get("prompt", ""),
                "response": row.get("response", ""),
                "current_rule_code": row.get("heuristic_code", ""),
                "current_rule_reason": row.get("heuristic_reason", ""),
                "instruction": prompt,
            }
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    print(f"Wrote {args.output} with {len(df)} rows")


if __name__ == "__main__":
    main()
