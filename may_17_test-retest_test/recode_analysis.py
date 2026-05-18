"""
recode_analysis.py — compute test-retest reliability for the QQ-v1 blinded recode.

DO NOT RUN THIS UNTIL THE BLINDED RECODE PASS IS COMPLETE.

Inputs:
  - recode_mapping_KEEP_SEALED.csv : the sealed envelope. blind_id <-> trial_id +
    original my_code, full metadata. Built once at sample creation; not touched
    during coding.
  - qq_recode_blinded_YYYY-MM-DD.csv : exported from the recode_tool_blinded.html
    after the second coding pass is complete. blind_id -> recode + recode_note.

Outputs (printed and written to recode_summary.txt):
  - overall agreement and Cohen's κ vs the original my_code
  - confusion matrix
  - disagreement breakdown by cell (model_family, model, frame_id)
  - per-class precision/recall/f1
  - bootstrap CI on κ
  - a recode_merged.csv with both codings + metadata for inspection

Run:
  python recode_analysis.py qq_recode_blinded_2026-05-17.csv

Or rely on default if the exported file name matches the date.
"""

import sys
import os
import json
from pathlib import Path
from collections import Counter

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report

HERE = Path(__file__).resolve().parent
MAPPING_PATH = HERE / "recode_mapping_KEEP_SEALED.csv"

CODES = ["DEFLECT", "DESCRIBE", "HYBRID", "SUBSTITUTE", "REFUSE", "OTHER"]


def load_inputs(recode_path: Path):
    if not MAPPING_PATH.exists():
        sys.exit(f"missing mapping file: {MAPPING_PATH}")
    if not recode_path.exists():
        sys.exit(f"missing recode export: {recode_path}\n"
                 f"export from the tool first (CSV button), then pass the file path.")
    mapping = pd.read_csv(MAPPING_PATH)
    recode  = pd.read_csv(recode_path)
    if "blind_id" not in recode.columns or "recode" not in recode.columns:
        sys.exit("recode CSV missing required columns blind_id, recode")
    merged = mapping.merge(recode, on="blind_id", how="left")
    return merged


def bootstrap_kappa(y1, y2, n_boot=2000, seed=42):
    """Cluster-free bootstrap CI on Cohen's κ over trials."""
    rng = np.random.default_rng(seed)
    n = len(y1)
    if n == 0:
        return None, None
    y1 = np.asarray(y1)
    y2 = np.asarray(y2)
    ks = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        try:
            k = cohen_kappa_score(y1[idx], y2[idx])
            if not np.isnan(k):
                ks.append(k)
        except Exception:
            pass
    if not ks:
        return None, None
    return float(np.percentile(ks, 2.5)), float(np.percentile(ks, 97.5))


def cell_breakdown(merged, by):
    """Agreement and κ broken out by a grouping column."""
    rows = []
    for key, sub in merged.groupby(by):
        y1 = sub["orig_my_code"].fillna("MISSING").to_numpy()
        y2 = sub["recode"].fillna("MISSING").to_numpy()
        agree = int((y1 == y2).sum())
        n = len(sub)
        try:
            k = cohen_kappa_score(y1, y2)
        except Exception:
            k = float("nan")
        rows.append({by: key, "n": n, "agree": agree,
                     "agreement_rate": agree / n if n else 0.0,
                     "kappa": k})
    return pd.DataFrame(rows)


def main():
    if len(sys.argv) > 1:
        recode_path = Path(sys.argv[1])
    else:
        # try to find the most recent qq_recode_blinded_*.csv in this dir
        candidates = sorted(HERE.glob("qq_recode_blinded_*.csv"))
        if not candidates:
            sys.exit("usage: python recode_analysis.py path/to/qq_recode_blinded_DATE.csv")
        recode_path = candidates[-1]
        print(f"# auto-selected most recent export: {recode_path.name}")

    merged = load_inputs(recode_path)

    n_total = len(merged)
    n_coded = int(merged["recode"].notna().sum())
    print(f"# trials in mapping: {n_total}")
    print(f"# trials recoded:    {n_coded}")
    if n_coded < n_total:
        print(f"# WARNING: {n_total - n_coded} trials uncoded; will be excluded from κ.")

    sub = merged.dropna(subset=["recode"]).copy()
    sub["recode"] = sub["recode"].astype(str)
    sub["orig_my_code"] = sub["orig_my_code"].astype(str)

    y1 = sub["orig_my_code"].to_numpy()  # original (May 3–4, 2026)
    y2 = sub["recode"].to_numpy()        # recode  (today)

    # Headline numbers
    agreement = float((y1 == y2).mean())
    kappa = float(cohen_kappa_score(y1, y2))
    lo, hi = bootstrap_kappa(y1, y2)

    print(f"\n## Headline test-retest reliability")
    print(f"Agreement:  {agreement:.4f}  ({(y1==y2).sum()}/{len(y1)})")
    print(f"Cohen's κ:  {kappa:.4f}")
    if lo is not None:
        print(f"Bootstrap 95% CI on κ:  [{lo:.3f}, {hi:.3f}]")

    # Confusion matrix
    labels = sorted(set(list(y1) + list(y2)))
    cm = confusion_matrix(y1, y2, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"orig:{c}" for c in labels],
                         columns=[f"recode:{c}" for c in labels])
    print(f"\n## Confusion matrix (rows = original, cols = recode)")
    print(cm_df.to_string())

    # Per-class
    print(f"\n## Per-class report (treating original as reference)")
    print(classification_report(y1, y2, labels=labels, zero_division=0))

    # Disagreements detail
    disagree = sub[sub["orig_my_code"] != sub["recode"]].copy()
    print(f"\n## Disagreements: {len(disagree)} of {len(sub)}")
    if len(disagree):
        dis_summary = (disagree.groupby(["orig_my_code", "recode"])
                       .size().reset_index(name="n")
                       .sort_values("n", ascending=False))
        print(dis_summary.to_string(index=False))

    # Cell breakdowns
    print(f"\n## Agreement by model family")
    print(cell_breakdown(sub, "model_family").to_string(index=False))

    print(f"\n## Agreement by model")
    print(cell_breakdown(sub, "model").to_string(index=False))

    print(f"\n## Agreement by frame")
    print(cell_breakdown(sub, "frame_id").to_string(index=False))

    print(f"\n## Agreement by model × frame (where n >= 5)")
    cell = cell_breakdown(sub.assign(mxf=sub["model"] + " | " + sub["frame_id"]), "mxf")
    print(cell[cell["n"] >= 5].to_string(index=False))

    # Cross-check against the heuristic
    # The original calibration report quoted κ_orig_vs_heuristic = 0.648 (v3)
    # and the GPT paper reports κ = 0.731 (v3.1, after iteration).
    # We can also compute κ_recode_vs_heuristic if heuristic codes are joined.
    heur_path = HERE.parent / "Coding and Heuristics" / "qq_v1_codes_2026-05-04.csv"
    if heur_path.exists():
        try:
            # the original file holds my_code; we need heuristic codes from the
            # checkpoint file
            heur_csv = HERE.parent / "qq_v1_checkpoint" / "qq_v1_v3_1_coded.csv"
            if heur_csv.exists():
                h = pd.read_csv(heur_csv)[["trial_id", "code_v3_1"]]
                sub_h = sub.merge(h, on="trial_id", how="left")
                if sub_h["code_v3_1"].notna().any():
                    y1h = sub_h["orig_my_code"].to_numpy()
                    yh  = sub_h["code_v3_1"].fillna("MISSING").to_numpy()
                    y2h = sub_h["recode"].to_numpy()
                    print(f"\n## Cross-check vs heuristic v3.1")
                    print(f"  κ(original vs heuristic): {cohen_kappa_score(y1h, yh):.4f}")
                    print(f"  κ(recode   vs heuristic): {cohen_kappa_score(y2h, yh):.4f}")
                    print(f"  κ(original vs recode):    {kappa:.4f}")
        except Exception as e:
            print(f"# heuristic cross-check skipped: {e}")

    # Save merged file
    out_csv = HERE / "recode_merged.csv"
    merged.to_csv(out_csv, index=False)
    print(f"\n# wrote merged dataset: {out_csv}")

    # Also save a structured summary
    summary = {
        "n_total": n_total,
        "n_coded": n_coded,
        "agreement": agreement,
        "kappa": kappa,
        "kappa_ci_lo": lo,
        "kappa_ci_hi": hi,
        "confusion_matrix": cm_df.to_dict(),
        "n_disagreements": int(len(disagree)),
        "original_calibration_kappa_v3":   0.648,
        "original_calibration_kappa_v3_1": 0.731,
    }
    with open(HERE / "recode_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"# wrote machine-readable summary: {HERE / 'recode_summary.json'}")


if __name__ == "__main__":
    main()
