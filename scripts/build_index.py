#!/usr/bin/env python3
"""
Muse Video Skill — build_index.py
Automatically generate references/cases/INDEX.md from case file YAML frontmatter.

Usage:
  python scripts/build_index.py --check       # validate only, exit 1 on errors
  python scripts/build_index.py --write       # validate + write INDEX.md
  python scripts/build_index.py --diff        # show diff without writing

All case files must have YAML frontmatter (delimited by ---) with:
  id, name, type, year, director, primary_scene, secondary_scene, tags,
  techniques: {narrative, cinematography, color, vfx, sound, creative},
  styles: [...],
  scene_relations: {extra_strong: [...], extra_reference: [...]}
"""

import argparse
import os
import re
import sys
import textwrap
from collections import defaultdict
from datetime import datetime, timezone
from dataclasses import dataclass, field
from difflib import unified_diff
from pathlib import Path
from typing import Optional

import yaml

VERSION = "0.1.0"

# ─── Constants ────────────────────────────────────────────────────────────────

CASE_TYPES = [
    "film", "commercial", "short-film", "music-video",
    "animation", "documentary", "experimental", "logo-animation",
]

SCENE_TYPES = ["studio-ad", "logo-animation", "product-demo", "sci-fi", "custom"]

ROLE_LABELS = {
    "narrative": ("叙事技法", "Writer"),
    "cinematography": ("镜头语言", "DP"),
    "color": ("色彩/美术", "Art Director"),
    "vfx": ("特效语言", "VFX Supervisor"),
    "sound": ("声音设计", "Sound Designer"),
    "creative": ("创意广告专属", "Studio-Ad, Product-Demo"),
}

TYPE_ENUM_TABLE = """### 类型枚举

| 缩写 | 含义 | 典型特征 |
|------|------|---------|
| film | 电影 | 完整叙事弧线，2h±，多场次 |
| commercial | 广告片 | 短时长(15s-3min)，品牌目标，强记忆点 |
| short-film | 短片 | 15min±，完整故事，常有实验性 |
| music-video | MV | 音乐驱动，视觉节奏优先 |
| experimental | 实验影像 | 打破常规，技法探索，非叙事 |
| animation | 动画 | 全CG/手绘/定格 |
| documentary | 纪录片 | 真实素材，访谈，档案 |
| logo-animation | LOGO动画 | 品牌标识演绎，动态图形，短时长(5s-90s)"""


# ─── Data model ───────────────────────────────────────────────────────────────

@dataclass
class Case:
    id: str
    name: str
    type: str
    year: str
    director: str
    primary_scene: str
    secondary_scene: str
    tags: list = field(default_factory=list)
    techniques: dict = field(default_factory=dict)
    styles: list = field(default_factory=list)
    scene_relations: dict = field(default_factory=dict)

    @classmethod
    def from_frontmatter(cls, fm: dict, case_id: str) -> "Case":
        techniques = fm.get("techniques", {})
        scene_relations = fm.get("scene_relations", {})

        # Derive base scene relations from primary/secondary
        primary = fm.get("primary_scene", "")
        secondary = fm.get("secondary_scene", "")

        strong = [primary] if primary else []
        reference = [secondary] if secondary else []

        # Merge extra relations (handle both [] and null)
        extra_strong = scene_relations.get("extra_strong") or []
        for s in extra_strong:
            if s and s not in strong:
                strong.append(s)
        extra_reference = scene_relations.get("extra_reference") or []
        for s in extra_reference:
                if s and s not in reference:
                    reference.append(s)

        return cls(
            id=case_id,
            name=fm.get("name", case_id),
            type=fm.get("type", ""),
            year=str(fm.get("year", "")),
            director=fm.get("director", "—"),
            primary_scene=primary,
            secondary_scene=secondary,
            tags=fm.get("tags", []),
            techniques=techniques,
            styles=fm.get("styles", []),
            scene_relations={"strong": strong, "reference": reference},
        )


# ─── Frontmatter parser ──────────────────────────────────────────────────────

def parse_frontmatter(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file. Returns None if no frontmatter found.

    Handles two formats:
    1. Frontmatter at the very start:   ---\n...\n---\n
    2. Frontmatter after title:        # Title\n---\n...\n---\n
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the first --- that opens a YAML block
    # Look for --- at position 0, or after a # heading line
    fm_start = -1
    for match in re.finditer(r'(?m)^---\s*$', content):
        pos = match.start()
        # Accept if it's at position 0 or preceded by a heading line
        if pos == 0:
            fm_start = pos
            break
        # Check if preceding line is a # heading
        before = content[:pos].rstrip()
        prev_line = before.split("\n")[-1] if before else ""
        if re.match(r'^# .+', prev_line):
            fm_start = pos
            break

    if fm_start == -1:
        return None

    # Find closing --- (must be on its own line, after fm_start)
    fm_open_end = content.index("\n", fm_start) + 1  # end of the opening --- line
    rest = content[fm_open_end:]
    close_match = re.search(r'(?m)^---\s*$', rest)
    if not close_match:
        return None

    close_pos = fm_open_end + close_match.start()
    yaml_str = content[fm_open_end:close_pos].strip()

    if not yaml_str:
        return None

    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        print(f"⚠ YAML parse error in {filepath.name}: {e}", file=sys.stderr)
        return None


# ─── Loader ───────────────────────────────────────────────────────────────────

def load_all_cases(cases_dir: Path) -> list[Case]:
    """Scan cases_dir for .md files and parse their frontmatter."""
    cases = []
    errors = []

    for filepath in sorted(cases_dir.glob("*.md")):
        # Skip template and index files
        if filepath.name.startswith("_") or filepath.name == "INDEX.md":
            continue

        fm = parse_frontmatter(filepath)
        if fm is None:
            errors.append(f"  ✗ {filepath.name}: no valid YAML frontmatter found")
            continue

        case_id = fm.get("id", "")
        if not case_id:
            errors.append(f"  ✗ {filepath.name}: missing 'id' in frontmatter")
            continue

        try:
            case = Case.from_frontmatter(fm, case_id)
            cases.append(case)
        except Exception as e:
            errors.append(f"  ✗ {filepath.name}: {e}")
            continue

    if errors:
        print("ERROR: Failed to load cases:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)

    return cases


# ─── Validator ────────────────────────────────────────────────────────────────

def validate(cases: list[Case]) -> tuple[list[str], list[str]]:
    """Validate all cases. Returns (errors, warnings)."""
    errors = []
    warnings = []

    # Check required fields
    for c in cases:
        if not c.type:
            errors.append(f"  ✗ {c.id}: missing 'type'")
        if not c.name:
            errors.append(f"  ✗ {c.id}: missing 'name'")
        if not c.primary_scene:
            errors.append(f"  ✗ {c.id}: missing 'primary_scene'")

    # Check duplicate IDs
    ids = [c.id for c in cases]
    dupes = [id for id in set(ids) if ids.count(id) > 1]
    for d in dupes:
        errors.append(f"  ✗ Duplicate case ID: '{d}'")

    # Collect all technique names for similarity checking
    all_techs: dict[str, list[str]] = defaultdict(list)
    for c in cases:
        for role, techs in c.techniques.items():
            for t in techs:
                t_clean = t.strip()
                if t_clean:
                    all_techs[t_clean].append(c.id)

    # Check for near-duplicate technique names
    tech_names = sorted(all_techs.keys())
    for i, t1 in enumerate(tech_names):
        for t2 in tech_names[i + 1 :]:
            # Simple heuristic: if one is a substring of the other, or edit distance <= 3
            if t1 in t2 or t2 in t1:
                warnings.append(
                    f"  ⚠ Technique name overlap: '{t1}' and '{t2}' — consider merging"
                )
            elif _edit_distance(t1, t2) <= 3 and len(t1) > 4 and len(t2) > 4:
                warnings.append(
                    f"  ⚠ Similar technique names: '{t1}' vs '{t2}' — "
                    f"may be duplicates"
                )

    # Check style name consistency (case-insensitive)
    all_styles: dict[str, str] = {}
    for c in cases:
        for s in c.styles:
            lower = s.lower().strip()
            if lower in all_styles and all_styles[lower] != s:
                warnings.append(
                    f"  ⚠ Style case mismatch: '{s}' in {c.id} vs "
                    f"'{all_styles[lower]}' elsewhere"
                )
            all_styles[lower] = s

    return errors, warnings


def _edit_distance(s1: str, s2: str) -> int:
    """Levenshtein distance (simple implementation)."""
    if len(s1) < len(s2):
        return _edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(
                curr[j] + 1,
                prev[j + 1] + 1,
                prev[j] + (0 if c1 == c2 else 1),
            ))
        prev = curr
    return prev[-1]


# ─── Markdown helpers ─────────────────────────────────────────────────────────

def md_table(headers: list[str], rows: list[list[str]]) -> str:
    """Generate a markdown table."""
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("------" for _ in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def sort_case_ids(case_ids: list[str], all_cases: list[Case]) -> list[str]:
    """Sort case IDs by type then alphabetical."""
    case_map = {c.id: c for c in all_cases}
    type_order = {t: i for i, t in enumerate(CASE_TYPES)}

    def sort_key(cid):
        c = case_map.get(cid)
        if c:
            return (type_order.get(c.type, 99), cid)
        return (99, cid)

    return sorted(case_ids, key=sort_key)


# ─── Table builders ───────────────────────────────────────────────────────────

def build_master_registry(cases: list[Case]) -> str:
    """§一 主注册表"""
    headers = ["ID", "名称", "类型", "年份", "导演/工作室", "主场景", "辅场景", "核心技法标签"]

    type_order = {t: i for i, t in enumerate(CASE_TYPES)}
    sorted_cases = sorted(cases, key=lambda c: (type_order.get(c.type, 99), -int(c.year) if c.year.isdigit() else 0, c.id))

    rows = []
    for c in sorted_cases:
        key_tags = ", ".join(c.tags[:6]) if c.tags else "—"
        rows.append([
            c.id, c.name, c.type, c.year, c.director,
            c.primary_scene, c.secondary_scene, key_tags,
        ])

    return f"""## 一、主注册表 Master Registry

{md_table(headers, rows)}

{TYPE_ENUM_TABLE}"""


def build_technique_tables(cases: list[Case]) -> str:
    """§二 技法→案例映射 (6 sub-tables)"""
    # Build reverse index: role → {technique: [case_ids]}
    index: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for c in cases:
        for role, techs in c.techniques.items():
            if role not in ROLE_LABELS:
                continue
            # creative only applies to commercial type
            if role == "creative" and c.type != "commercial":
                continue
            for t in techs:
                t_clean = t.strip()
                if t_clean:
                    index[role][t_clean].append(c.id)

    sections = []
    for role in ["narrative", "cinematography", "color", "vfx", "sound", "creative"]:
        label, owner = ROLE_LABELS[role]
        tech_map = index[role]

        if not tech_map:
            continue

        section = f"### {label} (→ {owner})\n\n"
        rows = []
        for tech_name in sorted(tech_map.keys()):
            case_ids = tech_map[tech_name]
            rows.append([tech_name, ", ".join(sort_case_ids(case_ids, cases))])

        section += md_table(["技法", "案例 ID"], rows)
        sections.append(section)

    return f"""## 二、技法 → 案例 Mapping

> Agent 查询路径：用户提到某个技法 → 查此表 → 加载对应案例文件 → 读取该技法的具体拆解。

{chr(10).join(sections)}"""


def build_scene_mapping(cases: list[Case]) -> str:
    """§三 场景类型→案例映射"""
    # Collect all scene types used
    scene_index: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"strong": [], "reference": []})

    for c in cases:
        for strength in ["strong", "reference"]:
            for scene in c.scene_relations.get(strength, []):
                if scene:
                    scene_index[scene][strength].append(c.id)

    # Sort scene types: known ones first, then alphabetical
    known_order = {s: i for i, s in enumerate(SCENE_TYPES)}
    sorted_scenes = sorted(
        scene_index.keys(),
        key=lambda s: (known_order.get(s, 99), s),
    )

    rows = []
    for scene in sorted_scenes:
        entry = scene_index[scene]
        strong = ", ".join(sort_case_ids(entry["strong"], cases)) if entry["strong"] else "—"
        reference = ", ".join(sort_case_ids(entry["reference"], cases)) if entry["reference"] else "—"
        rows.append([scene, strong, reference])

    return f"""## 三、场景类型 → 案例 Mapping

> Agent 查询路径：用户选择/匹配到某个场景类型 → 查此表 → 加载该场景最相关的案例。

{md_table(["场景类型", "强相关案例", "可参考案例"], rows)}"""


def build_style_mapping(cases: list[Case]) -> str:
    """§四 风格/情绪→案例映射"""
    style_index: dict[str, list[str]] = defaultdict(list)
    for c in cases:
        for s in c.styles:
            s_clean = s.strip()
            if s_clean:
                style_index[s_clean].append(c.id)

    if not style_index:
        return """## 四、风格/情绪 → 案例 Mapping

> 暂无风格标签数据。为案例添加 `styles:` frontmatter 字段后自动生成。"""

    rows = []
    for style in sorted(style_index.keys()):
        case_ids = style_index[style]
        rows.append([style, ", ".join(sort_case_ids(case_ids, cases))])

    return f"""## 四、风格/情绪 → 案例 Mapping

{md_table(["风格/情绪", "案例 ID"], rows)}"""


def build_role_section() -> str:
    """§五 角色维度→案例映射 (静态)"""
    return """## 五、角色维度 → 案例 Mapping

> **默认规则**：全部案例覆盖 5 个角色维度（Writer / DP / Art Director / VFX Supervisor / Sound Designer）。
> 具体案例推荐见 [§二 技法→案例表](#二技法--案例-mapping)，已按角色分节：
> - 叙事技法 → Writer
> - 镜头语言 → DP
> - 色彩/美术方向 → Art Director
> - 特效技法 → VFX Supervisor
> - 声音设计 → Sound Designer
>
> **「广告创意综合」维度**：仅适用于 commercial 类型。其余类型（film / short-film / experimental / animation / documentary / music-video / logo-animation）不参与此维度。"""


def build_sop_section(case_count: int, recent_ids: list[str]) -> str:
    """§六 更新工作流 SOP"""
    recent_str = " + ".join(recent_ids[:4]) if recent_ids else "—"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return f"""## 六、更新工作流 (SOP)

### 添加新案例

```
1. Agent 或用户发现值得收录的作品
2. Agent 检查 cases/ 目录是否已存在
3. 若不存在 → 确认收录
4. Agent 观看/研究作品 → 按 _TEMPLATE.md 格式拆解
5. Agent 创建 references/cases/<id>.md，填写 YAML frontmatter
6. Agent 运行 python scripts/build_index.py --check  → 校验
7. Agent 运行 python scripts/build_index.py --write  → 自动生成 INDEX.md
8. git commit + push
```

### 修改/推翻已有案例

```
1. 指出具体问题（哪个技法分析不对、哪个角色段不准确）
2. Agent 修改 references/cases/<id>.md（正文 + frontmatter）
3. Agent 运行 python scripts/build_index.py --write
4. git commit + push
```

### 索引一致性检查 (自动)

```
python scripts/build_index.py --check
```
脚本自动检查：
□ 所有案例有有效的 YAML frontmatter
□ 必填字段完整（id / name / type / primary_scene）
□ 无重复 case ID
□ 技法命名一致性（自动检测相似名称）
□ 风格标签大小写一致

---

*自动生成于 {date_str} | build_index.py v{VERSION} | 案例总数：{case_count}（{recent_str}）*"""


# ─── Assembler ────────────────────────────────────────────────────────────────

def assemble_index(cases: list[Case], recent_ids: list[str] = None) -> str:
    """Assemble the complete INDEX.md."""
    if recent_ids is None:
        recent_ids = []

    sections = [
        "# 案例索引 — Case Index\n",
        "> 影视作品 + 创意广告双轨收录。每新增一个案例 → 本文件由 `scripts/build_index.py` 自动生成。\n"
        ">\n"
        "> **更新方式**：编辑案例文件的 YAML frontmatter → 运行 `python scripts/build_index.py --write`。\n"
        "> **禁止手动编辑此文件**——所有数据来源于案例文件 frontmatter。\n",
        "---\n",
        build_master_registry(cases),
        "---\n",
        build_technique_tables(cases),
        "---\n",
        build_scene_mapping(cases),
        "---\n",
        build_style_mapping(cases),
        "---\n",
        build_role_section(),
        "---\n",
        build_sop_section(len(cases), recent_ids),
    ]

    return "\n".join(sections)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Auto-generate INDEX.md from case file frontmatter"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Validate only (exit 1 on errors, 0 on pass)",
    )
    parser.add_argument(
        "--write", action="store_true",
        help="Validate + write INDEX.md",
    )
    parser.add_argument(
        "--diff", action="store_true",
        help="Show diff between current and generated INDEX.md without writing",
    )
    parser.add_argument(
        "--cases-dir", type=str, default=None,
        help="Path to references/cases/ directory",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Path to output INDEX.md (default: cases-dir/INDEX.md)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress non-error output",
    )
    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    cases_dir = Path(args.cases_dir) if args.cases_dir else (skill_root / "references" / "cases")
    output_path = Path(args.output) if args.output else (cases_dir / "INDEX.md")

    if not cases_dir.exists():
        print(f"ERROR: Cases directory not found: {cases_dir}", file=sys.stderr)
        sys.exit(1)

    # Load
    cases = load_all_cases(cases_dir)
    if not args.quiet:
        print(f"✓ Loaded {len(cases)} cases from {cases_dir}", file=sys.stderr)

    # Validate
    errors, warnings = validate(cases)
    if warnings and not args.quiet:
        for w in warnings:
            print(w, file=sys.stderr)

    if errors:
        print(f"\n❌ {len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"✓ Validation passed (0 errors, {len(warnings)} warnings)", file=sys.stderr)

    # Generate
    new_index = assemble_index(cases)

    # --check mode: exit here
    if args.check:
        print("✓ All checks passed. INDEX.md would be generated successfully.", file=sys.stderr)
        return

    # --diff mode: show diff
    if args.diff:
        old_content = ""
        if output_path.exists():
            old_content = output_path.read_text(encoding="utf-8")
        diff = unified_diff(
            old_content.splitlines(keepends=True),
            new_index.splitlines(keepends=True),
            fromfile=str(output_path),
            tofile=f"{output_path} (generated)",
        )
        sys.stdout.writelines(diff)
        return

    # --write mode: write file
    if args.write:
        # Backup old file if it exists
        if output_path.exists():
            backup_path = output_path.with_suffix(".md.bak")
            output_path.rename(backup_path)
            if not args.quiet:
                print(f"  Backed up old INDEX.md → {backup_path.name}", file=sys.stderr)

        output_path.write_text(new_index, encoding="utf-8")
        if not args.quiet:
            print(f"✅ INDEX.md generated → {output_path}", file=sys.stderr)
            print(f"   {len(cases)} cases, {len(new_index.splitlines())} lines", file=sys.stderr)
        return

    # Default: print to stdout
    print(new_index)


if __name__ == "__main__":
    main()
