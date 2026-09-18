#!/usr/bin/env python3
"""Offline, fail-closed maintenance evidence screening; never runs or publishes.

Input assertions are not authenticated observations. An eligible result still
requires an independent artifact review. See docs/MAINTENANCE.md.
"""

import argparse
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path


POLICY_VERSION = "maintenance-v1"
SCORES = ("relevance", "gap_evidence", "portability", "testability", "affordability")
COMMON_CHECKS = ("license", "security", "public_data_authorization")
RELEASE_CHECKS = COMMON_CHECKS + (
    "quantities_units_negation", "qualifiers_scope_causality_citations",
    "stance_priorities_voice", "privacy_consent", "no_default_raw_text_storage",
    "profile_state_and_file_boundaries", "public_export_sanitized", "rollback_ready",
)
TIERS = ("screening", "docs_structure", "targeted_bugfix", "style_improvement")
PATHS = ("human-writing", "academic-clarity", "combined")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
LIMITS = {"weekly_candidates": 1, "triage_minutes": 20, "monthly_model_calls": 48}


class InvalidEvidence(ValueError):
    """Malformed or unsupported evidence must never produce eligibility."""


def obj(value, keys, where):
    if type(value) is not dict or set(value) != set(keys):
        raise InvalidEvidence(f"{where}: expected exactly {', '.join(keys)}")
    return value


def text(value, where):
    if type(value) is not str or not value.strip():
        raise InvalidEvidence(f"{where}: expected nonempty text")
    return value


def boolean(value, where):
    if type(value) is not bool:
        raise InvalidEvidence(f"{where}: expected boolean, not a truthy substitute")
    return value


def integer(value, where, minimum=0, maximum=10000):
    if type(value) is not int or not minimum <= value <= maximum:
        raise InvalidEvidence(f"{where}: expected integer in [{minimum}, {maximum}]")
    return value


def choice(value, values, where):
    if type(value) is not str or value not in values:
        raise InvalidEvidence(f"{where}: unsupported value; choose from {', '.join(values)}")
    return value


def array(value, where, minimum=0, maximum=10000):
    if type(value) is not list or not minimum <= len(value) <= maximum:
        raise InvalidEvidence(f"{where}: expected list with {minimum}..{maximum} items")
    return value


def digest(value, where):
    if type(value) is not str or not SHA256.fullmatch(value):
        raise InvalidEvidence(f"{where}: expected lowercase SHA-256")


def check(value, where, reasons):
    obj(value, ("status", "evidence"), where)
    choice(value["status"], ("pass", "fail", "unknown"), where + ".status")
    text(value["evidence"], where + ".evidence")
    if value["status"] != "pass":
        reasons.append(f"{where}: not observed and checked as passing ({value['status']})")


def require_true(value, where, reasons):
    if not boolean(value, where):
        reasons.append(f"{where}: required verified condition is false")


def exact_sign_test(wins, losses):
    """One-sided P[X >= wins], X ~ Binomial(wins + losses, 1/2).

    Ties/unstable/invalid remain in effect-size denominators, not this
    conditional sign test. Fractions avoid rounding around the decision gate.
    """
    integer(wins, "wins")
    integer(losses, "losses")
    n = wins + losses
    return Fraction(sum(math.comb(n, k) for k in range(wins, n + 1)), 2 ** n)


def budget_check(value, reasons):
    keys = tuple(LIMITS) + ("paid_api", "new_subscription", "expansion_authorization",
                          "quota_or_auth_blocked", "rate_limited", "transport_failures")
    obj(value, keys, "budget")
    authorization = value["expansion_authorization"]
    if authorization is not None:
        text(authorization, "budget.expansion_authorization")
    for key, limit in LIMITS.items():
        if integer(value[key], "budget." + key) > limit and authorization is None:
            reasons.append(f"budget.{key}: exceeds default {limit} without explicit expansion authority")
    for key in ("paid_api", "new_subscription"):
        if boolean(value[key], "budget." + key) and authorization is None:
            reasons.append(f"budget.{key}: new cost requires explicit authority")
    for key in ("quota_or_auth_blocked", "rate_limited"):
        if boolean(value[key], "budget." + key):
            reasons.append(f"budget.{key}: stop; do not bypass the provider limit")
    if integer(value["transport_failures"], "budget.transport_failures") >= 2:
        reasons.append("budget.transport_failures: stop after two transport failures")


def common_evidence(value, extra_keys, reasons):
    obj(value, ("kind", "artifacts") + extra_keys, "evidence")
    choice(value["kind"], ("observed", "synthetic", "unsupported"), "evidence.kind")
    if value["kind"] != "observed":
        reasons.append("evidence.kind: only observed, reviewable evidence supports release review")
    for index, artifact in enumerate(array(value["artifacts"], "evidence.artifacts", 1)):
        where = f"evidence.artifacts[{index}]"
        obj(artifact, ("reference", "sha256"), where)
        text(artifact["reference"], where + ".reference")
        digest(artifact["sha256"], where + ".sha256")


def cell_key(value, where):
    language = choice(value["language"], ("zh", "en"), where + ".language")
    path = choice(value["path"], PATHS, where + ".path")
    return language, path


def protocol(value, style, reasons):
    flags = ("frozen_before_trials", "fixed_sample", "no_optional_stopping",
             "source_level_units", "settings_identical")
    if style:
        flags += ("fresh_heldout", "anonymous", "swapped_order", "judge_independent")
    keys = ("reference", "policy_version", "candidate_sha256", "incumbent_sha256", "cells") + flags
    if style:
        keys += ("judge_type", "judge_identity", "independence_evidence")
    obj(value, keys, "protocol")
    text(value["reference"], "protocol.reference")
    if value["policy_version"] != POLICY_VERSION:
        raise InvalidEvidence("protocol.policy_version: unsupported or changed policy")
    for key in ("candidate_sha256", "incumbent_sha256"):
        digest(value[key], "protocol." + key)
    if value["candidate_sha256"] == value["incumbent_sha256"]:
        reasons.append("protocol: candidate and incumbent snapshots are identical")
    for flag in flags:
        require_true(value[flag], "protocol." + flag, reasons)
    if style:
        choice(value["judge_type"], ("independent_human", "independent_model_family", "same_model"),
               "protocol.judge_type")
        text(value["judge_identity"], "protocol.judge_identity")
        text(value["independence_evidence"], "protocol.independence_evidence")
        if value["judge_type"] == "same_model":
            reasons.append("protocol.judge_type: same-model judging is exploratory, not general-advantage evidence")
    planned = {}
    for cell in array(value["cells"], "protocol.cells", 1, 6):
        obj(cell, ("language", "path", "source_ids"), "protocol.cell")
        key = cell_key(cell, "protocol.cell")
        if key in planned:
            raise InvalidEvidence("protocol.cells: duplicate language/path cell")
        ids = array(cell["source_ids"], "protocol.cell.source_ids", 1)
        for source in ids:
            text(source, "protocol.cell.source_id")
        if len(set(ids)) != len(ids):
            raise InvalidEvidence("protocol.cell.source_ids: duplicate source-level unit")
        planned[key] = ids
    return planned


def actual_cells(cells, planned):
    actual = {}
    for cell in array(cells, "evidence.cells", 0, 6):
        obj(cell, ("language", "path", "units"), "evidence.cell")
        key = cell_key(cell, "evidence.cell")
        if key not in planned or key in actual:
            raise InvalidEvidence("evidence.cells: unplanned or duplicate cell")
        units = {}
        for unit in array(cell["units"], "evidence.cell.units"):
            if type(unit) is not dict:
                raise InvalidEvidence("evidence.unit: expected object")
            source = text(unit.get("source_id"), "evidence.unit.source_id")
            if source not in planned[key] or source in units:
                raise InvalidEvidence("evidence.units: unplanned or duplicate source-level unit")
            units[source] = unit
        actual[key] = units
    return actual


def observation(value, style, where, reasons):
    keys = ("normal", "swapped") if style else ("result",)
    obj(value, keys + ("candidate_fidelity", "privacy", "fidelity_dispute", "critical_issue"), where)
    for key in ("candidate_fidelity", "privacy"):
        state = choice(value[key], ("pass", "fail", "unknown"), where + "." + key)
        if state != "pass":
            reasons.append(f"{where}.{key}: {state}; a hard protection is not passing")
    for key in ("fidelity_dispute", "critical_issue"):
        if boolean(value[key], where + "." + key):
            reasons.append(f"{where}.{key}: unresolved/critical issue blocks eligibility")
    values = []
    for key in keys:
        allowed = ("win", "loss", "tie", "invalid") if style else ("pass", "fail", "invalid")
        values.append(choice(value[key], allowed, where + "." + key))
    return values


def style_evidence(evidence, reasons):
    common_evidence(evidence, ("protocol", "cells"), reasons)
    planned = protocol(evidence["protocol"], True, reasons)
    actual = actual_cells(evidence["cells"], planned)
    # The registered family includes every cell AND both controls, even if
    # results are absent or unfavorable. There is no caller-supplied K.
    family_size = 2 * len(planned)
    alpha = Fraction(1, 20 * family_size)
    metrics = []
    for key, sources in planned.items():
        n = len(sources)
        counts = {control: dict.fromkeys(("win", "loss", "tie", "unstable", "invalid"), 0)
                  for control in ("incumbent", "plain")}
        for source in sources:
            unit = actual.get(key, {}).get(source)
            if unit is None:
                for count in counts.values():
                    count["invalid"] += 1
                continue
            obj(unit, ("source_id", "comparisons"), "style.unit")
            obj(unit["comparisons"], ("incumbent", "plain"), "style.comparisons")
            for control, count in counts.items():
                votes = []
                for repeat, result in enumerate(array(unit["comparisons"][control], "style.repeats", 2, 2), 1):
                    where = f"{key[0]}/{key[1]}/{source}/{control}/repeat-{repeat}"
                    votes += observation(result, True, where, reasons)
                outcome = "invalid" if "invalid" in votes else votes[0] if len(set(votes)) == 1 else "unstable"
                count[outcome] += 1
        for control, count in counts.items():
            net = Fraction(count["win"] - count["loss"], n)
            loss_rate = Fraction(count["loss"], n)
            unstable_rate = Fraction(count["unstable"] + count["invalid"], n)
            p_value = exact_sign_test(count["win"], count["loss"])
            label = "/".join(key) + "/" + control
            if n < 30:
                reasons.append(f"{label}: N={n} independent source units is below 30")
            if count["invalid"]:
                reasons.append(f"{label}: {count['invalid']} invalid/missing units remain in N; incomplete evidence")
            if net < Fraction(15, 100):
                reasons.append(f"{label}: net preference below 0.15")
            if loss_rate > Fraction(1, 10):
                reasons.append(f"{label}: loss rate above 0.10")
            if unstable_rate > Fraction(1, 10):
                reasons.append(f"{label}: unstable/invalid rate above 0.10")
            if p_value > alpha:
                reasons.append(f"{label}: exact one-sided sign test exceeds 0.05/{family_size}")
            metrics.append({"language": key[0], "path": key[1], "control": control,
                            "N": n, **count, "net_preference": float(net),
                            "loss_rate": float(loss_rate), "unstable_rate": float(unstable_rate),
                            "sign_test_p": float(p_value), "family_size": family_size,
                            "adjusted_alpha": float(alpha)})
    return metrics


def bugfix_evidence(evidence, reasons):
    common_evidence(evidence, ("protocol", "cells"), reasons)
    planned = protocol(evidence["protocol"], False, reasons)
    actual = actual_cells(evidence["cells"], planned)
    guards, originals, metrics = set(), 0, []
    source_roles = {}
    for key, sources in planned.items():
        local_guards, failures, missing = set(), 0, 0
        for source in sources:
            unit = actual.get(key, {}).get(source)
            if unit is None:
                missing += 1
                continue
            obj(unit, ("source_id", "role", "unseen", "incumbent_reproduced", "repeats"), "bugfix.unit")
            role = choice(unit["role"], ("original", "guard"), "bugfix.role")
            unseen = boolean(unit["unseen"], "bugfix.unseen")
            baseline = array(unit["incumbent_reproduced"], "bugfix.incumbent_reproduced", 2, 2)
            for outcome in baseline:
                boolean(outcome, "bugfix.incumbent_reproduced[]")
            if source in source_roles and source_roles[source] != role:
                raise InvalidEvidence("bugfix: original source cannot be relabeled as an unseen guard")
            source_roles[source] = role
            if role == "original":
                originals += 1
                if baseline != [True, True]:
                    reasons.append(f"{source}: original failure not reproduced in both incumbent repeats")
            else:
                if not unseen:
                    reasons.append(f"{source}: guard was not unseen before the frozen candidate")
                guards.add(source)
                local_guards.add(source)
            for repeat, result in enumerate(array(unit["repeats"], "bugfix.repeats", 2, 2), 1):
                where = f"{key[0]}/{key[1]}/{source}/repeat-{repeat}"
                if observation(result, False, where, reasons) != ["pass"]:
                    failures += 1
        if missing:
            reasons.append(f"{'/'.join(key)}: {missing} planned units missing; no exclusions allowed")
        if failures:
            reasons.append(f"{'/'.join(key)}: {failures} observed failing/invalid repeats")
        minimum = 12 if len(planned) == 1 else 6
        if len(local_guards) < minimum:
            reasons.append(f"{'/'.join(key)}: fewer than {minimum} unseen source-level guards")
        metrics.append({"language": key[0], "path": key[1], "N": len(sources),
                        "guards": len(local_guards), "failing_repeats": failures, "missing": missing})
    if originals == 0:
        reasons.append("bugfix: original reproduction case is missing")
    if len(guards) < 12:
        reasons.append("bugfix: fewer than 12 distinct unseen guard sources overall")
    return metrics


def assess(record):
    """Return a decision without mutating input or performing external actions."""
    reasons, metrics = [], []
    result = {"policy_version": POLICY_VERSION, "decision": "reject", "reasons": reasons,
              "metrics": metrics, "automatic_publish": False,
              "limitation": "Reported evidence is not authenticated by this offline tool; eligibility is not proof or publication authority."}
    try:
        obj(record, ("schema_version", "synthetic", "tier", "candidate", "claim", "screening",
                     "checks", "review", "budget", "evidence"), "record")
        if type(record["schema_version"]) is not int or record["schema_version"] != 1:
            raise InvalidEvidence("schema_version: unsupported version")
        example = boolean(record["synthetic"], "synthetic")
        tier = choice(record["tier"], TIERS, "tier")
        result["tier"] = tier
        result["candidate"] = text(record["candidate"], "candidate")
        expected_claim = {"screening": "none", "docs_structure": "none",
                          "targeted_bugfix": "targeted_fix", "style_improvement": "general_style_advantage"}[tier]
        if record["claim"] != expected_claim:
            raise InvalidEvidence(f"claim: {tier} supports only {expected_claim}; personal-voice claims need actual user feedback")
        obj(record["screening"], SCORES, "screening")
        score = 0
        for key in SCORES:
            part = obj(record["screening"][key], ("score", "rationale"), "screening." + key)
            score += integer(part["score"], "screening." + key + ".score", 0, 2)
            text(part["rationale"], "screening." + key + ".rationale")
        result["screening_score"] = score
        required_checks = COMMON_CHECKS if tier == "screening" else RELEASE_CHECKS
        obj(record["checks"], required_checks, "checks")
        for name in required_checks:
            check(record["checks"][name], "checks." + name, reasons)
        budget_check(record["budget"], reasons)
        veto = any(record["checks"][name]["status"] == "fail" for name in ("license", "security"))
        if score < 7:
            reasons.append("screening: score below 7/10; defer investigation")
        if tier == "screening":
            if record["review"] is not None or record["evidence"] is not None:
                raise InvalidEvidence("screening: review and evidence must be null; use a release tier for evidence")
        else:
            review = obj(record["review"], ("reviewer", "independent_of_author", "evidence"), "review")
            text(review["reviewer"], "review.reviewer")
            text(review["evidence"], "review.evidence")
            require_true(review["independent_of_author"], "review.independent_of_author", reasons)
            if tier == "docs_structure":
                common_evidence(record["evidence"], ("behavior_unchanged", "structure_checks_passed"), reasons)
                for key in ("behavior_unchanged", "structure_checks_passed"):
                    require_true(record["evidence"][key], "evidence." + key, reasons)
            elif tier == "targeted_bugfix":
                metrics.extend(bugfix_evidence(record["evidence"], reasons))
            else:
                metrics.extend(style_evidence(record["evidence"], reasons))
        if example:
            reasons.append("synthetic: demonstration/fixture is not empirical evidence and cannot qualify")
        if veto or example:
            result["decision"] = "reject"
        elif reasons:
            result["decision"] = "defer"
        else:
            result["decision"] = "investigate" if tier == "screening" else "eligible_for_release_review"
            reasons.append("Screening heuristic only; not a release or improvement claim." if tier == "screening"
                           else "Recorded criteria met; independently verify artifacts and scope before publishing under existing authority.")
    except InvalidEvidence as error:
        result["decision"] = "reject"
        reasons.append(str(error))
    return result


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidEvidence(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="JSON evidence record; read-only, no network or inference")
    args = parser.parse_args(argv)
    try:
        data = args.evidence.read_bytes()
        if len(data) > 5 * 1024 * 1024:
            raise InvalidEvidence("evidence exceeds 5 MiB; use source-level summaries, not private raw text")
        record = json.loads(data, object_pairs_hook=no_duplicate_keys,
                            parse_constant=lambda value: (_ for _ in ()).throw(InvalidEvidence("nonfinite JSON number: " + value)))
        result = assess(record)
        result["input_sha256"] = hashlib.sha256(data).hexdigest()
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        result = {"policy_version": POLICY_VERSION, "decision": "reject", "reasons": [str(error)],
                  "metrics": [], "automatic_publish": False}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["decision"] == "eligible_for_release_review" else 2 if result["decision"] == "reject" else 1


if __name__ == "__main__":
    raise SystemExit(main())
