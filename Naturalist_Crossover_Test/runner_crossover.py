#!/usr/bin/env python3
"""
The Question Question — v1 runner.

Adapted from gpt54_on_gpt_words.py (BC3). Iterates frames.csv, calls each model
N replicates per row, writes JSONL results.

Architectural support:
- GPT-5.4 family (nano, mini, full) via openai SDK
- Claude family (Haiku 4.5, Sonnet 4.6, Opus 4.7) via anthropic SDK

Both keys must be set as environment variables for a full run:
    export OPENAI_API_KEY=sk-...
    export ANTHROPIC_API_KEY=sk-ant-...

Or restrict to one architecture with --arch gpt or --arch claude.

Usage:
    python runner.py --dry-run                                 # smoke test
    python runner.py --limit 10 --out results/smoke.jsonl      # 10 trials, real API
    python runner.py --reps 6 --out results/full.jsonl         # full run
    python runner.py --reps 6 --arch claude --out results/claude_only.jsonl
    python runner.py --reps 6 --out results/full.jsonl --resume

Resume reads existing JSONL and skips trials by trial_id.

Frame design and word selection rationale: see README.md.
"""

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

# ----- Configuration -----

DEFAULT_FRAMES_CSV = "frames.csv"
DEFAULT_REPS = 6
DEFAULT_OUT = "results/qq_v1_results.jsonl"

MAX_TOKENS = 500          # response cap; BC3 max was ~400
TEMPERATURE = 1.0         # match BC3
RETRY_LIMIT = 3
RETRY_BACKOFF_SEC = 4

# ----- Pricing (per million tokens, standard non-batch) -----
# Used only for cost estimation in summary, not billing.
PRICING = {
    "gpt-5.4-nano":               (0.20, 1.25),
    "gpt-5.4-mini":               (0.75, 4.50),
    "gpt-5.4":                    (2.50, 15.00),
    "claude-haiku-4-5-20251001":  (1.00, 5.00),
    "claude-sonnet-4-6":          (3.00, 15.00),
    "claude-opus-4-7":            (5.00, 25.00),
}


# ----- API call dispatchers -----

def call_gpt(prompt, model, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    """Call OpenAI's API. Returns (response_text, input_tokens, output_tokens, latency_sec).

    Note: GPT-5.4 family uses `max_completion_tokens` (the rebrand from
    `max_tokens`). Temperature is passed strictly at TEMPERATURE — if any
    model in the family rejects it, we want to fail loudly rather than
    silently introduce a cross-tier sampling confound.
    """
    from openai import OpenAI
    client = OpenAI()
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=max_tokens,
        temperature=temperature,
    )
    latency = time.time() - t0
    text = resp.choices[0].message.content
    in_toks = resp.usage.prompt_tokens
    out_toks = resp.usage.completion_tokens
    return text, in_toks, out_toks, latency


def call_claude(prompt, model, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    """Call Anthropic's API. Returns (response_text, input_tokens, output_tokens, latency_sec)."""
    import anthropic
    client = anthropic.Anthropic()
    t0 = time.time()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - t0
    text = resp.content[0].text if resp.content else ""
    in_toks = resp.usage.input_tokens
    out_toks = resp.usage.output_tokens
    return text, in_toks, out_toks, latency


def dispatch(prompt, model):
    """Route to the right SDK based on model name prefix."""
    if model.startswith("gpt"):
        return call_gpt(prompt, model)
    elif model.startswith("claude"):
        return call_claude(prompt, model)
    else:
        raise ValueError(f"Unknown model: {model}")


def call_with_retry(prompt, model):
    """Wrap dispatch with retries + exponential-ish backoff."""
    last_err = None
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            return dispatch(prompt, model), attempt, None
        except Exception as e:
            last_err = e
            if attempt < RETRY_LIMIT:
                time.sleep(RETRY_BACKOFF_SEC * attempt)
    return (None, 0, 0, 0.0), RETRY_LIMIT, str(last_err)


# ----- Trial ID + estimated cost -----

def trial_id(row, rep_n):
    """Stable per-trial identifier so --resume works."""
    return f"{row['word_author']}_{row['word']}_{row['frame_id']}_{row['model']}_r{rep_n}"


def estimate_cost(in_toks, out_toks, model):
    if model not in PRICING:
        return 0.0
    p_in, p_out = PRICING[model]
    return (in_toks * p_in + out_toks * p_out) / 1_000_000


# ----- Progress tracker -----

class Progress:
    """Live progress, tally, ETA, and sidecar progress.json.

    Uses tqdm if available; otherwise emits a carriage-return single-line
    bar to stderr. Writes a small JSON snapshot next to the output file so
    you can poll status from another shell without parsing the JSONL.
    """

    def __init__(self, total, out_path, snapshot_every=5):
        self.total = total
        self.snapshot_path = Path(out_path).with_suffix(".progress.json")
        self.snapshot_every = snapshot_every
        self.t_start = time.time()
        self.done = 0
        self.ok = 0
        self.errors = 0
        self.cost = 0.0
        self.in_toks = 0
        self.out_toks = 0
        self.per_model = {}  # model -> {"ok": int, "err": int}
        self._last_snapshot = 0
        self._tqdm = None
        try:
            from tqdm import tqdm
            self._tqdm = tqdm(total=total, unit="trial", file=sys.stderr,
                              dynamic_ncols=True, smoothing=0.05)
        except ImportError:
            print(f"[progress] tqdm not installed; using plain progress lines",
                  file=sys.stderr)

    def update(self, model, ok, in_toks=0, out_toks=0, cost=0.0):
        self.done += 1
        self.in_toks += in_toks
        self.out_toks += out_toks
        self.cost += cost
        bucket = self.per_model.setdefault(model, {"ok": 0, "err": 0})
        if ok:
            self.ok += 1
            bucket["ok"] += 1
        else:
            self.errors += 1
            bucket["err"] += 1

        elapsed = time.time() - self.t_start
        rate = self.done / elapsed if elapsed > 0 else 0
        remaining = self.total - self.done
        eta_sec = remaining / rate if rate > 0 else 0

        if self._tqdm is not None:
            self._tqdm.set_postfix({
                "ok": self.ok,
                "err": self.errors,
                "cost": f"${self.cost:.3f}",
            }, refresh=False)
            self._tqdm.update(1)
        else:
            mins, secs = divmod(int(eta_sec), 60)
            hrs, mins = divmod(mins, 60)
            print(
                f"\r[progress] {self.done}/{self.total} "
                f"ok={self.ok} err={self.errors} "
                f"rate={rate:.2f}/s ETA={hrs:02d}:{mins:02d}:{secs:02d} "
                f"cost~${self.cost:.4f}",
                end="", file=sys.stderr, flush=True,
            )

        if self.done - self._last_snapshot >= self.snapshot_every or self.done == self.total:
            self._write_snapshot(eta_sec, rate)
            self._last_snapshot = self.done

    def _write_snapshot(self, eta_sec, rate):
        snap = {
            "done": self.done,
            "total": self.total,
            "ok": self.ok,
            "errors": self.errors,
            "rate_per_sec": round(rate, 3),
            "eta_sec": round(eta_sec, 1),
            "elapsed_sec": round(time.time() - self.t_start, 1),
            "cost_estimate_usd": round(self.cost, 6),
            "input_tokens_total": self.in_toks,
            "output_tokens_total": self.out_toks,
            "per_model": self.per_model,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        try:
            tmp = self.snapshot_path.with_suffix(".progress.json.tmp")
            tmp.write_text(json.dumps(snap, indent=2))
            tmp.replace(self.snapshot_path)
        except Exception as e:
            print(f"\n[progress] snapshot write failed: {e}", file=sys.stderr)

    def close(self):
        if self._tqdm is not None:
            self._tqdm.close()
        else:
            print("", file=sys.stderr)  # newline after the in-place bar
        elapsed = time.time() - self.t_start
        print(
            f"[done] {self.done}/{self.total} trials | "
            f"ok={self.ok} err={self.errors} | "
            f"elapsed={elapsed:.1f}s | "
            f"cost~${self.cost:.4f}",
            file=sys.stderr,
        )
        if self.per_model:
            print("[done] per-model breakdown:", file=sys.stderr)
            for model, counts in sorted(self.per_model.items()):
                print(f"  {model:32s}  ok={counts['ok']:4d}  err={counts['err']:4d}",
                      file=sys.stderr)


# ----- Main run loop -----

def run(args):
    frames_path = Path(args.frames)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing trial_ids if resuming
    seen = set()
    if args.resume and out_path.exists():
        with open(out_path) as f:
            for line in f:
                try:
                    seen.add(json.loads(line)["trial_id"])
                except (json.JSONDecodeError, KeyError):
                    pass
        print(f"[resume] Found {len(seen)} existing trials in {out_path}", file=sys.stderr)

    # Load frame templates
    with open(frames_path) as f:
        all_rows = list(csv.DictReader(f))

    # Filter by architecture if requested.
    # Note: the original QQ-v1 runner filtered by word_author because the
    # first run intentionally paired GPT models with GPT-authored words and
    # Claude models with Claude-authored words. The crossover run decouples
    # word_author from model_family, so filtering must use model_family.
    if args.arch == "gpt":
        all_rows = [r for r in all_rows if r["model_family"].lower() == "gpt"]
    elif args.arch == "claude":
        all_rows = [r for r in all_rows if r["model_family"].lower() == "claude"]

    # Build the trial plan: each frames.csv row × N reps
    plan = []
    for row in all_rows:
        for rep_n in range(1, args.reps + 1):
            tid = trial_id(row, rep_n)
            if tid in seen:
                continue
            plan.append((row, rep_n, tid))

    if args.limit:
        plan = plan[: args.limit]

    print(f"[plan] {len(plan)} trials to run "
          f"({len(all_rows)} frame-rows × {args.reps} reps, "
          f"minus {len(seen)} resumed)", file=sys.stderr)

    if args.dry_run:
        print("[dry-run] First 3 trials would be:", file=sys.stderr)
        for row, rep_n, tid in plan[:3]:
            print(f"  {tid}", file=sys.stderr)
            print(f"    prompt: {row['prompt']}", file=sys.stderr)
        return

    # Run
    progress = Progress(total=len(plan), out_path=out_path)
    try:
        with open(out_path, "a") as out_f:
            for row, rep_n, tid in plan:
                (response_text, in_toks, out_toks, latency), attempts, err = \
                    call_with_retry(row["prompt"], row["model"])

                cost = estimate_cost(in_toks, out_toks, row["model"]) if not err else 0.0

                record = {
                    "trial_id": tid,
                    "word": row["word"],
                    "word_author": row["word_author"],
                    "word_meta": row["word_meta"],
                    "model_family": row["model_family"],
                    "model": row["model"],
                    "model_tier": row["model_tier"],
                    "status": row["status"],
                    "category": row["category"],
                    "condition": row["condition"],
                    "frame_id": row["frame_id"],
                    "frame_name": row["frame_name"],
                    "speech_act": row["speech_act"],
                    "person": row["person"],
                    "rep_n": rep_n,
                    "prompt": row["prompt"],
                    "response": response_text,
                    "response_status": "ok" if not err else "error",
                    "input_tokens": in_toks,
                    "output_tokens": out_toks,
                    "latency_sec": round(latency, 3),
                    "attempts": attempts,
                    "error": err,
                    "estimated_cost_usd": round(cost, 6),
                }
                out_f.write(json.dumps(record) + "\n")
                out_f.flush()
                progress.update(
                    model=row["model"],
                    ok=(err is None),
                    in_toks=in_toks,
                    out_toks=out_toks,
                    cost=cost,
                )
    finally:
        progress.close()


def main():
    p = argparse.ArgumentParser(description="QQ-v1 crossover-capable runner")
    p.add_argument("--frames", default=DEFAULT_FRAMES_CSV,
                   help="path to frames.csv")
    p.add_argument("--out", default=DEFAULT_OUT,
                   help="output JSONL path")
    p.add_argument("--reps", type=int, default=DEFAULT_REPS,
                   help="replicates per (word × frame × model) cell")
    p.add_argument("--arch", choices=["both", "gpt", "claude"], default="both",
                   help="restrict to one architecture")
    p.add_argument("--limit", type=int, default=None,
                   help="cap total trials (for smoke testing)")
    p.add_argument("--dry-run", action="store_true",
                   help="print plan but don't call APIs")
    p.add_argument("--resume", action="store_true",
                   help="skip trials already present in output JSONL")
    args = p.parse_args()
    run(args)


if __name__ == "__main__":
    main()
