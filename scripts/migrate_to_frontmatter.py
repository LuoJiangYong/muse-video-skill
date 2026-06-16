#!/usr/bin/env python3
"""
Muse Video Skill — migrate_to_frontmatter.py (ONE-TIME USE)

Parse existing case files (pre-frontmatter format) and insert YAML frontmatter
at the beginning of each file. Run once to migrate all 38 cases, then this
script is no longer needed.

Usage:
  python scripts/migrate_to_frontmatter.py --dry-run     # preview without writing
  python scripts/migrate_to_frontmatter.py --write        # actually modify files
  python scripts/migrate_to_frontmatter.py --file BR2049.md  # migrate single file
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

# ─── Constants ────────────────────────────────────────────────────────────────

# Mapping from Chinese role labels in 技法标签 to English role keys
ROLE_MAP = {
    "叙事": "narrative",
    "镜头": "cinematography",
    "色彩": "color",
    "特效": "vfx",
    "声音": "sound",
    "创意策略": "creative",
    "广告创意": "creative",
    "创意": "creative",
    "美术": "color",  # sometimes 色彩 is labeled as 美术
}

# Order of roles in frontmatter output
ROLE_ORDER = ["narrative", "cinematography", "color", "vfx", "sound", "creative"]


def parse_meta_table(content: str) -> dict:
    """Parse the 元信息 markdown table. Returns dict of field→value."""
    meta = {}

    # Find 元信息 section
    meta_match = re.search(r'## 元信息\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    if not meta_match:
        return meta

    table_text = meta_match.group(1)

    # Parse pipe-delimited rows
    for line in table_text.split("\n"):
        # Match | field | value |
        m = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            if key and val and not key.startswith("--") and not key.startswith("字段"):
                meta[key] = val

    return meta


def parse_technique_tags(content: str) -> dict:
    """Parse the 技法标签 section. Returns dict of role→[techniques]."""
    techniques = {}

    # Find 技法标签 section
    tech_match = re.search(r'## 技法标签\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    if not tech_match:
        return techniques

    section = tech_match.group(1)

    # Parse bullet list: - **角色**：技法1, 技法2, 技法3
    for line in section.split("\n"):
        line = line.strip()
        # Match: - **叙事**：LOGO=角色IP, 无对白微叙事
        m = re.match(r'-\s*\*\*(.+?)\*\*\s*[：:]\s*(.+)', line)
        if m:
            role_label = m.group(1).strip()
            tech_str = m.group(2).strip()

            # Map Chinese role label to English key
            role_key = ROLE_MAP.get(role_label)
            if not role_key:
                # Try partial match
                for label, key in ROLE_MAP.items():
                    if label in role_label:
                        role_key = key
                        break
            if not role_key:
                continue

            # Split techniques by comma
            techs = [t.strip() for t in tech_str.split(",") if t.strip()]
            # Remove parenthetical descriptions like "（看向镜头）"
            techs_clean = []
            for t in techs:
                # Strip Chinese parentheses and their content
                t = re.sub(r'[（(][^）)]*[）)]', '', t).strip()
                if t:
                    techs_clean.append(t)

            if techs_clean:
                techniques[role_key] = techs_clean

    return techniques


def parse_keywords(meta: dict) -> list[str]:
    """Extract keywords/tags from meta dict."""
    kw = meta.get("关键词", "")
    if kw:
        return [k.strip() for k in kw.split(",") if k.strip()]
    return []


def extract_case_id_from_title(content: str) -> str:
    """Extract case ID from the first # heading."""
    m = re.match(r'^#\s*(\S+)', content)
    if m:
        return m.group(1)
    return ""


def migrate_file(filepath: Path, dry_run: bool = False) -> bool:
    """Migrate a single case file. Returns True if migration was needed."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has frontmatter
    if content.startswith("---"):
        print(f"  ⊘ {filepath.name}: already has frontmatter, skipping")
        return False

    # Parse sections
    meta = parse_meta_table(content)
    techniques = parse_technique_tags(content)

    if not meta:
        print(f"  ✗ {filepath.name}: could not parse 元信息 table")
        return False

    # Build frontmatter data
    case_id = meta.get("ID", "") or extract_case_id_from_title(content)
    name = meta.get("名称", case_id)
    case_type = meta.get("类型", "")
    year = meta.get("年份", "")
    director = meta.get("导演/工作室", "—")
    primary_scene = meta.get("主场景", "")
    secondary_scene = meta.get("辅场景", "")
    tags = parse_keywords(meta)

    # Organize techniques in role order
    fm_techniques = {}
    for role in ROLE_ORDER:
        if role in techniques:
            fm_techniques[role] = techniques[role]
        else:
            fm_techniques[role] = []

    fm = {
        "id": case_id,
        "name": name,
        "type": case_type,
        "year": year,
        "director": director,
        "primary_scene": primary_scene,
        "secondary_scene": secondary_scene,
        "tags": tags,
        "techniques": fm_techniques,
        "styles": [],
        "scene_relations": {
            "extra_strong": [],
            "extra_reference": [],
        },
    }

    # Generate YAML frontmatter block
    yaml_str = yaml.dump(
        fm, allow_unicode=True, default_flow_style=False, sort_keys=False,
        width=120,
    )
    frontmatter = f"---\n{yaml_str}---\n\n"

    # Insert frontmatter after the first # heading line
    # Find first heading
    heading_match = re.match(r'(^# .*\n)', content)
    if heading_match:
        new_content = heading_match.group(1) + frontmatter + content[heading_match.end():]
    else:
        new_content = frontmatter + content

    if dry_run:
        print(f"  ✓ {filepath.name}: would add frontmatter ({len(yaml_str)} chars)")
        # Show techniques found
        for role, techs in fm_techniques.items():
            if techs:
                print(f"      {role}: {len(techs)} techniques")
        return True

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    tech_count = sum(len(t) for t in fm_techniques.values())
    print(f"  ✓ {filepath.name}: added frontmatter | {len(fm_techniques)} roles, {tech_count} techniques, {len(tags)} tags")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate existing case files to YAML frontmatter format (one-time use)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--write", action="store_true", help="Actually modify files")
    parser.add_argument("--file", type=str, help="Migrate a single file (e.g., BR2049.md)")
    parser.add_argument("--cases-dir", type=str, default=None, help="Path to references/cases/")
    args = parser.parse_args()

    if not args.dry_run and not args.write:
        print("ERROR: Specify --dry-run or --write", file=sys.stderr)
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    cases_dir = Path(args.cases_dir) if args.cases_dir else (skill_root / "references" / "cases")

    if args.file:
        filepath = cases_dir / args.file
        if not filepath.exists():
            print(f"ERROR: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        files = [filepath]
    else:
        files = sorted(cases_dir.glob("*.md"))
        # Filter out template and index
        files = [f for f in files if not f.name.startswith("_") and f.name != "INDEX.md"]

    print(f"{'DRY RUN' if args.dry_run else 'WRITING'}: {len(files)} files in {cases_dir}")
    print()

    migrated = 0
    skipped = 0
    for f in files:
        try:
            if migrate_file(f, dry_run=args.dry_run):
                migrated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ✗ {f.name}: ERROR: {e}")

    print(f"\nDone: {migrated} migrated, {skipped} skipped, {len(files)} total")


if __name__ == "__main__":
    main()
