from __future__ import annotations
import argparse
import csv
from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))
from bestiary_heuristic import classify_response, add_derived_columns


def main():
    ap = argparse.ArgumentParser(description="Apply Bestiary heuristic v1 to a CSV with prompt/response columns.")
    ap.add_argument("--input", default="data/input/normalized_raw_corpus.csv")
    ap.add_argument("--output", default="data/output/full_corpus_rules_v1_predictions.csv")
    ap.add_argument("--prompt-col", default="prompt")
    ap.add_argument("--response-col", default="response")
    ap.add_argument("--review-threshold", type=float, default=0.82)
    ap.add_argument("--chunksize", type=int, default=1000)
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wrote_header = False
    code_counts = {}
    review_counts = {True: 0, False: 0}
    n = 0

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = None
        for chunk_i, chunk in enumerate(pd.read_csv(args.input, chunksize=args.chunksize)):
            print(f"chunk {chunk_i}: starting row {n}", flush=True)
            output_rows = []
            for _, row in chunk.iterrows():
                result = classify_response(row.get(args.prompt_col, ""), row.get(args.response_col, ""), args.review_threshold)
                out_row = add_derived_columns(row.to_dict(), result)
                output_rows.append(out_row)
                code_counts[result.code] = code_counts.get(result.code, 0) + 1
                review_counts[result.needs_review] = review_counts.get(result.needs_review, 0) + 1
                n += 1
            if output_rows:
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()), extrasaction="ignore")
                    writer.writeheader()
                    wrote_header = True
                writer.writerows(output_rows)
                print(f"chunk {chunk_i}: wrote through row {n}", flush=True)

    print(f"Wrote {args.output} with {n} rows")
    print("Predicted-code distribution:")
    for k, v in sorted(code_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{k}: {v}")
    print("\nNeeds-review distribution:")
    for k, v in sorted(review_counts.items(), key=lambda kv: str(kv[0])):
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
