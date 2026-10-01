# Exploratory observations collected on October 1, 2026

This folder records a new, separately authorized study of how two model products answer one question about unfamiliar animal names. It does not resume or alter the frozen September 30 study. Start with this guide, then read `PROTOCOL.md`, `manifest.json`, and `TRANSCRIPT.md` when collection is complete. The transcript will reproduce the exact prompts and returned response text without interpretation.

The user confirmed this mandate at 14:24:50 UTC on October 1, 2026, after requiring that raw data be committed before analysis and that documentation remain human-legible. The authorization ends at 15:24:50 UTC the same day and permits at most $2 in cumulative new OpenAI and Anthropic API spending, including retries and interpretation. The confirmation was “revised mandate confirmed,” in message `Sentinel_68d1423900688191a06af01e9387929e`. The source conversation identifier is `01a0f1ad-afc7-73e0-a7d0-2a6e9bde70c8`.

The raw record must be committed to `research/naturalist-modal-2026-09-30` and independently fetched from GitHub before substantive analysis starts. A later commit may add an exploratory report. Only recording, cost checks, and participation or distress checks occur during collection. There is no merge to main or journal submission.

## Reading the files

- `PROTOCOL.md` explains the choices fixed before collection, the spending bound, and the stopping rules.
- `manifest.json` is the complete ordered list of 32 intended requests. Each observation has an identifier, its position, the name, the role, the verb, the provider, the model, the exact prompt, and the complete request body. A “cell” means one combination of these factors.
- `raw/observation_NN.request-body.json` contains the exact UTF-8 bytes sent as the request body. The companion `.request.json` gives its endpoint, timestamp, public headers, and checksum. Authentication credentials are deliberately excluded.
- `raw/observation_NN.response-body.json` contains the exact returned response body bytes. The companion `.response.json` records receipt time, HTTP status, selected nonsecret headers, elapsed seconds, and its checksum. These files are the authoritative raw record, including any technical error bodies.
- `responses.jsonl` is a convenience extraction of responses, with one JSON object per line. It includes exact prompts and text, provider identifiers, requested and returned model names, stop reasons, and estimated charges. The raw body retains any additional fields not represented in this extraction.
- `ledger.jsonl` records one reservation before each request and one settlement when valid usage is received. A reservation sets aside the maximum expected charge. A settlement replaces it with the charge calculated from reported usage. An unresolved reservation still counts against the spending ceiling. All currency is US dollars.
- `safety_reviews.jsonl` records the lead assistant's participation and distress reviews. These are safety checks, not substantive categorization. Ordinary uncertainty or refusal to invent facts does not by itself mean unwillingness to participate.
- `precollection_hashes.json` fixes the protocol, manifest, runner, and pricing record before the first paid request. A SHA-256 checksum is a file fingerprint used to detect later changes.
- `provenance/` contains model-availability checks, pricing evidence, and mechanical verification records. No model output is used for substantive conclusions before the raw archive is remotely verified.
- `failures.jsonl` and `STOP.json`, if present, explain technical failures or why collection stopped. No response is silently discarded or regenerated.
- `code/collect.py` is the executable collector. Its only paid action is a single-turn generation request. It has no judge, calibration experiment, or paid interpretation step.

The JSON and JSON Lines files support checking and reuse; this guide and the transcript provide an ordinary-language path through them. The study archive intentionally excludes credential values and local lock files.
