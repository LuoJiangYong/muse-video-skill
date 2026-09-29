# 生图模型路由与适配 — Image-Gen Routing

> **角色**：生图模型选择与参数适配中枢 —— 选择流程 + 适配章节（每模型一节，标题即注册）+ 参考图注入规则。首次生图前决定「用哪个模型、带哪些参考图、什么参数」。
> **边界**：本文件定义选择与参数规范（含已验证命令模板）；实际生图调用由 Agent 在 Phase 3.5 / 6 / 7 序列中执行（调用用户配置的工具）。不持有执行逻辑。
> **被依赖**：`pipelines/default.md`（Phase 3 步骤 4 / 3.5 / 6 步骤 5 / 7 选项 C）
> **宪法位置**：`references/image-gen-routing.md` — 交叉关注点，放 references 根目录（镜像 `model-compiler.md` 的多模型适配模式）。
> **最后更新**：2026-09-29 | v0.33.0

---

## 生图模型选择（流程）

> 与 Phase 7.5 视频侧 `model-compiler.md` §模型选择 同构：**先选模型，再生成**；已适配列表从本文「适配：<模型名>」章节标题解析。

**触发时机**：首次生图前——通常 Phase 3.5 步骤 0；若 3.5 被跳过（image_gen 不可用或用户要求跳过），顺延至最早的生成点（Phase 3 步骤 4 / Phase 6 步骤 5）随首次生成触发。选择结果跨 Phase 复用，不重复询问（除用户主动更换）。

1. **探测可用能力**（当前会话环境）：
   - `arkcli`（`arkcli auth status` → `logged_in: true` 时可用；模型 = profile 默认 or 用户指定）
   - ComfyUI（本地，用户声明或探测）
   - 会话内可用生图工具（以实际环境为准）
   - 用户指定（含自备工具）
2. **展示候选**：≤3 个 + 「其他（告诉我模型/工具名）」+ 「帮我推荐」
3. **询问规则**：
   - 候选 ≥2 → **显式询问**；仅 1 个 → 告知并确认，不追问
   - 探测不到 → 直接询问用户「你配置/打算用哪个生图工具或模型？」
   - 「帮我推荐」→ 按项目特征推荐：本地免费优先 ComfyUI；云端质量 → Seedream；快速原型 → 轻量工具
4. **路由**：命中「适配：<模型名>」章节 → 载入参数；**无适配章节 → 走 §未适配模型处理**
5. **落点**：写入 Project State `image_gen.target_model`（+ `_meta.selected_phase`）

---

## 未适配模型处理

> 「skill 没有已有参数的 → 查对应模型文档」（2026-09-28 裁定）。

1. **Agent 读取官方文档**：`web_extract` / `browser_navigate` 打开模型官方文档
2. **提炼五要素**：模型 ID / 调用方式（CLI / API）/ 参考图输入能力（张数 / 强度参数 / 输入类型）/ 尺寸与比例限制 / 关键参数
3. **构建临时参数集**：按提炼结果组装调用模板，标注 **「📄 文档推断·未实测」**
4. **首案例试跑**：最小成本生成 1 张 + 用户确认后，才进入批量生成
5. **升级路径**：试跑通过后，可在后续迭代把参数固化回本文档的新「适配」章节（标注 ✅ 实测）

---

## 参考图注入规则

> 生成时从顶层 `file_registry` 选择参考图注入（用途 → 参考图映射）；本地文件形式统一 `file://D:/<正斜杠路径>`（Seedream 见 §适配；其他模型按各自章节）。

| 生成用途 | 注入的参考图 | 强度建议 |
|---------|-------------|---------|
| 角色概念图 | 该角色的用户参考照片（role=reference_image，weight 0.8-1.0 的角色锚）；无用户照片 → 纯文字 | 按模型能力（ComfyUI IP-Adapter 0.6-0.8） |
| 场景 moodboard | 该场景的实景参考图（用户 / 搜索，role=reference_image） | 0.5-0.7 语义 |
| 分镜 panel（含角色） | 角色锚 refs + 场景 refs（多参考） | 角色高 / 场景中 |
| 分镜 panel（空镜） | 场景 refs | 0.5-0.7 语义 |
| 产品资产图 / 道具资产图（门禁选定） | 用户提供的产品/道具素材（role=reference_image）；无 → 纯文字 | 0.5-0.7 语义 |

- **强度映射**：`file_registry.weight` 为**视频侧**（Seedance reference_image_weight）语义；生图侧强度按各模型自己的能力参数映射（Seedream 无显式强度参数——经提示词措辞控制；ComfyUI 用 IP-Adapter weight）。**不得混用权重数值**。
- **模型不支持参考图输入** → 降级纯文字 prompt + 显式警告「模型不支持参考图，角色/场景一致性降级」。
- **引用纪律**：注入的 refs 适用 `references/reference-image-over-text.md`（不重述、不转述）。
- **登记回写**：生成产物按 `pipelines/default.md` 序列登记顶层 `file_registry`（`source: "generated"`；批次 F1 起属门禁选定资产范围的产物追加 `asset` 三键，协议见 `references/reference-image-over-text.md` §资产引用协议）；本 panel 用了哪些 refs 记录到 `storyboard[].refs_used`。

---

## 适配：Seedream（arkcli）

> **调用工具**：`arkcli +gen --modality image`｜**实测状态**：✅ 2026-09-29 实测通过（单参考 + 双参考各 1 例）

### 参考图能力矩阵

| 能力 | 实测/说明 |
|------|----------|
| 参考图张数 | 多张（`--input` 可重复；2 张实测通过；上限以官方文档为准） |
| 强度参数 | 无显式参数——参考强度经提示词措辞控制 |
| 输入形式 | **`ref:file://D:/<正斜杠绝对路径>`（钉定通道）** / 公网 URL |
| 输出尺寸 | `--size`（4.5 下限 ≈3.69M px，如 2048x2048） |
| 输出格式 | `--output-format jpeg\|png`（未实测） |
| 水印 | 强制「AI生成」标识（实测 `--watermark=false` 未能去除） |

### 参数速查

| 参数 | 用途 |
|------|------|
| `--modality image` | **必须**（否则默认走视频端点） |
| `--input 'ref:file://D:/...'` | 参考图（可重复） |
| `--size 2048x2048` | 输出尺寸 |
| `--image-count/-n` | 多张输出（未实测） |
| `--seed` | 可复现（未实测） |
| `--save-to <dir>` | 输出目录（**固定文件名 `ark-gen.jpeg`——多次生成须独立目录或立即改名**） |
| `--debug` | 显示请求/响应详情 |
| `--dry-run` | 免费预览请求构造（⚠️ 不检验真实可跑性，见下） |

### 已实测命令（2026-09-29）

```bash
arkcli +gen --model doubao-seedream-4-5-251128 --modality image --size 2048x2048 \
  --input 'ref:file://D:/<绝对路径>/角色参考.jpg' \
  --input 'ref:file://D:/<绝对路径>/场景参考.jpg' \
  --save-to "<输出目录>" \
  "prompt..."
```

### ⚠️ 陷阱（Windows）

- **不要用 `@路径`**（反斜杠 / 正斜杠 / 相对路径 / MSYS 路径全部失败——`invalid port` bug，v1.0.1 未修复）
- 三斜杠 `file:///D:/...` 也不可用（打开 `/D:/...` 失败）——**必须用两斜杠 + 盘符形式 `file://D:/...`**
- 输出固定文件名 `ark-gen.jpeg`：批量生成时必须逐张改名 / 独立目录
- dry-run `validated: true` ≠ 真实可跑（`@`形式 dry 全过、真跑全挂）

### 模型 ID

| 模型 | ID | 备注 |
|------|-----|------|
| Seedream 4.5（主力） | `doubao-seedream-4-5-251128` | 本次实测所用 |
| Seedream 5.0 | `doubao-seedream-5-0-260128` | 同族；参数预计一致（未实测） |

---

## 适配：ComfyUI（Flux / SDXL + IP-Adapter / FaceID）

> **调用工具**：ComfyUI 本地工作流｜**实测状态**：📄 按本仓库既有材料归纳（`media/character-consistency.md` / `media/image-gen-guide.md`）；本机未实测（需本地 GPU 环境）

### 参考图能力矩阵

| 能力 | 说明 |
|------|------|
| 参考图张数 | 取决于工作流（IP-Adapter 可多路） |
| 强度参数 | IP-Adapter weight 0.6-0.8 / FaceID weight 0.8-1.0（见 `references/media/character-consistency.md`） |
| 输入形式 | 本地文件路径（工作流 LoadImage 节点） |
| 输出尺寸 | 1024×576 (16:9) / 1024×1792 (9:16)（Flux） |
| 输出格式 | PNG（含工作流元数据） |

### 要点

- 角色一致性组合：IP-Adapter（跨镜头）+ FaceID（面部特写）（策略矩阵见 `references/media/character-consistency.md`）
- 参数速查（Flux: steps 20-28 / CFG 3.5-5.0；SDXL: steps 25-40 / CFG 5-8）见 `references/media/image-gen-guide.md`
- prompt 模板：使用 `media/image-gen-guide.md` 的分镜图 / 角色设计模板

---

## 扩展指南

> 新增生图模型支持时，在本文件末尾追加「适配：<模型名>」章节（章节标题即注册——选择流程自动解析）。

### 必填项

1. **模型标识**：模型 ID / 调用工具
2. **参考图能力矩阵**：张数上限 / 强度参数 / 输入类型 / 尺寸下限 / 输出格式
3. **参数速查 + 调用示例**
4. **实测状态标注**：✅ 实测（≥1 个真实案例）或 📄 文档推断

### 测试要求

5. **至少 1 个实测案例**：用真实参考图生成并目检注入效果

---

> 相关：`references/media/image-gen-guide.md`（prompt 怎么写）· `references/media/character-consistency.md`（一致性策略）· `references/free-image-sources.md`（参考图从哪来）· `references/model-compiler.md`（视频侧编译，同构路由模式）
