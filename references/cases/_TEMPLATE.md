# _TEMPLATE.md — 案例拆解模板

> 使用说明：复制此文件为 `references/cases/<id>.md`，按模板填写。
> 完成后运行 `python scripts/build_index.py --check && python scripts/build_index.py --write` 自动更新 INDEX.md。
>
> **写作原则**：
> - 每个角色段落用「技法名称：具体表现」的格式，让 Agent 能直接提取为角色 prompt 注入。
> - 避免泛泛而谈（「色调很美」→ 无效）。给出可操作参数（「主色 #B85C38，强调暖橙与深蓝黑的对比」→ 有效）。
> - 每个技法标注「适用场景」，让 Agent 知道什么时候引用这段。
> - YAML frontmatter 中的技法名尽量简短（2-6 字），与已有案例命名保持一致（`--check` 会检测相似名称）。
>
> **Frontmatter 字段说明**：
> - `type` — film / commercial / short-film / music-video / experimental / animation / documentary / logo-animation
> - `primary_scene` / `secondary_scene` — 从 SKILL.md §路由决策树 定义的场景类型中选择。运行 `python scripts/build_index.py --list-scenes` 查看当前可用值。primary 自动视为 strong 关联，secondary 自动视为 reference。
> - `primary_scene` / `secondary_scene` 只能从 SKILL.md 路由树定义的场景类型中选择，`--check` 会拒绝非法值。
> - `techniques.creative` — 仅 commercial 类型填写，其他类型留 `[]`
> - `styles` — 风格标签，格式 `[cyberpunk, epic, dreamy]`，可自由命名，`--check` 会输出已有风格
> - `scene_relations.extra_strong/extra_reference` — 在 primary/secondary 之外的额外场景关联，通常留 `[]`

***

# 【案例名称】— 【一句话定位】

---
id: SHORT-ID
name: "作品完整名称（中文/原文）"
type: film
year: 'YYYY'
director: "导演/工作室"
primary_scene: studio-ad
secondary_scene: studio-ad
tags:
  - 关键词1
  - 关键词2

techniques:
  narrative:
    - 技法1
    - 技法2
  cinematography:
    - 技法1
    - 技法2
  color:
    - 技法1
  vfx:
    - 技法1
  sound:
    - 技法1
  creative: []

styles: []

scene_relations:
  extra_strong: []
  extra_reference: []

---

## 元信息

| 字段 | 值 |
|------|-----|
| ID | 短标识符，如 `BR2049` |
| 名称 | 作品完整名称（中文/原文） |
| 类型 | film / commercial / short-film / music-video / experimental / animation / documentary / logo-animation |
| 年份 | YYYY |
| 导演/工作室 | |
| 摄影师 | |
| 时长 | mm:ss |
| 品牌/客户 | （广告片必填） |
| 关键词 | 逗号分隔，3-5个 |
| 主场景 | 从 SKILL.md §路由决策树 定义的场景类型中选择。运行 `build_index.py --list-scenes` 查看可用值。 |
| 辅场景 | 同上 |
| 观看链接 | URL（可选但强烈建议） |

---

## 技法标签

> 此处为正文的技法概述（可包含详细描述）。INDEX.md 的交叉引用数据来源于上方 YAML frontmatter 的 `techniques:` 字段。
> frontmatter 中技法名保持简短（2-6 字），此处可展开说明。

- **叙事**：
- **镜头**：
- **色彩**：
- **特效**：
- **声音**：
- **广告创意**：（广告片专属标签）

---

## 叙事技法（→ Writer）

> 用「技法名：具体表现 + 可操作参数」的格式。每个技法一段。

### 【技法名】

- **表现**：（在这场戏/这个段落中具体发生了什么）
- **手法**：（创作者用了什么技术/结构）
- **可迁移**：（在做类似项目时可以怎么用这个技法）
- **适用场景**：（studio-ad / sci-fi / product-demo / ...）

### 【技法名】

...（每个案例建议 2-4 个叙事技法）

---

## 镜头语言（→ DP）

> 格式同上。聚焦：机位、运动、灯光、构图、景深、画幅比。

### 【技法名】

- **表现**：
- **技术参数**：（景别 / 运动方式 / 镜头焦段 / 灯光设置）
- **可迁移**：
- **适用场景**：

...（每个案例建议 3-5 个镜头技法）

---

## 色彩/美术（→ Art Director）

> 格式：用表格呈现场景→色彩的对应关系。每个场景附加情绪关键词。

| 场景/段落 | 主色 (hex) | 辅色 (hex) | 情绪 | 设计理由 |
|-----------|-----------|-----------|------|---------|
| | `#XXXXXX` | `#XXXXXX` | | |

### 世界观/场景设计要点

- （美术风格的核心原则）
- （道具/服装/环境的标志性元素）

---

## 特效语言（→ VFX）

### 【技法名】

- **表现**：
- **实现思路**：（CG / 实拍合成 / 粒子系统 / ...）
- **可迁移**：

...（每个案例建议 2-3 个特效技法）

---

## 声音设计（→ Sound Designer）

### 【技法名】

- **表现**：
- **声音层次**：（对白 / 环境 / 音乐 / 音效的比例关系）
- **可迁移**：

...（每个案例建议 2-3 个声音设计技法）

---

## 创意策略（→ 广告片专属）

> 仅 commercial 类型填写。聚焦：品牌信息、受众心理、记忆点设计。

### 【策略名】

- **表现**：
- **品牌目的**：
- **可迁移**：

---

## 适用提示

> Agent 加载此案例时，先读这段，快速判断是否适用于当前项目。

- **最佳匹配场景**：（什么时候最应该引用这个案例）
- **不适用场景**：（什么时候不应该引用）
- **引用优先级**：（核心引用 / 补充参考 / 特定技法借用）

---

## 参考资源

- 幕后花絮：
- 导演访谈：
- 技术解析文章：
- 拉片视频：

***

## 拉片附录（→ 精确复刻）

> **仅高质量案例填写。** 用户认定案例质量极高时，Agent 进行逐镜头深层录入。
> 设计规范见 `references/pull-sheet-implementation.md`。

### 镜头序列总览（按场景分组）

```markdown
### 场景1: 【场景名称】（【时间码起止】）
| # | 时间码 | 时长 | 景别 | 构图 | 运镜 | 色调+场景 | 角色 | 音效 | 叙事功能 | 特效 | 分镜图 |
|---|--------|------|------|------|------|----------|------|------|----------|------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 场景2: ...
```

> 列名说明：时间码/景别/构图/运镜/色调+场景/音效/叙事功能/角色/特效 — 与拆解管线（default.md 2.5b）字段一致。时长=派生值，分镜图=逐镜头截图。

### 叙事节奏（→ Writer）

（每场景镜头时长分布 / 节奏曲线 / 叙事功能标记）

### 镜头语言序列（→ DP）

（全片景别序列 / 构图模式 / 运镜方式 / 焦距选择）

### 色调+场景搭建序列（→ Art Director）

（逐场景调色参数 / 光源方向 / 空间布局 / 核心道具 / 视觉重心）

### 角色设计序列（→ Writer + Art Director + DP + Sound）

（如有角色——视觉特征 / 出场方式 / 配色关系 / 声音线索）

### 音效序列（→ Sound）

（配乐风格变化 / 音效类型 / 无声段落 / 节奏断点）

### 特效序列（→ VFX）

（转场类型 / 特效时机 / 粒子/材质标注）

### 分镜精选帧

| # | 对应镜头 | 时间码 | 技法要点 | 路径 |
|---|---------|--------|---------|------|
| 1 | ... | ... | ... | assets/CASE-ID/frame_XX.jpg |

> 分镜图存储于 `references/cases/assets/<CASE-ID>/`，案例文件用相对路径引用。
> 数量按视频实际，覆盖全部核心场景和关键技法处。
