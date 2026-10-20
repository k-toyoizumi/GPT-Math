#!/usr/bin/env python3
"""Inventory tracked Lean sources and declared Lake libraries; fail closed."""
import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path


def inventory(root: Path):
    root = root.resolve()
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", "*.lean"],
        capture_output=True, check=True,
    )
    paths = sorted(Path(p.decode("utf-8")) for p in proc.stdout.split(b"\0") if p)
    if not paths:
        raise ValueError("No tracked Lean files: refusing vacuous CI success")
    if any(p.is_absolute() or ".." in p.parts or not (root / p).is_file() for p in paths):
        raise ValueError("Tracked Lean path missing or unsafe")
    with (root / "lakefile.toml").open("rb") as f:
        config = tomllib.load(f)
    targets = [entry["name"] for entry in config.get("lean_lib", [])]
    if not targets or len(targets) != len(set(targets)):
        raise ValueError("Missing or duplicate [[lean_lib]] targets")
    missing = [name for name in targets if Path(name.replace(".", "/") + ".lean") not in paths]
    if missing:
        raise ValueError("Lake target has no tracked Lean source: " + ", ".join(missing))
    registry = json.loads((root / "lean-sources.json").read_text())
    if set(registry) != {p.as_posix() for p in paths}:
        raise ValueError("tracked Lean sources differ from explicit registry")
    adopted = []
    for path, entry in registry.items():
        if entry["status"] == "adopted":
            if entry["target"] not in targets:
                raise ValueError("adopted source has no build target")
            adopted.append(entry["target"])
        elif entry["status"] not in ("draft", "excluded") or not entry.get("reason"):
            raise ValueError("invalid source classification")
    if set(config.get("defaultTargets", [])) != set(adopted):
        raise ValueError("defaultTargets differ from adopted targets")
    return [p.as_posix() for p in paths], adopted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--files", action="store_true")
    group.add_argument("--targets", action="store_true")
    args = parser.parse_args()
    try:
        files, targets = inventory(args.root)
    except (OSError, subprocess.CalledProcessError, ValueError, tomllib.TOMLDecodeError) as e:
        print(f"LEAN_INVENTORY_FAILURE: {e}", file=sys.stderr)
        return 1
    if args.files:
        print("\n".join(files))
    elif args.targets:
        print(" ".join(targets))
    else:
        print(json.dumps({"tracked_lean_files": files, "lake_targets": targets, "file_count": len(files)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
