**简体中文** ｜ [English](README.en.md)

# Muse Video — 视频创作虚拟剧组引擎

产出一个视频开拍前需要的全部策划案：剧本、分镜、美术方向、提示词，并编译成下游视频模型可直接执行的调用指令。38 个标杆案例技法库 × 六角色协作，做你的「虚拟剧组」。

> Virtual film-crew engine for video creation — idea → script, storyboard, art direction, prompts → model-ready call instructions. 38-case technique library × six-role crew × end-to-end review gates.
> 状态：开发中 ｜ 通用 Agent Skills 格式（适配任何支持 skills 的 AI Agent）

---

## 解决什么问题

| 痛点 | Muse Video 怎么做 |
|------|------------------|
| 有创意但不会写专业分镜脚本 | 好莱坞格式剧本 + 6/9 宫格分镜 + 技术表——文学剧本 / 分镜卡片 / 编译预览 / 技术表四种成品一键导出 |
| 想做某个风格但说不清楚 | 38 个标杆案例技法库——说「参考 Apple 1984」比描述「反乌托邦蓝灰色调」快 10 倍 |
| 策划来回改、改完还是散 | 8+1 阶段管线，每阶段 Director 审核 ≤2 轮，产出全程 `_meta` 可追溯 |
| 策划案再好，下游模型用不起来 | Phase 7.5 模型编译：六段式 prompt + 多模态参考图映射 + 调用命令 + 成本估算（已适配 Seedance 2.0）|
| 参考图满天飞、对不上号 | 参考图引用链 + 资产化（人物 / 产品主体 / 关键分镜 / 关键道具）——按资产 ID 全链引用，不转述 |

---

## 怎么用

在任何支持 Agent Skills 的 AI Agent 中，像这样说话：

```
帮我策划一个产品广告，风格参考 Apple Don't Blink
```

```
帮我构思科幻短片的故事板，想要银翼杀手那种巨物美学
```

Agent 会自动匹配案例技法 → 注入角色 prompt → 走管线 → 导出 Creative Package。

---

## 产出长什么样

| 组成 | 内容 |
|------|------|
| 剧本 | 场景 / 对白 / 动作 / 镜头语言（文学剧本 HTML 导出，Courier 标准格式）|
| 分镜 | 6/9 宫格分镜卡片：描述 / 机位 / 灯光 / 美术 / VFX / 生图 prompt |
| 美术方向 | 色调板（hex + 成因字段）+ 风格参考 + 场景构成 + 角色设定 |
| 提示词 | 每格分镜的 image_prompt、全片 video prompt 素材 |
| 字幕层 | 文案（中 / 英 / 双语）× 字体族 × 位置——与画面 prompt 解耦，编译为烧录 spec |
| 音频路线 | 配乐 / 配音 / 音效的路线选择 + 生成 brief（解耦，不代生成）|
| 模型调用指令 | Phase 7.5 编译：六段式 prompt + 多模态引用 + arkcli 命令 + 成本估算 + 下游工具配置（ComfyUI / HyperFrames / Kling）|

完整成品见 [`assets/examples/`](assets/examples/)——科幻短片与棚拍广告两个全流程示例（含 HTML / Excel 导出）。

---

## 工作流

```
用户描述想法
    │
    ├─ 路由决策树 → 判场景类型（4 种模板 + 自定义）与复杂度
    ├─ 加载匹配案例技法 → 注入对应角色 prompt
    ├─ 8+1 阶段管线推进（角色产出 → Director 审核 → 下一阶段）
    └─ 导出 Creative Package → 下游工具对接
```

- **六角色虚拟剧组**：Director（导演）/ Writer（编剧）/ DP（摄影）/ Art Director（美术）/ VFX（特效）/ Sound Designer（声音）——每角色独立文档，按需加载
- **两条管线**：Default（8 阶段 + 1 预留，完整创作）/ Fast-Track（合并阶段，简单需求一稿过）
- **四种场景模板**：棚拍广告 / 产品演示 / LOGO 演绎 / 科幻设定——可扩展自定义

**不做**：视频渲染/合成、AI 生图/生视频——本 Skill 产出策划案与调用指令，实际生成交给下游工具（HyperFrames / ComfyUI / Kling / 火山引擎 等）。

---

## 门禁 / 确认环节

| 触发点 | 你的动作 | 默认 |
|--------|---------|------|
| Phase 3.5 风格定样 | 看图确认色调 / 风格方向 | image_gen 不可用时跳过 |
| Phase 3.5 资产生成门禁 | 决定关键资产（人物 / 产品）是否生成、生成范围 | 先出候选清单再询问 |
| Phase 6 分镜 | 决定是否调用 image_gen 生成分镜图 | 显式询问 |
| Phase 7 HTML 分镜 | **唯一最终确认关卡**：确认即锁定（四选项 + 默认）| 逐项核对后确认 |
| Phase 7.5 编译预览 | 二次确认模型调用指令（含音频模型引导）| 导出编译预览 HTML 核对 |

---

## 案例库

38 个标杆案例，按角色维度建六组技法交叉索引（叙事 / 镜头 / 色彩美术 / 特效 / 声音 / 创意广告）：

| 类型 | 数量 | 代表 |
|------|------|------|
| 商业广告 | 25 | Apple 1984 / Guinness Surfer / Honda Cog / Sony Balls |
| 电影 | 4 | 银翼杀手 2049 / 花样年华 / 流浪地球 / 环太平洋 |
| LOGO 演绎 | 3 | NIO 十周年 / Apple Event 合集 / Pixar Luxo Jr. |
| 短片 | 2 | ACHROMA / Cosmos Laundromat |
| 其他 | 4 | Piper（动画）/ Koyaanisqatsi（纪录片）/ Machine Hallucination（实验）/ The One Moment（MV）|

> 完整注册表 + 技法交叉索引 → [`references/cases/INDEX.md`](references/cases/INDEX.md)

---

## 目录结构

```
muse-video-skill/
├── SKILL.md                    ← 路由中枢（入口）
├── CONSTITUTION.md             ← 设计宪法（5 条原则 + 数据流 + 禁止模式）
├── README.md / README.en.md    ← 项目页（中文 / English）
├── LICENSE                     ← MIT
├── .github/workflows/          ← CI 质量门（语法 / 索引 / 契约）
├── references/                 ← 领域知识（按需加载）
│   ├── cases/                  ← 38 标杆案例 + 索引 + 案例帧素材
│   ├── roles/                  ← 6 角色文档
│   ├── scenes/                 ← 4 场景模板 + 新场景模板
│   ├── pipelines/              ← 2 管线（default / fast-track）
│   └── media/ · meta/ · *.md   ← 生图知识 / 验证清单 / 路由与编译文档
├── scripts/                    ← 9 个确定性脚本（索引 / 校验 / 组装 / 导出）
├── assets/
│   ├── schemas/                ← Project State JSON Schema（角色间唯一接口）
│   ├── templates/              ← 剧本 / 分镜 / 导出模板（4 种导出格式）
│   └── examples/               ← 2 个全流程示例（含成品导出）
└── metadata/                   ← fields.yaml / phase_gates.yaml / CHANGELOG
```

---

## 安装

本 Skill 采用通用 Agent Skills 格式（`SKILL.md`），任何支持 skills 的 AI Agent 均可装载。

**方式一 · 克隆（总是最新）：**

```bash
git clone https://github.com/LuoJiangYong/muse-video-skill.git
# 放入所用 Agent 的 skills 目录，例如：
#   Claude Code  → ~/.claude/skills/muse-video/
#   Hermes Agent → ~/.hermes/skills/creative/muse-video/
```

**方式二 · Hermes Skills Hub：**

```bash
hermes skills install muse-video-skill
```

---

## 开发自检

```bash
python scripts/build_index.py --check --deps   # 索引完整性 + 死链检查（期望 0 errors）
python scripts/inventory.py --json             # 文件级盘点（按角色分类）
python scripts/validate_state.py --input <project-state.json> --phase 7   # 阶段门禁校验
python -m py_compile scripts/*.py              # 全脚本可编译
```

---

## 来源与致谢

案例库收录的影视作品与广告均标注作品与创作者，技法拆解仅用于学习研究；商标与影像版权归各自权利人所有。

---

## 许可证

[MIT](LICENSE) © 2026 Jiang Yong Luo

---

## 版本

[v0.36.2](metadata/CHANGELOG.md) — 中英双语项目页 + MIT LICENSE；38 案例技法库 × 六角色 × 8+1 阶段管线，参考图资产化 / 字幕层 / 音频路线 / 模型编译（Seedance 2.0）。
