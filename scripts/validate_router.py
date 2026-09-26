"""Validate the published skill package; this does not execute model routing."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree

import yaml

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
FILES = ("SKILL.md", "README.md", "agents/openai.yaml", "references/cost-control.md")
MODELS = ("gpt-6-luna", "gpt-6-sol", "gpt-6-astra")
ROUTES = {
    "efficient": ((0, 1), (2, 3), (4, 6), (7, 10)),
    "balanced": ((0, 1), (2, 2), (3, 5), (6, 10)),
    "quality": (None, (0, 1), (2, 4), (5, 10)),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_files(root: Path = ROOT) -> dict[str, str]:
    return {name: (root / name).read_text(encoding="utf-8-sig") for name in FILES}


def parse_routes(skill: str) -> dict[str, tuple[tuple[int, int] | None, ...]]:
    found = {}
    for line in skill.splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5 or cells[0] not in ROUTES:
            continue
        require(cells[0] not in found, "duplicate route mode")
        ranges = []
        covered = set()
        for cell in cells[1:]:
            if cell == "—":
                ranges.append(None)
                continue
            match = re.fullmatch(r"C (\d+)(?:[–-](\d+))?", cell)
            require(match is not None, f"invalid route: {cell}")
            start, end = int(match[1]), int(match[2] or match[1])
            require(0 <= start <= end <= 10, "route score out of range")
            scores = set(range(start, end + 1))
            require(not scores & covered, "route overlap")
            covered |= scores
            ranges.append((start, end))
        require(covered == set(range(11)), "route gap")
        found[cells[0]] = tuple(ranges)
    require(found == ROUTES, "routing table drift")
    return found


def validate(files: dict[str, str], root: Path = ROOT) -> str:
    skill = files["SKILL.md"]
    frontmatch = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    require(frontmatch is not None, "missing YAML frontmatter")
    front = yaml.safe_load(frontmatch[1])
    require(front.get("name") == "codex-risk-router", "skill identity")
    require("$codex-risk-router" in front.get("description", ""), "skill invocation")
    require("do not activate merely to inspect or edit this skill" in front["description"], "skill nonactivation boundary")

    match = re.search(r"Router version: `(\d+\.\d+\.\d+)`", skill)
    require(match is not None, "missing router version")
    version = match[1]
    require(f"Router {version}" in files["README.md"], "README version drift")
    parse_routes(skill)

    mentioned = set(re.findall(r"`(gpt-[a-z0-9.-]+)`", skill))
    require(mentioned == set(MODELS), "model IDs")
    require("gpt-5.6" not in skill, "outdated worker model")
    for term in (
        "Astra as supervisor and Luna/Sol as workers",
        "It must not implement patches",
        "max_dispatches = 4",
        "max_parallel_workers = 1",
        "one corrective implementation dispatch total",
        'fork_turns = "none"',
        "accepted_unverified",
        "supervisor_unverified",
        "Separate read-only Sol high review",
    ):
        require(term in skill, f"missing supervisor/budget rule: {term}")

    metadata = yaml.safe_load(files["agents/openai.yaml"])
    require(metadata.get("policy") == {"allow_implicit_invocation": False}, "activation policy")
    interface = metadata.get("interface", {})
    require("$codex-risk-router" in interface.get("default_prompt", ""), "metadata invocation")
    for key in ("icon_small", "icon_large"):
        icon = interface.get(key, "")
        require(icon.startswith("./assets/") and (root / icon).is_file(), "missing icon")
        ElementTree.parse(root / icon)

    for name, content in files.items():
        if not name.endswith(".md"):
            continue
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in link and not link.startswith("#"):
                target = root / Path(name).parent / link.split("#", 1)[0]
                require(target.is_file(), f"broken link: {name}: {link}")
        for sample in re.findall(r"```toml\n(.*?)```", content, re.S):
            tomllib.loads(sample)
    return version


if __name__ == "__main__":
    try:
        print(f"PASS: FK Router {validate(load_files())} package, routes and metadata")
    except (ValueError, KeyError, TypeError, OSError, ElementTree.ParseError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
