# Muse Video Skill — Design Constitution

> **Muse** = 缪斯，灵感女神。这个 Skill 是天马行空创意的催化剂，不是约束创意的牢笼。

## Five Principles (The Law)

### 1. 高内聚 HIGH COHESION — One file, one job.

- A role's domain knowledge lives in exactly one file under `references/roles/<name>.md`. Never duplicated.
- A scene template is self-contained in `references/scenes/<type>.md`. It imports roles by reference, not by copy-paste.
- A pipeline definition lives in `references/pipelines/<name>.md` and describes WHEN to activate which roles — not HOW each role works.
- Role files know nothing about pipelines. Scene files know nothing about other scenes.
- Scripts under `scripts/` do ONE thing: format_script.py formats scripts, not storyboards.

**Violation signal:** You're pasting the same camera movement table into two role files. → Extract to a shared reference or pick one canonical home.

### 2. 低耦合 LOW COUPLING — Change one without touching others.

- Adding a new scene type (`references/scenes/car-commercial.md`) requires ZERO changes to any role file or pipeline file.
- Changing the Director's review criteria does not affect how the Writer generates scripts.
- The Project State JSON schema is the ONLY interface between roles. Roles read from project state, write to project state. They never call each other directly.
- SKILL.md routes to scenes and pipelines. It does NOT contain scene-specific logic.

**Violation signal:** You add a new role and must edit 3 scene files to make it work. → The role activation should be pipeline-driven, not hardcoded per scene.

### 3. 可扩展 EXTENSIBLE — New capability = new file + one-line registration.

- **New scene type:** Create `references/scenes/<type>.md` + add one entry to the route table in SKILL.md.
- **New role:** Create `references/roles/<name>.md` + add one entry to role activation list in SKILL.md.
- **New pipeline variant:** Create `references/pipelines/<variant>.md`. No other files change.
- **New output format:** Create `assets/templates/<format>.md`. No code changes needed.
- The `assets/examples/` directory grows organically — each completed project adds one example folder.

**Violation signal:** You add a scene type and need to modify `prompt_assembler.py`. → The assembler should be schema-driven, reading from Project State, not scene-type-aware.

### 4. 易维护 MAINTAINABLE — Traceability over cleverness.

- Every creative output in the final package MUST be traceable to the role that produced it.
- Project State JSON is the single source of truth. All roles read from and write to it.
- Each role's output section in Project State includes a `_meta` field: `{ "role": "writer", "revision": 2, "director_approved": true }`.
- Agent prompts are stored as markdown in references, not embedded in code. Non-technical users can read and edit them.
- All file paths are relative to the skill root. No absolute paths, no environment assumptions.

**Violation signal:** You can't tell whether a line of dialogue came from the Writer or was added by the Director. → Missing `_meta` traceability.

### 5. 高效简洁 LEAN — Fewer than 3 consumers? No abstraction.

- If only ONE pipeline phase uses a helper function → inline it in that phase's script.
- If only TWO scene types share a pattern → duplicate it. Extraction is premature until the third consumer.
- Markdown-first. No YAML config files, no JSON schemas, no Python classes — until a real problem demands them.
- `references/` files are loaded by the Agent ON DEMAND. The Agent never loads all role files at once — only the ones needed for the current pipeline phase.
- SKILL.md stays under 3,000 characters (~1,200 tokens). If it grows past that, you're putting reference material in the wrong place.

**Violation signal:** A shared utility module with one caller. → Delete the module, inline the code.

---

## Directory Layout

```
muse-video/
│
├── CONSTITUTION.md              ← THIS FILE. Design law. Read first.
├── SKILL.md                     ← Thin center: routing, decisions, phase triggers. ≤3000 chars.
│
├── references/                  ← THICK RADIATION. Domain knowledge, loaded on demand.
│   ├── roles/                   ← Each role's expertise, prompt templates, quality standards.
│   │   ├── director.md          # Vision setting, review criteria, iteration strategy
│   │   ├── writer.md            # Narrative structures, dialogue craft, emotional pacing
│   │   ├── dp.md                # Camera language, lighting setups, composition grids
│   │   ├── art-director.md      # Color theory, style library, world-building visuals
│   │   ├── vfx.md               # Materials, particles, transitions, compositing
│   │   └── sound-designer.md    # Music direction, SFX mapping, narration tone
│   │
│   ├── scenes/                  ← Scene-type-specific templates and constraints.
│   │   ├── studio-ad.md         # Studio advertising: lighting, camera, props, talent
│   │   ├── logo-animation.md    # Logo motion: material types, dynamic rhythm, brand rules
│   │   ├── product-demo.md      # Product showcase: feature→shot mapping, B-roll, CTA
│   │   └── sci-fi.md            # Sci-fi world-building: tech rules, VFX language, alienation
│   │
│   ├── pipelines/               ← WHEN to activate roles, in what order, with what loop rules.
│   │   ├── default.md           # Standard 7-phase pipeline (full creative process)
│   │   └── fast-track.md        # Accelerated pipeline for simple/single-scene requests
│   │
│   └── media/                   ← Cross-cutting media generation knowledge.
│       ├── image-gen-guide.md   # Prompt engineering for AI image generation
│       ├── character-consistency.md  # Strategies for character consistency (the hard problem)
│       └── tool-matrix.md       # When to use ComfyUI vs Kling vs Runway vs HyperFrames
│
├── scripts/                     ← DETERMINISTIC LOGIC. Agent calls, does not rewrite.
│   ├── format_script.py         # Input: scene array → Output: formatted shooting script
│   ├── storyboard_grid.py       # Input: storyboard array → Output: grid layout (2×3, 3×3)
│   ├── prompt_assembler.py      # Input: full Project State → Output: Creative Pack JSON
│   └── moodboard_compare.py     # Input: 2+ visual directions → Output: comparison matrix
│
├── assets/                      ← TEMPLATES, SCHEMAS, EXAMPLES, FONTS.
│   ├── templates/               ← Output templates. Agent fills in the blanks.
│   │   ├── script.md            # Shooting script template
│   │   ├── storyboard.md        # Storyboard panel template
│   │   └── creative-pack.md     # Final deliverable template
│   │
│   ├── schemas/                 ← Data contracts.
│   │   └── project-state.json   # Project State JSON Schema (THE interface between roles)
│   │
│   └── examples/                ← Real-world complete examples. Grows with usage.
│       ├── studio-ad-full/      # Complete studio ad project (all phases)
│       └── sci-fi-short/        # Complete sci-fi short project (all phases)
│
└── .gitignore
```

---

## Data Flow (The Central Nervous System)

```
USER: "帮我做一支赛博朋克手机广告"
          │
          ▼
┌─────────────────────────────────────────────────────┐
│ SKILL.md — Router                                   │
│ 1. Detect: scene type = studio-ad, mood = cyberpunk │
│ 2. Load: scenes/studio-ad.md + pipelines/default.md │
│ 3. Init: Project State JSON (empty skeleton)        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 1: 需求沟通 (Director)                          │
│ Director role loads → interviews user → fills:       │
│   project.aspect_ratio, duration_est, genre, tone    │
│   director_notes.vision, constraints                 │
│ Output: Project State (phase 1 populated)             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 2-3: 内容梳理 + 视觉开发 (Parallel)             │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│ │ Writer   │  │Art Dir   │  │   DP     │            │
│ │ script   │  │ palette  │  │ camera   │            │
│ │ logline  │  │ mood     │  │ lighting │            │
│ └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│      └──────────────┼─────────────┘                  │
│                     ▼                                │
│              Director Review                         │
│         ┌──────┼──────┐                              │
│      APPROVE REVISE REJECT                           │
│         │      │       │                             │
│         ▼      ▼       ▼                             │
│       继续  角色修改  重新定调                         │
│             (≤2轮loop)                                │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 4-5: 脚本 + 分镜 (Sequential)                   │
│ Director approved script → DP adds camera direction   │
│ → VFX adds effect notes → Storyboard assembly         │
│ → Image generation for key panels → Director review   │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 6-7: 组装 + 调优                                │
│ prompt_assembler.py: Project State → Creative Pack    │
│ Sound Designer: music/SFX/narration references        │
│ Director: final tuning notes (color, pacing, effects) │
│                                                       │
│ OUTPUT: Creative Pack JSON + 分镜图集                  │
│ → User exports to ComfyUI / HyperFrames / Kling       │
└──────────────────────────────────────────────────────┘
```

### Key rules of the data flow:

1. **Project State JSON is the ONLY shared state.** Roles never communicate directly. They read state, produce output, write state.
2. **Director is the gatekeeper.** No role output becomes "approved" without Director sign-off.
3. **Max 2 revision loops per phase.** After two rounds of "revise", Director must either approve with notes or restart the phase.
4. **Parallel phases are truly parallel.** Writer, Art Director, and DP work from the same Director brief simultaneously. They do NOT see each other's outputs until Director review — this preserves creative independence.
5. **Storyboard is the integration point.** All prior outputs converge into the storyboard. Each panel links to: script scene, character, palette, camera direction, VFX note.

---

## Forbidden Patterns (What NOT to Do)

1. **SKILL.md exceeding 3,000 characters.** Cut it. Move content to references/.
2. **Role files referencing other role files.** Roles are independent. Only Director orchestrates.
3. **Hardcoding scene-specific logic in scripts.** Scripts read from Project State JSON, which is schema-driven, not scene-type-aware.
4. **Loading all reference files at start.** Agent must load references ON DEMAND as pipeline phases activate.
5. **Skipping Director review.** Every creative phase ends with Director sign-off. No exceptions, even for fast-track.
6. **Generating actual video/audio.** This Skill produces a Creative PACKAGE (prompts + references + script). Actual generation is delegated to ComfyUI/HyperFrames/Kling/etc.
7. **Inventing project requirements.** If user hasn't specified aspect ratio, genre, or platform — ASK. Director phase is mandatory.

---

## Versioning

- This constitution supersedes all prior design documents for this skill.
- Amendments require: (a) documented reason, (b) impact analysis on existing files, (c) commit with `docs: constitution amendment — <reason>`.
- Principle numbers 1-5 are immutable. Sub-sections can evolve.

---

*Last amended: 2026-06-12. Author: Director-Agent (Hermes).*
