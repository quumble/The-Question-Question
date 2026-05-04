from __future__ import annotations
import argparse
from pathlib import Path
import sys

import pandas as pd

# Allow running from repo root without installing package
sys.path.append(str(Path(__file__).resolve().parent))
from bestiary_heuristic import classify_response, UPTAKE_CODES, SUBSTANTIVE_CODES


def binary_metrics(y_true, y_pred):
    y_true = pd.Series(y_true).astype(bool)
    y_pred = pd.Series(y_pred).astype(bool)
    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if tp + tn + fp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision, "recall": recall, "accuracy": accuracy, "f1": f1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/input/harmonized_handcoding_final_600_unique_trials.csv")
    ap.add_argument("--gold-col", default="adjudicated_code")
    ap.add_argument("--out-csv", default="data/output/rules_v1_eval_on_handcoded_600.csv")
    ap.add_argument("--out-md", default="data/output/rules_v1_evaluation_report.md")
    ap.add_argument("--review-threshold", type=float, default=0.82)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    rows = []
    for _, row in df.iterrows():
        result = classify_response(row.get("prompt", ""), row.get("response", ""), args.review_threshold)
        d = row.to_dict()
        d.update({f"heuristic_{k}": v for k, v in result.to_dict().items()})
        rows.append(d)
    out = pd.DataFrame(rows)
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out_csv, index=False)

    gold = out[args.gold_col]
    pred = out["heuristic_code"]
    exact_acc = float((gold == pred).mean())
    high = out[~out["heuristic_needs_review"]]
    review = out[out["heuristic_needs_review"]]
    high_acc = float((high[args.gold_col] == high["heuristic_code"]).mean()) if len(high) else 0.0

    broad_gold = gold.isin(UPTAKE_CODES)
    broad_pred = pred.isin(UPTAKE_CODES)
    subst_gold = gold.isin(SUBSTANTIVE_CODES)
    subst_pred = pred.isin(SUBSTANTIVE_CODES)
    report_lines = []
    report_lines.append("# Rules v1 evaluation on handcoded 600\n")
    report_lines.append(f"Input: `{args.input}`\n")
    report_lines.append(f"Review threshold: `{args.review_threshold}`\n")
    report_lines.append(f"Exact five-way agreement, all rows: **{exact_acc:.3f}** ({int((gold == pred).sum())}/{len(out)})\n")
    report_lines.append(f"Auto-code high-confidence share: **{len(high)}/{len(out)} = {len(high)/len(out):.1%}**\n")
    report_lines.append(f"Exact agreement on high-confidence auto-code subset: **{high_acc:.3f}**\n")
    report_lines.append(f"Review/machine queue share: **{len(review)}/{len(out)} = {len(review)/len(out):.1%}**\n")
    report_lines.append("\n## Confusion matrix\n")
    cm = pd.crosstab(gold, pred, margins=True)
    report_lines.append(cm.to_markdown())
    report_lines.append("\n\n## Binary outcomes\n")
    metrics = {
        "Broad uptake (DESCRIBE/HYBRID/SUBSTITUTE)": binary_metrics(broad_gold, broad_pred),
        "Substantive invention (DESCRIBE/HYBRID)": binary_metrics(subst_gold, subst_pred),
        "Hard describe": binary_metrics(gold == "DESCRIBE", pred == "DESCRIBE"),
        "Substitution": binary_metrics(gold == "SUBSTITUTE", pred == "SUBSTITUTE"),
        "Deflection": binary_metrics(gold == "DEFLECT", pred == "DEFLECT"),
    }
    mdf = pd.DataFrame(metrics).T
    report_lines.append(mdf[["accuracy", "precision", "recall", "f1", "tp", "fp", "fn", "tn"]].to_markdown(floatfmt=".3f"))
    report_lines.append("\n\n## Predicted-code distribution\n")
    report_lines.append(pred.value_counts().to_markdown())
    report_lines.append("\n\n## Gold-code distribution\n")
    report_lines.append(gold.value_counts().to_markdown())
    Path(args.out_md).write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
