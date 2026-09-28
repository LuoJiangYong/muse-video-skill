# 参考图优于文字描述 — Reference Image Over Text

> **角色**：参考图引用链的权威源 —— 全管线引用纪律 + 编译器检测规则。用户提供的参考照片（角色外观、场景实景）中的视觉信息，不应在 Project State 或 prompt 中用大段文字重新描述；参考图直接对接下游工具（Seedance reference_image），文字层只负责参考图覆盖不到的部分（构图 / 色调 / 运镜 / 氛围）。
> **被依赖**：roles/art-director.md（步骤 0）· roles/dp.md
> **宪法位置**：`references/reference-image-over-text.md` — 交叉关注点，放 references 根目录。
> **最后更新**：2026-09-28 | v0.31.0

---

## 全管线执行纪律

> 参考图是**数据**，不是**元数据**：登记进顶层 `file_registry`，各阶段按逻辑名引用，不转述。

| Phase | 角色 | 纪律 |
|-------|------|------|
| 1 | Director | 用户提供参考照片 → 登记顶层 `file_registry`（logical_name → local_path / role / source） |
| 3 | Art Director | **步骤 0**：检查 `file_registry` —— 有参考图仅引用 file_id / local_path，不重述外观特征 |
| 4 | DP | 运镜 / 构图描述不重述参考图已有内容（构图信息经 image_ref 传递） |
| 6 | Storyboard | panel prompt 只写参考图**没有**的（构图 / 运镜 / 色调 / 氛围）；参考图用 file_id / 占位符引用 |
| 7.5 | Model Compiler | 引用 `file_registry` 的 file_id → `image_ref_N`；如 compiled_prompt 重复描述参考图已有特征 → 追加 `_quality` 警告 |

### 编译器检测规则（Phase 7.5）

- `compiled_prompt` 中出现参考图已有视觉特征的文字重述 → `_quality.warnings` 追加：「image_ref_N 已含 [该特征]，prompt 重复描述 → 建议删除」
- 干跑清单已含「所有 image_ref file_id 在 file_registry 中可查」（见 `references/model-compiler.md` §干跑验证清单）

---

## 为什么

1. **文字描述是信息损失**。一张 200KB 的照片包含数百万像素的精确信息，文字最多捕捉几十个粗略特征。用文字重新描述参考图 = 故意降低信息精度。
2. **AI 模型消费参考图比消费文字描述更准确**。Seedance 的 `reference_image_weight=0.9` 比 prompt 中的「深琥珀色圆眼、粉红色小鼻头」更可靠。
3. **用户提供参考图就是为了省去文字描述**。用户花时间找/拍参考图，Agent 不应该再花更多 token 去描述它。

## 正确做法

### 角色参考（猫、人物等）

```json
// ✅ 对——只引用文件，不描述特征
{
  "traits": "参照用户原始照片 080ffe6c...jpg",
  "ref_image_prompt": "参照原始照片",
  "consistency_notes": "原始照片直接作为Seedance reference_image(weight=0.9)"
}

// ❌ 错——大段文字重新描述参考图已有内容
{
  "traits": "纯白长毛波斯系猫，深琥珀色大圆眼，粉红色小鼻头，圆脸娃娃脸，小圆耳带长长耳饰毛，丰厚白色围脖毛，体型半矮胖圆圆。穿浅蓝白相间洛丽塔裙（裙身浅蓝#B0C4DE，领口白色荷叶边）..."
}
```

### 场景参考（地标、窗外景色等）

```json
// ✅ 对——引用文件路径 + 构图/色调描述
{
  "prompt": "韦斯安德森对称构图。猫背影坐于车厢座椅，望向车窗外。窗外景色参照用户广州天际参考图。车厢3200K暖光vs窗外5500K日光。PUDONG-CAT马卡龙色谱。"
}

// ❌ 错——重新描述参考图中的建筑
{
  "prompt": "窗外广州日落天际线——广州塔银灰塔身居中偏左，猎德大桥红色拱形跨江，东西塔分立两侧，金色斜阳打亮CBD群楼，天空淡蓝到橙粉渐变..."
}
```

## Prompt 分工表

| 内容来源 | 放哪里 | 不放哪里 |
|---------|--------|---------|
| 猫的外观 | 参考图文件 → Seedance `reference_image` | ❌ characters[].traits 大段文字 |
| 窗外景色 | 参考图文件 → 文件引用 | ❌ prompt 中逐一描述建筑 |
| 桥的结构 | 参考图文件 → 文件引用 | ❌ scene_composition 中逐一描述拱圈/拉索 |
| 构图/对称/中轴 | ✅ prompt / camera_notes | — |
| 色调/色温 | ✅ palette / lighting | — |
| 运镜/景别 | ✅ shot_list | — |
| 氛围/情绪 | ✅ mood / visual_cause | — |

## 例外

以下情况可以用文字补充描述：
- 参考图中**没有**的元素（如「车门指示灯显示'欢迎来到广州'」）
- 参考图中**需要改变**的元素（如 PUDONG-CAT 案例中「窗外从上海陆家嘴换为广州珠江新城」——只需说「参照用户广州天际参考图」，不需要列出建筑名）
- 参考图本身的**构图建议**（如「参照PUDONG-CAT S2构图——猫背坐座椅看窗外」）

## Seedance Prompt 中的参考图引用

> **规则**：在 Seedance 六段式 prompt 中，引用参考图内容时使用占位符 `image_ref_N`（与 `--extra-body` 中的 `image_url` 顺序对应），而非重新描述参考图中的内容。

### 示例

```text
// ✅ 对——使用占位符引用参考图
Subject: image_ref_1中的白猫（用户原始照片），穿浅蓝白洛丽塔裙，
背影端坐于暖色列车座椅上。

Scene: 车窗外景色参照image_ref_2（用户广州日落天际线参考图）。
车厢内构图与氛围参照image_ref_3（PUDONG-CAT案例S2车厢构图）。

// ❌ 错——重新描述参考图中已有的猫特征和窗外建筑
Subject: 纯白长毛波斯系猫，深琥珀色大圆眼，粉红色小鼻头...
Scene: 窗外广州塔银灰塔身居中偏左，猎德大桥红色拱形跨江...
```

### 占位符映射表（必须与 --extra-body 顺序一致）

| 占位符 | 用途 | 文件 | weight |
|--------|------|------|--------|
| `image_ref_1` | 角色锚定 | 用户猫原照 | 0.9 |
| `image_ref_2` | 场景氛围 | 窗外天际参考 | 0.6 |
| `image_ref_3` | 构图风格 | PUDONG-CAT 案例帧 | 0.4 |

## 教训来源

> 教训来源：2026-06-30 猫游广州项目 Phase 7.5。用户审查 prompt 时指出「提示词没看到有说直接参考照片里的猫，构图也没看到参考已有的」。修正为 `image_ref_N` 占位符后通过。

2026-06-30 猫游广州项目。用户在 Phase 3/3.5/6 多次纠正 Agent 对参考图的文字描述：
- 「猫特征不赘述直接传下游」
- 「不需要额外大段提取已有真实参考的场景/人物/对象本身的文字特征」
- 「车窗外的描述也直接引用参考图片，提示词主要描述画面构图、色调、运镜等，参考图有的不需要再赘述」

---

> 相关：`references/free-image-sources.md`（免版权图源 —— 搜索获取的实景图同走本引用纪律）。
