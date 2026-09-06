# Project policy

Read this file only when `.codex/risk-router.toml` exists or the user requests persistent router setup.

## Recommended v2 policy

```toml
version = 2
mode = "balanced"          # efficient | balanced | quality
leadership = "adaptive"    # adaptive | astra
review = "proportional"    # proportional | astra
xhigh = "ask"              # auto | ask | disabled
astra = "auto"             # implementation worker: auto | ask | disabled
stats = true
max_work_units = 1         # 1-3; still bounded by the current user authorization
```

Meanings:

- `leadership = "adaptive"`: keep ordinary routing in the current thread. Use Astra High as the single task owner for explicit audits, project-wide architecture, unresolved C8+ cross-system diagnosis or R8+ planning; do not place it in front of a duplicate worker for the same analysis.
- `leadership = "astra"`: require Astra High coordination for every routed task. This is an intentionally expensive opt-in.
- `review = "proportional"`: no reviewer for R0–3 with decisive checks, Sol High for R4–6 and Astra High for R7–10.
- `review = "astra"`: upgrade every otherwise-required independent review to Astra High. It does not create a review when none is required.
- `astra`: controls implementation workers only. `ask` requires task-scoped approval; `disabled` caps implementation at Sol High.
- `xhigh`: permits or restricts xHigh for Sol/Astra implementation workers. It never changes leadership or review effort.
- `max_work_units`: hard upper bound for the current request. It never grants implementation authority by itself and never permits silently continuing to the next roadmap phase.

## Existing v1 policy

Version 1 remains valid:

```toml
version = 1
mode = "balanced"
xhigh = "ask"
stats = true
astra = "auto"
```

Interpret missing v2 fields as:

```toml
leadership = "adaptive"
review = "proportional"
max_work_units = 1
```

Do not preserve the v0.3 fixed-Astra behavior merely because the policy predates v0.4. Fixed Astra leadership now requires the explicit v2 setting `leadership = "astra"`.

For backward compatibility, missing `astra` normally means `auto`. A v1 policy with `xhigh = "disabled"` and no `astra` retains the old Sol High implementation ceiling. This exception affects workers only.

Unknown keys remain untouched. Invalid known settings are reported and do not become permission.

## Setup

Persist settings only when requested or already authorized. Add this line to the applicable `AGENTS.md` only as part of that setup:

```text
For coding tasks in this repository, use $codex-risk-router and follow .codex/risk-router.toml.
```

The policy activates nothing by itself. It does not modify global client settings, grant external-write authority or prove model availability. Updating the skill does not automatically update installed copies or project policies.
