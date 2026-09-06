"""Offline repository consistency checks for FK Router.

These checks validate deterministic policy and package consistency. They do not
execute an LLM, confirm runtime model identity or benchmark workflow cost.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

from route import PROCESS_BUDGET, ROUTES


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/statistics.md",
    "references/project-policy.md",
    "references/model-notes.md",
    "docs/risk-router-flow.svg",
    "assets/icon.svg",
)
MODELS = {"gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-6-astra"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def markdown_routes(text: str) -> dict[str, dict[int, str]]:
    found: dict[str, dict[int, str]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0].lower() not in ROUTES:
            continue
        mode = cells[0].lower()
        require(mode not in found and len(cells) == 5, f"duplicate/malformed {mode} row")
        mapped: dict[int, str] = {}
        for model, cell in zip(
            ("gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-6-astra"),
            cells[1:],
        ):
            match = re.fullmatch(r"C (\d+)(?:[–-](\d+))?", cell)
            require(match is not None, f"invalid complexity range: {cell}")
            start, end = int(match[1]), int(match[2] or match[1])
            require(0 <= start <= end <= 10, f"out-of-range complexity: {cell}")
            for score in range(start, end + 1):
                require(score not in mapped, f"overlap in {mode} C{score}")
                mapped[score] = model
        require(set(mapped) == set(range(11)), f"gap in {mode}")
        found[mode] = mapped
    require(set(found) == set(ROUTES), "missing routing mode")
    return found


def script_routes() -> dict[str, dict[int, str]]:
    result: dict[str, dict[int, str]] = {}
    for mode, ranges in ROUTES.items():
        mapped: dict[int, str] = {}
        for start, end, model in ranges:
            for score in range(start, end + 1):
                require(score not in mapped, f"script overlap in {mode} C{score}")
                mapped[score] = model
        require(set(mapped) == set(range(11)), f"script gap in {mode}")
        result[mode] = mapped
    return result


def validate(files: dict[str, str], root: Path = ROOT) -> str:
    skill, readme = files["SKILL.md"], files["README.md"]
    parts = skill.split("---", 2)
    require(len(parts) == 3, "missing YAML frontmatter")
    front = yaml.safe_load(parts[1])
    require(front.get("name") == "codex-risk-router", "skill identity")
    require("$codex-risk-router" in front.get("description", ""), "description activation")

    match = re.search(r"Router version: `(\d+\.\d+\.\d+)`", skill)
    require(match is not None, "missing router version")
    version = match[1]
    for source, pattern in (
        (readme, r"router-v(\d+\.\d+\.\d+)-"),
        (readme, r'alt="FK Router v(\d+\.\d+\.\d+):'),
        (files["docs/risk-router-flow.svg"], r">v(\d+\.\d+\.\d+) ·"),
    ):
        current = re.search(pattern, source)
        require(current is not None and current[1] == version, "version drift")

    skill_routes = markdown_routes(skill)
    require(skill_routes == markdown_routes(readme), "README/SKILL routing drift")
    require(skill_routes == script_routes(), "Markdown/script routing drift")
    require(set(re.findall(r"`(gpt-[a-z0-9.-]+)`", skill)) == MODELS, "model IDs")

    metadata = yaml.safe_load(files["agents/openai.yaml"])
    require(set(metadata) == {"interface", "policy"}, "metadata sections")
    require(metadata["policy"] == {"allow_implicit_invocation": False}, "activation policy")
    interface = metadata["interface"]
    required_interface = {
        "display_name", "short_description", "default_prompt", "icon_small", "icon_large"
    }
    require(set(interface) == required_interface, "interface fields")
    require(25 <= len(interface["short_description"]) <= 64, "description length")
    require("$codex-risk-router" in interface["default_prompt"], "default invocation")
    for key in ("icon_small", "icon_large"):
        require(interface[key].startswith("./assets/"), "icon path")
        require((root / interface[key]).is_file(), "missing icon")

    for name, content in files.items():
        if name.endswith(".svg"):
            ET.fromstring(content)
        if name.endswith(".md"):
            for link in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in link and not link.startswith("#"):
                    target = root / Path(name).parent / link.split("#", 1)[0]
                    require(target.exists(), f"broken link: {name}: {link}")
            for sample in re.findall(r"```toml\n(.*?)```", content, re.S):
                tomllib.loads(sample)

    stats_match = re.search(
        r"```json\n(.*?)```", files["references/statistics.md"], re.S
    )
    require(stats_match is not None, "missing statistics example")
    stats = json.loads(stats_match[1])
    require(stats["schema_version"] == 2, "statistics schema")
    require(stats["router_version"] == version, "statistics version drift")
    require(stats["work_units_authorized"] <= PROCESS_BUDGET["work_units"], "work-unit budget")
    require(stats["implementation_attempts"] <= PROCESS_BUDGET["implementation_attempts"], "attempt budget")
    require(stats["workers_started"] <= PROCESS_BUDGET["implementation_workers"], "worker budget")
    require(stats["reviewers_started"] <= PROCESS_BUDGET["independent_reviewers"], "reviewer budget")

    required_skill_terms = (
        "A roadmap is not implementation authorization.",
        "Never reset a workflow limit",
        "the next roadmap phase would begin",
        "Implementation attempts | 2 total",
        "Do not spawn a separate coordinator merely to classify",
    )
    for term in required_skill_terms:
        require(term in skill, f"missing hardening rule: {term}")
    return version


def load_files(root: Path = ROOT) -> dict[str, str]:
    return {name: (root / name).read_text(encoding="utf-8-sig") for name in FILES}


if __name__ == "__main__":
    try:
        print(
            "PASS: FK Router "
            f"{validate(load_files())} package, deterministic routes, budgets and metadata"
        )
    except (ValueError, KeyError, IndexError, TypeError, OSError, ET.ParseError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
