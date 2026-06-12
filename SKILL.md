---
name: muse-video
description: "Use when the user wants to plan, brainstorm, or design a video project — ads, product demos, logo animations, sci-fi shorts, or any creative video. This is a pre-production engine that produces a Creative Package (script + storyboard + art direction + prompts), NOT a video renderer. For actual video rendering and composition, route to HyperFrames; for AI image/video generation, route to ComfyUI."
version: 0.6.0
author: Hermes Agent + 钱多多
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [video, creative, pre-production, storyboard, script, art-direction, filmmaking]
    related_skills: [hyperframes, comfyui, infographic-carousel]
---

# Muse Video — AI 视频前期策划引擎

> **定位**：产出 Creative Package（剧本 + 分镜 + 美术 + 提示词），由用户导入下游工具制作。
> **不做**：实际视频渲染（→ HyperFrames）、AI 生图/生视频（→ ComfyUI / image_gen）。
> **宪法**：加载 `CONSTITUTION.md` 了解 5 条设计原则 + 数据流 + 禁止模式。

## 路由决策树

```
用户请求视频相关创作
        │
        ├─ "我做了一个视频，帮我修改/加特效/加字幕" → 这不是本 Skill，路由到 HyperFrames
        ├─ "帮我生成一个视频/图片" → 这不是本 Skill，路由到 ComfyUI / image_gen
        │
        └─ "帮我策划/设计/构思一个视频" → ✅ 激活本 Skill
                │
                ├─ 用户提到具体案例/风格？
                │   → 加载 references/cases/INDEX.md
                │   → 匹配案例 → 加载 references/cases/<id>.md
                │
                ├─ 检测场景类型（关键词匹配）：
                │   studio-ad:      "广告/棚拍/TVC/品牌片"
                │   logo-animation: "LOGO/片头/品牌演绎/动画"
                │   product-demo:   "产品/演示/功能介绍/开箱"
                │   sci-fi:         "科幻/Cyberpunk/未来/赛博"
                │   custom:         无匹配 → 用通用流程
                │
                └─ 检测复杂度：
                    1-2 场景 / 无角色 / 用户催快 → fast-track 管线
                    多场景 / 有角色 / 需要深度策划 → default 管线
```

## 管线激活

### Default Pipeline（7 阶段，完整创作）
1. **需求沟通**（Director）→ 确认比例/用途/场景/约束
2. **内容梳理**（Writer + Director）→ 故事、场景、叙事结构
3. **视觉开发**（Art Director + Director）→ 色调、风格、人物设定，调用 image_gen 生成参考图
4. **脚本**（Writer → DP → Director review）→ 台词、镜头语言、动作、时长
5. **声音方向**（Sound Designer）→ 配乐风格、音效、旁白基调
6. **分镜**（Storyboard Assembly）→ 6/9 宫格分镜 + 对应提示词，调用 image_gen
7. **组装+调优**（Director）→ 运行 `scripts/prompt_assembler.py` 产出 Creative Pack

**每阶段**：角色产出 → Director 审核。通过 → 下一阶段。修改 ≤2 轮。拒绝 → 重启该阶段。
**角色文件**：按需加载 `references/roles/<name>.md`，不一次全载入。

### Fast-Track Pipeline（简化版）
合并阶段 2+3+4 → 一稿过，跳过 Director 多轮审核。仅适用于简单需求。

## 案例引用

当案例匹配时，Agent 加载案例文件，将对应段落注入角色 prompt：
- `BR2049` → sci-fi/赛博朋克的镜头+色彩+特效技法
- 更多案例见 `references/cases/INDEX.md` 交叉索引表
- 发现新案例 → 按 `references/cases/_TEMPLATE.md` 拆解 + 更新 INDEX.md 全表

## 导出格式

`scripts/export_html.py` → 文学剧本 HTML（Courier 标准格式）/ 分镜展示 HTML（卡片网格）
`scripts/export_xlsx.py` → 分镜技术表 Excel（镜号/景别/运动/灯光/VFX）
用户说"导出剧本/分镜表" → 自动触发对应脚本。

## 下游对接

产出 Creative Package JSON 后，提示用户可对接：
- `[HyperFrames]` → HTML 视频合成（场景、动画、字幕、配乐）
- `[ComfyUI]` → AI 图片/视频生成（分镜图、动态片段）
- Kling / Runway / Pika → 第三方 AI 视频工具
- 手动制作 → 用导出的 HTML/Excel 作为拍摄参考

## 禁止事项

- ❌ 跳过 Director 审核（每个阶段结束必须审核）
- ❌ 3 轮以上修改（超过 2 轮 → 接受带备注或重启阶段）
- ❌ 在 SKILL.md 中放详细技法（→ references/cases/）
- ❌ 在不加载案例的情况下引用案例技法
- ❌ 承诺角色一致性（诚实告知这是 AI 的限制）

## 产出验证

- [ ] Project State JSON 完整（所有 phase 的 `_meta.director_approved` = true）
- [ ] 每个角色产出有 `_meta` 追溯（role + revision）
- [ ] 案例引用已加载（如果用户提到了风格参考）
- [ ] Director 全程参与审核，无跳过阶段
- [ ] 导出格式已按用户需求生成
