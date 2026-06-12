#!/usr/bin/env python3
"""
Muse Video Skill — prompt_assembler.py
Input:  Full Project State JSON (stdin or --input file)
Output: Creative Pack JSON + Markdown — the final deliverable

Role: One job — assemble all role outputs into a unified Creative Package.
      Runs format_script.py and storyboard_grid.py as sub-steps,
      then merges everything with the creative-pack.md template.

Schema-driven: reads all sections from Project State JSON.
No scene-type-specific logic. No role inter-communication.
"""

import json
import sys
import os
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"

# ─── helpers ──────────────────────────────────────────────────────────────────

def safe_str(val, default: str = "—") -> str:
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def safe_list(val) -> list:
    """Ensure val is a list."""
    if isinstance(val, list):
        return val
    return []


def resolve_path(data: dict, dotted_path: str, default=None):
    """Resolve dotted path in nested dict."""
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


# ─── template engine (shared with format_script) ───────────────────────────────

def fill_template(template: str, project_state: dict) -> str:
    """Replace all {{placeholder}} and {{#each}} markers in template."""
    project = project_state.get("project", {})
    script = project_state.get("script", {})
    visual_dev = project_state.get("visual_dev", {})
    cinematography = project_state.get("cinematography", {})
    sound = project_state.get("sound", {})
    vfx = project_state.get("vfx", {})
    storyboard = project_state.get("storyboard", [])
    director_notes = project_state.get("director_notes", {})
    tuning_notes = project_state.get("tuning_notes", [])
    creative_pack = project_state.get("creative_pack", {})

    if not isinstance(storyboard, list):
        storyboard = []

    # ── Simple replacements ──
    simple = {
        "project.title": safe_str(project.get("title")),
        "project.scene_type": safe_str(project.get("scene_type")),
        "project.duration_est": safe_str(project.get("duration_est")),
        "project.aspect_ratio": safe_str(project.get("aspect_ratio"), "16:9"),
        "project.genre": safe_str(project.get("genre")),
        "project.platform": safe_str(project.get("platform")),
        "project.language": safe_str(project.get("language"), "zh-CN"),
        "director_notes.vision": safe_str(director_notes.get("vision")),
        "director_notes.tone": safe_str(director_notes.get("tone")),
        "script.logline": safe_str(script.get("logline")),
        "script.structure": safe_str(script.get("structure")),
        "script._meta.director_approved": safe_str(
            resolve_path(script, "_meta.director_approved", "false")
        ),
        "visual_dev.mood": safe_str(visual_dev.get("mood")),
        "visual_dev._meta.director_approved": safe_str(
            resolve_path(visual_dev, "_meta.director_approved", "false")
        ),
        "cinematography.camera_style": safe_str(cinematography.get("camera_style")),
        "cinematography.lighting_philosophy": safe_str(cinematography.get("lighting_philosophy")),
        "cinematography.lens_preference": safe_str(cinematography.get("lens_preference")),
        "cinematography.color_grading": safe_str(cinematography.get("color_grading")),
        "cinematography.movement_language": safe_str(cinematography.get("movement_language")),
        "cinematography._meta.director_approved": safe_str(
            resolve_path(cinematography, "_meta.director_approved", "false")
        ),
        "sound.music_style": safe_str(sound.get("music_style")),
        "sound.narration_tone": safe_str(sound.get("narration_tone")),
        "sound.narration_language": safe_str(sound.get("narration_language")),
        "sound.silence_usage": safe_str(sound.get("silence_usage")),
        "sound._meta.director_approved": safe_str(
            resolve_path(sound, "_meta.director_approved", "false")
        ),
        "vfx._meta.director_approved": safe_str(
            resolve_path(vfx, "_meta.director_approved", "false")
        ),
        "_version": VERSION,
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_panels_count": str(len(storyboard)),
        "_grid_layout": "2×3" if len(storyboard) <= 6 else "3×3",
        "_storyboard_approved": str(
            all(p.get("approved", False) for p in storyboard) if storyboard else False
        ),
    }

    def replace_placeholder(m):
        inner = m.group(1).strip()
        if inner.startswith("#"):
            return m.group(0)  # pass through for #each / #if
        return simple.get(inner, m.group(0))

    result = re.sub(r"\{\{(.+?)\}\}", replace_placeholder, template)

    # ── Expand {{#each array}}...{{/each}} blocks ──
    def expand_each(text: str, array_key: str, array_data: list) -> str:
        pattern = re.compile(
            r"\{\{#each\s+" + re.escape(array_key) + r"\s*\}\}(.*?)\{\{/each\}\}",
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            return text
        block_tmpl = match.group(1)
        parts = []
        for item in array_data:
            block = block_tmpl
            block = _fill_item_block(block, item)
            parts.append(block)
        return text[: match.start()] + "".join(parts) + text[match.end() :]

    def _fill_item_block(block: str, item: dict) -> str:
        """Replace {{field}} / {{sub.field}} / {{#if field}}...{{/if}} in a single item block."""

        def _repl(m):
            inner = m.group(1).strip()
            if inner.startswith("#if"):
                return m.group(0)  # handle separately
            if inner.startswith("#each"):
                return m.group(0)
            parts_inner = inner.split(".")
            val = item
            for p in parts_inner:
                if isinstance(val, dict):
                    val = val.get(p)
                else:
                    val = None
                    break
            if val is None:
                return ""
            if isinstance(val, list):
                return ", ".join(str(x) for x in val)
            return safe_str(val, "—")

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

        block = re.sub(
            r"\{\{#if\s+(.+?)\}\}(.*?)\{\{/if\}\}",
            _repl_if,
            block,
            flags=re.DOTALL,
        )
        return block

    # Expand each array section
    result = expand_each(result, "director_notes.constraints",
                         [{"this": c} for c in safe_list(director_notes.get("constraints"))])
    result = expand_each(result, "director_notes.decisions",
                         safe_list(director_notes.get("decisions")))
    result = expand_each(result, "script.scenes",
                         safe_list(script.get("scenes")))
    result = expand_each(result, "visual_dev.palette",
                         safe_list(visual_dev.get("palette")))
    result = expand_each(result, "visual_dev.style_refs",
                         safe_list(visual_dev.get("style_refs")))
    result = expand_each(result, "visual_dev.characters",
                         safe_list(visual_dev.get("characters")))
    result = expand_each(result, "visual_dev.image_refs",
                         safe_list(visual_dev.get("image_refs")))
    result = expand_each(result, "sound.music_refs",
                         [{"this": r} for r in safe_list(sound.get("music_refs"))])
    result = expand_each(result, "sound.sfx_notes",
                         [{"this": n} for n in safe_list(sound.get("sfx_notes"))])
    result = expand_each(result, "vfx.techniques",
                         safe_list(vfx.get("techniques")))
    result = expand_each(result, "vfx.transitions",
                         safe_list(vfx.get("transitions")))
    result = expand_each(result, "vfx.materials",
                         safe_list(vfx.get("materials")))
    result = expand_each(result, "storyboard", storyboard)
    result = expand_each(result, "tuning_notes",
                         safe_list(tuning_notes))
    result = expand_each(result, "creative_pack.kling_prompts",
                         [{"this": p} for p in safe_list(creative_pack.get("kling_prompts"))])
    result = expand_each(result, "creative_pack.runway_prompts",
                         [{"this": p} for p in safe_list(creative_pack.get("runway_prompts"))])

    # Cleanup unexpanded {{#each}} / {{#if}} blocks
    result = re.sub(r"\{\{#each\s+\S+?\}\}.*?\{\{/each\}\}", "", result, flags=re.DOTALL)
    result = re.sub(r"\{\{#if\s+\S+?\}\}.*?\{\{/if\}\}", "", result, flags=re.DOTALL)

    return result


# ─── downstream prompt generators ────────────────────────────────────────────

def build_comfyui_workflow(project_state: dict) -> dict:
    """Generate a ComfyUI-compatible workflow skeleton from Project State."""
    storyboard = project_state.get("storyboard", [])
    visual_dev = project_state.get("visual_dev", {})
    project = project_state.get("project", {})

    nodes = []
    palette = visual_dev.get("palette", [])
    palette_hex = [p.get("hex", "#ffffff") for p in palette] if palette else ["#ffffff"]

    for i, panel in enumerate(storyboard):
        nodes.append({
            "id": i + 1,
            "type": "KSampler",
            "inputs": {
                "positive": panel.get("prompt", ""),
                "negative": "ugly, blurry, low quality, distorted",
                "steps": 30,
                "cfg": 7.5,
                "sampler_name": "euler_ancestral",
                "scheduler": "normal",
                "denoise": 0.75,
            },
            "meta": {
                "panel_id": panel.get("panel_id", i),
                "scene_id": panel.get("scene_id"),
            },
        })

    return {
        "schema_version": "1.0",
        "generator": f"Muse Video Skill v{VERSION}",
        "project": project.get("title", "Untitled"),
        "aspect_ratio": project.get("aspect_ratio", "16:9"),
        "palette": palette_hex,
        "nodes": nodes,
    }


def build_hyperframes_config(project_state: dict) -> dict:
    """Generate a HyperFrames composition config from Project State."""
    project = project_state.get("project", {})
    script = project_state.get("script", {})
    visual_dev = project_state.get("visual_dev", {})
    storyboard = project_state.get("storyboard", [])

    scenes_cfg = []
    for scene in safe_list(script.get("scenes")):
        scenes_cfg.append({
            "id": scene.get("scene_id"),
            "title": scene.get("scene_title", "Untitled"),
            "duration": scene.get("duration", "5s"),
            "camera": scene.get("camera", {}),
        })

    return {
        "schema_version": "1.0",
        "generator": f"Muse Video Skill v{VERSION}",
        "project": project.get("title", "Untitled"),
        "aspect_ratio": project.get("aspect_ratio", "16:9"),
        "duration_est": project.get("duration_est", "30s"),
        "mood": visual_dev.get("mood", ""),
        "palette": [p.get("hex", "") for p in safe_list(visual_dev.get("palette"))],
        "panels_count": len(storyboard),
        "scenes": scenes_cfg,
    }


def build_kling_prompts(project_state: dict) -> list:
    """Generate Kling video prompts from storyboard panels."""
    storyboard = project_state.get("storyboard", [])
    project = project_state.get("project", {})
    prompts = []
    for panel in storyboard:
        base = panel.get("prompt", "")
        camera = panel.get("camera_notes", "")
        prompt = (
            f"{base}. Camera: {camera}. "
            f"Aspect ratio: {project.get('aspect_ratio', '16:9')}. "
            f"Cinematic quality, 4K, smooth motion."
        )
        prompts.append(prompt)
    return prompts


def build_runway_prompts(project_state: dict) -> list:
    """Generate Runway Gen-3 prompts from storyboard panels."""
    storyboard = project_state.get("storyboard", [])
    visual_dev = project_state.get("visual_dev", {})
    prompts = []
    for panel in storyboard:
        base = panel.get("prompt", "")
        mood = visual_dev.get("mood", "")
        prompt = f"{base}. Mood: {mood}. Cinematic, high production value."
        prompts.append(prompt)
    return prompts


# ─── main assembler ──────────────────────────────────────────────────────────

def assemble(project_state: dict) -> dict:
    """Main assembly function: Project State JSON → Creative Pack dict."""
    # Build downstream tool configs
    comfyui = build_comfyui_workflow(project_state)
    hyperframes = build_hyperframes_config(project_state)
    kling_prompts = build_kling_prompts(project_state)
    runway_prompts = build_runway_prompts(project_state)

    # Store in creative_pack section
    project_state.setdefault("creative_pack", {})
    project_state["creative_pack"]["comfyui_workflow"] = comfyui
    project_state["creative_pack"]["hyperframes_config"] = hyperframes
    project_state["creative_pack"]["kling_prompts"] = kling_prompts
    project_state["creative_pack"]["runway_prompts"] = runway_prompts

    return project_state


def render_markdown(project_state: dict, template_path: str | None = None) -> str:
    """Render Creative Pack as Markdown using the creative-pack.md template."""
    if template_path:
        p = Path(template_path)
        if p.exists():
            template = p.read_text(encoding="utf-8")
        else:
            template = _fallback_template()
    else:
        script_dir = Path(__file__).resolve().parent.parent
        tpl_path = script_dir / "assets" / "templates" / "creative-pack.md"
        if tpl_path.exists():
            template = tpl_path.read_text(encoding="utf-8")
        else:
            template = _fallback_template()

    # Serialize creative_pack sub-objects as JSON strings for template rendering
    cp = project_state.get("creative_pack", {})
    state_for_render = dict(project_state)
    state_for_render["creative_pack"] = dict(cp)
    state_for_render["creative_pack"]["comfyui_workflow"] = json.dumps(
        cp.get("comfyui_workflow", {}), indent=2, ensure_ascii=False
    )
    state_for_render["creative_pack"]["hyperframes_config"] = json.dumps(
        cp.get("hyperframes_config", {}), indent=2, ensure_ascii=False
    )

    return fill_template(template, state_for_render)


def _fallback_template() -> str:
    """Minimal built-in template if creative-pack.md is unavailable."""
    return """# {{project.title}} — Creative Pack

## Project
- Title: {{project.title}}
- Type: {{project.scene_type}}
- Duration: {{project.duration_est}}
- Aspect: {{project.aspect_ratio}}

## Director's Vision
{{director_notes.vision}}

## Script
**Logline:** {{script.logline}}
**Structure:** {{script.structure}}

{{#each script.scenes}}
### Scene {{scene_id}} — {{scene_title}}
{{action}}

{{/each}}

## Storyboard ({{_panels_count}} panels)
{{#each storyboard}}
- Panel {{panel_id}}: {{description}}
{{/each}}

Generated by Muse Video Skill v{{_version}} at {{_generated_at}}
"""


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Muse Video Skill — Assemble Project State JSON → Creative Package"
    )
    parser.add_argument(
        "--input", "-i", type=str, default=None,
        help="Path to Project State JSON file (default: stdin)",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file path for Creative Pack JSON (default: stdout)",
    )
    parser.add_argument(
        "--markdown", "-m", type=str, default=None,
        help="Output file path for Creative Pack Markdown (optional)",
    )
    parser.add_argument(
        "--template", "-t", type=str, default=None,
        help="Path to custom creative-pack template (default: assets/templates/creative-pack.md)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "both"],
        default="json",
        help="Output format: json (Creative Pack JSON), markdown, or both",
    )
    args = parser.parse_args()

    # Load Project State
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            project_state = json.load(f)
    else:
        project_state = json.load(sys.stdin)

    # Assemble
    assembled = assemble(project_state)

    # Output JSON
    if args.format in ("json", "both"):
        json_output = json.dumps(assembled, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"✅ Creative Pack JSON → {args.output}", file=sys.stderr)
        else:
            print(json_output)

    # Output Markdown
    if args.format in ("markdown", "both"):
        md_output = render_markdown(assembled, args.template)
        if args.markdown:
            with open(args.markdown, "w", encoding="utf-8") as f:
                f.write(md_output)
            print(f"✅ Creative Pack Markdown → {args.markdown}", file=sys.stderr)
        elif args.format == "markdown":
            print(md_output)
        elif args.format == "both" and not args.markdown:
            # If both but no separate markdown path, append after JSON
            if not args.output:
                print("\n---\n")
                print(md_output)


if __name__ == "__main__":
    main()
