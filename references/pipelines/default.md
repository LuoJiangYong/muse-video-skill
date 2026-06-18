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
Phase 4: 脚本              → Writer→DP→Director 链式产出，含镜头语言
Phase 5: 声音方向          → Sound Designer 定配乐/音效/旁白基调
Phase 6: 分镜              → Storyboard 组装 + 生图 → Director 审核
Phase 7: 组装+调优         → prompt_assembler.py 产出 Creative Pack
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
   - URL：`yt-dlp` 下载（Android client 防 bot 检测，复用 `case-study-workflow.md` 已有经验）
   - 预处理：`ffprobe` 检查 codec → av1 必须 `ffmpeg` 转 H.264（CRF 26-28）；检查文件大小 → >30MB 压缩至 720p
   - 下载失败 → 告警用户：「无法下载，能否提供本地文件 / 文字描述风格 / 其他链接？」。如用户三者都给不出 → 跳过拆解，继续步骤 3

   **b. 逐镜头拆解（内部工作）**
   - 调用 `video_analyze` 两遍：第一遍整体分析，第二遍逐镜头精确提取
   - 每镜头记录：时间码 / 景别 / 构图 / 运镜 / 调色 / 音效 / 叙事功能
   - 生成拉片表（Agent 工作草稿，不入 Project State）

   **c. 拉片表校准**
   - 向用户展示拉片表，请用户验证 AI 理解是否准确
   - 用户指正错误 → 修正后聚合；用户确认 → 进入聚合

   **d. 聚合为技法摘要**
   - 从拉片表中提取跨镜头的规律，归纳为 5 角色技法：
     narrative / cinematography / color / sound / vfx
   - 结构与静态案例 `techniques` 字段 1:1 对应（仅技法名 + 关键参数，不含拉片层细节）

   **e. 技法摘要确认**
   - 向用户展示技法摘要，确认重点借鉴方向（哪个技法要 / 哪个忽略）
   - 确认后写入 Project State（`reference_analysis` 字段，结构同静态案例数据）
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
   - **Approve** → 进入 Phase 4
   - **Revise** → Art Director 调整后重交
   - **Reject** → 重新定调

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
5. 可选：调用 `image_gen` 为关键 panel 生成参考图
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
2. 运行 `scripts/prompt_assembler.py` → 产出 Creative Pack JSON
3. Director 添加 `tuning_notes.*`：调色建议 / 节奏调整 / 特效微调 / 最终确认
4. 按需运行 `scripts/export_html.py` / `scripts/export_xlsx.py` 生成导出文件
5. 向用户交付，提示下游工具对接（HyperFrames / ComfyUI / Kling 等）

---

## Loop 规则速查

| 规则 | 说明 |
|------|------|
| **每阶段最多 2 轮修改** | Phase 2-6 统一适用。第 1 轮 Revise→修改重交；第 2 轮 Revise→Director 必须 approve（可带 conditions）或 reject 重启 |
| **Reject 的后果** | 该阶段产出丢弃，回到该阶段的「触发条件」重新执行。不跨阶段回退 |
| **Director 自身不审核** | Phase 1 和 Phase 7 是 Director 自行执行的阶段，无需自审 |
| **Approve with conditions** | Director 可以 approve 但附加条件（如「色调 approve，但场景 3 的蓝色饱和度降低 10%」），条件在后续阶段执行 |

---

## 角色激活矩阵

| 角色 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Phase 7 |
|------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| Director | 🟢 执行 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟡 审核 | 🟢 执行 |
| Writer | — | 🟢 产出 | — | 🟢 产出 | — | — | — |
| Art Director | — | — | 🟢 产出 | — | — | — | — |
| DP | — | — | — | 🟢 产出 | — | — | — |
| Sound Designer | — | — | — | — | 🟢 产出 | — | — |
| VFX | — | — | — | — | — | 🟢 产出 | — |

🟢 = 执行/产出 &nbsp;&nbsp; 🟡 = 审核 &nbsp;&nbsp; — = 不激活

---

## 跨阶段依赖

- Phase 3 可读取 Phase 2 的 `script.scenes[]`（场景列表），但不读取 Phase 4 的对白
- Phase 4 串行：Writer 先产出 → DP 再叠加镜头（防止 DP 影响对白）
- Phase 5 可读取 Phase 4 的完整产出（声音需知道每个场景的情绪）
- Phase 6 读取全部前置产出（集成点）
- VFX 在 Phase 6 被激活，其标注叠加到分镜 panel 上
