```
══════════════════════════════════════════════
Muse Video Skill — v0.27.0 全链路审计 Handoff
将此提示词粘贴到 /new session 中启动审计
══════════════════════════════════════════════

项目身份
名称：Muse Video Skill（AI 视频前期策划引擎）
GitHub：LuoJiangYong/muse-video-skill（分支 main，最新 8d0e92a）
本地路径：D:\hermes workspace\muse video skill
当前版本：v0.27.0（已完成 v0.26.3 P0+P1 + v0.27.0 方案A）

══════════════════════════════════════════════
全部决策汇总
══════════════════════════════════════════════

| # | 议题 | 结论 |
|---|------|------|
| 1 | 角色身份层方案 | 方案A：Phase 2 Writer 产出 script.character_bible[]（identity+voice），AD P3 翻译为视觉，Writer P4+Sound P5 消费 |
| 2 | identity 字段粒度 | 6 字段：archetype/personality/background/motivation/flaw/role_arc |
| 3 | voice 字段归属 | character_bible（Writer 定义，Sound 翻译为音频），不留在 AD 模板 |
| 4 | AD 读 Writer 产出是否违规 | 不违规——Phase 3 已有先例（读 script.scenes[]），Project State JSON 是宪法规定的唯一接口 |
| 5 | DP 是否读 character_bible | 不读——DP 只消费视觉维度（体型/材质/服装色），与 identity 无关 |

══════════════════════════════════════════════
两轮改动摘要
══════════════════════════════════════════════

v0.26.3 P0+P1（角色消费全链路闭合）：
  - Writer/DP/Sound Agent Prompt 瘦身（HOW→WHAT，技法下沉）
  - 新增 §角色驱动对白（Writer）、§角色材质与灯光+§角色体型与构图（DP）、§角色声音签名（Sound）
  - has_characters 管线结构化提取
  - fields.yaml 消费声明修正

v0.27.0 方案A（角色身份层 character_bible）：
  - writer.md：宪法区分 P2/P4，新增 §角色身份定义（identity+voice 模板），Agent Prompt 更新
  - art-director.md：宪法追齐 Phase 3 实际输入，新增 §角色视觉翻译（identity→visual 映射），Agent Prompt 更新
  - sound-designer.md：宪法加读 character_bible，§角色声音签名拆两层（voice 权威源+visual 辅助），Agent Prompt 更新
  - default.md：Phase 2 产出表+Phase 3 输入表+操作序列同步
  - prompt_assembler.py：expand_each 支持 script.character_bible
  - CONSTITUTION/SKILL/CHANGELOG：版本升至 0.27.0
  - Step 13 修复：writer.md §角色驱动对白 触发行从 visual_dev.character_design[] 改为 character_bible[].voice + character_design[]

══════════════════════════════════════════════
审计目标
══════════════════════════════════════════════

对 v0.26.3 + v0.27.0 的所有改动做五维交叉审计：
  1. 元数据一致性（fields.yaml ↔ phase_gates.yaml ↔ 角色文档 ↔ default.md）
  2. 上下游消费完整性（每个字段：谁产出→谁消费→技法段→Agent Prompt→管线表 五层对齐）
  3. 宪法合规性（5 原则 + 禁止模式 + 角色三层架构）
  4. Director 门控覆盖（Director 能否在每跳节点有效审核角色相关产出？审核标准是否覆盖 character_bible 质量？）
  5. 旧引用残留（搜索 visual_dev.character_design 的每一次引用，确认为正确用途）

══════════════════════════════════════════════
关键文件速查
══════════════════════════════════════════════

宪法与元数据：
  CONSTITUTION.md             (282行) — 5原则+禁止模式+数据流+元数据治理
  SKILL.md                    (124行) — 路由树+场景类型+禁止事项
  metadata/fields.yaml        (495行) — 字段级元数据（path/type/affected_roles）
  metadata/phase_gates.yaml   (93行)  — 阶段门禁规则（requires_approved_sections/required_fields）
  metadata/CHANGELOG.md       (1062行)— 版本变更日志

角色文档（三层架构：宪法约束→技法库→Agent Prompt）：
  references/roles/director.md        (239行) — P1+审核节点，vision模板(L28-70)+审核标准(L74-116)+Agent Prompt(L220-239)
  references/roles/writer.md          (279行) — P2+P4 激活，§角色身份定义(L137) + §角色驱动对白(L120)
  references/roles/art-director.md    (351行) — P3 激活，§角色视觉翻译(L247) + §人物造型 Checklist(L198)
  references/roles/dp.md              (249行) — P4 激活，§角色体型与构图(L167) + §角色材质与灯光(L93)
  references/roles/sound-designer.md  (228行) — P5 激活，§角色声音签名(L81，双层)

管线与脚本：
  references/pipelines/default.md  (268行) — 7阶段产出表+输入表+操作序列
  scripts/prompt_assembler.py      (517行) — expand_each 段(L191-226)

设计规范：
  references/role-doc-design.md — 角色文档三层架构 + Agent Prompt 1行引用规则 + 修正流程（从元数据出发）

══════════════════════════════════════════════
预期数据流（v0.27.0 修正后）
══════════════════════════════════════════════

P1 Director → director_notes.vision + has_characters
    │
    ▼
P2 Writer → script.character_bible[]（identity + voice — 权威源）
    │  ▲ Director 审核（门控点 #1：character_bible 质量）
    ▼
P3 AD → 读 character_bible + script.scenes[]
         → §角色视觉翻译：identity → visual_profile + wardrobe
         → 产出 visual_dev.character_design[]
    │  ▲ Director 审核（门控点 #2：视觉翻译是否忠于 character_bible identity）
    ▼
P4 Writer → 读 character_bible[].voice + character_design[]
            → §角色驱动对白：写对白（不再逆推 visual_profile）
P4 DP → 读 character_design[]（仅 visual_profile + wardrobe）
        → §角色体型+§角色材质：构图+灯光
    │  ▲ Director 审核（门控点 #3：对白是否与 character_bible voice 一致）
    ▼
P5 Sound → 读 character_bible[].voice + character_design[]
           → §角色声音签名（voice 权威源 → 配乐动机+音效标记）
    │  ▲ Director 审核（门控点 #4：声音签名是否与 character_bible voice 一致）
    ▼
P6-7 → 分镜组装 + 终审

══════════════════════════════════════════════
⚠️ 已知风险：Director 门控盲区
══════════════════════════════════════════════

director.md 的审核标准（L88-94）是通用的——「产出符合 vision」「内部自洽」「完整性达标」。
v0.27.0 新增 character_bible 后，Director 在 4 个门控点需要审核角色相关产出，
但审核标准中没有任何角色专项检查项。潜在问题：

  门控点 #1 (Phase 2)：Writer 产出 character_bible
    - 当前能审：完整性（字段是否全填）✅  内部自洽（archetype 与 personality 是否矛盾）✅
    - 可能遗漏：identity 是否具体到可供 AD 翻译为视觉？voice 是否具体到可供 Sound 映射为音频？
    - 风险：Director approve 了一个所有 identity 字段都填了但都是泛化占位符的 character_bible

  门控点 #2 (Phase 3)：AD 产出 character_design
    - 当前能审：色调是否匹配 vision ✅
    - 可能遗漏：visual_profile 是否忠于 character_bible identity？
      例：character_bible 说"内敛克制"，AD 给了亮色暴露服装 → Director 能发现吗？
    - 风险：AD 的视觉翻译偏离 identity，Writer P4 基于偏离的视觉写对白

  门控点 #3 (Phase 4)：Writer 产出对白
    - 当前能审：对白密度/字数 ✅
    - 可能遗漏：对白风格是否与 character_bible.voice 一致？
    - 风险：Writer 读了 character_bible.voice 但没真正用

  门控点 #4 (Phase 5)：Sound 产出声音签名
    - 当前能审：配乐风格方向 ✅
    - 可能遗漏：配乐动机是否从 character_bible.voice 推导？
    - 风险：Sound 回退到从 visual_profile 逆推

══════════════════════════════════════════════
审计 SOP（逐项执行）
══════════════════════════════════════════════

1. 环境确认
   cd "D:\hermes workspace\muse video skill"
   git status --short  # 应干净
   git log --oneline -8  # 确认 7 commits 完整
   python scripts/build_index.py --check --deps  # 应 0 errors, 0 dead links

2. 元数据交叉审计（fields.yaml ↔ 角色宪法 ↔ default.md ↔ phase_gates.yaml）
   对每个受影响字段（script.character_bible / visual_dev.characters / script.scenes），
   用 search_files 验证：
   a) fields.yaml affected_roles 与角色文档宪法约束一致
   b) fields.yaml affected_phases 与 default.md 阶段产出/输入表一致
   c) visual_dev.characters 的 affected_roles = [art-director, writer, dp, sound-designer]
   d) script.character_bible 的 affected_roles = [writer, art-director, sound-designer]（不含 DP）
   e) phase_gates.yaml Phase 3 门禁：requires_approved_sections 含 script（覆盖 character_bible）
   f) phase_gates.yaml Phase 2 门禁：required_fields 不含 character_bible（正确——条件产出不应硬门禁）

3. Director 门控覆盖审计（重点）
   读 references/roles/director.md，对照以下清单逐项检查：

   a) Vision 模板（L28-70）：
      - L69 "角色需求" 字段是否驱动了 has_characters 提取？✅（default.md Phase 1 步骤 4b）
      - 是否需要新增字段让 Director 在 Phase 1 就描述角色方向？
        当前 vision 模板没有「角色方向描述」字段——Director 对"K 是沉默调查员"的认知
        写在 vision 自由文本中，Writer 从中提取。这够不够？

   b) 审核标准（L74-116）：
      - 通用 APPROVE 条件（L88-94）是否覆盖 character_bible 质量？
        逐条对照：✅方向一致 ✅内部自洽 ✅完整性 ✅无硬伤 ✅可推进下一阶段
        ⚠️ 缺少角色专项：identity 具体性 / voice 可翻译性
      - 是否需要新增角色专项审核条件？如：
        「角色身份字段无泛化占位符（如 archetype 不能只写'反英雄'而不描述具体特质）」
        「voice 字段足够具体，可供 Sound 直接映射为音频参数」

   c) Phase 2 审核节点（default.md L92-95）：
      - Writer 产出含 character_bible 后，Director 的审核操作序列是否足够？
      - 当前 default.md 只写「Director 审核（按 director.md 审核标准）」——需不需要
        显式标注「如有角色，检查 character_bible 的 identity+voice 完整性」？

   d) Phase 3 审核节点（default.md L120-123）：
      - AD 产出 character_design 后，Director 是否验证 visual 翻译忠于 character_bible？
      - 当前审核指令只提色调/风格/场景空间，未提角色视觉翻译验证

   e) Phase 4 审核节点（default.md L147-150）：
      - Writer 对白 + DP 镜头后，Director 是否验证对白与 character_bible voice 一致？

   f) Phase 5 审核节点（default.md L173-176）：
      - Sound 声音签名后，Director 是否验证其与 character_bible voice 一致？

   g) Director Agent Prompt（L220-239）：
      - 是否需要加角色相关审核指令？当前完全未提角色
      - 「你不得」列表中是否需要加角色相关禁止项？如：
        「不得在 character_bible 只有占位符时 approve Phase 2」

   h) 门禁完整性：
      - 如果 Director 在 Phase 2 approve 了不合格的 character_bible，
        Phase 3 门禁（phase_gates.yaml）能否拦截？→ 不能——门禁只检查 script section
        是否 approved，不检查内容质量。门控依赖 Director 的人工审核质量。
      - 这是设计意图还是缺陷？→ 判断：门禁是技术检查（字段是否存在），
        质量是 Director 的人为判断。如果 Director 的审核标准没有角色专项检查，
        质量门控就是盲区。

4. 角色三层架构审计（逐个角色，读文件验证）
   对 Writer/AD/DP/Sound 四个角色，验证三层齐全且一致：
   a) 宪法约束 header（文件前5行 blockquote）→ 读列表与 Agent Prompt 消费指令一致
   b) 技法段 → 触发行描述的数据源与宪法约束一致；映射表输入维度在数据源中存在
   c) Agent Prompt → 消费指令引用技法段名称精确匹配；消费指令 ≤1 行/数据源
   d) 禁止项 → 窄化到具体错误行为

   重点检查点：
   - Writer L122 触发行：是否写 "script.character_bible[].voice + visual_dev.character_design[]"
   - Writer L266 Agent Prompt：读 character_bible.voice + character_design → §角色驱动对白
   - AD L341 Agent Prompt：读 character_bible → §角色视觉翻译 → 填 checklist
   - Sound L83 触发行：是否写 "script.character_bible[] + visual_dev.character_design[]"
   - Sound L214 Agent Prompt：读 character_bible.voice + character_design → §角色声音签名
   - DP L239 Agent Prompt：只读 character_design[]，不含 character_bible（正确）

5. 上下游消费完整性（逐个字段，追踪 5 层）
   对 script.character_bible 字段：
   ┌─ 生产者：Writer P2（writer.md 宪法 + Agent Prompt L265 + default.md L80 + L91）
   ├─ 消费者1 AD P3：宪法 L5 / §角色视觉翻译 L247 / Agent Prompt L341 / default.md L105
   ├─ 消费者2 Writer P4：宪法 L5 / §角色驱动对白 L122 / Agent Prompt L266
   ├─ 消费者3 Sound P5：宪法 L5 / §角色声音签名 L83 / Agent Prompt L214 / default.md Phase 5（script.* 通配符）
   ├─ 门控点：Director Phase 2/3/4/5 审核节点 ×4
   └─ 非消费者 DP：宪法 L5 无 character_bible / Agent Prompt L239 无 character_bible ✓

   对 visual_dev.character_design 字段：
   ┌─ 生产者：AD P3
   ├─ 消费者1 Writer P4：宪法 L5 / §角色驱动对白 L122 / Agent Prompt L266
   ├─ 消费者2 DP P4：宪法 L5 / §角色体型+§角色材质 / Agent Prompt L239
   ├─ 消费者3 Sound P5：宪法 L5 / §角色声音签名 L83 / Agent Prompt L214
   ├─ 门控点：Director Phase 3/4/5 审核节点 ×3
   └─ 检查：此字段是否仍只含视觉维度（不应含 personality/voice）

6. 宪法合规审计
   对照 CONSTITUTION.md：
   - 原则1 高内聚：character_bible 是否只在 script.* 下、Writer 单一归属、无重复定义？
   - 原则2 低耦合：所有消费是否通过 Project State JSON、无角色文件互相引用？
   - 原则3 可扩展：新增字段是否只需改 fields.yaml + 消费者各 1 行指令？
   - 原则4 易维护：character_bible 和 character_design 是否通过 character_id 关联可追溯？
   - 原则5 高效简洁：character_bible 消费者 ≥ 3？
   - 禁止模式2：role 文件是否引用了其他 role 文件？
   - 禁止模式4：角色文档是否按需加载（非一次全载）？
   - 禁止模式5：Director 是否在 Phase 1 之外跳过审核？
   - 元数据治理：fields.yaml 字段数是否与实际 Schema 同步？

7. 旧引用残留扫描
   search_files pattern="visual_dev.character_design" target=content
   逐条确认每处引用是正确用途（AD 产出声明 / DP 消费视觉 / 历史 CHANGELOG）还是遗漏更新

   同样搜索 "visual_dev.characters"（Schema 名）确认 prompt_assembler.py + creative-pack.md 引用正确

8. 收尾
   git status  # 确认干净
   汇总审计报告：列出所有 ✅ 通过项 + ⚠️ 风险项 + ❌ 缺陷项
   对 ⚠️ 风险项给出建议（修/不修/记录为技术债）
   对 ❌ 缺陷项立即修复 → commit → push
   如全部 ✅：报告"审计通过，任务可关闭"

══════════════════════════════════════════════
已知陷阱
══════════════════════════════════════════════

- patch 工具在 prompt_assembler.py 中遇到 "Found 2 matches" 错误——script.scenes expand_each 出现两次，
  需带更多上下文或用 sed 直接插入
- read_file 返回的 content 含行号前缀，不能直接写回文件
- CHANGELOG.md 必须每步同步更新，不能等到最后批量补
- 用户对 git commit+push 遗漏零容忍——每个逻辑步骤结束立即 add+commit+push
- SKILL.md / CONSTITUTION.md / CHANGELOG.md 三个文件的版本号必须一致
- director.md L69 "角色需求" 字段的枚举值是 "有角色 / 无角色 / 不确定"——
  这与 has_characters 的 true/false/null 对应，但 vision 模板本身没有「角色方向描述」字段
```
