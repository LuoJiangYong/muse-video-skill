# 标准管线 — Default Pipeline（7 阶段）

> **定位**：这是完整创作流程的调度表。它定义 WHEN 激活哪个角色、产出什么、谁来审核——不定义 HOW（HOW 在 references/roles/ 中）。
> **适用**：多场景项目 / 有角色设定 / 需要深度策划 / 用户未明确要求加速。
> **宪法约束**：每阶段 ≤2 轮修改 loop，Director 是唯一审核人，所有角色产出写入 Project State JSON。

---

## 阶段总览

```
Phase 1: 需求沟通          → Director 访谈用户，确定基础参数
Phase 2: 内容梳理          → Writer 生成叙事结构，Director 审核
Phase 3: 视觉开发          → Art Director 定色调/风格/场景搭建，Director 审核
Phase 3.5: 风格定样          → image_gen 生成场景 moodboard + 角色概念图，用户看图确认（条件性子阶段）
Phase 4: 脚本              → Writer→DP→Director 链式产出，含镜头语言
Phase 5: 声音方向          → Sound Designer 定配乐/音效/旁白基调
Phase 6: 分镜              → Storyboard 组装 + 生图 → Director 审核
Phase 7: 组装+调优         → prompt_assembler.py 产出 Creative Pack → HTML storyboard 确认门禁
Phase 7.5: 模型编译        → Model Compiler 编译为模型调用指令（仅 Seedance 2.0）
Phase 8: 下游工具引导      → 【预留】工具选择与费用预估（不执行）
```

---

## Phase 1: 需求沟通

| 维度 | 内容 |
|------|------|
| **激活角色** | Director（唯一） |
| **触发条件** | 用户请求视频策划，路由到本管线 |
| **输入** | 用户原始请求（自然语言） |
| **产出** | Project State JSON：project.*（aspect_ratio, duration_est, genre, tone, platform）, director_notes.vision, director_notes.constraints, director_notes.has_characters（bool/null，从 vision 模板「角色需求」字段提取） |
| **Director 审核** | 本阶段自动通过（Director 自身执行，无需自审） |
| **Loop 规则** | 无限制——此阶段是需求澄清，直到用户确认方向为止 |

### 操作序列

1. Director 加载 `references/roles/director.md` → vision 模板
2. Director 访谈用户，逐项确认：画幅比例 / 预估时长 / 类型 / 情绪基调 / 目标平台

2.5 **【参考视频拆解】** 如用户提供参考视频（消息中含本地文件路径 `*.mp4/*.mov` 或 YouTube/Bilibili 等可下载 URL）→ 触发以下子流程。文字描述不走此分支，走步骤 3 案例匹配。

   **a. 获取 + 预处理**
   - 本地文件：直接读取
   - URL：`yt-dlp` 下载（Android client 防 bot 检测，复用 `references/media/case-study-workflow.md` 已有经验）
   - 预处理：`ffprobe` 检查 codec → av1 必须 `ffmpeg` 转 H.264（CRF 26-28）；检查文件大小 → >30MB 压缩至 720p
   - 下载失败 → 告警用户：「无法下载，能否提供本地文件 / 文字描述风格 / 其他链接？」。如用户三者都给不出 → 跳过拆解，继续步骤 3

   **b. 逐镜头拆解 + 抽帧（内部工作）**
   - 调用 `video_analyze` 两遍：第一遍整体分析，第二遍逐镜头精确提取
   - 生成拉片表——格式见 `_TEMPLATE.md` §拉片附录 镜头序列总览（11列，与案例库同构）
   - `ffmpeg` 逐镜头抽帧 → 分镜图内嵌到拉片表（`![]`(tmp/frame_XX.jpg)）
   - 拉片表为 Agent 工作草稿，不入 Project State

   **c. 拉片表校准**
   - 向用户展示拉片表，请用户验证 AI 理解是否准确
   - 用户指正错误 → 修正后聚合；用户确认 → 进入聚合

   **d. 聚合为技法摘要**
   - 从拉片表中提取跨镜头的规律，归纳为 6 角色技法（条件性）：
     narrative / cinematography / color+scene / character（如有角色） / sound / vfx
   - 结构与静态案例 `techniques` 字段 1:1 对应（仅技法名 + 关键参数，不含拉片层细节）
   - 拉片表（含抽帧）留存为临时文件，后续角色直接从中取帧参考，无需再抽

   **e. 技法摘要确认**
   - 向用户展示技法摘要，确认重点借鉴方向（哪个技法要 / 哪个忽略）
   - 确认后写入 Project State：`reference_analysis.techniques`（技法摘要）
   - 写入 `_meta: { phase: 1, action: "reference_deconstruct" }`

3. 如用户提到具体风格/案例 → 加载 `references/cases/INDEX.md` → 匹配案例 → 注入参考
4. Director 将确认结果写入 `project.*` 和 `director_notes.*`
4b. Agent 从 vision 模板提取结构化字段：director_notes.has_characters（「有角色」→true、「无角色」→false、「不确定」→null）
5. 向用户复述确认后的参数，等待用户说「确认/开始/好」

---

## Phase 2: 内容梳理

| 维度 | 内容 |
|------|------|
| **激活角色** | Writer（产出）→ Director（审核） |
| **触发条件** | Phase 1 用户确认后 |
| **输入** | director_notes.vision, project.genre, project.tone |
| **产出** | script.logline, script.synopsis, script.narrative_structure, script.scenes[]（每个场景的 slug/setting/summary，不含具体对白）, script.character_bible[]（如有角色，定义 identity + voice） |
| **Director 审核** | ✅ 必须审核 |
| **Loop 规则** | ≤2 轮修改。第 2 轮后 Director 必须 approve（可带 conditions）或 reject 重启 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 2`
   - 如 BLOCKED → 输出阻塞原因（通常是 Phase 1 的 project.* 或 director_notes.vision 未填写），回到 Phase 1 补充
   - 如 PASS → 继续
1. Writer 加载 `references/roles/writer.md` → 叙事结构库
2. Writer 读取 `director_notes.vision`，生成 logline + synopsis + narrative_structure
2b. 如有角色需求（`director_notes.has_characters = true`）→ Writer 按 §角色身份定义 模板产出 `script.character_bible[]`（identity + voice）
3. Writer 将产出写入 Project State JSON `script.*` 字段
4. Director 审核（按 director.md 审核标准：通过/修改/拒绝）
   - 如有角色需求（has_characters = true），重点检查 character_bible[] 的 identity 是否具体、voice 是否可翻译
   - **Approve** → 进入 Phase 3
   - **Revise** → Writer 修改后重新提交（≤2 轮）
   - **Reject** → 重写 vision 后重启 Phase 2

---

## Phase 3: 视觉开发

| 维度 | 内容 |
|------|------|
| **激活角色** | Art Director（产出）→ Director（审核） |
| **触发条件** | Phase 2 Director 审核通过 |
| **输入** | director_notes.vision, script.logline, script.scenes[], script.character_bible[]（如有角色）, project.genre, project.tone |
| **产出** | visual_dev.color_palette[], visual_dev.style_direction, visual_dev.mood_references[], visual_dev.scene_composition[]（每个场景的空间布局/核心道具/视觉重心）, visual_dev.character_design[]（如有角色）, visual_dev.world_building（在 scene_composition 之上叠加 sci-fi 规则） |
| **Director 审核** | ✅ 必须审核 |
| **Loop 规则** | ≤2 轮修改 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 3`
   - 如 BLOCKED → 输出阻塞原因，回到 Phase 2 完成 Writer 产出后再试
   - 如 PASS → 继续
1. Art Director 加载 `references/roles/art-director.md` → 色调规则 + 风格库 + 场景搭建模板
2. 如用户提到案例 → 加载对应案例的色彩/美术段
3. Art Director 产出色调方案（含 hex 值）、风格方向、情绪参考
3b. Art Director 为每个场景产 scene_composition：空间布局 / 核心道具 / 视觉重心 / 深度策略（通用，不限场景类型）
4. 可选：调用 `image_gen` 生成 moodboard 参考图（如 ComfyUI 可用）
5. Director 审核：色调是否匹配 vision？风格是否冲突？场景空间是否合理、视觉重心是否清晰？
   - 如有角色需求，额外检查：character_design[] 的视觉翻译是否忠于 character_bible[].identity（例：character_bible 说「内敛克制」，AD 不应给亮色暴露服装）
   - **Approve** → 进入 Phase 4
   - **Revise** → Art Director 调整后重交
   - **Reject** → 重新定调

---

### Phase 3.5: 风格定样（条件性子阶段）

| 维度 | 内容 |
|------|------|
| **激活条件** | image_gen 可用（任一 provider 在线）。不可用则跳过，显式记录 `style_sample.skipped: true, reason: "no image_gen available"` |
| **触发条件** | Phase 3 Director 审核通过 |
| **输入** | visual_dev.color_palette[], visual_dev.style_direction, visual_dev.mood_references[], visual_dev.scene_composition[], visual_dev.character_design[]（如有角色） |
| **产出** | style_sample.scenes[]（2-3 张场景 moodboard），style_sample.characters[]（如有角色，每角色 1-2 张概念图），style_sample.user_decision（approved / revise / skipped） |
| **Director 审核** | 用户确认后 Director 记录决策 |
| **Loop 规则** | ≤2 轮调整。Revise → 标注具体问题（如「场景 3 蓝色过冷」「角色服装与世界观不搭」）→ 回到 Phase 3 仅调整被标注维度，不需全量重做 |

#### 操作序列

1. **场景选择**：从 visual_dev.scene_composition[] 中选取 2-3 个代表性场景
   - 必选：开场场景（定调）
   - 必选：情绪转折/高潮场景（验证 mood→visual_cause 映射）
   - 可选：结尾场景（验证全局一致性）
2. **生成场景 moodboard**：调用 image_gen，每场景 1 张
   - prompt 来源：style_direction 关键词 + color_palette hex 描述 + visual_cause + spatial_layout 概要
   - 图片附带色板叠加信息（hex 值标注）
3. **如有角色 → 生成角色概念图**（仅当 has_characters = true 且 character_design[] 非空）
   - 每角色 2 张：面部肖像（face_features + distinguishing_marks）+ 全身造型（height_build + wardrobe + silhouette）
   - prompt 使用与场景相同的 color_palette + style_direction——验证角色与场景的色彩一致性
4. **呈现给用户**（结构化格式）：
   ```
   [风格定样]

   场景 moodboard：
   - [场景名]：[图片] + 色板 + visual_cause

   角色概念（如有）：
   - [角色名]：[面部肖像] [全身造型] + 设计来源

   请确认：
   - ✅ 色调/风格方向正确 → Phase 4
   - 🔄 需要调整：[具体哪个场景/角色的哪个维度]
   - ⏭ 跳过样本，直接进入 Phase 4（不推荐——Phase 6 返工成本更高）
   ```
5. **门禁**：
   - Approved → `style_sample.user_decision = "approved"` → 进入 Phase 4
   - Revise → 标注具体问题 → 回到 Phase 3 调整被标注维度 → 调整后重新定样（≤2 轮）
   - Skipped（用户 insist）→ 显式警告：`「Phase 6 才发现风格跑偏的话，Phase 4-5 需重做」` → 记录后进入 Phase 4
6. **成本透明**：生成前告知用户预算（2-4 张图 ≈ $0.02-0.10），用户确认后执行

#### 跳过降级规则

| 场景 | 行为 |
|------|------|
| image_gen 全不可用 | 跳过 Phase 3.5，`style_sample.skipped: true, reason: "no image_gen available"`。不阻塞管线 |
| image_gen 可用，用户要求跳过 | Agent 必须推送警告后记录。用户 insist 后跳过 |
| 角色图生成失败（但场景图成功） | 场景图正常定样，角色图标注 `generation_failed`，Phase 4 Writer 基于文字 character_design 继续 |
| Fast-Track 管线 | Phase 3.5 不激活——快速管线默认接受首次 AD 产出 |

---

## Phase 4: 脚本

| 维度 | 内容 |
|------|------|
| **激活角色** | Writer（文本）→ DP（镜头）→ Director（审核），链式顺序 |
| **触发条件** | Phase 3 Director 审核通过 |
| **输入** | Phase 2 产出的 script.* + Phase 3 产出的 visual_dev.* |
| **产出** | script.scenes[].dialogue, script.scenes[].action, cinematography.shot_list[], cinematography.camera_notes[]（每个场景的 shot type/movement/lens/lighting） |
| **Director 审核** | ✅ 必须审核 |
| **Loop 规则** | ≤2 轮修改 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 4`
   - 如 BLOCKED → 输出阻塞原因（通常是 Phase 3 的 visual_dev 色调方案未完成），回到 Phase 3 完成后再试
   - 如 PASS → 继续
1. Writer 基于 Phase 2 的叙事结构，为每个场景补充：对白 / 动作描述 / 时长估算
2. DP 加载 `references/roles/dp.md` → 镜头语言 + 灯光模板
3. DP 为每个场景的每个镜头补充：shot type / movement / lens / lighting setup
4. **注意**：Writer 和 DP 串行执行（DP 依赖 Writer 的场景结构，但 DP 不改对白）
5. Director 审核：脚本节奏是否合理？镜头语言是否匹配情绪？
   - 如有角色需求，额外检查：对白风格是否与 character_bible[].voice 一致？（不能所有角色同一种语气）
   - **Approve** → 进入 Phase 5
   - **Revise** → 标注问题，Writer/DP 分别修改
   - **Reject** → 回到 Phase 2 重写 vision（罕见）

---

## Phase 5: 声音方向

| 维度 | 内容 |
|------|------|
| **激活角色** | Sound Designer（产出）→ Director（审核） |
| **触发条件** | Phase 4 Director 审核通过 |
| **输入** | 完整 script.* + project.tone + visual_dev.* |
| **产出** | sound.music_style, sound.sfx_map[]（场景→音效映射）, sound.narration_tone, sound.silence_strategy, sound.reference_tracks[] |
| **Director 审核** | ✅ 必须审核 |
| **Loop 规则** | ≤2 轮修改 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 5`
   - 如 BLOCKED → 输出阻塞原因（通常是 Phase 4 的 script.scenes 或 cinematography 未完成），回到 Phase 4 完成后再试
   - 如 PASS → 继续
1. Sound Designer 加载 `references/roles/sound-designer.md`
2. 读取每个场景的情绪基调 → 匹配配乐风格 → 映射音效类型
3. 产出声音方向（不是最终音轨，是方向性指导）
4. Director 审核：声音方向是否增强而非分散注意力？
   - 如有角色需求，额外检查：配乐动机是否从 character_bible[].voice 推导（非 visual_profile 逆推）？每个角色是否有独立声音签名？
   - **Approve** → 进入 Phase 6
   - **Revise** → Sound Designer 调整
   - **Reject** → 重新定调

---

## Phase 6: 分镜

| 维度 | 内容 |
|------|------|
| **激活角色** | Storyboard 组装（集成角色）→ VFX（特效标注）→ Director（审核） |
| **触发条件** | Phase 5 Director 审核通过 |
| **输入** | 全部前置产出：script.* + cinematography.* + visual_dev.* + vfx.* |
| **产出** | storyboard.panels[]（每个 panel：编号 / 关联 scene / shot 描述 / camera / lighting / vfx / image_prompt / 参考图 URL） |
| **Director 审核** | ✅ 必须审核 |
| **Loop 规则** | ≤2 轮修改 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 6`
   - 如 BLOCKED → 输出阻塞原因（通常是 Phase 5 的 sound.music_style 未填写），回到 Phase 5 完成后再试
   - 如 PASS → 继续
1. 为每个脚本场景生成 1-3 个关键分镜 panel
2. 每个 panel 从 Project State JSON 中提取对应信息：
   - script（对白/动作）→ panel.description
   - cinematography（镜头/灯光）→ panel.camera, panel.lighting
   - visual_dev（色调/风格/场景搭建）→ panel.art_direction
   - vfx（特效标注）→ panel.vfx_notes
3. VFX 加载 `references/roles/vfx.md` → 为需要特效的 panel 补充材质/粒子/转场说明
4. 为每个 panel 生成 `image_prompt`（可注入 image_gen 的完整 prompt）
5. **【显式确认：分镜图生成】** 向用户展示已组装的分镜面板摘要（panel 数量 / 关键画面描述 / 镜头参数）。
   询问用户：「是否调用 image_gen 为关键分镜面板生成参考图？（生成后 Phase 7 的 HTML storyboard 将包含实际画面预览）」
   - 选择「**生成**」→ 为 storyboard 中标记为 `layout: "wide"` 或 `"establishing"` 的 panel 生成配图
   - 选择「**跳过**」→ 继续。Phase 7 HTML storyboard 将使用文字占位符
   - 提示：如跳过，Phase 7 确认时仍可返回本步骤定向重生成（不丢失已确认的剧本和分镜结构）
6. Director 审核：分镜是否讲清楚了故事？画面构图是否一致？
   - **Approve** → 进入 Phase 7
   - **Revise** → 调整 panel 描述/prompt
   - **Reject** → 回到 Phase 4 重写关键场景

---

## Phase 7: 组装+调优

| 维度 | 内容 |
|------|------|
| **激活角色** | Director（调优） |
| **触发条件** | Phase 6 Director 审核通过 |
| **输入** | 完整 Project State JSON（所有 phase 的产出） |
| **产出** | 完整 Creative Package（JSON + 分镜图集），含 tuning_notes.* |
| **Director 审核** | 本阶段是终审，Director 自身执行 |

### 操作序列

0. **【门禁检查】** 运行 `python scripts/validate_state.py --phase 7`
   - 如 BLOCKED → 输出阻塞原因（分镜未完成/未审批/缺失），回到 Phase 6 修复后再试
   - 如 PASS → 继续
1. 检查 Project State JSON 完整性：所有 `_meta.director_approved` = true
2. 加载 `references/meta/verification-checklist.md` 逐项检查
3. 运行 `scripts/prompt_assembler.py` → 产出 Creative Pack JSON
3. Director 添加 `tuning_notes.*`：调色建议 / 节奏调整 / 特效微调 / 最终确认
4. 按需运行 `scripts/export_html.py` / `scripts/export_xlsx.py` 生成导出文件

5. **【HTML Storyboard 确认门禁 — 唯一最终确认关卡】**
   运行 `scripts/export_html.py --mode storyboard` 生成完整分镜预览 HTML。
   向用户展示 HTML storyboard 路径 + 关键参数摘要（总镜数 / 总时长 / 分辨率建议）。
   显式提示：「请查看 HTML storyboard，确认**分镜内容**（镜头顺序 / 构图描述 / 景别 / 运镜 / 时长 / 节奏）。HTML 排版为自动生成，仅用于快速预览，不代表最终视觉质量。**您确认的每一张参考图将直接进入 Phase 7.5 模型编译，最终喂给 AI 视频模型。**」

6. **【用户操作 — 四选项 + 默认】**

   ┌─────────────────────────────────────────────────────────────────┐
   │ **选项 A：「确认，进入编译」**                                      │
   │   → 批准 storyboard._meta.director_approved = true               │
   │   → 锁定分镜（确认后只读，修改需走选项 D 完整回退）                   │
   │   → 进入 Phase 7.5 模型编译                                       │
   │                                                                 │
   │ **选项 B：「修改分镜文本/顺序」（第一层 — 就地修改）**                │
   │   → 用户指定要修改的 panel_id + 修改内容                           │
   │   → Director 直接编辑 storyboard[].prompt / scenes[].duration     │
   │   → ⚠️ 可修改：prompt 文本 / 时长 / panel 顺序 / tuning_notes      │
   │   → ❌ 不可修改：camera.movement / palette / 场景叙事结构（需选项 D） │
   │   → 修改完成 → 重新导出 HTML → 回到步骤 5 确认门禁                  │
   │                                                                 │
   │ **选项 C：「重新生成某个画面」（第二层 — 定向重生成）**                │
   │   → 用户指定 panel_id（可多选，如 S03, S05）                       │
   │   → 回到 Phase 6 步骤 5，仅对指定 panel 重新调用 image_gen           │
   │   → 新图片 URL 写入 storyboard[panel].generated_url                │
   │   → ⚠️ 相邻 panel 可能风格不一致 → 提示但不禁用                      │
   │   → 重生成完成 → 重新导出 HTML → 回到步骤 5 确认门禁                │
   │                                                                 │
   │ **选项 D：「调整运镜/色调/结构」（第三层 — 完整回退）**                │
   │   → 用户描述不满意的维度                                           │
   │   → Director 判断回退目标 Phase（3/4/5/6）                         │
   │   → 执行「保留式回退」：仅修改受影响 scene/panel，不推翻全部          │
   │   → 回退到 Phase 3（色调）→ AD 重定 palette → 级联到 Phase 6/7      │
   │   → 回退到 Phase 4（运镜/剧本）→ Writer/DP 重写 → 级联到 Phase 6/7  │
   │   → 级联更新完成 → 回到 Phase 7 步骤 5 确认门禁                     │
   │                                                                 │
   │ **默认（30s 无操作）** → 等同于选项 A，自动进入 Phase 7.5            │
   │   → 编译为确定性转换，不产生费用，可在 Phase 7.5 质量标记中发现问题   │
   └─────────────────────────────────────────────────────────────────┘

7. 确认通过 → Director 批准 storyboard._meta.director_approved = true
   → 进入 Phase 7.5（模型编译）

---

## Phase 7.5: 模型编译

| 维度 | 内容 |
|------|------|
| **激活角色** | Model Compiler |
| **触发条件** | Phase 7 Creative Package 完成 + Director 确认 |
| **输入** | Project State（script + cinematography + visual_dev + sound + storyboard） |
| **产出** | model_compilation JSON（编译后的模型调用指令） |
| **Director 审核** | 可选 — 编译器产出为确定性转换。用户可选择「信任编译器」跳过审查，或逐镜检查 prompt_trace |
| **Loop 规则** | 不适用 — 编译为确定性转换，无创意判断。如用户对编译结果不满意 → 调整上游 Phase 3/4/5/6 产出后重新编译 |

### 操作序列

1. Model Compiler 加载 `references/model-compiler.md`
2. 读取 Project State 中所有相关字段（见 model-compiler.md §输入）
3. 检测 `target_model` → 跳转对应适配章节（当前仅 Seedance 2.0）
4. 按编译规则逐镜生成 `model_compilation.shots[]`：
   a. 六段式 prompt 编译（含 Narrative Anchor 保留规则）
   b. 镜头运动术语翻译（双层查表：默认映射 + 场景覆盖 + movement_language 消歧）
   c. 5 槽分配（三套策略自动选择：character_driven / product_driven / graphic_driven）
   d. arkcli 命令生成（Windows 安全路径：Files API file_id + --extra-body，不用 --input @本地文件）
   e. 质量标记（GOOD / DEGRADED / INSUFFICIENT）+ 成本估算
5. 构建 video_ref 镜头链（`model_compilation.shot_chain`）
6. 运行干跑验证清单（见 model-compiler.md §干跑验证清单）
7. 输出编译摘要给用户（shot 数 / 预估成本 / 质量警告）
8. 用户可选择：
   - **信任输出** → 批准 `model_compilation._meta.director_approved = true`
   - **逐镜检查** → 审查 `prompt_trace` → 批准
   - **不满意** → 返回上游 Phase 调整后重新编译
9. 如任何 shot 的 `_quality.overall = INSUFFICIENT` → **暂停**，要求用户确认后继续

---

## Phase 8: 下游工具引导（预留 — 未建设）

> **状态**：⚠️ 预留阶段，不建设。当前管线在 Phase 7.5 后结束，用户自行选择下游工具执行。
> **设计原则**：Phase 8 是「机场指示牌」——告诉你哪个登机口，不替你登机。

| 维度 | 内容 |
|------|------|
| **激活角色** | Tool Guide（待建） |
| **触发条件** | Phase 7.5 编译完成 + Director 确认（待定） |
| **输入** | `model_compilation` JSON |
| **产出** | 工具选项菜单（费用预估 / 时间预估 / 适用场景 / 推荐方案） |
| **边界** | **仅引导选择，不执行工具**。执行权交给 `volcengine-ark` / `hyperframes` / `comfyui` 等 skill |

### 建设时必须遵守的约束

1. **不执行工具**。Phase 8 不调用 arkcli、不触发 HyperFrames 合成、不启动 ComfyUI
2. **不重复 skill 功能**。`volcengine-ark` skill 已有完整的 arkcli 执行流程，Phase 8 只做「选择 + 引导」
3. **费用预估必须保守**。用 `model_compilation` 中的 `estimated_cost_cny` 作为参考
4. **预留多工具路由**。未来支持：Seedance → HyperFrames 合成、直接 arkcli 执行、ComfyUI 本地生成

---

## Loop 规则速查

| 规则 | 说明 |
|------|------|
| **每阶段最多 2 轮修改** | Phase 2-6 统一适用。第 1 轮 Revise→修改重交；第 2 轮 Revise→Director 必须 approve（可带 conditions）或 reject 重启 |
| **NITPICK 不消耗 loop** | 仅有 [NITPICK] 无 [CRITICAL]/[SUGGESTION] 的轮次不计入 2 轮配额——Director 应直接 APPROVE 附带 NITPICK |
| **Reject 的后果** | 该阶段产出丢弃，回到该阶段的「触发条件」重新执行。一般不允许跨阶段回退 |
| **Phase 7 跨阶段回退（例外）** | 用户在 Phase 7 确认门禁选择「选项 D：完整回退」时，Director 可回退到 Phase 3/4/5/6。执行「保留式回退」——仅修改受影响 scene/panel，不推翻全部。此为用户主动触发的例外，优先级高于通用 Reject 规则 |
| **Director 自身不审核** | Phase 1 和 Phase 7 是 Director 自行执行的阶段，无需自审。但 Phase 7 的 HTML storyboard 确认门禁是用户确认关卡（非 Director 自审） |
| **Approve with conditions** | Director 可以 approve 但附加条件（如「色调 approve，但场景 3 的蓝色饱和度降低 10%」），条件在后续阶段执行 |

---

## 角色激活矩阵

| 角色 | Phase 1 | Phase 2 | Phase 3 | Phase 3.5 | Phase 4 | Phase 5 | Phase 6 | Phase 7 | Phase 7.5 | Phase 8 |
|------|:-------:|:-------:|:-------:|:---------:|:-------:|:-------:|:-------:|:-------:|:---------:|:-------:|
| Director | 🟢 执行 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟢 执行 | 🟡 审核 | — |
| Writer | — | 🟢 产出 | — | — | 🟢 产出 | — | — | — | — | — |
| Art Director | — | — | 🟢 产出 | — | — | — | — | — | — | — |
| DP | — | — | — | — | 🟢 产出 | — | — | — | — | — |
| Sound Designer | — | — | — | — | — | 🟢 产出 | — | — | — | — |
| VFX | — | — | — | — | — | — | 🟢 产出 | — | — | — |
| Model Compiler | — | — | — | — | — | — | — | — | 🟢 执行 | — |
| Tool Guide | — | — | — | — | — | — | — | — | — | 🔵 预留 |

🟢 = 执行/产出 &nbsp;&nbsp; 🟡 = 审核 &nbsp;&nbsp; — = 不激活

---

## 跨阶段依赖

- Phase 3 可读取 Phase 2 的 `script.scenes[]`（场景列表），但不读取 Phase 4 的对白
- Phase 4 串行：Writer 先产出 → DP 再叠加镜头（防止 DP 影响对白）
- Phase 5 可读取 Phase 4 的完整产出（声音需知道每个场景的情绪）
- Phase 6 读取全部前置产出（集成点）
- VFX 在 Phase 6 被激活，其标注叠加到分镜 panel 上
- Phase 7.5 读取 Phase 3/4/5/6 的全部产出，不修改任何上游字段
- Phase 7 确认门禁支持返回 Phase 6 步骤 5（定向重生成，选项 C）或回退 Phase 3/4（完整回退，选项 D）。回退时执行「保留式」——未受影响部分不丢弃
- Phase 8 预留读取 `model_compilation` JSON → 引导用户选择下游工具（不执行）
