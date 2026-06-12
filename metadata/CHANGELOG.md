# Changelog — 版本变更日志

> 记录每次修改的动机、内容、影响范围、迁移指南。
> 每次 git commit 涉及实质改动时同步更新此文件。
> 格式：`## [version] — YYYY-MM-DD`

---

## [0.7.0] — 2026-06-12

### 新增 — Phase 7: 国际标杆广告案例扩充（4 个案例文件，优先级 1）

**Old Spice — `references/cases/OLDSPICE-MAN.md` (230+ 行)**
- Tom Kuntz 执导，33 秒单镜头喜剧广告的病毒革命
- 14+ 技法 × 5 角色维度：无缝口头转场 / 打破第四面墙 / 荒诞逻辑链 / 喜剧节奏公式(1笑点/3s) / 连续单镜头错觉 / 身体即产品载体 / 男中音旁白节奏 / 荒诞夸大策略 / 病毒一句话公式
- 5 场景色调对照表(纯白浴室→金色海滩) + 帧匹配转场缝合技术 + 幽默推销3步模型
- 填补盲区：🎯 喜剧/幽默广告（全库首个）

**John Lewis — `references/cases/JOHNLEWIS-PENGUIN.md` (250+ 行)**
- Dougal Wilson 执导，2 分钟圣诞情感叙事的标杆
- 15+ 技法 × 5 角色维度：情感蓄力结构(90%积累→5%释放) / 儿童视角 / 反转结局3步释放 / 非人类情感代言 / CGI企鹅动画+实拍融合 / 翻唱编排策略 / 无对白音乐叙事 / 静默品牌登场
- 5 场景色调对照表(深木色暖家→金色晨光释放) + 灯光匹配HDRI技术 + 品牌隐形策略
- 填补盲区：🎯 长叙事情感广告（全库首个）

**Sony Bravia — `references/cases/SONY-BALLS.md` (230+ 行)**
- Nicolai Fuglsig 执导，25 万颗弹力球零 CGI 实拍的视觉革命
- 14+ 技法 × 5 角色维度：无叙事纯视觉 / 产品隐喻4步递进 / Show-Don't-Tell极致 / 超高速摄影1000fps / 广角全景23机位 / 色彩光谱编排 / 零CGI实拍调度 / 音乐反差策略(Heartbeats) / 纯隐喻型广告
- 6 场景色调对照表(灰色街景→光谱色带) + 歌曲去电子化改编公式
- 填补盲区：🎯 视觉奇观型广告（全库首个）

**Volvo Trucks — `references/cases/VOLVO-SPLIT.md` (240+ 行)**
- Andreas Nilsson 执导，Van Damme 在两台倒行卡车间劈叉
- 15+ 技法 × 5 角色维度：极简信息设计(3信息点) / 产品演示即叙事 / 一镜到底航拍 / 对称史诗构图 / 黎明金色时刻 / Enya音乐反差 / 极限信任证明 / 病毒一句话公式
- 4 场景色调对照表(三色极简：金色/灰色/银色) + 信息层频谱分离音频 + 产品演示即表演模型
- 填补盲区：产品演示型广告的「表演化」升级

### 变更 — INDEX.md + registry 全表同步

- 主注册表：+4 行（12 案例总计）
- 叙事技法表：+15 条目 → 共 38 条目
- 镜头语言表：+14 条目 → 共 39 条目
- 色彩/美术表：+13 条目 → 共 27 条目
- 特效语言表：+12 条目 → 共 29 条目
- 声音设计表：+13 条目 → 共 28 条目
- 创意广告表：+14 条目 → 共 20 条目
- 场景→案例表：studio-ad/product-demo 增强（+4 案例）
- 风格/情绪表：+humorous + absurd + heartwarming → 共 15 标签
- 角色维度表：6 角色全部更新，每个角色必看案例增至 7-9 个

### 盲区覆盖率

| 盲区类型 | Phase 6 | Phase 7 | 状态 |
|---------|---------|---------|------|
| 喜剧/幽默广告 | 0 | 1 (OLDSPICE-MAN) | ✅ 已覆盖 |
| 长叙事情感广告(60-120s) | 0 | 1 (JOHNLEWIS-PENGUIN) | ✅ 已覆盖 |
| 视觉奇观型广告(纯CG/特殊摄影) | 0 | 1 (SONY-BALLS) | ✅ 已覆盖 |
| 品牌宣言型 | 1 (部分) | 1 (NIKE-YCS) | ⚠️ 部分覆盖 |
| 病毒/社交传播型(≤30s) | 0 | 1 (OLDSPICE-MAN) | ✅ 已覆盖 |

### 统计

| 指标 | Phase 6 | Phase 7 | 增量 |
|------|---------|---------|------|
| 总案例数 | 8 | 12 | +4 |
| 广告案例 | 3 | 7 | +4 |
| 总文件数 | 46 | 50 | +4 |
| 覆盖角色维度 | 5/5 | 5/5 | — |
| 索引表数量 | 10 | 10 | — |

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`, `references/cases/INDEX.md`
- 新增文件：4 个（OLDSPICE-MAN.md / JOHNLEWIS-PENGUIN.md / SONY-BALLS.md / VOLVO-SPLIT.md）
- 下游影响：SKILL.md 路由表无需修改（INDEX.md 交叉引用自动生效）

### 迁移指南

- 无需迁移。所有 Phase 0-6 文件保持不变，Phase 7 为纯增量。
- 4 个案例文件均按 `_TEMPLATE.md` 格式，≥200 行 / ≥12 技法 / 5 角色维度全覆盖。

---

## [0.6.0] — 2026-06-12

### 新增 — Phase 6: 硬核电影案例扩充（3 个案例文件）

**花样年华 — `references/cases/WKW-ML.md` (240+ 行)**
- 王家卫美学终极标本，15+ 技法 × 5 角色维度
- 核心技法：留白叙事 / 重复结构 / 框架构图(偷窥视角) / 慢快门步印 / 旗袍色彩叙事 / 音乐锚点
- 7 场景色调对照表 + 23 套旗袍→情绪映射系统 + 墙纸视觉密度分析
- 填补盲区：艺术电影类型首次纳入案例库

**流浪地球 — `references/cases/WANDERING-E.md` (250+ 行)**
- 中国硬核科幻工程美学标杆，16+ 技法 × 5 角色维度
- 核心技法：集体英雄主义 / 巨物尺度公式(人 1.8m→地球 12,742km) / 五域色调体系 / 行星发动机火焰 VFX / 低频嗡鸣次声波
- 6 场景色调对照表 + 地下城烟火气设计哲学 + Boids 运载车集群
- 填补盲区：中国科幻美学首次纳入案例库（区别于西方赛博朋克）

**环太平洋 — `references/cases/PACIFIC-RIM.md` (260+ 行)**
- Guillermo del Toro 巨型机甲标杆，16+ 技法 × 5 角色维度
- 核心技法：双人共驾 Drift 系统 / 重量感运动公式(2-3s 惯性缓冲) / 霓虹雨夜色调 / 机械物理模拟 / 关节专属声音设计
- 5 场景色调对照表 + 「熟悉+陌生」怪兽设计原则 + 雨水粒子系统三层架构
- 填补盲区：巨型机甲/物理重量感类型首次纳入案例库

### 变更 — INDEX.md 全表同步

- 主注册表：+3 行 (8 案例 总计)
- 叙事技法表：+12 条目 → 共 23 条目
- 镜头语言表：+12 条目 → 共 25 条目
- 色彩/美术表：+8 条目 → 共 14 条目
- 特效语言表：+10 条目 → 共 17 条目
- 声音设计表：+9 条目 → 共 15 条目
- 场景→案例表：+custom (art-film) + sci-fi/logo-animation 增强
- 风格/情绪表：+nostalgic + melancholic + cyberpunk-adjacent → 共 12 标签
- 角色维度表：5 角色全部更新，每个角色必看案例增至 4-5 个

### 统计

| 指标 | Phase 5 | Phase 6 | 增量 |
|------|---------|---------|------|
| 总案例数 | 5 | 8 | +3 |
| 电影案例 | 1 | 4 | +3 |
| 总文件数 | 43 | 46 | +3 |
| 覆盖角色维度 | 5/5 | 5/5 | — |
| 索引表数量 | 8 | 10 | +2 |

---

## [0.5.0] — 2026-06-12

### 新增 — Phase 5: 案例库扩充（4 个案例文件）

**Apple Welcome Home — `references/cases/APPLE-WH.md` (219 行)**
- Spike Jonze 为 Apple HomePod 执导的标杆级广告片
- 14 项技法 × 5 角色维度：无对白叙事 / 身体驱动转场 / 单镜头错觉缝合 / 空间扭曲跟拍 / 360° 环绕运动 / 物理空间拉伸 VFX / 镜像无限反射 / 色彩渗入转场 / 音乐驱动节奏 / 环境音景空间定位 / 产品隐形植入 / 艺术家背书 / 感官替代功能
- 6 场景色调对照表（灰→黄→蓝→粉→彩→灰）

**Nike You Can't Stop Us — `references/cases/NIKE-YCS.md` (217 行)**
- Oscar Hudson 执导，24 名运动员 × 36 种运动 × 53 组分屏匹配
- 14 项技法 × 5 角色维度：隐喻剪辑 / 无旁白累积 / 集体叙事 / 分屏匹配几何精度 / 档案素材统一化 / 动态节奏数学设计 / 分屏匹配隐藏艺术 / 动态节奏变速 / 声画对位 / 静默爆发 / 品牌精神替代产品展示 / 集体共鸣 / 蓄力结构
- 5 场景色调对照表 + 详细时间轴节奏参数

**Apple Don't Blink — `references/cases/APPLE-DB.md` (226 行)**
- Apple 2019 年终产品回顾，107 秒展示 80+ 功能点
- 13 项技法 × 5 角色维度：功能叙事 / 极简旁白子弹规则 / 密度递增 S 曲线 / 高速剪辑第一帧即最终帧 / 产品密度空间 / 微距功能视觉化 / UI 标注叠加 / 产品极速转场 / 节奏递增音频 / 产品声音符号化 / 产品密度=竞争力 / 节奏递增心理操控 / 证明-不解释
- 5 场景色调对照表 + 功能→画面映射公式

**Cosmos Laundromat — `references/cases/COSMOS-L.md` (225 行)**
- Blender Foundation 开源短片，暖色科幻的自然光革命
- 14 项技法 × 5 角色维度：环境叙事 / 非人类主角情感 / 无对白情感渐进 / 自然光模拟 CG 革命 / 巨物尺度对比 / 微距材质凝视 / 虚拟摄影机物理感 / 材质渲染物理真实性 / 光传输模拟 / 体积光效情绪 / 异世界音景 / 音乐情感引导 / 材质声音地图
- 7 场景色调对照表（从「绿色牢笼」到「蓝色自由」）

### 修改

- `SKILL.md`：版本号 0.4.0 → 0.5.0
- `metadata/registry.yaml`：4 个案例文件 status=complete，Phase 5 统计；总文件数 39→43
- `references/cases/INDEX.md`：最后更新日期标注 Phase 5 完成状态

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`, `references/cases/INDEX.md`
- 新增文件：4 个（APPLE-WH.md / NIKE-YCS.md / APPLE-DB.md / COSMOS-L.md）
- 下游影响：SKILL.md 路由表无需修改（INDEX.md 交叉引用已在 Phase 1 完成）；场景文档中的案例引用表已预填这些案例 ID

### 迁移指南

- 无需迁移。所有 Phase 0-4 文件保持不变，Phase 5 为纯增量。
- 4 个案例文件均按 `_TEMPLATE.md` 格式，与 BR2049.md 同深度标准，可直接被 Agent 引用。

---

## [0.4.0] — 2026-06-12

### 新增 — Phase 4: 示例项目（2 个示例，16+ 文件）

**完整棚拍广告案例 —「光影之间」**
- `assets/examples/studio-ad-full/README.md`：创意 brief + 管线执行记录 + 产出清单 + 脚本再生指南
- `assets/examples/studio-ad-full/project-state.json`：完整 Project State JSON（5 场景 + 7 分镜，27KB，所有 `_meta.director_approved=true`）
- 脚本产出：`script.md` / `storyboard.md` / `creative-pack.json` + `.md` / `studio-ad-literary.html` + `-storyboard.html` / `tech-breakdown.xlsx`
- 创意特征：减法灯光哲学（BR2049 单一光源）+ 材质叙事（8微距剪辑）+ 沉默对白（仅4字旁白）+ 光传递转场 + 金色粒子首尾呼应

**完整科幻短片案例 —「最后的记忆贩」**
- `assets/examples/sci-fi-short/README.md`：创意 brief + 管线执行记录 + BR2049 技法映射表 + 产出清单
- `assets/examples/sci-fi-short/project-state.json`：完整 Project State JSON（8 场景 + 8 分镜 + 1 角色，53KB，所有 `_meta.director_approved=true`）
- 脚本产出：`script.md` / `storyboard.md` / `creative-pack.json` + `.md` / `sci-fi-literary.html` + `-storyboard.html` / `tech-breakdown.xlsx`
- 创意特征：BR2049 全景式致敬——12 项技法直接继承（沉默对白/信息释放节奏/巨物尺度对比/单一光源/环形构图/dolly克制/场景色调对照/粒子氛围/全息不完美/巨物缓动/工业环境音/爆发式巨响）
- 角色设计：Kael（记忆贩）— 面部仅在 2 个镜头中完全展示（叙事手段）

### 修改

- `SKILL.md`：版本号 0.3.0 → 0.4.0
- `metadata/registry.yaml`：2 个示例文件 status not_started→complete，BR2049 依赖补充；Phase 4 统计更新

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 新增文件：10 个（2 个 README + 2 个 project-state.json + 6 个补充产出文件）
- 下游影响：无（所有新文件均为新建，不修改已有 Phase 0-3 文件）

### 迁移指南

- 无需迁移。Phase 0-3 的所有文件保持不变。
- 两个示例项目均可独立运行：进入对应目录，按 README.md 中的「脚本再生」命令重新生成所有产出。

---

## [0.3.0] — 2026-06-12

### 新增 — Phase 3: 脚本+模板+导出（12 个文件）

**Markdown 模板（3 个）**
- `assets/templates/script.md`：剧本 Markdown 模板，含场景分解、技术备注、元信息节
- `assets/templates/storyboard.md`：分镜 Markdown 模板，支持 2×3/3×3 网格，含 AI 提示词+审核状态
- `assets/templates/creative-pack.md`：创作包 Markdown 模板，完整 10 节结构（项目概要→下游工具对接）

**核心脚本（3 个）**
- `scripts/format_script.py`：scene array → 好莱坞剧本格式。schema-driven，支持 {{#each}} 遍历和 {{#if}} 条件块，CLI 支持 --input/--output/--template
- `scripts/storyboard_grid.py`：storyboard array → 2×3/3×3 网格 Markdown。自动选择网格布局（≤6→2×3，≤9→3×3），支持 --grid 强制覆盖
- `scripts/prompt_assembler.py`：完整 Project State → Creative Pack JSON + Markdown。自动生成 ComfyUI/HyperFrames/Kling/Runway 下游工具配置

**导出脚本（3 个）**
- `scripts/export_html.py`：Project State → 文学剧本 HTML（Courier 标准格式）+ 分镜展示 HTML（卡片网格，支持 dark mode）
- `scripts/export_xlsx.py`：Project State → 分镜技术表 Excel（多 Sheet：分镜表/项目概要/色调方案/特效清单/声音方案），依赖 openpyxl
- `scripts/moodboard_compare.py`：2+ 视觉方向 → 对比矩阵（色调对比/风格参考/相似度分析/推荐方向）

**导出模板（3 个）**
- `assets/templates/export/script-literary.html`：文学剧本 HTML 模板，Courier Prime 字体，标准剧本页边距，支持打印优化
- `assets/templates/export/script-storyboard.html`：分镜展示 HTML 模板，响应式卡片网格，含图片占位、审核状态徽章
- `assets/templates/export/script-tech.xlsx`：Excel 模板定义（JSON 驱动），5 个 Sheet 的列/行定义、条件格式、全局样式

### 修改

- `SKILL.md`：版本号 0.2.0 → 0.3.0
- `metadata/registry.yaml`：12 个文件 status not_started→complete；Phase 3 统计更新

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 新增依赖：format_script.py/storyboard_grid.py → templates/script.md/storyboard.md；prompt_assembler.py → templates/creative-pack.md
- 下游影响：无（所有新文件均为新建，不修改已有文件）

### 迁移指南

- 无需迁移。Phase 0-2 的所有文件保持不变。
- export_xlsx.py 需要 `pip install openpyxl`（仅在使用 Excel 导出时需要）

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
