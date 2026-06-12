# 光影之间 — Creative Pack

> **Muse Video Skill 创作包**
> 本文件是完整的视频前期策划产出，包含剧本、分镜、美术方向、声音设计和下游工具提示词。
> 可导入 ComfyUI / HyperFrames / Kling / Runway 等下游工具执行制作。

---

<!--
  模板说明：
  - 本模板由 prompt_assembler.py 读取并填充。
  - 完整的 Project State JSON → Creative Pack Markdown。
  - 所有节映射到 Project State JSON 的顶层字段。
-->

## 1. 项目概要

| 项目 | 内容 |
|------|------|
| **标题** | 光影之间 |
| **类型** | studio-ad |
| **画幅** | 16:9 |
| **预估时长** | 30s |
| **风格** | luxury-minimalist |
| **平台** | all-platform |
| **语种** | zh-CN |

---

## 2. 导演阐述

> **Vision**：一支30秒的奢侈品级智能手表棚拍广告。用极简主义的灯光和构图，将产品从「科技配件」提升为「腕间艺术品」。核心视觉策略：减法灯光+高反差+液态金属流动感。每一帧都是精心设计的静物画，产品在光影交替中展现材质之美。

| 维度 | 内容 |
|------|------|
| **情绪基调** | 冷静、高级、克制、未来感 |

### 创作约束

- 产品LOGO必须在前3秒出现

- 全片不使用CGI——所有效果通过实拍灯光+微距实现

- 背景始终保持纯黑或深灰，产品是唯一视觉焦点

- 结尾品牌落版3秒


### 关键决策

- **Phase phase2**：5场景线性叙事：悬念→材质→功能→佩戴→品牌（理由：奢侈品广告遵循'渴望累积'逻辑）

- **Phase phase3**：色调方案：深黑(#0D0D0D)+暖金(#C8A96E)+冷蓝(#4A7FA5)，参考BR2049华莱士总部的金色水面底光（理由：暖金传达奢华，冷蓝传达科技，深黑提供画布）

- **Phase phase4**：DP使用90%静态镜头+极缓dolly推进，全片只有1个手持镜头（理由：BR2049式克制运动，让观众的注意力完全在产品上）


---

## 3. 剧本

> **Logline**：一道光线划过暗夜，唤起一支腕表的觉醒——从材质到功能，从佩戴到身份，光影之间，时间有了形状。
> **叙事结构**：5场线性叙事（悬念→材质→功能→佩戴→品牌）

### 场景分解



#### 第 1 场 — 暗夜初醒（5s）

**地点**：摄影棚——黑背景，产品旋转台 · **时间**：无时间概念（纯黑环境）

**动作**：全黑画面。一束极细的金色侧光从画面右上方缓缓扫入，像黎明第一道光。光触及表盘的边缘，金属边框折射出第一道暖金色光芒。表盘缓缓旋转10°，光追随之。背景粒子（金色微尘）开始缓慢漂浮。

**对白**：（无对白）

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| 极端特写（表盘局部） | 静态——极缓dolly推进（20秒内推进15%） | 100mm微距镜头 | 单一金色侧光（模拟BR2049华莱士总部金色水面底光），无辅光——画面90%是纯黑 | 金色微尘粒子漂浮（模拟BR2049式粒子氛围） | 极低频嗡鸣（模拟BR2049工业环境音），音量从无渐入 |



#### 第 2 场 — 材质交响（8s）

**地点**：摄影棚——多光源细节拍摄台 · **时间**：无时间概念

**动作**：快速剪辑序列（8个微距镜头，每个1秒）：
① 表冠的拉丝纹理（顶光硬光）→ ② 表带的皮革毛孔（侧光柔光）→ ③ 蓝宝石玻璃的倒角边缘（逆光折射）→ ④ 表扣的抛光镜面（环形光）→ ⑤ 表盘的太阳纹（旋转底光）→ ⑥ 指针的夜光涂层（紫外光激发）→ ⑦ 背透机芯的齿轮（顶光微距）→ ⑧ 整体45°展示面（Hero Shot）。
每个镜头切换时，光从一个材质「传递」到下一个材质，形成视觉流。

**对白**：（无对白，仅音效）

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| 微距大特写（每个镜头都针对特定材质）→ 最后Hero Shot为中景 | 静态（8个镜头）→ 极缓dolly推进（Hero Shot） | 100mm微距镜头（微距）+ 50mm（Hero Shot） | 按材质切换灯光：拉丝金属=侧顶硬光 / 皮革=大型柔光箱 / 玻璃=逆光+反光板 / 抛光=环形柔光 / 夜光=UV灯+全黑 | 镜头之间的光传递转场——上一个镜头的光源方向延续到下一个镜头的第一个1/3秒 | 每切换一个材质，对应一个清脆的金属/皮革/玻璃音效（ASMR级别），叠加在持续的低频嗡鸣上 |



#### 第 3 场 — 功能觉醒（7s）

**地点**：摄影棚——产品使用场景模拟台 · **时间**：无时间概念

**动作**：表盘从息屏到亮屏的完整过程（2.5秒慢动作）：
微弱的呼吸灯在表盘边缘亮起→屏幕从中心渐变点亮→AMOLED纯黑背景下，时间数字以优雅的无衬线字体浮现→表盘显示心率监测动画（一道红色光波扫过屏幕）。
随后（4.5秒）：手指从画面外伸入，轻触表盘——屏幕响应触控，切换到消息通知界面。指尖与玻璃的接触点有微弱的静电感光效。

**对白**：（无对白）

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| 从极端特写（息屏状态，占画幅80%）拉远至中景（手指触控，占画幅40%） | 极缓dolly拉远 | 100mm微距→50mm | 息屏阶段保持纯黑+表盘边缘微弱的呼吸光。亮屏后以屏幕本身的光源作为唯一主光（面光），辅以极弱的背面轮廓光分离表盘与黑色背景。手指入画后增加一个顶部的柔光箱（模拟天然光源） | AMOLED屏幕光芒效果（纯黑下的像素级发光），触控静电光效（微弱蓝白色电弧），心率监测红色光波动画 | 息屏→亮屏：渐强的电子合成器pad（模拟Vangelis CS-80音色）。亮屏瞬间：一声清脆的'叮'（类似Mac开机声但更低频）。心率监测：低频心跳声叠加。手指触控：一声轻微的点击+触觉反馈嗡嗡声 |



#### 第 4 场 — 腕间艺术（7s）

**地点**：摄影棚——腕部佩戴拍摄台（演员的手腕） · **时间**：无时间概念

**动作**：演员的手腕从画面下方缓缓升起（慢动作），手表已佩戴好。手腕旋转——先展示表盘正面（面向镜头），再缓慢旋转至侧面（展示表冠），最后回到正面静止。
演员的袖口是深灰色精纺羊毛西装——与表盘的深黑形成微妙层次。手腕的动作优雅而克制，像古典芭蕾的手部姿势。
最后1.5秒：手腕静止，表盘在画面正中。一束金色顶光落下，照亮整支表。

**对白**：（无对白）

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| 中特写（手腕+手表占画幅50%）→ 近特写（手表占画幅70%） | dolly极缓推进（7秒内从50%→70%）+ 0.5秒静态收尾 | 85mm人像镜头 | 大型柔光箱从顶部45°角下打（模拟天窗自然光），辅以侧面的金色反光板（暖调补充）。演员手腕下方有一块小型白色反光板消除下巴阴影。深灰袖口与黑背景之间用极弱的背面轮廓光分离 | 演员腕部的柔和光晕（模拟高质感广告中的'皮肤辉光'），手表金属边框的微反射——映出摄影棚柔光箱的虚化倒影 | 持续的低频pad逐渐加入弦乐群（大提琴+低音提琴），营造'佩戴仪式感'。0:20处加入一声极轻微的布料摩擦声（袖口与表带接触） |



#### 第 5 场 — 品牌落版（3s）

**地点**：摄影棚——正面Hero Shot + 品牌LOGO · **时间**：无时间概念

**动作**：手表从45°展示面缓缓旋转至完全正面（Hero Shot），旋转过程中金色粒子从中涌出并在表盘周围形成环绕的光轨。旋转完成后，手表静止在画面正中。品牌LOGO从表盘上方以淡入方式浮现（小字号，下方配品牌标语）。画面保持1秒后淡出至黑。

**对白**：旁白（低沉男声，中文）：'光影之间。'（仅4个字）

| 镜头 | 运镜 | 焦段 | 灯光 | 特效 | 声音 |
|------|------|------|------|------|------|
| Hero Shot——正面微俯中景 | 静态（产品旋转由转台完成，摄影机不移动） | 50mm标准镜头 | 三点布光（经典广告落版）：主光=正面偏上大型柔光箱（柔光），辅光=两侧反光板（消除阴影），轮廓光=背面两个聚光灯+蜂巢（分离产品与深灰背景）。所有光源色温统一5600K，保持产品色彩中性 | 金色粒子环绕光轨（3D粒子系统——在ComfyUI/HyperFrames中实现），LOGO淡入动画（0.5秒），画面暗角效果 | 音乐在落版前0.5秒达到情绪高点（大提琴+合成器pad的和声峰值），旁白说完后音乐立即收束——留0.5秒纯环境音+粒子音效，然后静默淡出 |



---

## 4. 视觉开发

> **视觉基调**：冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。

### 色调方案

| `#0D0D0D` | **深渊黑** | primary bg —— 所有场景的背景色，提供无限深的画布 |

| `#C8A96E` | **暖金** | accent —— 主高光色，金属边框反光，粒子色，品牌LOGO色 |

| `#4A7FA5` | **冷蓝** | secondary accent —— 屏幕光，科技感点缀，表盘夜光 |

| `#F5F0E8` | **暖白** | text / 柔光高光 —— 反光板反射色，文字色 |

| `#2A2A2A` | **深灰** | secondary bg —— 部分场景的渐变背景，袖口色 |


### 风格参考

- **film** — *Blade Runner 2049 华莱士总部*：金色水面底光 + 纯黑背景 + 粒子漂浮 —— 借鉴其「单一光源+纯黑」的极简灯光哲学

- **photographer** — *Peter Lindbergh 静物摄影*：高反差黑白摄影中的材质表现 —— 借鉴其对金属/皮革/玻璃质感的极致追求

- **other** — *Apple Watch 广告系列*：产品旋转展示 + 微距材质剪辑 + 极简旁白 —— 借鉴其产品叙事节奏


### 角色设定


### 参考图

- `luxury smartwatch, black titanium case, sapphire glass, on pure black background, single golden rim light from top-right, minimalist product photography, 8K, ultra-detailed metal texture, cinematic lighting, fog-like gold dust particles floating` → —（{{#if approved}}✅ 通过⏳ 待审核）

- `extreme macro shot of brushed titanium watch case texture, hard top light revealing micro-details, industrial design, 100mm macro lens, pure black background, product photography, 8K ultra detailed` → —（{{#if approved}}✅ 通过⏳ 待审核）

- `luxury watch worn on wrist, dark grey wool suit cuff, top-down softbox lighting, elegant hand gesture, minimalist composition, the watch as the brightest element, golden light accent, cinema-grade photography` → —（{{#if approved}}✅ 通过⏳ 待审核）


---

## 5. 摄影指导

| 维度 | 方向 |
|------|------|
| **摄影风格** | 克制与精确。90%的镜头为静态或极缓的dolly推进/拉远。全片仅场景4有一个手持感微动（dolly模拟）。镜头语言服务于'凝视产品'的核心概念——让观众有时间看清每一个细节。 |
| **灯光哲学** | 减法灯光。学习BR2049的单一光源原则——每个场景先确定唯一主光源方向，其他灯只做补充不抢主光。产品广告的最大陷阱是灯光太多太杂，本片反向操作：黑色背景+精准控光。 |
| **焦段偏好** | 100mm微距（材质特写）+ 85mm（佩戴场景）+ 50mm（Hero Shot/品牌落版）。所有镜头使用大光圈（f/1.4-f/2.8）创造极浅景深——背景自然虚化，无需后期。 |
| **色调调色** | 最终调色方向：整体降低饱和度10%，增强金色暖调的饱和度5%。暗部压到纯黑（IRE 0-5%），高光保留在IRE 70-80%（避免clipping）。参考BR2049的'褪色金'质感。 |
| **运镜语言** | dolly慢推（90%镜头）+ 0.5秒静态收尾。推进速度≤步行速度的1/4。转场通过光的方向延续（上一镜头的光源方向作为下一镜头的起始光方向）。 |

---

## 6. 声音设计

| 维度 | 方向 |
|------|------|
| **配乐风格** | Vangelis式合成器氛围音景（参考BR2049原声）。双层结构：低频pad层（CS-80音色，持续温暖嗡鸣）+ 中频旋律碎片（偶尔出现，不连续）。整体音量保持在背景，不为音乐而音乐。 |
| **参考曲目** | Vangelis - Blade Runner Blues（CS-80合成器低频pad）, Hans Zimmer - Time（弦乐渐进堆叠法）, M83 - Wait（合成器+大提琴组合）,  |
| **音效备注** | - 场景1：金色微尘粒子音效（类似细沙流动的ASMR质感）\\n- 场景2：每个材质切换对应一个清脆的拟音（金属=银铃/皮革=轻擦/玻璃=叮/夜光=电子脉冲）\\n- 场景3：心率监测=低频心跳声（40BPM），触控=轻微点击+触觉反馈嗡声，亮屏=Mac开机声低频版\\n- 场景4：袖口与表带接触的布料摩擦声（极轻微）\\n- 场景5：粒子汇聚的'嗖'声（类似光剑收起），LOGO浮现=低频'嗡——'\\n |
| **旁白基调** | 低沉男声（30-40岁），中文普通话。语气冷静、克制，像在耳边的低语。只说4个字，不加任何情绪。 |
| **旁白语言** | zh-CN |
| **静默运用** | 关键策略：音乐在落版前0.5秒达到峰值后立即收束→留0.5秒纯环境音+粒子音效→然后静默淡出。静默是最后一个'音符'。参考BR2049的爆发式巨响后回到安静的手法。 |

---

## 7. 视觉特效

| 技法 | 用途 | 涉及场景 |
|------|------|----------|
| 金色微尘粒子系统 | 场景1/5——漂浮在黑色背景中的金色微粒，慢速随机运动，密度不均匀（有团块） | 1, 5 |
光传递转场 | 场景2——每个材质镜头切换时，上一镜头的光源方向作为下一镜头起始光方向 | 2 |
AMOLED屏幕发光 | 场景3——纯黑背景下屏幕像素级发光，模拟真实AMOLED的对比度 | 3 |
触控静电光效 | 场景3——手指与屏幕接触点的微弱蓝白色电弧 | 3 |
皮肤辉光 | 场景4——演员腕部的柔和光晕，模拟高端广告摄影中的漫反射 | 4 |
金属微反射 | 场景4——手表金属边框映出柔光箱的虚化倒影 | 4 |
粒子环绕光轨 | 场景5——金色粒子在表盘周围形成环绕光轨，3D粒子系统 | 5 |
画面暗角 | 场景5——四角微弱的暗角效果（vignette） | 5 |


### 转场设计

- 第 1 场 → 第 2 场：**光传递——金色侧光延续至场景2第一个镜头** — 场景1最后一帧的金色侧光方向（右上→左下），在场景2第一个镜头中保持相同方向

- 第 2 场 → 第 3 场：**硬切——材质特写最后一帧（Hero Shot正面）直接切到息屏表盘正面** — 两个正面构图的直接切换，利用产品位置一致性制造无缝感

- 第 3 场 → 第 4 场：**软过渡——屏幕光渐暗→手腕升起** — 场景3最后一帧的屏幕光渐暗至全黑（0.5秒），然后场景4的手腕从下方升入亮光中

- 第 4 场 → 第 5 场：**金色粒子引入——粒子从场景4的最后1秒开始浮现** — 在场景4静止收尾的0.5秒内，金色粒子从表盘缝隙中开始浮现，延续至场景5


### 材质清单

- **拉丝钛合金**：哑光金属，单向拉丝纹理，深灰色调，各向异性反射（场景 2）

- **蓝宝石玻璃**：高折射率（1.77），抗反射镀膜，倒角边缘有微弱的蓝色/紫色折射（场景 2, 3）

- **意大利小牛皮**：哑光表面，可见天然毛孔纹理，深棕色，柔软褶皱（场景 2, 4）

- **316L精钢**：镜面抛光，高反射率，冷色调（偏蓝）（场景 2）


---

## 8. 分镜

> **总镜数**：7 | **网格布局**：3×3



### Panel 1 — 第 1 场（extreme-close-up）

| 项目 | 内容 |
|------|------|
| **描述** | 全黑画面。一束极细的金色侧光从右上方扫入，触及表盘边缘。金属边框折射出暖金色光芒。背景纯黑。 |
| **提示词** | `extreme close-up of luxury smartwatch edge, black titanium case, single golden rim light from top-right, 90% pure black frame, one golden highlight on metal edge, minimalist, cinematic product photography, fog-like gold dust particles floating, 8K ultra-detailed, 16:9` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 2 — 第 2 场（extreme-close-up）

| 项目 | 内容 |
|------|------|
| **描述** | 表冠的拉丝钛合金纹理，硬顶光揭示微米级细节。金属表面呈现单向拉丝的精密质感。 |
| **提示词** | `extreme macro shot of brushed titanium watch crown, hard top light revealing micro-details, industrial design precision engineering, pure black background, 100mm macro lens, product photography, 8K ultra detailed, 16:9` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 3 — 第 2 场（extreme-close-up）

| 项目 | 内容 |
|------|------|
| **描述** | 表带的意大利小牛皮——微观镜头下可见天然毛孔纹理和柔软褶皱。柔和的侧光勾勒出皮革的温润质感。 |
| **提示词** | `extreme macro of Italian calfskin leather watch strap, natural pore texture visible, soft side light, warm brown tones, pure black background, luxurious material study, 100mm macro, 8K ultra detailed, 16:9` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 4 — 第 3 场（close-up）

| 项目 | 内容 |
|------|------|
| **描述** | 表盘从息屏渐变亮屏的瞬间。AMOLED纯黑背景下，时间数字以优雅的无衬线字体浮现。屏幕边缘有微弱呼吸光。 |
| **提示词** | `close-up of smartwatch AMOLED screen turning on, pure black display, white minimal sans-serif digital time appearing, subtle blue edge glow, pure black background, futuristic interface, cinematic lighting from the screen itself, 8K, 16:9` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 5 — 第 3 场（medium）

| 项目 | 内容 |
|------|------|
| **描述** | 手指从画面外伸入轻触表盘。指尖与玻璃的接触点有微弱蓝白色静电光效。表盘显示心率监测红色光波。 |
| **提示词** | `medium shot of human finger touching smartwatch screen, electrostatic blue-white sparkle at contact point, red heart-rate wave animation on AMOLED display, pure black background, soft top light, minimalist tech aesthetic, 50mm lens, 8K, 16:9` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 6 — 第 4 场（medium-close-up）

| 项目 | 内容 |
|------|------|
| **描述** | 演员手腕从画面下方升起，手表佩戴完好。深灰色精纺羊毛西装袖口构成画面下半部的自然画框。手腕在画面中央偏上。 |
| **提示词** | `medium close-up of elegant wrist wearing luxury smartwatch, dark grey wool suit cuff, hand rising gracefully from bottom of frame, top-down large softbox lighting, golden accent rim light, pure dark gradient background, cinematic portrait, 85mm lens, 8K, 16:9, shallow depth of field` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



### Panel 7 — 第 5 场（medium）

| 项目 | 内容 |
|------|------|
| **描述** | Hero Shot——手表从45°旋转至完全正面，金色粒子环绕成光轨。产品严格居中。品牌LOGO以淡入方式浮现。 |
| **提示词** | `hero shot of luxury black smartwatch, centered, front-facing, slightly top-down angle, golden particles orbiting in light trail around the watch, elegant brand logo fading in above, classic three-point studio lighting, dark gradient background, premium product photography, 50mm lens, 8K, 16:9, cinematic` |
| **生成图** | — |
| **状态** | {{#if approved}}✅⏳ |



---

## 9. 最终调优备注


- **[high] color**：金色暖调(#C8A96E)在最终调色中需确保不偏黄——保持'褪色金'质感，参考BR2049赌场废墟色调

- **[medium] pacing**：场景2的8个材质快速剪辑中，第3-4个之间建议加入0.3秒的全黑过渡（眨眼效果），防止视觉疲劳

- **[medium] composition**：品牌落版（场景5）的LOGO浮现速度建议从0.5秒调整为0.8秒——让观众有时间记住品牌名

- **[low] sound**：场景1的低频嗡鸣音量建议从-24dB渐入而非从静默——给观众一个音频'预警'

- **[medium] vfx**：金色粒子的运动速度建议在0.5x-1x之间随机变化——等速运动看起来CG感太强


---

## 10. 下游工具对接

### ComfyUI 工作流
```json
{{creative_pack.comfyui_workflow}}
```

### HyperFrames 配置
```json
{{creative_pack.hyperframes_config}}
```

### Kling 提示词

- extreme close-up of luxury smartwatch edge, black titanium case, single golden rim light from top-right, 90% pure black frame, one golden highlight on metal edge, minimalist, cinematic product photography, fog-like gold dust particles floating, 8K ultra-detailed, 16:9. Camera: 100mm微距，静态→极缓推进，单一金色侧光. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- extreme macro shot of brushed titanium watch crown, hard top light revealing micro-details, industrial design precision engineering, pure black background, 100mm macro lens, product photography, 8K ultra detailed, 16:9. Camera: 100mm微距，静态，硬顶光. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- extreme macro of Italian calfskin leather watch strap, natural pore texture visible, soft side light, warm brown tones, pure black background, luxurious material study, 100mm macro, 8K ultra detailed, 16:9. Camera: 100mm微距，静态，大型柔光箱侧光. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- close-up of smartwatch AMOLED screen turning on, pure black display, white minimal sans-serif digital time appearing, subtle blue edge glow, pure black background, futuristic interface, cinematic lighting from the screen itself, 8K, 16:9. Camera: 100mm微距→50mm，极缓dolly拉远. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- medium shot of human finger touching smartwatch screen, electrostatic blue-white sparkle at contact point, red heart-rate wave animation on AMOLED display, pure black background, soft top light, minimalist tech aesthetic, 50mm lens, 8K, 16:9. Camera: 50mm，静态→极缓拉远，屏幕光为主光+顶部柔光箱. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- medium close-up of elegant wrist wearing luxury smartwatch, dark grey wool suit cuff, hand rising gracefully from bottom of frame, top-down large softbox lighting, golden accent rim light, pure dark gradient background, cinematic portrait, 85mm lens, 8K, 16:9, shallow depth of field. Camera: 85mm，dolly极缓推进（50%→70%），天窗柔光+金色反光板. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.

- hero shot of luxury black smartwatch, centered, front-facing, slightly top-down angle, golden particles orbiting in light trail around the watch, elegant brand logo fading in above, classic three-point studio lighting, dark gradient background, premium product photography, 50mm lens, 8K, 16:9, cinematic. Camera: 50mm，静态（产品旋转由转台完成），三点布光. Aspect ratio: 16:9. Cinematic quality, 4K, smooth motion.


### Runway 提示词

- extreme close-up of luxury smartwatch edge, black titanium case, single golden rim light from top-right, 90% pure black frame, one golden highlight on metal edge, minimalist, cinematic product photography, fog-like gold dust particles floating, 8K ultra-detailed, 16:9. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- extreme macro shot of brushed titanium watch crown, hard top light revealing micro-details, industrial design precision engineering, pure black background, 100mm macro lens, product photography, 8K ultra detailed, 16:9. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- extreme macro of Italian calfskin leather watch strap, natural pore texture visible, soft side light, warm brown tones, pure black background, luxurious material study, 100mm macro, 8K ultra detailed, 16:9. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- close-up of smartwatch AMOLED screen turning on, pure black display, white minimal sans-serif digital time appearing, subtle blue edge glow, pure black background, futuristic interface, cinematic lighting from the screen itself, 8K, 16:9. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- medium shot of human finger touching smartwatch screen, electrostatic blue-white sparkle at contact point, red heart-rate wave animation on AMOLED display, pure black background, soft top light, minimalist tech aesthetic, 50mm lens, 8K, 16:9. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- medium close-up of elegant wrist wearing luxury smartwatch, dark grey wool suit cuff, hand rising gracefully from bottom of frame, top-down large softbox lighting, golden accent rim light, pure dark gradient background, cinematic portrait, 85mm lens, 8K, 16:9, shallow depth of field. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.

- hero shot of luxury black smartwatch, centered, front-facing, slightly top-down angle, golden particles orbiting in light trail around the watch, elegant brand logo fading in above, classic three-point studio lighting, dark gradient background, premium product photography, 50mm lens, 8K, 16:9, cinematic. Mood: 冷静克制的高级感。像走进一个只有一支表的黑色画廊——所有注意力都在产品上。金色光芒像液态金属在暗夜中流动。. Cinematic, high production value.


---

## 元信息

| 字段 | 值 |
|------|-----|
| **生成时间** | 2026-06-12T07:38:46Z |
| **生成工具** | Muse Video Skill — prompt_assembler.py v0.3.0 |
| **编剧审核** | True |
| **美术审核** | True |
| **摄影审核** | True |
| **声音审核** | True |
| **特效审核** | True |
| **分镜审核** | True |
