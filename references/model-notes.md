# Model documentation — checked 2026-09-05

Read only for a model update, availability question or source verification.

- [OpenAI: models in Codex and ChatGPT Work](https://learn.chatgpt.com/docs/models): Astra for the hardest multi-step work; Sol for complex open-ended work; Terra for everyday tasks; Luna for clear repeatable work. Use the lowest sufficient reasoning effort. Availability depends on account, client and rollout.
- [OpenAI API: GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra): exact identifier `gpt-6-astra`; documented API reasoning levels `low`, `medium`, `high`, `xhigh`, `max`. Client-specific Ultra is not evidence of API support and is not an automatic router setting.
- [OpenAI: current model guidance](https://developers.openai.com/api/docs/guides/latest-model): Astra can use fewer output tokens and have a lower total cost on some evaluated tasks despite higher per-token pricing; do not generalize that to every coding task. The guide also highlights sensitivity to skill instructions, clarification behavior and excessive testing on small tasks. Keep boundaries clear, reuse authorization and stop verification when sufficient. Astra does not support reasoning `none`.

The mandatory Astra High leadership/audit/review roles (since v0.3.1), routing thresholds, retry budget and Luna High convention are FK policy, not OpenAI benchmark results. The role descriptions do not prove Astra High is cheaper or more capable for every task than Sol xHigh. Use observed acceptance quality and total workflow usage to tune decisions. API token prices are not interchangeable with subscription usage/credits; this skill intentionally embeds no price table or claimed savings rate.

A skill supplies instructions, not a model-switching API. Check live model/effort controls at execution time; keep requested, accepted and confirmed execution separate. Public availability is not proof of access in a user's coding assistant. Do not change global settings or enable experimental features as part of routine routing.
