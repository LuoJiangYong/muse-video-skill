#!/usr/bin/env python3
"""
Muse Video Skill — storyboard_grid.py
Input:  Project State JSON (stdin or --input file)
Output: Storyboard grid layout — 2×3 or 3×3 (Markdown)

Role: One job — storyboard array → grid layout. Not scripts, not formats.
Schema-driven: reads storyboard[] from Project State JSON, no scene-type logic.
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"

# Grid layout configuration
GRID_CONFIG = {
    6: {"name": "2×3", "cols": 3, "rows": 2, "max_panels": 6},
    9: {"name": "3×3", "cols": 3, "rows": 3, "max_panels": 9},
}


def safe_str(val, default: str = "—") -> str:
    """Return string value or default if None/empty."""
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def resolve(data: dict, path: str, default="—") -> str:
    """Resolve a dotted path in a nested dict."""
    keys = path.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        else:
            return default
        if current is None:
            return default
    return safe_str(current, default)


def determine_grid(panel_count: int) -> dict:
    """Determine best grid layout for the number of panels.

    Strategy:
      - ≤6 panels → 2×3 grid
      - ≤9 panels → 3×3 grid
      - >9 panels → 3×3 grid with overflow note
    """
    if panel_count <= 6:
        return GRID_CONFIG[6]
    else:
        return GRID_CONFIG[9]


def format_panel_text(panel: dict, idx: int) -> str:
    """Format a single storyboard panel as Markdown."""
    lines = []
    panel_id = panel.get("panel_id", idx + 1)
    scene_id = panel.get("scene_id", "—")

    total_panels = idx + 1  # will be replaced by caller
    lines.append(f"### 【Panel {panel_id}】— 第 {scene_id} 场\n")
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| **景别** | {safe_str(panel.get('layout'))} |")
    lines.append(f"| **画面描述** | {safe_str(panel.get('description'))} |")
    lines.append("")

    # AI prompt
    prompt = safe_str(panel.get("prompt"), "")
    if prompt:
        lines.append("#### AI 生成提示词")
        lines.append("```")
        lines.append(prompt)
        lines.append("```")
        lines.append("")

    # Technical notes
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| **镜头备注** | {safe_str(panel.get('camera_notes'))} |")
    lines.append(f"| **特效备注** | {safe_str(panel.get('vfx_notes'))} |")

    char_ids = panel.get("character_ids", [])
    char_str = ", ".join(str(c) for c in char_ids) if char_ids else "—"
    lines.append(f"| **关联角色** | {char_str} |")

    gen_url = safe_str(panel.get("generated_url"), "—")
    lines.append(f"| **参考图** | {gen_url} |")

    approved = panel.get("approved", False)
    status_icon = "✅ 已审核" if approved else "⏳ 待审核"
    lines.append(f"| **状态** | {status_icon} |")
    lines.append("")

    meta = panel.get("_meta", {})
    lines.append(f"| **审核版本** | {safe_str(meta.get('revision'), '1')} |")
    lines.append(f"| **导演审核** | {safe_str(meta.get('director_approved'), 'false')} |")
    lines.append("")

    return "\n".join(lines)


def build_output(project_state: dict) -> str:
    """Build the complete storyboard grid Markdown output."""
    project = project_state.get("project", {})
    storyboard = project_state.get("storyboard", [])

    if not isinstance(storyboard, list):
        storyboard = []

    panel_count = len(storyboard)
    grid = determine_grid(panel_count)

    lines = []
    lines.append(f"# {safe_str(project.get('title'))} — 分镜\n")
    lines.append(
        f"> **场景类型**：`{safe_str(project.get('scene_type'))}` | "
        f"**时长**：`{safe_str(project.get('duration_est'))}` | "
        f"**画幅**：`{safe_str(project.get('aspect_ratio'), '16:9')}`"
    )
    lines.append(f"> **网格布局**：{grid['name']}（{panel_count} 格）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 画面网格")
    lines.append("")

    if panel_count == 0:
        lines.append("> ⚠️ 分镜数据为空，请确认 Project State JSON 中 storyboard[] 已填充。")
    else:
        if panel_count > grid["max_panels"]:
            lines.append(
                f"> ⚠️ 当前 {panel_count} 格超出 {grid['name']} 网格上限（{grid['max_panels']} 格），"
                f"仅展示前 {grid['max_panels']} 格。建议拆分为多个网格。"
            )
            lines.append("")

        for i, panel in enumerate(storyboard[: grid["max_panels"]]):
            lines.append(format_panel_text(panel, i))

    # Metadata footer
    lines.append("---")
    lines.append("")
    lines.append("## 元信息")
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("|------|-----|")
    lines.append(f"| **总镜数** | {panel_count} |")
    lines.append(f"| **网格布局** | {grid['name']} |")
    lines.append(
        f"| **生成时间** | {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} |"
    )
    lines.append(f"| **生成工具** | Muse Video Skill — storyboard_grid.py v{VERSION} |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Storyboard array → grid layout (2×3 / 3×3) Markdown"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="Path to Project State JSON file (default: stdin)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--grid",
        type=str,
        choices=["2x3", "3x3", "auto"],
        default="auto",
        help="Force grid layout (default: auto-select based on panel count)",
    )
    args = parser.parse_args()

    # Load project state
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            project_state = json.load(f)
    else:
        project_state = json.load(sys.stdin)

    # Override grid if specified by user
    if args.grid != "auto":
        if args.grid == "2x3":
            project_state.setdefault("_grid_layout", "2×3")
        elif args.grid == "3x3":
            project_state.setdefault("_grid_layout", "3×3")

    # Build output
    output = build_output(project_state)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Storyboard grid written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
