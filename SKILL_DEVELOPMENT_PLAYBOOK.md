# Hermes Skill 开发方法论 — 通用框架和可复用模式

> 提取自 Muse Video Skill 开发全流程。适用于任何复杂 Skill（多文件、多角色、有 Schema、需长期演进）的开发。
>
> **核心理念**：架构先行 → 元数据同步 → 分 Phase 隔离 → 案例驱动演进。

---

## 一、Skill 复杂度分级

先判断你的 Skill 属于哪个级别：

| 级别 | 特征 | 推荐方法 | 例子 |
|------|------|---------|------|
| **L1 单一** | 1 个 SKILL.md，无引用文件 | 写就完了 | "用 gh CLI 创建 Issue" |
| **L2 模块** | SKILL.md + 几个 references/ | 架构先行（轻量） | "ComfyUI 安装和生图" |
| **L3 系统** | 多角色/多 Agent、有共享 Schema、需要长期演进 | **完整方法论** | Muse Video Skill |

**本文件面向 L3 级别**。L1/L2 可以复用其中的部分模式。

---

## 二、架构宪法模板

### 2.1 5 条设计原则（通用版）

每个项目替换括号内的领域词：

```markdown
### 1. 高内聚 HIGH COHESION — One file, one job.
- 【你的领域】的知识只存在于一个文件中，绝不重复。
- 【领域模块 A】和【领域模块 B】互不包含对方内容。

### 2. 低耦合 LOW COUPLING — 改一个不动其他。
- 新增【领域模块 C】不需要修改任何已有文件。
- 【共享 Schema】是模块间的唯一接口。模块间不直接调用。

### 3. 可扩展 EXTENSIBLE — 新能力 = 新文件 + 一行注册。
- 新增【能力 X】= 新增文件 + 在路由表中加一行。
- 零代码改动，零已有文件修改。

### 4. 易维护 MAINTAINABLE — 可追溯性好过聪明。
- 每个产出来源可追溯。
- 元数据回答"改 X 会影响什么"而不用读代码。

### 5. 高效简洁 LEAN — <3 个消费者就不抽象。
- <3 个地方用同一个模式 → 复制，不提取。
- Markdown 优先，不加框架和配置层，除非真实问题需要。
```

### 2.2 目录布局模板

```
<skill-name>/
├── CONSTITUTION.md              ← 设计宪法（本文件格式）
├── SKILL.md                     ← 路由中枢（≤3500 chars 正文）
│
├── references/                  ← 辐射层：领域知识，按需加载
│   ├── <domain-a>/              ← 按领域分目录
│   ├── <domain-b>/
│   └── cases/                   ← （可选）案例库
│       ├── INDEX.md             ← 多维交叉索引
│       ├── _TEMPLATE.md         ← 标准化模板
│       └── <case-id>.md         ← 单个案例
│
├── scripts/                     ← 确定性逻辑（Agent 调用，不重写）
│   └── <tool>.py
│
├── assets/                      ← 模板、Schema、示例
│   ├── schemas/
│   │   └── <shared-state>.json  ← 共享数据契约
│   ├── templates/
│   └── examples/
│
├── metadata/                    ← 元数据维护体系
│   ├── registry.yaml            ← 文件级注册表
│   ├── fields.yaml              ← 字段级元数据
│   ├── dependencies.yaml        ← 上下游依赖图
│   └── CHANGELOG.md             ← 版本变更日志
│
└── .gitignore
```

### 2.3 关键决策：SKILL.md 多薄才算薄？

| 放 SKILL.md | 放 references/ |
|-------------|----------------|
| 路由决策树（if X then load Y） | 领域知识正文 |
| 阶段/角色激活清单（名称 + 何时触发） | 角色的详细技法、模板、Prompt |
| 禁止事项清单 | 案例拆解全文 |
| 管线流程（步骤名 + 顺序） | 每个步骤的具体操作指南 |
| 下游对接提示 | 工具使用详细文档 |

**判断标准**：如果一段内容 Agent 只在特定条件触发时才需要 → 放 references/。如果每一次激活 Skill 都需要 → 放 SKILL.md。

---

## 三、元数据维护体系模板

### 3.1 registry.yaml 模板

```yaml
# File Registry

files:
  - path: <relative-path>
    role: <constitution|routing|domain-doc|case|pipeline|schema|script|template|example|metadata>
    phase: <0|1|2|3|4>
    status: <not_started|draft|complete|needs_update>
    dependencies: [<list of file paths>]
    dependents: [<list of file paths>]
    owner: <owner-tag>
    description: "<one-line>"

# --- 统计 ---
# Total files: N
# Phase 0 (complete): N0
# Phase 1 (complete): N1
# ...
```

### 3.2 fields.yaml 模板

```yaml
# Field Metadata

fields:
  - path: <json-path>
    type: <string|integer|array|object|enum>
    default: <value>
    description: "<one-line>"
    affected_roles: [<list>]
    affected_phases: [<list>]
    version_added: "<semver>"
    breaking_change: <true|false>
```

### 3.3 dependencies.yaml 模板

```yaml
# Dependency Graph

dependencies:
  - upstream: <file-path>
    downstream: [<list of file paths>]
    impact: "<BREAKING|HIGH|MEDIUM|LOW> — <one-line reason>"

# --- 影响等级速查 ---
# BREAKING: 必须全量 review + 可能需要迁移
# HIGH: 需要重跑测试 + review 下游文件
# MEDIUM: 需要 review 下游文件
# LOW: 通常只影响自身
```

### 3.4 元数据更新 SOP

```
每次 git commit 涉及实质改动时：
  1. 文件增删改 → 更新 registry.yaml
  2. Schema 字段增删改 → 更新 fields.yaml
  3. 依赖关系变化 → 更新 dependencies.yaml
  4. 版本发布 → 更新 CHANGELOG.md
```

---

## 四、案例库索引模式

> 适用场景：Skill 需要积累参考案例/模板/最佳实践，且需要按多维度快速检索。

### 4.1 INDEX.md 结构

```markdown
# 案例索引

## 一、主注册表（每个案例一行）
| ID | 名称 | 类型 | 维度A | 维度B | 标签 |

## 二、标签/技法 → 案例 Mapping（倒排索引）
| 技法 | 案例 ID |

## 三、维度A → 案例 Mapping
| 维度值 | 相关案例 |

## 四、维度B → 案例 Mapping
| 维度值 | 相关案例 |

## 五、更新工作流 (SOP)
```

### 4.2 关键设计决策

- **INDEX.md 是单文件**：Agent 一次读取即可定位所有案例，不需遍历。
- **倒排索引（技法→案例）** 是必要的：Agent 不需要知道案例名，只需要匹配技法。
- **每次添加案例 = 更新 N 张表**：Agent 自检清单防止不一致。

---

## 五、SKILL.md 路由中枢模式

### 5.1 必须包含的元素

```markdown
## 路由决策树
（ASCII 流程图：用户意图 → 条件分支 → 资源加载）

## 管线/流程激活
（阶段列表：名称 + 触发条件 + 角色/资源激活清单）

## 下游对接
（产出后可以对接哪些其他 Skill 或工具）

## 禁止事项
（硬性规则，Agent 必须遵守的约束）

## 产出验证
（自检清单：完成任务后 Agent 自我验证）
```

### 5.2 字符预算分配

| 部分 | 占比 | 说明 |
|------|------|------|
| 路由决策树 | 35% | 这是 SKILL.md 存在的核心理由 |
| 管线激活 | 25% | 阶段名 + 触发条件 + 资源清单 |
| 禁止事项 | 15% | 用 ❌ 前缀，短句 |
| 下游对接 | 10% | 一行一工具 |
| 产出验证 | 10% | 3-5 条自检 |
| 其他（概述/用法） | 5% | 越少越好 |

---

## 六、Phase 分阶段开发 SOP

### 6.1 为什么分 Phase

复杂 Skill 在一个 session 中开发会导致上下文衰减——Phase 3 时 Agent 已经忘了 Phase 1 的设计细节，质量逐 Phase 下降。

### 6.2 Phase 定义

| Phase | 产出 | 文件数（典型） | 独立 Session |
|-------|------|--------------|-------------|
| **0** | CONSTITUTION.md + Schema + .gitignore | 3-5 | ✅ |
| **1** | SKILL.md + 案例库骨架 | 3-5 | ✅ |
| **2** | references/ 全部领域文档 | 10-20 | ✅ |
| **3** | scripts/ + assets/ 全部 | 10-15 | ✅ |
| **4** | 完整示例 + 验证 + 安装 | 3-5 | ✅ |

### 6.3 Session 切换协议

```
1. 当前 session 完成一个 Phase → git commit + push
2. 更新 metadata/registry.yaml（标记当前 Phase 文件为 complete）
3. 产出下一 Phase 的启动提示词（包含：当前状态、待办清单、关键约束）
4. /new → /skill <name> → 粘贴提示词
```

### 6.4 启动提示词模板

```markdown
你是 Hermes Agent。继续开发 <skill-name> Skill 的 Phase <N>。

## 项目状态
- 仓库：<repo-url>
- 本地路径：<absolute-path>
- 已完成：Phase 0 (CONSTITUTION + Schema), Phase 1 (SKILL.md + 案例库)
- 当前 Phase：<N> — <phase-description>
- 之后：Phase <N+1> (<description>), Phase <N+2> (<description>)

## 当前 Phase 待办

创建以下文件（按优先级排序）：

### 第一批：<category>（<N> 个文件）
1. `<path>` — <description>
2. `<path>` — <description>
...

### 第二批：<category>（<N> 个文件）
...

## 关键约束
- 先读 CONSTITUTION.md 了解设计原则和禁止模式
- 用 metadata/registry.yaml 查已有文件的状态和依赖
- 新增/修改文件时同步更新 metadata/registry.yaml
- 每完成一批文件 → git commit + push
- 所有内容用中文（用户偏好）
- 角色/领域文件格式参考 references/cases/_TEMPLATE.md 的结构

## 参考
- 共享 Schema：assets/schemas/<name>.json
- 已有案例模板：references/cases/_TEMPLATE.md
- 相似文件示例：<path-to-existing-similar-file>
```

---

## 七、需求评估框架

> 在动手写代码之前，从「国际顶尖导演/领域专家」角度审视 Skill 定位。

### 7.1 评估维度

| 维度 | 问自己 | Muse Video 的答案 |
|------|--------|------------------|
| **战略定位** | 这个 Skill 在 Hermes 工具链中填补了什么空白？ | 前期策划（HyperFrames=后期, ComfyUI=生成） |
| **核心产出** | 用户最终拿到什么？不是什么？ | Creative Package JSON，不是视频文件 |
| **边界清晰度** | 什么归我管？什么交给别的 Skill？ | 策划归我，渲染/生成归别人 |
| **技术可行性** | 最难的部分是什么？有什么硬限制？ | 角色一致性是 AI 的硬限制，不能承诺 |
| **复杂度风险** | 什么会让这个项目失控？如何防范？ | 多角色无限循环 → 宪法规定 max 2 轮 |
| **扩展路径** | 未来最容易扩展的方向是什么？ | 案例库和场景类型，加文件不加代码 |
| **用户摩擦** | 用户最可能在哪一步放弃？ | HTML 画布 → 降级为 Markdown 看板 |

### 7.2 评估输出格式

```markdown
## 战略定位
（一段话：是什么、不是为什么、填补了什么空白）

## 与现有工具的关系
| 阶段 | 现有工具 | 定位 |
|------|---------|------|
| 阶段A | 工具X | ... |
| 阶段B | ❌ 空白 | ← 本 Skill |

## 薄弱点和缓解策略
1. **薄弱点**：... → **缓解**：...
2. ...

## 总体评分
| 维度 | 评分 | 说明 |
|------|------|------|
| 定位清晰度 | ⭐⭐⭐⭐⭐ | ... |
```

---

## 八、Git 同步纪律

```
每个开发步骤 → git commit + push
Commit 格式：<type>: <简短描述>
  type: feat | fix | refactor | docs | chore

推荐 commit 时机：
  - 完成一个 Phase
  - 完成一批相关文件（3-5 个）
  - 完成一个重要架构决策并写入宪法
  - 修复一个 bug

不要等到整个 session 结束才提交。
```

---

## 九、通用开发提示词集合

### 9.1 启动新 Skill 项目

```
我要开发一个 Hermes Skill：【一句话描述】。

先进行需求评估，站在【领域专家视角】评估：
1. Skill 的战略定位和核心产出
2. 与现有 Hermes 工具链的关系
3. 薄弱点和缓解策略
4. 总体可行性和风险

不要写代码，只做评估。我确认后再进入架构设定。
```

### 9.2 架构设定

```
批准评估结果。进入架构设定阶段。

要求：
- 最高宪法：高内聚、低耦合、可扩展、易维护、高效简洁
- 架构风格："中心短，辐射厚"（SKILL.md 只放路由，references/ 放重文档）
- 目录结构：CONSTITUTION.md + SKILL.md + references/ + scripts/ + assets/ + metadata/
- 建立三层元数据体系（registry + fields + dependencies）
- 每个步骤 git commit + push

产出：
1. CONSTITUTION.md（5 条原则 + 目录布局 + 数据流 + 禁止模式 + 元数据治理章）
2. 共享 Schema/数据结构
3. .gitignore
```

### 9.3 编写 SKILL.md

```
架构完成。编写 SKILL.md（路由中枢）。

要求：
- ≤3500 chars 正文
- 包含：路由决策树、管线/阶段激活清单、禁止事项、产出验证
- 所有领域知识指向 references/，不内嵌
- Frontmatter 完整（name/description/version/author/license/metadata）
- 建立案例库骨架（INDEX.md + _TEMPLATE.md + 一个完整示例）
```

### 9.4 继续下一个 Phase

```
继续开发 Phase <N>。【粘贴 Phase 启动提示词】
```

---

## 附录：Muse Video Skill 完整文件清单

| 文件 | Phase | 状态 | 用途 |
|------|-------|------|------|
| `CONSTITUTION.md` | 0 | complete | 5 条宪法 + 目录 + 数据流 + 元数据治理 |
| `assets/schemas/project-state.json` | 0 | complete | 50 字段共享 Schema |
| `.gitignore` | 0 | complete | 排除产物/环境 |
| `SKILL.md` | 1 | complete | 路由中枢（3500 chars） |
| `references/cases/INDEX.md` | 1 | complete | 6 表交叉索引 |
| `references/cases/_TEMPLATE.md` | 1 | complete | 案例拆解模板 |
| `references/cases/BR2049.md` | 1 | complete | 银翼杀手 2049 完整拆解 |
| `metadata/registry.yaml` | 1 | complete | 39 文件注册表 |
| `metadata/fields.yaml` | 1 | complete | 50 字段元数据 |
| `metadata/dependencies.yaml` | 1 | complete | 22 对依赖关系 |
| `metadata/CHANGELOG.md` | 1 | complete | v0.1.0 变更日志 |
| `references/roles/*.md` (×6) | 2 | 待开工 | 6 个角色文档 |
| `references/scenes/*.md` (×4) | 2 | 待开工 | 4 个场景文档 |
| `references/pipelines/*.md` (×2) | 2 | 待开工 | 2 个管线文档 |
| `references/media/*.md` (×3) | 2 | 待开工 | 生图指南+一致性+工具矩阵 |
| `scripts/*.py` (×6) | 3 | 待开工 | 格式化+网格+组装+对比+导出 |
| `assets/templates/**` (×6) | 3 | 待开工 | Markdown + HTML + Excel 模板 |
| `assets/examples/**` (×2) | 4 | 待开工 | 完整案例 |

---

*整理日期：2026-06-12 | 来源：Muse Video Skill 开发全流程*
