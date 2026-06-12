# {{project.title}} — 分镜

> **场景类型**：`{{project.scene_type}}` | **时长**：`{{project.duration_est}}` | **画幅**：`{{project.aspect_ratio}}`
> **网格布局**：{{_grid_layout}}（{{_panels_count}} 格）

---

<!--
  模板说明：
  - 本模板由 storyboard_grid.py 读取并填充。
  - 支持 2×3（6 格）或 3×3（9 格）两种网格布局。
  - 每个 panel 映射到 Project State JSON 的 storyboard[] 数组。
  - _grid_layout 和 _panels_count 由脚本注入。
-->

## 画面网格

{{#each storyboard}}

### 【Panel {{panel_id}}】— 第 {{scene_id}} 场

| 项目 | 内容 |
|------|------|
| **景别** | {{layout}} |
| **画面描述** | {{description}} |

#### AI 生成提示词
```
{{prompt}}
```

#### 技术备注
| 项目 | 内容 |
|------|------|
| **镜头备注** | {{camera_notes}} |
| **特效备注** | {{vfx_notes}} |
| **关联角色** | {{character_ids}} |
| **参考图** | {{generated_url}} |
| **状态** | {{#if approved}}✅ 已审核{{else}}⏳ 待审核{{/if}} |

| **审核版本** | {{_meta.revision}} |
| **导演审核** | {{_meta.director_approved}} |

---

{{/each}}

## 元信息

| 字段 | 值 |
|------|-----|
| **总镜数** | {{_panels_count}} |
| **网格布局** | {{_grid_layout}} |
| **生成时间** | {{_generated_at}} |
| **生成工具** | Muse Video Skill — storyboard_grid.py v{{_version}} |
