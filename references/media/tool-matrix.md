# 工具矩阵 — Tool Selection Matrix

> **定位**：帮助 Agent 和用户决定「这个项目/这个阶段用哪个工具？」。不是工具教程——是决策指南。
> **覆盖工具**：ComfyUI / HyperFrames / Kling / Runway / Pika / Suno / LibTV / TAPNOW / 即梦 / happyhorse。以 Muse Video 的产出物（Creative Package）为起点倒推工具选择。
> **宪法约束**：Muse Video 不生成实际视频/音频——只产出 Creative Package。本矩阵帮助用户将 Package 中的每个部分对接到正确的工具。

---

## 工具能力总览

| 工具 | 能做 | 不能做 | 学习曲线 | 成本 |
|------|------|--------|---------|------|
| **ComfyUI** | 静帧生图、风格迁移、局部重绘、视频生成（AnimateDiff/VideoCrafter） | 实时渲染、音频、视频剪辑、字幕叠加 | 陡峭（节点式） | 本地免费 / 云端付费 |
| **HyperFrames** | HTML 视频合成（场景+动画+字幕+配乐），文本/图像/音频混合编排 | AI 生图/生视频（它是合成器，不是生成器） | 中等 | 本地免费 |
| **Kling** | 高质量文生视频/图生视频，最长 2min | 静帧出图不如 Flux、音频 | 低（网页端） | 按秒付费 |
| **Runway** | 视频生成（Gen-3 Alpha）、视频编辑、运动笔刷、绿幕 | 静帧出图（已弱化）、音频 | 低 | 订阅制 |
| **Pika** | 快速文生视频/图生视频、视频风格化 | 长视频、复杂场景 | 极低 | 免费额度+付费 |
| **Suno AI** | AI 音乐生成（含歌词+人声） | 视频、图像、音效设计 | 低 | 免费额度+付费 |
| **LibTV (liblib.tv)** | AI 图片/视频生成+编辑，中文 prompt 友好，风格模型丰富 | 实时渲染、复杂 3D、音频 | 低 | 免费额度+付费 |
| **TAPNOW** | 快速 AI 创意出图，移动端友好，一键风格迁移 | 视频生成、精细参数控制 | 极低 | 免费额度+付费 |
| **即梦 (Jimeng)** | 高质量 AI 图片/视频生成，中文语义理解强，集成抖音生态 | 专业级节点式精细控制 | 低 | 免费额度+付费 |
| **happyhorse (阿里快马)** | AI 图片生成，通义系列模型，电商场景优化 | 视频生成、音频 | 低 | 免费额度+付费 |

---

## 决策树：从 Creative Package 到工具

```
我的 Creative Package 中有 [X]，该用什么工具生成？

1. 分镜参考图（storyboard image_prompt）
   → ComfyUI (Flux/SDXL) 静帧生图
   理由：质量最高、可控性最强、可配合 IP-Adapter 等一致性工具

2. 动态视频片段（需要从零生成）
   ├─ 质量优先、预算充足 → Kling / Runway Gen-3
   │   理由：目前视频生成质量天花板
   ├─ 快速原型 / 低成本 → Pika
   │   理由：最快从文字到视频
   └─ 需要精确控制（指定相机运动、时间轴）→ ComfyUI + AnimateDiff
       理由：最可控，但需要技术能力

3. 视频合成（已有素材→拼接+特效+字幕+配乐）
   → HyperFrames
   理由：为 HTML 视频合成而设计，原生支持字幕+动画+音频同步

4. 配乐/背景音乐
   → Suno AI
   理由：AI 音乐生成的最佳选择，支持风格定制+人声

5. 音效设计
   ├─ 通用音效 → 音效素材库（Artlist/Epidemic Sound）
   └─ 特殊音效（全息投影声/能量场声）→ 合成器 / 后期处理
```

---

## 各场景类型推荐工具链

| 场景类型 | 参考图 | 视频片段 | 合成+字幕+配乐 | 音效 |
|---------|--------|---------|--------------|------|
| **棚拍广告** | ComfyUI (Flux) 生成 moodboard + 分镜图 | Kling/Runway（如果做动态广告） | HyperFrames | 素材库 |
| **产品演示** | ComfyUI (SDXL) + 精确产品 prompt | Kling（产品动态展示） | HyperFrames | 素材库 + UI 音效 |
| **LOGO 演绎** | ComfyUI (Flux/SDXL) | ComfyUI + AnimateDiff 或 HyperFrames（CSS 动画） | HyperFrames | 合成器 |
| **科幻设定** | ComfyUI (Flux) 电影感静帧 | Kling / Runway | HyperFrames | 合成器 + 素材库 |

---

## 工具切换信号

| 当前工具 | 信号 | 切换目标 |
|---------|------|---------|
| **ComfyUI** | 生成的图风格不稳定、画质达到瓶颈 | 检查 prompt 和参数 → 考虑升级到 Flux（如用 SDXL） |
| **Kling** | 视频动作不自然、角色变形 | Runway（Gen-3 Alpha 角色一致性更好） |
| **Runway** | 场景太复杂、时间太长 | Kling（复杂场景上限更高） |
| **HyperFrames** | 需要复杂的 3D 变换/CG 特效 | ComfyUI + AnimateDiff / Blender |
| **Suno** | 音乐风格不够精确、长度不够 | 多段拼接 or 考虑素材库授权音乐 |

---

## Creative Package → 工具输入映射

| Creative Package 字段 | 对应工具 | 如何输入 |
|----------------------|---------|---------|
| `storyboard.panels[].image_prompt` | ComfyUI | 直接作为 positive prompt 输入 |
| `visual_dev.color_palette[]` | ComfyUI / HyperFrames | ComfyUI 用 color LUT；HyperFrames 用 CSS 变量 |
| `cinematography.shot_list[]` | 所有视频工具 | 作为镜头描述注入视频生成 prompt |
| `script.scenes[]` | HyperFrames | 作为时间轴场景描述 |
| `storyboard.panels[].camera` | HyperFrames / Kling | HyperFrames 用 CSS transform 模拟；Kling 用 camera control 描述 |
| `sound.music_style` | Suno AI | 作为风格 prompt 输入 |
| `sound.sfx_map[]` | 素材库 | 作为搜索关键词 |
| `sound.narration_tone` | 任何 TTS 工具 | 作为语音合成参数（语速/语调/音色） |

---

## 成本-质量权衡

```
                         高成本 × 高质量
                              │
                    Kling ────┼──── Runway Gen-3
                              │
              ComfyUI+LoRA ───┼──── ComfyUI+Flux
                              │
        ComfyUI+SDXL ─────────┼──── Suno Pro
                              │
   HyperFrames ───────────────┼──── Pika
                              │
                         低成本 × 快速
```

### 推荐起步方案（零预算）

1. **参考图**：ComfyUI（本地免费）+ Flux/SDXL 模型
2. **视频合成**：HyperFrames（本地免费）
3. **音乐**：Suno 免费额度
4. **音效**：免费素材库（Freesound.org / Pixabay）

### 推荐进阶方案（有预算）

1. **参考图**：ComfyUI + 定制 LoRA（角色一致性）
2. **视频片段**：Kling（高质量动态片段）
3. **视频合成**：HyperFrames
4. **音乐**：Suno Pro（商业授权）
5. **音效**：Artlist / Epidemic Sound 订阅

---

## Agent 注入 Prompt 段落

```
当用户需要选择下游工具时：

1. 确认 Creative Package 的哪个部分需要生成
2. 用决策树匹配最佳工具
3. 参考成本-质量权衡表给出选项（至少给「免费方案」和「最佳质量方案」两个选项）
4. 如果用户说「我不知道用哪个」→ 默认推荐：ComfyUI（参考图）+ HyperFrames（合成）+ Suno（音乐）
5. 不要替用户决定预算——列出选项，让用户选择
```
