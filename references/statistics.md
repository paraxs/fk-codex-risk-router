# Optional task statistics

Read only when `stats = true`. The parent writes one compact JSON object after the current work unit stops. Do not read old entries merely to append a new one. Workers and reviewers never write statistics.

```json
{"schema_version":2,"recorded_at":null,"router_version":"0.4.0","task_class":"code-fix","complexity":6,"risk":4,"mode":"balanced","work_units_authorized":1,"work_units_completed":1,"execution_mode":"delegated","leadership_policy":"adaptive","coordinator_model":null,"coordinator_reasoning":null,"coordinator_runtime_status":"direct","requested_worker_model":"gpt-5.6-terra","requested_worker_reasoning":"high","worker_runtime_status":"accepted_unverified","implementation_attempts":1,"workers_started":1,"review_required":true,"requested_review_model":"gpt-5.6-sol","requested_review_reasoning":"high","review_runtime_status":"accepted_unverified","reviewers_started":1,"blocking_review_findings":0,"validation_failures":0,"validation":"pass","stop_reason":"work_unit_complete","outcome":"pass"}
```

Rules:

- `recorded_at` is an observed UTC ISO-8601 timestamp or null.
- Use generic task classes such as `code-fix`, `feature`, `docs`, `analysis` or `other`; record no project names, file names, prompts, code, secrets or user data.
- Keep actual model/effort fields absent or null unless the host exposes them. Accepted selection is not confirmation.
- `implementation_attempts` includes the initial implementation and one possible correction/model switch. It cannot exceed 2 for the default work unit.
- `workers_started` cannot exceed 1 and `reviewers_started` cannot exceed 1 under the default budget.
- `pass` requires completed acceptance checks and any required review.
- A missing required check or review produces `blocked`, not an assumed pass.
- A telemetry write failure does not justify rerunning implementation.

Optional `workflow_usage` and `elapsed_seconds` may be recorded only when complete and reliably exposed. Label partial usage as partial; never present it as a total. Do not add calls solely to collect optional counters.

Retain legacy schema-v1 records without migration. Compare cost only across similar accepted work units using total workflow usage, elapsed time, retry rate and blocking review findings. Do not tune routing from worker tokens alone.
