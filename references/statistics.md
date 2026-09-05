# Optional task statistics

Read only when `stats = true`. Only the parent appends one compact JSON object per bounded task to `.codex/risk-router-log.jsonl` after acceptance or a final block/failure. Preserve existing entries and schema compatibility. Do not log code, prompts, diffs, secrets or user data. Use a generic task label. Do not read accumulated history merely to append a result.

Example (one JSONL line):

```json
{"schema_version":1,"recorded_at":null,"router_version":"0.3.3","task":"bounded-fix","task_class":"code-fix","coordinator_model":"gpt-6-astra","coordinator_reasoning":"high","coordinator_actual_model":null,"coordinator_actual_reasoning":null,"coordinator_runtime_status":"accepted_unverified","complexity":9,"risk":6,"execution_mode":"delegated","requested_model":"gpt-6-astra","requested_reasoning":"high","current_model":null,"current_reasoning":null,"runtime_status":"accepted_unverified","fallback":null,"attempt_count":1,"retry_count":0,"escalations":[],"review_model":"gpt-6-astra","review_reasoning":"high","review_actual_model":null,"review_actual_reasoning":null,"review_runtime_status":"accepted_unverified","first_pass_success":true,"blocking_review_findings":0,"validation_failures":0,"validation":"pass","outcome":"pass"}
```

The example is illustrative, not an execution record. New records use `schema_version = 1` and `recorded_at` as an observed UTC ISO-8601 timestamp, or null if unavailable. Retain legacy entries without these fields; no rewrite/migration is required. Additional optional fields:

- `task_class`: generic category such as `code-fix`, `feature`, `docs`, `analysis` or `other`; no project/file names.
- `first_pass_success`: true only when the initial implementation passes acceptance including required review without a corrective attempt or blocking finding; false when observed otherwise, null if unknown/not applicable.
- `blocking_review_findings` and `validation_failures`: counts observed across the bounded task, including resolved findings/failures; count a carried-forward finding once, and use null if not reliably tracked. These counts may be nonzero for an eventual pass.
- `workflow_usage`: optional aggregate token counts with scope/unit/source, only if reliable for all contributing roles/attempts. Keep partial measurements labeled partial, never present them as totals.
- `elapsed_seconds`: observed whole-task wall time, not the sum of concurrent agent durations; absent/null if unavailable.

Do not add tool calls solely to collect optional counters. Use existing evidence; unknown is not zero.

Keep `execution_mode` separate from runtime status. Actual model/effort fields stay null unless exposed; accepted requests are not confirmation. Record coordinator, worker and reviewer independently. For `direct`, requested worker fields are null and worker status is `direct`. For `current`, record selected route and confirmed current metadata. When no reviewer ran, review fields are null; a required unavailable review blocks acceptance, not an implicit pass.

`attempt_count` includes the initial implementation and corrections/model switches; `retry_count` excludes the initial attempt. Pre-execution provider failures do not count as implementation attempts. `pass` requires completed acceptance criteria and required review; use `blocked` or `fail` otherwise.

Usage and elapsed-time fields are optional; leave them absent/null when not reliably exposed. Include all contributing roles and attempts in workflow totals; do not double-count cumulative session usage. No invented prices, savings or quality percentages. A logging failure should be disclosed but does not invalidate otherwise verified task acceptance; do not rerun implementation to repair telemetry.
