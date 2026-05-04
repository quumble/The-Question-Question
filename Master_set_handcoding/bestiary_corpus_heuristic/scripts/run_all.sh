#!/usr/bin/env bash
set -euo pipefail
python src/evaluate_heuristic.py
python src/apply_heuristic.py
python src/export_machine_review_batch.py
