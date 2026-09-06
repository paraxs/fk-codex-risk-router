---
name: codex-risk-router
description: Route explicitly requested Codex coding work across Luna, Terra, Sol and Astra with one bounded work unit, deterministic route selection, proportionate review and hard workflow limits. Use only when invoked as $codex-risk-router or required by applicable AGENTS.md.
---

# FK Router — Codex Risk Router

Router version: `0.4.0` · Model guidance checked: `2026-09-05`

## Purpose

Choose the least costly workflow likely to satisfy the current acceptance criteria. Optimize the complete workflow: coordination, context transfer, implementation, validation, review and corrections.

Correctness outranks token reduction, but extra agents, broad exploration, speculative architecture, duplicated diagnosis and repeated verification require a concrete reason. A model name is not evidence that a workflow is economical or correct.

Preserve the user's scope, architecture, working behavior, authorization boundaries and explicit budget. For single-file or single-HTML projects, keep that form unless the user explicitly authorizes a structural change.

A skill cannot switch its own running model or prove which model ran. Use only native controls exposed by the host and report requested, accepted and confirmed runtime state truthfully.

## 1. Activation

Activate only when the user invokes `$codex-risk-router` or applicable `AGENTS.md` requires it. A policy file, repository name or plain mention is not an activation mechanism. Maintaining this skill does not route unrelated work.

Read applicable `AGENTS.md` once. Read `.codex/risk-router.toml` only if it exists. Without a policy, use the defaults in this file and create no configuration or log.

## 2. Define one work unit before routing

Write a compact internal contract containing:

- one observable objective;
- authorized files/components and actions;
- explicit exclusions;
- acceptance checks;
- the stopping point.

The default allowance for one user request is **one implementation work unit**. Planning and read-only diagnosis may precede it, but they do not authorize additional implementation phases.

Use `plan_only` and do not edit when the request:

- asks for an audit, roadmap, strategy or briefing without explicitly requesting implementation;
- combines a broad audit/roadmap with several implementation phases;
- leaves the first implementation target materially ambiguous.

When several independent changes are explicitly requested, select the smallest coherent first work unit, complete it, report the remaining units and stop. Continue only after a new user instruction, unless the user explicitly authorized a named multi-unit batch in the current request. Even then, define the total batch limit before editing and stop at that limit.

Never reset a workflow limit by renaming a task, phase, package or objective. A roadmap is not implementation authorization.

## 3. Classify complexity and risk

Score complexity `C` and risk `R` from 0–10. Use the factors below as a short judgment aid; do not print the factor-by-factor deliberation routinely.

| Complexity factor | 0 | 1 | 2 |
|---|---|---|---|
| Ambiguity | exact cause/change | limited unknowns | approach substantially unknown |
| Coupling | isolated | one subsystem | multiple subsystems/layers |
| Causal depth | local | non-trivial flow | lifecycle/concurrency/distributed state |
| Architecture | established pattern | moderate choice | major trade-off/new design |
| Context breadth | narrow | several callers/files | broad system context |

| Risk factor | 0 | 1 | 2 |
|---|---|---|---|
| Blast radius | isolated | feature/module | system-wide |
| Data/security | none | limited | integrity/auth/secrets/security boundary |
| Reversibility | clean revert | multi-step | migration/irreversible state |
| Side effects | local | shared/staging | production/billing/external write |
| Verification | deterministic | partial | weak observability/material uncertainty |

Floors:

- unresolved architecture or cross-system diagnosis: `C >= 8`;
- persistent-data migration, auth/security boundaries or production infrastructure: `R >= 8`;
- unknown data-loss risk or irreversible external effect: `R >= 9`.

Mechanical volume alone does not raise complexity. High risk strengthens safeguards and review; it does not automatically justify a stronger implementation model.

## 4. Select the implementation model

Use [scripts/route.py](scripts/route.py) when available to convert `C`, `R`, mode and policy into a deterministic recommendation. If it cannot run, apply the same table directly.

| Mode | Luna | Terra | Sol | Astra |
|---|---|---|---|---|
| efficient | C 0–4 | C 5–7 | C 8–9 | C 10 |
| balanced | C 0–3 | C 4–6 | C 7–9 | C 10 |
| quality | C 0–2 | C 3–5 | C 6–8 | C 9–10 |

Model identifiers and initial reasoning:

- Luna: `gpt-5.6-luna`, High; only bounded, explicit and testable work.
- Terra: `gpt-5.6-terra`, Medium; High for `C >= 6` or unresolved non-trivial data flow.
- Sol: `gpt-5.6-sol`, Medium for a clear bounded approach; High for `C >= 8` or unresolved diagnosis.
- Astra: `gpt-6-astra`, High for `C >= 9` or major unresolved architecture.

Use xHigh only for a specific unresolved reasoning problem when lower effort is unlikely to succeed or already failed and policy permits it. Never select Max or Ultra automatically.

Apply worker ceilings from [references/project-policy.md](references/project-policy.md) only when a policy exists.

## 5. Coordinate without duplicating work

Default leadership is `adaptive`:

- Keep routing and coordination in the current thread when it can define the bounded contract and operate within host limits.
- Do not spawn a separate coordinator merely to classify, narrate or transfer the task.
- Use Astra High as the single task owner for an explicitly requested audit, project-wide architecture decision, unresolved cross-system diagnosis with `C >= 8`, or high-risk planning with `R >= 8`. Do not add a separate Astra coordinator in front of another worker for the same diagnosis.
- If Astra leadership is warranted but unavailable, complete only safe read-only preparation and report the limitation. Routine lower-risk implementation is not blocked solely because a separate Astra coordinator is unavailable.

Policy may set `leadership = "astra"`; this is an intentionally expensive opt-in that requires Astra High coordination for every routed task. Do not infer it from an older policy.

Keep substantial diagnosis and its authorized implementation with one capable owner when handing it off would duplicate the same investigation. Reuse an existing matching worker for corrections within the same work unit.

## 6. Hard workflow budget

Unless the user explicitly sets a smaller limit, one request has this maximum process budget:

| Resource | Maximum |
|---|---:|
| Implementation work units | 1 |
| Implementation workers | 1 |
| Independent reviewers | 1 when required |
| Implementation attempts | 2 total |
| Full review passes | 1 |
| Focused reviewer recheck after a fix | 1 |
| Baseline validation rounds | 1 |
| Focused validation rerun after a fix | 1 |

The initial implementation counts as attempt 1. A correction or model switch counts as attempt 2. Provider failure before work begins does not count, but try an unavailable route only once.

Do not add a framework, dependency, test harness, migration layer, backup family, large documentation set or architecture abstraction unless the current acceptance criteria or evidenced risk requires it. Do not create multiple safety copies when version control or one explicit checkpoint already provides recovery.

Parallel workers may inspect truly independent areas, but they do not increase the implementation-worker or work-unit limit. Never let several agents edit one coupled artifact concurrently.

## 7. Execute and validate

Choose the cheapest execution shape that avoids duplicated context:

- `direct`: current thread implements a localized task or already owns substantial relevant context and is sufficiently capable.
- `delegated`: one worker receives the bounded contract and only the necessary source facts.
- `fallback_current`: native worker selection is unavailable, but current execution is permitted and capable. Disclose the fallback.
- `plan_only`: no implementation is authorized or the work unit is not sufficiently defined.

A worker handoff contains only the objective, scope, exclusions, acceptance checks, relevant evidence and `STOP` conditions. Do not send full conversation history unless the host forces inheritance and the task cannot be performed safely without it.

Validate the changed behavior with the smallest decisive check set. Storage/import/migration work needs disposable round trips and error-path preservation. PDF layout work needs representative visual inspection. Do not repeat passing checks without a relevant code or environment change.

## 8. Proportionate independent review

An implementation worker cannot independently approve its own non-trivial work.

| Risk | Required independent review after implementation |
|---|---|
| R 0–3 | None when decisive deterministic checks pass; otherwise Sol High |
| R 4–6 | Sol High |
| R 7–10 | Astra High |

Use Astra High for an explicitly requested audit or architecture review. The audit itself is the review deliverable; do not automatically add another reviewer to review the auditor.

Policy `review = "astra"` upgrades every required independent review to Astra High. It does not create a review where the table says none.

The reviewer is read-only by default and receives intended behavior, relevant diff/source, constraints and validation evidence. It reports blocking defects separately from optional improvements. Optional polish does not start a repair loop or prevent acceptance.

One blocking finding may consume the single corrective attempt and focused recheck. A second material failure exhausts the work-unit budget.

## 9. Stop conditions

Stop and report instead of continuing when any condition holds:

- the current work unit passes acceptance;
- the request only authorized planning/audit;
- the next roadmap phase would begin;
- material scope or architecture expansion is needed;
- a new migration, destructive action, production write or external side effect lacks authorization;
- two implementation attempts have been consumed;
- required validation or review cannot run;
- the remaining uncertainty needs user information or a product decision.

After stopping, report completed scope, evidence, remaining work and one concrete next decision. Do not continue because time or context remains.

## 10. Runtime truth and reporting

Use these runtime states separately for coordinator, worker and reviewer:

- `confirmed`: exposed model and effort match the request;
- `accepted_unverified`: native selection was accepted but effective metadata is hidden;
- `mismatch`: exposed runtime differs;
- `unavailable`: route could not run;
- `direct`: no model switch was requested.

Never claim token savings, model execution or acceptance without evidence. A green structural test does not prove LLM routing behavior.

Report briefly in the user's language:

- result and changed scope;
- decisive validation and review;
- remaining limitation or next work unit;
- one routing line: `C/R · execution · requested/actual model · attempts · review · stop reason`.

Only when `stats = true`, read [references/statistics.md](references/statistics.md) and append one compact parent-owned record after the work unit stops. Workers and reviewers never write router statistics.
