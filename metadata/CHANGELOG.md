# Changelog — 版本变更日志

> 记录每次修改的动机、内容、影响范围、迁移指南。
> 每次 git commit 涉及实质改动时同步更新此文件。
> 格式：`## [version] — YYYY-MM-DD`

---

## [0.20.0] — 2026-06-16

### 新增 — APPLE-EDUCATION 案例（Apple教育品牌片 × 教室叙事 × CGI隐喻 × 品牌使命）

**案例新增：APPLE-EDUCATION — Apple Education: Ready for every learning opportunity**
- 类型：commercial（品牌使命型广告）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：教室微故事叙事, CGI隐喻叙事(Amazona鹦鹉群), 品牌使命叙事, 产品退位叙事, 师生共创叙事, 自然光课堂摄影, 学生视线高度运镜, CGI鹦鹉群集成, 原创indie-pop配乐
- 特征：1:47, 4553万播放, Ms. Charlene教师, 15-20名学生, CGI鹦鹉隐喻创造力, 零产品规格
- 独特价值：首个品牌使命型案例（不同于3C产品介绍片和快闪广告）、首个CGI动物隐喻案例、首个教育场景案例、首个「产品退位=品牌上位」策略案例

### 新增 — APPLE-EVENT-HIGHLIGHTS 案例（Apple九月发布会集锦 × 产品速览 × 密度叙事）

**案例新增：APPLE-EVENT-HIGHLIGHTS — Catch up quick | Apple September event highlights**
- 类型：commercial（发布会集锦型广告）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：产品速览叙事, 密度递增结构, 产品对比排列, 女声非正式旁白, 无故事纯信息叙事, CGI内部透视, 多产品并列构图, 功能可视化动画, 女声快节奏旁白, 信息压缩策略
- 特征：2:35, 255万播放, 7款产品(2分35秒), Tim Cook开场, 女声快节奏旁白(~190wpm), 46:1压缩比
- 独特价值：首个发布会集锦案例、首个多产品速览格式案例、首个「无故事纯信息」叙事案例、与APPLE-EDUCATION形成「使命vs信息」「慢vs快」「情感vs功能」极端对照

### 类型覆盖
- commercial 20→23（新增教育品牌片×1 + 发布会集锦×1）
- 案例总数：27→29

## [0.19.0] — 2026-06-16

### 新增 — APPLE-FLASH 案例（Apple快闪产品美学 × AirPods Pro 3 + MacBook Neo all-new 双片对比）

**案例新增：APPLE-FLASH — Apple快闪产品美学（双视频对比分析）**
- 类型：commercial（超短片产品广告，合计1分23秒）
- 20+ 技法 × 5 角色维度 × 5 创意策略维度
- 核心技法：特征罗列叙事, 音乐驱动叙事, 无旁白纯视听叙事, 顶拍手部编舞, 身体即产品载体, 霓虹电子色谱, glitch数码故障转场, 抽象几何动画合成, 电子鼓打贝斯驱动, indie-pop配乐, 拟音同步打击
- 特征：AirPods Pro 3 (48s, 281万播放) + MacBook Neo all-new (35s, 488万播放)，均无传统旁白，音乐驱动剪辑，文字叠加传递产品信息
- 来源：YouTube 官方视频通过 video_analyze 两轮分析（H.264 编码，成功绕过 av1 陷阱）
- 独特价值：首个合并双视频对比分析案例，提取 Apple 超短片「快闪公式」（音乐驱动+无旁白+文字覆盖+身体交互），展示同一套公式在可穿戴产品 vs 笔记本电脑上的差异化应用
- 类型覆盖新增：commercial×21（总计 27 案例，类型枚举未变）

### 关键教训

- **video_analyze 可用于 H.264 编码视频**（此前认为 DeepSeek 不支持 video_analyze，实际是 av1 编码导致 400/413 错误）
- **Android client 可绕过 YouTube bot 检测**（`--extractor-args "youtube:player_client=android"`）
- **超短片（<1分钟）合并处理效率高**：两支配对短片拆解为一个案例，技法提取聚焦「共性公式」而非逐片重复

## [0.18.0] — 2026-06-15

### 新增 — IPAD-AIR-M4 案例（iPad Air M4 × 场景融入叙事 × 紫色视觉锚点 × M4）

**案例新增：IPAD-AIR-M4 — Introducing iPad Air with M4**
- 类型：commercial（3C产品介绍片）
- 20 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：场景融入叙事, 碎片化生活蒙太奇, 产品即场景配件, 低角度日常仰视, 屏幕自发光照明, 遮挡式场景转场, 独立民谣配乐, 环境音自然融入
- 特征：1:10, 紫色iPad Air, M4芯片, Magic Keyboard, 6+场景切换, 生活即创作叙事
- 来源：YouTube 官方视频通过 vision_analyze 多帧分析（DeepSeek 不支持 video_analyze, 使用 1fps 帧提取+vision 分析替代）
- 独特价值：首个「场景融入」叙事案例（产品藏入场景而非抽离展示）、首个遮挡式转场案例、首个紫色视觉签名策略案例、与 IPHONE-AIR 形成「神圣悬浮vs生活融入」对照体系

### 新增 — IPHONE-AIR 案例（iPhone Air × 极致轻薄叙事 × 悬浮美学 × A19 Pro）

**案例新增：IPHONE-AIR — Introducing iPhone Air**
- 类型：commercial（3C产品介绍片）
- 21 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：极致轻薄叙事, 悬浮失重隐喻, 工业解剖叙事, 芯片聚光揭示, 侧剖面零度视角, 爆炸分解CGI, 芯片聚光灯渲染, 无旁白纯视觉叙事
- 特征：2:30, 800万播放, A19 Pro芯片, 无旁白, Clark "Lambent Rag" 配乐
- 来源：YouTube 官方视频通过 vision_analyze 多帧分析
- 独特价值：首个「薄即信仰」单一属性极致放大案例、首个无旁白纯视觉叙事案例、首个芯片聚光揭示（心脏揭示仪式）案例、与 IPHONE17PRO 形成「设计vs制造」对照体系

---

## [0.16.0] — 2026-06-15

### 新增 — MACBOOK-NEO 案例（MacBook Neo 产品介绍 × 解构重组叙事 × 手部交互 × $599）

**案例新增：MACBOOK-NEO — Hello, MacBook Neo**
- 类型：commercial（3C产品介绍片）
- 25+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：解构重组叙事, 价格锚点叙事, 手部交互运镜, 定格装配镜头, 零件飞入装配CGI, 图标实体化动画, 虚实手部交互合成, 四色年轻化色谱, 温暖男声旁白
- 特征：3:50, 4款配色（Citrus/Blush/Indigo/Silver）, A18 Pro芯片, 16小时续航, $599起售价, 手部占比约40%画面
- 来源：YouTube 官方视频通过 video_analyze 两轮深度分析
- 独特价值：首个入门级产品案例、首个价格锚点策略案例、首个手部交互驱动案例、首个四色年轻化策略案例

**元数据更新**
- metadata/registry.yaml：+9 行, Total files: 65→66, Phase 8: 8→9
- references/cases/INDEX.md：+1 主注册表行, +4 叙事技法, +5 镜头技法, +3 色彩技法, +5 特效技法, +4 声音技法, +4 创意广告技法, 5 风格扩充, 6 角色维度扩充
- SKILL.md：version 0.15.0→0.16.0

**统计**：案例 25→26 (film×4, commercial×18, short-film×1, music-video×1, animation×1, documentary×1)

## [0.15.0] — 2026-06-15

### 新增 — IPHONE17PRO 案例（iPhone 17 Pro 产品介绍 × 制造过程叙事 × 3C工业美学）

**案例新增：IPHONE17PRO — Introducing iPhone 17 Pro**
- 类型：commercial（3C产品介绍片）
- 25+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：制造过程叙事, 工业设计自述, 铝合金CNC微距, 内部透视运镜, 子弹时间阵列, Unibody一体成型CGI, 均热板气液循环可视化, Genlock多机位同步, 工业拟音驱动节奏, 女VP自述旁白
- 特征：3:57, 5 段落结构（制造工艺→核心性能→耐用测试→影像实战→成品展示）, Molly Anderson VP出镜解说, 3款钛金属配色
- 来源：YouTube 官方视频通过 video_analyze 两轮深度分析
- 独特价值：首个3C产品制造过程案例、首个Unibody一体成型工艺案例、首个VP真人代言案例、首个Genlock技术案例

**元数据更新**
- metadata/registry.yaml：+9 行, Total files: 64→65, Phase 8: 7→8
- references/cases/INDEX.md：+1 主注册表行, +5 叙事技法, +6 镜头技法, +3 色彩技法, +5 特效技法, +4 声音技法, +4 创意广告技法, +1 风格标签(cinematic), 4 风格扩充, 6 角色维度扩充
- SKILL.md：version 0.14.0→0.15.0, 案例 24→25

**统计**：案例 24→25 (film×4, commercial×17, short-film×1, music-video×1, animation×1, documentary×1)，新增 cinematic 风格标签 ✅

## [0.14.0] — 2026-06-15

### 新增 — PUDONG-CAT 案例（橘猫POV × Wes Anderson美学 × AI生成 × 城市文明）

**案例新增：PUDONG-CAT — 文明浦东·橘猫篇**
- 类型：commercial（城市文明宣传片）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：文明行为叙事, AI生成叙事, 韦斯安德森叙事美学, 绝对对称构图体系, 平面化运镜, 多分屏蒙太奇, 韦斯安德森马卡龙色谱, 多AI管线素材融合, 去政务化文明叙事
- 特征：1:20, 16 个场景, 全 AI 生成（Kling/Luma/Runway）, 橘猫为文明代言人, 7 次分屏蒙太奇
- 来源：本地视频文件通过 video_analyze 两轮深度分析
- 独特价值：首个 AI 生成宣传片案例、首个 Wes Anderson 美学案例、首个去政务化政府传播案例

**元数据更新**
- metadata/registry.yaml：+7 行, Total files: 63→64, Phase 8: 6→7
- references/cases/INDEX.md：+1 主注册表行, +3 叙事技法(含动物代言人/猫视角POV/地标符号化合并), +5 镜头技法, +3 色彩技法, +4 特效技法, +4 声音技法, +4 创意广告技法, +1 风格标签(whimsical), 4 风格扩充
- SKILL.md：version 0.13.0→0.14.0

**统计**：案例 23→24 (film×4, commercial×16, short-film×1, music-video×1, animation×1, documentary×1)，新增 whimsical 风格标签 ✅

## [0.13.0] — 2026-06-15

### 新增 — BJIFF-SWIFT 案例（雨燕POV × 北京地标 × 电影嵌套 × 北影节）

**案例新增：BJIFF-SWIFT — 第十六届北京国际电影节雨燕宣传片**
- 类型：commercial（电影节宣传片）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：电影嵌套叙事, 影史致敬叙事, 电影即城市, 鸟瞰雨燕POV, 胶片物理化, 建筑→电影设备变形, 片场同期声, 影院呼吸感静默, slogan延迟揭示
- 特征：1:31, 11 个场景, CG雨燕+实景融合, 红高粱/卧虎藏龙致敬, 三段式色调递进, 场记板转场
- 来源：本地视频文件通过 video_analyze 两轮深度分析
- 独特价值：首个电影节宣传片案例、首个电影嵌套叙事案例、首个CG动物+实景融合案例

**元数据更新**
- metadata/registry.yaml：+7 行, Total files: 62→63, Phase 8: 5→6
- references/cases/INDEX.md：+1 主注册表行, +3 叙事技法(含动物代言人/地标符号化合并), +5 镜头技法, +4 色彩技法, +4 特效技法, +4 声音技法, +4 创意广告技法, +1 风格标签(cinematic), 5 风格扩充
- SKILL.md：version 0.12.0→0.13.0

**统计**：案例 22→23 (film×4, commercial×15, short-film×1, music-video×1, animation×1, documentary×1)，新增 cinematic 风格标签 ✅

## [0.12.0] — 2026-06-15

### 新增 — VOLCENGINE-FL 案例（POV过山车 × 武汉地标 × 赛博国潮 × AI发布会）

**案例新增：VOLCENGINE-FL — 火山引擎 Force Link AI 创新巡展·武汉站宣传片**
- 类型：commercial（AI发布会宣传片）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：POV过山车叙事, 时空穿越叙事, 文化符号巨型化叙事, AI能力隐喻叙事, 全程POV主观镜头, 赛博国潮色谱, 全CG POV过山车管线, 国乐+EDM融合
- 特征：1:04, 13 个武汉地标场景, 全程无打断POV, 暖→冷→暖 5段色温切换, 编钟→电子递进音轨
- 来源：本地视频文件通过 video_analyze 两轮深度分析（需 ffmpeg 压缩后分析）
- 独特价值：首个全CG POV过山车案例、首个赛博国潮风格案例、首个AI发布会邀请式叙事案例

**元数据更新**
- metadata/registry.yaml：+7 行（1 案例 entry），Total files: 61→62, Phase 8: 4→5
- references/cases/INDEX.md：+1 主注册表行, +4 叙事技法(含地标符号化合并), +5 镜头技法, +4 色彩技法, +4 特效技法, +4 声音技法, +4 创意广告技法, +1 风格标签(futuristic), 6 风格扩充
- SKILL.md：version 0.11.0→0.12.0

**统计**：案例 21→22 (film×4, commercial×14, short-film×1, music-video×1, animation×1, documentary×1)，新增 futuristic 风格标签 ✅

## [0.11.0] — 2026-06-15

### 新增 — LJZ-COFFEE 案例（微缩模型 × 咖啡节 × 城市品牌叙事）

**案例新增：LJZ-COFFEE — 陆家嘴咖啡文化节十周年宣传片**
- 类型：commercial（节庆活动宣传片）
- 20+ 技法 × 5 角色维度 × 4 创意策略维度
- 核心技法：微缩城市叙事, 地标符号化, 品牌庆典叙事, 逐镜元素递增, 微缩俯拍移轴, 液体合成+微缩融合, 咖啡色谱体系, 暖色调情感霸权, 器具拟音驱动节奏
- 特征：0:37, 14 个微缩场景, 1:100-1:200 比例模型, 90% 暖色调, 无旁白纯视觉+音乐+拟音驱动
- 来源：本地视频文件通过 video_analyze 两轮深度分析创建
- 独特价值：首次收录微缩模型艺术技法、城市地标改造叙事、咖啡品类色谱体系

**元数据更新**
- metadata/registry.yaml：+7 行（1 案例 entry），Total files: 60→61, Phase 8: 3→4
- references/cases/INDEX.md：+1 主注册表行, +4 叙事技法, +5 镜头技法, +4 色彩技法, +4 特效技法, +4 声音技法, +4 创意广告技法, +1 风格标签(playful), 5 风格扩充(dreamy/colorful/heartwarming/surreal), 角色维度表全部更新
- SKILL.md：version 0.10.1→0.11.0

**统计**：案例 20→21 (film×4, commercial×13, short-film×1, music-video×1, animation×1, documentary×1)，新增 playful 风格标签 ✅

## [0.10.1] — 2026-06-15

### 新增 — LOUVRE-MAP 案例（展览宣传片 × 猫视角叙事）

**案例新增：LOUVRE-MAP — 卢浮宫×浦东美术馆「图案的奇迹」展览宣传片**
- 类型：commercial（文化展览宣传片）
- 16+ 技法 × 5 角色维度 × 2 创意策略维度
- 核心技法：动物代言人叙事, 双城蒙太奇, 反射转场(水面/玻璃), 瓷盘圆形iris转场, CG猫+实景融合, 蓝金双色色彩霸权
- 特征：1:18, 白猫串联巴黎→上海双城, 无猫叫的克制声音设计, CG+实拍+插画三层融合
- 来源：X/Twitter @Khazix0918 用户分享，视频下载后通过 video_analyze 深度分析

**元数据更新**
- metadata/registry.yaml：+9 行（1 案例 entry），Total files: 59→60
- references/cases/INDEX.md：+1 主注册表行, +5 叙事技法, +4 镜头技法, +2 色彩技法, +3 特效技法, +3 声音技法, +2 创意广告技法, +1 风格标签(elegant)
- SKILL.md：version 0.10.0→0.10.1

**统计**：案例 19→20, 新增 elegant 风格标签, 首次使用视频下载+AI分析方式创建案例 ✅

## [0.10.0] — 2026-06-15

### 新增 — Phase 8: 3 案例 × 3 新类型（music-video / animation / documentary）

**案例新增：OKGO-TOM — OK Go "The One Moment" (music-video)**
- 开 music-video 类型首例
- 17+ 技法 × 5 角色维度 × 6 创意策略维度
- 核心技法：极压时间叙事, 超高速摄影6000fps, 精密计时链318事件, 音乐可视化叙事, 零CGI全实拍
- 特征：4.2s 实时→4min 慢放, 单镜头一次性工程, 破坏即创作

**案例新增：PIPER — Pixar "Piper" (animation)**
- 开 animation 类型首例
- 17+ 技法 × 5 角色维度
- 核心技法：无对白成长叙事, 照片级渲染, 微观史诗, 羽毛SSS次表面散射, Foley替对白
- 特征：6min 无对白, 奥斯卡最佳动画短片 2017, 暖色+photorealistic 风格

**案例新增：KOYAANISQATSI — "Koyaanisqatsi" (documentary)**
- 开 documentary 类型首例
- 15+ 技法 × 5 角色维度
- 核心技法：蒙太奇即论点, 延时摄影叙事, Philip Glass极简主义配乐, 无主角史诗叙事, 工业vs自然对立
- 特征：86min 无对白无旁白, 纯影像+音乐, 1982年胶片纯实拍

**元数据更新**
- metadata/registry.yaml：+24 行（3 案例 entries），Total files: 56→59
- references/cases/INDEX.md：+3 主注册表行, +13 叙事技法, +11 镜头技法, +8 色彩技法, +9 特效技法, +9 声音技法, +2 创意广告技法, +5 风格标签, 角色维度表全部更新
- SKILL.md：version 0.9.0→0.10.0

**统计**：案例 16→19 (film×4, commercial×11, short-film×1, music-video×1, animation×1, documentary×1)，类型 5/8→8/8 全覆盖 ✅

### 新增 — Phase 9: 阶段门禁验证系统

**metadata/phase_gates.yaml — 门禁规则声明**
- 6 个阶段的进入条件（phase_2 ~ phase_7）
- 每个阶段定义：requires_approved_sections（前置 section 的 _meta.director_approved 链）、required_fields（硬门禁）、warn_if_empty（软提醒）
- 声明式 YAML，validate_state.py 的规则源

**scripts/validate_state.py — 门禁验证脚本**
- CLI 工具：`python scripts/validate_state.py --input <project-state.json> --phase <2-7> [--quiet]`
- 检查内容：section 审批链完整性、必填字段非空、建议字段提醒、storyboard panel 审批完整性（phase_7）
- 输出格式：Agent 可操作的结构化输出（BLOCKERS / WARNINGS / INFO 分层）
- 退出码：0=PASS（可进入阶段），1=BLOCKED（需修复前置阶段）

**references/pipelines/default.md — 管线文档更新**
- Phase 2-7 的「操作序列」各加第 0 步：门禁检查
- 阻塞时指明返回到哪个前置阶段修复
- Phase 7 的门禁替代了原来手动的 `_meta.director_approved` checklist（第 1 步保留作为双重确认）

**元数据更新**
- metadata/registry.yaml：+2 行（phase_gates.yaml + validate_state.py），Total files: 54→56
- metadata/dependencies.yaml：+2 对依赖关系（phase_gates→validate_state / schema→validate_state），default.md 的 downstream 新增 phase_gates.yaml

### 影响范围
- 新增文件：metadata/phase_gates.yaml、scripts/validate_state.py（2 个）
- 修改文件：metadata/registry.yaml、metadata/dependencies.yaml、references/pipelines/default.md、metadata/CHANGELOG.md（4 个）
- 下游影响：无。validate_state.py 是纯读数工具，不修改任何现有文件。

### 迁移指南
- 无需迁移。两个示例 project-state.json 均已通过全部阶段的验证（exit_code=0）。
- 管线执行中新增强制的门禁步骤，Agent 需在进入 Phase 2-7 前先运行验证脚本。

---

## [0.8.1] — 2026-06-12

### 文档增强 — README + 生图指南 + 工具矩阵

**README.md — 新增场景覆盖简介**
- 在「工作流」与「案例库」之间新增「覆盖场景」表
- 覆盖 5 种场景：棚拍广告 / 产品演示 / LOGO 演绎 / 科幻设定 / 艺术短片(自定义)
- 每种场景标注定位 + 一句话 + 场景文档引用

**image-gen-guide.md — 新增主流模型基准**
- 工具速查表新增：ChatGPT Image (GPT-4o)、NanoBanana (Google)、即梦 (Jimeng)
- 适用工具头部更新，覆盖现有 7 种工具

**tool-matrix.md — 工具能力总览扩展**
- 新增 4 个国产/新兴工具：LibTV (liblib.tv)、TAPNOW、即梦 (Jimeng)、happyhorse (阿里快马)
- 覆盖工具头部从 6 个扩展至 10 个

### 影响范围
- README.md (+14 行)
- references/media/image-gen-guide.md (+3 行，header 更新)
- references/media/tool-matrix.md (+4 行，header 更新)

## [0.8.0] — 2026-06-12

### 新增 — Phase 7: 国际标杆广告案例扩充（优先级 2，4 个案例）

**Honda — `references/cases/HONDA-COG.md` (330+ 行)**
- Antoine Bardou-Jacquet 执导，84 个 Accord 零件零 CGI 实拍的工程史诗
- 16+ 技法 × 5 角色维度：连锁反应叙事 / 产品零件即角色 / 多米诺悬念结构 / 606次概率管理 / 微距追踪 / 机械打击乐 / 无配乐无旁白 / 声音饥饿策略 / 零件即品牌 / 信息自我发现
- 5 场景色调对照表（纯白极简空间） + 606次实拍概率管理技术 + 信息自我发现品牌策略
- 填补盲区：🎯 鲁布·戈德堡机械型广告（全库首个）

**Guinness — `references/cases/GUINNESS-SURFER.md` (370+ 行)**
- Jonathan Glazer 执导，纯隐喻广告的绝对巅峰——被票选为「史上最佳广告」
- 17+ 技法 × 5 角色维度：品牌隐喻叙事 / 等待即叙事 / 完全无产品 / Moby Dick 式文学旁白 / 黑白史诗摄影 / 浪头即角色 / 巨浪微人对比 / 黑暗电子驱动(Leftfield) / 旁白节奏化 / 三重普遍性策略 / 突破品类惯例
- 5 场景色调对照表（纯黑白银盐美学） + 浪中白马VFX + 声音三级弧线
- 填补盲区：🎯 纯隐喻无产品广告（全库首个） / 🎯 黑白广告美学（全库首个）

**Apple — `references/cases/APPLE-1984.md` (400+ 行)**
- Ridley Scott 执导，超级碗一次性播出的品牌宣言革命——定义了 Apple 未来 40 年的品牌定位
- 17+ 技法 × 5 角色维度：反乌托邦叙事 / 品牌宣言结构 / 敌我冲突模型 / 英雄之旅压缩 / 工业科幻美学 / 队列vs个体构图 / Big Brother超尺度 / 铝热剂爆炸实拍 / 工业drone压迫 / 旁白神谕模式 / 一次性播出策略 / 品牌神话构建
- 5 场景色调对照表（蓝灰反乌托邦+白色红色自由符号） + 1984年纯实拍VFX + 敌我冲突reframe策略
- 填补盲区：🎯 品牌宣言型广告（全库首个） / 🎯 超级碗一次性播出策略（全库首个）

**IKEA — `references/cases/IKEA-LAMP.md` (380+ 行)**
- Spike Jonze 执导，反广告的广告——前半段让观众为一盏台灯心碎，后半段嘲笑这种情感
- 16+ 技法 × 5 角色维度：物的人类化 / 情感反转陷阱 / 反广告叙事 / 诗意→讽刺调性切换 / POV台灯视角 / 雨夜情绪摄影 / 无特效即特效 / 极情绪钢琴硬切断 / 理性dry旁白 / 反广告的广告 / 消费主义自嘲 / 第四面墙温和爆破
- 5 场景色调对照表（冷蓝雨夜vs暖黄室内） + 音乐硬切断「情感→理性」过渡 + 消费主义自嘲策略
- 填补盲区：🎯 反广告/元广告（全库首个） / 🎯 物的人类化叙事（全库首个） / 🎯 Spike Jonze 导演双案例（与 APPLE-WH 形成风格对比）

### 变更 — INDEX.md + registry 全表同步

- 主注册表：+4 行（16 案例总计）
- 叙事技法表：+17 条目 → 共 55 条目
- 镜头语言表：+15 条目 → 共 54 条目
- 色彩/美术表：+10 条目 → 共 37 条目
- 特效语言表：+9 条目 → 共 38 条目
- 声音设计表：+12 条目 → 共 40 条目
- 创意广告表：+13 条目 → 共 33 条目
- 场景→案例表：sci-fi/studio-ad/product-demo 增强（+4 案例）
- 风格/情绪表：+poetic 标签 + melancholic/surreal 案例增强 → 共 17 标签
- 角色维度表：6 角色全部更新，每个角色必看案例增至 11-12 个

### 4 案例盲区覆盖总览

| 盲区 | 案例 | 独特性 |
|------|------|--------|
| 鲁布·戈德堡机械广告 | HONDA-COG | 零CGI 606次实拍 + 84零件连锁 |
| 纯隐喻无产品广告 | GUINNESS-SURFER | 史上最佳广告 + 黑白冲浪史诗 |
| 品牌宣言型广告 | APPLE-1984 | 超级碗一次性播出 + 定义Apple40年 |
| 反广告/元广告 | IKEA-LAMP | 情感反转陷阱 + 第四面墙温和爆破 |

### 案例总数里程碑：8 → 12 → 16

Phase 6: 8 案例 → Phase 7-P1: 12 案例 → Phase 7-P2: 16 案例（翻倍完成）

---

## [0.7.0] — 2026-06-12

### 新增 — Phase 7: 国际标杆广告案例扩充（4 个案例文件，优先级 1）

**Old Spice — `references/cases/OLDSPICE-MAN.md` (230+ 行)**
- Tom Kuntz 执导，33 秒单镜头喜剧广告的病毒革命
- 14+ 技法 × 5 角色维度：无缝口头转场 / 打破第四面墙 / 荒诞逻辑链 / 喜剧节奏公式(1笑点/3s) / 连续单镜头错觉 / 身体即产品载体 / 男中音旁白节奏 / 荒诞夸大策略 / 病毒一句话公式
- 5 场景色调对照表(纯白浴室→金色海滩) + 帧匹配转场缝合技术 + 幽默推销3步模型
- 填补盲区：🎯 喜剧/幽默广告（全库首个）

**John Lewis — `references/cases/JOHNLEWIS-PENGUIN.md` (250+ 行)**
- Dougal Wilson 执导，2 分钟圣诞情感叙事的标杆
- 15+ 技法 × 5 角色维度：情感蓄力结构(90%积累→5%释放) / 儿童视角 / 反转结局3步释放 / 非人类情感代言 / CGI企鹅动画+实拍融合 / 翻唱编排策略 / 无对白音乐叙事 / 静默品牌登场
- 5 场景色调对照表(深木色暖家→金色晨光释放) + 灯光匹配HDRI技术 + 品牌隐形策略
- 填补盲区：🎯 长叙事情感广告（全库首个）

**Sony Bravia — `references/cases/SONY-BALLS.md` (230+ 行)**
- Nicolai Fuglsig 执导，25 万颗弹力球零 CGI 实拍的视觉革命
- 14+ 技法 × 5 角色维度：无叙事纯视觉 / 产品隐喻4步递进 / Show-Don't-Tell极致 / 超高速摄影1000fps / 广角全景23机位 / 色彩光谱编排 / 零CGI实拍调度 / 音乐反差策略(Heartbeats) / 纯隐喻型广告
- 6 场景色调对照表(灰色街景→光谱色带) + 歌曲去电子化改编公式
- 填补盲区：🎯 视觉奇观型广告（全库首个）

**Volvo Trucks — `references/cases/VOLVO-SPLIT.md` (240+ 行)**
- Andreas Nilsson 执导，Van Damme 在两台倒行卡车间劈叉
- 15+ 技法 × 5 角色维度：极简信息设计(3信息点) / 产品演示即叙事 / 一镜到底航拍 / 对称史诗构图 / 黎明金色时刻 / Enya音乐反差 / 极限信任证明 / 病毒一句话公式
- 4 场景色调对照表(三色极简：金色/灰色/银色) + 信息层频谱分离音频 + 产品演示即表演模型
- 填补盲区：产品演示型广告的「表演化」升级

### 变更 — INDEX.md + registry 全表同步

- 主注册表：+4 行（12 案例总计）
- 叙事技法表：+15 条目 → 共 38 条目
- 镜头语言表：+14 条目 → 共 39 条目
- 色彩/美术表：+13 条目 → 共 27 条目
- 特效语言表：+12 条目 → 共 29 条目
- 声音设计表：+13 条目 → 共 28 条目
- 创意广告表：+14 条目 → 共 20 条目
- 场景→案例表：studio-ad/product-demo 增强（+4 案例）
- 风格/情绪表：+humorous + absurd + heartwarming → 共 15 标签
- 角色维度表：6 角色全部更新，每个角色必看案例增至 7-9 个

### 盲区覆盖率

| 盲区类型 | Phase 6 | Phase 7 | 状态 |
|---------|---------|---------|------|
| 喜剧/幽默广告 | 0 | 1 (OLDSPICE-MAN) | ✅ 已覆盖 |
| 长叙事情感广告(60-120s) | 0 | 1 (JOHNLEWIS-PENGUIN) | ✅ 已覆盖 |
| 视觉奇观型广告(纯CG/特殊摄影) | 0 | 1 (SONY-BALLS) | ✅ 已覆盖 |
| 品牌宣言型 | 1 (部分) | 1 (NIKE-YCS) | ⚠️ 部分覆盖 |
| 病毒/社交传播型(≤30s) | 0 | 1 (OLDSPICE-MAN) | ✅ 已覆盖 |

### 统计

| 指标 | Phase 6 | Phase 7 | 增量 |
|------|---------|---------|------|
| 总案例数 | 8 | 12 | +4 |
| 广告案例 | 3 | 7 | +4 |
| 总文件数 | 46 | 50 | +4 |
| 覆盖角色维度 | 5/5 | 5/5 | — |
| 索引表数量 | 10 | 10 | — |

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`, `references/cases/INDEX.md`
- 新增文件：4 个（OLDSPICE-MAN.md / JOHNLEWIS-PENGUIN.md / SONY-BALLS.md / VOLVO-SPLIT.md）
- 下游影响：SKILL.md 路由表无需修改（INDEX.md 交叉引用自动生效）

### 迁移指南

- 无需迁移。所有 Phase 0-6 文件保持不变，Phase 7 为纯增量。
- 4 个案例文件均按 `_TEMPLATE.md` 格式，≥200 行 / ≥12 技法 / 5 角色维度全覆盖。

---

## [0.6.0] — 2026-06-12

### 新增 — Phase 6: 硬核电影案例扩充（3 个案例文件）

**花样年华 — `references/cases/WKW-ML.md` (240+ 行)**
- 王家卫美学终极标本，15+ 技法 × 5 角色维度
- 核心技法：留白叙事 / 重复结构 / 框架构图(偷窥视角) / 慢快门步印 / 旗袍色彩叙事 / 音乐锚点
- 7 场景色调对照表 + 23 套旗袍→情绪映射系统 + 墙纸视觉密度分析
- 填补盲区：艺术电影类型首次纳入案例库

**流浪地球 — `references/cases/WANDERING-E.md` (250+ 行)**
- 中国硬核科幻工程美学标杆，16+ 技法 × 5 角色维度
- 核心技法：集体英雄主义 / 巨物尺度公式(人 1.8m→地球 12,742km) / 五域色调体系 / 行星发动机火焰 VFX / 低频嗡鸣次声波
- 6 场景色调对照表 + 地下城烟火气设计哲学 + Boids 运载车集群
- 填补盲区：中国科幻美学首次纳入案例库（区别于西方赛博朋克）

**环太平洋 — `references/cases/PACIFIC-RIM.md` (260+ 行)**
- Guillermo del Toro 巨型机甲标杆，16+ 技法 × 5 角色维度
- 核心技法：双人共驾 Drift 系统 / 重量感运动公式(2-3s 惯性缓冲) / 霓虹雨夜色调 / 机械物理模拟 / 关节专属声音设计
- 5 场景色调对照表 + 「熟悉+陌生」怪兽设计原则 + 雨水粒子系统三层架构
- 填补盲区：巨型机甲/物理重量感类型首次纳入案例库

### 变更 — INDEX.md 全表同步

- 主注册表：+3 行 (8 案例 总计)
- 叙事技法表：+12 条目 → 共 23 条目
- 镜头语言表：+12 条目 → 共 25 条目
- 色彩/美术表：+8 条目 → 共 14 条目
- 特效语言表：+10 条目 → 共 17 条目
- 声音设计表：+9 条目 → 共 15 条目
- 场景→案例表：+custom (art-film) + sci-fi/logo-animation 增强
- 风格/情绪表：+nostalgic + melancholic + cyberpunk-adjacent → 共 12 标签
- 角色维度表：5 角色全部更新，每个角色必看案例增至 4-5 个

### 统计

| 指标 | Phase 5 | Phase 6 | 增量 |
|------|---------|---------|------|
| 总案例数 | 5 | 8 | +3 |
| 电影案例 | 1 | 4 | +3 |
| 总文件数 | 43 | 46 | +3 |
| 覆盖角色维度 | 5/5 | 5/5 | — |
| 索引表数量 | 8 | 10 | +2 |

---

## [0.5.0] — 2026-06-12

### 新增 — Phase 5: 案例库扩充（4 个案例文件）

**Apple Welcome Home — `references/cases/APPLE-WH.md` (219 行)**
- Spike Jonze 为 Apple HomePod 执导的标杆级广告片
- 14 项技法 × 5 角色维度：无对白叙事 / 身体驱动转场 / 单镜头错觉缝合 / 空间扭曲跟拍 / 360° 环绕运动 / 物理空间拉伸 VFX / 镜像无限反射 / 色彩渗入转场 / 音乐驱动节奏 / 环境音景空间定位 / 产品隐形植入 / 艺术家背书 / 感官替代功能
- 6 场景色调对照表（灰→黄→蓝→粉→彩→灰）

**Nike You Can't Stop Us — `references/cases/NIKE-YCS.md` (217 行)**
- Oscar Hudson 执导，24 名运动员 × 36 种运动 × 53 组分屏匹配
- 14 项技法 × 5 角色维度：隐喻剪辑 / 无旁白累积 / 集体叙事 / 分屏匹配几何精度 / 档案素材统一化 / 动态节奏数学设计 / 分屏匹配隐藏艺术 / 动态节奏变速 / 声画对位 / 静默爆发 / 品牌精神替代产品展示 / 集体共鸣 / 蓄力结构
- 5 场景色调对照表 + 详细时间轴节奏参数

**Apple Don't Blink — `references/cases/APPLE-DB.md` (226 行)**
- Apple 2019 年终产品回顾，107 秒展示 80+ 功能点
- 13 项技法 × 5 角色维度：功能叙事 / 极简旁白子弹规则 / 密度递增 S 曲线 / 高速剪辑第一帧即最终帧 / 产品密度空间 / 微距功能视觉化 / UI 标注叠加 / 产品极速转场 / 节奏递增音频 / 产品声音符号化 / 产品密度=竞争力 / 节奏递增心理操控 / 证明-不解释
- 5 场景色调对照表 + 功能→画面映射公式

**Cosmos Laundromat — `references/cases/COSMOS-L.md` (225 行)**
- Blender Foundation 开源短片，暖色科幻的自然光革命
- 14 项技法 × 5 角色维度：环境叙事 / 非人类主角情感 / 无对白情感渐进 / 自然光模拟 CG 革命 / 巨物尺度对比 / 微距材质凝视 / 虚拟摄影机物理感 / 材质渲染物理真实性 / 光传输模拟 / 体积光效情绪 / 异世界音景 / 音乐情感引导 / 材质声音地图
- 7 场景色调对照表（从「绿色牢笼」到「蓝色自由」）

### 修改

- `SKILL.md`：版本号 0.4.0 → 0.5.0
- `metadata/registry.yaml`：4 个案例文件 status=complete，Phase 5 统计；总文件数 39→43
- `references/cases/INDEX.md`：最后更新日期标注 Phase 5 完成状态

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`, `references/cases/INDEX.md`
- 新增文件：4 个（APPLE-WH.md / NIKE-YCS.md / APPLE-DB.md / COSMOS-L.md）
- 下游影响：SKILL.md 路由表无需修改（INDEX.md 交叉引用已在 Phase 1 完成）；场景文档中的案例引用表已预填这些案例 ID

### 迁移指南

- 无需迁移。所有 Phase 0-4 文件保持不变，Phase 5 为纯增量。
- 4 个案例文件均按 `_TEMPLATE.md` 格式，与 BR2049.md 同深度标准，可直接被 Agent 引用。

---

## [0.4.0] — 2026-06-12

### 新增 — Phase 4: 示例项目（2 个示例，16+ 文件）

**完整棚拍广告案例 —「光影之间」**
- `assets/examples/studio-ad-full/README.md`：创意 brief + 管线执行记录 + 产出清单 + 脚本再生指南
- `assets/examples/studio-ad-full/project-state.json`：完整 Project State JSON（5 场景 + 7 分镜，27KB，所有 `_meta.director_approved=true`）
- 脚本产出：`script.md` / `storyboard.md` / `creative-pack.json` + `.md` / `studio-ad-literary.html` + `-storyboard.html` / `tech-breakdown.xlsx`
- 创意特征：减法灯光哲学（BR2049 单一光源）+ 材质叙事（8微距剪辑）+ 沉默对白（仅4字旁白）+ 光传递转场 + 金色粒子首尾呼应

**完整科幻短片案例 —「最后的记忆贩」**
- `assets/examples/sci-fi-short/README.md`：创意 brief + 管线执行记录 + BR2049 技法映射表 + 产出清单
- `assets/examples/sci-fi-short/project-state.json`：完整 Project State JSON（8 场景 + 8 分镜 + 1 角色，53KB，所有 `_meta.director_approved=true`）
- 脚本产出：`script.md` / `storyboard.md` / `creative-pack.json` + `.md` / `sci-fi-literary.html` + `-storyboard.html` / `tech-breakdown.xlsx`
- 创意特征：BR2049 全景式致敬——12 项技法直接继承（沉默对白/信息释放节奏/巨物尺度对比/单一光源/环形构图/dolly克制/场景色调对照/粒子氛围/全息不完美/巨物缓动/工业环境音/爆发式巨响）
- 角色设计：Kael（记忆贩）— 面部仅在 2 个镜头中完全展示（叙事手段）

### 修改

- `SKILL.md`：版本号 0.3.0 → 0.4.0
- `metadata/registry.yaml`：2 个示例文件 status not_started→complete，BR2049 依赖补充；Phase 4 统计更新

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 新增文件：10 个（2 个 README + 2 个 project-state.json + 6 个补充产出文件）
- 下游影响：无（所有新文件均为新建，不修改已有 Phase 0-3 文件）

### 迁移指南

- 无需迁移。Phase 0-3 的所有文件保持不变。
- 两个示例项目均可独立运行：进入对应目录，按 README.md 中的「脚本再生」命令重新生成所有产出。

---

## [0.3.0] — 2026-06-12

### 新增 — Phase 3: 脚本+模板+导出（12 个文件）

**Markdown 模板（3 个）**
- `assets/templates/script.md`：剧本 Markdown 模板，含场景分解、技术备注、元信息节
- `assets/templates/storyboard.md`：分镜 Markdown 模板，支持 2×3/3×3 网格，含 AI 提示词+审核状态
- `assets/templates/creative-pack.md`：创作包 Markdown 模板，完整 10 节结构（项目概要→下游工具对接）

**核心脚本（3 个）**
- `scripts/format_script.py`：scene array → 好莱坞剧本格式。schema-driven，支持 {{#each}} 遍历和 {{#if}} 条件块，CLI 支持 --input/--output/--template
- `scripts/storyboard_grid.py`：storyboard array → 2×3/3×3 网格 Markdown。自动选择网格布局（≤6→2×3，≤9→3×3），支持 --grid 强制覆盖
- `scripts/prompt_assembler.py`：完整 Project State → Creative Pack JSON + Markdown。自动生成 ComfyUI/HyperFrames/Kling/Runway 下游工具配置

**导出脚本（3 个）**
- `scripts/export_html.py`：Project State → 文学剧本 HTML（Courier 标准格式）+ 分镜展示 HTML（卡片网格，支持 dark mode）
- `scripts/export_xlsx.py`：Project State → 分镜技术表 Excel（多 Sheet：分镜表/项目概要/色调方案/特效清单/声音方案），依赖 openpyxl
- `scripts/moodboard_compare.py`：2+ 视觉方向 → 对比矩阵（色调对比/风格参考/相似度分析/推荐方向）

**导出模板（3 个）**
- `assets/templates/export/script-literary.html`：文学剧本 HTML 模板，Courier Prime 字体，标准剧本页边距，支持打印优化
- `assets/templates/export/script-storyboard.html`：分镜展示 HTML 模板，响应式卡片网格，含图片占位、审核状态徽章
- `assets/templates/export/script-tech.xlsx`：Excel 模板定义（JSON 驱动），5 个 Sheet 的列/行定义、条件格式、全局样式

### 修改

- `SKILL.md`：版本号 0.2.0 → 0.3.0
- `metadata/registry.yaml`：12 个文件 status not_started→complete；Phase 3 统计更新

### 影响分析

- 受影响的文件：`SKILL.md`, `metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 新增依赖：format_script.py/storyboard_grid.py → templates/script.md/storyboard.md；prompt_assembler.py → templates/creative-pack.md
- 下游影响：无（所有新文件均为新建，不修改已有文件）

### 迁移指南

- 无需迁移。Phase 0-2 的所有文件保持不变。
- export_xlsx.py 需要 `pip install openpyxl`（仅在使用 Excel 导出时需要）

---

## [0.2.0] — 2026-06-12

### 新增 — Phase 2: 角色+场景+管线+媒体（16 个文件）

**管线文档（2 个）**
- `references/pipelines/default.md`：标准 7 阶段管线。每阶段的角色激活表、输入/输出定义、Director 审核触发条件、loop 规则（≤2 轮）、角色激活矩阵
- `references/pipelines/fast-track.md`：快速 3 阶段管线。阶段合并策略（2+3+4→一稿过）、并行执行规则、自动降级条件

**角色文档（6 个）**
- `references/roles/director.md`：Vision 模板（7 个确认项）、审核标准（APPROVE/REVISE/REJECT 判定条件）、迭代策略（≤2 轮 loop）、拍板话术（4 种场景）
- `references/roles/writer.md`：叙事结构库（6 种：三段式/英雄之旅/蒙太奇/问题-解决/反转/情绪递进）、对白技巧、情绪节奏公式、logline 模板
- `references/roles/dp.md`：镜头语言词汇表（8 种 shot types + 11 种 movements + 6 种 lens choices）、灯光方案模板、构图网格（9 种）、运镜决策树
- `references/roles/art-director.md`：情绪→色调映射表（10 种情绪）、风格库（6 种：minimalist/cyberpunk/warm-cinematic/cold-dystopian/dreamy-surreal/gritty-realism）、人物造型 checklist、世界观构建模板
- `references/roles/vfx.md`：材质库（固体/流体/粒子/发光 4 大类 25+ 材质，含 PBR 参数）、转场类型表（12 种+决策树）、合成层级模板、CG vs 实拍判断流程图
- `references/roles/sound-designer.md`：配乐风格库（13 种，含 tempo+instrumentation）、音效分类体系（6 类）、旁白基调选择器、静默部署策略（BR2049 式声音层次）、参考曲目搜索关键词

**场景文档（4 个）**
- `references/scenes/studio-ad.md`：灯光方案（三点布光+减法灯光）、机位模板（5 机位）、道具清单、演员调度、提示词模板。引用 APPLE-WH/APPLE-DB/BR2049
- `references/scenes/product-demo.md`：功能→镜头映射、B-roll 配比公式（按片长）、CTA 时机决策、3 种叙事模板。引用 APPLE-DB/NIKE-YCS/COSMOS-L
- `references/scenes/sci-fi.md`：世界观规则模板、科技一致性检查清单（6 项）、异化美感参数（7 策略+3 强度）、提示词模板。引用 BR2049/COSMOS-L
- `references/scenes/logo-animation.md`：材质-品牌关联表（8 种）、三阶段节奏模型、动态参数速查、品牌色精确匹配规则。引用 NIKE-YCS/APPLE-WH/BR2049

**媒体参考（3 个）**
- `references/media/image-gen-guide.md`：ComfyUI/Flux/SDXL/SD1.5 的 prompt 模板（4 种场景）、参数速查、负面提示词策略、质量检查清单
- `references/media/character-consistency.md`：6 种策略矩阵（种子固定/IP-Adapter/FaceID/LoRA/参考图重投/ControlNet）、诚实能力边界标注、推荐组合策略、用户诚实标注模板
- `references/media/tool-matrix.md`：ComfyUI vs HyperFrames vs Kling vs Runway vs Pika vs Suno 的选择决策树、Creative Package→工具输入映射、成本-质量权衡

### 修改

- `metadata/registry.yaml`：16 个文件 status not_started→complete；修复 default.md↔director.md 的循环依赖（default.md 不再依赖 director.md）

### 影响分析

- 受影响的文件：`metadata/registry.yaml`, `metadata/CHANGELOG.md`
- 受影响的依赖：`SKILL.md` 的 dependents 列表（pipeline + role + scene + media 文件均已就绪）
- 下游影响：无（所有新文件均为新建，不修改已有文件）

### 迁移指南

- 无需迁移。Phase 0-1 的所有文件保持不变。

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
