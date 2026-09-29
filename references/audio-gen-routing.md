# 音频生成路由与适配 — Audio-Gen Routing

> **角色**：音频路线选择与适配中枢 —— 路线询问 + 适配章节（每模型一节，标题即注册）+ 音轨登记规则。声音方向定稿后决定「音频怎么出、用哪个模型、如何交付」。
> **边界**：本文件定义选择与规范；**执行边界 = 仅编译指令，不代生成**（2026-09-29 裁定）——实际生成由用户/下游工具执行。不持有执行逻辑。
> **被依赖**：`pipelines/default.md`（Phase 5 步骤 3b 路线询问 / Phase 7.5 步骤 7b 模型引导）
> **宪法位置**：`references/audio-gen-routing.md` — 交叉关注点，放 references 根目录（镜像 `image-gen-routing.md` / `model-compiler.md` 的适配模式）。
> **最后更新**：2026-09-29 | v0.35.1

---

## 音频路线选择（流程）

> 与生图/视频侧同构：先定路线，再选模型。Phase 5 末尾询问（步骤 3b），选择写入 `audio_gen.route`。

1. **展示路线候选**（≤3 + 其他/说明）：
   - **R1 视频模型原生**：Seedance `--generate-audio` 音画同步——零额外成本；音乐不可定制、无歌词
   - **R2 外部生成**：音乐模型 + 配音（TTS/专用工具）+ 音效素材库 → 音轨文件 → 后期对轨合成
   - **R3 无音频**（纯视觉）
   - **R4 混合**：如原生环境音 + 外部配乐（**须明示分工**，避免双轨打架）
2. **询问规则**：≥2 候选 → 显式询问；不确定时默认建议「要定制音乐 → R2；音画同步即可 → R1」
3. **模型选择时机**：R2 / R4 → Phase 7.5 编译完成后询问引导（步骤 7b）——音乐首批适配见 §适配：MiniMax Music 3.0；配音规划见 §适配：配音（TTS）
4. **落点**：`audio_gen.route`（+ `_meta`）；音轨产物登记顶层 `file_registry`（`asset_type: "audio"`，协议见 `references/reference-image-over-text.md` §资产引用协议）

> **商用授权提示（每次询问/选定附上）**：音乐与配音生成服务的授权条款各异——选定前确认「是否可商用 / 是否需署名 / 输出归属」。

> **音乐可用性提示（2026-09-29 核实）**：MiniMax 音乐 API（`music-3.0` 付费接口）自 2026-08-20 起**不再面向新用户**、免费接口已停止服务——R2 / R4 路线采用前先核账户可用性；替代路径见 §适配：MiniMax Music 3.0。

---

## 未适配模型处理

> 镜像 image-gen-routing：没有已有参数的 → 查对应模型官方文档。

1. **Agent 读取官方文档**：`web_extract` / `browser_navigate` 打开模型官方文档
2. **提炼五要素**：模型 ID / 调用方式（CLI / API）/ 输入格式（prompt / 歌词 / 参考音频）/ 时长与输出规格 / **商用授权条款**
3. **构建临时参数集**：标注 **「📄 文档推断·未实测」**
4. **首案例试跑**：最小成本生成 1 段 + 用户确认后，才进入批量
5. **升级路径**：试跑通过后，把参数固化回本文档的新「适配」章节（标注 ✅ 实测）

---

## 音轨登记规则

| 音轨类型 | 登记键（顶层 file_registry） | 说明 |
|---------|------------------------------|------|
| 配乐（音乐段落） | `audio_music_<slug>` | 段落级产物（按 scene 段落生成；整片连贯音乐须切分对轨） |
| 配音（旁白/对白） | `audio_vo_<seq>` | 逐句/逐段产物；参数来自 `sound.narration` |
| 音效 | `audio_sfx_<slug>` | 素材库获取或生成；关键词来自 `sound.sfx_notes` |

- 全部登记 `asset` 键：`{asset_type: "audio", asset_id: "audio_<slug>", is_canonical: …}`；`source` 按来源填（`generated` / `search` / `user`）
- **对轨纪律**：AI 视频时长不精确 → 音轨按「段落级」制作，交付后按实际时长裁切 / loop（**不承诺帧级同步**）

---

## 适配：MiniMax Music 3.0（音乐 · 首批）

> **端点**：`POST https://api.minimax.cn/v1/music_generation`（Bearer API_key）｜**实测状态**：📄 文档核实·未实测（2026-09-29 按官方文档回填；试跑后升级 ✅）

> ⚠️ **可用性公告（官方原文要点）**：自 **2026-08-20** 起，付费接口（音乐生成 / 歌词生成）**不再面向新用户**提供服务（历史付费用户可继续使用）；免费接口（`Music-3.0-free` / `Music-2.6-free` / `music-cover-free`）**已停止服务**。替代路径：① [MiniMax Audio](https://www.minimax.cn/audio) 产品；② **开源模型** `MiniMax-Music3`（[Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-Music3) / [ModelScope](https://modelscope.cn/models/MiniMax/MiniMax-Music3)，可自部署）。**采用前先核账户可用性。**

| 项 | 内容 |
|----|------|
| 模型标识 | `music-3.0`（推荐；Token Plan / 付费用户，RPM 120）｜同族：`music-2.6`（上一代）· `music-cover`（翻唱，需参考音频） |
| 输入格式 | `prompt` 风格/情绪/场景描述（≤2000 字符）+ `lyrics` 歌词（`\n` 分行；结构标签 `[Intro]` `[Verse]` `[Pre Chorus]` `[Chorus]` `[Interlude]` `[Bridge]` `[Outro]` `[Post Chorus]` `[Transition]` `[Break]` `[Hook]` `[Build Up]` `[Inst]` `[Solo]`；非纯音乐必填 ≤3500） |
| 纯音乐 / 自动写词 | `is_instrumental: true` → 免歌词（prompt 必填）；`lyrics_optimizer: true` + lyrics 空 → 按 prompt 自动生成歌词 |
| 关键参数 | `model` / `prompt` / `lyrics` / `is_instrumental` / `lyrics_optimizer` / `stream`（默认 false）/ `output_format`（`hex` 默认 · `url` 24h）/ `audio_setting`（`sample_rate` 44100 · `bitrate` 256000 · `format` mp3）/ `aigc_watermark`（默认 false，非流式生效） |
| 输出 | 响应 `data.audio`（hex 或 url）+ `extra_info`（`music_duration` 毫秒 · `sample_rate` · `channel` 2 · `bitrate` · `size`）；url 有效期 24 小时 |
| 时长与规格 | 由歌词 / 描述决定；示例输出 mp3 44.1kHz 立体声 256kbps |
| 商用授权 | ⚠️ **必查**：按 MiniMax 服务条款核实商用范围与署名要求（`aigc_watermark` 默认关闭） |
| 实测状态 | 📄 文档核实·未实测——**专项试跑（最小成本 1 段）通过后升级 ✅** |

调用示例（官方文档）：

```bash
curl --request POST \
  --url https://api.minimax.cn/v1/music_generation \
  --header 'Authorization: Bearer <API_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "music-3.0",
    "prompt": "独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆",
    "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步",
    "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"}
  }'
```

> 段落级纪律：接口单次生成整曲——按 §音轨登记规则 生成后按 scene 段落切分 / 对轨（不承诺帧级同步）。
> 衔接：`model-compiler.md` §音频编译 按路线产出「音频生成指令 + 对轨指引」；本节参数已回填（2026-09-29），试跑后升级 ✅。

---

## 适配：配音（TTS）— 火山 DoubaoVoice 音频生成

> **端点**：`POST https://openspeech.bytedance.com/api/v3/tts/create`（非流式）｜**实测状态**：📄 文档核实·未实测（专项待开——“先不测试”，2026-09-29 裁定）

| 项 | 内容 |
|----|------|
| 鉴权 | 请求头 `X-Api-Key`（新版控制台单头；旧版 `X-Api-App-Id` + `X-Api-Access-Key` 双头将下线）+ `X-Api-Request-Id`（追踪 ID） |
| 模型标识 | `seed-audio-1.0`——语种：中文 / 英文 / 日语 / 韩语 / 西语系 / 德 / 法 / 巴葡 / 泰 / 越 / 马来 / 菲 / 意 / 俄 / 荷 / 波 / 土；支持**时间轴控制**（自然语言控制总时长与人声时间段） |
| 输入 | `text_prompt` ≤3000 字符——三模式：纯文本 / 参考音频（`@音频N` 引用，≤3 条、单条 ≤30s / ≤10MB、wav·mp3·pcm·ogg_opus）/ 参考图片（≤1 张 ≤10MB、jpeg·png·webp）；`speaker`（音色 ID）/ `audio_data` / `audio_url` 三选一互斥；图片与音频参考不可混用 |
| 输出配置 | `audio_config`：`format`（默认 wav）/ `sample_rate` / `speech_rate` [-50,100] / `loudness_rate` [-50,100] / `pitch_rate` [-12,12] / `enable_subtitle`（**句 / 词级时间戳**） |
| 输出 | `audio`（Base64）+ `url`（2 小时有效）+ `original_duration`（**计费依据，单次上限 120 秒**）；`enable_subtitle: true` → `subtitle`（sentences / words 毫秒级时间戳） |
| 水印 | `watermark.aigc_watermark`（显式，结尾节奏标识）/ `aigc_metadata`（隐式）；`content_producer` · `produce_id` · `content_propagator` · `propagate_id`（内容制作 / 传播信息） |
| 商用授权 | ⚠️ 按火山引擎服务条款核实（水印与内容信息按合规需要开启） |
| 实测状态 | 📄 文档核实·未实测——**专项试跑后升级 ✅** |

**与声音方向衔接**（映射建议，专项细化）：`sound.narration.tone` → `text_prompt` 描述性控制；`pace` → `speech_rate`；`distance` / `reverb` → `text_prompt` 描述；台词清单（`audio_gen.voice.lines[]`）→ 逐句调用 + 拼接对轨。`enable_subtitle` 词级时间戳可用于**声字对齐**（衔接 `model-compiler.md` §字幕合成 spec 的后期对轨）。

- 本机备选（事实记录，非推荐）：Hermes `text_to_speech` 工具当前可用（edge provider，免费；中文须在配置中切换 zh-CN 音色）——专项时按需评估
- 参数落点：`sound.narration`；台词清单落点：`audio_gen.voice.lines[]`

---

## 扩展指南

> 新增音频模型支持时，在本文件末尾追加「适配：<模型名>」章节（章节标题即注册——选择流程自动解析）。

### 必填项

1. **模型标识**：模型 ID / 调用工具
2. **输入能力**：prompt / 歌词 / 参考音频支持情况
3. **参数速查 + 调用示例**
4. **商用授权**（音乐类必填）
5. **实测状态标注**：✅ 实测（≥1 个真实案例）或 📄 文档推断

---

> 相关：`references/roles/sound-designer.md`（声音方向产出）· `references/model-compiler.md`（音频编译）· `references/media/tool-matrix.md`（下游音乐/音效工具）· `references/image-gen-routing.md`（生图侧同构路由）
