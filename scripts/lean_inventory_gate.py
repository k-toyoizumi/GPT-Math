#!/usr/bin/env python3
"""Fail CI if tracked Lean files are omitted from Lake targets or contain proof holes.

The textual scan is only a guardrail, not a kernel axiom-dependency audit.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys
import tomllib

FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom)\b")

def code_only(source: str) -> str:
    """Blank nested Lean comments and ordinary string literals."""
    out = []
    i, n, depth = 0, len(source), 0
    while i < n:
        two = source[i:i + 2]
        if depth:
            if two == "/-":
                depth += 1
                out.extend("  ")
                i += 2
            elif two == "-/":
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif two == "/-":
            depth = 1
            out.extend("  ")
            i += 2
        elif two == "--":
            j = source.find("\n", i)
            if j < 0:
                out.extend(" " * (n - i))
                i = n
            else:
                out.extend(" " * (j - i))
                i = j
        elif source[i] == '"':
            out.append(" ")
            i += 1
            while i < n:
                if source[i] == "\\" and i + 1 < n:
                    out.extend("  ")
                    i += 2
                elif source[i] == '"':
                    out.append(" ")
                    i += 1
                    break
                else:
                    out.append("\n" if source[i] == "\n" else " ")
                    i += 1
        else:
            out.append(source[i])
            i += 1
    if depth:
        raise ValueError("unterminated Lean block comment")
    return "".join(out)

def check(repo: Path):
    with (repo / "lakefile.toml").open("rb") as f:
        config = tomllib.load(f)
    libs = [x["name"] for x in config.get("lean_lib", [])]
    if not libs or len(libs) != len(set(libs)):
        raise ValueError("missing or duplicate Lean library targets")
    raw = subprocess.check_output(["git", "ls-files", "-z", "--", "*.lean"], cwd=repo)
    files = sorted(Path(x.decode("utf-8")) for x in raw.split(b"\0") if x)
    modules = [(".".join(p.with_suffix("").parts), p) for p in files]
    names = [m for m, _ in modules]
    if not names or len(names) != len(set(names)):
        raise ValueError("missing or duplicate Lean sources")
    if set(names) != set(libs):
        raise ValueError(f"Lean inventory mismatch: unregistered={sorted(set(names)-set(libs))}; missing_source={sorted(set(libs)-set(names))}")
    native = []
    for module, path in modules:
        code = code_only((repo / path).read_text(encoding="utf-8"))
        marker = FORBIDDEN.search(code)
        if marker:
            raise ValueError(f"forbidden Lean token {marker.group()!r} in {path}")
        if re.search(r"\bnative_decide\b", code):
            native.append(module)
    return names, native

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", action="store_true")
    args = parser.parse_args()
    try:
        modules, native = check(Path.cwd())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"Lean inventory FAIL: {exc}", file=sys.stderr)
        return 1
    if args.targets:
        print(" ".join(modules))
    else:
        print(f"Lean inventory PASS: {len(modules)} tracked modules")
        print("native_decide modules (compiler trust; not kernel-only):", ", ".join(native) or "none")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
