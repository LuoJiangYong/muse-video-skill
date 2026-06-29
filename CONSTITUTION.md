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
│   ├── cases/                   ← Case studies: films + commercials analyzed by role dimension.
│   │   ├── INDEX.md             # Multi-dimensional cross-reference (技法×场景×风格×角色)
│   │   ├── _TEMPLATE.md         # Case file template — copy and fill for each new case
│   │   ├── BR2049.md            # Blade Runner 2049 — cyberpunk visual language
│   │   └── ...                  # One file per case, infinite expansion
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
│   ├── build_index.py           # Auto-generate INDEX.md from case YAML frontmatter
│   ├── inventory.py             # Dynamic file registry — replaces static registry.yaml
│   ├── format_script.py         # Input: scene array → Output: formatted shooting script
│   ├── storyboard_grid.py       # Input: storyboard array → Output: grid layout (2×3, 3×3)
│   ├── prompt_assembler.py      # Input: full Project State → Output: Creative Pack JSON
│   ├── moodboard_compare.py     # Input: 2+ visual directions → Output: comparison matrix
│   ├── export_html.py           # Input: Project State JSON → Output: literary script HTML
│   └── export_xlsx.py           # Input: Project State JSON → Output: tech breakdown Excel
│
├── assets/                      ← TEMPLATES, SCHEMAS, EXAMPLES, FONTS.
│   ├── templates/               ← Output templates. Agent fills in the blanks.
│   │   ├── script.md            # Shooting script template
│   │   ├── storyboard.md        # Storyboard panel template
│   │   ├── creative-pack.md     # Final deliverable template
│   │   └── export/              ← Export format templates (JSON → human-readable)
│   │       ├── script-literary.html     # Literary script HTML (Courier, industry-standard)
│   │       ├── script-storyboard.html   # Storyboard gallery HTML (card grid)
│   │       └── script-tech.xlsx         # Technical breakdown Excel (camera, lighting, VFX)
│   │
│   ├── schemas/                 ← Data contracts.
│   │   └── project-state.json   # Project State JSON Schema (THE interface between roles)
│   │
│   └── examples/                ← Real-world complete examples. Grows with usage.
│       ├── studio-ad-full/      # Complete studio ad project (all phases)
│       └── sci-fi-short/        # Complete sci-fi short project (all phases)
│
├── metadata/                    ← METADATA. Tool-driven, minimal static footprint.
│   ├── fields.yaml              # Field metadata: JSON field → affected roles + phases
│   └── CHANGELOG.md             # Version history with migration guides
│
├── .gitignore
```

---

## Data Flow (The Central Nervous System)

```
USER: "帮我做一支赛博朋克手机广告"
          │
          ▼
┌─────────────────────────────────────────────────────┐
│ SKILL.md — Router                                   │
│ 1. Detect: scene type → route to pipeline           │
│ 2. Load: scenes/<type>.md + pipelines/default.md    │
│ 3. Init: Project State JSON (empty skeleton)        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 1: 需求沟通 (Director)                          │
│ Director interviews user → fills:                    │
│   project.* (aspect_ratio, duration_est, genre,      │
│             tone, platform, audience)                │
│   director_notes.vision, constraints                 │
│   [Optional] 参考视频拆解 → reference_analysis        │
│                                                       │
│ Director 确认 → Phase 2                               │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 2: 内容梳理 (Writer → Director)                 │
│ Writer reads director_notes.vision → produces:       │
│   script.logline, synopsis, narrative_structure      │
│   script.scenes[] (slug/setting/summary)             │
│   script.character_bible[] (如有角色)                 │
│                                                       │
│ Director review → Phase 3                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 3: 视觉开发 (Art Director → Director)           │
│ AD reads vision + scenes → produces:                 │
│   visual_dev.color_palette[] (含 hex + visual_cause) │
│   visual_dev.style_direction, mood_references[]      │
│   visual_dev.scene_composition[] (空间/道具/视觉重心)  │
│   visual_dev.character_design[] (如有角色)            │
│                                                       │
│ Director review → Phase 3.5 (如可用) 或 Phase 4       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 3.5: 风格定样 (条件性 — image_gen 可用时)       │
│ 2-3 场景 moodboard + 角色概念图 (如有)                │
│   → 用户看图确认色调/风格方向                          │
│   → Approved → Phase 4                               │
│   → Revise → 回 Phase 3 调整                          │
│   → image_gen 不可用 → 跳过，显式记录                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 4: 脚本 (Writer → DP → Director)                │
│ Writer 基于 Phase 2 结构补充对白/动作/时长             │
│   → DP 叠加镜头语言 (shot type/movement/lens/light)   │
│   → 产出: script.scenes[].dialogue/action             │
│           cinematography.shot_list/camera_notes       │
│                                                       │
│ Director review → Phase 5                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 5: 声音方向 (Sound Designer → Director)         │
│ SD reads script + tone + visual_dev → produces:      │
│   sound.music_style, sfx_map[], narration_tone       │
│   sound.silence_strategy, reference_tracks[]         │
│                                                       │
│ Director review → Phase 6                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 6: 分镜 (Storyboard Assembly + VFX → Director)  │
│ 集成全部前置产出 → 生成分镜 panel[]                    │
│   每 panel 含: description / camera / lighting        │
│               art_direction / vfx_notes / image_prompt│
│   VFX 为需要特效的 panel 补充材质/粒子/转场            │
│                                                       │
│ Director review → Phase 7                             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ PHASE 7: 组装+调优 (Director)                         │
│ prompt_assembler.py → Creative Pack JSON              │
│ Director: tuning_notes (color/pacing/effects)         │
│ export_html.py / export_xlsx.py → 导出文件            │
│                                                       │
│ OUTPUT: Creative Package → 下游工具对接                │
│   (HyperFrames / ComfyUI / Kling / 火山引擎 / etc.)   │
└──────────────────────────────────────────────────────┘
```

### Key rules of the data flow:

1. **Project State JSON is the ONLY shared state.** Roles never communicate directly. They read state, produce output, write state.
2. **Director is the gatekeeper.** No role output becomes "approved" without Director sign-off.
3. **Max 2 revision loops per phase.** After two rounds of "revise", Director must either approve with notes or restart the phase.
4. **Phases are serial; Phase 4 has an internal chain.** Phases execute one at a time, each building on prior outputs. Within Phase 4 only, Writer → DP is a sequential chain: Writer produces dialogue first, then DP layers cinematography on top. No other phase has internal role chains.
5. **Phase 3.5 is conditional.** Active only when image_gen is available. Skipped otherwise with explicit record. Fast-Track pipeline skips it entirely.
6. **Storyboard is the integration point.** All prior outputs (script, cinematography, visual_dev, vfx) converge into Phase 6 storyboard panels.

---

## Forbidden Patterns (What NOT to Do)

1. **SKILL.md exceeding 3,000 characters.** Cut it. Move content to references/.
2. **Role files referencing other role files.** Roles are independent. Only Director orchestrates.
3. **Hardcoding scene-specific logic in scripts.** Scripts read from Project State JSON, which is schema-driven, not scene-type-aware.
4. **Loading all reference files at start.** Agent must load references ON DEMAND as pipeline phases activate.
5. **Skipping Director review.** Every creative phase ends with Director sign-off. No exceptions, even for fast-track.
6. **Generating actual video/audio.** This Skill produces a Creative PACKAGE (prompts + references + script). Actual generation is delegated to ComfyUI/HyperFrames/Kling/etc.
7. **Inventing project requirements.** If user hasn't specified aspect ratio, genre, or platform — ASK. Director phase is mandatory.
8. **Exceeding 3 revision rounds.** Max 2 rounds of REVISE per phase. After 2 rounds, Director must APPROVE (with conditions) or REJECT.
9. **Putting detailed techniques in SKILL.md.** Techniques belong in references/cases/ or references/roles/, never in SKILL.md.
10. **Citing case techniques without loading the case file.** Always load the case via references/cases/<id>.md before referencing its techniques.
11. **Promising character consistency beyond AI limits.** Be honest: AI character consistency is ~70-80% at best. Never promise 100%.
12. **Manually editing INDEX.md.** INDEX.md is auto-generated by scripts/build_index.py from case YAML frontmatter. Manual edits will be overwritten.

---

## 元数据治理 METADATA GOVERNANCE

> 工具驱动的动态元数据：`scripts/inventory.py` 替代静态 `registry.yaml`，`scripts/build_index.py --check --deps` 替代 `dependencies.yaml`。`metadata/fields.yaml` 保留骨架（enum_values 标注为自动生成）。`metadata/CHANGELOG.md` 保留。

### 三层结构

| 层级 | 工具/文件 | 回答的问题 |
|------|----------|-----------|
| **文件级** | `scripts/inventory.py --json` | 「有哪些文件？按角色如何分类？」 |
| **字段级** | `metadata/fields.yaml` | 「改了 Schema 的 X 字段，哪些角色和阶段会受影响？」 |
| **依赖级** | `scripts/build_index.py --check --deps` | 「改了文件 X，哪些文件引用了它？有无死链接？」 |

### 更新纪律

```
每次 git commit 涉及实质性改动时：

1. 文件增删改 → inventory.py --json 自动反映（无需手动更新）
2. Schema 字段增删改 → 更新 metadata/fields.yaml
   - 新字段：加一行（path + type + default + affected_roles + affected_phases）
   - 删字段：移除对应行 + 标注 breaking_change: true
   - 改字段：更新对应行 + 如果类型变化，标注 breaking_change: true
3. 依赖关系验证 → build_index.py --check --deps
   - 自动检测 references/ 内的死链接（引用不存在的文件）
   - 跳过模板占位符（含 < > 的引用）
4. 版本发布 → 更新 metadata/CHANGELOG.md
   - 记录：新增/修改/删除 + 影响分析 + 迁移指南
```

### 快速查询模板

**「有哪些文件？」**
```bash
python scripts/inventory.py              # 按角色分类的摘要
python scripts/inventory.py --json       # 全量 JSON
python scripts/inventory.py --deps <file>  # 上下游引用
```

**「有无死链接？」**
```bash
python scripts/build_index.py --check --deps
```

**「改了 Schema 的 Y 字段，会影响什么？」**
```bash
# 查 fields.yaml 的 affected_roles → 列出受影响角色
# 查 fields.yaml 的 affected_phases → 列出受影响阶段
```

### 自检清单

- [ ] `inventory.py --json` 输出完整无报错
- [ ] `build_index.py --check --deps` 0 errors + 0 dead links
- [ ] `fields.yaml` 中的字段列表与实际 Schema 同步
- [ ] `CHANGELOG.md` 中最近一条 entry 的版本号与 git tag 一致
- [ ] `SKILL.md` / `CONSTITUTION.md` / `CHANGELOG.md` 三个文件的版本号一致（升版本时最容易漏 SKILL.md）

---

## 版本管理

- This constitution supersedes all prior design documents for this skill.
- Amendments require: (a) documented reason, (b) impact analysis on existing files, (c) commit with `docs: constitution amendment — <reason>`.
- Principle numbers 1-5 are immutable. Sub-sections can evolve.

---

*Last amended: 2026-06-29. Author: Director-Agent (Hermes). v0.29.0 — 数据流图重写：反映实际 7+0.5 阶段串行管线（Phase 1→2→3→3.5→4→5→6→7）；修正"并行阶段"为"串行阶段+Phase 4 内 Writer→DP 链式"；新增 Phase 3.5 条件性子阶段规则。AD 角色文件新增 visual_cause 字段（CHAI 反主观化规则）。继承 v0.28.0 参考视频拆解管线 + 拉片附录 + 全角色消费映射 + character_bible 跨角色闭环。*
