#!/usr/bin/env python3
"""
Muse Video Skill — inventory.py
Dynamic file registry — replaces static metadata/registry.yaml.

Usage:
  python scripts/inventory.py                    # summary by role
  python scripts/inventory.py --json             # full JSON output
  python scripts/inventory.py --deps <file>      # find upstream/downstream references
  python scripts/inventory.py --list-roles       # list discovered roles
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

VERSION = "0.1.0"

SCAN_DIRS = ["references", "scripts", "assets", "metadata"]
SKIP_PATTERNS = ["__pycache__", "*.pyc", ".git", "INDEX.md.bak", "*.bak"]


def scan_files(skill_root: Path) -> dict[str, list[dict]]:
    """Scan all tracked directories and classify files by role."""
    by_role: dict[str, list[dict]] = defaultdict(list)

    for dir_name in SCAN_DIRS:
        dir_path = skill_root / dir_name
        if not dir_path.exists():
            continue
        for fpath in sorted(dir_path.rglob("*")):
            if not fpath.is_file():
                continue
            # Skip patterns
            if any(fpath.match(p) for p in SKIP_PATTERNS):
                continue

            rel = fpath.relative_to(skill_root)
            role = classify_role(rel)
            entry = {
                "path": str(rel).replace("\\", "/"),
                "size": fpath.stat().st_size,
                "role": role,
            }
            by_role[role].append(entry)

    return dict(by_role)


def classify_role(rel_path: Path) -> str:
    """Classify a file by its directory prefix."""
    p = str(rel_path).replace("\\", "/")
    if p.startswith("references/roles/"):
        # Extract role name from filename
        name = rel_path.stem
        return name
    if p.startswith("references/scenes/"):
        return "scene"
    if p.startswith("references/cases/"):
        return "case"
    if p.startswith("references/pipelines/"):
        return "pipeline"
    if p.startswith("references/media/"):
        return "media"
    if p.startswith("scripts/"):
        return "script"
    if p.startswith("assets/"):
        return "asset"
    if p.startswith("metadata/"):
        return "metadata"
    return "other"


def find_deps(skill_root: Path, target_file: str) -> dict:
    """Find files that reference `target_file` and files that `target_file` references."""
    target = target_file.replace("\\", "/")
    upstream = []   # files that reference target
    downstream = []  # files that target references

    target_path = skill_root / target_file
    if target_path.exists():
        try:
            content = target_path.read_text(encoding="utf-8")
            # Find markdown links and file references in target
            refs = set(re.findall(r'`([^`]+\.(?:md|py|yaml|json))`', content))
            refs.update(re.findall(r'\[.*?\]\(([^)]+)\)', content))
            downstream = sorted(refs)
        except Exception:
            pass

    # Find files that reference the target
    for dir_name in SCAN_DIRS:
        dir_path = skill_root / dir_name
        if not dir_path.exists():
            continue
        for fpath in dir_path.rglob("*"):
            if not fpath.is_file():
                continue
            if any(fpath.match(p) for p in SKIP_PATTERNS):
                continue
            if fpath == target_path:
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
                if target_file in content or target in content:
                    upstream.append(str(fpath.relative_to(skill_root)).replace("\\", "/"))
            except Exception:
                pass

    return {
        "target": target_file,
        "upstream": sorted(upstream),
        "downstream": downstream,
    }


def main():
    parser = argparse.ArgumentParser(description="Muse Video Skill — Dynamic file inventory")
    parser.add_argument("--json", action="store_true", help="Full JSON output")
    parser.add_argument("--deps", type=str, metavar="FILE", help="Find deps for FILE")
    parser.add_argument("--list-roles", action="store_true", help="List discovered roles")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent

    if args.deps:
        result = find_deps(skill_root, args.deps)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    inventory = scan_files(skill_root)

    if args.list_roles:
        for role in sorted(inventory.keys()):
            print(role)
        return

    if args.json:
        print(json.dumps(inventory, indent=2, ensure_ascii=False))
        return

    # Default: summary
    total = sum(len(files) for files in inventory.values())
    print(f"Muse Video Skill — File Inventory (v{VERSION})")
    print(f"  Root: {skill_root}")
    print(f"  Total files: {total}")
    print()
    for role in sorted(inventory.keys()):
        files = inventory[role]
        print(f"  [{role}] ({len(files)} files)")
        for f in files:
            print(f"    {f['path']}  ({f['size']:,} bytes)")


if __name__ == "__main__":
    main()
