# {{project.title}} — Creative Pack

> **Muse Video Skill 创作包**
> 本文件是完整的视频前期策划产出，包含剧本、分镜、美术方向、声音设计和下游工具提示词。
> 可导入 ComfyUI / HyperFrames / Kling / Runway 等下游工具执行制作。

---

<!--
  模板说明：
  - 本模板由 prompt_assembler.py 读取并填充。
  - 完整的 Project State JSON → Creative Pack Markdown。
  - 所有节映射到 Project State JSON 的顶层字段。
-->

## 1. 项目概要

| 项目 | 内容 |
|------|------|
| **标题** | {{project.title}} |
| **类型** | {{project.scene_type}} |
| **画幅** | {{project.aspect_ratio}} |
| **预估时长** | {{project.duration_est}} |
| **风格** | {{project.genre}} |
| **平台** | {{project.platform}} |
| **语种** | {{project.language}} |

---

## 2. 导演阐述

> **Vision**：{{director_notes.vision}}

| 维度 | 内容 |
|------|------|
| **情绪基调** | {{director_notes.tone}} |

### 创作约束
{{#each director_notes.constraints}}
- {{this}}
{{/each}}

### 关键决策
{{#each director_notes.decisions}}
- **Phase {{phase}}**：{{decision}}（理由：{{rationale}}）
{{/each}}

---

## 3. 剧本

> **Logline**：{{script.logline}}
> **叙事结构**：{{script.structure}}

### 场景分解

{{#each script.scenes}}

#### 第 {{scene_id}} 场 — {{scene_title}}（{{duration}}）

**地点**：{{location}} · **时间**：{{time_of_day}}

**动作**：{{action}}

**对白**：{{dialogue}}

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| {{camera.shot_type}} | {{camera.movement}} | {{camera.lens}} | {{camera.lighting}} | {{vfx_notes}} | {{sound_notes}} |

{{/each}}

---

## 4. 视觉开发

> **视觉基调**：{{visual_dev.mood}}

### 色调方案
{{#each visual_dev.palette}}
| `{{hex}}` | **{{name}}** | {{usage}} |
{{/each}}

### 风格参考
{{#each visual_dev.style_refs}}
- **{{ref_type}}** — *{{name}}*：{{description}}
{{/each}}

### 角色设定
{{#each visual_dev.characters}}

#### {{name}}（{{role}}）
| 项目 | 内容 |
|------|------|
| **视觉特征** | {{traits}} |
| **情绪方向** | {{mood}} |
| **一致性要点** | {{consistency_notes}} |
| **生图提示词** | `{{ref_image_prompt}}` |

{{/each}}

### 参考图
{{#each visual_dev.image_refs}}
- `{{prompt}}` → {{generated_url}}（{{#if approved}}✅ 通过{{else}}⏳ 待审核{{/if}}）
{{/each}}

---

## 5. 摄影指导

| 维度 | 方向 |
|------|------|
| **摄影风格** | {{cinematography.camera_style}} |
| **灯光哲学** | {{cinematography.lighting_philosophy}} |
| **焦段偏好** | {{cinematography.lens_preference}} |
| **色调调色** | {{cinematography.color_grading}} |
| **运镜语言** | {{cinematography.movement_language}} |

---

## 6. 声音设计

| 维度 | 方向 |
|------|------|
| **配乐风格** | {{sound.music_style}} |
| **参考曲目** | {{#each sound.music_refs}}{{this}}, {{/each}} |
| **音效备注** | {{#each sound.sfx_notes}}- {{this}}\\n{{/each}} |
| **旁白基调** | {{sound.narration_tone}} |
| **旁白语言** | {{sound.narration_language}} |
| **静默运用** | {{sound.silence_usage}} |

---

## 7. 视觉特效

| 技法 | 用途 | 涉及场景 |
|------|------|----------|
| {{#each vfx.techniques}}{{name}} | {{usage}} | {{scene_ids}} |
{{/each}}

### 转场设计
{{#each vfx.transitions}}
- 第 {{from_scene}} 场 → 第 {{to_scene}} 场：**{{type}}** — {{description}}
{{/each}}

### 材质清单
{{#each vfx.materials}}
- **{{name}}**：{{properties}}（场景 {{scene_ids}}）
{{/each}}

---

## 8. 分镜

> **总镜数**：{{_panels_count}} | **网格布局**：{{_grid_layout}}

{{#each storyboard}}

### Panel {{panel_id}} — 第 {{scene_id}} 场（{{layout}}）

| 项目 | 内容 |
|------|------|
| **描述** | {{description}} |
| **提示词** | `{{prompt}}` |
| **生成图** | {{generated_url}} |
| **状态** | {{#if approved}}✅{{else}}⏳{{/if}} |

{{/each}}

---

## 9. 最终调优备注

{{#each tuning_notes}}
- **[{{priority}}] {{category}}**：{{note}}
{{/each}}

---

## 10. 下游工具对接

### ComfyUI 工作流
```json
{{creative_pack.comfyui_workflow}}
```

### HyperFrames 配置
```json
{{creative_pack.hyperframes_config}}
```

### Kling 提示词
{{#each creative_pack.kling_prompts}}
- {{this}}
{{/each}}

### Runway 提示词
{{#each creative_pack.runway_prompts}}
- {{this}}
{{/each}}

---

## 元信息

| 字段 | 值 |
|------|-----|
| **生成时间** | {{_generated_at}} |
| **生成工具** | Muse Video Skill — prompt_assembler.py v{{_version}} |
| **编剧审核** | {{script._meta.director_approved}} |
| **美术审核** | {{visual_dev._meta.director_approved}} |
| **摄影审核** | {{cinematography._meta.director_approved}} |
| **声音审核** | {{sound._meta.director_approved}} |
| **特效审核** | {{vfx._meta.director_approved}} |
| **分镜审核** | {{_storyboard_approved}} |
