# Project policy

Read only when `.codex/risk-router.toml` exists or the user requests persistent setup. A policy file alone does not activate the skill. Existing schema `version = 1` remains supported; preserve unknown keys and accept `quality-first` as an alias for `quality`.

```toml
version = 1
mode = "balanced" # efficient | balanced | quality
xhigh = "ask"     # auto | ask | disabled
stats = true
astra = "auto"    # implementation workers only; auto | ask | disabled; optional
```

- `xhigh` applies to Sol/Astra workers only. `auto` permits justified xHigh; `ask` needs task-scoped approval unless already granted; `disabled` forbids it. Never bypass a refusal with Max/Ultra. Leadership/review remain exactly High.
- `astra` controls implementation workers, not leadership/review. `auto` permits warranted Astra workers; `ask` needs task-scoped approval unless already granted; `disabled` caps workers at Sol. Standing Astra High leadership/review authorization needs no repeated approval.
- Missing `astra` means `auto`, except an existing `xhigh = "disabled"` without `astra` retains a **Sol High implementation ceiling**. Explicit `astra = "auto"` allows Astra workers up to High with xHigh disabled. Since v0.3.1, fixed leadership/review supersedes that old router ceiling only for those roles. Explain this distinction when relevant; preserve the file. Separate binding access/budget restrictions or a later explicit prohibition still block the role, never authorize a substitute.
- Without a policy, use task-local balanced, xHigh ask, Astra auto, stats off. Do not create settings or interrupt work for setup.
- If a known setting is malformed or unsupported, report it and resolve the affected route; do not silently treat an invalid restriction as permission. Unrelated unknown keys stay untouched.

Persist settings only when requested or already authorized. Reuse user preferences; preserve other content. Only as part of authorized setup, add this opt-in to applicable `AGENTS.md` if absent:

```text
For coding tasks in this repository, use $codex-risk-router and follow .codex/risk-router.toml.
```

These are router policy fields, not native model configuration. Do not rewrite global client settings. Updating the skill does not automatically update separate installed copies, project policies or logs.
