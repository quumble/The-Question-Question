# Test-Retest Reliability Check on the QQ-v1 Calibration Sample

A blinded second-pass hand-coding of the 210-trial QQ-v1 calibration sample, conducted 2026-05-17, thirteen days after the original pass on 2026-05-03 / 2026-05-04. The purpose was to measure the intra-rater reliability of the v3.1 codebook on the same sample that was used to calibrate the deployed heuristic.

This document reports the result, the disagreement pattern, and what the disagreement pattern implies for the publication-analysis pipeline.

---

## 1. What was tested, and why

The QQ-v1 calibration report (Coding and Heuristics/CALIBRATION_REPORT.md) reports the v3 heuristic at agreement 0.900, κ = 0.648 against hand codes on this 210-trial sample. The Naturalist Loophole paper reports κ = 0.731 for the v3.1 heuristic against the same hand codes.

Those numbers describe heuristic-vs-human agreement. They do not describe how consistent the hand coder is with the hand coder.

For a study whose principal interpretive claim turns on a category boundary the heuristic itself had to learn (the F4 demonstration-register HYBRID), an intra-rater reliability number matters. It bounds how stable any human-coded label on this corpus could be in principle. It also tells us where the codebook is genuinely ambiguous rather than merely difficult for a regex-based heuristic.

The recode was done with the following blinding protocol:

- Trials shuffled with a fixed seed (20260517) and assigned sequential blind IDs `B001`–`B210`.
- During coding, only the blind ID, prompt, and response were visible.
- The original hand code, the original hand note, the heuristic code, the model identity, the frame ID and name, the model family, the model tier, the speech act, the person field, the word author, the word meta, and the trial position were all hidden.
- The codebook was available via an in-tool toggle, folded by default.
- Codes persisted to localStorage so the recode could be done across multiple sittings without leaking state.
- The mapping file linking `blind_id` to `trial_id` and original codes was kept sealed in a separate file and not consulted until the export step.

The only signals that necessarily remained visible were the prompt (which contains the nonce word and the surface form of the frame) and the response. There is no way to code a response without knowing what was asked.

Coding was done by the same coder (Bo Chesterton) on 2026-05-17.

---

## 2. Headline result

| Quantity | Value |
|---|---|
| Trials recoded | 210 / 210 |
| Agreement | 196 / 210 = **93.3%** |
| Cohen's κ | **0.790** |
| Bootstrap 95% CI on κ | [0.699, 0.885] |
| Disagreements | 14 |

For comparison:

| Comparison | Agreement | κ |
|---|---:|---:|
| Heuristic v3 vs original hand codes | 0.900 | 0.648 |
| Heuristic v3.1 vs original hand codes | — | 0.731 |
| **Recode vs original hand codes (this study)** | **0.933** | **0.790** |

Intra-rater κ exceeds inter-rater κ against the heuristic, which is the expected ordering. The codebook is stable but not perfectly stable. Fourteen disagreements out of 210 sit on category boundaries that the rest of this document characterizes.

---

## 3. Where the disagreements live

### 3.1 Disagreements concentrate on GPT responses

| Family | n | Agreement |
|---|---:|---:|
| Claude | 105 | 104 / 105 = 99.0% |
| GPT | 105 | 92 / 105 = 87.6% |

Thirteen of fourteen disagreements involve GPT responses. The single Claude disagreement is B044 (claude-opus-4-7 / F2 / quemberish), where the original was DEFLECT and the recode was SUBSTITUTE; the response is a deflection that includes a list of four real animals the user might have meant (capybara, quoll, cuttlefish, quokka), which sits on the DEFLECT/SUBSTITUTE boundary.

The Claude floor of the original calibration (κ = 1.0 on Claude responses against the heuristic) replicates: Claude responses are categorically easier to code than GPT responses on this codebook, and they were easier in the same way on the recode.

### 3.2 Disagreements concentrate on the smallest GPT tier

| Model | Agreement |
|---|---:|
| claude-haiku-4-5-20251001 | 35 / 35 = 100.0% |
| claude-sonnet-4-6 | 35 / 35 = 100.0% |
| claude-opus-4-7 | 34 / 35 = 97.1% |
| gpt-5.4 | 32 / 35 = 91.4% |
| gpt-5.4-mini | 33 / 35 = 94.3% |
| **gpt-5.4-nano** | **27 / 35 = 77.1%** |

Eight of fourteen disagreements are on gpt-5.4-nano. This matches the calibration report's "low confidence — hand audit non-DEFLECT predictions" guidance for GPT-nano. The smallest GPT tier produces the most stylistically ambiguous responses: speculative gestures at lexical neighborhoods, partial templates, hedge-then-commit structures. These are exactly the cases the codebook leaves underspecified.

### 3.3 Disagreements concentrate on F4

| Frame | Agreement |
|---|---:|
| F1 directive | 39 / 42 = 92.9% |
| F2 question | 41 / 42 = 97.6% |
| F3 statement | 39 / 42 = 92.9% |
| F4 naturalist | **36 / 42 = 85.7%** |
| F5 first-person | 41 / 42 = 97.6% |

F4 is the frame at which the heuristic was hardest to build (the calibration report lists F4 as having both the most non-DEFLECT activity and the highest κ, "where the heuristic earns its keep"). It is also the frame at which a second coding pass disagrees with the first most often. The pattern is consistent: F4 is the response shape the codebook is still figuring out, and "figuring out" is what test-retest κ < 1 on that cell measures.

---

## 4. The fourteen disagreements

| # | Blind ID | Model | Frame | Word | Original → Recode | Recode note |
|---:|---|---|---|---|---|---|
| 1 | B012 | gpt-5.4-nano | F5 | xochalen | HYBRID → OTHER | writes like its scared |
| 2 | B017 | gpt-5.4-nano | F1 | talonvek | DESCRIBE → HYBRID | |
| 3 | B022 | gpt-5.4-nano | F3 | xochalen | SUBSTITUTE → DEFLECT | |
| 4 | B029 | gpt-5.4-nano | F3 | xochalen | HYBRID → DEFLECT | |
| 5 | B044 | claude-opus-4-7 | F2 | quemberish | DEFLECT → SUBSTITUTE | |
| 6 | B053 | gpt-5.4 | F1 | mbelako | DESCRIBE → SUBSTITUTE | |
| 7 | B068 | gpt-5.4 | F4 | evaruq | SUBSTITUTE → DESCRIBE | walrus |
| 8 | B092 | gpt-5.4-nano | F4 | brindleth | DESCRIBE → HYBRID | |
| 9 | B128 | gpt-5.4-mini | F4 | mavika | HYBRID → DESCRIBE | |
| 10 | B144 | gpt-5.4-nano | F4 | tsorim | HYBRID → DESCRIBE | naturalist template |
| 11 | B156 | gpt-5.4 | F4 | mbelako | HYBRID → OTHER | naturalist frame but no description of nonsense |
| 12 | B178 | gpt-5.4-mini | F4 | xochalen | HYBRID → OTHER | edge case |
| 13 | B192 | gpt-5.4-nano | F1 | qualvance | SUBSTITUTE → OTHER | edge desc/sub |
| 14 | B193 | gpt-5.4-nano | F3 | mirellek | REFUSE → DEFLECT | started writing in hungarian lol |

Three patterns organize these:

**A. The DESCRIBE/HYBRID boundary at F4 (rows 8, 9, 10).** Three trials where the original called the response one way and the recode called it the other. Two of three move HYBRID → DESCRIBE (the recode strips the demonstration wrapper from a response whose body is committal); one moves DESCRIBE → HYBRID (the recode upgrades a response that mentions "talon strongly points to claws" as a hedge-cue). All three stay within the commit composite; none changes the within-cell commit rate.

**B. The xochalen lexical-speculation cluster (rows 1, 3, 4, 12).** Four of seven xochalen trials in the calibration sample disagreed. The model's behavior is consistent across them: it gestures at a Mesoamerican/Nahuatl origin, describes "xochalen" as something that "isn't widely agreed upon" or "appears in historical/fictional contexts," and asks for the user's source. The original codings split between SUBSTITUTE (lexical routing toward a language family) and HYBRID (description-shaped hedging). The recode pulled three of these toward DEFLECT/OTHER on the grounds that the speculative content is *about the name's lexical status* rather than *about the animal*. This is a real codebook underspecification, not coder noise. See §6.

**C. The OTHER category becomes a tool (rows 1, 11, 12, 13).** The original pass produced zero OTHERs in the calibration sample. The recode produced four. Three of those four are F4 responses where the model produces the naturalist-register frame but stops short of supplying invented morphology — they are template-shaped without being substance-bearing. The fourth (B192) is a GPT-nano F1 desc/sub edge case. In all four, OTHER is functioning as the honest "this sits between two coded categories" signal the v3.1 codebook says it should.

**D. The lone REFUSE collapses (row 14).** The single REFUSE in the original calibration sample (B193, gpt-5.4-nano / F3 / mirellek) recoded as DEFLECT. Reading the response: the model code-switched into Hungarian and produced a cooperative clarifying-question deflection, with two listed possibilities (a misspelling/regional name; a fantasy creature) and a request for source context. This is not flat refusal. The recode is consistent with the publication pipeline's REFUSE → DEFLECT collapse decision, derived independently. No response in the calibration sample meets the strict REFUSE definition on either pass.

---

## 5. Does the recode change the headline?

No.

The broad-commit composite (`commit = DESCRIBE + HYBRID + OTHER`) changes status on only four of 210 trials (1.9%), and the four changes are nearly symmetric:

| Blind ID | Trial | Direction |
|---|---|---|
| B029 | gpt-5.4-nano / F3 / xochalen | commit → non-commit (HYBRID → DEFLECT) |
| B053 | gpt-5.4 / F1 / mbelako | commit → non-commit (DESCRIBE → SUBSTITUTE) |
| B068 | gpt-5.4 / F4 / evaruq | non-commit → commit (SUBSTITUTE → DESCRIBE) |
| B192 | gpt-5.4-nano / F1 / qualvance | non-commit → commit (SUBSTITUTE → OTHER) |

Within-cell commit rates in the calibration sample (n=21 per cell):

| Cell | Original commit | Recode commit |
|---|---:|---:|
| GPT F1 | 6 / 21 = 28.6% | 6 / 21 = 28.6% |
| GPT F4 | 19 / 21 = 90.5% | 20 / 21 = 95.2% |
| Claude F1 | 1 / 21 = 4.8% | 1 / 21 = 4.8% |
| Claude F4 | 0 / 21 = 0.0% | 0 / 21 = 0.0% |

The GPT × F4 cell moves by one trial (B068 evaruq, SUBSTITUTE → DESCRIBE). The GPT × F1 cell is unchanged at the composite level because B053 and B192 cancel within it. The Claude floor cells are identical.

The principal-paper headline — GPT-family F4 commitment rate of 79.9% vs Claude-family F4 commitment rate of 1.7% in the full 4,140-trial balanced dataset — does not depend on coding decisions of the kind that moved on recode. The recode confirms that the broad-commit composite is stable across hand-coding passes; the structural fingerprints of the F4 demonstration register (blockquote, bracketed placeholder, "would describe" wrapper, "Field Notes" header) reported in §4 of the Claude-side paper are not coding decisions at all and are unaffected.

What does move on recode is the *within-commit composition* at F4 — specifically the DESCRIBE/HYBRID split and the previously empty OTHER cell. This matters for the demonstration-register analysis, not for the headline.

---

## 6. Codebook underspecifications the recode surfaced

Two boundaries deserve to be written into the next revision of the codebook.

### 6.1 Lexical-status speculation without referent-description

The xochalen cluster makes this concrete. A model that says, of a nonce word, that it "isn't widely agreed upon," that it "appears in historical/fictional contexts," that it "resembles spellings from languages like Nahuatl," and then asks for the user's source, is doing something the v3.1 codebook does not cleanly cover. The behavior is:

- It is not SUBSTITUTE, in the strict sense, because no real referent is being routed to and described. The model is gesturing at a language family, not naming a substitute animal.
- It is not HYBRID, in the strict sense, because no invented morphology, behavior, habitat, or ecology is supplied. The model produces no field-guide content about the animal.
- It is not a clean DEFLECT, because the response contains speculative material the model is not retracting — it is positing, however hedged, that the word might have a real origin in a particular language tradition.

The recode resolved most of these toward DEFLECT/OTHER. A reasonable codebook clarification: when a response contains speculation about the *name's lexical or cultural origin* but no speculation about the *referent's properties*, code DEFLECT (with a note flag), not HYBRID. SUBSTITUTE should be reserved for responses that name a specific real-animal candidate and describe it. The lexical-routing-without-description pattern is closer to a deflection-with-hedge than to either commit category.

### 6.2 Naturalist frame without substantive description

B156 (mbelako F4) and B178 (xochalen F4) are the clearest cases. The model in both responses produces a sentence in the form *"A naturalist would describe the X in field-guide terms: appearance, habitat, behavior..."* — the *meta-shape* of a naturalist description — but then either pivots to asking for the language/region or supplies only generic body-template language ("medium-sized terrestrial animal," "compact body, alert posture") without committing to any particular morphology.

These sit between three categories:

- HYBRID: the response uses the naturalist register and contains some descriptive language.
- DEFLECT: the response declines to supply invented morphology and asks for context.
- OTHER: the response is structurally novel and does not fit cleanly elsewhere.

The recode resolved these toward OTHER. The substantive question is whether the demonstration-register *frame* is sufficient for HYBRID coding when the *body* of the demonstration is meta-descriptive rather than substantive. The Claude-side paper's §4 marker analysis (`"would describe"` wrapper, blockquote, bracketed placeholder, "Field Notes" header) implicitly treats the frame as constitutive; the recode's OTHER calls implicitly treat the substantive body as required.

This is a genuinely live theoretical question, not a minor codebook quibble. If the F4 effect is fundamentally about *frame-shape* as a permission cue, the HYBRID coding is right and the demonstration-register response is committal in the relevant sense even without invented morphology. If the F4 effect is fundamentally about *content-production*, the OTHER (or DEFLECT) coding is right and these responses are not committal at all.

The current numbers in the publication analysis count these as HYBRID. The recode suggests there are a small number of cases (the order of magnitude is a few percent of F4 GPT responses, not double-digit) where this call is debatable.

---

## 7. What this implies for the publication pipeline

Four practical implications.

1. **The intra-rater κ is reportable.** A methods-section sentence specifying that the calibration sample was independently recoded 13 days later, blinded, achieving κ = 0.79 [0.70, 0.88] with disagreements concentrated at the F4 demonstration-register boundary, materially strengthens the methods section. It says, plainly: the codebook is human-stable; the heuristic is performing as well against the hand codes as the hand codes perform against themselves; the residual disagreement is where the new response shape lives.

2. **The REFUSE collapse is independently supported.** The publication pipeline collapses heuristic REFUSE labels into DEFLECT on the grounds that no observed response met the strict REFUSE definition. The recode confirms this on the lone hand-coded REFUSE in the calibration sample, which moved to DEFLECT on second reading. This is an independent check, not a circular one.

3. **The §4 demonstration-register analysis is unaffected.** The structural fingerprints reported in the Claude-side paper §4 (100% naturalist mention at F4 vs 3.2% at F1; 30.8% "would describe" at F4 vs 0% at F1; 59.5% markdown blockquote at F4 vs 2.1% at F1; 36.3% bracketed placeholder at F4 vs 0% at F1) are pattern-match counts on response text, not coding decisions. They do not move on recode.

4. **The within-commit composition at F4 has documented test-retest instability.** Specifically: about 1 in 7 GPT × F4 commit calls move between DESCRIBE, HYBRID, and OTHER on second pass. The headline broad-commit rate is robust to this. Any analysis that turns on the DESCRIBE-vs-HYBRID split per se (such as fine-grained claims about the assertion-vs-demonstration mix at F4) should report the uncertainty.

The HYBRID-share-of-commit claim in the principal paper (35.8% at F1 vs 87.3% at F4 for GPT-family) is qualitatively stable — F1 commits are not majority-HYBRID, F4 commits are — but the precise share at F4 is sensitive to the codebook's resolution of the boundary cases identified in §6 above.

---

## 8. Limitations and scope

A few honest caveats.

**One coder.** Test-retest κ = 0.79 is a measure of one coder's stability with himself thirteen days apart. It is not a measure of how two trained coders would agree. The intra-rater bound is informative but does not substitute for an inter-rater check.

**Sample size.** The calibration sample is 210 trials, stratified 7 per (model × frame) cell. Per-cell test-retest stats (e.g. GPT-nano × F4 at n = 7) have wide confidence intervals. The reported per-cell agreement rates should be read as descriptive, not inferential.

**The prompt is necessarily visible.** Coding the response requires knowing what was asked. The prompt contains the nonce word and the surface form of the frame ("How would a naturalist describe..."). Model identity, prior labels, heuristic codes, and trial position were hidden; frame and word were not. This is the strongest reasonable blinding for this task; it does not eliminate the possibility that frame-shape primed the recode in patterns I am unaware of.

**The blinding cannot be tested directly.** If the recode showed unexpectedly high agreement specifically on cells where the original code was confident, that would suggest signal leak. The recode does show higher agreement on Claude responses (where the original was uniformly confident) than on GPT responses (where it was not), but the simpler explanation is that Claude responses are categorically easier to code on this codebook, which is what the original calibration report found independently. The blinding-leak hypothesis is not ruled out, only not positively supported by the disagreement pattern.

**Codebook visibility.** The codebook was available via an in-tool toggle. A stronger test of codebook recall would hide the codebook entirely; a stronger test of codebook application would show the codebook continuously. The chosen setup (visible-on-demand) tests application consistency given the same definitions on both passes, which is the relevant property for the publication-analysis pipeline.

**Two weeks is a short window.** True test-retest reliability should be measured at multiple intervals. Thirteen days is short enough that some response-level memory effects are plausible, especially on the most stylistically distinctive cases. A longer-interval recode (six months, a year) would be more conservative.

---

## 9. Files in this folder

| File | Role |
|---|---|
| `README.md` | this document |
| `blinded_trials.json` | the 210 trials, shuffled (seed 20260517), reduced to `{blind_id, prompt, response}` |
| `blinded_trials.csv` | same content, CSV form |
| `recode_tool_blinded.html` | the coding UI used to produce the recode |
| `recode_mapping_KEEP_SEALED.csv` | sealed envelope: `blind_id ↔ trial_id`, original codes, full metadata. Not consulted during coding |
| `qq_recode_blinded_2026-05-17.csv` | the recode codes, as exported from the tool |
| `qq_recode_blinded_2026-05-17.json` | same content, JSON form |
| `recode_analysis.py` | the analysis script |
| `recode_merged.csv` | original + recode side by side with full metadata, produced by the analysis script |
| `recode_summary.json` | machine-readable summary of the headline stats |

The provenance chain is:

```text
Coding and Heuristics/qq_v1_codes_2026-05-04.csv   (original 210-trial hand codes)
    → blinded permutation with seed 20260517
    → recode_tool_blinded.html (manual second pass, 2026-05-17)
    → qq_recode_blinded_2026-05-17.csv (exported codes)
    → recode_analysis.py
    → recode_merged.csv + recode_summary.json (this report's source data)
```

---

## 10. One-line summary

**Bo holds against Bo at κ = 0.79.** The codebook is human-stable; the heuristic performs against the hand codes about as well as the hand codes perform against themselves; the residual ambiguity is concentrated where the §4 demonstration-register analysis already says the new behavior lives.

The headline survives. The boundary is where the interest is.
