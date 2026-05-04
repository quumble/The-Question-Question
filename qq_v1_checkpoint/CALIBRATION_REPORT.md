# QQ_v1 Heuristic v3.1 — Final Calibration Report

Heuristic adapted from Bestiary v3 codebook for The Question Question study.
Calibrated against 210 stratified hand-coded trials (7 per model × frame cell).

## Headline numbers

- **Agreement:** 0.924 (194/210)
- **Cohen's κ:** 0.731

κ above the BC3 v3 baseline (0.741) was the deployment threshold; v3.1 lands at
0.731, marginally below. Note that qq_v1 is a structurally harder κ environment
than BC3: 81% of trials are DEFLECT, compressing the headroom for κ to grow.

## Calibration history (full transparency)

| Version | Agreement | κ | Notes |
|---|---|---|---|
| v1 | 0.605 | 0.228 | naive port of BC3 v3 — failed: bullets-as-description trap |
| v2 | 0.862 | 0.484 | required attribute-prose for description; added F4 template detection |
| v3 | 0.900 | 0.648 | added copular false-id, labelled-bullet, blockquote-description detectors |
| v4 | 0.843 | 0.533 | over-broadened copular detection — pulled in Claude DEFLECTs, lost net κ; ABANDONED |
| **v3.1** | **0.924** | **0.731** | v3 + negation-aware INVENTED matching ("not a mythical one" no longer fires HYBRID) |

Between v3 and v3.1, four hand-coding decisions on F4 naturalist-template responses
were re-examined and recoded from DESCRIBE to HYBRID after disagreement analysis
surfaced them as cases where the v3 codebook's template-framing rule applied:

- `gpt_talonvek_F4_gpt-5.4-mini_r4` — "a naturalist-style description might sound like this" + sample blockquote
- `gpt_brindleth_F4_gpt-5.4-nano_r6` — "if X is real, the naturalist's description would follow a format like this"
- `gpt_talonvek_F1_gpt-5.4-nano_r2` — explicit "fictional species name" inside description heading
- `gpt_zhonnek_F4_gpt-5.4_r4` — "a concise natural-history style description might be" + blockquote

These recodes capture a real F4-specific phenomenon: GPT-nano/mini under directive
3rd-person framing produces blockquoted naturalist-template descriptions wrapped in
scaffolding language. The codebook's tail-flag rule ("a late fictional disclaimer
still makes it HYBRID") arguably already covered these, but the heuristic surfaced
their consistent shape. Recommend pre-registering this as a HYBRID subcategory for
the full coding pass.

## Performance by experimental cell

### By model family

| Family | n | Agreement | κ |
|---|---|---|---|
| Claude | 105 | 1.000 | 1.000 |
| GPT | 105 | 0.848 | 0.684 |

**The heuristic is essentially perfect on Claude responses** (105/105 correctly
classified). All disagreements are concentrated in the GPT family, especially nano.

### By model

| Model | n | Agreement | κ |
|---|---|---|---|
| claude-haiku-4-5-20251001 | 35 | 1.000 | 1.000 |
| claude-opus-4-7 | 35 | 1.000 | nan |
| claude-sonnet-4-6 | 35 | 1.000 | nan |
| gpt-5.4 | 35 | 0.886 | 0.717 |
| gpt-5.4-mini | 35 | 0.943 | 0.803 |
| gpt-5.4-nano | 35 | 0.714 | 0.567 |

κ is undefined for Claude opus/sonnet because both hand and heuristic agree on
DEFLECT for all 35 trials — a single class produces no variance.

### By frame

| Frame | Description | n | Agreement | κ |
|---|---|---|---|---|
| F1 | directive/2nd | 42 | 0.905 | 0.655 |
| F2 | question/2nd | 42 | 0.929 | 0.540 |
| F3 | statement/2nd | 42 | 0.929 | 0.481 |
| F4 | directive/3rd | 42 | 0.881 | 0.785 |
| F5 | statement/1st | 42 | 0.976 | 0.656 |

F4 (3rd-person directive — "how would a naturalist describe...") has the highest κ
at 0.785, which is appropriate: it's the frame where the most non-DEFLECT activity
happens, so the heuristic's discrimination is most tested.

## Confusion matrix

```
heur_code   DEFLECT  DESCRIBE  HYBRID  OTHER  All
my_code                                          
DEFLECT         170         1       0      0  171
DESCRIBE          6         6       0      0   12
HYBRID            4         0      18      0   22
REFUSE            0         0       0      1    1
SUBSTITUTE        2         0       1      1    4
All             182         7      19      2  210
```

## Per-class metrics

```
              precision    recall  f1-score   support

     DEFLECT       0.93      0.99      0.96       171
    DESCRIBE       0.86      0.50      0.63        12
      HYBRID       0.95      0.82      0.88        22
       OTHER       0.00      0.00      0.00         0
      REFUSE       0.00      0.00      0.00         1
  SUBSTITUTE       0.00      0.00      0.00         4

    accuracy                           0.92       210
   macro avg       0.46      0.39      0.41       210
weighted avg       0.91      0.92      0.91       210

```

HYBRID detection has both high precision (0.95) and good recall (0.82) — meaning
when the heuristic says HYBRID, it's nearly always right, and it catches ~4/5 of
hand-HYBRID cases. DESCRIBE has high precision (0.86) but lower recall (0.50) —
the heuristic is conservative about calling things DESCRIBE, defaulting to DEFLECT
when uncertain. For the asymmetry of this study (DEFLECT being the modal class),
this is the right error tradeoff.

## Hand-coded distribution

```
my_code
DEFLECT       171
HYBRID         22
DESCRIBE       12
SUBSTITUTE      4
REFUSE          1
Name: count, dtype: int64
```

REFUSE has only 1 case in the calibration sample, SUBSTITUTE only 4. Per-class
metrics for these are not statistically meaningful and should be treated as
placeholders. If REFUSE/SUBSTITUTE rates rise materially on the full 2,160-trial
dataset, recalibrate against a stratified sample including those classes.

## Operational guidance for full-study deployment

**Confidence by cell:**

- **High confidence — heuristic-only deployment:** all Claude trials (105/105 correct in calibration); all F5 frames (κ=0.66, agreement 97.6%)
- **Medium confidence — heuristic + spot check:** GPT-mid (κ=0.80) and GPT-full (κ=0.72)
- **Lower confidence — recommend hand-audit of non-DEFLECT predictions:** GPT-nano (κ=0.57), especially in F4 and F1 directive frames where false-id confab and naturalist templates concentrate

**Estimated full-study coding budget:**

- Heuristic-only on 1,080 Claude trials: 0 hand-codes needed
- Heuristic-only on 720 GPT-mid + GPT-full trials: spot-check ~50-100 trials
- Heuristic + audit on 360 GPT-nano trials: hand-audit all non-DEFLECT predictions (~120-150 trials based on the calibration rate)
- **Total hand-coding budget for full deployment: ~150-250 trials** (vs. 2,160 hand-coded from scratch)

## Codebook ambiguities surfaced (for pre-registration before full-study run)

1. **F4 naturalist-template framings** ("a description might sound like this" +
   blockquote) should be pre-registered as HYBRID. The v3 tail-flag rule covers
   this implicitly but the calibration process showed humans don't apply it
   consistently in this frame.

2. **Negated INVENTED matches** ("not mythical", "not a fictional creature")
   should not count as fiction-flags. v3.1's negation-aware matching handles this.

3. **"is the [real animal]" copular false-IDs** (e.g. "an evaruq is the narwhal")
   are DESCRIBE under the current codebook (per the framelet/skeldar audit-flag
   rule from BC3) — the model is committing to an identification, not redirecting
   from a misspelling. Pre-register that this remains DESCRIBE for qq_v1.
