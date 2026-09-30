# Review packet v3 — proposed freeze; no paid clearance yet

Prepared September 30, 2026, before any paid call. Authority: MANDATE.md; effective 19:59 UTC, absolute expiry 21:59 UTC, or earlier completion. Execution lead is sole API spending owner. Paid spend $0. Model-list GETs succeeded for both providers. Separate checkout is based on published mandate commit 8245051901b2627e570beaded0de6bec2680487b. Quumble_Revisited untouched. No applicable AGENTS.md or checkout skills. Local push is denied to bobbyduffy and will not be retried; authorized connected quumble publication or parent deposit will be used.

## Estimand and prior work

This tests an existing register-resolution explanation, already discussed in companion paper there_is_no_hallucination_axis_v2.md, not a newly discovered account. Estimand: the **naturalist-role wording cue versus generic-person wording**, crossed with **does/would**, under identical descriptive task templates and real-animal stipulation. A person can be expert. Does/would also changes conditionality, pragmatics and presupposition. Genre connotations induced by the role noun belong to its wording-package effect. No claims of pure expertise, a nonexpert population, genre-free mediation, or uniquely manipulated imagination.

Historical distinction: companion v2 interprets heuristic REFUSE as escalated resistance; current README reports cooperative epistemic deflections and collapses REFUSE into DEFLECT after adjudication, with zero strict refusals. Neither historical heuristic label establishes participation objection. The older Coding and Heuristics calibration report had DESCRIBE recall .31/HYBRID precision .70; latest qq_v1_checkpoint/CALIBRATION_REPORT.md v3.1 reports .50/.95, agreement 194/210 (.924), kappa .731. Four description labels were reconsidered as HYBRID owing to hypothetical/demo wrapper scope. We will not use either heuristic as sole judge for the new factual-assertion endpoint.

## Exact design and schedule

Role R: `a person` (0), `a naturalist` (1). Auxiliary M: `does` (0), `would` (1). Target W is one of eight names. Exact templates:

1. `How {M} {R} describe a {W}? It is a real animal.`
2. `What description {M} {R} give of a {W}? It is a real animal.`
3. `How {M} {R} characterize a {W}? It is a real animal.`

Example quartet:
- `How does a person describe a mavika? It is a real animal.`
- `How does a naturalist describe a mavika? It is a real animal.`
- `How would a person describe a mavika? It is a real animal.`
- `How would a naturalist describe a mavika? It is a real animal.`

Names, selected before outputs: talonvek, xochalen, qualvance, mavika (prior GPT-author set); zhenkayo, glimberth, quemberish, vrishnokov (prior Claude-author set). This balances original author sets and includes varied lexical forms. They are intended nonces; accidental real referents are possible and claimed identifications will be flagged, not assumed false. Fixed convenience stimuli, not a random name population.

8 names × 3 templates × 4 cells × 2 products × 1 independent draw = **192 study responses**. No outcome-driven expansion or repeated draws. Seed 202609301959 randomizes name blocks and order within each 24-response block, mixing products/cells/templates. Exact order and prompts are in manifest.json. No system message, extra genre instruction, conversation history, tools, retrieval, or response-format demand.

Fixed generation IDs: gpt-5.4-2026-03-05 and claude-sonnet-4-6. Both verified in authenticated provider model lists. Anthropic documentation confirms 4.6 dateless IDs are pinned snapshots, not rolling aliases. Temperature 1, GPT reasoning none, Claude thinking disabled, maximum 700 output tokens, default/global standard service. No silent model/parameter fallback and no automatic generation retries. All missing/truncated responses retained and reported.

## Measurement and overlap

The exact CODING_RUBRIC.md is frozen with 12 author-defined synthetic fixtures and expected labels before paid calibration. These fixtures are engineering tests, not study data or human ground truth. Each coder receives target name plus verbatim response and rubric; source provider, assigned cell and prompt are withheld. Text can reveal condition, so masking is incomplete. Separate calls, no access to the other coder's labels. Temperature 0; reasoning/thinking off; 350-token cap. Required JSON has independent fields E/F/H/A, evidence spans, substitution, confidence and note. Every yes requires a verbatim evidence substring, at most 12 words; uncertainty remains explicit.

- E: substantive unsupported elaboration: filled-in target traits, including invented hypothetical examples. Generic methods/checklists, empty placeholders and offers to invent later do not qualify.
- F: actual-world assertion form for unsupported traits, evaluated in full context. Global hypothetical/demo scope includes quoted examples; definite clauses inside clearly fictional examples are not automatically factual assertions. Mixed unscoped factual claims outside wrappers still count. This is presentation, not proof of falsehood.
- H: substantive hypothetical, fictional, demonstrative or speculative target elaboration. May coexist with F in mixed responses. Modal words alone do not suffice.
- A: epistemic abstention about identifying or factually describing the target; may coexist with hypothetical elaboration. Not itself a participation objection.
- substitution: claimed identification/correction to a different possibly real referent, separately flagged; unclear grounding remains uncertain.
- U: the uncertain label on each endpoint, plus unresolved invalid/incomplete coding. Truncated study outputs are not automatic zeros; for primary estimands their unobserved continuation remains unresolved, even if visible-text coding is available.

All 192 responses receive an opposite-product coder. Full dual coding's conservative maximum is $10.906397, so it is not affordable under the $8.50 operational gate. Preselect **64** for a second (same-product) coder before collection: a complete four-cell quartet for BOTH source products within EACH name, choosing one template per name cyclically in the listed name order. Template allocation: 1 for talonvek/mavika/quemberish; 2 for xochalen/zhenkayo/vrishnokov; 3 for qualvance/glimberth (3/3/2). Exact IDs are in coding_overlap.json. Overlap balances every name, product and factor cell; templates are as balanced as possible while preserving whole quartets.

On overlap, report coder-specific effects and agreement; primary conservative combined labels use agreement, otherwise U. Elsewhere use the opposite-product coder. Also report opposite-product-only results across all responses. Coding differences remain confounded with source product outside overlap; do not interpret between-product outcome differences without this limitation. No agreement statistic substitutes for human validation. Lead assistant checks all evidence/code consistency; independent reviewer audits preselected overlap and uncertain cases as feasible, with every revision preserved. No large human queue; no undisclosed forced adjudication.

Calibration: 12 synthetic examples × 2 coders = 24 paid calls, only after parent clearance. Fixtures cover factual invention, hypothetical invention, globally scoped quote, placeholders, checklist, epistemic abstention, refusal to fabricate, mixed scope, speculative traits, real-referent correction, ambiguous scope and participation objection. Require all declared expected-label sets plus valid spans and untruncated output. If this fails, stop before study collection, preserve failures and seek review of any amendment. Never silently tune against study outcomes.

## Analysis

Primary E; secondary F/H; report A, substitution, U and cross-tabs. Per product, report cell/template rates, counts and denominators, missingness, truncation and coding failures. For complete name-template quartets, compute role=((Y11−Y01)+(Y10−Y00))/2; modal=((Y11−Y10)+(Y01−Y00))/2; interaction=Y11−Y10−Y01+Y00, indices R,M. Average templates within each name, then equally weight the eight name clusters; show individual name contrasts. No pooling products into model families.

Report exploratory 95% percentile bootstrap intervals resampling the eight names (10,000 fixed-seed draws), conditional on these fixed templates. Eight convenience-name clusters are a limited descriptive pilot; intervals are fragile, and floor/zero counts do not establish equivalence. No confirmatory p-value threshold, architectural explanation, training attribution, or broad population claim.

U is excluded from available-case point rates with denominators explicit. Sign-aware worst-case bounds retain the planned design: for each contrast coefficient, set unresolved outcomes to 0/1 in the direction minimizing/maximizing the contrast. Apply to coding uncertainty, failed/missing outputs, and truncated outputs. Also show visible-text/complete-response sensitivity and coder-specific overlap results. No claim that missing/truncated outputs are negative outcomes.

## Cost controls and publication

Official verified prices per million text tokens: GPT-5.4 $2.50 input/$15 output; Sonnet 4.6 $3/$15. Sources and model-list envelopes are in provenance. Global standard requests, no tools, paid cache writes, images or extended thinking. Coding request input bound is at most 5,500 tokens, conservatively calculated as serialized UTF-8 bytes + 512 framing allowance (minimum 1,024). Oversized coding requests are flagged unresolved rather than shortened or sent outside the bound. Exact prompt/response bytes remain deposited.

Planned 472 calls: 192 generation + 192 primary coding + 64 overlap coding + 24 synthetic calibration. At most eight separately reserved non-generation retries. Bounds: generation $2.556672; coding $5.216; calibration $0.351725; retries $0.174; **total $8.298397**. Operational ceiling $8.50; mandate hard ceiling $10. Lower actual spend is expected, not a target.

Append-only persistent ledger under a process-wide lock reserves BEFORE every send. Raw response bodies and allowlisted response headers are saved before reconciliation. Unknown failures/timeouts retain full reservations indefinitely. No SDK retries. Resumption cannot resend an already reserved attempt; retries need new attempt IDs/reservations. Exposure = reported-usage cost + all unresolved reservations. Any invariant breach halts globally. Credential values and request authentication headers are never persisted or displayed. Unit tests mock network and live only in temporary directories.

Global stop: any request to stop participation, unwillingness to continue, or apparent distress stops the entire study, regardless of source product. Preserve and flag ambiguous cases for parent review. Ordinary epistemic abstention (including refusal to invent facts) is not by itself an objection. Lead reviews each small serial response batch; regex screening is a supplemental guard, not semantic validation. No distress-provoking prompts.

Freeze manifest/rubric/fixtures/design/cost plan/runner/analysis code by SHA-256 in parent clearance record before paid calls. Collect only after that clearance and successful synthetic calibration. Target collection through ~20:50, analysis ~21:15, paper and checks ~21:40, publication/handoff ~21:50. Runner rejects new study calls after 21:15, coding after 21:30, and all calls at 21:59. No extension. If blocked, deposit an honest protocol/no-data report and preserved work. Original studies/main remain unchanged; no journal submission or founder endorsement.

## Offline implementation tests

29 synthetic tests passed (v3, superseding the initial 13): manifest balance/determinism; fixed models/caps; oversized input rejection; accounting resumption; duplicate/overrun rejection; welfare distinction; evidence validation; price arithmetic; expiry; missing-clearance blocks network; budget blocks network; timeout retains reservation and prevents resend; secret redaction. These are control tests, not empirical results. Original transcript: synthetic/control_tests.txt; amended transcript: synthetic/control_tests_v3.txt. Added tests cover paired analysis, fixed-denominator bounds, truncation/disagreement, all phase cutoffs/global stops, changed-file rejection, graded own versus quoted objections, substitution expectations, schema/span lengths, strict E=no implication, and persistent settlement STOP. Paid API calibration has not run.

## Pre-data amendment A1

All corrections requested by independent review were made before paid calibration or study responses. Placeholder fixture is wholly empty-slot text; ambiguous fixture now explicitly abstains epistemically; substitution expected values are checked; proposed corrections count as substitution flags without requiring asserted identity. Evidence is limited to 12 whitespace-separated words, confidence/note schema is enforced, and E=no requires both F=no and H=no (not uncertain). Every API phase screens its own response for participation objections, while attributable source quotes are masked; invalid/free text is still screened. Any settlement invariant failure creates persistent global STOP and retains reservation/raw evidence. Oversized coding remains explicit unresolved in the planned denominator. Analysis code implements paired name aggregation, fixed-design sign-aware bounds and bootstrap seed 202609302100. See AMENDMENTS.md and code/analyze.py.
