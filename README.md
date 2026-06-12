# Muse Video — AI 视频前期策划引擎

产出一个视频在开拍前需要的全部策划案：剧本、分镜、美术方向、提示词。用 16 个标杆案例的风格和技法做你的"虚拟剧组"。

---

## 解决什么问题

| 痛点 | Muse Video 怎么做 |
|------|------------------|
| 有创意但不会写专业分镜脚本 | 输出标准好莱坞格式剧本 + 6/9 宫格分镜 + 技术表 |
| 想做某个风格但说不清楚 | 引用 16 个标杆案例——说"参考 Apple 1984"比描述"反乌托邦蓝灰色调"快 10 倍 |
| 策划来回改、改完还是散 | 7 阶段管线，每阶段 Director 审核 ≤2 轮，产出有 `_meta` 追溯 |

---

## 特点

- **16 个标杆案例库** — 电影×4 / 广告×11 / 短片×1，技法交叉索引 10 张表（叙事、镜头、色彩、特效、声音、创意策略…）
- **6 角色协作管线** — Writer / DP / Art Director / VFX / Sound Designer / Director，每角色有独立文档，按阶段加载
- **双模工作流** — 完整 7 阶段（深度项目） / Fast-Track（简单需求合并阶段，一稿过）
- **多格式导出** — 文学剧本 HTML（Courier 标准格式）、分镜展示 HTML（卡片网格）、技术表 Excel

---

## 怎么用

在已安装本 Skill 的 AI Agent 中，像这样说话：

```
帮我策划一个产品广告，风格参考 Apple Don't Blink
```

```
帮我构思科幻短片的故事板，想要银翼杀手那种巨物美学
```

Agent 会自动匹配案例技法 → 注入角色 prompt → 走管线 → 导出。

---

## 工作流

```
用户描述想法
    │
    ├─ 路由决策树 → 判断场景类型 + 复杂度
    ├─ 加载匹配案例技法 → 注入对应角色 prompt
    ├─ 管线推进（角色产出 → Director 审核 → 下一阶段）
    └─ 导出 Creative Package
```

**不做**：视频渲染/合成、AI 生图/生视频。这些是下游工具的工作——如有 HyperFrames/ComfyUI 可对接，没有也不影响策划案产出。

---

## 覆盖场景

| 场景 | 定位 | 一句话 |
|------|------|--------|
| 🎥 **棚拍广告** | 受控环境下的品牌视觉叙事 | 每个像素都是设计出来的 |
| 📱 **产品演示** | 产品是唯一明星，叙事服务功能展示 | 每个镜头回答「能做什么、为什么需要」 |
| ✨ **LOGO 演绎** | 3-10 秒纯粹视觉冲击 | 让标志被记住 |
| 🚀 **科幻设定** | 构建不存在的世界并让观众相信 | 核心不是「多炫」而是「规则感」 |
| 🎨 **艺术短片（自定义）** | 无固定范式，风格驱动 | 场景文档 + 案例参考灵活组合 |

> 每个场景有独立文档（`references/scenes/`），定义角色优先级、叙事结构、灯光/美术模板。

---

## 案例库

| 类型 | 案例 | 年份 | 导演 | 一句话 |
|------|------|------|------|--------|
| 🎬 电影 | 银翼杀手 2049 | 2017 | Denis Villeneuve | 巨物美学 + 色彩叙事的 cyberpunk 标杆 |
| 🎬 电影 | 花样年华 | 2000 | 王家卫 | 留白叙事 + 框架构图 + 慢快门步印 |
| 🎬 电影 | 流浪地球 | 2019 | 郭帆 | 巨物尺度 + 集体英雄主义 + 五域色调体系 |
| 🎬 电影 | 环太平洋 | 2013 | Guillermo del Toro | 重量感运动 + 霓虹雨夜 + 机械物理模拟 |
| 📺 广告 | Apple 1984 | 1984 | Ridley Scott | 品牌宣言 × 超级碗一次性播出——定义 Apple 40 年 |
| 📺 广告 | Guinness Surfer | 1999 | Jonathan Glazer | 纯隐喻巅峰——全片无产品，被票选为「史上最佳广告」 |
| 📺 广告 | Honda Cog | 2003 | A. Bardou-Jacquet | 鲁布·戈德堡机械 × 606 次实拍零 CGI |
| 📺 广告 | Sony Balls | 2005 | Nicolai Fuglsig | 25 万颗弹力球——纯视觉奇观 × 零 CGI |
| 📺 广告 | IKEA Lamp | 2003 | Spike Jonze | 反广告的广告——让你为一盏灯哭，再笑你哭了 |
| 🎞 短片 | Cosmos Laundromat | 2015 | Blender Foundation | 开源动画的自然光革命 |

> 完整 16 案例 + 交叉索引 → [`references/cases/INDEX.md`](references/cases/INDEX.md)

---

## 目录结构

```
muse-video-skill/
├── SKILL.md                          ← 路由中枢（入口）
├── CONSTITUTION.md                   ← 5 条设计宪法
├── references/
│   ├── cases/                        ← 16 案例 + INDEX + 模板
│   ├── roles/                        ← 6 角色文档
│   ├── scenes/                       ← 4 场景类型文档
│   ├── pipelines/                    ← 2 管线定义
│   └── media/                        ← 生图指南
├── scripts/                          ← 导出脚本
│   ├── export_html.py
│   ├── export_xlsx.py
│   └── prompt_assembler.py
├── assets/
│   ├── schemas/                      ← JSON Schema
│   ├── templates/                    ← 剧本/分镜/导出模板
│   └── examples/                     ← 2 个完整示例
└── metadata/
    ├── registry.yaml                 ← 文件级注册表
    ├── CHANGELOG.md                  ← 版本变更日志
    └── fields.yaml                   ← 字段级元数据
```

---

## 安装

本 Skill 在 Hermes Agent 中通过 `hermes skills install` 安装，或直接克隆到 skills 目录：

```bash
git clone https://github.com/LuoJiangYong/muse-video-skill.git
```

---

## 版本

[v0.8.1](metadata/CHANGELOG.md) — Phase 0-7 全部完成，54 文件，16 案例。
