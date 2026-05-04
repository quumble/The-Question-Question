# QQ_v1 Heuristic v3 — Calibration Report

Heuristic adapted from Bestiary v3 codebook for The Question Question study.
Calibrated against 210 stratified hand-coded trials (7 per model × frame cell).

## Headline numbers

- **Agreement:** 0.900 (189/210)
- **Cohen's κ:** 0.648

BC3 baseline was κ=0.741 on a different study (5 conditions × multiple word
sets). qq_v1 is harder for κ because DEFLECT is 81% of the class — the heuristic
has to discriminate within a narrow non-DEFLECT minority of ~40 trials.

## Performance by experimental cell

### By model family

| Family | n | Agreement | κ |
|---|---|---|---|
| Claude | 105 | 1.000 | 1.000 |
| GPT | 105 | 0.800 | 0.589 |

**Critical finding**: the heuristic is essentially perfect (κ=1.0) on Claude responses
and shaky on GPT (κ=0.59). All disagreements come from the GPT family, with
nano contributing the most.

### By model

| Model | n | Agreement | κ |
|---|---|---|---|
| claude-haiku-4-5-20251001 | 35 | 1.000 | 1.000 |
| claude-opus-4-7 | 35 | 1.000 | n/a |
| claude-sonnet-4-6 | 35 | 1.000 | n/a |
| gpt-5.4 | 35 | 0.829 | 0.577 |
| gpt-5.4-mini | 35 | 0.914 | 0.708 |
| gpt-5.4-nano | 35 | 0.657 | 0.492 |

κ is undefined for Claude opus/sonnet because both hand and heuristic agree on
DEFLECT for all 35 trials — a single class produces no variance.

### By frame

| Frame | Description | n | Agreement | κ |
|---|---|---|---|---|
| F1 | directive/2nd | 42 | 0.881 | 0.568 |
| F2 | question/2nd | 42 | 0.905 | 0.398 |
| F3 | statement/2nd | 42 | 0.929 | 0.481 |
| F4 | directive/3rd | 42 | 0.810 | 0.669 |
| F5 | statement/1st | 42 | 0.976 | 0.656 |

F4 (3rd-person directive, "how would a naturalist describe...") has both the most
non-DEFLECT activity and the highest κ — that's where the heuristic earns its keep.

## Confusion matrix

```
heur_code   DEFLECT  DESCRIBE  HYBRID  OTHER  All
my_code                                          
DEFLECT         170         1       0      0  171
DESCRIBE          6         5       5      0   16
HYBRID            4         0      14      0   18
REFUSE            0         0       0      1    1
SUBSTITUTE        2         0       1      1    4
All             182         6      20      2  210
```

## Per-class metrics

```
              precision    recall  f1-score   support

     DEFLECT       0.93      0.99      0.96       171
    DESCRIBE       0.83      0.31      0.45        16
      HYBRID       0.70      0.78      0.74        18
       OTHER       0.00      0.00      0.00         0
      REFUSE       0.00      0.00      0.00         1
  SUBSTITUTE       0.00      0.00      0.00         4

    accuracy                           0.90       210
   macro avg       0.41      0.35      0.36       210
weighted avg       0.88      0.90      0.88       210

```

## Disagreement breakdown

21 disagreements total. By type:

```
my_code     heur_code
DESCRIBE    DEFLECT      6
            HYBRID       5
HYBRID      DEFLECT      4
SUBSTITUTE  DEFLECT      2
DEFLECT     DESCRIBE     1
REFUSE      OTHER        1
SUBSTITUTE  HYBRID       1
            OTHER        1
dtype: int64
```

## Hand-coded distribution (for reference)

```
my_code
DEFLECT       171
HYBRID         18
DESCRIBE       16
SUBSTITUTE      4
REFUSE          1
Name: count, dtype: int64
```

Notable: REFUSE only has 1 case in the calibration sample, SUBSTITUTE only 4.
The heuristic's per-class metrics for these classes aren't meaningful at this n.
If REFUSE/SUBSTITUTE rates rise on the full dataset, recalibrate.

## Iteration history

| Version | Agreement | κ | Notes |
|---|---|---|---|
| v1 | 0.605 | 0.228 | naive port of BC3 v3 — failed: bullets-as-description trap (DEFLECT→HYBRID/DESCRIBE leakage) |
| v2 | 0.862 | 0.484 | required attribute-prose for description; added template-detection for F4 confab |
| v3 | **0.900** | **0.648** | added copular false-id ("X is the narwhal"), labelled-bullet, blockquote-description |
| v4 | 0.843 | 0.533 | over-broadened copular detection — pulled in Claude DEFLECTs, lost net κ |

v3 is the deployment version.

## Operational guidance

**Confidence by cell:**

- **High confidence — deploy heuristic-only:** all Claude trials (105/105 in calibration), all F5, F2, F3 trials with DEFLECT-favoring frames
- **Medium confidence — heuristic + spot check:** GPT-mid and GPT-full
- **Low confidence — hand audit non-DEFLECT predictions:** GPT-nano, especially in F4 and F1 directive frames where the false-id confab is concentrated

**For full-study deployment on the 2,160-trial dataset:**

1. Run heuristic on all 2,160 trials
2. Hand-audit a stratified random sample of GPT-nano non-DEFLECT predictions
3. Flag any DESCRIBE→HYBRID borderline cases for codebook clarification

## Known limitations / codebook ambiguities surfaced

Five DESCRIBE→HYBRID disagreements on F4 nano/mini show the heuristic
aggressively detecting template scaffolding ("a naturalist might write something
like...") that hand-coding treated as DESCRIBE because the embedded blockquote was
substantively committal. This is a genuine codebook-edge phenomenon — F4
"naturalist-template" responses sit on the DESCRIBE/HYBRID boundary in a way that
v3's tail-flag rule ("a late fictional disclaimer still makes it HYBRID") doesn't
clearly resolve. Worth pre-registering a tighter rule before the full coding pass.
