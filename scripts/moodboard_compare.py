#!/usr/bin/env python3
"""
Muse Video Skill — moodboard_compare.py
Input:  2+ visual direction definitions (via Project State JSON or dedicated input)
Output: Comparison matrix — side-by-side analysis of competing visual directions

Role: One job — compare visual directions and produce a structured comparison matrix.
      Used during Phase 3 (视觉开发) when Director wants to evaluate multiple
      Art Director proposals before committing to one.

Schema-driven: reads visual_dev data from Project State JSON.
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"


def safe_str(val, default: str = "—") -> str:
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def compare_palettes(a: list, b: list) -> str:
    """Compare two palettes and return brief analysis."""
    a_hex = [p.get("hex", "") for p in a]
    b_hex = [p.get("hex", "") for p in b]
    overlap = set(a_hex) & set(b_hex)
    if overlap:
        return f"共享 {len(overlap)} 色（{', '.join(sorted(overlap))}）"
    else:
        return "色调完全独立，无重叠"


def similarity_assessment(a: dict, b: dict) -> str:
    """Return a qualitative similarity assessment between two visual directions."""
    reasons = []

    a_mood = safe_str(a.get("mood"), "")
    b_mood = safe_str(b.get("mood"), "")
    if a_mood and b_mood:
        # Simple keyword overlap
        a_words = set(a_mood.lower().split())
        b_words = set(b_mood.lower().split())
        common = a_words & b_words
        if len(common) >= 3:
            reasons.append(f"情绪基调高度重叠（共同关键词：{', '.join(sorted(common))}）")
        elif len(common) >= 1:
            reasons.append(f"情绪基调部分重叠（共同关键词：{', '.join(sorted(common))}）")
        else:
            reasons.append("情绪基调截然不同")

    a_palette = a.get("palette", [])
    b_palette = b.get("palette", [])
    if a_palette and b_palette:
        reasons.append(f"色调：{compare_palettes(a_palette, b_palette)}")

    a_chars = len(a.get("characters", []))
    b_chars = len(b.get("characters", []))
    if a_chars or b_chars:
        reasons.append(f"角色数量：{a_chars} vs {b_chars}")

    if not reasons:
        return "信息不足以判断"
    return "；".join(reasons)


def build_comparison_matrix(directions: list) -> str:
    """Build a Markdown comparison matrix for 2+ visual directions."""
    if len(directions) < 2:
        return "⚠️ 需要至少 2 个视觉方向才能进行对比。"

    lines = []
    lines.append("# 美术方案对比矩阵\n")
    lines.append(f"> 生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"> 方案数量：{len(directions)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Overview table ──
    lines.append("## 方案概览\n")
    headers = ["维度"] + [f"方案 {i+1}" for i in range(len(directions))]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["------"] * len(headers)) + "|")

    compare_fields = [
        ("情绪基调", "mood"),
        ("角色数量", lambda d: str(len(d.get("characters", [])))),
        ("色调数量", lambda d: str(len(d.get("palette", [])))),
        ("风格参考数", lambda d: str(len(d.get("style_refs", [])))),
        ("参考图数", lambda d: str(len(d.get("image_refs", [])))),
        ("导演审核", lambda d: "✅" if d.get("_meta", {}).get("director_approved") else "⏳"),
    ]

    for label, field in compare_fields:
        row = [f"**{label}**"]
        for d in directions:
            if callable(field):
                val = field(d)
            else:
                val = safe_str(d.get(field, ""))
            row.append(val)
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    # ── Palette comparison ──
    lines.append("## 色调对比\n")
    all_palettes = []
    for i, d in enumerate(directions):
        for p in d.get("palette", []):
            all_palettes.append({
                "方案": f"方案 {i+1}",
                "名称": p.get("name", "—"),
                "色值": p.get("hex", "—"),
                "用途": p.get("usage", "—"),
            })

    if all_palettes:
        lines.append("| 方案 | 名称 | 色值 | 用途 |")
        lines.append("|------|------|------|------|")
        for p in all_palettes:
            hex_val = p["色值"]
            color_preview = f"![{hex_val}](https://singlecolorimage.com/{hex_val.lstrip('#')}/16x16)" if hex_val != "—" else ""
            lines.append(f"| {p['方案']} | {p['名称']} | `{hex_val}` {color_preview} | {p['用途']} |")
        lines.append("")

    # ── Style references comparison ──
    lines.append("## 风格参考对比\n")
    for i, d in enumerate(directions):
        refs = d.get("style_refs", [])
        lines.append(f"### 方案 {i+1}\n")
        if refs:
            for r in refs:
                lines.append(f"- **{r.get('ref_type', '—')}** — *{r.get('name', '—')}*：{r.get('description', '—')}")
        else:
            lines.append("- 无风格参考")
        lines.append("")

    # ── Pairwise similarity ──
    lines.append("## 相似度分析\n")
    for i in range(len(directions)):
        for j in range(i + 1, len(directions)):
            assessment = similarity_assessment(directions[i], directions[j])
            lines.append(f"**方案 {i+1} vs 方案 {j+1}**：{assessment}")
    lines.append("")

    # ── Recommendation ──
    lines.append("## 推荐方向\n")
    lines.append("> 以下为客观对比数据，最终决策由 Director 根据 `director_notes.vision` 判断。")
    lines.append("")
    lines.append("| 评判维度 | 权重 | 方案选择建议 |")
    lines.append("|----------|------|-------------|")
    criteria = [
        ("品牌契合度", "高", "对比各方案色调是否符合品牌色规范"),
        ("情绪传达", "高", "对比 mood 描述与 director_notes.tone 的对齐度"),
        ("可行性", "中", "对比角色/场景复杂度与项目 constraints 的匹配度"),
        ("独特性", "中", "对比风格参考的多样性"),
        ("迭代成本", "低", "对比 _meta.revision 数"),
    ]
    for criterion, weight, note in criteria:
        lines.append(f"| {criterion} | {weight} | {note} |")
    lines.append("")

    lines.append("---")
    lines.append(f"*Generated by Muse Video Skill — moodboard_compare.py v{VERSION}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Compare 2+ visual directions → comparison matrix"
    )
    parser.add_argument("--input", "-i", type=str, default=None,
                        help="Path to JSON file containing an array of visual direction objects")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output file path (default: stdout)")
    parser.add_argument("--from-project-state", type=str, default=None,
                        help="Extract visual_dev from a full Project State JSON (single-direction mode)")
    parser.add_argument("--compare-with", type=str, default=None,
                        help="Second visual_dev JSON to compare against --from-project-state")
    args = parser.parse_args()

    directions = []

    # Mode 1: Full comparison of an array of visual directions
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            directions = data
        elif isinstance(data, dict):
            # Could be a single direction or project state
            if "visual_dev" in data:
                directions = [data.get("visual_dev", {})]
            else:
                directions = [data]

    # Mode 2: Compare two project states
    if args.from_project_state:
        with open(args.from_project_state, "r", encoding="utf-8") as f:
            ps1 = json.load(f)
        directions.append(ps1.get("visual_dev", {}))

        if args.compare_with:
            with open(args.compare_with, "r", encoding="utf-8") as f:
                ps2 = json.load(f)
            directions.append(ps2.get("visual_dev", {}))

    # Mode 3: stdin (expects array or project state)
    if not directions and not sys.stdin.isatty():
        data = json.load(sys.stdin)
        if isinstance(data, list):
            directions = data
        elif isinstance(data, dict):
            if "visual_dev" in data:
                directions = [data.get("visual_dev", {})]
            else:
                directions = [data]

    if len(directions) < 2:
        print("ERROR: Need at least 2 visual directions to compare.", file=sys.stderr)
        print("Provide --input with an array, or --from-project-state + --compare-with", file=sys.stderr)
        sys.exit(1)

    output = build_comparison_matrix(directions)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Comparison matrix → {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
