# Model guidance — checked 2026-09-05

Read only for a model update, availability question or source verification.

- [OpenAI: models in Codex and ChatGPT Work](https://learn.chatgpt.com/docs/models): Astra for the hardest multi-step work; Sol for complex open-ended work; Terra for everyday tasks; Luna for clear repeatable work. Use the lowest sufficient reasoning effort. Availability depends on account, client and rollout.
- [OpenAI API: GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra): exact identifier `gpt-6-astra`; documented API reasoning levels `low`, `medium`, `high`, `xhigh`, `max`. Client-specific Ultra is not evidence of API support and is not an automatic router setting.
- [OpenAI: current model guidance](https://developers.openai.com/api/docs/guides/latest-model): Astra can use fewer output tokens and have a lower total cost on some evaluated tasks despite higher per-token pricing; do not generalize that to every coding task. The guide also highlights sensitivity to skill instructions, clarification behavior and excessive testing on small tasks. Keep boundaries clear, reuse authorization and stop verification when sufficient. Astra does not support reasoning `none`.

The v0.4 routing thresholds, hard work-unit budget, proportional review tiers and Luna High convention are FK policy, not OpenAI benchmark results. Astra High remains the default for explicit audits, architecture review and the highest risk tier; it is no longer an unconditional coordinator/reviewer for every routed task. The role descriptions do not prove Astra High is cheaper or more capable for every task than Sol High or Sol xHigh.

A skill supplies instructions, not a model-switching API. Check live model/effort controls at execution time; keep requested, accepted and confirmed execution separate. Public availability is not proof of access in a user's coding assistant. Do not change global settings or enable experimental features as part of routine routing.

Evaluate cost using the complete accepted workflow, including coordination, context transfer, workers, reviews, retries and elapsed time. API token prices are not interchangeable with subscription usage or credits. Embed no price table or claimed savings percentage.
