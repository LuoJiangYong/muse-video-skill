# 案例拉片层 — 实施方案

> 创建于 2026-06-18，v0.27.0 讨论结论。在新会话实施时引用此文件。

## 定位

案例文件 `§拉片附录`，仅用户指定的高质量案例。逐镜头技术参数 + 分镜图，供精确复刻时角色按需消费。

## 拉片附录结构

```
§拉片附录（→ 精确复刻）

├─ 镜头序列总览表（人工索引，按场景分组子表）
│
├─ §叙事节奏（→ Writer）
├─ §镜头语言序列（→ DP）
├─ §色调+场景搭建序列（→ Art Director）
├─ §角色设计序列（→ Writer + Art Director + DP + Sound）
├─ §音效序列（→ Sound）
├─ §特效序列（→ VFX）
└─ §分镜精选帧（→ Storyboard / image_gen reference）
```

## 总览表格式（按场景分组）

```markdown
### 场景1: 名称（时间码起止）
| # | 时间码 | 时长 | 景别 | 构图 | 运镜 | 色调+场景 | 角色 | 音效 | 叙事功能 | 特效 | 分镜图 |
|---|--------|------|------|------|------|----------|------|------|----------|------|--------|

### 场景2: ...
```

列名与拆解管线（default.md 步骤 2.5b）字段一一对应：时间码/景别/构图/运镜/色调+场景/音效/叙事功能/角色/特效。拉片独有：时长（派生值）、分镜图（帧）。

## 角色分段消费映射

| 拉片分段 | 消费角色 | 管线阶段 |
|------|:---:|:---:|
| 叙事节奏 | Writer | P2/P4 |
| 镜头语言序列 | DP | P4 |
| 色调+场景搭建序列 | Art Director | P3 |
| 角色设计序列 | Writer+AD+DP+Sound | P2-P5 |
| 音效序列 | Sound | P5 |
| 特效序列 | VFX | P6 |
| 分镜精选帧 | Storyboard(全量)+DP/AD(按需) | P3/P4/P6 |

## 分镜图

- 存储：`references/cases/assets/<CASE-ID>/`
- 数量：按视频实际，覆盖全部核心场景和关键技法
- 案例文件用相对路径引用
- Storyboard P6 作 image_gen 的 reference_image

## 约束

- 拉片层 vs 技法层：不互抄。拉片=证据，技法=结论
- 拉片层 vs 拆解管线：不交叉。拉片在案例库，拆解当场消费
- build_index.py 不索引拉片层（只索引 YAML frontmatter）
- 已有 38 案例不全量回填（用户挑选，视频源可达的才补）
- 触发：用户建案例时主动指定「高质量，做深层录入」

## 待改动文件

1. 新建 `references/pull-sheet-layer-design.md`（全量设计文档 → 即本文件）
2. 更新 `_TEMPLATE.md`：技法层末尾加 §拉片附录 骨架（标注「仅高质量案例填写」）
3. 新建 `references/cases/assets/` 目录
4. 更新 `case-study-workflow.md`：加「深度录入」流程
5. 更新 `SKILL.md`：案例引用段加一行

## 相关上下文

- 拆解管线已实施：`default.md` Phase 1 步骤 2.5，6 维度聚合（narrative/cinematography/color+scene/character/sound/vfx）
- v0.27.0 角色消费全链路已闭合，Art Director 职责含 scene_composition + character_design
- 角色文档设计规范：`references/role-doc-design.md`（三层结构）
- 维护审计清单：`references/skill-maintenance.md`（8 类审计）
- 扩展 Phase 3 审计：`references/extending-phase-3.md`（7 点审计）
