# Model Compiler（模型编译器）

> **角色**：读取 Project State 中所有创意角色的产出，编译为目标 AI 视频模型的调用指令。不执行网络请求，不修改上游数据。
> **边界声明**：本编译器产出模型调用指令**文本**（CLI 命令或 API JSON）。实际执行由 `volcengine-ark` skill 或用户手动完成。编译器是格式转换层，不是执行层。
> **宪法位置**：`references/model-compiler.md` — 交叉关注点，非创意角色，放在 references 根目录。
> **最后更新**：2026-06-29 | v0.30.0

---

## 边界声明

1. **只读消费者**：编译器读取 Project State 的所有上游字段（script / cinematography / visual_dev / sound / storyboard），不修改任何上游产出。
2. **不执行网络请求**：产出的 `arkcli_command` 是文本，不调用 `arkcli`。File Registry 中的 `file_id` 来自 Phase 3.5/6 或其他阶段的上传——编译器只引用，不上传。
3. **不替代创意判断**：编译器不会「修正」Writer 的场景描述或 DP 的运镜选择。它只做格式转换——中文术语→英文 prompt、分散字段→合并模板。
4. **质量标记不阻塞**：遇到劣质输入时标记警告（GOOD/DEGRADED/INSUFFICIENT），但不回退上游阶段。`INSUFFICIENT` 级别暂停等用户确认。

---

## 输入（从 Project State 读取的字段）

| 字段路径 | 用途 | 映射到 |
|----------|------|--------|
| `project.scene_type` | 选择分配策略 | slot_allocation 策略选择 |
| `project.aspect_ratio` | 画面比例 | arkcli --ratio |
| `director_notes.vision` | 创意方向校验 | 编译一致性参考 |
| `director_notes.has_characters` | 角色存在性判定 | 选择 character_driven vs 其他分配策略 |
| `script.scenes[]` | 场景描述（location / action / dialogue） | 六段式 Subject + Action + Scene 段 |
| `script.scenes[].camera` | 镜头方向（shot_type / movement / lens / lighting） | 六段式 Camera + Lighting 段 + 术语翻译表 |
| `visual_dev.palette[]` | 色调方案（含 visual_cause） | 六段式 Lighting 段 |
| `visual_dev.mood` | 视觉情绪 | 六段式 Style 段 |
| `visual_dev.style_direction` | 风格方向 | 六段式 Style 段 |
| `visual_dev.characters[]` | 角色视觉设定（traits / consistency_notes） | 六段式 Subject 段细节 |
| `visual_dev.scene_composition[]` | 场景空间布局 | 六段式 Scene 段细节 |
| `cinematography.camera_style` | 全局摄影风格 | 术语翻译偏好 |
| `cinematography.movement_language` | 运动语言偏好 | 术语翻译消歧 |
| `sound.music_style` | 配乐风格 | audio_config |
| `sound.narration_tone` | 旁白基调 | audio_prompt |
| `storyboard[]` | 分镜面板（含 prompt / camera_notes / vfx_notes） | multimodal_refs + 编译交叉校验 |

---

## 输出（model_compilation JSON schema）

输出写入 Project State 的 `model_compilation` 字段。完整 schema 见 `assets/schemas/project-state.json`。

核心结构：
```jsonc
{
  "model_compilation": {
    "_meta": { "compiler_version": "1.0.0", "target_model": "...", "director_approved": false },
    "target_model": "doubao-seedance-2-0-260128",
    "file_registry": { /* file_id 映射表，含 local_path */ },
    "shots": [ /* 每镜编译结果 */ ],
    "shot_chain": { /* video_ref 链 */ }
  }
}
```

每个 shot 含：`compiled_prompt`（六段式合并）、`prompt_trace`（逐段溯源）、`multimodal_refs`（文件引用）、`slot_allocation`（5 槽分配）、`arkcli_command`（可执行命令）、`estimated_tokens`（成本估算）、`_quality`（质量标记）。

---

## 通用编译流程

```
1. 读取 Project State → 提取所有输入字段（见上表）
2. 检测 target_model → 跳转对应适配章节（当前仅 Seedance 2.0）
3. 确定分配策略（character_driven / product_driven / graphic_driven）
4. 逐镜编译：
   a. 六段式 prompt 编译（保留 Narrative Anchor）→ compiled_prompt
   b. 镜头运动术语翻译（双层查表：默认→场景覆盖→movement_language 消歧）
   c. 5 槽分配（三套策略）
   d. 多模态引用映射
   e. 质量标记（GOOD/DEGRADED/INSUFFICIENT）
   f. 成本估算
5. 构建 video_ref 镜头链
6. 生成 arkcli 命令（Windows 安全路径：Files API + --extra-body）
7. 运行干跑验证清单
8. 输出编译摘要给用户
```

---

## 稀疏输入处理

六段式编译模板不强制 6 段全部非空：

| 段 | 源字段 | 空值处理 |
|----|--------|---------|
| Subject | script.scenes[].action + visual_dev.characters | 空 → 标记 [OMITTED]，从 Scene 段开始 |
| Action | script.scenes[].action | 空 → 标记 [OMITTED] |
| Scene | script.scenes[].location + visual_dev.scene_composition | 空 → 填充 "Interior/Exterior scene" 占位 |
| Camera | script.scenes[].camera + cinematography | 空 → 填充 "Static shot" 默认值，标记质量警告 |
| Lighting | script.scenes[].camera.lighting + visual_dev.palette.visual_cause | 空 → 从 visual_dev.mood 推断，标记质量警告 |
| Style | visual_dev.style_direction + visual_dev.mood | 空 → 填充 "Cinematic, photorealistic" 默认值 |

空段 ≥3 个 → 该 shot 标记为 `_quality.overall = INSUFFICIENT`，编译暂停等用户确认。

---

## 质量标记

每个 shot 编译后输出质量标记：

```jsonc
"_quality": {
  "overall": "GOOD",          // GOOD | DEGRADED | INSUFFICIENT
  "warnings": [
    "camera.movement field is empty — using static default",
    "visual_dev.palette has no visual_cause for scene 1 — Lighting segment may be generic"
  ]
}
```

| 级别 | 条件 | 行为 |
|------|------|------|
| GOOD | 所有段有足够源数据，≤1 个警告 | 正常产出 |
| DEGRADED | 2 个警告或 1 个段使用了默认值 | 正常产出 + 警告列表 |
| INSUFFICIENT | ≥3 段使用了默认值 | **暂停**，要求用户确认后继续 |

---

## 干跑验证清单

编译完成后、执行前，逐项检查：

- [ ] 所有 camera 术语在翻译表中有对应（或标记 `[TRANSLATION_AMBIGUITY]`）
- [ ] 所有 image_ref file_id 在 file_registry 中可查
- [ ] 每镜 duration ≥ 4s（Seedance 2.0 硬下限）
- [ ] resolution 值合法（`4k` / `1080p` / `720p` / `480p`）
- [ ] `--extra-body` JSON 语法有效（无未闭合引号/括号）
- [ ] 每镜 `compiled_prompt` 非空
- [ ] video_ref 链中相邻镜头时长和分辨率一致

---

## 禁止事项

- ❌ 修改上游任何角色的产出字段
- ❌ 执行 arkcli 命令（只产出文本）
- ❌ 在 prompt_trace 中改写原始文本（original 必须逐字复制，compiled 是翻译后版本）
- ❌ 替 Director 做创意判断（比如「这个运镜描述不好，我换成更好的」）
- ❌ 在没有用户确认的情况下跳过 INSUFFICIENT 镜头
- ❌ 为不存在的 file_id 生成引用（必须先查 file_registry）
- ❌ 使用 `--input @本地文件` 语法（Windows bug）——始终走 Files API file_id 路径

---

# 模型适配：Seedance 2.0

> **模型 ID**：`doubao-seedance-2-0-260128`
> **文档**：https://www.volcengine.com/docs/82379/2291680
> **验证状态**：✅ 2026-06-23 实测通过（10s 4K 三幕结构）

---

## Seedance 2.0 多模态输入标签

| 标签 | 用途 | Muse Video 映射来源 |
|------|------|-------------------|
| `first_frame_ref` | 指定视频起始画面 | Phase 6 分镜图 / Phase 3.5 moodboard |
| `last_frame_ref` | 指定结束画面 | Phase 6 下一镜首帧 |
| `image_ref_1..N` | 风格/角色/构图参考（最多 5 张） | Phase 3 AD moodboard + 用户原始照片 |
| `video_ref` | 前一个镜头的输出 → 风格继承 | Phase 6 上一镜视频产出 |
| `audio_ref` | 音频驱动口型/节奏 | Phase 5 Sound Designer 参考音频 |

---

## Prompt 六段式编译模板

Seedance 2.0 推荐结构：**Subject → Action → Scene → Camera → Lighting → Style**

```
<Subject>核心主体描述</Subject>
<Action>主体的动作与细节</Action>
<Scene>场景与环境</Scene>
<Camera>镜头运动与景别</Camera>
<Lighting>光影条件</Lighting>
<Style>艺术风格</Style>
```

### 段映射规则

| 段 | 源字段 | 编译规则 |
|----|--------|---------|
| Subject | `script.scenes[].action` 的主体部分 + `visual_dev.characters[].traits` | 提取角色外观特征。如含情绪锚点（愣住/迟疑/猛然/缓缓），**必须保留**到本段末尾（Narrative Anchor 规则） |
| Action | `script.scenes[].action` 的动作部分 | 提取动作动词和时间副词。保持叙事张力 |
| Scene | `script.scenes[].location` + `visual_dev.scene_composition[scene_id]` | 空间描述 + 关键道具 + 时间。如果 scene_composition 有「前中远景」描述→整合为环境细节 |
| Camera | `script.scenes[].camera` + `cinematography` | 经术语翻译表（见下）转换为英文 |
| Lighting | `script.scenes[].camera.lighting` + `visual_dev.palette[].visual_cause` | visual_cause 优先（已有光的方向/色温/强度参数）；如为空则从 palette 的 name + usage 推断 |
| Style | `visual_dev.style_direction` + `visual_dev.mood` | 合并为 1-2 句风格描述 |

### Narrative Anchor 规则

Writer 的 `action` 字段常含情绪描述（愣住、迟疑、猛然转身、缓缓抬头等），这些在六段式的 Subject / Action 段中没有天然槽位，但它们是影片叙事张力的核心。

**规则**：如果 Writer 的 `script.scenes[].action` 包含以下情绪锚点词，必须在 compiled prompt 的 Subject 段末尾保留：

```
情绪锚点词库：愣住 / 迟疑 / 猛然 / 缓缓 / 颤抖 / 凝视 / 屏息 / 倒退 / 冲 / 扑 / 僵 / 怔 / 呆
```

编译示例：
- 原文：「他推开门，愣住了。房间空无一人，但桌上咖啡还冒着热气。」
- 编译：`A man pushes open a door. He freezes, stunned. The room is empty except for a cup of coffee still steaming on the table.`
- ❌ 错误编译：`A man enters a room. The room is empty.`（丢失了情绪和悬念）

---

## 镜头运动术语翻译表

> **双层结构**：默认映射 + 场景覆盖。`cinematography.movement_language` 字段优先消歧。

### 默认映射

| DP 术语 | Seedance prompt 片段 | FLAG |
|---------|---------------------|------|
| 推（推进） | `Dolly in toward subject, smooth forward movement` | — |
| 拉（拉远） | `Dolly back, camera retreating from subject` | — |
| 摇（水平摇镜） | `Panning left` / `Panning right` | — |
| 移（横移） | `Lateral tracking shot, camera moving sideways` | — |
| 跟（跟拍） | `Following subject, steady tracking shot` | — |
| 升（上升） | `Crane up, camera rising vertically` | — |
| 降（下降） | `Crane down, camera descending vertically` | — |
| 仰拍 | `Low angle shot, camera looking upward` | — |
| 俯拍 | `High angle shot, camera looking downward` | — |
| 特写 | `Extreme close-up shot` / `Close-up shot` | — |
| 中景 | `Medium shot, waist-up framing` | — |
| 全景 | `Wide establishing shot` | — |
| 固定 | `Static camera, locked off tripod` | `--camera-fixed` |
| 手持 | `Handheld camera, subtle natural camera shake` | — |
| 环绕 | `Orbiting camera, circling around subject` | — |
| 急推 | `Snap zoom, rapid push-in` | — |
| 慢推 | `Slow creep zoom, barely perceptible forward motion` | — |
| 过肩 | `Over-the-shoulder shot` | — |
| POV | `POV subjective camera, first person perspective` | — |
| 鸟瞰 | `Bird's eye view, top-down aerial shot` | — |

### 场景覆盖（当默认映射与场景类型冲突时）

| 场景类型 | 术语 | 覆盖 |
|----------|------|------|
| `product-demo` | 推 | `Smooth zoom in on product`（产品展示用变焦，不用 dolly） |
| `product-demo` | 环绕 | `Product turntable rotation, camera orbiting slowly` |
| `logo-animation` | 推 | `Elegant push-in toward logo center` |
| `logo-animation` | 固定 | `Camera locked off, centered composition` + `--camera-fixed` |

### movement_language 消歧

如果 `cinematography.movement_language` 字段有值，翻译偏好向该风格靠拢：

| movement_language | 对「跟」的翻译 | 对「手持」的翻译 |
|-------------------|--------------|----------------|
| `"dolly precision"` | `Precision dolly tracking` | 不使用（风格冲突，回退默认） |
| `"handheld intimate"` | `Intimate handheld follow, slight bounce` | `Natural handheld, documentary-style micro-jitter` |
| `"steadicam smooth"` | `Steadicam glide, floating tracking` | 不使用（回退默认） |

未覆盖的术语 → 编译时附加 `[TRANSLATION_AMBIGUITY]` 标记提醒用户审查。

---

## 5 槽分配算法（三套策略）

Seedance 2.0 每镜最多 5 张 `image_ref`。根据项目类型自动选择分配策略。

### 策略选择

| 策略 | 触发条件 |
|------|---------|
| `character_driven` | `director_notes.has_characters = true`（默认） |
| `product_driven` | `project.scene_type = product-demo` |
| `graphic_driven` | `project.scene_type = logo-animation` |

### 策略 1：character_driven

| 槽位 | 用途 | weight | 分配 |
|------|------|--------|------|
| P0 | 角色锚点 | 0.8-1.0 | 最多 2 个角色各占 1 槽。超过 2 个角色 → 选 screen_time 最多的 2 个。超过 3 个角色 → 选主角 + 关键配角 |
| P1 | first_frame_ref | — | 分镜首帧（独立字段，占用 1 槽） |
| P2 | 场景 mood | 0.5-0.7 | 1 张。多场景 → 选当前镜所在场景的 mood |
| P3 | 风格参考 | 0.4-0.5 | 1 张。AD 的 moodboard 精选 |
| P4 | 道具/服装 | 0.5 | 剩余的 image_ref 槽。无关键道具时留给 first_frame 的补充 |

### 策略 2：product_driven

| 槽位 | 用途 | weight | 分配 |
|------|------|--------|------|
| P0 | 产品参考 | 0.9 | 产品实物图 / 3D 渲染图 |
| P1 | first_frame_ref | — | 分镜首帧 |
| P2 | 场景 mood | 0.6 | 展示环境 mood |
| P3 | 风格参考 | 0.4 | 品牌视觉风格 |
| P4 | 材质参考 | 0.5 | 产品材质特写 |

### 策略 3：graphic_driven

| 槽位 | 用途 | weight | 分配 |
|------|------|--------|------|
| P0 | first_frame_ref | — | 分镜首帧（LOGO 动画的构图锚点） |
| P1 | 风格参考 | 0.4 | 动画风格参考 |
| P2 | 材质参考 | 0.5 | 金属/玻璃/发光材质 |
| P3 | — | — | 空（LOGO 动画通常不需要 5 张图） |
| P4 | — | — | 空 |

### 溢出处理

需求超过 5 张时，`slot_allocation` 列出两组：

```jsonc
"slot_allocation": {
  "strategy": "character_driven",
  "allocated": [ /* P0→P4 按优先级排列 */ ],
  "overflow": [ /* 因上限未分配的参考图 */ ]
}
```

用户可在 `overflow` 中手动调换到 `allocated`。

---

## 角色一致性策略（无需 Seedream 中转）

> ⚠️ 这是 2026-06-23 实测验证的核心发现。

**错误做法**：用 Seedream 以用户照片为参考生成角色设定图 → 再喂 Seedance。

**正确做法**：直接用用户原始照片作为 Seedance 的 `image_ref`（`role: reference_image`, `weight: 0.9`）。Seedance 2.0 的 `reference_image_weight` 参数直接控制面部还原强度，效果优于 Seedream 中转。

编译时：
1. 角色参考图直接入 `file_registry` → `image_ref_1`，weight = 0.9
2. `compiled_prompt` 中描述服装变化：`The character does NOT wear the clothes from the reference image — instead, he wears a...`
3. 场景 mood 图走 Seedream 生成空镜（无人物），weight = 0.6

---

## arkcli 命令生成（Windows 安全路径）

> ⚠️ `--input @本地文件` 在 Windows 上有路径解析 bug（v0.1.17-v1.0.1）。**禁止使用**。

### 正确流程

```bash
# Step 1: 用火山引擎 Files API 上传所有参考图 → 获取 file_id
# （此步骤由 Phase 3.5 或用户手动完成。编译器引用 file_registry 中的已有 file_id）

# Step 2: 编译器生成 --extra-body 注入命令
arkcli +gen \
  --model doubao-seedance-2-0-260128 \
  --duration {shot.duration} --resolution {shot.resolution} --ratio {project.aspect_ratio} \
  --generate-audio \
  --extra-body '{
    "input":[
      {"type":"input_image","image_url":"file-{character_file_id}","role":"reference_image","reference_image_weight":0.9},
      {"type":"input_image","image_url":"file-{scene_mood_file_id}","role":"reference_image","reference_image_weight":0.6}
    ]
  }' \
  --force --wait "{compiled_prompt}"
```

- **type**: `input_image`
- **image_url**: file_id（优先，无需公网可达）或 HTTP URL
- **role**: `reference_image` / `first_frame` / `last_frame`
- **reference_image_weight**: 0.0-1.0
- **--force**: 必须——extra-body 字段可能不在 arkcli 参数校验 schema 中
- **--wait**: 阻塞直到生成完成

### file_id 生命周期说明

火山引擎 Files API 的 file_id 有效期未在官方文档中明确。实测中数小时内有效。`file_registry` 中每条记录保留 `local_path` 作为备份——如果 file_id 失效，可重新上传。

### 分辨率与成本

| resolution | 参数值 | 最短时长 | tokens/4s | 相对成本 | 建议场景 |
|------------|--------|---------|-----------|---------|---------|
| 4K | `4k` | 4s | ~785,700 | 4× | 最终出片 |
| 1080p | `1080p` | 4s | ~196,425 | 1× | 分镜迭代 |
| 720p | `720p` | 4s | ~98,000 | 0.5× | 快速原型 |
| 480p | `480p` | 4s | ~49,000 | 0.25× | 极速草稿 |

**建议**：分镜迭代用 1080p/720p，最终出片用 4K。

---

## 镜头间一致性控制（video_ref 链）

Seedance 2.0 支持 `video_ref` 保持风格/角色一致：

```
shot_S01: first_frame_ref = storyboard_S01.png
         ↓ 产出 shot_S01.mp4

shot_S02: first_frame_ref = storyboard_S02.png
         video_ref = shot_S01.mp4     ← 继承上一镜的风格/角色特征
         ↓ 产出 shot_S02.mp4

shot_S03: first_frame_ref = storyboard_S03.png
         video_ref = shot_S02.mp4
         ...
```

编译器在 `shot_chain` 中描述链接关系。仅在 Seedance 2.0 可用（1.5 Pro 不支持 video_ref）。

---

## 4K 分辨率验证

| 参数值 | 结果 | 说明 |
|--------|------|------|
| `4k` | ✅ 成功 | 输出 3840×2160 HEVC |
| `2160p` | ❌ 拒绝 | 不在有效枚举中 |
| `3840x2160` | ❌ 拒绝 | 不接受 W×H 格式 |
| `1440p` | ❌ 拒绝 | 2.0 不支持此分辨率 |

---

# 扩展指南

> 新增模型支持时，在本文件末尾追加「模型适配：<模型名>」章节。

## 新增模型需提供的必填项

1. **Prompt 编译模板**：从 Project State 的哪些字段映射到模型的 prompt 格式（如 Seedance 的六段式、Kling 的自由文本）
2. **多模态引用映射**：模型的参考图 API 如何对接 `multimodal_refs` 字段（如 Seedance 的 `image_ref + weight`、Kling 的首帧/尾帧上传）
3. **执行命令/API 模板**：产出的可执行指令格式（CLI 命令字符串 或 REST API JSON body）
4. **成本估算公式**：预估 tokens 或 credits

## 可选项

5. **镜头运动翻译表**：如果模型支持镜头控制（否则跳过）
6. **参考图分配策略**：如果模型的参考图机制与 Seedance 的 5 槽不同（否则复用通用策略）
7. **模型特有约束**：最小时长、分辨率限制、比例限制等

## 测试要求

8. **至少 1 个实测案例**：用实际 Creative Package 编译并验证
