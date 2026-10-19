#!/usr/bin/env python3
"""Reject unpinned Lean/Mathlib dependencies before running Lake.

A passing static check is NOT evidence that Actions used the lockfile.
"""
import json
import re
import sys
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")
TOOLCHAIN = re.compile(r"leanprover/lean4:v\d+\.\d+\.\d+(?:-rc\d+)?\Z")


def check(root: Path):
    tc = (root / "lean-toolchain").read_text(encoding="utf-8").strip()
    if not TOOLCHAIN.fullmatch(tc):
        raise ValueError("lean-toolchain is not an exact Lean 4 release")
    path = root / "lake-manifest.json"
    if not path.is_file():
        raise ValueError("missing lake-manifest.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    packages = data.get("packages")
    if not isinstance(packages, list) or not packages:
        raise ValueError("missing manifest packages")
    names = []
    for package in packages:
        if not isinstance(package, dict):
            raise ValueError("invalid package")
        name, rev = package.get("name"), package.get("rev")
        if not isinstance(name, str) or not name:
            raise ValueError("missing package name")
        if not isinstance(rev, str) or not SHA.fullmatch(rev):
            raise ValueError(f"{name}: dependency revision is not a 40-digit SHA")
        names.append(name)
    if len(set(names)) != len(names):
        raise ValueError("duplicate dependency names")
    if "mathlib" not in names:
        raise ValueError("Mathlib not pinned")
    return tc, len(names)


if __name__ == "__main__":
    try:
        toolchain, count = check(Path.cwd())
    except (OSError, ValueError, TypeError) as error:
        print(f"DEPENDENCY LOCK FAIL: {error}", file=sys.stderr)
        sys.exit(1)
    print(f"DEPENDENCY LOCK PASS: {toolchain}, {count} packages")
