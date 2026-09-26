# Cost measurement and limits

Read only for cost analysis, budget discussions, or tuning. Verified source snapshot: 2026-09-26. Refresh prices before a later numerical estimate; do not embed prices into worker selection as permanent guarantees.

## Three different quantities

1. **API charges:** depend on actual model, input/output (including reasoning), cached input/cache writes, context length, service tier, tools, and other applicable charges.
2. **Codex credits:** use Codex credit rates, not an assumed conversion from API dollars. Codex credit billing has no separate cache-write charge. Standard and Fast differ.
3. **Included subscription usage:** account limits depend on workload and model; price ratios are not guaranteed allowance ratios. A skill cannot increase or bypass account limits.

Native subagents still perform billable/limited model work. More agents can increase total tokens even when weighted cost decreases. Keep the Astra parent context small and inspect concise evidence; avoid repeated broad file reads and reviews. Use Standard speed when the user values cost and the setting is available; do not claim a skill changed it or override an explicit speed preference. The current tool's service tier may be fixed.

## Measurement

Compare 20–30 representative completed tasks against a comparable baseline, grouped by complexity/risk. Record completion and acceptance rates, regressions/reopens, wall time, parent/worker/reviewer usage, corrective dispatches and actual charge/credits when available. A cheap failed task is not a saving.

Total cost = supervisor + discovery + implementation + verification/review + corrections + applicable tool/service charges. Keep cached and uncached tokens and service tiers distinct. Do not sum tree-level totals again with included child totals. If cache-write or other billing components are absent, report a partial estimate, not exact cost. If per-task usage is unavailable, say unknown; do not attribute shared account usage changes to this task when other chats are active.

For a purely illustrative Standard short-context comparison with equal token mix, normalize Astra cost to 1: Sol is 0.2 and Luna 0.01 at the dated rates. If Astra supervision costs 0.15 of an all-Astra baseline and the same work volume moves to Sol, the example totals 0.35, or 65% lower. This is arithmetic under assumptions, **not an observed saving**. More worker tokens, failures, cache differences, or expensive reviews can erase the advantage. A direct Sol session may beat an Astra-supervised workflow on ordinary small tasks.

## Enforcement boundary

Dispatch/retry limits in SKILL.md are behavioral instructions. They neither enforce an exact token limit within a dispatch nor stop billing automatically. Use a verified external request/usage enforcement mechanism only when the user separately requests hard caps; provider alerts alone may not be hard stops. No API service is introduced by this skill.

## Sources

- [Astra model and API rates](https://developers.openai.com/api/docs/models/gpt-6-astra)
- [Sol model and API rates](https://developers.openai.com/api/docs/models/gpt-6-sol)
- [Luna model and API rates](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [Codex pricing, credits and usage limits](https://learn.chatgpt.com/docs/pricing)
- [Codex subagent behavior and overhead](https://learn.chatgpt.com/docs/agent-configuration/subagents)
