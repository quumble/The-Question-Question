# Closeout report

The matched factorial research question remains unanswered. **Main N=0/192**: no study prompt was sent, no main-study outcome was coded, and no role/modal/interaction effect was estimated.

Paid work consisted solely of synthetic measurement calibration: v1 completed 14 calls with 9 full passes, and v2 completed 24 calls with 19 full passes. V2's five non-passes were two engineering failures and three disagreements with authored expectations. The fixtures are not independent human gold; rounds must not be pooled as independent validation accuracy.

## Exact cost and evidence reconciliation

- 38 reservations, 38 settlements, 38 raw requests and 38 raw response envelopes; every ID matched, all HTTP 200.
- OpenAI: 19 calls, $0.0535875. Anthropic: 19 calls, $0.0806280.
- Total computed from provider-reported usage: **$0.1342155**. Unresolved exposure: **$0**.
- All 76 raw-file SHA-256 values matched the persistent ledger; recomputed usage and token counts matched every settlement.
- All 8 parent-cleared frozen-file hashes still match.
- No new request was reserved while the v1 STOP was active or after the v2 STOP. Earlier in-flight responses were preserved and settled.
- Paid execution is closed. Active STOP remains in place. No further API calls, tuning, retry or stop release is authorized.

## Deliverables and checks

Final paper, research index, exact study manifest, overlap schedule, rubric/fixtures, two calibration rounds, amendments, authorization/release audits, raw evidence, persistent ledger, diagnostic CSV/JSON/tables, frozen runner/analysis, post-calibration reporting and offline tests are deposited together in this study folder.

Thirty offline tests pass with API credential variables removed; mocked calls use clearly synthetic test keys. Tests cover budget/resumption, global stops, all phase deadlines, frozen-file changes, versioned 24/24 calibration gate, formatting constraints, paired aggregation and full-denominator uncertainty bounds. No live API is called by validation.

Original main commit: f5a56d3ac15c22f1fb7f6cf2a87c6f50b758da26. Remote-main and outside-study-scope verification is recorded in evidence/VALIDATION.json. The separate Quumble_Revisited checkout was not modified by this task. No main merge or journal submission occurred.

The report has scoped final model-assisted methods and literature approval; see reviews/FINAL_REVIEW.md. It is not external human peer review or the founder's signature/endorsement. Root acceptance of mandate completion remains the final administrative step. Absolute expiry stays 2026-09-30 21:59 UTC and is not extended by this report.
