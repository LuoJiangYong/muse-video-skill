# {{project.title}} — 剧本

> **场景类型**：`{{project.scene_type}}` | **时长**：`{{project.duration_est}}` | **画幅**：`{{project.aspect_ratio}}`
> **Logline**：{{script.logline}}
> **叙事结构**：{{script.structure}}
> **语种**：{{project.language}}

---

<!-- 
  模板说明：
  - 本模板由 format_script.py 读取并填充。
  - 占位符格式：{{section.field}}，映射到 Project State JSON。
  - scenes 为数组，脚本需遍历填充每个场景块。
  - _meta 信息用于追溯，避免手动删除。
-->

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

#### 技术备注
| 项目 | 内容 |
|------|------|
| **镜头** | {{camera.shot_type}} |
| **运镜** | {{camera.movement}} |
| **焦段** | {{camera.lens}} |
| **灯光** | {{camera.lighting}} |
| **构图** | {{camera.composition_notes}} |
| **特效** | {{vfx_notes}} |
| **声音** | {{sound_notes}} |

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
