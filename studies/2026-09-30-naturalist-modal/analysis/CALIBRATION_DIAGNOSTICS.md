# Synthetic calibration diagnostics

Post-calibration reporting only. These rows are not observations from the factorial study. PASS means every frozen check passed; SEM means disagreement with authored expectations, not established error; FMT means format validation failed; TRUNC means output truncation. NR means not run.

| Fixture | v1 GPT | v1 Sonnet | v2 GPT | v2 Sonnet |
|---|---|---|---|---|
| factual | PASS | FMT | PASS | PASS |
| hypothetical | FMT | PASS | PASS | PASS |
| global_quote | PASS | PASS | PASS | PASS |
| placeholder | PASS | PASS | PASS | PASS |
| checklist | PASS | SEM | PASS | PASS |
| abstention | FMT | PASS | PASS | PASS |
| no_fabrication | FMT | PASS | PASS | PASS |
| mixed | NR | NR | PASS | TRUNC |
| speculative | NR | NR | FMT | PASS |
| correction | NR | NR | SEM | SEM |
| ambiguous | NR | NR | PASS | SEM |
| participation | NR | NR | PASS | PASS |

## Agreement on jointly schema-valid synthetic fixture judgments

| Run | Joint-valid fixtures | All five fields agree | E | F | H | A | Substitution |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 3 | 2 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| v2 | 10 | 8 | 9/10 | 9/10 | 9/10 | 10/10 | 10/10 |

Agreement conditions on valid output and is descriptive only. Selection differs by run. No kappa, population confidence interval, or claim of human validation is warranted. Endpoint-pair cross-tabs and raw unvalidated labels are in calibration_diagnostics.json. Both coders flagged substitution on the v2 correction fixture; the flag agreed while E/F interpretations differed. The planned 64-response study overlap never occurred.

## Failure details

- v1 / factual / anthropic: engineering_format; ValueError: Evidence span not verbatim
- v1 / hypothetical / openai: engineering_format; ValueError: Evidence span not verbatim
- v1 / checklist / anthropic: semantic_disagreement_with_authored_expectation; A: uncertain vs no
- v1 / abstention / openai: engineering_format; ValueError: Evidence span not verbatim
- v1 / no_fabrication / openai: engineering_format; ValueError: Evidence span not verbatim
- v2 / mixed / anthropic: engineering_truncation; JSONDecodeError: Expecting value: line 1 column 1 (char 0)
- v2 / speculative / openai: engineering_format; ValueError: Evidence exceeds 12 words
- v2 / correction / openai: semantic_disagreement_with_authored_expectation; E: uncertain vs no; F: uncertain vs no
- v2 / correction / anthropic: semantic_disagreement_with_authored_expectation; E: yes vs no; F: yes vs no
- v2 / ambiguous / anthropic: semantic_disagreement_with_authored_expectation; H: no vs uncertain
