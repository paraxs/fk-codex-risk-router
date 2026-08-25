---
name: fk-codex-risk-router
description: Route Codex coding work across GPT-5.6 Luna, Terra, and Sol using separate complexity and risk scores, a small per-project cost/quality policy, bounded subagent tasks, risk- and complexity-based independent review, limited retries, escalation, and lightweight routing statistics. Use when explicitly invoked as `$fk-codex-risk-router` or when applicable `AGENTS.md` project guidance requires it; do not invoke implicitly for ordinary coding work.
---

# Codex Risk Router

Router version: `0.2.1`

## Goal

Use the cheapest sufficiently capable GPT-5.6 model for each bounded coding task without sacrificing reliability or spending more on orchestration than the work justifies.

Workflow:

`activation -> project policy -> classify -> direct or delegate -> execute -> validate -> review -> escalate if needed -> report`

Do not add an orchestration service, MCP server, database, dashboard, Agents SDK layer, or nested agent hierarchy.

## Invariants

- Score **complexity** and **risk** separately.
- Complexity selects the worker; risk selects safeguards and review strength.
- High risk alone does not imply xHigh reasoning.
- Luna always uses High reasoning; do not downgrade it to Medium or Low.
- Luna receives only bounded, explicit, testable work.
- Direct execution is allowed only for eligible micro-tasks under the delegation gate; otherwise follow the worker routing table.
- Prefer native `spawn_agent` with explicit `model` and `reasoning_effort` overrides over model-pinned custom agent TOMLs.
- Default child context to `fork_turns = "none"`.
- A worker may get at most one same-tier corrective retry.
- Scope expansion causes `BLOCKED` or escalation, never silent expansion.
- Do not claim a requested model was actually used unless runtime metadata confirms it.
- `max` reasoning is out of scope for v0.2.1.

## 1. Activation and delegation gate

This skill is explicit-only. Activate it only when either:
- the user explicitly invokes `$fk-codex-risk-router`; or
- applicable project instructions in `AGENTS.md` require `$fk-codex-risk-router`.

Otherwise, do not apply this router to ordinary coding work.

The presence of `.codex/risk-router.toml` is project policy, not an activation trigger. Do not assume that the file can activate this skill by itself.

Once active, classify the task before deciding whether to spawn.

Direct execution is a micro-task shortcut, not an alternative routing tier.

Use direct execution only when ALL conditions are true:
- complexity <= 2
- risk <= 2
- no independent review is required
- the change is narrowly localized
- validation is deterministic
- delegation would add obvious overhead for a trivial change

For complexity >= 3, follow the worker routing table.

Do not bypass Luna, Terra, or Sol merely because the current agent is already capable of doing the work.

If the current parent model or reasoning effort is unknown, do not assume that direct execution is cheaper than delegation.

For tasks that do not qualify for direct execution, delegate according to the worker routing table. Do not keep work in the current agent merely because it is already running, stronger than the routed worker, or appears capable of completing the task itself.

For direct execution, record the worker as `direct`, the runtime status as `direct`, and continue with the same validation and reporting discipline. Do not spawn a token worker merely to satisfy the routing table.

## 2. Project policy

Before the first skill-managed task, read `.codex/risk-router.toml`.

If absent, ask exactly:

1. `Working mode? A = Efficient, B = Balanced, C = Quality First`
2. `Use Sol xHigh for very difficult tasks? A = automatically, B = ask first, C = disabled / Sol High is the maximum`

Then create:

```toml
version = 1
mode = "balanced" # efficient | balanced | quality
xhigh = "ask"      # auto | ask | disabled
stats = true
```

Map answers directly.

On first project opt-in, also add this single instruction to the applicable project `AGENTS.md`, preserving existing content and avoiding duplicates:

```text
For coding tasks in this repository, use $fk-codex-risk-router and follow .codex/risk-router.toml.
```

Before asking the two setup questions, state that the answers will persist the project opt-in through `.codex/risk-router.toml` and this `AGENTS.md` instruction. If the user requests one-off routing instead, use `balanced`, `xhigh = "ask"`, and `stats = false` for that task without creating or modifying either file.

Rules:
- `auto`: use xHigh when routing selects it.
- `ask`: ask once for that task before xHigh.
- `disabled`: Sol High is the ceiling.
- Do not ask more setup questions unless a material project constraint cannot fit this policy.

## 3. Complexity score

Score each factor 0-2.

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Ambiguity | exact change/cause | some unknowns | root cause/approach substantially unknown |
| Coupling | isolated | one subsystem/several files | multiple subsystems/services/layers |
| Causal depth | local/deterministic | non-trivial state/data flow | concurrency, distributed state, race/lifecycle behavior |
| Architecture/novelty | established pattern | moderate design choice | new architecture/major tradeoff/unfamiliar territory |
| Context breadth | narrow | moderate repo context | broad repo/cross-system understanding |

`COMPLEXITY = sum` (0-10)

Floors:
- architectural refactor or unresolved cross-system design: `>= 7`
- race condition, distributed-state diagnosis, severe multi-system debugging uncertainty: `>= 8`

Mechanical volume alone does not raise complexity.

## 4. Risk score

Score each factor 0-2.

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Blast radius | isolated | module/feature regression | system-wide/many users or components |
| Data/security | none | indirect/limited | auth, permissions, secrets, security boundary, data integrity |
| Reversibility | clean revert | multi-step rollback | migration, external/irreversible state |
| Side effects | local | shared/staging | production, live data, deployment, billing, external write |
| Verification | strong deterministic checks | partial | weak observability/material residual uncertainty |

`RISK = sum` (0-10)

Floors:
- auth, permissions, secrets, security boundary: `>= 8`
- persistent-data/database migration: `>= 8`
- destructive or production-infrastructure mutation: `>= 8`
- unknown data-loss risk or irreversible external side effect: `>= 9`

Risk changes validation, review, and approval requirements. Do not upgrade worker reasoning solely because risk is high.

## 5. Worker routing

Use explicit GPT-5.6 slugs.

| Mode | Luna High | Terra High | Sol High | Sol xHigh* |
|---|---:|---:|---:|---:|
| efficient | C 0-4 | C 5-7 | C 8-9 | C 10 |
| balanced | C 0-3 | C 4-6 | C 7-8 | C 9-10 |
| quality | C 0-2 | C 3-5 | C 6-7 | C 8-10 |

Models:
- Luna: `gpt-5.6-luna`
- Terra: `gpt-5.6-terra`
- Sol: `gpt-5.6-sol`

`*` xHigh is subject to project policy. If unavailable or disallowed, use Sol High and record the ceiling/fallback.

If the native spawn surface rejects a requested model/effort, use the next stronger available compatible route when possible. Do not loop on unavailable combinations.

## 6. Bounded delegation

Use a native implementation/worker role for code changes and a read-only/explorer role for discovery or review when available.

Default:
- set `model` explicitly
- set `reasoning_effort` explicitly
- set `fork_turns = "none"`
- restate only necessary context in the child message
- use a small positive turn count only when restating required context would be materially worse
- never default to `fork_turns = "all"`

Every implementation handoff should contain:

```text
TASK:
<one bounded task>

GOAL:
<observable outcome>

SCOPE:
<relevant files/components>

DO NOT CHANGE:
<explicit boundaries>

ACCEPTANCE CRITERIA:
<concrete pass conditions>

VALIDATION:
<tests/checks>

STOP:
If material scope expansion, destructive/external action, new security-sensitive work,
migration work not already authorized, or changes outside the boundary are required,
return BLOCKED with the reason and required scope.
```

Never give Luna an open instruction such as `improve the user system`.

Large but mechanical work should be decomposed instead of escalated merely because it is large.

## 7. Validation

After implementation run the most relevant non-destructive checks available:
- targeted tests
- type/lint checks when applicable
- affected build checks
- minimal smoke test if full validation is too expensive

If validation cannot run, state why and treat verification confidence as weaker.

## 8. Independent review

A worker does not automatically approve its own non-trivial work.

| Risk | Review |
|---|---|
| 0-2 | worker validation is enough if deterministic and tests pass; otherwise Terra High |
| 3-5 | independent Terra High |
| 6-8 | independent Sol High |
| 9-10 | independent Sol xHigh if policy permits; otherwise Sol High + strongest practical verification |

When independent review is required, also apply this complexity floor:

| Complexity | Minimum reviewer |
|---|---|
| 0-5 | Terra High |
| 6-10 | Sol High |

Use the stronger of the risk-based review tier and the complexity floor. This floor does not force independent review for `R 0-2` when deterministic checks pass.

Reviewers:
- use a separate thread/subagent
- default to `fork_turns = "none"`
- receive intended behavior, changed scope/diff, constraints, and validation results
- look for correctness, regressions, security issues, and missing tests
- do not re-implement unless explicitly delegated after review

Normal approval boundaries still apply to destructive actions, production changes, deployments, purchases, and external writes.

## 9. Retry and escalation

One same-tier corrective retry is allowed only when the failure is understood, bounded, and does not materially change risk or complexity.

Escalate when:
- that retry fails
- root cause remains unclear
- scope materially expands
- a stop boundary is crossed
- complexity crosses the next routing threshold
- a corrected result is rejected again

Escalation:

`Luna -> Terra -> Sol High -> Sol xHigh (policy permitting)`

If Sol High is the project ceiling and cannot resolve the task reliably, stop and report the limitation. Never silently override project policy.

## 10. Runtime truth

Treat the current native spawn surface as the capability source.

For every skill-managed task record one runtime status:
- `direct`: no worker was spawned; the current session executed the task
- `confirmed`: exposed runtime model/effort matches the request
- `accepted_unverified`: spawn accepted the override but effective runtime metadata is not exposed
- `mismatch`: exposed runtime metadata differs
- `unavailable`: requested route could not spawn

Do not convert `accepted_unverified` into a claim that Luna/Terra/Sol definitely ran.

## 11. Lightweight statistics

If `stats = true`, append one compact JSON object per skill-managed task to:

`.codex/risk-router-log.jsonl`

Do not log source code, prompts, diffs, secrets, or user data.

Only the parent/router appends statistics, after validation and any required review are complete. Subagents never write to `.codex/risk-router-log.jsonl` and never determine the final `outcome` themselves.

Every statistics entry must include the current `router_version`. This is the behavioral router version and is independent of the project policy schema field `version = 1`.

For delegated execution, use fields like:

```json
{
  "router_version": "0.2.1",
  "task": "short non-sensitive label",
  "complexity": 5,
  "risk": 3,
  "execution_mode": "delegated",
  "requested_model": "gpt-5.6-terra",
  "requested_reasoning": "high",
  "current_model": null,
  "current_reasoning": null,
  "runtime_status": "accepted_unverified",
  "fallback": null,
  "retry_count": 0,
  "escalations": [],
  "review_model": "gpt-5.6-terra",
  "validation": "pass",
  "outcome": "pass"
}
```

For direct execution, keep requested worker fields null and record the current session only when the runtime exposes it reliably:

```json
{
  "router_version": "0.2.1",
  "task": "short non-sensitive label",
  "complexity": 1,
  "risk": 1,
  "execution_mode": "direct",
  "requested_model": null,
  "requested_reasoning": null,
  "current_model": null,
  "current_reasoning": null,
  "runtime_status": "direct",
  "fallback": null,
  "retry_count": 0,
  "escalations": [],
  "review_model": null,
  "validation": "pass",
  "outcome": "pass"
}
```

Record token/usage data only when the runtime exposes it reliably; never estimate it.

Do not tune routing thresholds until roughly 20-30 real routed tasks provide evidence.

## 12. Final report

Keep the user-facing report compact:

```text
Done.

Routing:
- Complexity: X/10
- Risk: Y/10
- Worker requested: <direct or model / effort>
- Runtime: <direct | confirmed | accepted_unverified | mismatch | unavailable>
- Fallback: <none or model / effort>
- Review: <model / effort or not required>
- Escalations: <none or short summary>

Changed:
- <files/components>

Validation:
- <checks/results>

Remaining uncertainty:
- <none or concrete caveat>
```

Scores and routing metadata may be shown. Do not expose private chain-of-thought.

## v0.2.1 boundary

Do not add custom model-pinned agent TOMLs, Agents SDK, MCP orchestration, external services, databases, dashboards, nested agent hierarchies, automatic `max` reasoning, or repeated retry loops unless measured results later justify them.
