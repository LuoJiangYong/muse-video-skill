# Changelog — 版本变更日志

> 记录每次修改的动机、内容、影响范围、迁移指南。
> 每次 git commit 涉及实质改动时同步更新此文件。
> 格式：`## [version] — YYYY-MM-DD`

---

## [0.1.0] — 2026-06-12

### 新增

- **CONSTITUTION.md**：5 条设计宪法 + 完整目录布局 + 数据流图 + 禁止模式清单
- **SKILL.md**：路由中枢（≤3500 chars 正文），包含意图检测、场景路由、管线激活、阶段触发
- **assets/schemas/project-state.json**：项目状态 JSON Schema，所有 6 个角色的唯一共享接口。50 个字段，覆盖 project/director_notes/script/visual_dev/cinematography/sound/vfx/storyboard/creative_pack/tuning_notes
- **references/cases/INDEX.md**：6 表交叉索引（主注册表 + 技法→案例 + 场景→案例 + 风格→案例 + 角色→案例 + 更新 SOP）
- **references/cases/_TEMPLATE.md**：标准化案例拆解模板（按角色维度结构化）
- **references/cases/BR2049.md**：银翼杀手 2049 完整拆解（12 技法 × 5 角色维度 × 6 场景色调对照）
- **metadata/registry.yaml**：文件级注册表（39 个文件，含状态/依赖/归属/描述）
- **metadata/fields.yaml**：字段级元数据（50 个字段，含类型/默认值/影响角色/影响阶段）
- **metadata/dependencies.yaml**：上下游依赖图（22 对依赖关系，含影响等级）
- **metadata/CHANGELOG.md**：本文件
- **.gitignore**：排除产物/环境/IDE/OS 文件

### 设计决策

1. **美术定调 + 人物设定合并为「视觉开发」**（采纳评估阶段建议#2）
2. **新增「声音指导」角色**（采纳评估阶段建议#3）
3. **Creative Package JSON 标准化**（采纳评估阶段建议#4）
4. **案例库采用 6 表交叉索引 + Agent 自检清单**（解决高效索引和更新问题）
5. **导出格式：HTML（文学剧本 + 分镜展示）+ Excel（分镜技术表）**（采纳评估阶段建议）
6. **元数据维护体系：三层结构（registry + fields + dependencies）**（本次新增）

### 依赖

- 无外部运行时依赖
- 下游关联 Skill：HyperFrames, ComfyUI, image_gen

### 迁移

- 初始版本，无需迁移

---

## 模板：未来版本用的格式

```markdown
## [X.Y.Z] — YYYY-MM-DD

### 新增
- 

### 修改
- 

### 删除
- 

### 影响分析
- 受影响的文件：...
- 受影响的字段：...
- 需要迁移的内容：...

### 迁移指南
1. ...
2. ...
```
