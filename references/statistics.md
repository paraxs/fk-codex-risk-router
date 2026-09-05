# Optional task statistics

Read only when `stats = true`. Only the parent appends one compact JSON object per bounded task to `.codex/risk-router-log.jsonl` after acceptance or a final block/failure. Preserve existing entries and schema compatibility. Do not log code, prompts, diffs, secrets or user data. Use a generic task label. Do not read accumulated history merely to append a result.

Example (one JSONL line):

```json
{"router_version":"0.3.2","task":"bounded-fix","coordinator_model":"gpt-6-astra","coordinator_reasoning":"high","coordinator_actual_model":null,"coordinator_actual_reasoning":null,"coordinator_runtime_status":"accepted_unverified","complexity":9,"risk":6,"execution_mode":"delegated","requested_model":"gpt-6-astra","requested_reasoning":"high","current_model":null,"current_reasoning":null,"runtime_status":"accepted_unverified","fallback":null,"attempt_count":1,"retry_count":0,"escalations":[],"review_model":"gpt-6-astra","review_reasoning":"high","review_actual_model":null,"review_actual_reasoning":null,"review_runtime_status":"accepted_unverified","validation":"pass","outcome":"pass"}
```

Keep `execution_mode` separate from runtime status. Actual model/effort fields stay null unless exposed; accepted requests are not confirmation. Record coordinator, worker and reviewer independently. For `direct`, requested worker fields are null and worker status is `direct`. For `current`, record selected route and confirmed current metadata. When no reviewer ran, review fields are null; a required unavailable review blocks acceptance, not an implicit pass.

`attempt_count` includes the initial implementation and corrections/model switches; `retry_count` excludes the initial attempt. Pre-execution provider failures do not count as implementation attempts. `pass` requires completed acceptance criteria and required review; use `blocked` or `fail` otherwise.

Usage and elapsed-time fields are optional; leave them absent/null when not reliably exposed. Include all contributing roles and attempts in workflow totals; do not double-count cumulative session usage. No invented prices, savings or quality percentages. A logging failure should be disclosed but does not invalidate otherwise verified task acceptance; do not rerun implementation to repair telemetry.
