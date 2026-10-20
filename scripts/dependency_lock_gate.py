#!/usr/bin/env python3
"""Fail closed on an unpinned Lean/Mathlib manifest (static gate only).

A passing check is not evidence that a GitHub Actions run invoked this gate.
"""
import json
import re
import sys
import tomllib
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")
TOOLCHAIN = re.compile(r"leanprover/lean4:v\d+\.\d+\.\d+(?:-rc\d+)?\Z")
MATHLIB_V424_SHA = "f897ebcf72cd16f89ab4577d0c826cd14afaafc7"


def check(root: Path):
    tc = (root / "lean-toolchain").read_text(encoding="utf-8").strip()
    if not TOOLCHAIN.fullmatch(tc):
        raise ValueError("lean-toolchain is not an exact Lean 4 release")
    with (root / "lakefile.toml").open("rb") as handle:
        lake = tomllib.load(handle)
    requirements = [p for p in lake.get("require", []) if p.get("name") == "mathlib"]
    if len(requirements) != 1:
        raise ValueError("expected exactly one Mathlib requirement")
    requirement = requirements[0]
    if requirement.get("scope") != "leanprover-community":
        raise ValueError("unexpected Mathlib source scope")
    if requirement.get("rev") != "v4.24.0" or tc != "leanprover/lean4:v4.24.0":
        raise ValueError("Lean/Mathlib version mismatch with audited v4.24.0 lock")
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
    mathlib = next((p for p in packages if p["name"] == "mathlib"), None)
    if mathlib is None:
        raise ValueError("Mathlib not pinned")
    if (mathlib.get("rev") != MATHLIB_V424_SHA or
        mathlib.get("inputRev") != "v4.24.0" or
        mathlib.get("url") != "https://github.com/leanprover-community/mathlib4" or
        mathlib.get("inherited") is not False):
        raise ValueError("Mathlib manifest differs from audited v4.24.0 pin")
    return tc, len(names)


if __name__ == "__main__":
    try:
        toolchain, count = check(Path.cwd())
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"DEPENDENCY LOCK FAIL: {error}", file=sys.stderr)
        sys.exit(1)
    print(f"DEPENDENCY LOCK PASS: {toolchain}, {count} packages")
