# 生图指南 — Image Generation Guide

> **定位**：各场景提示词模板的中枢 + AI 生图工具的参数速查。不教「怎么用 ComfyUI」——教「怎么写出能用的 prompt」。
> **适用工具**：ComfyUI (Flux/SDXL/SD1.5) / ChatGPT Image (GPT-4o) / Midjourney / DALL-E / NanoBanana (Google) / 即梦 (Jimeng)。以 Flux/SDXL 为基准，标注其他工具的差异。
> **宪法约束**：本文件是交叉参考——Art Director 和各场景文档的提示词模板最终都汇聚到这里。

---

## 工具速查

| 工具 | 最佳用途 | Prompt 特点 | 输出分辨率 | 注意 |
|------|---------|------------|-----------|------|
| **Flux (ComfyUI)** | 电影级静帧、概念图 | 自然语言 prompt，对质感和光照理解最好 | 1024-2048px | 对人脸的理解不如 SDXL 精细 |
| **SDXL (ComfyUI)** | 角色设计、风格化图像 | 标签式 prompt + 权重语法 | 1024×1024 | 需要 negative prompt |
| **SD1.5 (ComfyUI)** | 快速出图、低显存 | 标签式 prompt，需要更多引导 | 512×768 | 画质上限低，角色一致性难 |
| **Midjourney** | 创意概念、氛围图 | 自然语言 + 参数（--ar, --style） | 1024-2048px | 可控性低，适合探索方向 |
| **DALL-E 3** | 快速验证、文字渲染 | 自然语言，文字理解最好 | 1024×1024 | 风格化能力弱于 Flux |
| **ChatGPT Image (GPT-4o)** | 文字渲染、多轮编辑、对话式出图 | 自然语言，支持对话迭代修改，文字渲染最强 | 1024×1024 / 1024×1536 | 风格化偏保守；多轮编辑是核心优势 |
| **NanoBanana (Google)** | 轻量快速原型、移动端、低延迟 | 自然语言，轻量快速，适合大批量迭代 | 512-1024px | 画质上限低；速度快，适合探索方向 |
| **即梦 (Jimeng/字节)** | 中文语义生图/生视频、社交媒体素材 | 中文自然语言，对中国元素理解好 | 1024-2048px | 视频生成能力突出；集成抖音生态 |

---

## Prompt 模板

### 通用电影感模板（Flux/SDXL）

```
[主体描述], [环境], [灯光方案], [色调], [构图法], [画幅比例], [画质关键词]

组成要素：
1. 主体：什么 / 什么材质 / 什么状态 / 在做什么
2. 环境：在哪里 / 什么天气 / 什么时间 / 什么氛围
3. 灯光：主光源类型 + 方向 + 色温（详见 DP 的灯光方案模板）
4. 色调：主色 hex 或颜色描述（详见 Art Director 的色调方案）
5. 构图：构图法 + 镜头景别（详见 DP 的镜头词汇表）
6. 画幅：16:9 / 9:16 / 1:1 / 2.39:1
7. 画质：8K, cinematic, photorealistic, film grain, volumetric lighting
```

### 分镜图模板（每个 storyboard panel 一条）

```
[panel 编号]：[场景 slug]
[主体] 在 [环境] 中，[动作]，[灯光] 来自 [方向]，[色调]，[景别]，[构图法]，[画幅比例]，电影级画面

示例：
"Panel 03：s02_confrontation
穿长款风衣的男性角色在巨型混凝土走廊中，侧身站立望向远方，单一橙色顶光从上方洒下产生长阴影，尘橙色+蓝黑色调，全景，三分法（人物在左1/3），2.39:1，电影级画面，volumetric dust particles"
```

### 产品图模板

```
[产品名称/描述]，[材质关键词]，[角度]视角，[灯光]灯光，[背景]，产品摄影，商业广告，[画幅比例]，8K 高清

材质关键词参考（VFX 材质库）：
- 玻璃: glass material, caustics, transparent, refractive, clean edges
- 金属: polished metal, chrome reflection, brushed aluminum, metallic sheen
- 塑料: matte plastic, soft highlights, satin finish, smooth surface
- 陶瓷: ceramic, matte glaze, subtle texture, warm white
```

### 角色设计图模板

```
[角色描述]，[年龄+性别]，[体型]，[发型+发色]，[服装风格]，[姿势]，[灯光]，[背景]，角色设计，概念艺术，[风格]

示例：
"25岁女性赛博朋克黑客，苗条体型，短发不对称染蓝色，穿着机能风黑色夹克+高领内搭，侧身站立查看全息投影手环，蓝色底光+品红色环境光，暗色背景，角色设计，概念艺术，cyberpunk style, character turnaround sheet"
```

---

## 参数速查

### Flux (ComfyUI) 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| **Steps** | 20-28 | 25 步是画质/速度平衡点 |
| **CFG** | 3.5-5.0 | Flux 的 CFG 远低于 SDXL |
| **Resolution** | 1024×576 (16:9) / 1024×1792 (9:16) | Flux 支持非 1:1 原生分辨率 |
| **Sampler** | Euler / DPM++ 2M | Euler 最稳定 |
| **Scheduler** | Simple / Beta | Simple 更快，Beta 细节稍好 |

### SDXL 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| **Steps** | 25-40 | 高步数改善细节 |
| **CFG** | 5-8 | 过高会过饱和/失真 |
| **Resolution** | 1024×1024 (原生) / 896×1152 (9:16) | 非 1:1 需要 Hires fix |
| **Sampler** | DPM++ 2M Karras / Euler A | DPM++ 细节好，Euler A 创意多 |
| **Hires Fix** | 1.5-2x upscale + 15-20 steps | 非 1:1 画幅必须开启 |

### SD1.5 推荐参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| **Steps** | 20-30 | 30 步以上收益递减 |
| **CFG** | 7-9 | SD1.5 需要较高 CFG |
| **Resolution** | 512×768 (竖) / 768×512 (横) | 原生最佳分辨率 |
| **Hires Fix** | 必须开启 | 直接生成高分辨率会多头/多肢 |

---

## 负面提示词策略

### 通用 Negative Prompt（SDXL/SD1.5）

```
ugly, deformed, blurry, low quality, bad anatomy, extra limbs, 
poorly drawn face, disfigured, watermark, text, signature, 
out of frame, cropped, jpeg artifacts, bad proportions,
duplicate, cloned face, extra fingers, mutated hands
```

> Flux 通常不需要 negative prompt（Flux 对负面提示词不敏感）。如果 Flux 出图有问题，调整 CFG 比加负面词更有效。

### 场景专属负面提示词

| 场景 | 追加 Negative |
|------|--------------|
| 棚拍广告 | `cluttered background, harsh shadows, uneven lighting, amateur snapshot` |
| 产品演示 | `blurry product, distorted shape, wrong color, reflection artifacts` |
| LOGO 演绎 | `unreadable text, wrong font, messy background, low contrast` |
| sci-fi | `cartoon, anime, illustration, low poly, video game graphics, unreal engine look` |
| 角色设计 | `asymmetrical face, crossed eyes, bad hands, extra fingers, inconsistent clothing` |

---

## 提示词质量检查

- [ ] 包含 7 要素：主体 + 环境 + 灯光 + 色调 + 构图 + 画幅 + 画质
- [ ] 灯光有明确方向（不是 "good lighting" 而是 "key light from top-left"）
- [ ] 色调有颜色词（不是 "nice colors" 而是 "warm amber tones"）
- [ ] 构图有具体方法（不是 "good composition" 而是 "rule of thirds"）
- [ ] 画质关键词 ≤ 5 个（不要堆砌 "8K, 4K, HD, high quality, ultra detailed, masterpiece"）
- [ ] 负面提示词只针对已知问题（不要泛泛写 "bad, ugly, worst"）
- [ ] 如果是产品图 → 产品名/材质/角度/背景都明确
- [ ] 如果是角色 → 年龄/性别/体型/发型/服装/姿势都描述

---

## Agent 注入 Prompt 段落

```
当你需要生成 AI 图像时：

1. 从对应的场景文档/角色文档中提取 prompt 模板
2. 填充 7 要素（主体+环境+灯光+色调+构图+画幅+画质）
3. 根据目标工具选择参数（Flux: steps=25, CFG=4 / SDXL: steps=30, CFG=6）
4. SDXL/SD1.5 添加通用 negative prompt
5. 调用 image_gen 工具生成
6. 生成后检查是否符合 prompt 描述（不要假设生成成功）
```
