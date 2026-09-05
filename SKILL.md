---
name: codex-risk-router
description: Require GPT-6 Astra High for orchestration, project leadership, audits and review; route implementation workers across Luna, Terra, Sol and Astra by complexity, risk and workflow cost. Use when the user invokes FK Router or $codex-risk-router, or applicable AGENTS.md requires it. Preserve explicit-only activation, project policy, bounded retries and independent review.
---

# FK Router — Codex Risk Router

Router version: `0.3.1` · Model documentation checked: `2026-09-05`

## Goal and boundaries

Choose the least costly route likely to meet the task's acceptance criteria, including context transfer, retries and review. Do not optimize token count at the expense of correctness. Model roles and supported identifiers are documented; the thresholds below are project heuristics, not benchmark-proven optima.

Preserve the existing task, architecture and working behavior. For single-HTML projects, preserve single-HTML/local-use requirements. Add no orchestration service, custom model-pinned agent TOMLs, dashboard, database or nested agent hierarchy.

- Complexity selects implementation worker capability; risk selects safeguards and whether independent review is required.
- High risk alone does not require an Astra implementation worker or xHigh. Leadership and review have the fixed role requirement below.
- Preserve the existing Luna High convention; Luna only receives explicit, bounded, testable tasks.
- Choose reasoning separately from model. No automatic `max` or `ultra`.
- A skill cannot change its own running model by instruction. Use only exposed, permitted runtime controls; never claim a switch without evidence.
- Explicit user choices, budget limits and tool restrictions remain binding. Worker ceilings are separate from the fixed leadership/review requirement. Existing authorization remains valid; routing grants no new action permissions.

### Fixed leadership and review roles

Always assign **orchestrator/router, project lead, auditor and reviewer/checker** to **`gpt-6-astra` with `reasoning_effort = "high"`**. This is the user's standing role policy, independent of task complexity, risk and working mode. High means exactly High, not Medium, xHigh, Max or Ultra.

Use one Astra High coordinator for task classification, scope, worker selection, escalation and final acceptance. These role names do not require four agents. An independent reviewer must use an Astra High thread separate from the implementation thread; the coordinator may also review a worker's work if it did not implement the change and has an independent context. A coordinator that implemented a change cannot count its own review as independent.

Establish the required coordinator model/effort using supported native controls before making routing or project-lead decisions. If the current session differs, use a supported model handoff/selection; do not merely label it Astra or create a nested coordinator hierarchy. If Astra High is unavailable, forbidden by a binding restriction or mismatched at runtime, report the affected leadership/review role as BLOCKED and the needed model setting/access. **No substitute model or different effort for these roles.** An accepted override without effective metadata remains `accepted_unverified`, never confirmed.

Implementation workers may use the routing table and run deterministic tests, collect evidence and report results. They do not become the auditor, project lead or final approver. This fixed-role rule does not add independent review to eligible micro-tasks.

## 1. Activation and policy

Activate only when explicitly requested by name or required by applicable `AGENTS.md`. A policy file alone is not an activation trigger. Maintaining this skill is not itself an instruction to route unrelated work.

Read applicable `AGENTS.md` and `.codex/risk-router.toml` once per task/session unless they change. Preserve existing files, unknown keys and opt-in policy. Accept `quality-first` as an alias for existing mode `quality`.

Existing schema `version = 1` remains supported. Optional `astra` extends it; a version migration is unnecessary:

```toml
version = 1
mode = "balanced" # efficient | balanced | quality
xhigh = "ask"      # auto | ask | disabled
stats = true
astra = "auto"     # implementation workers: auto | ask | disabled; optional
```

Interpretation:
- `xhigh`: applies to Sol and Astra implementation workers; leadership/review stay exactly High. `auto` permits a justified xHigh route; `ask` needs task-scoped approval unless already granted; `disabled` forbids xHigh. Never route around a refusal with Max/Ultra.
- `astra`: controls implementation workers only. `auto` permits Astra when warranted; `ask` needs task-scoped approval unless already granted; `disabled` caps implementation model choice at Sol. Astra High leadership/review is already authorized by the standing role policy; do not ask for that authorization again.
- Backward compatibility: missing `astra` means `auto`, EXCEPT an existing `xhigh = "disabled"` policy without `astra` retains a **Sol High maximum for implementation workers**. An explicit `astra = "auto"` permits Astra workers up to High even with xHigh disabled. From v0.3.1, the user-authorized fixed-role rule supersedes the old router ceiling for leadership/review only; state this distinction when relevant and preserve the file. A separate binding access/budget restriction or a later explicit user prohibition still blocks the role, rather than permitting a substitute.
- Missing policy: use task-local `balanced`, `xhigh = "ask"`, `astra = "auto"`, `stats = false`; do not interrupt ordinary work with setup questions or create project files just to run the router.
- Persist policy only when project setup/persistence is requested or already authorized. Reuse stated preferences. Add the following opt-in line to applicable `AGENTS.md` only as part of that setup, preserving other content and avoiding duplicates:

```text
For coding tasks in this repository, use $codex-risk-router and follow .codex/risk-router.toml.
```

These are router policy fields, not native Codex model configuration. Do not rewrite global client settings. A request to update this skill does not update separate copies on a user's PC automatically.

## 2. Classify a bounded task

Score factors 0–2 each; use the sum 0–10. Do not print all factors routinely.

| Complexity factor | 0 | 1 | 2 |
|---|---|---|---|
| Ambiguity | exact change/cause | some unknowns | cause/approach substantially unknown |
| Coupling | isolated | one subsystem/several files | multiple subsystems/layers |
| Causal depth | local/deterministic | non-trivial data flow | concurrency/distributed state/lifecycle |
| Architecture/novelty | known pattern | moderate choice | major tradeoff/new architecture |
| Context breadth | narrow | moderate | broad cross-system context |

Complexity floors: architectural refactor/unresolved cross-system design C >= 7; race condition/distributed-state diagnosis/severe cross-system uncertainty C >= 8. Mechanical volume alone does not increase C.

| Risk factor | 0 | 1 | 2 |
|---|---|---|---|
| Blast radius | isolated | feature/module | system-wide |
| Data/security | none | indirect/limited | data integrity/auth/secrets/security boundary |
| Reversibility | clean revert | multi-step rollback | migration/irreversible state |
| Side effects | local | shared/staging | production/billing/external write |
| Verification | strong deterministic checks | partial | weak observability/material uncertainty |

Risk floors: auth/permissions/secrets/security boundaries, persistent-data migration, destructive or production-infrastructure mutation R >= 8; unknown data-loss risk or irreversible external side effect R >= 9.

For calculations, geometry, quantities, technical rules and data persistence, validate substantive invariants against known examples or authoritative requirements. Neither a low C nor a strong model replaces that check. Do not change domain rules based on model confidence alone.

## 3. Worker and reasoning

Use only model/effort combinations exposed by the current runtime. Exact identifiers:

| Model | Identifier | Routing role |
|---|---|---|
| Luna | `gpt-5.6-luna` | clear, repeatable, tightly specified work |
| Terra | `gpt-5.6-terra` | everyday implementation and localized debugging |
| Sol | `gpt-5.6-sol` | complex code changes and ambiguous diagnosis |
| Astra | `gpt-6-astra` | hardest cross-system diagnosis, architecture and sustained multi-step work |

Initial implementation worker selection, before worker ceilings and the execution gate; never use this table for leadership, audits or review:

| Mode | Luna | Terra | Sol | Astra |
|---|---|---|---|---|
| efficient | C 0–4 | C 5–7 | C 8–9 | C 10 |
| balanced | C 0–3 | C 4–6 | C 7–8 | C 9–10 |
| quality | C 0–2 | C 3–5 | C 6–7 | C 8–10 |

Initial implementation-worker reasoning (leadership/review always Astra High):
- Luna: High, preserving established policy.
- Terra: Medium for clear implementation; High for C >= 6 or unresolved non-trivial state/data flow.
- Sol: Medium for bounded work with an established approach; High for C >= 8 or unresolved diagnosis/design.
- Astra: High for C >= 9 or unresolved cross-system diagnosis; Medium for a bounded C 8 analysis with clear inputs and acceptance criteria.
- xHigh: only when a specific unresolved reasoning problem warrants it, lower effort is unlikely to suffice or has failed, and policy permits it. Never selected merely by risk score or model prestige.

Use Astra directly when initial complexity warrants it; do not first spend tokens on a predictable ladder of failures. If Astra resolves the cause/design into a clear implementation, reclassify that implementation and route it separately only when the handoff will pay off. Do not keep Astra for follow-up mechanical edits by inertia.

## 4. Execute with proportionate overhead

Choose one execution mode:
1. `direct`: a localized micro-task with C <= 2, R <= 2, deterministic validation and no independent review need; delegation adds obvious overhead. The Astra High coordinator may perform this micro-task itself, subject to the fixed-role runtime truth rule; do not claim cost savings without measurements.
2. `current`: the exposed current worker model AND effort match the selected allowed implementation route; continue that worker session under Astra High coordination. No duplicate worker for the same work. Required independent review still applies.
3. `delegated`: native delegation is available and permitted; request the routed model/effort explicitly. Do not keep substantial work in a more expensive current model simply because it is capable.
4. `fallback_current`: implementation model control/delegation is absent or blocked and the current session is permitted and capable of attempting the implementation. This is a worker fallback only; Astra High coordination remains required. State the limitation, run proportionate validation and never claim the recommended model ran. Do not bypass an explicit model/cost ceiling. If the minimum necessary capability or review cannot be provided, report `BLOCKED` for that phase.

Treat live tool metadata as authoritative; a stale model cache or public model page does not prove account access. Prefer advertised native controls over custom launchers. Do not spawn agents only to narrate routing, repeat completed analysis or circumvent a delegation restriction.

When an implementation route is unavailable, try an untried compatible permitted worker route once, then use a safe available worker fallback or report the blocker. An unavailable/disabled Astra implementation worker may fall back to Sol High, or Sol xHigh only when justified and permitted. These fallbacks never apply to the coordinator, project lead, auditor or reviewer. Never retry a model-not-found combination or loop through aliases. Authentication/network/tool failures require fixing their cause, not a stronger reasoning model.

## 5. Bounded handoff and context budget

Use native worker or read-only review roles when exposed. Set `model` and `reasoning_effort` explicitly, and normally `fork_turns = "none"`. Use a small positive turn count only when necessary; never default to full-history forks, which may disable overrides.

Give a worker only:
- TASK and observable GOAL;
- relevant files/functions and source facts;
- boundaries and already-authorized scope;
- acceptance criteria and targeted validation;
- prior failed hypothesis/error when escalating;
- STOP: return BLOCKED before unauthorized scope expansion or action.

Workers do not invoke this router recursively or append router statistics. Use at most one implementation worker per coupled change. Parallel workers are useful only for independently owned tasks whose gains justify duplicated context; do not split coupled single-HTML edits across simultaneous writers.

Search narrowly (`rg`), read affected functions and callers, batch independent reads, reuse validated findings. Transfer file references and concise evidence rather than whole files/chat history. Keep stable instructions stable. Do not repeatedly research model docs per task: consult [model-notes.md](references/model-notes.md) only for availability, future model updates or a source question.

## 6. Validate and review

Define acceptance criteria before editing. Run relevant targeted tests, build/type checks or smoke tests; add a regression test when it covers the actual bug/risk. Do not add implementation-mirroring tests for harmless edits. Stop testing when acceptance criteria and required gates pass; expand only for a concrete residual risk.

PDF layout changes require visual inspection of representative exports. Storage/import/migration changes require disposable-data round trips and preservation/error-path checks. State unavailable checks and their practical consequence.

Independent review requirement:

| Risk | Review requirement |
|---|---|
| R 0–2 | no separate reviewer when deterministic checks pass; otherwise independent Astra High |
| R 3–10 | independent Astra High |

Every model-based audit or review uses **Astra High**, including explicitly requested audits of low-risk work. Risk and complexity affect review scope and practical checks, never the reviewer's model or effort. Terra/Sol reviewer routes and reviewer xHigh/Medium substitutions are not permitted. If Astra High cannot perform a required review, acceptance remains BLOCKED; a Sol review is not a compliant fallback.

Give the independent Astra High reviewer intended behavior, relevant diff, constraints and test results. Inspect correctness, regressions and missing meaningful checks; do not repeat the implementation. One substantive review plus focused verification of resulting fixes is normally enough. No duplicate review just to create separate auditor and checker titles.

If an independent review is required but unavailable, report it as missing, never substitute self-review as independent. Complete safe preparation; mark acceptance blocked where that gate remains required. An unresolved material finding prevents `pass`.

## 7. Retry, escalation and stopping

Allow at most one same-route corrective retry, only for an understood bounded defect. Across a bounded objective, permit at most **three implementation attempts total**, including the initial attempt, corrections and attempts after switching models. A model switch or renaming the task does not reset the budget. Provider failures before execution do not count as implementation attempts; availability retries remain bounded by section 4.

On unclear cause, repeat failure or increased complexity, reclassify and select the next justified route directly. Typical implementation capability progression: Luna -> Terra -> Sol -> Astra. The Astra High coordinator decides escalation and remains at High. Raising implementation-worker effort within Sol/Astra is an alternative when deeper reasoning on the same well-defined problem is likely to help; these are not compulsory consecutive steps.

Do not alternate models on the same unresolved error. Do not escalate for missing credentials, required user data or permissions. At the attempt limit or policy ceiling, stop speculative edits; report evidence, remaining blocker and the concrete next step. Continue unrelated authorized safe work where useful. New attempts require a materially new input/approach and authorization rather than an automatic retry loop.

## 8. Runtime truth and lightweight statistics

Never present a requested model as confirmed merely because spawn accepted it. Use:
- `direct`: no worker/model switch, micro-task;
- `confirmed`: runtime model AND effort match the selected route;
- `accepted_unverified`: override accepted but effective model/effort not exposed;
- `mismatch`: exposed runtime differs;
- `unavailable`: selected route cannot run.

`execution_mode` is `direct`, `current`, `delegated` or `fallback_current`; it is separate from runtime status. For a mismatch, recheck capability and policy before accepting results. Record runtime model/effort only when exposed; otherwise null. Apply the same truth rule separately to the Astra High coordinator and reviewers. Record their requested model/effort, actual model/effort when exposed and runtime status; worker metadata does not prove the coordinator identity.

If `stats = true`, only the parent appends one compact JSON object per bounded task to `.codex/risk-router-log.jsonl` after validation/review or a final block. Preserve existing entries/schema compatibility. Do not log code, prompts, diffs, secrets or user data. Example (one JSONL line):

```json
{"router_version":"0.3.1","task":"bounded-fix","coordinator_model":"gpt-6-astra","coordinator_reasoning":"high","coordinator_actual_model":null,"coordinator_actual_reasoning":null,"coordinator_runtime_status":"accepted_unverified","complexity":9,"risk":6,"execution_mode":"delegated","requested_model":"gpt-6-astra","requested_reasoning":"high","current_model":null,"current_reasoning":null,"runtime_status":"accepted_unverified","fallback":null,"attempt_count":1,"retry_count":0,"escalations":[],"review_model":"gpt-6-astra","review_reasoning":"high","review_runtime_status":"accepted_unverified","validation":"pass","outcome":"pass"}
```

For `direct`, requested worker fields are null. For `current`, record the selected route and confirmed current metadata. Outcome `pass` requires completed acceptance criteria/review; use `blocked` or `fail` otherwise. Keep usage fields optional and null/absent if not exposed. Never invent token savings, prices or percentage quality scores. Evaluate threshold changes only after roughly 20–30 real comparable tasks using failures, total usage and review findings, not model names alone.

## 9. Report

Use the user's language. Report changes, validation, remaining uncertainty and one compact routing line with requested model/effort, actual runtime status, Astra High coordination, review and escalation when applicable. Show C/R if useful; do not dump factor tables or internal deliberation. Report limitations plainly, including when the environment could only recommend a model rather than execute it.
