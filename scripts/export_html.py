#!/usr/bin/env python3
"""
Muse Video Skill — export_html.py
Input:  Project State JSON (stdin or --input file)
Output: Literary script HTML, storyboard gallery HTML, and/or compilation preview HTML (Phase 7.5)

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

VERSION = "0.4.0"


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


def fill_html_template(template: str, project_state: dict, simple_extra: dict = None, shots: list = None) -> str:
    """Fill {{placeholder}} and {{#each}} blocks in HTML templates.
    simple_extra: extra top-level replacements (e.g. compilation summary chips).
    shots: pre-computed shot view list for {{#each model_compilation.shots}}."""
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

    if simple_extra:
        simple.update(simple_extra)

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
            if inner.startswith("#") or inner.startswith("/"):
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
            node = item
            for p in field.split("."):
                if isinstance(node, dict):
                    node = node.get(p)
                else:
                    node = None
                    break
            return body if node else ""

        # Innermost-first loop — nested {{#if}} blocks inside each-items resolve correctly.
        _if_pat = re.compile(r"\{\{#if\s+([^\s{}]+)\}\}((?:(?!\{\{#if)[\s\S])*?)\{\{/if\}\}")
        while True:
            block, n = _if_pat.subn(_repl_if, block)
            if n == 0:
                return block

    # Expand arrays
    result = _expand_each(result, "script.scenes", safe_list(script.get("scenes")))
    result = _expand_each(result, "storyboard", storyboard)
    if shots is not None:
        result = _expand_each(result, "model_compilation.shots", shots)

    # Top-level {{#if KEY}}…{{else}}…{{/if}} resolved via simple values (unknown keys left to cleanup)
    def _top_if(m):
        field = m.group(1).strip()
        if field not in simple:
            return m.group(0)
        return m.group(2) if simple.get(field) else (m.group(3) or "")
    result = re.sub(
        r"\{\{#if\s+([^\s{}]+)\}\}((?:(?!\{\{#if)[\s\S])*?)\{\{else\}\}((?:(?!\{\{#if)[\s\S])*?)\{\{/if\}\}",
        _top_if, result)

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


def build_refs_html(image_refs: list, registry: dict) -> str:
    """Render image_ref -> file_registry mapping rows for the compilation preview."""
    if not image_refs:
        return '<div class="ref-empty">（本镜未引用参考图）</div>'
    rows = []
    for idx, name in enumerate(image_refs, 1):
        entry = registry.get(str(name)) or {}
        local_path = entry.get("local_path") or "—"
        weight = entry.get("weight", "—")
        source = entry.get("source") or "—"
        file_id = entry.get("file_id") or "—"
        pending = ' <span class="ref-pend">⚠️ 待上传（PENDING）</span>' if str(file_id).upper() == "PENDING" else ""
        thumb = ""
        if local_path != "—":
            thumb = ('<img class="ref-thumb" src="' + str(local_path) + '" alt="' + str(name)
                     + '" onerror="this.style.display=\'none\'">')
        rows.append(
            '<div class="ref-row"><span class="ref-idx">image_ref_' + str(idx) + '</span>'
            + '<b>' + str(name) + '</b>'
            + '<span class="ref-meta">' + str(local_path) + ' · weight=' + str(weight)
            + ' · ' + str(source) + ' · file_id=' + str(file_id) + '</span>'
            + pending + thumb + '</div>'
        )
    return "".join(rows)


def export_compilation(project_state: dict, output_path: str) -> None:
    """Render script-compilation.html — Phase 7.5 compilation preview (reads model_compilation)."""
    script_dir = Path(__file__).resolve().parent.parent
    tpl_path = script_dir / "assets" / "templates" / "export" / "script-compilation.html"
    if tpl_path.exists():
        template = tpl_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Template not found: {tpl_path}")

    mc = project_state.get("model_compilation") or {}
    shots = mc.get("shots") or []
    if not isinstance(shots, list):
        shots = []
    # Registry resolution: top-level file_registry first, then legacy path.
    registry = project_state.get("file_registry") or mc.get("file_registry") or {}

    durations = []
    for s in shots:
        try:
            durations.append(int(s.get("duration") or 0))
        except (TypeError, ValueError):
            pass
    total_duration = f"{sum(durations)}s / {len(shots)} 镜" if shots else "—"

    costs = []
    for s in shots:
        c = s.get("estimated_cost_cny")
        if c and str(c) not in costs:
            costs.append(str(c))
    est_cost = " + ".join(costs) if costs else "—"

    order = {"GOOD": 0, "DEGRADED": 1, "INSUFFICIENT": 2}
    worst = None
    for s in shots:
        q = ((s.get("_quality") or {}).get("overall")) or ""
        if q in order and (worst is None or order[q] > order[worst]):
            worst = q
    worst_quality = worst or ("GOOD" if shots else "—")

    target_model = mc.get("target_model") or ((mc.get("_meta") or {}).get("target_model")) or "—"

    shots_view = []
    for s in shots:
        s2 = dict(s)
        refs = ((s.get("multimodal_refs") or {}).get("image_refs")) or []
        if not isinstance(refs, list):
            refs = []
        s2["_refs_html"] = build_refs_html(refs, registry)
        q = ((s.get("_quality") or {}).get("overall")) or ""
        s2["_quality_open"] = "open" if (q and q != "GOOD") else ""
        warnings = (s.get("_quality") or {}).get("warnings") or []
        s2["_quality_warnings_html"] = "".join("<li>" + str(w) + "</li>" for w in warnings)
        shots_view.append(s2)

    simple_extra = {
        "compilation.target_model": safe_str(target_model),
        "compilation.total_duration": safe_str(total_duration),
        "compilation.est_cost": safe_str(est_cost),
        "compilation.worst_quality": safe_str(worst_quality),
    }

    html = fill_html_template(template, project_state, simple_extra=simple_extra, shots=shots_view)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Compilation preview HTML → {output_path}", file=sys.stderr)


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
    parser.add_argument("--compilation", "-c", type=str, default=None,
                        help="Output path for compilation preview HTML (Phase 7.5)")
    parser.add_argument("--all", "-a", type=str, default=None,
                        help="Base output path for both exports (appends -literary.html / -storyboard.html)")
    args = parser.parse_args()

    if not args.literary and not args.storyboard and not args.compilation and not args.all:
        parser.error("At least one of --literary, --storyboard, --compilation, or --all is required")

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

    # Export compilation preview
    if args.compilation:
        export_compilation(project_state, args.compilation)

    # Export both
    if args.all:
        base = args.all.rstrip("/")
        export_literary(project_state, f"{base}-literary.html")
        export_storyboard(project_state, f"{base}-storyboard.html")


if __name__ == "__main__":
    main()
