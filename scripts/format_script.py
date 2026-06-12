#!/usr/bin/env python3
"""
Muse Video Skill — format_script.py
Input:  Project State JSON (stdin or --input file)
Output: Standard Hollywood-style formatted script (Markdown)

Role: One job — scene array → formatted script. Not storyboards.
Schema-driven: reads script.scenes[] from Project State JSON, no scene-type logic.
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"

# ─── template loader ──────────────────────────────────────────────────────────

def load_template(template_path: str | None = None) -> str:
    """Load the script.md template, or use built-in fallback."""
    if template_path:
        p = Path(template_path)
        if p.exists():
            return p.read_text(encoding="utf-8")
    # Built-in fallback template (mirrors assets/templates/script.md)
    return """# {{project.title}} — 剧本

> **场景类型**：`{{project.scene_type}}` | **时长**：`{{project.duration_est}}` | **画幅**：`{{project.aspect_ratio}}`
> **Logline**：{{script.logline}}
> **叙事结构**：{{script.structure}}

---

## 场景分解

{{#each script.scenes}}

### 第 {{scene_id}} 场 — {{scene_title}}

| 项目 | 内容 |
|------|------|
| **时长** | {{duration}} |
| **地点** | {{location}} |
| **时间** | {{time_of_day}} |

#### 动作描述
{{action}}

#### 对白
{{dialogue}}

{{#if camera}}
#### 技术备注
| 镜头 | 运镜 | 焦段 | 灯光 | 构图 |
|------|------|------|------|------|
| {{camera.shot_type}} | {{camera.movement}} | {{camera.lens}} | {{camera.lighting}} | {{camera.composition_notes}} |
{{/if}}

{{#if vfx_notes}}> 🎬 **特效**：{{vfx_notes}}{{/if}}
{{#if sound_notes}}> 🔊 **声音**：{{sound_notes}}{{/if}}

---

{{/each}}

## 元信息

| 字段 | 值 |
|------|-----|
| **编剧版本** | {{script._meta.writer_revision}} |
| **DP 版本** | {{script._meta.dp_revision}} |
| **导演审核** | {{script._meta.director_approved}} |
| **生成时间** | {{_generated_at}} |
| **生成工具** | Muse Video Skill — format_script.py v{{_version}} |
"""


# ─── placeholder substitution ─────────────────────────────────────────────────

def safe_str(val, default: str = "—") -> str:
    """Return string value or default if None/empty."""
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def resolve(data: dict, path: str, default="—") -> str:
    """Resolve a dotted path in a nested dict, e.g. 'script.logline'."""
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


def fill_template(template: str, project_state: dict) -> str:
    """Replace all {{placeholder}} markers in template with values from project state."""
    import re

    # ── Section-level variables (top-level project fields) ──
    project = project_state.get("project", {})
    script = project_state.get("script", {})
    script_meta = script.get("_meta", {})
    director_notes = project_state.get("director_notes", {})

    replacements = {
        "project.title": safe_str(project.get("title")),
        "project.scene_type": safe_str(project.get("scene_type")),
        "project.duration_est": safe_str(project.get("duration_est")),
        "project.aspect_ratio": safe_str(project.get("aspect_ratio"), "16:9"),
        "project.language": safe_str(project.get("language"), "zh-CN"),
        "script.logline": safe_str(script.get("logline")),
        "script.structure": safe_str(script.get("structure")),
        "script._meta.writer_revision": safe_str(script_meta.get("writer_revision"), "1"),
        "script._meta.dp_revision": safe_str(script_meta.get("dp_revision"), "1"),
        "script._meta.director_approved": safe_str(script_meta.get("director_approved"), "false"),
        "_version": VERSION,
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # ── Process {{#each script.scenes}}...{{/each}} blocks ──
    scenes = script.get("scenes", [])

    def expand_each_block(text: str, array_key: str) -> str:
        """Expand a {{#each array_key}}...{{/each}} block for array items.
        
        Template placeholders use the item's field names directly:
          {{scene_id}} → item["scene_id"]
          {{camera.shot_type}} → item["camera"]["shot_type"]
          {{#if vfx_notes}}...{{/if}} → show block only if field is truthy
        """
        pattern = re.compile(
            r"\{\{#each\s+" + re.escape(array_key) + r"\s*\}\}(.*?)\{\{/each\}\}",
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            return text
        block_template = match.group(1)
        array = project_state
        for k in array_key.split("."):
            array = array.get(k, []) if isinstance(array, dict) else []
        if not isinstance(array, list):
            array = []
        expanded_parts = []
        for item in array:
            block = block_template
            
            def replace_placeholder(m):
                """Replace {{a.b.c}} with nested dict value from item."""
                inner = m.group(1).strip()
                
                # Handle {{#if field}}...{{/if}} — process these later
                if inner.startswith("#"):
                    return m.group(0)  # pass through
                
                # Resolve dotted path within item
                parts = inner.split(".")
                val = item
                for p in parts:
                    if isinstance(val, dict):
                        val = val.get(p)
                    else:
                        val = None
                        break
                if val is None:
                    val = ""
                return safe_str(val, "—")
            
            # Replace all {{placeholder}} patterns
            block = re.sub(r"\{\{(.+?)\}\}", replace_placeholder, block)
            
            # Handle conditional blocks: {{#if field}}content{{/if}}
            def replace_if_block(m):
                field_name = m.group(1).strip()
                body = m.group(2)
                # Resolve dotted field from item
                parts = field_name.split(".")
                val = item
                for p in parts:
                    if isinstance(val, dict):
                        val = val.get(p)
                    else:
                        val = None
                        break
                return body if val else ""
            
            block = re.sub(
                r"\{\{#if\s+(.+?)\}\}(.*?)\{\{/if\}\}",
                replace_if_block,
                block,
                flags=re.DOTALL,
            )
            expanded_parts.append(block)
        return text[: match.start()] + "".join(expanded_parts) + text[match.end() :]

    result = template

    # Expand scenes array block
    result = expand_each_block(result, "script.scenes")

    # ── Simple {{placeholder}} substitutions ──
    for key, val in replacements.items():
        result = result.replace(f"{{{{{key}}}}}", str(val))

    # Clean up any remaining {{#if}} or {{#each}} that weren't processed
    result = re.sub(r"\{\{#if\s+\S+\}\}.*?\{\{/if\}\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{\{#each\s+\S+\}\}.*?\{\{/each\}\}", "", result, flags=re.DOTALL)

    return result


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Format Project State JSON → Hollywood shooting script (Markdown)"
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
        "--template", "-t",
        type=str,
        default=None,
        help="Path to custom script template (default: assets/templates/script.md)",
    )
    args = parser.parse_args()

    # Resolve template path
    if args.template:
        template_path = args.template
    else:
        # Default: look for template relative to this script
        script_dir = Path(__file__).resolve().parent.parent
        template_path = str(script_dir / "assets" / "templates" / "script.md")

    # Load project state
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            project_state = json.load(f)
    else:
        project_state = json.load(sys.stdin)

    # Load template
    template = load_template(template_path)

    # Fill template
    output = fill_template(template, project_state)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Script written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
