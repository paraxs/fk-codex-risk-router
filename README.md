# FK Codex Risk Router 0.5.0

Codex skill for a strict GPT-6 division of work: **Astra supervises; Luna and Sol execute.** The [skill](SKILL.md) classifies complexity and risk separately, delegates bounded work, verifies results, and limits dispatches and corrections. The [cost note](references/cost-control.md) explains what the skill can and cannot save.

Version 0.5.0 replaces the 0.4.0 behavior that allowed Astra implementation, GPT-5.6 workers, and direct execution in the parent thread. The substantive rules follow the revised 0.3.0 skill package; the GitHub version is 0.5.0 to keep the repository history monotonic.

## Use

Install this repository as the `codex-risk-router` skill folder in your Codex skills directory. In a new **GPT-6 Astra** chat, invoke:

```powershell
git clone https://github.com/paraxs/fk-codex-risk-router.git "$env:USERPROFILE\.codex\skills\codex-risk-router"
```

For an existing unmodified Git installation, run `git pull --ff-only` inside its skill folder. If you installed a ZIP, replace that skill folder with the repository contents. Keep only one installed copy.

```text
$codex-risk-router Behebe den beschriebenen Fehler. Astra soll klassifizieren und prüfen; Luna oder Sol sollen die Umsetzung erledigen.
```

The skill is explicit-only; a plain mention or policy file does not activate it. A skill cannot change the model of its running chat. If the current model is confirmed to be other than Astra or native model-overridden delegation is unavailable, it reports that limitation instead of claiming the requested workflow ran.

The defaults are efficient routing, Sol xhigh disabled, four counted subagent dispatches, one corrective implementation dispatch, one worker at a time, and no persistent statistics. An existing `.codex/risk-router.toml` can provide the policy described in [SKILL.md](SKILL.md). The skill does not create or change that file on its own.

## Verification and limits

Run `python scripts/validate_router.py` and `python -m unittest discover -s tests -v`. CI runs both. They verify the package and routing table; they cannot prove how an LLM follows the instructions, which model actually ran, or what a user's subscription saves. Measure completed tasks and full workflow usage before claiming a savings percentage. Native subagents may consume more total tokens than a single-agent run.
