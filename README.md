# FK Router

[![Router version](https://img.shields.io/badge/router-v0.4.0-6C5CE7)](./SKILL.md)
[![Activation](https://img.shields.io/badge/activation-explicit--only-0EA5E9)](./agents/openai.yaml)

A bounded Codex workflow router for GPT-5.6 Luna, Terra, Sol and GPT-6 Astra. Version 0.4.0 removes unconditional Astra coordination, adds a deterministic route helper and enforces one implementation work unit with hard process limits by default.

<p align="center">
  <img src="docs/risk-router-flow.svg" width="100%" alt="FK Router v0.4.0: explicit activation, one bounded work unit, proportionate model selection, targeted review and mandatory stop." />
</p>

## Why v0.4.0

Version 0.3.x could create an expensive three-context workflow for ordinary changes: Astra High coordination, a separate implementation worker and Astra High review. Its attempt limit applied per “bounded objective”, so a broad roadmap could be split into many objectives and continue without a project-level stop.

Version 0.4.0 changes the contract:

- one implementation work unit per user request by default;
- a roadmap or audit does not authorize implementation;
- limits cannot reset when a phase or package is renamed;
- at most one implementation worker, one required reviewer and two implementation attempts;
- no separate coordinator solely for routing or narration;
- Astra High as the single owner of explicit audits, project-wide architecture, unresolved C8+ cross-system diagnosis and R8+ planning, without a duplicate worker for the same analysis;
- proportional review: deterministic R0–3 needs no reviewer, R4–6 uses Sol High, R7–10 uses Astra High;
- one deterministic script converts C/R and policy into the model, review and budget recommendation;
- mandatory stop before the next roadmap phase.

These are workflow controls, not claims of measured savings. The router still cannot force or verify a model when the host does not expose native selection and runtime metadata.

## Activation

Invoke explicitly:

```text
$codex-risk-router implement the requested coding change
```

Or persist activation in an applicable `AGENTS.md`:

```text
For coding tasks in this repository, use $codex-risk-router and follow .codex/risk-router.toml.
```

A policy file alone does not activate the skill. Plain mentions are not guaranteed because `allow_implicit_invocation` remains false.

## Worker routing

`C` is the assessed complexity from 0–10.

| Mode | Luna | Terra | Sol | Astra |
|---|---|---|---|---|
| Efficient | C 0–4 | C 5–7 | C 8–9 | C 10 |
| Balanced | C 0–3 | C 4–6 | C 7–9 | C 10 |
| Quality | C 0–2 | C 3–5 | C 6–8 | C 9–10 |

Luna remains High by user preference. Terra and Sol begin at Medium where the task is clear and move to High for deeper diagnosis. Astra implementation begins at High. xHigh requires a specific unresolved reasoning need and policy permission.

Run the deterministic helper:

```bash
python scripts/route.py 6 4 --mode balanced --task-kind implementation
```

The JSON result reports the recommended worker, leadership need, review tier and hard process budget. It launches no model and claims no runtime identity.

## Review policy

| Risk | Independent review |
|---|---|
| R 0–3 | None when decisive deterministic checks pass; otherwise Sol High |
| R 4–6 | Sol High |
| R 7–10 | Astra High |

An explicit audit or architecture review uses Astra High, but the audit itself is not automatically reviewed by a second Astra thread.

## Project policy

Recommended v2 policy:

```toml
version = 2
mode = "balanced"
leadership = "adaptive"
review = "proportional"
xhigh = "ask"
astra = "auto"
stats = true
max_work_units = 1
```

Existing v1 policies remain valid. Missing v2 fields default to adaptive leadership, proportional review and one work unit. See [project-policy.md](references/project-policy.md).

## Install or update

Personal installation:

```bash
git clone https://github.com/paraxs/fk-codex-risk-router.git "$HOME/.agents/skills/codex-risk-router"
```

Repository-scoped installation:

```bash
git clone https://github.com/paraxs/fk-codex-risk-router.git .agents/skills/codex-risk-router
```

For an unmodified Git installation:

```bash
git pull --ff-only
```

For a ZIP installation, replace the entire existing skill folder and restart Codex. Keep only one installed copy. Preserve project `.codex/risk-router.toml`, `AGENTS.md` and statistics when replacing the skill.

## Validation

```bash
python scripts/validate_router.py
python -m unittest discover -s tests -v
```

The tests verify policy calculations, route coverage, hard limits, metadata and repository consistency. They do not execute an LLM or prove actual token savings. Real cost tuning requires comparable accepted tasks with complete workflow usage.
