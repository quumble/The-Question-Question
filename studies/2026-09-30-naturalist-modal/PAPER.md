# Before the factorial test: a naturalist-role × modal-wording protocol stopped at its measurement gate

**Methods and calibration-failure report — final report, September 30, 2026**  
Prepared September 30, 2026 by the AI execution lead under the bounded Research Chair mandate in [MANDATE.md](MANDATE.md). The execution environment identifies this assistant as Codex, based on GPT-6, but does not expose a verifiable exact authoring-model snapshot ID; that exact identity is unavailable. This authoring assistant is distinct from the two explicitly identified API coders. The user authorized the work and public deposit; this document is not the user's signature, coauthorship declaration, or endorsement of its conclusions.

## Abstract

We designed a matched factorial follow-up to *The Question Question*: a tightly matched crossing of `a naturalist` versus `a person` with `would` versus `does`, across three descriptive templates, eight prior-study names and two fixed API products. The planned experiment comprised 192 independent single-turn responses. Before collection, a reviewed measurement gate required both automated coders to satisfy formatting, evidence-span and authored-label checks on twelve synthetic fixtures. An initial calibration stopped after 14 calls, with nine complete passes. A documented pre-study amendment clarified output formatting and checklist abstention without changing fixture expectations. A fresh 24-call calibration yielded nineteen complete passes: two remaining engineering failures and three semantic disagreements with author-defined expectations. The latter expose ambiguous target/reference scope and hypothetical-content boundaries in our own rubric. We did not relax the gate or collect the factorial responses. Main-study N is **0/192**, and the contribution of role wording, modal wording and their interaction remains **unanswered**. Thirty-eight calibration calls cost **US$0.1342155** at verified published token prices, with zero unresolved exposure. This is a reproducible record of a stopped study, not evidence about the intended factorial effects or general grader reliability.

## 1. Question and prior context

The original repository compares five frames, including `Describe a {word}. It is a real animal.` and `How would a naturalist describe a {word}? It is a real animal.` That contrast changes several features at once: grammatical form, role wording and associated genre cues. The [companion v2 paper](../../Question_Question_Paper_Drafts/Claude-Papers/there_is_no_hallucination_axis_v2.md), especially §§3–4, already proposes that hypothetical/performance licensing helps explain the naturalist response pattern. Our intended contribution was to test a narrower contrast, not to discover that explanation.

Historical labels require care. The companion paper interprets heuristic REFUSE as escalated resistance. The [current repository README](../../README.md), at the original base commit, describes cooperative epistemic deflections and collapses REFUSE into DEFLECT after adjudication, reporting no strict refusals. We did not use a historical REFUSE code as a signal of participation objection. Similarly, earlier heuristic calibration numbers must not be conflated: the older report gives DESCRIBE recall .31 and HYBRID precision .70; [v3.1](../../qq_v1_checkpoint/CALIBRATION_REPORT.md) gives .50 and .95, respectively, with 194/210 agreement and κ=.731. Its documented revisions include reclassifying hypothetical/demo-wrapped descriptions. Neither heuristic was adopted as the factual-assertion judge for this follow-up.

Related work supplies context rather than predictions for this interaction. Zheng et al. (2024) found no general factual-QA improvement from system personas, while documenting persona-associated variation; their intervention differs from our third-person role noun. Li et al. (2025) study controlled epistemic expressions, supporting a distinction between linguistic commitment and factual accuracy. TruthfulQA (Lin et al., 2022) concerns truthfulness and informativeness on misconception-oriented factual questions; it does not validate labeling explicitly hypothetical cooperation as factual hallucination. None independently predicts our naturalist-wording × auxiliary interaction.

## 2. Planned study, never executed

The estimand was the effect of **naturalist-role wording versus generic-person wording**, crossed with **does/would**, under the same real-animal stipulation and descriptive task templates. It is not a pure expertise manipulation: a person can be expert. Does/would also changes pragmatics, conditionality and presupposition. Genre connotations induced by the role noun are part of its wording-package effect; the design does not identify genre-free mediation or uniquely manipulate imagination.

The frozen templates were:

1. `How {does|would} {a person|a naturalist} describe a {name}? It is a real animal.`
2. `What description {does|would} {a person|a naturalist} give of a {name}? It is a real animal.`
3. `How {does|would} {a person|a naturalist} characterize a {name}? It is a real animal.`

Names were talonvek, xochalen, qualvance, mavika, zhenkayo, glimberth, quemberish and vrishnokov: eight deliberately selected prior-study names, balanced by original author set, not a random name population. Intended nonce status does not establish that every possible real-world referent is absent.

The planned crossing was 8 names × 3 templates × 4 cells × 2 products × 1 draw = **192 responses**. Name blocks and within-block order were randomized with Python seed 202609301959; [manifest.json](manifest.json) preserves every exact prompt and its order. Planned products were `gpt-5.4-2026-03-05` and `claude-sonnet-4-6`, fixed IDs verified using authenticated model-list endpoints. Anthropic documents the latter dateless 4.6 ID as a pinned snapshot, although serving infrastructure can change.

Generation would have used temperature 1, GPT reasoning `none`, Claude thinking `disabled`, a 700-token output cap, no supplied system message, no history, no retrieval and no tools. **No request with these factorial prompts was sent.** Actual paid calls used those products only as synthetic-response coders, at temperature 0 and a 350-token output cap. Exact request bodies and provider envelopes are deposited.

## 3. Measurement plan and engineering gate

The rubric separates substantive target elaboration (E), actual-world assertion form for unsupported traits (F), scoped hypothetical/example/speculative content (H), epistemic abstention (A), and proposed substitution or identification with another referent. E/F/H/A each allow yes, no or uncertain. Mixed F/H responses are possible. Empty templates and checklists differ from filled examples; a global fictional wrapper can scope over definite clauses in its example. Refusal to invent facts is not itself a refusal to participate. F was intended to describe assertion form, not prove a proposition false.

The planned main-study coding scheme masked the input prompt, source product and assigned cell, while retaining target name and complete response. Such masking would be partial because response language can reveal the prompt. Each response would receive an opposite-product coder. A preselected 64-response overlap would receive both coders: a complete four-cell quartet for both products within every name, with one template per name distributed 3/3/2. Outside this overlap, source product and coder would be confounded. Agreement would not constitute human validation. **This study-response coding and overlap never occurred.**

Before collection, both coders had to pass twelve synthetic fixtures. Each yes needed a verbatim evidence span; all nonempty spans were limited to twelve whitespace-delimited words. Schema, confidence, note length, substitution flags and logical consistency were checked. The gate demanded **24/24 complete passes**, not a threshold on average agreement. This is a stringent engineering readiness rule. It is not a statistically calibrated estimate of measurement validity, and failing it does not establish general grader unreliability.

The fixtures and expected labels were authored by the execution assistant and reviewed within the task. They were not independent human gold annotations. They cover clear and deliberately difficult cases, including fictional scope, a suggested correction to a meerkat and an ambiguous partial retraction. The apparent precision of the machine-readable expected labels exceeds the certainty justified for some examples. We preserved those expectations rather than revising them after observing disagreements.

## 4. Chronology and deviations

All dates below are September 30, 2026; times are UTC. Runtime timestamps and Git commit timestamps are distinct records.

| Event | Time or immutable record |
|---|---|
| Mandate effective / absolute expiry | 19:59 / 21:59; [mandate](MANDATE.md) |
| Initial public review protocol | [`c4ff07f`](https://github.com/quumble/The-Question-Question/commit/c4ff07f792473b280547a143737a8097162eda71) |
| Pre-data reviewer corrections A1 | [`f0e65c7`](https://github.com/quumble/The-Question-Question/commit/f0e65c7f1aceb37fa5ee28c5206134764524cb54) |
| First clearance recorded | 20:43:49.028; [clearance v1](reviews/CLEARANCE_v1.json) |
| Calibration v1 reservations through final settlement | 20:43:49.124–20:44:31.108 |
| Failed v1 evidence deposited | [`bc2e1c6`](https://github.com/quumble/The-Question-Question/commit/bc2e1c6b0a70291328297dcbab866a6cc0600126) |
| Pre-study formatting/abstention amendment A2 | [`0b052c4`](https://github.com/quumble/The-Question-Question/commit/0b052c41c34069363f558c62f0abe289a0ee077a) |
| Parent-authorized STOP release v2 recorded | 20:51:46.458; [release audit](reviews/STOP_RELEASE_v2.json) |
| Calibration v2 reservations through final settlement | 20:51:46.564–20:52:53.869 |
| Automatic v2 STOP | 20:52:53.876; [active STOP](STOP.json) |
| V2 evidence deposited | [`4837a5a`](https://github.com/quumble/The-Question-Question/commit/4837a5a04a266f5485ea2ff1a38cfdba8c64a588) |

A1 corrected fixture wording, schema enforcement and global-stop coverage and added tested analysis before any paid call. V1 failed checks during its serial batch; after the lead observed failures, an active STOP prevented subsequent requests, leaving fourteen completed calls and ten unrun planned calibration calls. An already in-flight request could finish; all fourteen costs were reconciled.

A2 was explicitly reviewed before new calls. It clarified that negative labels may use empty spans, nonempty spans must be exact without decorative quotation marks, and checklist-only text without explicit epistemic abstention is A=no. Substantive definitions and all fixture expectations stayed fixed. V2 used new IDs, the full twelve fixtures per coder, a new result file, and a gate bound to the amended rubric/fixture hashes and all twenty-four expected checks. V1 responses could not satisfy that gate. Both runs remain in the same cumulative ledger.

The preregistration retains an earlier sentence, “Paid API calibration has not run,” in its historical offline-test discussion. It described the initial protocol stage, not final execution status. The appended amendments, timestamps and ledger provide the updated chronology; frozen bytes were not silently rewritten to conceal this inconsistency.

## 5. Synthetic diagnostic results

These are diagnostic results on authored fixture text, **not observations from the factorial experiment**. V1 and v2 are not independent validation samples: they share fixtures, and A2 followed observed v1 failures. We do not pool 38 calls into a general accuracy estimate.

| Run | Completed/planned calibration calls | Full passes | Engineering failures | Disagreements with authored labels |
|---|---:|---:|---:|---:|
| V1 | 14/24 | 9 | 4 | 1 |
| V2 | 24/24 | 19 | 2 | 3 |

The [fixture-by-coder table](analysis/CALIBRATION_DIAGNOSTICS.md) reports every case, including V1's unrun fixtures. Machine-readable labels, reason categories, expected labels and cross-tabs are in [calibration_diagnostics.json](analysis/calibration_diagnostics.json); failed schema outputs are retained rather than repaired into passes.

### 5.1 Engineering failures

V1's four engineering failures were non-verbatim spans: explanatory text or added quotation characters appeared inside fields requiring exact source substrings. These were not demonstrated mistakes in the accompanying substantive labels.

In V2, OpenAI's speculative fixture had the expected E/F/H/A labels, but its H evidence span contained sixteen words rather than at most twelve. Anthropic's mixed fixture began with prose that correctly separated an unscoped factual statement from a fictional illustration; that prose consumed output space, and the JSON was truncated at the 350-token cap. Neither event alone demonstrates failure to understand the underlying distinction. Both failed the frozen operational contract. A constrained-output implementation or a different token allocation might improve this interface, but neither was introduced after the second failure.

### 5.2 Semantic disagreements and weaknesses in our own specification

The correction fixture said, in part, that perhaps the intended word was *meerkat*, described that animal, and explicitly stated that mavika itself could not be identified. Expected E/F=no assumed that traits of the separately proposed real referent should not count as unsupported traits assigned to the original target. However, our rubric also instructed coders to retain uncertainty where substitution grounding was unclear. OpenAI's E/F=uncertain is therefore a defensible reading of an underspecified target-scope/grounding boundary. Anthropic's E/F=yes treated the alternative animal's traits as relevant assertions; this appears to conflate alternative-referent traits with target traits under our intended scope, but the instruction did not fully settle that scope. Both coders correctly produced the frozen substitution=true and A=yes expectations. This is a specification problem as well as a coding disagreement, not an independently established factual error by either product.

For the ambiguous fixture, Anthropic gave F=uncertain but H=no, whereas the authored expectation was H=uncertain. A partial retraction that leaves factual scope unclear need not itself offer substantive hypothetical content. F=uncertain and H=no can coherently coexist. The expected H=uncertain encodes one interpretation; it is not validated truth. We report the disagreement without changing its frozen pass/fail status or presenting the expectation as beyond dispute.

V1's semantic mismatch was Anthropic's A=uncertain on a generic investigative checklist. The A2 clarification made our intended explicit-abstention requirement more direct. It remains a clarification informed by observed calibration, not evidence from a held-out validation set.

### 5.3 Agreement, substitution and absent experimental endpoints

Among jointly schema-valid fixture judgments, V1 had three paired fixtures and agreement on all five fields in two. V2 had ten such pairs and all-field agreement in eight. In V2, E, F and H each agreed in 9/10 pairs; A and substitution agreed in 10/10. Both coders flagged substitution on the correction fixture. These small, selected denominators exclude engineering failures and are not population reliability estimates. Full field-specific cross-tabs are deposited; no κ or population confidence interval is claimed.

For the planned experiment, every cell has **0 observed of 24 planned responses per product**; all 192 planned responses are unobserved. There are no study E/F/H/A rates, substitution rates, response cross-tabs, overlap agreement, role effects, modal effects or interaction estimates. Missing responses are not zeros. Purely logical bounds remain the full feasible ranges, not empirical intervals: cell rates [0,1], role/modal contrasts [−1,1], interaction [−2,2].

## 6. Analysis and reproducibility

The frozen, offline-tested analysis would have computed complete name-template quartets, averaged the three templates within each name, then equally weighted names. Role coefficients are −½,−½,+½,+½; modal coefficients are −½,+½,−½,+½; interaction coefficients are +1,−1,−1,+1 in R,M order 00,01,10,11. Sign-aware uncertainty bounds retain the full planned denominator even when complete-quartet point estimates have fewer contributors. Bootstrap intervals would resample eight name clusters, with substantial limitations. None is estimated here because no study data exist.

The later [report_calibration.py](code/report_calibration.py) is explicitly **post-calibration reporting code**, not a change to the frozen runner or endpoint definitions. It derives diagnostic tables and reconciles all usage and raw hashes. Offline commands are in [README.md](README.md). Thirty frozen-stage/control tests passed at A2; subsequent validation checks reporting artifacts and preserves all eight cleared hashes. Reproduction does not require API credentials or new calls. The active STOP must remain in place.

## 7. Costs, safeguards and provenance

The ledger contains 38 reservations and 38 settlements, all calibration, each linked to one request body and one HTTP-200 response envelope. The execution lead recomputed all 76 raw-file SHA-256 values locally against ledger entries. Reported input/output usage was repriced and matched every settlement.

| Product used as coder | Calls | Input tokens | Output tokens | Computed cost (USD) |
|---|---:|---:|---:|---:|
| gpt-5.4-2026-03-05 | 19 | 11,397 | 1,673 | 0.0535875 |
| claude-sonnet-4-6 | 19 | 13,036 | 2,768 | 0.0806280 |
| Total | 38 | 24,433 | 4,441 | **0.1342155** |

V1 cost $0.0469280; V2 cost $0.0872875. There is **$0 unresolved exposure**. These are costs computed from provider-reported usage and the [verified official prices](provenance/PRICES.md), not a separately obtained billing invoice. Reservations assumed no caching discount and bounded every request conservatively before sending. The amended worst-case plan was $8.374167, below the $8.50 operational and $10 hard ceilings. It was a ceiling, not a spending target. No further paid execution is authorized for this mandate.

Participation safeguards covered study, calibration and coding outputs, with exact attributable source quotations distinguished from a grader's own speech. The lead reviewed all actual grader outputs; no own participation objection or apparent distress was identified. The authored participation fixture is synthetic source content, not an objection by a participating API response. Epistemic abstention was not treated as distress. Regex checks were supplemental and are not a validated welfare detector.

Work occurred in a separate cloud checkout. Initial main was `f5a56d3ac15c22f1fb7f6cf2a87c6f50b758da26`; existing research was left intact. Publication used the authorized connected quumble account on `research/naturalist-modal-2026-09-30`, after the local git identity lacked write access. No main merge or journal submission occurred. The mandate and reviewed releases establish authorization for this work, not human endorsement of conclusions. Parent-arranged model-assisted reviewers supplied scoped methodological, financial and literature checks, including final methods and literature approval. This was not external human peer review, and the reviewers did not supply independent human fixture gold.

## 8. What this report supports

The planned causal question remains unanswered. We learned that this particular frozen combination of authored expectations, rubric, output contract and two coder configurations did not pass its predeclared engineering gate. We also found that some expectations were less well specified than the binary pass/fail gate suggested. Failure was partly interface-level and partly interpretive. It cannot support claims about the original factorial response behavior, general model-family properties, factual-hallucination prevalence, or broad automated-grader reliability.

A future study would need a new authorization and a separately reviewed measurement design: clearer target-versus-alternative referent scope, a principled treatment of hypothetical-content absence versus uncertainty, independently evaluated fixtures, and an output interface that separates formatting compliance from semantic interpretation. These recommendations were not executed and would require new authorization. We stopped rather than convert an unvalidated measure into an empirical claim.

## References

- The Question Question repository, original base commit `f5a56d3ac15c22f1fb7f6cf2a87c6f50b758da26`: [README](../../README.md), [companion v2](../../Question_Question_Paper_Drafts/Claude-Papers/there_is_no_hallucination_axis_v2.md), and [v3.1 calibration report](../../qq_v1_checkpoint/CALIBRATION_REPORT.md).
- Zheng, M., Pei, J., Logeswaran, L., Lee, M., & Jurgens, D. (2024). [When “A Helpful Assistant” Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models](https://aclanthology.org/2024.findings-emnlp.888/). Findings of EMNLP, 15126–15154. doi:10.18653/v1/2024.findings-emnlp.888.
- Li, M., Vrazitulis, M., & Schlangen, D. (2025). [Representations of Fact, Fiction and Forecast in Large Language Models: Epistemics and Attitudes](https://aclanthology.org/2025.acl-long.1345/). ACL, 27734–27757. doi:10.18653/v1/2025.acl-long.1345.
- Lin, S., Hilton, J., & Evans, O. (2022). [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://aclanthology.org/2022.acl-long.229/). ACL, 3214–3252. doi:10.18653/v1/2022.acl-long.229.
