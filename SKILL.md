---
name: muse-video
description: "When the user asks to 策划/构思/设计/写脚本/画分镜 for a video project — e.g. '帮我策划一个广告创意' '这个产品演示视频怎么拍' '帮我写科幻短片的分镜脚本' '给我这个品牌TVC的美术方向'。Not for actual video rendering/compositing or AI image/video generation."
version: 0.30.3
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
> **不做**：实际视频渲染、AI 生图/生视频。如有 HyperFrames/ComfyUI 等下游工具可对接；如无，产出策划案供手动制作。
> **宪法**：加载 `CONSTITUTION.md` 了解 5 条设计原则 + 数据流 + 禁止模式。

## 路由决策树

```
用户请求视频相关创作
        │
        ├─ "我做了一个视频，帮我修改/加特效/加字幕" → 这不是本 Skill。如已配置 HyperFrames 等视频合成工具可路由；否则告知用户本 Skill 产出分镜脚本供参考。
        ├─ "帮我生成一个视频/图片" → 这不是本 Skill。如已配置 ComfyUI/image_gen 可在视觉阶段按需调用；否则用文字描述替代。
        │
        └─ "帮我策划/设计/构思一个视频" → ✅ 激活本 Skill
                │
                ├─ 用户提供参考视频（本地文件 / 可下载 URL）？
                │   → 触发 Phase 1 拆解子流程（见 default.md §Phase 1 步骤 2.5）
                │   → 逐镜头拆解为拉片表 → 用户校准 → 聚合为技法摘要
                │   → 技法摘要写入 Project State，后续角色直接消费
                │   → 下载失败：告警 + 问替代方案，不降级不猜测
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

### Default Pipeline（8 阶段 + 1 预留，完整创作）
1. **需求沟通**（Director）→ 确认比例/用途/场景/约束
2. **内容梳理**（Writer + Director）→ 故事、场景、叙事结构
3. **视觉开发**（Art Director + Director）→ 色调、风格、场景搭建、人物设定。含反主观化规则：情绪标签映射 visual_cause 字段（见 `references/anti-subjective-rule.md`）
3.5 **风格定样**（条件性）→ image_gen 生成场景 moodboard + 角色概念图 → 用户看图确认 → 锁定风格方向。不可用时跳过
4. **脚本**（Writer → DP → Director review）→ 台词、镜头语言、动作、时长
5. **声音方向**（Sound Designer）→ 配乐风格、音效、旁白基调
6. **分镜**（Storyboard Assembly）→ 6/9 宫格分镜 + 显式询问用户是否调用 image_gen 生成分镜图
7. **组装+调优**（Director）→ `prompt_assembler.py` 产出 Creative Pack → HTML storyboard 确认门禁（四选项 + 默认，唯一最终确认关卡）。参考图直接进入下游编译，确认即锁定
7.5 **模型编译**（Model Compiler）→ Creative Package 编译为目标模型调用指令（六段式 prompt + 多模态引用 + arkcli 命令 + 成本估算）。仅 Seedance 2.0
8 **下游工具引导**（预留）→ 工具选择与费用预估（不执行，建设时遵循「机场指示牌」原则）

**每阶段**：角色产出 → Director 审核。通过 → 下一阶段。修改 ≤2 轮。拒绝 → 重启该阶段。
**角色文件**：按需加载 `references/roles/<name>.md`，不一次全载入。

### Fast-Track Pipeline（简化版）
合并阶段 2+3+4 → 一稿过，跳过 Director 多轮审核。仅适用于简单需求。

## 案例引用

> 案例匹配 → 加载 `references/cases/INDEX.md`。新增案例 → `references/cases/_TEMPLATE.md`。索引由 `scripts/build_index.py` 自动生成，禁止手动编辑 INDEX.md。

## 导出格式

`scripts/export_html.py` → 文学剧本 HTML（Courier 标准格式）/ 分镜展示 HTML（卡片网格）
`scripts/export_xlsx.py` → 分镜技术表 Excel（镜号/景别/运动/灯光/VFX）
用户说"导出剧本/分镜表" → 自动触发对应脚本。

## 下游对接

> 产出 Creative Package 后，按 `references/downstream-integration.md` 对接下游工具（HyperFrames / ComfyUI / Kling / 火山引擎 / etc.）。

## INDEX.md 自动化

> 见 `references/index-automation.md`。`build_index.py --check` 校验，`--write` 重新生成。禁止手动编辑。

## 产出验证

> 见 `references/meta/verification-checklist.md`。
