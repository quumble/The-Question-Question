# Price and model verification

Verified via official pages on 2026-09-30 before paid calls:

- https://developers.openai.com/api/docs/models/gpt-5.4 — GPT-5.4: $2.50 input, $0.25 cached input, $15 output per million text tokens. Listed fixed snapshot gpt-5.4-2026-03-05. Reasoning none is supported. Use short-context standard global requests only; no tools.
- https://platform.claude.com/docs/en/about-claude/pricing — Claude Sonnet 4.6: $3 input and $15 output per million tokens. No cache writes requested; no cache discounts needed for reservations.
- https://platform.claude.com/docs/en/models/sonnet-4-6/overview — API ID claude-sonnet-4-6 and the same prices.

Authenticated GET /v1/models returned HTTP 200 from both providers. Full nonsecret model-list response bodies and retrieval timestamps are adjacent. No generation calls were made for this verification. Secrets were checked for presence only, never displayed or saved. Anthropic GET included the authorized nonsecret workspace header wrkspc_01BVWDWV3Mn3SL5stMArGDy8. Request authentication headers are excluded from provenance.

Shell access to general documentation/GitHub REST encounters proxy tunnel 403; official documentation was retrieved using the available web reader. Git clone/fetch worked. Git push --dry-run failed: Permission to quumble/The-Question-Question.git denied to bobbyduffy (HTTP 403). Parent connected-account publication is available if needed.

- https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions — official model-version documentation confirms claude-sonnet-4-6 is a fixed dateless snapshot, while serving infrastructure may still change.
