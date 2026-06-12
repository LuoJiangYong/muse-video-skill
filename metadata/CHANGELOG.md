# Changelog — 版本变更日志

> 记录每次修改的动机、内容、影响范围、迁移指南。
> 每次 git commit 涉及实质改动时同步更新此文件。
> 格式：`## [version] — YYYY-MM-DD`

---

## [0.2.0] — 2026-06-12

### 新增 — Phase 2: 角色+场景+管线+媒体（16 个文件）

**管线文档（2 个）**
- `references/pipelines/default.md`：标准 7 阶段管线。每阶段的角色激活表、输入/输出定义、Director 审核触发条件、loop 规则（≤2 轮）、角色激活矩阵
- `references/pipelines/fast-track.md`：快速 3 阶段管线。阶段合并策略（2+3+4→一稿过）、并行执行规则、自动降级条件

**角色文档（6 个）**
- `references/roles/director.md`：Vision 模板（7 个确认项）、审核标准（APPROVE/REVISE/REJECT 判定条件）、迭代策略（≤2 轮 loop）、拍板话术（4 种场景）
- `references/roles/writer.md`：叙事结构库（6 种：三段式/英雄之旅/蒙太奇/问题-解决/反转/情绪递进）、对白技巧、情绪节奏公式、logline 模板
- `references/roles/dp.md`：镜头语言词汇表（8 种 shot types + 11 种 movements + 6 种 lens choices）、灯光方案模板、构图网格（9 种）、运镜决策树
- `references/roles/art-director.md`：情绪→色调映射表（10 种情绪）、风格库（6 种：minimalist/cyberpunk/warm-cinematic/cold-dystopian/dreamy-surreal/gritty-realism）、人物造型 checklist、世界观构建模板
- `references/roles/vfx.md`：材质库（固体/流体/粒子/发光 4 大类 25+ 材质，含 PBR 参数）、转场类型表（12 种+决策树）、合成层级模板、CG vs 实拍判断流程图
- `references/roles/sound-designer.md`：配乐风格库（13 种，含 tempo+instrumentation）、音效分类体系（6 类）、旁白基调选择器、静默部署策略（BR2049 式声音层次）、参考曲目搜索关键词

**场景文档（4 个）**
- `references/scenes/studio-ad.md`：灯光方案（三点布光+减法灯光）、机位模板（5 机位）、道具清单、演员调度、提示词模板。引用 APPLE-WH/APPLE-DB/BR2049
- `references/scenes/product-demo.md`：功能→镜头映射、B-roll 配比公式（按片长）、CTA 时机决策、3 种叙事模板。引用 APPLE-DB/NIKE-YCS/COSMOS-L
- `references/scenes/sci-fi.md`：世界观规则模板、科技一致性检查清单（6 项）、异化美感参数（7 策略+3 强度）、提示词模板。引用 BR2049/COSMOS-L
- `references/scenes/logo-animation.md`：材质-品牌关联表（8 种）、三阶段节奏模型、动态参数速查、品牌色精确匹配规则。引用 NIKE-YCS/APPLE-WH/BR2049

**媒体参考（3 个）**
- `references/media/image-gen-guide.md`：ComfyUI/Flux/SDXL/SD1.5 的 prompt 模板（4 种场景）、参数速查、负面提示词策略、质量检查清单
- `references/media/character-consistency.md`：6 种策略矩阵（种子固定/IP-Adapter/FaceID/LoRA/参考图重投/ControlNet）、诚实能力边界标注、推荐组合策略、用户诚实标注模板
- `references/media/tool-matrix.md`：ComfyUI vs HyperFrames vs Kling vs Runway vs Pika vs Suno 的选择决策树、Creative Package→工具输入映射、成本-质量权衡

### 修改

- `metadata/registry.yaml`：16 个文件 status not_started→complete；修复 default.md↔director.md 的循环依赖（default.md 不再依赖 director.md）

### 影响分析

- 受影响的文件：`metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 受影响的依赖：`SKILL.md` 的 dependents 列表（pipeline + role + scene + media 文件均已就绪）
- 下游影响：无（所有新文件均为新建，不修改已有文件）

### 迁移指南

- 无需迁移。Phase 0-1 的所有文件保持不变。

---

## [0.1.0] — 2026-06-12

### 新增

- **CONSTITUTION.md**：5 条设计宪法 + 完整目录布局 + 数据流图 + 禁止模式清单
- **SKILL.md**：路由中枢（≤3500 chars 正文），包含意图检测、场景路由、管线激活、阶段触发
- **assets/schemas/project-state.json**：项目状态 JSON Schema，所有 6 个角色的唯一共享接口。50 个字段，覆盖 project/director_notes/script/visual_dev/cinematography/sound/vfx/storyboard/creative_pack/tuning_notes
- **references/cases/INDEX.md**：6 表交叉索引（主注册表 + 技法→案例 + 场景→案例 + 风格→案例 + 角色→案例 + 更新 SOP）
- **references/cases/_TEMPLATE.md**：标准化案例拆解模板（按角色维度结构化）
- **references/cases/BR2049.md**：银翼杀手 2049 完整拆解（12 技法 × 5 角色维度 × 6 场景色调对照）
- **metadata/registry.yaml**：文件级注册表（39 个文件，含状态/依赖/归属/描述）
- **metadata/fields.yaml**：字段级元数据（50 个字段，含类型/默认值/影响角色/影响阶段）
- **metadata/dependencies.yaml**：上下游依赖图（22 对依赖关系，含影响等级）
- **metadata/CHANGELOG.md**：本文件
- **.gitignore**：排除产物/环境/IDE/OS 文件

### 设计决策

1. **美术定调 + 人物设定合并为「视觉开发」**（采纳评估阶段建议#2）
2. **新增「声音指导」角色**（采纳评估阶段建议#3）
3. **Creative Package JSON 标准化**（采纳评估阶段建议#4）
4. **案例库采用 6 表交叉索引 + Agent 自检清单**（解决高效索引和更新问题）
5. **导出格式：HTML（文学剧本 + 分镜展示）+ Excel（分镜技术表）**（采纳评估阶段建议）
6. **元数据维护体系：三层结构（registry + fields + dependencies）**（本次新增）

### 依赖

- 无外部运行时依赖
- 下游关联 Skill：HyperFrames, ComfyUI, image_gen

### 迁移

- 初始版本，无需迁移

---

## 模板：未来版本用的格式

```markdown
## [X.Y.Z] — YYYY-MM-DD

### 新增
- 

### 修改
- 

### 删除
- 

### 影响分析
- 受影响的文件：...
- 受影响的字段：...
- 需要迁移的内容：...

### 迁移指南
1. ...
2. ...
```
