#!/usr/bin/env python3
"""
Muse Video Skill — export_html.py
Input:  Project State JSON (stdin or --input file)
Output: Literary script HTML and/or storyboard gallery HTML

Role: One job — render Project State → polished HTML export files.
      Uses templates from assets/templates/export/.
Schema-driven: reads from Project State JSON, no scene-type logic.
"""

import json
import sys
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"


def safe_str(val, default: str = "—") -> str:
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def safe_list(val) -> list:
    if isinstance(val, list):
        return val
    return []


def resolve_path(data: dict, dotted_path: str, default=None):
    keys = dotted_path.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        else:
            return default
        if current is None:
            return default
    return current


def fill_html_template(template: str, project_state: dict) -> str:
    """Fill {{placeholder}} and {{#each}} blocks in HTML templates."""
    project = project_state.get("project", {})
    script = project_state.get("script", {})
    director_notes = project_state.get("director_notes", {})
    storyboard = project_state.get("storyboard", [])
    if not isinstance(storyboard, list):
        storyboard = []

    # Simple replacements
    simple = {
        "project.title": safe_str(project.get("title")),
        "project.scene_type": safe_str(project.get("scene_type")),
        "project.duration_est": safe_str(project.get("duration_est")),
        "project.aspect_ratio": safe_str(project.get("aspect_ratio"), "16:9"),
        "project.genre": safe_str(project.get("genre")),
        "project.platform": safe_str(project.get("platform")),
        "project.language": safe_str(project.get("language"), "zh-CN"),
        "director_notes.vision": safe_str(director_notes.get("vision")),
        "script.logline": safe_str(script.get("logline")),
        "script.structure": safe_str(script.get("structure")),
        "script._meta.writer_revision": safe_str(resolve_path(script, "_meta.writer_revision", "1")),
        "script._meta.dp_revision": safe_str(resolve_path(script, "_meta.dp_revision", "1")),
        "script._meta.director_approved": safe_str(resolve_path(script, "_meta.director_approved", "false")),
        "_version": VERSION,
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_panels_count": str(len(storyboard)),
        "_grid_layout": "2×3" if len(storyboard) <= 6 else "3×3",
        "_is_3x3": "true" if len(storyboard) > 6 else "",
    }

    def _repl_simple(m):
        inner = m.group(1).strip()
        if inner.startswith("#"):
            return m.group(0)
        return simple.get(inner, m.group(0))

    result = re.sub(r"\{\{(.+?)\}\}", _repl_simple, template)

    # Expand each blocks
    def _expand_each(text: str, key: str, data: list) -> str:
        pattern = re.compile(
            r"\{\{#each\s+" + re.escape(key) + r"\s*\}\}(.*?)\{\{/each\}\}",
            re.DOTALL,
        )
        m = pattern.search(text)
        if not m:
            return text
        block_tmpl = m.group(1)
        parts = []
        for item in data:
            block = block_tmpl
            block = _fill_item(block, item)
            parts.append(block)
        return text[: m.start()] + "".join(parts) + text[m.end() :]

    def _fill_item(block: str, item: dict) -> str:
        def _repl(m):
            inner = m.group(1).strip()
            if inner.startswith("#"):
                return m.group(0)
            parts = inner.split(".")
            v = item
            for p in parts:
                if isinstance(v, dict):
                    v = v.get(p)
                else:
                    v = None
                    break
            if v is None:
                return ""
            if isinstance(v, list):
                return ", ".join(str(x) for x in v)
            return safe_str(v, "—")

        block = re.sub(r"\{\{(.+?)\}\}", _repl, block)

        def _repl_if(m):
            field = m.group(1).strip()
            body = m.group(2)
            pf = field.split(".")
            v = item
            for p in pf:
                if isinstance(v, dict):
                    v = v.get(p)
                else:
                    v = None
                    break
            return body if v else ""

        block = re.sub(r"\{\{#if\s+(.+?)\}\}(.*?)\{\{/if\}\}", _repl_if, block, flags=re.DOTALL)
        return block

    # Expand arrays
    result = _expand_each(result, "script.scenes", safe_list(script.get("scenes")))
    result = _expand_each(result, "storyboard", storyboard)

    # Cleanup
    result = re.sub(r"\{\{#each\s+\S+?\}\}.*?\{\{/each\}\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{\{#if\s+\S+?\}\}.*?\{\{/if\}\}", "", result, flags=re.DOTALL)

    return result


def export_literary(project_state: dict, output_path: str) -> None:
    """Render script-literary.html."""
    script_dir = Path(__file__).resolve().parent.parent
    tpl_path = script_dir / "assets" / "templates" / "export" / "script-literary.html"
    if tpl_path.exists():
        template = tpl_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Template not found: {tpl_path}")

    html = fill_html_template(template, project_state)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Literary script HTML → {output_path}", file=sys.stderr)


def export_storyboard(project_state: dict, output_path: str) -> None:
    """Render script-storyboard.html."""
    script_dir = Path(__file__).resolve().parent.parent
    tpl_path = script_dir / "assets" / "templates" / "export" / "script-storyboard.html"
    if tpl_path.exists():
        template = tpl_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Template not found: {tpl_path}")

    html = fill_html_template(template, project_state)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Storyboard HTML → {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Export Project State → polished HTML files"
    )
    parser.add_argument("--input", "-i", type=str, default=None,
                        help="Path to Project State JSON (default: stdin)")
    parser.add_argument("--literary", "-l", type=str, default=None,
                        help="Output path for literary script HTML")
    parser.add_argument("--storyboard", "-s", type=str, default=None,
                        help="Output path for storyboard gallery HTML")
    parser.add_argument("--all", "-a", type=str, default=None,
                        help="Base output path for both exports (appends -literary.html / -storyboard.html)")
    args = parser.parse_args()

    if not args.literary and not args.storyboard and not args.all:
        parser.error("At least one of --literary, --storyboard, or --all is required")

    # Load Project State
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            project_state = json.load(f)
    else:
        project_state = json.load(sys.stdin)

    # Export literary
    if args.literary:
        export_literary(project_state, args.literary)

    # Export storyboard
    if args.storyboard:
        export_storyboard(project_state, args.storyboard)

    # Export both
    if args.all:
        base = args.all.rstrip("/")
        export_literary(project_state, f"{base}-literary.html")
        export_storyboard(project_state, f"{base}-storyboard.html")


if __name__ == "__main__":
    main()
