# 下游工具对接 — Downstream Integration

> **定位**：Muse Video 产出 Creative Package 后的下游工具路径。列出可选对接方案及选择指南。
> **更新纪律**：新增下游工具时更新此文件，保持工具列表与实际配置一致。

---

## 合成渲染

| 工具 | 类型 | 适用场景 | 前置条件 |
|------|------|---------|---------|
| **HyperFrames** | HTML 视频合成 | 场景动画、字幕、转场、配乐、渲染 MP4 | `npx hyperframes` 已安装 |
| **FFmpeg** | 命令行合成 | 简单拼接、字幕烧录、手动后期 | `ffmpeg` binary（几乎总是可用） |
| 手动制作 | — | 用导出的 HTML/Excel 作为拍摄参考 | 无 |

## AI 视频生成

| 工具 | 类型 | 适用场景 | 前置条件 |
|------|------|---------|---------|
| **火山引擎 arkcli** | 云端 CLI | Seedance 2.0 视频生成，逐镜精确控制 | `npm i -g @volcengine/ark-cli` + API key |
| **Kling** | 云端 API | 高质量短视频 | API key |
| **Runway Gen-4** | 云端 API | 电影级质量 | API key |
| **Pika** | 云端 API | 快速原型 | API key |
| **ComfyUI** | 本地/云端 | SDXL/Flux/Wan/Hunyuan 图片+视频 | GPU ≥6GB 或 Comfy Cloud |

## AI 图片生成

| 工具 | 类型 | 适用场景 | 前置条件 |
|------|------|---------|---------|
| **ComfyUI** | 本地/云端 | 分镜图、moodboard、角色概念图 | GPU ≥6GB |
| **FAL.ai / image_gen** | 云端 API | 快速出图（FLUX 等） | API key |
| **火山引擎 Seedream** | 云端 CLI | 高质量角色图/场景图 | `arkcli` + API key |

## 音频

| 工具 | 类型 | 适用场景 | 前置条件 |
|------|------|---------|---------|
| **HyperFrames Media** | 本地 | Kokoro TTS（54 种声音）+ Whisper 字幕 | HyperFrames 已安装 |
| **Suno AI** | 云端 API | AI 音乐生成 | Suno 账号 |
| **HeartMuLa** | 本地 | 开源音乐生成 | GPU ≥8GB |
| 免版税素材 | 免费 | archive.org / Free Music Assembly | 无 |

## 封面设计

| 工具 | 类型 | 适用场景 | 前置条件 |
|------|------|---------|---------|
| **cover-design-guide** | HTML 模板 | 视频号 3:4 + 小红书 4:3 封面 | 见 `references/cover-design-guide.md` |

---

## 选择指南

1. **有分镜需求 → 火山引擎 arkcli**（Muse Video 精细分镜管线首选）
2. **快速原型 → LibTV / ComfyUI**（"一句话出片"）
3. **本地优先 → ComfyUI**（需 GPU）
4. **零成本 → HyperFrames + 免版税素材 + Piper TTS**
