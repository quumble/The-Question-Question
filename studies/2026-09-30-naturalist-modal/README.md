# Naturalist-role × modal-wording follow-up — stopped at calibration

**Main study: 0/192 responses. Research question unanswered.** Two synthetic calibration rounds did not satisfy the reviewed gate. Paid execution is closed; active STOP remains. Total API cost computed from reported usage: **$0.1342155**, 38 calls, zero unresolved exposure.

Start with [PAPER.md](PAPER.md). It is a methods/calibration-failure report, not an empirical result for the factorial experiment.

## Research index

| Material | Purpose |
|---|---|
| [MANDATE.md](MANDATE.md) | Confirmed authority, acceptance, fixed 19:59–21:59 UTC term |
| [PREREGISTRATION.md](PREREGISTRATION.md), [AMENDMENTS.md](AMENDMENTS.md) | Frozen design and preserved amendment chronology |
| [manifest.json](manifest.json), [coding_overlap.json](coding_overlap.json) | Exact never-executed study prompts, randomization and overlap |
| [CODING_RUBRIC.md](CODING_RUBRIC.md), [fixtures](synthetic/fixtures.json) | Exact rubric and authored synthetic expectations |
| [V1 failure checkpoint](synthetic/calibration_failure_checkpoint.json), [V2 result](synthetic/calibration_v2_result.json) | Preserved calibration pass/fail records |
| [Diagnostic tables](analysis/CALIBRATION_DIAGNOSTICS.md), [JSON](analysis/calibration_diagnostics.json), [CSV](analysis/calibration_diagnostics.csv) | Post-calibration synthetic reporting; not factorial outcomes |
| [Ledger](ledger.jsonl), [completion report](COMPLETION_REPORT.json) | Every reservation/settlement and reconciled totals |
| [Raw calibration files](raw/calibration/) | 38 exact request payloads and 38 response envelopes; no request authentication headers |
| [Reviews](reviews/), [STOP.json](STOP.json) | Frozen hashes, authorizations, prior stop/release and active global stop |
| [Pricing/model provenance](provenance/PRICES.md) | Official price references and nonsecret model-list responses |
| [Runner](code/study.py), [planned analysis](code/analyze.py) | Frozen collection controls and tested paired-analysis implementation |
| [Post-calibration report code](code/report_calibration.py) | Offline reporting and per-attempt raw/usage reconciliation |

The two calibration rounds reuse authored fixtures, and round 2 followed round 1 failures. Do not pool 38 calls as independent validation accuracy. The historical phrase “Paid API calibration has not run” in a preserved preregistration section refers to the initial draft stage, not final status.

## Reproduce offline

From the repository root, with Python 3.12 or a compatible standard-library Python:

```bash
python -m unittest discover -s studies/2026-09-30-naturalist-modal/code -p 'test_*.py' -v
python studies/2026-09-30-naturalist-modal/code/report_calibration.py
python studies/2026-09-30-naturalist-modal/code/study.py status
```

These commands do not invoke generation APIs. Reporting imports definitions from the runner but never invokes its paid call function. It verifies all raw-file hashes, usage settlement, model IDs, complete accounting and unchanged cleared hashes before regenerating diagnostic tables and the completion JSON. Tests mock network calls and use temporary directories. Do not delete STOP or invoke paid execution; this mandate's collection is closed.

No study-response files exist, by design. The planned-analysis code is tested on clearly labeled synthetic values; running it with no study data would produce only uninformative missing-data bounds. Such output is not an observed null effect.

All additions are confined to this study folder on the separate research branch. Original studies and main remain unchanged. No journal submission, merge, or founder endorsement is implied.
