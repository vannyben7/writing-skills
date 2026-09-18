"""Offline upstream-check tests: every API response and subprocess is mocked."""

import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "upstream_checker", Path(__file__).resolve().parents[1] / "scripts" / "check_upstreams.py")
watcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watcher)

HEAD = "a" * 40
NEXT_HEAD = "b" * 40
FILE = "c" * 40
LICENSE = "d" * 40
CHANGED = "e" * 40
FIRST = "2026-01-01T00:00:00+00:00"
SECOND = "2026-01-08T00:00:00+00:00"
REPO = "example/writing"
BASE = f"repos/{REPO}"


def watchlist():
    return {"schema_version": 1, "sources": [{
        "id": "example-writing", "repository": REPO, "why": "Synthetic source",
        "paths": [
            {"path": "SKILL.md", "kind": "instructions", "why": "Editing rules"},
            {"path": "LICENSE", "kind": "license", "why": "License notice"},
        ],
    }]}


def responses(head=HEAD, file_sha=FILE, license_sha=LICENSE):
    return {
        BASE: {"full_name": REPO, "default_branch": "main", "archived": False,
               "license": {"spdx_id": "MIT"}},
        f"{BASE}/commits/main": {"sha": head},
        f"{BASE}/releases/latest": watcher.APIError("http_error", 404),
        f"{BASE}/git/trees/{head}?recursive=1": {
            "truncated": False, "tree": [
                {"path": "SKILL.md", "type": "blob", "sha": file_sha},
                {"path": "LICENSE", "type": "blob", "sha": license_sha},
            ]},
        f"{BASE}/compare/{HEAD}...{NEXT_HEAD}": {"status": "ahead"},
    }


class MockAPI:
    def __init__(self, data):
        self.data, self.calls = data, []

    def get(self, endpoint):
        self.calls.append(endpoint)
        if endpoint not in self.data:
            raise AssertionError(f"Unexpected API request: {endpoint}")
        value = self.data[endpoint]
        if isinstance(value, Exception):
            raise value
        return copy.deepcopy(value)


def snapshot(data=None, previous=None):
    return watcher.collect_snapshot(watchlist(), previous, MockAPI(data or responses()),
                                    SECOND if previous else FIRST)


def types(result):
    return [item["type"] for item in result["sources"][0]["events"]]


def http(data=None, status=200, returncode=None):
    body = json.dumps({} if data is None else data)
    return subprocess.CompletedProcess(
        [], (0 if status == 200 else 1) if returncode is None else returncode,
        f"HTTP/2.0 {status} Example\nContent-Type: application/json\n\n{body}", "")


class SnapshotTests(unittest.TestCase):
    def test_first_run_is_baseline_not_updates(self):
        result = snapshot()
        self.assertTrue(result["baseline"])
        self.assertTrue(result["sources"][0]["baseline"])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(types(result), [])
        self.assertEqual(result["sources"][0]["state"]["latest_release"], {"status": "none"})

    def test_no_change_updates_freshness_only(self):
        first = snapshot()
        second = snapshot(previous=first)
        self.assertFalse(second["baseline"])
        self.assertEqual(types(second), [])
        self.assertEqual(second["sources"][0]["state"], first["sources"][0]["state"])
        self.assertEqual(second["sources"][0]["last_success_at"]["head"], SECOND)

    def test_commit_only_is_not_watched_file_change(self):
        result = snapshot(responses(head=NEXT_HEAD), snapshot())
        self.assertEqual(types(result), ["new_commit"])
        self.assertFalse(result["sources"][0]["events"][0]["review_required"])

    def test_watched_change_is_distinct_from_new_commit(self):
        result = snapshot(responses(head=NEXT_HEAD, file_sha=CHANGED), snapshot())
        self.assertEqual(types(result), ["watched_path_changed", "new_commit"])
        self.assertEqual(result["sources"][0]["events"][0]["path"], "SKILL.md")

    def test_license_file_and_metadata_changes_are_visible(self):
        data = responses(license_sha=CHANGED)
        data[BASE]["license"]["spdx_id"] = "Apache-2.0"
        result = snapshot(data, snapshot())
        self.assertEqual(types(result), ["license_file_changed", "license_metadata_changed"])

    def test_repository_failures_preserve_successful_state(self):
        first = snapshot()
        for error in (watcher.APIError("http_error", 404), watcher.APIError("http_error", 429),
                      watcher.APIError("timeout"), watcher.APIError("network_or_cli_error")):
            with self.subTest(error=error.record()):
                result = snapshot({BASE: error}, first)
                current = result["sources"][0]
                self.assertEqual(current["state"], first["sources"][0]["state"])
                self.assertEqual(current["last_success_at"], first["sources"][0]["last_success_at"])
                self.assertEqual(current["status"], "unavailable")
                self.assertEqual(current["current"]["repository"], "unknown")
                self.assertEqual(types(result), [])

    def test_release_error_is_unknown_not_none_or_no_change(self):
        data = responses()
        data[f"{BASE}/releases/latest"] = {"id": 1, "tag_name": "v1", "published_at": FIRST}
        first = snapshot(data)
        for status in (403, 429, 500):
            with self.subTest(status=status):
                failed = responses()
                failed[f"{BASE}/releases/latest"] = watcher.APIError("http_error", status)
                result = snapshot(failed, first)["sources"][0]
                self.assertEqual(result["state"]["latest_release"], first["sources"][0]["state"]["latest_release"])
                self.assertEqual(result["current"]["latest_release"], "unknown")
                self.assertEqual(result["last_success_at"]["latest_release"], FIRST)
                self.assertEqual(result["status"], "partial")

    def test_new_release_is_reported(self):
        data = responses()
        data[f"{BASE}/releases/latest"] = {"id": 2, "tag_name": "v2", "published_at": SECOND}
        self.assertEqual(types(snapshot(data, snapshot())), ["latest_stable_release_changed"])

    def test_removed_path_and_possible_move_are_not_auto_followed(self):
        data = responses()
        data[f"{BASE}/git/trees/{HEAD}?recursive=1"]["tree"][0]["path"] = "moved/SKILL.md"
        result = snapshot(data, snapshot())["sources"][0]
        self.assertEqual(result["state"]["paths"]["SKILL.md"], {"status": "missing"})
        self.assertEqual(result["events"][0]["possible_moves"], ["moved/SKILL.md"])
        self.assertNotIn("moved/SKILL.md", result["state"]["paths"])

    def test_missing_path_at_baseline_is_a_configuration_warning(self):
        data = responses()
        data[f"{BASE}/git/trees/{HEAD}?recursive=1"]["tree"].pop(0)
        result = snapshot(data)
        self.assertEqual(types(result), ["watched_path_missing_at_baseline"])
        self.assertTrue(result["sources"][0]["events"][0]["review_required"])

    def test_truncated_tree_uses_pinned_contents_request(self):
        data = responses()
        tree = data[f"{BASE}/git/trees/{HEAD}?recursive=1"]
        tree["truncated"], tree["tree"] = True, []
        data[f"{BASE}/contents/SKILL.md?ref={HEAD}"] = {"type": "file", "sha": FILE}
        data[f"{BASE}/contents/LICENSE?ref={HEAD}"] = {"type": "file", "sha": LICENSE}
        self.assertEqual(snapshot(data)["status"], "ok")

    def test_tree_and_path_errors_preserve_previous_path(self):
        data = responses()
        data[f"{BASE}/git/trees/{HEAD}?recursive=1"] = watcher.APIError("http_error", 500)
        data[f"{BASE}/contents/SKILL.md?ref={HEAD}"] = watcher.APIError("timeout")
        data[f"{BASE}/contents/LICENSE?ref={HEAD}"] = {"type": "file", "sha": LICENSE}
        result = snapshot(data, snapshot())["sources"][0]
        self.assertEqual(result["current"]["paths"]["SKILL.md"], "unknown")
        self.assertEqual(result["state"]["paths"]["SKILL.md"]["sha"], FILE)
        self.assertEqual(result["last_success_at"]["paths"]["SKILL.md"], FIRST)

    def test_branch_rewrite_and_unknown_ancestry_need_review(self):
        for value in ({"status": "diverged"}, {"status": "behind"}, watcher.APIError("http_error", 404)):
            with self.subTest(value=value):
                data = responses(head=NEXT_HEAD)
                data[f"{BASE}/compare/{HEAD}...{NEXT_HEAD}"] = value
                result = snapshot(data, snapshot())
                self.assertEqual(types(result), ["head_changed"])
                self.assertTrue(result["sources"][0]["events"][0]["review_required"])

    def test_renamed_repository_needs_review(self):
        data = responses()
        data[BASE]["full_name"] = "example/renamed"
        self.assertEqual(types(snapshot(data, snapshot())), ["repository_renamed"])

    def test_malformed_api_data_is_unknown_and_retains_state(self):
        data = responses()
        data[f"{BASE}/commits/main"] = {"sha": "invalid"}
        result = snapshot(data, snapshot())["sources"][0]
        self.assertEqual(result["state"]["head"]["sha"], HEAD)
        self.assertEqual(result["current"]["head"], "unknown")
        self.assertEqual(result["status"], "partial")

    def test_invalid_local_input_is_rejected_before_network(self):
        invalid = [None, {"schema_version": 2}, {"schema_version": 1, "sources": []}]
        for path in ("../escape", "/absolute", "a/../b", "a\\b", "a//b"):
            data = watchlist()
            data["sources"][0]["paths"][0]["path"] = path
            invalid.append(data)
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(ValueError):
                watcher.collect_snapshot(data, None, MockAPI({}))

    def test_malformed_previous_is_rejected_before_network(self):
        for field, bad in (("state", []), ("last_success_at", {"paths": []})):
            data = snapshot()
            data["sources"][0][field] = bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                watcher.collect_snapshot(watchlist(), data, MockAPI({}))


class TransportTests(unittest.TestCase):
    @patch.object(watcher.subprocess, "run")
    def test_get_is_read_only_bounded_and_shell_free(self, run):
        run.return_value = http({"ok": True})
        api = watcher.GitHubAPI(timeout=3)
        self.assertEqual(api.get(BASE), {"ok": True})
        args, kwargs = run.call_args
        self.assertEqual(args[0][:6], ["gh", "api", "--hostname", "github.com", "--method", "GET"])
        self.assertNotIn("shell", kwargs)
        self.assertLessEqual(kwargs["timeout"], 3)
        self.assertEqual(kwargs["env"]["GH_PROMPT_DISABLED"], "1")

    @patch.object(watcher.subprocess, "run")
    def test_auth_and_rate_limit_stop_further_subprocesses(self, run):
        for status in (401, 403, 429):
            with self.subTest(status=status):
                run.reset_mock()
                run.return_value = http(status=status)
                api = watcher.GitHubAPI()
                with self.assertRaises(watcher.APIError) as first:
                    api.get(BASE)
                self.assertEqual(first.exception.status, status)
                for _ in range(3):
                    with self.assertRaises(watcher.APIError) as stopped:
                        api.get(BASE)
                    self.assertEqual(stopped.exception.kind, f"stopped_after_http_{status}")
                self.assertEqual(run.call_count, 1)

    @patch.object(watcher.subprocess, "run")
    def test_two_transport_failures_stop_further_subprocesses(self, run):
        for failure in (subprocess.TimeoutExpired("gh", 1), OSError("Unavailable"),
                        subprocess.CompletedProcess([], 1, "", "transport error"),
                        http(returncode=1)):
            with self.subTest(failure=failure):
                run.reset_mock()
                run.side_effect = [failure, failure] if isinstance(failure, Exception) else None
                run.return_value = failure
                api = watcher.GitHubAPI()
                for _ in range(2):
                    with self.assertRaises(watcher.APIError):
                        api.get(BASE)
                with self.assertRaises(watcher.APIError) as stopped:
                    api.get(BASE)
                self.assertEqual(stopped.exception.kind, "stopped_after_transport_failures")
                self.assertEqual(run.call_count, 2)

    @patch.object(watcher.subprocess, "run")
    def test_http_response_resets_transport_failure_counter(self, run):
        run.side_effect = [subprocess.TimeoutExpired("gh", 1), http(status=404),
                           subprocess.TimeoutExpired("gh", 1), http({"ok": True})]
        api = watcher.GitHubAPI()
        for _ in range(3):
            with self.assertRaises(watcher.APIError):
                api.get(BASE)
        self.assertEqual(api.get(BASE), {"ok": True})
        self.assertEqual(run.call_count, 4)
        self.assertIsNone(api.stopped)

    @patch.object(watcher.subprocess, "run")
    def test_stopped_run_retains_later_repository_state(self, run):
        config = watchlist()
        second = copy.deepcopy(config["sources"][0])
        second.update(id="second-writing", repository="example/second")
        config["sources"].append(second)
        first = snapshot()
        prior_second = copy.deepcopy(first["sources"][0])
        prior_second.update(id="second-writing", repository="example/second")
        first["sources"].append(prior_second)
        run.return_value = http(status=429)
        result = watcher.collect_snapshot(config, first, watcher.GitHubAPI(), SECOND)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(result["sources"][1]["state"], prior_second["state"])
        self.assertEqual(result["sources"][1]["current"]["repository"], "unknown")
        self.assertEqual(result["sources"][1]["errors"][0]["kind"], "stopped_after_http_429")

    @patch.object(watcher.subprocess, "run")
    def test_request_and_time_budgets_prevent_calls(self, run):
        run.return_value = http()
        api = watcher.GitHubAPI(max_requests=1)
        api.get(BASE)
        with self.assertRaises(watcher.APIError) as exhausted:
            api.get(BASE)
        self.assertEqual(exhausted.exception.kind, "budget_exhausted")
        self.assertEqual(run.call_count, 1)
        api = watcher.GitHubAPI(max_seconds=0)
        with self.assertRaises(watcher.APIError):
            api.get(BASE)
        self.assertEqual(run.call_count, 1)

    @patch.object(watcher.subprocess, "run")
    def test_invalid_json_is_reported_without_remote_error_text(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "HTTP/2.0 200 OK\n\nnot json", "remote text")
        with self.assertRaises(watcher.APIError) as error:
            watcher.GitHubAPI().get(BASE)
        self.assertEqual(error.exception.record(), {"kind": "invalid_json"})


if __name__ == "__main__":
    unittest.main()
