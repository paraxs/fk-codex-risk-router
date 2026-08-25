# fk-codex-risk-router

[![Router version](https://img.shields.io/badge/router-v0.2.1-6C5CE7)](./SKILL.md)
[![Activation](https://img.shields.io/badge/activation-explicit--only-0EA5E9)](./agents/openai.yaml)
[![Models](https://img.shields.io/badge/models-GPT--5.6%20Luna%20%7C%20Terra%20%7C%20Sol-111827)](./SKILL.md)

A Codex skill that routes bounded coding tasks across GPT-5.6 Luna, Terra, and Sol. It scores complexity and risk separately: complexity selects the worker; risk selects validation and independent review.

<p align="center">
  <img src="docs/risk-router-flow.svg" width="100%" alt="Flowchart of the Codex Risk Router from explicit activation through policy, separate complexity and risk scoring, worker and review selection, validation, retry, escalation, and reporting." />
</p>

## Routing contract

| Stage | Decision |
|---|---|
| Activation | Run only when invoked as `$fk-codex-risk-router` or required by the repository's `AGENTS.md`. |
| Project policy | Read `.codex/risk-router.toml`; on first opt-in, persist mode, xHigh policy, and statistics preference. |
| Complexity | Score ambiguity, coupling, causal depth, architecture/novelty, and context breadth from 0–2 each. |
| Risk | Score blast radius, data/security, reversibility, side effects, and verification strength from 0–2 each. |
| Execution | Use direct execution only for eligible micro-tasks; otherwise delegate to the routed GPT-5.6 worker. |
| Safeguards | Validate every result. Add an independent reviewer according to risk and the complexity floor. |
| Recovery | Allow one bounded same-tier correction, then escalate `Luna → Terra → Sol High → Sol xHigh` when policy permits. |
| Reporting | Report routing facts, validation, review, escalation, and remaining uncertainty without claiming unverified runtime metadata. |

## Worker selection

`C` is the 0–10 complexity score.

| Mode | Luna High | Terra High | Sol High | Sol xHigh* |
|---|---:|---:|---:|---:|
| Efficient | C 0–4 | C 5–7 | C 8–9 | C 10 |
| Balanced | C 0–3 | C 4–6 | C 7–8 | C 9–10 |
| Quality | C 0–2 | C 3–5 | C 6–7 | C 8–10 |

`*` Sol xHigh follows project policy: automatic, ask first, or disabled. If unavailable or disabled, Sol High is the ceiling and the fallback is recorded.

### Direct-execution gate

The parent may execute directly only when all conditions hold:

- `complexity ≤ 2` and `risk ≤ 2`;
- no independent review is required;
- the change is narrowly localized;
- validation is deterministic;
- delegation would add obvious overhead.

For `complexity ≥ 3`, the worker table applies.

## Review selection

`R` is the 0–10 risk score.

| Risk | Independent review |
|---:|---|
| R 0–2 | Not required when deterministic checks pass; otherwise Terra High |
| R 3–5 | Terra High |
| R 6–8 | Sol High |
| R 9–10 | Sol xHigh when permitted; otherwise Sol High plus the strongest practical verification |

For tasks that require independent review, complexity 6–10 sets a minimum reviewer of Sol High. The stronger applicable reviewer wins.

## Install

Personal installation:

```bash
git clone https://github.com/paraxs/fk-codex-risk-router.git "$HOME/.agents/skills/fk-codex-risk-router"
```

Repository-scoped installation:

```bash
git clone https://github.com/paraxs/fk-codex-risk-router.git .agents/skills/fk-codex-risk-router
```

Codex detects skill changes automatically. Restart Codex if the skill does not appear. See the [official OpenAI skill documentation](https://developers.openai.com/codex/skills) for skill locations and invocation behavior.

## Use

Invoke the skill explicitly:

```text
$fk-codex-risk-router implement the requested coding change
```

On first project opt-in, the router asks for:

1. mode: Efficient, Balanced, or Quality First;
2. Sol xHigh policy: automatic, ask first, or disabled.

The answers are stored in `.codex/risk-router.toml`, and the repository opt-in is recorded in `AGENTS.md`. For one-off routing, request one-off use; the router then uses balanced mode, asks before xHigh, disables statistics, and writes no project policy.

## Files

```text
fk-codex-risk-router/
├── SKILL.md                 # routing rules and operational contract
├── agents/openai.yaml       # explicit-only invocation policy
└── docs/risk-router-flow.svg
```

## Boundaries

Version 0.2.1 deliberately excludes custom model-pinned agent TOMLs, orchestration services, MCP routing layers, databases, dashboards, nested agent hierarchies, automatic `max` reasoning, and repeated retry loops.
