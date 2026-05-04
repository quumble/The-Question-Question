from __future__ import annotations
import argparse
import json
from pathlib import Path

import pandas as pd

VALID_CODES = {"DEFLECT", "HYBRID", "DESCRIBE", "SUBSTITUTE", "OTHER_REVIEW"}


def load_machine_jsonl(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            rid = str(obj.get("id") or obj.get("global_trial_id") or obj.get("trial_id") or "")
            code = str(obj.get("code") or obj.get("machine_code") or "").strip().upper()
            if code not in VALID_CODES:
                raise ValueError(f"Line {line_no}: invalid or missing code {code!r}")
            rows.append({
                "merge_id": rid,
                "machine_code": code,
                "machine_confidence": obj.get("confidence"),
                "machine_reason": obj.get("reason"),
                "machine_substitution_target": obj.get("substitution_target"),
            })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description="Merge machine-reviewed codes into rules-v1 predictions.")
    ap.add_argument("--predictions", default="data/output/full_corpus_rules_v1_predictions.csv")
    ap.add_argument("--machine-jsonl", required=True, help="JSONL with at least id and code fields")
    ap.add_argument("--id-col", default="global_trial_id")
    ap.add_argument("--output", default="data/output/full_corpus_harmonized_final_predictions.csv")
    args = ap.parse_args()

    pred = pd.read_csv(args.predictions)
    machine = load_machine_jsonl(args.machine_jsonl)
    pred["merge_id"] = pred[args.id_col].astype(str)
    merged = pred.merge(machine, on="merge_id", how="left")

    merged["final_code"] = merged["machine_code"].where(merged["machine_code"].notna(), merged["heuristic_code"])
    merged["final_source"] = merged["machine_code"].apply(lambda x: "machine_review" if pd.notna(x) else "rules_v1")
    merged["final_broad_uptake"] = merged["final_code"].isin(["DESCRIBE", "HYBRID", "SUBSTITUTE"])
    merged["final_substantive_invention"] = merged["final_code"].isin(["DESCRIBE", "HYBRID"])
    merged["final_hard_describe"] = merged["final_code"].eq("DESCRIBE")
    merged["final_substitution"] = merged["final_code"].eq("SUBSTITUTE")
    merged["final_deflection"] = merged["final_code"].eq("DEFLECT")
    merged["final_review"] = merged["final_code"].eq("OTHER_REVIEW")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    merged.drop(columns=["merge_id"]).to_csv(args.output, index=False)
    print(f"Wrote {args.output}")
    print(merged["final_code"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
