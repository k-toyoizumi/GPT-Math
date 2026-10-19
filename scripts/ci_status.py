#!/usr/bin/env python3
"""Summarize mandatory CI stage outcomes; diagnostics never mask job failure."""
import argparse
import csv
import json
import os
from pathlib import Path

STAGES = ("inventory", "python", "toolchain", "dependencies", "lean")
VALID = {"success", "failure", "skipped", "cancelled", "unknown"}
CATEGORIES = {
    "inventory": "proof_inventory_or_gate",
    "python": "python_reproduction_or_unit_tests",
    "toolchain": "lean_toolchain_installation",
    "dependencies": "lean_dependency_or_cache",
    "lean": "lean_compilation_or_proof",
}

def summarize(outcomes):
    if set(outcomes) != set(STAGES) or any(v not in VALID for v in outcomes.values()):
        raise ValueError("missing or invalid CI stage outcome")
    failures = [k for k in STAGES if outcomes[k] == "failure"]
    cancelled = [k for k in STAGES if outcomes[k] == "cancelled"]
    skipped = [k for k in STAGES if outcomes[k] in ("skipped", "unknown")]
    first = next(iter(failures or cancelled or skipped), None)
    category = ("success" if first is None else
                CATEGORIES[first] if first in failures else
                "cancelled_" + first if first in cancelled else
                "not_executed_" + first)
    return {
        "schema_version": 1,
        "all_pass": all(v == "success" for v in outcomes.values()),
        "primary_category": category,
        "failed_stages": failures,
        "cancelled_stages": cancelled,
        "skipped_or_unknown_stages": skipped,
        "step_outcomes": outcomes,
        "commit_sha": os.environ.get("GITHUB_SHA", "local-not-actions"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "scope": "CI step classification only; not a mathematical proof",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("ci-artifacts"))
    for stage in STAGES:
        parser.add_argument("--" + stage, choices=sorted(VALID), required=True)
    args = parser.parse_args()
    outcomes = {stage: getattr(args, stage) for stage in STAGES}
    report = summarize(outcomes)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "ci-status.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (args.out / "ci-status.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["stage", "outcome", "category"])
        for stage in STAGES:
            writer.writerow([stage, outcomes[stage], CATEGORIES[stage]])
    print("CI STATUS:", "PASS" if report["all_pass"] else "FAIL", report["primary_category"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
