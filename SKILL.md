---
name: codex-risk-router
description: Require GPT-6 Astra High for orchestration, project leadership, audits and review; route implementation workers across Luna, Terra, Sol and Astra by complexity, risk and workflow cost. Use when the user invokes FK Router or $codex-risk-router, or applicable AGENTS.md requires it. Preserve explicit-only activation, project policy, bounded retries and independent review.
---

# FK Router — Codex Risk Router

Router version: `0.3.2` · Model documentation checked: `2026-09-05`

## Goal and boundaries

Minimize total workflow cost, including discovery, context transfer, retries and review, subject to the task's acceptance criteria. Correctness comes before token reduction. Routing thresholds are heuristics, not benchmark-proven optima.

Preserve task scope, architecture and working behavior, including single-HTML/local-use requirements. Add no orchestration infrastructure, custom model-pinned agent TOMLs or nested agent hierarchy. User choices, budget limits and tool restrictions remain binding; routing grants no new action permissions.

**No over-engineering.** Keep solution complexity, abstractions, dependencies, agent count, documentation and verification effort proportionate to the actual task, risk and maintenance needs. Prefer the simplest complete, reliable solution; do not build for hypothetical future requirements. Add complexity only for a concrete current requirement or evidenced risk. Balance quality, cost and elapsed time; neither maximum process nor minimum effort is the goal. Required safety and correctness checks remain mandatory.

Complexity selects worker capability; risk selects safeguards and independent review, not automatically a stronger worker or xHigh. Choose model and reasoning separately; Luna always High and only for bounded, testable work. No automatic Max/Ultra. Model switching requires exposed, permitted runtime controls, not an instruction claiming a switch.

### Fixed leadership and review roles

Use **`gpt-6-astra` with exactly `reasoning_effort = "high"`** for coordination, project leadership, audits and review in every mode. One coordinator handles classification, scope, selection, escalation and acceptance; role titles do not require extra agents.

Independent review needs a thread separate from implementation. The coordinator can review if it has an independent context and supplied only requirements/source facts, not implementation or a detailed solution. Otherwise use a separate Astra High reviewer; self-review is not independent.

Establish coordinator model/effort through native controls before routing. If the session differs, use supported handoff/selection. Unavailable, forbidden or mismatched Astra High blocks the affected leadership/review role: report the required setting/access, with **no substitute model or effort**. Accepted overrides without effective metadata remain `accepted_unverified`.

Workers may implement, test and report evidence, not act as auditor or final approver. This role policy adds no review to eligible micro-tasks.

## 1. Activation and policy

Activate only when explicitly requested by name or required by applicable `AGENTS.md`. A policy file alone is not an activation trigger. Maintaining this skill is not itself an instruction to route unrelated work.

Read applicable `AGENTS.md` and `.codex/risk-router.toml` once, reusing already-loaded unchanged instructions. Without a policy, use task-local `balanced`, `xhigh = "ask"`, `astra = "auto"`, `stats = false`; create no project files and ask no setup questions.

Only if a policy exists or persistence is requested, read [project-policy.md](references/project-policy.md) for schema, legacy ceilings and authorized setup. Preserve unknown keys and existing authorization. Policy settings never grant extra action permissions or override binding user limits. Do not rewrite global client settings.

## 2. Scope discovery to the routing decision

Identify the requested outcome and the smallest observable acceptance check. Inspect only enough scope, dependencies and risk to select a capable route. The coordinator must not solve the implementation first and then pay a worker to repeat it.

When uncertainty could change the worker choice, use a focused search/read or diagnostic check. If diagnosis itself is substantial, give diagnosis and the authorized implementation to one suitably capable worker with a checkpoint before material scope expansion. Do not open an exploratory agent merely to prepare another agent's prompt.

Reuse a valid route for follow-up work within the same objective; reclassify only if evidence changes complexity, risk, scope or available capability. A new message does not by itself require a fresh investigation, handoff or attempt budget.

### Classify a bounded task

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
1. `direct`: localized micro-task, C <= 2, R <= 2, deterministic validation, no independent review need and obvious delegation overhead. The Astra High coordinator may implement it.
2. `current`: exposed current worker model AND effort match the allowed route; continue under Astra High coordination without a duplicate worker. Required review still applies.
3. `delegated`: permitted native delegation is available; request the selected model/effort. Do not retain substantial work in a more expensive model merely because it is capable.
4. `fallback_current`: worker controls/delegation are absent or blocked, but the current session is capable and permitted within model/cost ceilings. Disclose the fallback, not the recommended model as executed. Astra High coordination and required review still apply; block the affected phase if necessary capability or review is missing.

Treat live tool metadata as authoritative; a stale model cache or public model page does not prove account access. Prefer advertised native controls over custom launchers. Do not spawn agents only to narrate routing, repeat completed analysis or circumvent a delegation restriction.

For an unavailable worker, try one untried compatible permitted route, then safe worker fallback or BLOCKED. Unavailable/disabled Astra workers may fall back to Sol High, or justified/permitted Sol xHigh. Never substitute leadership/review. No model-not-found retries or alias loops; authentication/network/tool failures need their cause fixed, not stronger reasoning.

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

The task contract is stable: goal, scope/ownership, acceptance, authority and relevant evidence. Follow-ups to the same worker carry only changed facts, the failure evidence and the next bounded action. A replacement worker also needs that compact contract and the attempted approaches; do not send the full history or omit failure evidence to save tokens.

Search narrowly (`rg`), batch independent reads and return relevant excerpts, not repository dumps. Reuse unchanged instructions, findings and checks while their assumptions remain valid. Summarize successful tool output; retain exact relevant diagnostics and evidence locations for failures. Workers return the result, changed paths, checks/results and unresolved risks, not a work diary.

Load supporting references only at their stated trigger. Do not read historical statistics or model documentation during routine routing. Consult [model-notes.md](references/model-notes.md) only for availability, future model updates or a source question. These are context-efficiency rules, not permission to skip affected callers, risk evidence or required checks.

## 6. Validate and review

Define acceptance criteria before editing. Run relevant targeted tests, build/type checks or smoke tests; add a regression test when it covers the actual bug/risk. Do not add implementation-mirroring tests for harmless edits. Stop testing when acceptance criteria and required gates pass; expand only for a concrete residual risk.

PDF layout changes require visual inspection of representative exports. Storage/import/migration changes require disposable-data round trips and preservation/error-path checks. State unavailable checks and their practical consequence.

Independent review requirement:

| Risk | Review requirement |
|---|---|
| R 0–2 | no separate reviewer when deterministic checks pass; otherwise independent Astra High |
| R 3–10 | independent Astra High |

Explicit audits, including low-risk work, also require Astra High. Risk and complexity change review scope and checks, not the fixed model/effort. Missing required Astra High review blocks acceptance.

Give the independent Astra High reviewer intended behavior, relevant diff, constraints and test results. Inspect correctness, regressions and missing meaningful checks; do not repeat the implementation. One substantive review plus focused verification of resulting fixes is normally enough. No duplicate review just to create separate auditor and checker titles.

Verification evidence belongs to a specific revision, command and environment. Reuse it when unchanged; rerun affected checks after changes or when evidence is incomplete, stale or suspect. A reviewer independently inspects the diff and relevant source; it need not rerun every passing command. Expand into unchanged areas only to resolve a concrete dependency or risk. Separate blocking correctness/safety findings from optional improvements; optional polish does not trigger a repair loop or prevent acceptance.

Complete safe preparation when review is blocked; report the missing gate. An unresolved material finding prevents `pass`.

## 7. Retry, escalation and stopping

Allow at most one same-route corrective retry, only for an understood bounded defect. Across a bounded objective, permit at most **three implementation attempts total**, including the initial attempt, corrections and attempts after switching models. A model switch or renaming the task does not reset the budget. Provider failures before execution do not count as implementation attempts; availability retries remain bounded by section 4.

On unclear cause, repeat failure or increased complexity, reclassify and choose the next justified capability directly. Luna -> Terra -> Sol -> Astra is not a mandatory ladder. Raising Sol/Astra worker effort is an alternative when deeper reasoning on the same bounded problem will help; the coordinator remains High.

Do not alternate models on the same unresolved error. Do not escalate for missing credentials, required user data or permissions. At the attempt limit or policy ceiling, stop speculative edits; report evidence, remaining blocker and the concrete next step. Continue unrelated authorized safe work where useful. New attempts require a materially new input/approach and authorization rather than an automatic retry loop.

## 8. Runtime truth and lightweight statistics

Never present a requested model as confirmed merely because spawn accepted it. Use:
- `direct`: no worker/model switch, micro-task;
- `confirmed`: runtime model AND effort match the selected route;
- `accepted_unverified`: override accepted but effective model/effort not exposed;
- `mismatch`: exposed runtime differs;
- `unavailable`: selected route cannot run.

`execution_mode` is `direct`, `current`, `delegated` or `fallback_current`; it is separate from runtime status. For a mismatch, recheck capability and policy before accepting results. Record runtime model/effort only when exposed; otherwise null. Apply the same truth rule separately to the Astra High coordinator and reviewers. Record their requested model/effort, actual model/effort when exposed and runtime status; worker metadata does not prove the coordinator identity.

An explicit native model/effort request accepted without effective metadata can satisfy the role-selection gate as `accepted_unverified` when there is no contrary evidence and no binding requirement for confirmed identity. Disclose that limitation; do not block solely because metadata is absent or repeatedly probe an interface that does not expose it. This is not task acceptance: implementation, checks and required review must actually finish. Without either an accepted override or exposed matching identity, the required role is not established.

Only when `stats = true`, read [statistics.md](references/statistics.md) and let the parent append one compact task result; no worker logging or routine log-history reads. Without statistics, create no telemetry artifacts.

Outcome `pass` requires completed acceptance criteria and required review. Never invent token savings, prices or percentage quality scores. For an explicitly requested cost evaluation, compare total coordinator + worker + review + retry usage and elapsed time on comparable accepted tasks, including blocked/failed routes. Report unavailable measurements as unknown. Roughly 20–30 real comparable tasks can support initial threshold tuning, not a universal quality guarantee; never tune on cheap worker calls alone.

## 9. Report

Use the user's language. Report changes, validation, remaining uncertainty and one compact routing line with requested model/effort, actual runtime status, Astra High coordination, review and escalation when applicable. Show C/R if useful; do not dump factor tables or internal deliberation. Report limitations plainly, including when the environment could only recommend a model rather than execute it.
