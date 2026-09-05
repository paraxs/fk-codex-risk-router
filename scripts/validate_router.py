"""Repository consistency checks, not an LLM behavior or cost benchmark.

Run with Python 3.11+ and PyYAML. Never loaded during ordinary routing.
"""
import json
import re
import sys
import tomllib
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = ("SKILL.md", "README.md", "agents/openai.yaml",
         "references/statistics.md", "references/project-policy.md",
         "references/model-notes.md", "docs/risk-router-flow.svg", "assets/icon.svg")
MODELS = {"gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol", "gpt-6-astra"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def routing_table(text):
    rows = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.startswith("|") or cells[0].lower() not in {"efficient", "balanced", "quality"}:
            continue
        mode = cells[0].lower()
        require(mode not in rows and len(cells) == 5, f"Duplicate/malformed {mode} row")
        routes = {}
        for model, cell in zip(("Luna", "Terra", "Sol", "Astra"), cells[1:]):
            match = re.fullmatch(r"C (\d+)(?:[–-](\d+))?", cell)
            require(match, f"Invalid range: {cell}")
            start, end = int(match[1]), int(match[2] or match[1])
            require(0 <= start <= end <= 10, f"Out-of-range complexity: {cell}")
            for score in range(start, end + 1):
                require(score not in routes, f"Overlapping {mode} C{score}")
                routes[score] = model
        require(set(routes) == set(range(11)), f"Gaps in {mode}")
        rows[mode] = routes
    require(set(rows) == {"efficient", "balanced", "quality"}, "Missing routing mode")
    return rows


def validate(files, root=ROOT):
    skill, readme = files["SKILL.md"], files["README.md"]
    front = yaml.safe_load(skill.split("---", 2)[1])
    require(front.get("name") == "codex-risk-router" and bool(front.get("description")), "Skill identity")
    version = re.search(r"Router version: `(\d+\.\d+\.\d+)`", skill)
    require(version, "Missing router version")
    version = version[1]
    for source, pattern in ((readme, r"router-v(\d+\.\d+\.\d+)-"),
                            (readme, r"alt=\"FK Router v(\d+\.\d+\.\d+):"),
                            (files["docs/risk-router-flow.svg"], r">v(\d+\.\d+\.\d+) ·")):
        match = re.search(pattern, source)
        require(match and match[1] == version, "Version drift")
    require(routing_table(skill) == routing_table(readme), "README/SKILL routing drift")
    require(set(re.findall(r"`(gpt-[a-z0-9.-]+)`", skill)) == MODELS, "Unexpected/missing model ID")
    metadata = yaml.safe_load(files["agents/openai.yaml"])
    require(set(metadata) == {"interface", "policy"}, "Unexpected metadata section")
    require(set(metadata["policy"]) == {"allow_implicit_invocation"}, "Unexpected policy key")
    require(metadata["policy"]["allow_implicit_invocation"] is False, "Implicit activation enabled")
    interface = metadata["interface"]
    require(set(interface) == {"display_name", "short_description", "default_prompt", "icon_small", "icon_large"}, "Unexpected interface fields")
    require(all(isinstance(value, str) for value in interface.values()), "Interface values must be strings")
    require(25 <= len(interface["short_description"]) <= 64, "Description length")
    require("$codex-risk-router" in interface["default_prompt"], "Wrong invocation")
    for key in ("icon_small", "icon_large"):
        require(interface[key].startswith("./assets/") and (root / interface[key]).is_file(), "Invalid icon path")
    for name, content in files.items():
        if name.endswith(".svg"):
            ET.fromstring(content)
        if name.endswith(".md"):
            for link in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in link and not link.startswith("#"):
                    require((root / Path(name).parent / link.split("#", 1)[0]).exists(), f"Broken link: {name}: {link}")
            for sample in re.findall(r"```toml\n(.*?)```", content, re.S):
                tomllib.loads(sample)
    stats = json.loads(re.search(r"```json\n(.*?)```", files["references/statistics.md"], re.S)[1])
    require(stats["router_version"] == version, "Statistics version drift")
    require(stats.get("schema_version") == 1, "Statistics schema version")
    require("recorded_at" in stats, "Missing timestamp field")
    require(stats["retry_count"] == max(0, stats["attempt_count"] - 1), "Inconsistent attempts")
    require(not re.search(r"Luna\s*→\s*Terra\s*→\s*Sol\s*→\s*Astra", files["docs/risk-router-flow.svg"]), "SVG implies mandatory ladder")
    return version


def load_files(root=ROOT):
    return {name: (root / name).read_text(encoding="utf-8-sig") for name in FILES}


if __name__ == "__main__":
    try:
        print(f"PASS: FK Router {validate(load_files())} versions, routing coverage/parity, metadata, examples, links and SVG")
    except (ValueError, KeyError, IndexError, AttributeError, OSError, ET.ParseError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
