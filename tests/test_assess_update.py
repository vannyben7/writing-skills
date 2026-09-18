"""Synthetic policy arithmetic/schema fixtures, NOT writing-quality evidence."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("assess_update", ROOT / "scripts/assess_update.py")
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


def passed():
    return {"status": "pass", "evidence": "Synthetic unit-test review reference, not a real observation."}


def record(tier="docs_structure"):
    # synthetic=False exercises the declared-observation branch of the parser;
    # these generated records remain fictional tests, never release evidence.
    data = {
        "schema_version": 1, "synthetic": False, "tier": tier,
        "candidate": "fictional-candidate", "claim": "none",
        "screening": {key: {"score": 2, "rationale": "Fictional rationale for arithmetic testing."}
                      for key in policy.SCORES},
        "checks": {key: passed() for key in policy.RELEASE_CHECKS},
        "review": {"reviewer": "fictional-separate-reviewer", "independent_of_author": True,
                   "evidence": "Fictional review receipt."},
        "budget": {"weekly_candidates": 1, "triage_minutes": 20, "monthly_model_calls": 48,
                   "paid_api": False, "new_subscription": False, "expansion_authorization": None,
                   "quota_or_auth_blocked": False, "rate_limited": False, "transport_failures": 0},
        "evidence": {"kind": "observed", "artifacts": [{"reference": "fixture-only", "sha256": "a" * 64}],
                     "behavior_unchanged": True, "structure_checks_passed": True},
    }
    if tier == "screening":
        data["checks"] = {key: passed() for key in policy.COMMON_CHECKS}
        data["review"] = data["evidence"] = None
    return data


def trial_protocol(style, cells):
    result = {"reference": "fictional-locked-plan", "policy_version": policy.POLICY_VERSION,
              "candidate_sha256": "b" * 64, "incumbent_sha256": "c" * 64,
              "frozen_before_trials": True, "fixed_sample": True, "no_optional_stopping": True,
              "source_level_units": True, "settings_identical": True, "cells": cells}
    if style:
        result.update(fresh_heldout=True, anonymous=True, swapped_order=True, judge_independent=True,
                      judge_type="independent_human", judge_identity="fictional-reader",
                      independence_evidence="Fictional separation and calibration record.")
    return result


def observation(vote="win", style=True):
    result = {"candidate_fidelity": "pass", "privacy": "pass", "fidelity_dispute": False,
              "critical_issue": False}
    result.update({"normal": vote, "swapped": vote} if style else {"result": vote})
    return result


def style_record(n=30, votes=None, languages=("zh",)):
    data = record("style_improvement")
    data["claim"] = "general_style_advantage"
    plans, cells = [], []
    for language in languages:
        ids = [f"{language}-source-{i:03}" for i in range(n)]
        plans.append({"language": language, "path": "human-writing", "source_ids": ids})
        units = []
        for i, source in enumerate(ids):
            vote = votes[i] if votes else "win"
            comparisons = {control: [observation(vote), observation(vote)] for control in ("incumbent", "plain")}
            units.append({"source_id": source, "comparisons": comparisons})
        cells.append({"language": language, "path": "human-writing", "units": units})
    data["evidence"] = {"kind": "observed", "artifacts": [{"reference": "fictional-logs", "sha256": "d" * 64}],
                        "protocol": trial_protocol(True, plans), "cells": cells}
    return data


def bugfix_record(languages=("zh",), guards_per_cell=12):
    data = record("targeted_bugfix")
    data["claim"] = "targeted_fix"
    plans, cells = [], []
    for index, language in enumerate(languages):
        units = []
        roles = (["original"] if index == 0 else []) + ["guard"] * guards_per_cell
        for i, role in enumerate(roles):
            units.append({"source_id": f"{language}-{i:03}", "role": role, "unseen": role == "guard",
                          "incumbent_reproduced": [role == "original"] * 2,
                          "repeats": [observation("pass", False), observation("pass", False)]})
        plans.append({"language": language, "path": "human-writing", "source_ids": [u["source_id"] for u in units]})
        cells.append({"language": language, "path": "human-writing", "units": units})
    data["evidence"] = {"kind": "observed", "artifacts": [{"reference": "fictional-logs", "sha256": "d" * 64}],
                        "protocol": trial_protocol(False, plans), "cells": cells}
    return data


class AssessmentTests(unittest.TestCase):
    def decision(self, data, expected):
        result = policy.assess(data)
        self.assertEqual(result["decision"], expected, result)
        self.assertIs(result["automatic_publish"], False)
        return result

    def test_screening_is_not_release(self):
        data = record("screening")
        self.decision(data, "investigate")
        data["screening"]["relevance"]["score"] = 0
        data["screening"]["gap_evidence"]["score"] = 0
        self.decision(data, "defer")

    def test_license_and_security_veto_even_with_ten_points(self):
        for key in ("license", "security"):
            data = record()
            data["checks"][key]["status"] = "fail"
            self.decision(data, "reject")

    def test_docs_eligible_without_writing_claim(self):
        self.decision(record(), "eligible_for_release_review")
        data = record()
        data["evidence"]["behavior_unchanged"] = False
        self.decision(data, "defer")

    def test_missing_all_hard_flags_fail_closed(self):
        for key in policy.RELEASE_CHECKS:
            data = record()
            del data["checks"][key]
            self.decision(data, "reject")

    def test_unknown_or_failed_protection_not_default_pass(self):
        for status in ("unknown", "fail"):
            data = record()
            data["checks"]["privacy_consent"]["status"] = status
            self.decision(data, "defer")

    def test_exact_types_unknown_fields_and_empty_support(self):
        mutations = [lambda x: x.update(schema_version=True),
                     lambda x: x.update(synthetic="false"),
                     lambda x: x.update(threshold=0),
                     lambda x: x["screening"]["relevance"].update(score=True),
                     lambda x: x["checks"]["license"].update(evidence=" "),
                     lambda x: x["budget"].update(monthly_model_calls=-1)]
        for mutation in mutations:
            data = record()
            mutation(data)
            self.decision(data, "reject")

    def test_unsupported_and_synthetic_evidence(self):
        for kind in ("synthetic", "unsupported"):
            data = record()
            data["evidence"]["kind"] = kind
            self.decision(data, "defer")
        data = record()
        data["synthetic"] = True
        self.decision(data, "reject")

    def test_actual_example_never_qualifies(self):
        data = json.loads((ROOT / "examples/update-evidence.json").read_text())
        result = self.decision(data, "reject")
        self.assertTrue(any("synthetic" in r for r in result["reasons"]))

    def test_review_requires_separate_operational_reviewer(self):
        data = record()
        data["review"]["independent_of_author"] = False
        self.decision(data, "defer")

    def test_unsupported_personal_voice_or_tier_claim(self):
        for claim in ("personal_voice_validated", "general_style_advantage"):
            data = record()
            data["claim"] = claim
            self.decision(data, "reject")

    def test_budget_stops_and_expansion_never_bypasses_provider_stop(self):
        for key, value in (("weekly_candidates", 2), ("triage_minutes", 21), ("monthly_model_calls", 49),
                           ("paid_api", True), ("new_subscription", True)):
            data = record()
            data["budget"][key] = value
            self.decision(data, "defer")
            data["budget"]["expansion_authorization"] = "Fictional explicit authority for this test."
            self.decision(data, "eligible_for_release_review")
        for key, value in (("quota_or_auth_blocked", True), ("rate_limited", True), ("transport_failures", 2)):
            data = record()
            data["budget"].update({key: value, "expansion_authorization": "Fictional authority."})
            self.decision(data, "defer")

    def test_bugfix_requires_original_and_twelve_guards_two_repeats(self):
        self.decision(bugfix_record(), "eligible_for_release_review")
        self.decision(bugfix_record(guards_per_cell=11), "defer")
        data = bugfix_record()
        data["evidence"]["cells"][0]["units"][0]["incumbent_reproduced"][1] = False
        self.decision(data, "defer")
        data = bugfix_record()
        data["evidence"]["cells"][0]["units"][1]["repeats"].pop()
        self.decision(data, "reject")

    def test_bugfix_bilingual_split_and_unseen_protection(self):
        self.decision(bugfix_record(("zh", "en"), 6), "eligible_for_release_review")
        data = bugfix_record(("zh", "en"), 6)
        data["evidence"]["cells"][1]["units"][0]["unseen"] = False
        self.decision(data, "defer")

    def test_bugfix_any_failure_or_missing_case_blocks(self):
        data = bugfix_record()
        data["evidence"]["cells"][0]["units"][2]["repeats"][1]["result"] = "fail"
        self.decision(data, "defer")
        data = bugfix_record()
        data["evidence"]["cells"][0]["units"].pop()
        result = self.decision(data, "defer")
        self.assertEqual(result["metrics"][0]["N"], 13)
        self.assertEqual(result["metrics"][0]["missing"], 1)

    def test_style_passing_and_original_record_unchanged(self):
        data = style_record()
        before = copy.deepcopy(data)
        result = self.decision(data, "eligible_for_release_review")
        self.assertEqual(data, before)
        self.assertEqual(len(result["metrics"]), 2)
        self.assertEqual(result["metrics"][0]["N"], 30)
        self.assertEqual(result["metrics"][0]["win"], 30)  # NOT 120 judgments.

    def test_small_n_not_fixed_by_repeats(self):
        self.decision(style_record(n=29), "defer")

    def test_all_ties_keep_denominator_and_cannot_win(self):
        result = self.decision(style_record(votes=["tie"] * 30), "defer")
        metric = result["metrics"][0]
        self.assertEqual((metric["N"], metric["tie"], metric["sign_test_p"]), (30, 30, 1.0))

    def test_cross_cell_and_control_correction(self):
        votes = ["win"] * 6 + ["tie"] * 24  # p=1/64 passes .025 but fails .0125.
        one = self.decision(style_record(votes=votes), "eligible_for_release_review")
        two = self.decision(style_record(votes=votes, languages=("zh", "en")), "defer")
        self.assertEqual(one["metrics"][0]["family_size"], 2)
        self.assertEqual(two["metrics"][0]["family_size"], 4)
        self.assertTrue(any("0.05/4" in reason for reason in two["reasons"]))

    def test_missing_units_and_missing_cells_not_dropped(self):
        data = style_record()
        data["evidence"]["cells"][0]["units"].pop()
        result = self.decision(data, "defer")
        self.assertEqual((result["metrics"][0]["N"], result["metrics"][0]["invalid"]), (30, 1))
        data = style_record(languages=("zh", "en"))
        data["evidence"]["cells"].pop()
        result = self.decision(data, "defer")
        self.assertEqual(result["metrics"][-1]["invalid"], 30)
        self.assertEqual(result["metrics"][0]["family_size"], 4)

    def test_excluded_field_and_duplicate_source_rejected(self):
        data = style_record()
        data["evidence"]["cells"][0]["excluded"] = 1
        self.decision(data, "reject")
        data = style_record()
        data["evidence"]["protocol"]["cells"][0]["source_ids"][1] = "zh-source-000"
        self.decision(data, "reject")

    def test_swapped_and_repeat_disagreement_is_unstable(self):
        for field, repeat in (("swapped", 0), ("normal", 1)):
            data = style_record()
            for unit in data["evidence"]["cells"][0]["units"][:4]:
                unit["comparisons"]["incumbent"][repeat][field] = "tie"
            result = self.decision(data, "defer")
            self.assertEqual(result["metrics"][0]["unstable"], 4)
            self.assertEqual(result["metrics"][0]["N"], 30)

    def test_unstable_boundary_is_inclusive(self):
        data = style_record()
        for unit in data["evidence"]["cells"][0]["units"][:3]:
            unit["comparisons"]["incumbent"][0]["swapped"] = "tie"
        self.decision(data, "eligible_for_release_review")

    def test_losses_and_net_effect_have_separate_gates(self):
        result = self.decision(style_record(votes=["win"] * 26 + ["loss"] * 4), "defer")
        self.assertTrue(any("loss rate" in r for r in result["reasons"]))
        result = self.decision(style_record(votes=["win"] * 4 + ["tie"] * 26), "defer")
        self.assertTrue(any("net preference" in r for r in result["reasons"]))

    def test_critical_disputed_unknown_semantics_are_hard_gates(self):
        for key, value in (("critical_issue", True), ("fidelity_dispute", True),
                           ("candidate_fidelity", "unknown"), ("privacy", "fail")):
            data = style_record()
            data["evidence"]["cells"][0]["units"][0]["comparisons"]["plain"][0][key] = value
            self.decision(data, "defer")

    def test_same_model_judge_remains_exploratory(self):
        data = style_record()
        data["evidence"]["protocol"]["judge_type"] = "same_model"
        self.decision(data, "defer")

    def test_plan_lock_settings_and_freshness_not_optional(self):
        for flag in ("fixed_sample", "frozen_before_trials", "no_optional_stopping", "fresh_heldout",
                     "settings_identical", "judge_independent", "source_level_units", "anonymous", "swapped_order"):
            data = style_record()
            data["evidence"]["protocol"][flag] = False
            self.decision(data, "defer")
        data = style_record()
        del data["evidence"]["protocol"]["fresh_heldout"]
        self.decision(data, "reject")

    def test_exact_sign_test_invariants(self):
        self.assertEqual(policy.exact_sign_test(0, 0), 1)
        self.assertEqual(policy.exact_sign_test(6, 0), Fraction(1, 64))
        self.assertEqual(policy.exact_sign_test(3, 1), Fraction(5, 16))
        for n in range(1, 15):
            values = [policy.exact_sign_test(w, n - w) for w in range(n + 1)]
            self.assertEqual(values, sorted(values, reverse=True))
            self.assertEqual(values[0], 1)
            self.assertEqual(values[-1], Fraction(1, 2 ** n))

    def test_cli_duplicate_keys_nonfinite_missing_file_and_no_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            for raw in ('{"schema_version": 1, "schema_version": 1}', '{"score": NaN}', '[1, 2]'):
                path.write_text(raw)
                before = sorted(Path(directory).iterdir())
                result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/assess_update.py"), str(path)],
                                        text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(json.loads(result.stdout)["decision"], "reject")
                self.assertEqual(before, sorted(Path(directory).iterdir()))
                self.assertEqual(path.read_text(), raw)
            path.unlink()
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/assess_update.py"), str(path)],
                                    text=True, capture_output=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["decision"], "reject")


if __name__ == "__main__":
    unittest.main()
