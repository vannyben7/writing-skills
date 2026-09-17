#!/usr/bin/env python3
"""Offline structural checks for the public writing-skills file set."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
SKILLS = {"human-writing": "2.12.1", "academic-clarity": "1.1.1"}
ROOT_FILES = {
    ".github/workflows/check-release.yml", ".gitignore", "LICENSE", "README.md",
    "RELEASE_FILES.txt", "THIRD_PARTY_NOTICES.md", "EVALUATION.md",
    "scripts/check_release.py",
}
FIXTURE = "skills/human-writing/assets/TEST-profile.json"
PRIVATE_DIRECTORIES = {
    "writing-profiles", "profiles", "samples", "private", "runs", "baseline",
    "corpus", "holdout", "model-outputs", "node_modules", "__pycache__",
    ".cache", ".npm", ".agents", ".codex",
}


class ReleaseError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseError(message)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def check_public_path(relative: str) -> None:
    path = PurePosixPath(relative)
    require(not path.is_absolute() and ".." not in path.parts,
            f"Nonportable manifest path: {relative}")
    require(not PRIVATE_DIRECTORIES.intersection(path.parts),
            f"Private or generated directory is not public: {relative}")
    require(not any(part.startswith(".validation-") for part in path.parts),
            f"Temporary validation artifact: {relative}")
    name = path.name.lower()
    require(not (name.startswith((".env", "credentials")) or
                 name.endswith((".log", ".pem", ".key", ".pyc", ".tgz")) or
                 name in {".netrc", ".npmrc", ".ds_store"}),
            f"Private or generated file is not public: {relative}")


def load_file_set() -> set[str]:
    listed = [line.strip() for line in read("RELEASE_FILES.txt").splitlines()
              if line.strip()]
    require(len(listed) == len(set(listed)), "Duplicate release allowlist entry")
    expected = set(listed)
    require(ROOT_FILES <= expected, "Release allowlist omits root integration files")
    for relative in expected:
        check_public_path(relative)
        require(relative in ROOT_FILES or any(
            relative.startswith(f"skills/{name}/") for name in SKILLS),
            f"Unexpected release location: {relative}")

    actual: set[str] = set()
    for directory, dirs, names in os.walk(ROOT, topdown=True):
        base = Path(directory)
        for name in list(dirs):
            item = base / name
            require(not item.is_symlink(),
                    f"Symlinked directory is not allowed: {item.relative_to(ROOT)}")
            if base == ROOT and name == ".git":
                dirs.remove(name)  # Local repository metadata is never a release file.
                continue
            check_public_path(item.relative_to(ROOT).as_posix())
        for name in names:
            item = base / name
            relative = item.relative_to(ROOT).as_posix()
            require(not item.is_symlink(), f"Symlinked file is not allowed: {relative}")
            check_public_path(relative)
            actual.add(relative)
    require(actual == expected,
            f"Release file mismatch; missing={sorted(expected - actual)}, "
            f"unlisted={sorted(actual - expected)}")
    return actual


def check_public_text(relative: str, text: str) -> None:
    # Construct prefixes so the scanner does not mistake its own rules for data.
    personal_prefixes = ["/" + "Users" + "/", "/" + "home" + "/",
                         "/" + "private" + "/var/", "/" + "mnt" + "/data/"]
    require(not any(prefix in text for prefix in personal_prefixes),
            f"Local personal or working-data path in {relative}")
    require(re.search(r"[A-Za-z]:\\(?:Users|Documents and Settings)\\", text) is None,
            f"Local personal Windows path in {relative}")
    require(re.search(r"skill" + r"-iteration-\d{4}-\d{2}-\d{2}", text) is None,
            f"Private work-folder identifier in {relative}")
    require(re.search(r"\br\d+-(?:pilot|holdout|baseline)\b", text) is None,
            f"Private evaluation run identifier in {relative}")
    secret_patterns = (
        r"\bAKIA[0-9A-Z]{16}\b", r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",
        r"\bgithub_pat_[A-Za-z0-9_]{40,}\b", r"\bsk-[A-Za-z0-9_-]{32,}\b",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    )
    require(not any(re.search(pattern, text) for pattern in secret_patterns),
            f"Credential-like content in {relative}; inspect it before publication")


def check_links(files: set[str]) -> None:
    for relative in sorted(files):
        if not relative.endswith(".md"):
            continue
        document = ROOT / relative
        for target in re.findall(r"\]\(([^)]+)\)", read(relative)):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http", "mailto"} or target.startswith("#"):
                continue
            require(not parsed.scheme and not parsed.netloc,
                    f"Nonportable link in {relative}: {target}")
            destination = (document.parent / unquote(parsed.path)).resolve()
            require(destination.is_relative_to(ROOT),
                    f"Local link escapes release tree in {relative}: {target}")
            require(destination.exists(), f"Broken local link in {relative}: {target}")


def check_skills() -> None:
    entries = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    require(entries == set(SKILLS), "Expected exactly the two named skill entrypoints")
    for name, version in SKILLS.items():
        prefix = f"skills/{name}"
        skill = read(f"{prefix}/SKILL.md")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        require(frontmatter is not None, f"Missing frontmatter: {name}")
        metadata = frontmatter.group(1)
        require(re.search(rf"(?m)^name: {re.escape(name)}$", metadata) is not None,
                f"Skill name does not match directory: {name}")
        require(re.search(r"(?m)^description: .+", metadata) is not None,
                f"Missing skill description: {name}")
        require(f'  version: "{version}"' in metadata and
                re.search(r"(?m)^version:", metadata) is None,
                f"Skill version must remain under metadata: {name}")
        interface = read(f"{prefix}/agents/openai.yaml")
        require(f"${name}" in interface, f"Wrong UI invocation: {name}")
        require("MIT License" in read(f"{prefix}/LICENSE"),
                f"Missing preserved MIT notice: {name}")
        references = ROOT / prefix / "references"
        require(references.is_dir() and any(references.iterdir()),
                f"Missing reference resources: {name}")

    package = json.loads(read("skills/academic-clarity/package.json"))
    require(package.get("name") == "academic-clarity" and
            package.get("version") == SKILLS["academic-clarity"],
            "Academic Clarity package identity mismatch")
    require(package.get("private") is True, "Academic Clarity must stay npm-private")
    require(package.get("bin") == {"academic-clarity": "bin/cli.js"},
            "Academic Clarity CLI name mismatch")
    require(package.get("repository") == {
        "type": "git", "url": "git+https://github.com/vannyben7/writing-skills.git",
        "directory": "skills/academic-clarity",
    }, "Academic Clarity repository metadata mismatch")
    require({"references", "agents", "prompts", "examples"} <= set(package["files"]),
            "Academic Clarity package omits supporting directories")
    taxonomy = read("skills/academic-clarity/references/taxonomy.md")
    codes = re.findall(r"(?m)^\| (D\d+) \|", taxonomy)
    require(codes == [f"D{i}" for i in range(1, 15)], "Expected D1–D14 taxonomy")


def check_fixture() -> None:
    fixture = json.loads(read(FIXTURE))
    require(fixture.get("subject_type") == fixture.get("status") == "synthetic-test",
            "The public profile fixture must remain synthetic")
    require(fixture.get("enabled") is False and
            fixture.get("profile_id", "").startswith("TEST-"),
            "The public TEST fixture must remain disabled and labeled")
    require(all(item.get("subject_type") == "synthetic-test"
                for item in fixture["sample_evidence"]),
            "Every public fixture sample must remain synthetic")


def check_workflows(files: set[str]) -> None:
    root_workflows = {name for name in files if name.startswith(".github/workflows/")}
    require(root_workflows == {".github/workflows/check-release.yml"},
            "Unexpected repository-root workflow")
    for relative in files:
        if "/workflows/" not in relative:
            continue
        workflow = read(relative)
        require("npm-publish" not in PurePosixPath(relative).name and
                re.search(r"\bnpm\s+publish\b", workflow) is None,
                f"npm publication workflow is prohibited: {relative}")
    workflow = read(".github/workflows/check-release.yml")
    commands = re.findall(r"(?m)^\s*run:\s*(.+)$", workflow)
    require(commands == ["python3 scripts/check_release.py"],
            "Root CI must run only the offline structural check command")
    require("contents: read" in workflow, "Root CI must use read-only contents permission")


def run_checks() -> None:
    human = ROOT / "skills" / "human-writing"
    result = subprocess.run([sys.executable, "scripts/validate-package.py"],
                            cwd=human, text=True, capture_output=True)
    require(result.returncode == 0,
            f"Human Writing validator failed: {result.stdout}{result.stderr}")
    print(result.stdout.strip())
    node = shutil.which("node")
    require(node is not None, "Node.js 18+ is required for deterministic CLI checks")
    academic = ROOT / "skills" / "academic-clarity"
    for arguments in (["--check", "bin/cli.js"], ["bin/cli.js", "--help"],
                      ["bin/cli.js", "--version"]):
        result = subprocess.run([node, *arguments], cwd=academic,
                                text=True, capture_output=True)
        require(result.returncode == 0, f"Academic Clarity CLI failed: {arguments}")
        if arguments[-1] == "--help":
            require("  academic-clarity [options]" in result.stdout,
                    "Academic Clarity help uses the wrong command name")
        if arguments[-1] == "--version":
            require(result.stdout.strip() == SKILLS["academic-clarity"],
                    "Academic Clarity CLI version mismatch")


def main() -> int:
    try:
        files = load_file_set()
        for relative in sorted(files):
            text = read(relative)
            check_public_text(relative, text)
            if relative.endswith(".json"):
                document = json.loads(text)
                require("profile_id" not in document or relative == FIXTURE,
                        f"Unapproved profile artifact: {relative}")
        check_links(files)
        check_skills()
        check_fixture()
        check_workflows(files)
        run_checks()
    except (ReleaseError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Release check failed: {exc}", file=sys.stderr)
        return 1
    print(f"Release structure passed: {len(files)} allowlisted files, two independent skills.")
    print("No model calls, dependency installation, publication, or skill installation were run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
