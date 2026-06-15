#!/usr/bin/env python3
"""
Muse Video Skill — validate_state.py
Phase gate validator: checks whether a Project State JSON satisfies
the entry conditions for a given pipeline phase.

Usage:
    python scripts/validate_state.py --input project-state.json --phase 4
    python scripts/validate_state.py --input project-state.json --phase 7 --quiet

Exit codes:
    0 — PASS (all gates satisfied, ready to enter phase)
    1 — BLOCKED (one or more hard gates failed)
"""

import json
import sys
import os
import argparse
from pathlib import Path

VERSION = "0.1.0"

# ── Phase → Section mapping ──────────────────────────────────────────────────
# Maps pipeline phase numbers to the JSON sections that are produced during
# each phase. Used for display purposes (showing which phase produced what).
PHASE_ROLE_MAP = {
    1: "director_notes",
    2: "script",
    3: "visual_dev",
    4: "script + cinematography",
    5: "sound",
    6: "vfx + storyboard",
    7: "creative_pack",
}


def resolve_dotted(data: dict, dotted_path: str, default=None):
    """Resolve a dotted path in a nested dict, supporting array indices [N].

    Examples:
        resolve_dotted(d, "script.logline")        → d["script"]["logline"]
        resolve_dotted(d, "script.scenes[0].dialogue") → d["script"]["scenes"][0]["dialogue"]
    """
    import re

    current = data
    # Split on '.' but preserve [N] as part of the segment
    segments = re.split(r"\.(?![^\[]*\])", dotted_path)

    for seg in segments:
        if current is None:
            return default

        # Parse array index if present: e.g. "scenes[0]" → key="scenes", index=0
        match = re.match(r"^([^\[]+)(?:\[(\d+)\])?$", seg)
        if not match:
            return default

        key = match.group(1)
        idx = match.group(2)

        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default

        if idx is not None and isinstance(current, list):
            try:
                current = current[int(idx)]
            except (IndexError, ValueError):
                return default

    return current


def is_empty(val) -> bool:
    """Check whether a value is semantically empty.

    Returns True for: None, "", [], {}
    Returns False for: 0, False, non-empty strings/lists/dicts
    """
    if val is None:
        return True
    if isinstance(val, str) and val.strip() == "":
        return True
    if isinstance(val, (list, dict)) and len(val) == 0:
        return True
    return False


def load_yaml_simple(path: str) -> dict:
    """Load a simple YAML file without external dependencies.
    
    Supports the subset used by phase_gates.yaml (nested dicts, lists,
    string values). No anchors, aliases, or multi-line strings.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip comments and empty lines
    clean_lines = []
    for line in lines:
        stripped = line.rstrip()
        # Remove inline comments (but not inside quoted strings — simple heuristic)
        if "#" in stripped and '"' not in stripped.split("#")[0]:
            stripped = stripped.split("#")[0].rstrip()
        if stripped:
            clean_lines.append(stripped)

    # Parse with PyYAML if available, otherwise use basic parsing
    try:
        import yaml
        return yaml.safe_load("\n".join(clean_lines))
    except ImportError:
        pass

    # Fallback: parse the subset we actually need
    result = {}
    current_section = None
    current_list = None
    current_list_name = None
    indent_level = 0

    for line in clean_lines:
        # Count leading spaces
        stripped = line.lstrip()
        leading = len(line) - len(stripped)

        if ":" in stripped and not stripped.startswith("-"):
            # Key: value or Key:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()

            if val == "":
                # Nested dict opener
                if leading == 0:
                    current_section = key
                    result[current_section] = {}
                elif current_section:
                    # Could be a sub-section or a list of items
                    pass
            elif leading == 0:
                result[key] = val
            elif current_section and isinstance(result.get(current_section), dict):
                result[current_section][key] = parse_yaml_value(val)
        elif stripped.startswith("- "):
            item_val = parse_yaml_value(stripped[2:].strip())
            if current_list_name and current_list is not None:
                current_list.append(item_val)

    return result


def parse_yaml_value(val: str):
    """Parse a simple YAML scalar value."""
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.isdigit():
        return int(val)
    # Strip surrounding quotes if present
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1]
    return val


def load_gates(gates_path: str) -> dict:
    """Load phase gate rules from YAML."""
    raw = load_yaml_simple(gates_path)
    return raw.get("gates", {})


def load_project_state(input_path: str) -> dict:
    """Load Project State JSON."""
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_section_approved(state: dict, section: str) -> tuple:
    """Check whether a top-level section has _meta.director_approved = true.

    Returns: (passed: bool, message: str)
    """
    section_data = state.get(section)
    if section_data is None:
        return False, f"{section} — section 不存在于 Project State 中"

    meta = section_data.get("_meta") if isinstance(section_data, dict) else None
    if meta is None:
        return False, f"{section}._meta — 缺少追溯标记（请确保该阶段产出已写入 _meta）"

    approved = meta.get("director_approved")
    if approved is not True:
        return False, f"{section}._meta.director_approved — 不为 true（当前值: {approved}）。Director 审核未完成。"

    return True, f"{section} — ✅ APPROVED"


def check_storyboard_panels_approved(state: dict) -> tuple:
    """Check whether all storyboard panels have _meta.director_approved = true.

    Returns: (passed: bool, blocked_count: int, total_count: int)
    """
    panels = state.get("storyboard", [])
    if not isinstance(panels, list) or len(panels) == 0:
        return False, 0, 0

    blocked = []
    for panel in panels:
        meta = panel.get("_meta") if isinstance(panel, dict) else None
        if meta is None or meta.get("director_approved") is not True:
            panel_id = panel.get("panel_id", "?")
            blocked.append(str(panel_id))

    total = len(panels)
    blocked_count = len(blocked)
    return blocked_count == 0, blocked_count, total


def validate(state: dict, gate: dict, phase_key: str) -> dict:
    """Run all gate checks for a phase.

    Returns a dict with:
        passed: bool — True if no BLOCKED items
        blockers: list of str
        warnings: list of str
        info: list of str
    """
    result = {"passed": True, "blockers": [], "warnings": [], "info": []}

    phase_num = int(phase_key.replace("phase_", ""))
    desc = gate.get("description", phase_key)

    # ── 1. Check section approvals ──
    required_sections = gate.get("requires_approved_sections", [])
    for section in required_sections:
        passed, msg = check_section_approved(state, section)
        if not passed:
            result["blockers"].append(msg)
            result["passed"] = False
        else:
            result["info"].append(msg)

    # ── 2. Check storyboard panel approvals ──
    if gate.get("requires_all_panels_approved"):
        panels_ok, blocked, total = check_storyboard_panels_approved(state)
        if total == 0:
            result["blockers"].append(
                "storyboard — 分镜面板为空（至少需要 1 个 panel）"
            )
            result["passed"] = False
        elif not panels_ok:
            result["blockers"].append(
                f"storyboard — {blocked}/{total} 个 panel 的 _meta.director_approved 不为 true"
            )
            result["passed"] = False
        else:
            result["info"].append(
                f"storyboard — ✅ 全部 {total} 个 panel 已审批"
            )

    # ── 3. Check required fields ──
    for field_path in gate.get("required_fields", []):
        val = resolve_dotted(state, field_path)
        if is_empty(val):
            result["blockers"].append(f"{field_path} — 字段为空")
            result["passed"] = False
        else:
            result["info"].append(f"{field_path} — ✅ 已填写")

    # ── 4. Check warn_if_empty ──
    for field_path in gate.get("warn_if_empty", []):
        val = resolve_dotted(state, field_path)
        if is_empty(val):
            result["warnings"].append(f"{field_path} — 建议填写（不阻塞）")
        else:
            result["info"].append(f"{field_path} — ✅ 已填写")

    return result


def format_output(phase_key: str, gate: dict, result: dict, quiet: bool) -> str:
    """Format validation result for Agent consumption."""
    desc = gate.get("description", phase_key)
    lines = []

    if result["passed"]:
        status_line = f"✅ PASS — 可以进入 {desc}"
    else:
        status_line = f"❌ BLOCKED — 无法进入 {desc}"

    lines.append(status_line)
    lines.append("━" * 56)

    if quiet and result["passed"]:
        return status_line

    # Blockers first (most actionable)
    if result["blockers"]:
        for b in result["blockers"]:
            lines.append(f"  ✗ {b}")

    if result["warnings"]:
        for w in result["warnings"]:
            lines.append(f"  ⚠  {w}")

    if not quiet and result["info"]:
        for i in result["info"]:
            lines.append(f"  ℹ  {i}")

    lines.append("━" * 56)

    if result["blockers"]:
        lines.append("需要修复:")
        for i, b in enumerate(result["blockers"], 1):
            lines.append(f"  {i}. {b.split(' — ')[0]}")
        lines.append("")
        lines.append("建议操作: 回到前置阶段修复上述问题后重新验证。")

    return "\n".join(lines)


def find_gates_path() -> str:
    """Find phase_gates.yaml relative to this script (same skill root)."""
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    gates_path = skill_root / "metadata" / "phase_gates.yaml"
    if gates_path.exists():
        return str(gates_path)
    # Fallback: try relative to cwd
    cwd_path = Path.cwd() / "metadata" / "phase_gates.yaml"
    if cwd_path.exists():
        return str(cwd_path)
    raise FileNotFoundError(
        "Cannot find metadata/phase_gates.yaml. "
        "Ensure you're running from the skill root directory."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Muse Video — Phase Gate Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_state.py --input project-state.json --phase 4
  python scripts/validate_state.py --input project-state.json --phase 7 --quiet
        """,
    )
    parser.add_argument("--input", required=True, help="Path to Project State JSON file")
    parser.add_argument("--phase", type=int, required=True, choices=range(2, 8),
                        help="Target phase number (2-7)")
    parser.add_argument("--quiet", action="store_true",
                        help="Only output PASS/BLOCKED line, no details")
    args = parser.parse_args()

    # Load
    try:
        gates = load_gates(find_gates_path())
    except FileNotFoundError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(2)

    phase_key = f"phase_{args.phase}"
    gate = gates.get(phase_key)
    if gate is None:
        print(f"FATAL: No gate defined for {phase_key}", file=sys.stderr)
        sys.exit(2)

    try:
        state = load_project_state(args.input)
    except FileNotFoundError:
        print(f"FATAL: Project State file not found: {args.input}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"FATAL: Invalid JSON in {args.input}: {e}", file=sys.stderr)
        sys.exit(2)

    # Validate
    result = validate(state, gate, phase_key)
    output = format_output(phase_key, gate, result, args.quiet)
    print(output)

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
