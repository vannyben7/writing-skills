#!/usr/bin/env python3
"""Check package structure; this does not assess generated prose quality."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"Missing package file: {relative}")
    return path.read_text(encoding="utf-8")


def capture(pattern: str, source: str, message: str) -> str:
    match = re.search(pattern, source, re.MULTILINE)
    require(match is not None, message)
    return match.group(1)


skill = read("SKILL.md")
readme = read("README.md")
agents = read("AGENTS.md")
patterns = read("references/patterns.md")
plugin = json.loads(read(".claude-plugin/plugin.json"))
marketplace = json.loads(read(".claude-plugin/marketplace.json"))
fixture = json.loads(read("assets/TEST-profile.json"))

frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
require(frontmatter is not None, "SKILL.md must begin with YAML frontmatter")
metadata = frontmatter.group(1)
require(re.search(r"(?m)^name: human-writing$", metadata) is not None,
        "Keep the skill name human-writing")
require(re.search(r"(?m)^version:", metadata) is None,
        "Version belongs under metadata, not at the top level")
version = capture(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', metadata,
                  "Add metadata.version")
readme_version = capture(r"^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", readme,
                         "Add a README version entry")
require({version, readme_version, plugin.get("version")} == {version},
        "Use one version in SKILL.md, README.md, and plugin.json")
require("Independent local derivative" in metadata and "not an upstream release" in metadata,
        "Identify the independent local derivative in skill metadata")

skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
require(skill_files == {Path("SKILL.md")} and not (ROOT / "SKILL.md").is_symlink(),
        "Keep one regular SKILL.md at the package root")
require(plugin.get("name") == "human-writing" and plugin.get("skills") == ["./"],
        "Point the human-writing plugin loader to the root")
entries = marketplace.get("plugins", [])
require(marketplace.get("name") == "human-writing", "Keep the marketplace ID human-writing")
require(len(entries) == 1 and entries[0].get("name") == "human-writing"
        and entries[0].get("source") == "./", "Keep one local marketplace entry")
require("$human-writing" in read("agents/openai.yaml"), "Update the agent invocation name")
require(entries[0].get("description") == plugin.get("description"),
        "Keep plugin and marketplace descriptions in sync")
require(entries[0].get("keywords") == plugin.get("keywords"),
        "Keep plugin and marketplace keywords in sync")
require("references/patterns.md" in agents, "Update AGENTS.md for the reference catalog")
require("Copyright (c) 2025 Siqi Chen" in read("LICENSE"),
        "Keep the original copyright notice")

numbers = [int(number) for number in re.findall(r"(?m)^### ([0-9]+)\. ", patterns)]
require(numbers == list(range(1, 36)), f"Expected legacy IDs 1–35: {numbers}")
readme_numbers = [int(number) for number in re.findall(r"(?m)^\| ([0-9]+) \|", readme)]
require(readme_numbers == list(range(1, 36)), "README must index each legacy ID once")
require(len(skill.splitlines()) <= 220, "Keep the entrypoint at 220 lines or fewer")

required_references = {
    "patterns.md", "language-and-genre.md", "style-profiles.md",
    "composition-contract.md", "sources-and-decisions.md",
}
for reference in required_references:
    require(f"references/{reference}" in skill, f"Route {reference} from SKILL.md")
    read(f"references/{reference}")

# Local Markdown links should remain valid after moving or packaging references.
for document in ROOT.rglob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        destination = (document.parent / target.split("#", 1)[0]).resolve()
        require(destination.is_relative_to(ROOT),
                f"Nonportable link in {document.relative_to(ROOT)}: {target}")
        require(destination.exists(),
                f"Broken link in {document.relative_to(ROOT)}: {target}")

require(fixture.get("profile_id", "").startswith("TEST-"), "Mark the fixture TEST")
require(fixture.get("subject_type") == fixture.get("status") == "synthetic-test",
        "The fixture must not claim a real user or calibration")
require(fixture.get("enabled") is False, "Do not enable the TEST fixture by default")
sample_ids = [item["id"] for item in fixture["sample_evidence"]]
require(len(sample_ids) == len(set(sample_ids)), "Use unique fixture sample IDs")
require(all(item.get("subject_type") == "synthetic-test" for item in fixture["sample_evidence"]),
        "Label each fixture source as synthetic-test")
observations = list(fixture["common"])
for group in ("languages", "genres", "language_genre"):
    observations.extend(item for layer in fixture[group].values() for item in layer)
observation_ids = [item["id"] for item in observations]
require(len(observation_ids) == len(set(observation_ids)), "Use unique observation IDs")
for item in observations:
    require(bool(item.get("evidence")) and set(item["evidence"]) <= set(sample_ids),
            f"Observation needs resolvable evidence: {item['id']}")
    require(item.get("stability") in {"stable", "tentative"},
            f"Invalid observation stability: {item['id']}")
require(fixture["languages"].get("en") == [], "TEST fixture has no English evidence")

print(f"Human Writing local candidate v{version}: package checks passed")
print("These checks do not establish rewriting quality or personal-profile validation.")
