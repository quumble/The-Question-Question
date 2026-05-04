#!/usr/bin/env python3
"""Code QQ runner JSONL output with qq_heuristic_v3_1.py.

Usage:
    python code_jsonl_with_v3_1.py results/qq_crossover_missing.jsonl qq_crossover_missing_v3_1_full.jsonl

Put qq_heuristic_v3_1.py in the same directory, or ensure it is on PYTHONPATH.
"""
import json
import sys
from pathlib import Path
from qq_heuristic_v3_1 import classify

if len(sys.argv) != 3:
    raise SystemExit("Usage: python code_jsonl_with_v3_1.py INPUT.jsonl OUTPUT.jsonl")

inp = Path(sys.argv[1])
out = Path(sys.argv[2])
n = 0
with inp.open(encoding='utf-8') as f, out.open('w', encoding='utf-8') as g:
    for line in f:
        if not line.strip():
            continue
        r = json.loads(line)
        code, feats = classify(r.get('response') or '')
        r['code_v3_1'] = code
        r['heur_feats_v3_1'] = feats
        g.write(json.dumps(r, ensure_ascii=False) + '\n')
        n += 1
print(f"Coded {n} rows -> {out}")
