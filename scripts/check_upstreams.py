#!/usr/bin/env python3
"""Read GitHub metadata with gh; write one snapshot to stdout, never adopt code."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
KINDS = {"instructions", "documentation", "license", "examples", "metadata", "specification"}


class APIError(Exception):
    def __init__(self, kind: str, status: int | None = None):
        super().__init__(kind)
        self.kind, self.status = kind, status

    def record(self) -> dict:
        return {"kind": self.kind, **({"http_status": self.status} if self.status else {})}


def valid_sha(value: object) -> bool:
    return isinstance(value, str) and SHA.fullmatch(value) is not None


def read_json(path: Path, maximum: int) -> object:
    if path.stat().st_size > maximum:
        raise ValueError(f"Input exceeds size limit: {path.name}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_watchlist(data: object) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Watchlist needs schema_version 1")
    sources = data.get("sources")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 32:
        raise ValueError("Watchlist needs 1–32 sources")
    ids: set[str] = set()
    repositories: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("Watchlist source must be an object")
        identifier, repository = source.get("id"), source.get("repository")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier) or identifier in ids:
            raise ValueError("Invalid or duplicate source ID")
        if not isinstance(repository, str) or not REPOSITORY.fullmatch(repository) or repository.lower() in repositories:
            raise ValueError("Invalid or duplicate repository")
        if not isinstance(source.get("why"), str) or not source["why"].strip():
            raise ValueError("Each source needs a reason")
        ids.add(identifier)
        repositories.add(repository.lower())
        paths = source.get("paths")
        if not isinstance(paths, list) or not 1 <= len(paths) <= 16:
            raise ValueError("Each source needs 1–16 watched files")
        seen: set[str] = set()
        for item in paths:
            if not isinstance(item, dict):
                raise ValueError("Watched file must be an object")
            path = item.get("path")
            if (not isinstance(path, str) or not path or len(path) > 512 or
                    PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts or
                    str(PurePosixPath(path)) != path or "\\" in path or
                    any(ord(character) < 32 for character in path) or path in seen):
                raise ValueError("Invalid or duplicate watched path")
            if item.get("kind") not in KINDS or not isinstance(item.get("why"), str) or not item["why"].strip():
                raise ValueError("Watched file needs a supported kind and reason")
            seen.add(path)
    return data


def validate_previous(data: object) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("sources"), list):
        raise ValueError("Previous snapshot needs schema_version 1 and sources")
    ids = set()
    for source in data["sources"]:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str) or source["id"] in ids:
            raise ValueError("Malformed or duplicate previous source")
        ids.add(source["id"])
        state = source.get("state")
        stamps = source.get("last_success_at", {})
        if (not isinstance(state, dict) or not isinstance(stamps, dict) or
                not isinstance(stamps.get("paths", {}), dict)):
            raise ValueError("Previous source needs state and freshness records")
        if not isinstance(source.get("repository"), str) or not REPOSITORY.fullmatch(source["repository"]):
            raise ValueError("Invalid previous repository")
        if "head" in state and (not isinstance(state["head"], dict) or not valid_sha(state["head"].get("sha"))):
            raise ValueError("Invalid previous commit SHA")
        if not isinstance(state.get("paths", {}), dict):
            raise ValueError("Previous paths must be an object")
        for value in state.get("paths", {}).values():
            if not isinstance(value, dict) or value.get("status") not in {"present", "missing"}:
                raise ValueError("Invalid previous path state")
            if value["status"] == "present" and not valid_sha(value.get("sha")):
                raise ValueError("Invalid previous file SHA")
        if "repository" in state and not isinstance(state["repository"], dict):
            raise ValueError("Invalid previous repository state")
        if "latest_release" in state and (not isinstance(state["latest_release"], dict) or
                state["latest_release"].get("status") not in {"present", "none"}):
            raise ValueError("Invalid previous release state")
    return data


class GitHubAPI:
    """Bounded GET calls only. No automatic pagination, retry, shell, or downloads."""

    def __init__(self, timeout: int = 20, max_requests: int = 128, max_seconds: int = 300):
        self.timeout, self.max_requests = timeout, max_requests
        self.deadline = time.monotonic() + max_seconds
        self.requests = 0
        self.transient_failures = 0
        self.stopped: str | None = None

    def transport_failure(self, kind: str) -> APIError:
        self.transient_failures += 1
        if self.transient_failures >= 2:
            self.stopped = "stopped_after_transport_failures"
        return APIError(kind)

    def get(self, endpoint: str) -> object:
        if self.stopped:
            raise APIError(self.stopped)
        remaining = self.deadline - time.monotonic()
        if self.requests >= self.max_requests or remaining <= 0:
            raise APIError("budget_exhausted")
        self.requests += 1
        command = ["gh", "api", "--hostname", "github.com", "--method", "GET",
                   "--include", "-H", "Accept: application/vnd.github+json",
                   "-H", "X-GitHub-Api-Version: 2022-11-28", endpoint]
        try:
            result = subprocess.run(command, capture_output=True, text=True,
                                    timeout=min(self.timeout, remaining),
                                    env={**os.environ, "GH_PROMPT_DISABLED": "1"})
        except subprocess.TimeoutExpired as exc:
            raise self.transport_failure("timeout") from exc
        except OSError as exc:
            raise self.transport_failure("gh_unavailable") from exc
        if len(result.stdout) > 8_000_000:
            raise APIError("response_too_large")
        parts = re.split(r"\r?\n\r?\n", result.stdout, maxsplit=1)
        match = re.match(r"HTTP/\S+\s+(\d{3})", parts[0])
        status = int(match.group(1)) if match else None
        if status is None:
            raise self.transport_failure("network_or_cli_error")
        if status == 200 and (result.returncode or len(parts) != 2):
            raise self.transport_failure("network_or_cli_error")
        # Any HTTP response demonstrates transport recovery, including a 404.
        self.transient_failures = 0
        if status in {401, 403, 429}:
            self.stopped = f"stopped_after_http_{status}"
        if status is not None and status != 200:
            raise APIError("http_error", status)
        try:
            return json.loads(parts[1])
        except ValueError as exc:
            raise APIError("invalid_json") from exc


def object_response(data: object, required: tuple[str, ...]) -> dict:
    if not isinstance(data, dict) or any(key not in data for key in required):
        raise APIError("invalid_response")
    return data


def repository_value(data: object) -> dict:
    data = object_response(data, ("full_name", "default_branch", "archived"))
    if (not isinstance(data["full_name"], str) or not REPOSITORY.fullmatch(data["full_name"]) or
            not isinstance(data["default_branch"], str) or not data["default_branch"] or
            not isinstance(data["archived"], bool)):
        raise APIError("invalid_response")
    license_info = data.get("license")
    if license_info is not None and not isinstance(license_info, dict):
        raise APIError("invalid_response")
    return {"full_name": data["full_name"], "default_branch": data["default_branch"],
            "archived": data["archived"], "license_spdx": (license_info or {}).get("spdx_id"),
            "url": f"https://github.com/{data['full_name']}"}


def head_value(data: object, repository: str) -> dict:
    data = object_response(data, ("sha",))
    if not valid_sha(data["sha"]):
        raise APIError("invalid_response")
    return {"sha": data["sha"], "url": f"https://github.com/{repository}/commit/{data['sha']}"}


def file_value(data: object) -> dict:
    data = object_response(data, ("sha", "type"))
    if not valid_sha(data["sha"]) or data["type"] not in {"blob", "file", "symlink", "submodule", "tree", "dir", "commit"}:
        raise APIError("invalid_response")
    return {"status": "present", "sha": data["sha"],
            "type": {"file": "blob", "dir": "tree", "submodule": "commit"}.get(data["type"], data["type"])}


def release_value(data: object) -> dict:
    data = object_response(data, ("id", "tag_name"))
    if not isinstance(data["id"], int) or not isinstance(data["tag_name"], str):
        raise APIError("invalid_response")
    return {"status": "present", "id": data["id"], "tag": data["tag_name"][:240],
            "published_at": data.get("published_at")}


def check_source(source: dict, previous: dict | None, api: GitHubAPI, now: str) -> dict:
    same_source = previous is not None and previous["repository"].lower() == source["repository"].lower()
    old = copy.deepcopy(previous.get("state", {})) if same_source else {}
    state = copy.deepcopy(old)
    stamps = copy.deepcopy(previous.get("last_success_at", {})) if same_source else {}
    state.setdefault("paths", {})
    stamps.setdefault("paths", {})
    current = {"repository": "not_checked", "head": "not_checked", "latest_release": "not_checked",
               "paths": {item["path"]: "not_checked" for item in source["paths"]}}
    errors, events = [], []
    if previous is not None and not same_source:
        events.append({"type": "watch_source_changed", "review_required": True})

    def failure(facet: str, error: APIError, path: str | None = None) -> None:
        if path is None:
            current[facet] = "unknown"
        else:
            current["paths"][path] = "unknown"
        errors.append({"facet": facet, **({"path": path} if path else {}), **error.record()})

    def success(facet: str, value: dict) -> None:
        state[facet], stamps[facet], current[facet] = value, now, "ok"

    endpoint = f"repos/{source['repository']}"
    try:
        success("repository", repository_value(api.get(endpoint)))
    except APIError as exc:
        failure("repository", exc)
    if current["repository"] == "ok":
        branch = state["repository"]["default_branch"]
        try:
            success("head", head_value(api.get(f"{endpoint}/commits/{quote(branch, safe='')}"), source["repository"]))
        except APIError as exc:
            failure("head", exc)
        try:
            success("latest_release", release_value(api.get(f"{endpoint}/releases/latest")))
        except APIError as exc:
            if exc.status == 404:
                success("latest_release", {"status": "none"})
            else:
                failure("latest_release", exc)

    tree, complete = {}, False
    if current["head"] == "ok":
        head = state["head"]["sha"]
        try:
            raw_tree = object_response(api.get(f"{endpoint}/git/trees/{head}?recursive=1"), ("tree", "truncated"))
            if not isinstance(raw_tree["tree"], list) or not isinstance(raw_tree["truncated"], bool):
                raise APIError("invalid_response")
            for item in raw_tree["tree"]:
                if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                    raise APIError("invalid_response")
                tree[item["path"]] = file_value(item)
            complete = not raw_tree["truncated"]
        except APIError as exc:
            errors.append({"facet": "tree", **exc.record()})
            tree = {}
        for item in source["paths"]:
            path = item["path"]
            try:
                if path in tree:
                    value = tree[path]
                elif complete:
                    value = {"status": "missing"}
                else:
                    try:
                        value = file_value(api.get(f"{endpoint}/contents/{quote(path, safe='/')}?ref={head}"))
                    except APIError as exc:
                        if exc.status != 404:
                            raise
                        value = {"status": "missing"}
                state["paths"][path], stamps["paths"][path], current["paths"][path] = value, now, "ok"
                prior = old.get("paths", {}).get(path)
                if prior is not None and prior != value:
                    event = {"type": "license_file_changed" if item["kind"] == "license" else "watched_path_changed",
                             "path": path, "before": prior, "after": value}
                    if value["status"] == "missing" and complete and prior.get("sha"):
                        event["possible_moves"] = sorted(name for name, entry in tree.items()
                                                          if entry.get("sha") == prior["sha"])[:5]
                    events.append(event)
                elif prior is None and value["status"] == "missing":
                    events.append({"type": "watched_path_missing_at_baseline", "path": path, "review_required": True})
            except APIError as exc:
                failure("paths", exc, path)

    if current["repository"] == "ok" and "repository" in old:
        for field, event_type in [("full_name", "repository_renamed"), ("default_branch", "default_branch_changed"),
                                  ("license_spdx", "license_metadata_changed"), ("archived", "archive_status_changed")]:
            if old["repository"].get(field) != state["repository"].get(field):
                events.append({"type": event_type, "before": old["repository"].get(field),
                               "after": state["repository"].get(field), "review_required": True})
    if current["latest_release"] == "ok" and "latest_release" in old and old["latest_release"] != state["latest_release"]:
        events.append({"type": "latest_stable_release_changed", "before": old["latest_release"], "after": state["latest_release"]})
    if current["head"] == "ok" and "head" in old and old["head"]["sha"] != state["head"]["sha"]:
        relation = "unknown"
        try:
            comparison = object_response(api.get(f"{endpoint}/compare/{old['head']['sha']}...{state['head']['sha']}"), ("status",))
            if comparison["status"] not in {"ahead", "behind", "diverged", "identical"}:
                raise APIError("invalid_response")
            relation = comparison["status"]
        except APIError as exc:
            errors.append({"facet": "ancestry", **exc.record()})
        events.append({"type": "new_commit" if relation == "ahead" else "head_changed",
                       "before": old["head"]["sha"], "after": state["head"]["sha"], "ancestry": relation,
                       "review_required": relation in {"behind", "diverged", "unknown"}})

    status = "unavailable" if current["repository"] != "ok" else ("partial" if errors else "ok")
    return {"id": source["id"], "repository": source["repository"], "status": status,
            "baseline": not same_source, "state": state, "last_success_at": stamps,
            "current": current, "events": events, "errors": errors}


def collect_snapshot(watchlist: dict, previous: dict | None, api: GitHubAPI, now: str | None = None) -> dict:
    watchlist = validate_watchlist(watchlist)
    if previous is not None:
        validate_previous(previous)
    timestamp = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    prior = {source["id"]: source for source in (previous or {}).get("sources", [])}
    sources = [check_source(source, prior.get(source["id"]), api, timestamp) for source in watchlist["sources"]]
    digest = hashlib.sha256(json.dumps(watchlist, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return {"schema_version": 1, "checked_at": timestamp, "baseline": previous is None,
            "watchlist_sha256": digest, "status": "ok" if all(item["status"] == "ok" for item in sources) else "partial",
            "sources": sources}


def bounded_integer(low: int, high: int):
    def parse(value: str) -> int:
        result = int(value)
        if not low <= result <= high:
            raise argparse.ArgumentTypeError(f"Expected {low}–{high}")
        return result
    return parse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watchlist", type=Path, default=ROOT / "maintenance" / "WATCHLIST.json")
    parser.add_argument("--previous", type=Path, help="Previous snapshot; retain successful state across failures")
    parser.add_argument("--timeout", type=bounded_integer(1, 60), default=20, help="Per-call seconds (default: 20)")
    parser.add_argument("--max-requests", type=bounded_integer(1, 200), default=128)
    parser.add_argument("--max-seconds", type=bounded_integer(1, 1800), default=300)
    args = parser.parse_args(argv)
    try:
        watchlist = validate_watchlist(read_json(args.watchlist, 100_000))
        previous = validate_previous(read_json(args.previous, 2_000_000)) if args.previous else None
        snapshot = collect_snapshot(watchlist, previous, GitHubAPI(args.timeout, args.max_requests, args.max_seconds))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"Invalid local input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0 if snapshot["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
