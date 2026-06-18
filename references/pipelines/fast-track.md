# 快速管线 — Fast-Track Pipeline（3 阶段）

> **定位**：标准管线的加速变体。合并阶段以减少轮次和审核次数。仍遵守宪法——Director 不跳过，产出写入 Project State JSON。
> **适用条件**：1-2 场景 / 无角色设定 / 用户催快 / 已提供完整 brief。
> **决策阈值**：满足 ≥2 条适用条件 → 自动激活快速管线。

---

## 适用条件检测（Agent 路由用）

```python
# Agent 在路由时评估以下条件，满足 ≥2 条 → fast-track
conditions = [
    scene_count <= 2,                # 场景数 ≤ 2
    not has_characters,              # 无角色设定需求
    user_wants_fast,                 # 用户说"快点/简单点/随便搞"
    user_provided_full_brief,        # 用户已在请求中给出了完整 brief
]
```

---

## 阶段合并策略

```
标准 7 阶段:  1 → 2 → 3 → 4 → 5 → 6 → 7

快速 3 阶段:  1 → [2+3+4 合并] → [5+6+7 合并]

合并逻辑:
  阶段A（一组产出 + 一次审核）= Phase 2+3+4 合并（Writer + Art Director + DP 并行）
  阶段B（一组产出 + 一次审核）= Phase 5+6+7 合并（Sound + Storyboard + Assembly）
```

---

## 阶段 A：「一稿过」内容+视觉+脚本

| 维度 | 内容 |
|------|------|
| **激活角色** | Writer + Art Director + DP（并行产出）→ Director（一次性审核） |
| **触发条件** | Phase 1 用户确认方向后 |
| **输入** | director_notes.vision, project.*（来自 Phase 1） |
| **产出** | script.logline, script.synopsis, script.scenes[]（含对白+动作）, visual_dev.*（色调+风格+场景搭建）, cinematography.shot_list[]（每个场景的镜头） |
| **Director 审核** | ✅ 审核一次（合并后审核） |
| **Loop 规则** | 1 轮修改（不是 2 轮） |

### 操作序列

1. **Director 先将 vision brief 分发给 3 个角色**（一次性分发，不等结果）
2. Writer 加载 `references/roles/writer.md` → 产出 logline + synopsis + 场景+对白
3. Art Director 加载 `references/roles/art-director.md` → 产出色调方案 + 风格方向
4. DP 加载 `references/roles/dp.md` → 产出镜头方案 + 灯光方向
5. **注意**：3 个角色并行执行——他们各自只读 `director_notes.vision`，不互相等待
6. Director 收集 3 份产出 → 一次性审核（按 director.md 审核标准）
   - **Approve** → 进入阶段 B
   - **Revise（1 轮）** → 标注问题，角色修改后重交 → Director 必须 approve
   - **Reject** → 回到 Phase 1 重写 vision

### 并行规则

| 规则 | 说明 |
|------|------|
| **共享输入** | 3 个角色都只读 `director_notes.vision` + `project.*`。不读彼此产出 |
| **冲突处理** | 若 Writer 说「亲密特写」而 DP 说「广角远景」→ Director 在审核时裁决，选其一，不改回 |
| **独立性** | 遵循宪法原则 2：角色文件不互引，产出不互等 |
| **工具调用** | Art Director 可在此阶段调用 `image_gen` 生成 moodboard（如果触发条件允许） |

---

## 阶段 B：声音+分镜+组装

| 维度 | 内容 |
|------|------|
| **激活角色** | Sound Designer + VFX → Storyboard 组装 → Director（一次性审核） |
| **触发条件** | 阶段 A Director 审核通过 |
| **输入** | 完整 Project State（含 script.* + visual_dev.* + cinematography.*） |
| **产出** | sound.* + storyboard.panels[] + creative_pack（完整） |
| **Director 审核** | ✅ 终审（合并后审核） |
| **Loop 规则** | 1 轮修改 |

### 操作序列

1. Sound Designer 读取 script.scenes[] → 产出 sound.* 方向
2. VFX 加载 `references/roles/vfx.md` → 标注特效到 storyboard panels
3. 组装 storyboard：为每个场景生成 1-2 个关键 panel（标准管线是 1-3 个，快速管线减半）
4. Director 终审：全量产出是否自洽？
   - **Approve** → 组装 Creative Pack
   - **Revise（1 轮）** → 标注后修改重交

---

## 与标准管线的差异速查

| 维度 | 标准管线 | 快速管线 |
|------|---------|---------|
| 阶段数 | 7 | 3 |
| Phase 2-4 关系 | 串行，各审一次 | 合并，并行产出，审一次 |
| 修改轮数上限 | 2 轮 | 1 轮 |
| 分镜 panel 数/场景 | 1-3 个 | 1-2 个 |
| 调用 image_gen | 可选（Phase 3 + Phase 6） | 仅阶段 A 一次 |
| 导出文件 | HTML + Excel 双格式 | 默认仅 JSON，用户要时再导出 |
| 适用场景 | 复杂项目 | 简单需求 |
| Director 参与度 | 每个阶段审核 | 3 次审核（Phase 1 + 阶段 A + 阶段 B） |

---

## 降级规则

如快速管线执行过程中出现以下情况 → **自动降级为标准管线**：

- Director 在阶段 A 审核时发现超过 3 处需要修改 → 「创意复杂度超过快速管线能力，降级为标准管线，回到 Phase 2」
- 用户在阶段 A 审核后说「再改一下」超过 1 次 → 降级
- 用户中途追加需求（如「加一个角色」「再加一个场景」）→ 降级

降级时：已完成的部分保留在 Project State JSON 中（标记 `_meta.pipeline: "fast-track→default"`），从标准管线的对应阶段继续。
