# 火山引擎（方舟 Ark）视频生成 API 对接指南

> 最后更新：2026-06-29 | 基于 arkcli v1.0.1 实际操作验证 + Seedream 4.5/5.0 图生图 + Seedance 2.0 4K 视频生成

## arkcli vs LibTV 路由决策

| 场景 | 选 arkcli | 选 LibTV |
|---|---|---|
| Muse Video 精细分镜（逐镜 prompt 控制） | ✅ | ❌ 后端 Agent 会重新拆解 |
| 一句话出片（无分镜需求） | ⚠️ 过于重量 | ✅ |
| 需要图生视频（参考图/首帧） | ✅ `--input ref:URL` | ✅ 需先上传 OSS |
| 批量并发多镜头 | ✅ shell 循环逐条调 | ❌ 单会话串行 |
| 调试失败镜头 | ✅ 单镜重试 | ❌ 黑盒 |
| 透明定价 | ✅ `arkcli pricing` | ❌ |
| 接入零代码 | ✅ CLI 一行命令 | ✅ 3 行 Python |
| 多模型聚合（Kling/Wan） | ❌ 仅豆包系列 | ✅ |

> **铁律**：Muse Video 管线产出分镜 → arkcli。用户说「帮我快速做一个短视频」→ LibTV。

## 为什么选火山引擎直连而非 LibTV

| 考量 | 火山直连 | LibTV（LiblibAI） |
|---|---|---|
| **Muse Video 分镜精度** | ✅ 逐镜一一对应，不改写 prompt | ❌ 后端 Agent 重新拆解，失去控制 |
| **视频风格一致性** | ✅ 同一 seed + 模板，全片统一 | ⚠️ 后端 Agent 每次可能不同策略 |
| **成本透明** | ✅ 按 token 计费 | ❌ 不透明 |
| **调试** | ✅ 逐镜查看返回，失败可单镜重试 | ❌ 黑盒 |
| **批量处理** | ✅ 并发调用 N 个镜头 | ❌ 单会话串行 |
| **接入复杂度** | ✅ `arkcli +gen` 一行命令 | ✅ 3 行命令 |

> **路由决策**：Muse Video 精细分镜管线 → 火山直连。用户说「帮我快速生成一个短视频」（无分镜需求）→ LibTV。

## 平台信息

- **平台名称**：火山方舟（Ark）
- **文档入口**：https://www.volcengine.com/docs/82379
- **控制台**：https://console.volcengine.com/ark
- **CLI 工具**（推荐）：`npm i -g @volcengine/ark-cli` → 二进制名 `arkcli`（非 `ark`）
- **SDK**（备选）：`pip install volcenginesdkarkruntime`
- **Base URL**：`https://ark.cn-beijing.volces.com/api/v3/`
- **鉴权**：`arkcli auth login --no-browser`（SSO，推荐）或 AK/SK（在控制台 IAM 创建）

## arkcli 快速上手

`arkcli` 是官方 CLI 工具（v0.1.17+），**一行命令搞定图片/视频生成**，消除了本指南此前建议的 ~150 行 Python 编排脚本需求。

```bash
# 安装
npm i -g @volcengine/ark-cli@latest

# 登录（agent/沙箱环境用 --no-browser）
arkcli auth login --no-browser
# → 浏览器完成 SSO → 拿到 base64 授权码 →
arkcli auth login --no-browser --code <授权码>

# 分镜图（Seedream 4.5）⚠️ 必须加 --modality image
arkcli +gen --model doubao-seedream-4-5-251128 --modality image --size 2048x2048 \
  "赛博朋克城市夜景，霓虹灯雨，低角度仰拍"

# 视频生成（Seedance 2.0，同步等待）
arkcli +gen --model doubao-seedance-2-0-260128 \
  --duration 10 --resolution 4k --ratio 16:9 --generate-audio --wait \
  "prompt"

# 图生视频（用分镜图做首帧）
arkcli +gen --model doubao-seedance-1-5-pro-251215 \
  --input @storyboard_S03.png --duration 5 --wait \
  "保持画面构图，镜头缓慢推进"

# 快速迭代用草稿模式（更快更便宜）
arkcli +gen --model doubao-seedance-1-5-pro-251215 --draft --duration 3 --wait "..."

# 异步提交（不阻塞）+ 后续轮询
arkcli +gen --model doubao-seedance-2-0 --duration 5 "..."  # → task_id
arkcli gen get <task_id>  # 下载完成后的视频
arkcli gen list            # 查看所有异步任务
```

### arkcli 关键 flags

| Flag | 用途 |
|---|---|
| `--model <id>` | 模型 ID（seedance-2-0 / seedance-1-5-pro / seedream-5-0） |
| `--duration <秒>` | 视频时长 |
| `--wait` | 阻塞直到视频生成完成 |
| `--draft` | 草稿模式：更快更便宜，迭代用 |
| `--input @file` | 参考图片/视频（`@` 前缀 = 本地文件） |
| `--input first:URL` | 首帧参考（远程 URL） |
| `--generate-audio` | 生成同步音频 |
| `--camera-fixed` | 锁定虚拟摄像机不动 |
| `--save-to <dir>` | 保存目录（默认当前目录） |
| `--seed <int>` | 固定 seed 保证可复现 |
| `--ratio 16:9` | 画面比例 |

### arkcli 其他有用命令

| 命令 | 用途 |
|---|---|
| `arkcli models search seedance` | 查可用 Seedance 模型版本 |
| `arkcli pricing models` | 查当前账号定价 |
| `arkcli usage balance` | 查免费额度/资源包余额 |
| `arkcli usage stats --start ... --end ...` | 查用量统计 |
| `arkcli resources list` | 列当前 profile 可用资源 |
| `arkcli profile create` | 多项目/region 切换 |
| `arkcli helper configure hermes` | 配置 Hermes Agent Plan 集成 |

## 接入陷坑与已验证方案

### ⚠️ --input @file Windows 路径 bug (v0.1.17-v1.0.1)

`--input @file` 在 Windows 上将反斜杠路径转为 `file://D:\\...` URL 时解析失败（`invalid port` 错误）。**Workaround**: 用 HTTP URL 作为 --input 值（`--input "https://url/to/image.png"`）。模型可接受公网可达的 URL。也可用 Python SDK 通过 Base64 传图绕过此限制。`--input` 支持 role 前缀：`first:` / `last:` / `ref:` / `none:`。

### ⚠️ --ratio 2.39:1 不支持 seedance 2.0

宽银幕比例 `--ratio 2.39:1` API 报 `not valid for model`。用 `--ratio 16:9` 生成后在后期合成裁剪。

### ⚠️ 模型 ID 必须带版本号

裸名如 `doubao-seedance-2-0` 报 `does not exist`。正确格式：`doubao-seedance-2-0-260128`、`doubao-seedance-1-5-pro-251215`、`doubao-seedream-4-5-251128`。通过 `arkcli models search <name>` 查 `primary_version` 字段或从控制台文档获取。

### ⚠️ Seedream 必须加 --modality image

不加此 flag → arkcli 默认走视频端点 → `model_not_found (控制面可见但数据面 not found)`。这不是模型未开通——加 `--modality image` 即通。正确 ID：`doubao-seedream-4-5-251128` / `doubao-seedream-5-0-260128`。

### SSO + Profile 创建（非交互终端）

Agent 环境（非交互终端）下的完整接入流程（2026-06-21 实际跑通）：

```bash
# Step 1: 获取授权 URL
arkcli auth login --no-browser
# → 浏览器打开 authorize_url → 完成登录 → 复制授权码

# Step 2: 提交授权码（此步 SSO 成功但项目选择在 agent 环境会失败，正常）
arkcli auth login --no-browser --code "<授权码>"

# Step 3: 手动创建 Profile（绕过交互式项目选择）
arkcli profile create \
  --type platform \
  --project default \
  --region cn-beijing \
  --no-interactive \
  --set-default

# 验证
arkcli auth status    # → logged_in: true
arkcli profile show   # → base_url + api_key
```

**陷阱**：
- `--no-browser` flag 在 `login` 层，**不在** `volc-sso` 子命令层
- SSO 后的交互式项目选择在 agent 环境必失败 → 必须手动 `profile create --no-interactive`
- 授权码有效期仅 10 分钟
- `+connect` 安装技能在公开版二进制中不含内嵌 skill（需内场版本）

### Seedream 尺寸下限

`doubao-seedream-4-5` 要求最低 **3,686,400 像素**（≈ 2048×2048）。1280×720 = 921,600 会报错：
```
image size must be at least 3686400 pixels
```
解决：`--size 2048x2048` 或 `--size 2K`。

| 模型 | ID | 用途 | 备注 |
|---|---|---|---|
| **Seedance 2.0** | `doubao-seedance-2-0-260128` | 视频生成（4K） | --resolution 4k，~785K tokens/4s |
| **Seedance 1.5 Pro** | `doubao-seedance-1-5-pro-251215` | 视频生成（draft） | draft + camera_fixed 支持 |
| **Seedream 5.0** | `doubao-seedream-5-0-260128` | 图片生成 | ⚠️ 必须 --modality image |
| **Seedream 4.5** | `doubao-seedream-4-5-251128` | 图片生成（主力） | ⚠️ 必须 --modality image，≥2048×2048 |

## 计费

Seedance 2.0：输入 45 元/M token，输出 45 元/M token。

**5 秒视频参考成本：**
- 480p：~2.31 元
- 720p：~4.97 元
- 1080p：~12.26 元

新用户有免费试用额度。

## 调用示例（Python）

```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(
    ak=os.environ["VOLC_ACCESSKEY"],
    sk=os.environ["VOLC_SECRETKEY"]
)

# 图生视频（分镜关键帧 → 视频片段）
response = client.responses.create(
    model="doubao-seedance-2.0",
    input="赛博朋克城市夜景，镜头从地面缓慢上升，霓虹灯光在雨水中反射",
    video={
        "duration": 5,
        "resolution": "720p",
        "reference_image": ref_img_url  # 来自 Seedream 的分镜图
    }
)

# 生分镜关键帧
img_response = client.images.generate(
    model="doubao-seedream-5.0",
    prompt="赛博朋克城市夜景，霓虹灯雨，低角度仰拍，16:9",
    size="1280x720"
)
```

## 在 Muse Video 工作流中的位置

```
Muse Video Creative Package
        │
        ├─ Phase 7.5 模型编译 → model_compilation JSON
        │                        (六段式 prompt + image_ref + arkcli cmd)
        │
        ├─ Phase 6 分镜 → Seedream 5.0 生成分镜关键帧
        │                  (替换原 image_gen 调用)
        │
        ├─ 逐镜生成 → Seedance 2.0 图生视频
        │              (用 model_compilation 中的 arkcli 命令)
        │
        └─ 最终合成 → HyperFrames
```

## Prompt Compiler 设计思路

Muse Video 产出的是给人读的分镜描述（含镜头语言、光影、构图），需要编译成 Seedance 能消费的格式：

```json
{
  "shot_id": "S03",
  "model": "doubao-seedance-2.0",
  "prompt": "赛博朋克城市夜景，霓虹灯雨，低角度仰拍，镜头缓慢上升...",
  "reference_image": "storyboard_S03.png",
  "duration": 5,
  "resolution": "720p",
  "motion": "camera_pan_up"
}
```

Prompt Compiler 的职责：从 Creative Package 的分镜描述 + 导演备注 → 提取核心视觉元素 → 去掉叙事性语言 → 组装为英文/中文 prompt。关键是**不丢失 Muse Video 阶段的导演意图**。

> **v0.30.0 更新**：Prompt Compiler 已正式升级为 Phase 7.5 Model Compiler（见 `references/model-compiler.md`）。此处保留设计思路原文作为历史参考。
