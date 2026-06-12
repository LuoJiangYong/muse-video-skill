# 案例索引 — Case Index

> 影视作品 + 创意广告双轨收录。每新增一个案例 = 本文件加一行 + `references/cases/<id>.md` 创建。
>
> **更新纪律**：添加案例时，同步更新本文件的所有相关交叉索引表。删除/修改案例时，必须同时更新各表。

---

## 一、主注册表 Master Registry

| ID | 名称 | 类型 | 年份 | 导演/工作室 | 主场景 | 辅场景 | 核心技法标签 |
|----|------|------|------|-----------|--------|--------|------------|
| BR2049 | 银翼杀手2049 | film | 2017 | Denis Villeneuve | sci-fi | studio-ad | 巨物美学, 单一光源, 色彩叙事, 粒子氛围, 沉默对白, 环形构图 |
| APPLE-WH | Welcome Home | commercial | 2018 | Spike Jonze | studio-ad | product-demo | 超现实转场, 物理空间扭曲, 单镜头错觉, 色彩情绪, 舞蹈编排 |
| NIKE-YCS | You Can't Stop Us | commercial | 2020 | Oscar Hudson | product-demo | logo-animation | 分屏匹配, 动态节奏, 档案素材, 隐喻剪辑, 品牌精神 |
| APPLE-DB | Don't Blink | commercial | 2019 | — | product-demo | studio-ad | 高速剪辑, 产品密度, 节奏递增, 极简旁白, 功能叙事 |
|| COSMOS-L | Cosmos Laundromat | short-film | 2015 | Blender Foundation | sci-fi | product-demo | 材质渲染, 自然光, 角色动画, 环境叙事, 非人类主角 |
|| WKW-ML | 花样年华 | film | 2000 | 王家卫 | custom | studio-ad | 留白叙事, 重复结构, 框架构图, 色彩叙事, 慢快门步印, 旗袍叙事 |
|| WANDERING-E | 流浪地球 | film | 2019 | 郭帆 | sci-fi | product-demo | 巨物尺度, 集体英雄主义, 等离子蓝, 行星发动机, 低频嗡鸣, 中国民乐融合 |

### 类型枚举

| 缩写 | 含义 | 典型特征 |
|------|------|---------|
| film | 电影 | 完整叙事弧线，2h±，多场次 |
| commercial | 广告片 | 短时长(15s-3min)，品牌目标，强记忆点 |
| short-film | 短片 | 15min±，完整故事，常有实验性 |
| music-video | MV | 音乐驱动，视觉节奏优先 |
| experimental | 实验影像 | 打破常规，技法探索，非叙事 |
| animation | 动画 | 全CG/手绘/定格 |
| documentary | 纪录片 | 真实素材，访谈，档案 |

---

## 二、技法 → 案例 Mapping

> Agent 查询路径：用户提到某个技法 → 查此表 → 加载对应案例文件 → 读取该技法的具体拆解。

### 叙事技法 (→ Writer)

| 技法 | 案例 ID |
|------|---------|
| 沉默对白 | BR2049 |
| 信息释放节奏 | BR2049 |
| 反转结构 | BR2049 |
| 隐喻剪辑 | NIKE-YCS |
| 极简旁白 | APPLE-DB |
| 环境叙事 | COSMOS-L |
| 留白叙事 | WKW-ML |
| 重复结构 | WKW-ML |
| 未完成情感 | WKW-ML |
| 时代背景隐喻 | WKW-ML |
| 集体英雄主义 | WANDERING-E |
| 父子双线叙事 | WANDERING-E |
| 灾难阶梯 | WANDERING-E |
| 牺牲主题 | WANDERING-E |

### 镜头语言 (→ DP)

| 技法 | 案例 ID |
|------|---------|
| 巨物美学 | BR2049 |
| 单一光源 | BR2049 |
| 环形构图 | BR2049 |
| 单镜头错觉 | APPLE-WH |
| 高速剪辑 | APPLE-DB |
| 分屏匹配 | NIKE-YCS |
| 档案素材 | NIKE-YCS |
| 自然光模拟 | COSMOS-L |
| 框架构图 | WKW-ML |
| 慢快门步印 | WKW-ML |
| 浅景深孤立 | WKW-ML |
| 镜面反射 | WKW-ML |
| 极端低角度 | WKW-ML |
| 巨物尺度对比 | WANDERING-E |
| 广角畸变 | WANDERING-E |
| 第一视角穿越 | WANDERING-E |
| 零重力调度 | WANDERING-E |

### 色彩/美术 (→ Art Director)

| 技法 | 案例 ID |
|------|---------|
| 色彩叙事 | BR2049, APPLE-WH |
| 场景色调对照表 | BR2049 |
| 材质渲染 | COSMOS-L |
| 物理空间扭曲 | APPLE-WH |
| 旗袍色彩叙事 | WKW-ML |
| 墙纸视觉密度 | WKW-ML |
| 场景色调对照 | WKW-ML |
| 五域色调体系 | WANDERING-E |
| 地下城烟火气 | WANDERING-E |

### 特效语言 (→ VFX)

| 技法 | 案例 ID |
|------|---------|
| 粒子氛围 | BR2049 |
| 全息投影 | BR2049 |
| 超现实转场 | APPLE-WH |
| 分屏/画中画 | NIKE-YCS |
| 材质表现 | COSMOS-L |
| 步印模拟 | WKW-ML |
| 雨夜霓虹 | WKW-ML |
| 烟雾氛围层 | WKW-ML |
| 行星发动机火焰 | WANDERING-E |
| 地球冻结 | WANDERING-E |
| 大气抽离 | WANDERING-E |
| 运载车集群 | WANDERING-E |

### 声音设计 (→ Sound Designer)

| 技法 | 案例 ID |
|------|---------|
| 合成器低音+留白 | BR2049 |
| 环境音优先于对白 | BR2049 |
| 动态节奏 | NIKE-YCS |
| 音乐锚点 | WKW-ML |
| 对白省略 | WKW-ML |
| 低频嗡鸣 | WANDERING-E |
| 冰裂高频 | WANDERING-E |
| 中国民乐融合 | WANDERING-E |
| 多语言广播 | WANDERING-E |

### 创意广告专属 (→ Studio-Ad, Product-Demo)

| 技法 | 案例 ID |
|------|---------|
| 产品密度 | APPLE-DB |
| 功能叙事 | APPLE-DB |
| 节奏递增 | APPLE-DB |
| 品牌精神 | NIKE-YCS |
| 舞蹈编排 | APPLE-WH |
| 非人类主角 | COSMOS-L |

---

## 三、场景类型 → 案例 Mapping

> Agent 查询路径：用户选择/匹配到某个场景类型 → 查此表 → 加载该场景最相关的案例。

| 场景类型 | 强相关案例 | 可参考案例 |
|----------|----------|-----------|
| studio-ad | APPLE-WH, APPLE-DB | BR2049, NIKE-YCS |
| logo-animation | NIKE-YCS | APPLE-WH |
| product-demo | NIKE-YCS, APPLE-DB, COSMOS-L | APPLE-WH |
| sci-fi | BR2049, COSMOS-L, WANDERING-E | — |
| custom (art-film) | WKW-ML | — |

---

## 四、风格/情绪 → 案例 Mapping

| 风格/情绪 | 案例 ID |
|-----------|---------|
|| cyberpunk | BR2049 |
|| cyberpunk-adjacent | WANDERING-E |
| minimalist | APPLE-DB, BR2049 |
| surreal | APPLE-WH, COSMOS-L |
| epic | BR2049, NIKE-YCS, WANDERING-E |
| intimate | BR2049, WKW-ML |
| energetic | NIKE-YCS, APPLE-DB |
| dreamy | APPLE-WH, COSMOS-L, WKW-ML |
|| gritty | BR2049, WANDERING-E |
|| nostalgic | WKW-ML |
|| melancholic | WKW-ML |

---

## 五、角色维度 → 案例 Mapping

> 当用户想提升某个特定角色的表现时，直接推荐最相关的案例。

| 角色 | 必看案例 | 推荐案例 |
|------|---------|---------|
|| Writer (编剧) | BR2049, WKW-ML, WANDERING-E | NIKE-YCS |
| DP (摄影指导) | BR2049, APPLE-WH, WKW-ML, WANDERING-E | COSMOS-L |
| Art Director (美术) | BR2049, APPLE-WH, WKW-ML, WANDERING-E | COSMOS-L |
|| VFX Supervisor (特效) | BR2049, APPLE-WH, WKW-ML, WANDERING-E | COSMOS-L |
|| Sound Designer (声音) | BR2049, WKW-ML, WANDERING-E | NIKE-YCS |
| 广告创意综合 | APPLE-DB, NIKE-YCS | APPLE-WH |

---

## 六、更新工作流 (SOP)

### 添加新案例

```
1. Agent 或用户发现值得收录的作品
2. Agent 检查 INDEX.md 是否已存在
3. 若不存在 → 确认收录
4. Agent 观看/研究作品 → 按 _TEMPLATE.md 格式拆解
5. Agent 创建 references/cases/<id>.md
6. Agent 更新 INDEX.md：
   a. 主注册表：加一行
   b. 技法→案例表：每个新技法加一条
   c. 场景→案例表：加一条
   d. 风格→案例表：加一条
   e. 角色→案例表：加一条
7. git commit + push
```

### 修改/推翻已有案例

```
1. 指出具体问题（哪个技法分析不对、哪个角色段不准确）
2. Agent 修改 references/cases/<id>.md
3. 若技法标签变化 → 同步更新 INDEX.md 所有相关表
4. git commit + push
```

### 索引一致性检查 (Agent 自检清单)

```
□ 主注册表的 ID 与文件名一致
□ 每个技法标签在「技法→案例表」中至少出现一次
□ 主注册表的「主场景」「辅场景」与「场景→案例表」一致
□ 主注册表的「类型」枚举值正确
□ 每个案例 ID 在角色表中对应行完整
```

---

*最后更新：2026-06-12 | 案例总数：7（Phase 6 进行中: WKW-ML + WANDERING-E 已添加）*
