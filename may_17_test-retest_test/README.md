# QQ-v1 Recode — Test-Retest Reliability Pass

A blinded second-pass hand-coding of the original 210-trial calibration sample, to compute intra-rater (test-retest) reliability.

The original calibration sample was hand-coded on **2026-05-03 / 2026-05-04**. This recode is being done **2026-05-17**, ~13 days later.

---

## What is blinded

The recoder (Bo) does not see, during this pass:

- the original `my_code` label
- the original `my_note`
- the heuristic `code_v3_1` label
- the model identity (`gpt-5.4-nano`, `claude-sonnet-4-6`, etc.)
- the model family (GPT / Claude)
- the model tier (small / mid / large)
- the frame ID (`F1` / `F4` / etc.) and frame name
- the speech act and person fields
- the original trial position or trial ID
- the word author and word meta

The recoder *does* see:

- the prompt (which by necessity contains the word and the surface form of the frame — there is no way to code a response without knowing what was asked)
- the response
- the codebook (visible on demand via the toggle)
- a blinded ID (`B001`–`B210`) that is sequential over a shuffled permutation, so it conveys no information about the original ordering

This is the strongest reasonable blinding for an intra-rater reliability test of a coding scheme. The variables that *could* prime the coder (prior label, heuristic label, model identity) are hidden; the variables that *must* be visible to do the task at all (prompt, response) are visible.

---

## Files

| File | Role |
|---|---|
| `blinded_trials.json` | the 210 trials, shuffled (seed 20260517), reduced to `{blind_id, prompt, response}` only |
| `blinded_trials.csv` | same content as CSV, for inspection |
| `recode_tool_blinded.html` | the coding UI. localStorage-backed; resumes between sessions |
| `recode_mapping_KEEP_SEALED.csv` | **sealed envelope** — `blind_id <-> trial_id`, original `my_code`, full metadata. NOT to be opened during coding |
| `recode_analysis.py` | post-hoc analysis. Reads the mapping + the exported recode CSV; produces test-retest κ, confusion matrix, cell breakdowns |
| `qq_recode_blinded_YYYY-MM-DD.csv` | exported from the tool after recoding (CSV button) |
| `recode_merged.csv` | produced by `recode_analysis.py` — original + recode side by side for inspection |
| `recode_summary.json` | machine-readable summary of test-retest stats |

---

## How to run

### 1. Start the tool

The tool is a single HTML page that fetches `blinded_trials.json`. Because of browser file:// CORS rules, serve the folder over HTTP:

```bash
cd recode_2026-05
python -m http.server 8000
```

Then open `http://localhost:8000/recode_tool_blinded.html`.

### 2. Code the 210 trials

- Codes are saved to localStorage continuously; close the tab and come back any time
- Keyboard: `1` DEFLECT, `2` DESCRIBE, `3` HYBRID, `4` SUBSTITUTE, `5` REFUSE, `6` OTHER, `←`/`→` navigate, `n` focus the note field
- Notes are optional but useful for borderline DESCRIBE/HYBRID or anything tagged OTHER
- The codebook is available via the "show codebook" toggle near the top; v3.1 definitions

### 3. Export

When all 210 are coded:

- Click **export CSV**, save to this folder as `qq_recode_blinded_2026-05-17.csv` (or whatever today's date is)

### 4. Analyze

```bash
python recode_analysis.py qq_recode_blinded_2026-05-17.csv
```

Outputs:
- overall agreement and Cohen's κ (with bootstrap 95% CI)
- confusion matrix (original × recode)
- per-class precision/recall/f1
- agreement breakdown by model family, model, frame, and model × frame
- cross-check vs the heuristic
- writes `recode_merged.csv` (both codings side by side) and `recode_summary.json`

---

## What good numbers look like

Calibration-time κ (the heuristic vs Bo, May 4):

- v3 heuristic vs original hand codes: agreement 0.900, κ = 0.648
- v3.1 heuristic vs original hand codes (reported in GPT paper): κ = 0.731

Intra-rater (test-retest) κ should generally be *higher* than inter-coder κ — coders are more consistent with themselves than with each other. If test-retest κ comes in below 0.70 the codebook has a real ambiguity problem at some boundary; the most likely culprit is DESCRIBE/HYBRID at F4. If it comes in at 0.85+ the codebook is in good shape.

Cells of particular interest for the disagreement breakdown:
- **GPT × F4** — where the loophole lives and where the heuristic was shakiest
- **GPT-nano × F1** — the calibration-time problem cell
- **claude-sonnet-4-6 × F4** — load-bearing for the "Sonnet zero" finding

---

## What to do if disagreements are found

A disagreement on recode is not a "mistake" by either pass. It is data about codebook ambiguity. The right response is:

1. Examine each disagreement
2. Decide which call is closer to the codebook intent (do not default to the original or the recode)
3. If a systematic pattern appears (e.g. F4 templated responses with bracketed-placeholder blockquote always coded HYBRID by one pass and DESCRIBE by the other), document the pattern as a codebook clarification
4. Adjudicate the disagreements with the clarification rule; report both the pre-adjudication and post-adjudication numbers

Do not silently overwrite the original codes with the recode codes, or vice versa. Both passes go into the public dataset alongside the adjudicated final code.

---

## Blinding integrity check

After analysis is complete, examine the per-cell agreement rates. If the recode systematically *agrees more* with the original on cells where the response is short and stylistically distinctive (e.g. Claude DEFLECTs) and *disagrees more* on cells where the response is long and templated (e.g. GPT F4 HYBRID), that pattern reflects genuine codebook difficulty rather than failed blinding. If the recode disagrees suspiciously little overall (κ > 0.95 say), consider whether some signal leaked.

The mapping file's hash should not be checked or examined during the coding pass:

```text
recode_mapping_KEEP_SEALED.csv — keep this file unopened until the export step
```
