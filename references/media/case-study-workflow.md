# Case Study Creation — Video Analysis & Candidate Discovery

> **运行时依赖**：Phase 1 步骤 2.5a 参考视频拆解管线加载此文件，获取视频下载/编解码器/预处理经验。
> 前半部分：视频获取与分析工作流（下载、编解码器处理、压缩策略、常见陷阱）
> 后半部分：案例候选发现与筛选框架（批量 URL 识别、时长可行性分类、质量标准）

---

## Video Analysis Workflow (Phase 8 addition)

When the source video is behind a login/paywall (X/Twitter, streaming platforms, etc.) or you need deeper technical detail than a single watch provides:

### Download → Analyze → Create

1. **User downloads the video** and places it at a known path (e.g. `C:\Users\钱多多\Desktop\<file>.mp4`)
2. **Run video_analyze twice**:
   - First pass: broad analysis — type, duration, narrative structure, every scene, color, sound, VFX
   - Second pass: targeted analysis — specific timestamps for transitions, exact colors, cat/dog details, shot types per scene
3. **Cross-reference the two passes** — the second pass often corrects hallucinations from the first (e.g. first pass may claim "cat meow sounds" — second pass may clarify "no cat meow sounds")
4. **Create the case file** using the combined analysis as source material

### When to use this vs. traditional research

| Scenario | Method |
|----------|--------|
| Video on YouTube/Bilibili/public | Traditional: watch + web search for context |
| Video behind X/Twitter/streaming login wall | Video download → video_analyze workflow |
| Need frame-accurate technical detail | video_analyze (even for public videos) |
| Need director/studio/production credits | Web search (video_analyze can't see credits reliably) |

### Pitfall: YouTube bot detection blocks yt-dlp downloads ★ (Phase 9 discovery)

YouTube may return "Sign in to confirm you're not a bot" even for publicly available videos. The fix: use the Android player client, which has less aggressive bot detection:

```bash
# ❌ Fails with bot detection:
uv run yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]" "URL" -o "output.mp4"

# ✅ Android client bypasses bot detection:
uv run yt-dlp --extractor-args "youtube:player_client=android" --no-check-certificate \
  -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL" -o "output.mp4"
```

Note: the Android client may skip higher-resolution formats (SABR-only streaming experiment). The fallback format (usually 18 = 360p) is sufficient for video analysis purposes. Chrome cookie extraction (`--cookies-from-browser chrome`) may also fail — don't waste time debugging cookies; use the Android client directly.

### Pitfall: YouTube URL truncation in handoffs

YouTube video IDs are 11 characters. When a URL in a handoff has only 10 characters (e.g., `bg3iEHHTGQ` instead of `bg3iEHHTGtQ`), it was truncated. Always verify by searching YouTube for the video title rather than blindly trusting a handoff URL. Use:
```bash
# Verify a URL is valid before attempting download:
uv run yt-dlp --extractor-args "youtube:player_client=android" --no-check-certificate \
  --print title "URL" 2>&1 | head -5
```

video_analyze has a ~50 MB base64-encoded payload limit. Files as small as ~35 MB raw can exceed this after encoding. **Always check file size first** with `ls -lh` or `ffprobe`. If the raw file is >30 MB or encoded payload >50 MB, compress before analysis.

**★ CRITICAL: av1 codec base64 inflation (Phase 9 discovery) ★**

Av1-encoded videos produce significantly larger base64 payloads than H.264 videos of the same file size. A 15.7 MB av1 video can trigger a 413 error while a 30.2 MB H.264 video succeeds. The base64 encoding overhead for av1 is approximately 2-3× that of H.264 due to differences in how the two codecs structure their bitstreams.

**Always check the codec before video_analyze:**

```bash
# Step 0: Check codec — if av1, you MUST transcode to H.264
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "<input>"
```

**If codec is av1 → transcode to H.264 before ANY attempt:**

```bash
# av1 → H.264 transcode (even at same resolution, this drastically reduces base64 payload)
ffmpeg -y -i "<input>" -vf "scale=1280:720" -c:v libx264 -crf 26 -c:a aac -b:a 96k "<output.mp4>"
```

**Decision tree for video_analyze prep:**

```
ffprobe check
    │
    ├─ Codec = av1？
    │   └─ YES → ffmpeg to H.264 (CRF 26-28, scale as needed)
    │       └─ THEN check file size →
    │           ├─ <30 MB → try directly
    │           └─ >30 MB → compress further (scale=854:480, CRF 30)
    │
    └─ Codec = H.264 / HEVC？
        └─ Check file size →
            ├─ <30 MB → try directly
            ├─ 30-50 MB → compress to 720p/CRF 26
            └─ >50 MB → compress to 480p/CRF 30
```

**Two-tier strategy** (for H.264/HEVC after av1 transcode): Start with 720p/CRF 26 (~15-30 MB output). If video_analyze returns "413 Request Entity Too Large", fall back to 480p/CRF 30 (~5-10 MB output). The 413 error can occur even when the raw file appears under the limit — HTTP overhead and base64 inflation (~33% for H.264, more for av1) mean a 21 MB raw file can trigger it.

**Real session data points** (for calibration):
- IPHONE17PRO: 30.2 MB H.264, 1080p → ✅ PASS
- MACBOOK-NEO: 15.7 MB av1, 1080p → ❌ 413 FAIL → 480p H.264 8.8 MB → ✅ PASS
- PUDONG-CAT (prior session): ~35 MB, 1080p → 720p H.264 ~17 MB → ✅ PASS

**Long videos** (>60s): combine resolution reduction with CRF increase. A 90s 1440p video (55 MB raw) needs the 480p/CRF 30 path. A 30s 1080p video (28 MB raw) usually works at 720p/CRF 26.

### Pitfall: video_analyze hallucination

The AI model may hallucinate details (e.g. inventing cat meows that aren't there, missing subtle color shifts). Always run a **second targeted pass** asking for the specific details you plan to write about — the second pass often corrects errors. Never rely on a single video_analyze pass for production-quality case studies.

### ★ Pitfall: av1 codec causes 400 error on video_analyze (2026-06-15 verified)

Av1-encoded videos trigger a 400 deserialization error on video_analyze, even when the file is small (6-8 MB raw):
```
unknown variant `video_url`, expected `text`
```
This is NOT a model limitation — the same model processes H.264 videos without issue. The av1 codec's internal structure produces a base64 payload that the API cannot deserialize. After converting to H.264, the same 6-8 MB file passes without error.

**This 400 error is distinct from the 413 (payload too large) error.** The 400 happens at the deserialization layer (before size checks), while the 413 happens at the size-enforcement layer. Both are triggered by av1 more easily than H.264, but for different reasons.

**Fix: always transcode av1 → H.264 before video_analyze:**
```bash
ffmpeg -y -i "<input>" -vf "scale=1280:720" -c:v libx264 -crf 26 -c:a aac -b:a 96k "<output_h264.mp4>"
```

### Pitfall: Frame-only analysis misses narrator, sound, and text overlays (2026-06-15 discovered)

When video_analyze is unavailable and you use ffmpeg frame extraction + vision_analyze instead:
- ❌ **Narration/VO**: completely invisible — a video may have a full narrator track with zero visual evidence
- ❌ **Music style**: only guessable from YouTube description metadata
- ❌ **Text overlays**: may be partially visible in frames but their timing, animation, and sequencing are lost
- ❌ **Sound effects**: entirely invisible

**Real session consequence (2026-06-15):**
- IPHONE-AIR case written from frames claimed "无旁白纯视觉叙事" — but the actual video has Abidur Chowdhury's full narration track
- IPAD-AIR-M4 case claimed "独立民谣配乐" — but actual music has prominent vocalizations ("Mmm-mmm", "Ooh-ooh")
- IPAD-AIR-M4 missed ~40% of scenes (bubble gum, balloons, dog frisbee, elevator, gaming, floating person)

**Mitigation:** if you must use frame-only analysis, always supplement with YouTube metadata (description often lists narrator and music credits), and flag the case with a `<!-- TODO: video_analyze review -->` comment for later verification.


---

## Case Candidate Discovery — Batch YouTube URL Identification ★

When the user provides a batch of YouTube URLs for case candidates, identify them all at once with a single `execute_code` block instead of opening each in the browser individually:

```python
from hermes_tools import terminal

urls = ["vid1", "vid2", "vid3", ...]

for i, vid in enumerate(urls, 1):
    result = terminal(
        f'curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json" '
        f'2>/dev/null', timeout=10
    )
    data = json.loads(result['output'])
    print(f"#{i}. [{vid}] {data['title']}")
    print(f"    Author: {data.get('author_name', 'N/A')}")

# Optional: also extract duration and view counts from YouTube page HTML
```

**Duration extraction** (for viability assessment):
```python
result = terminal(
    f'curl -s "https://www.youtube.com/watch?v={vid}" 2>/dev/null '
    f'| grep -oP \'"lengthSeconds":"[0-9]+"\' | head -1', timeout=10
)
dur_sec = int(result['output'].split(':"')[1].rstrip('"'))
print(f"Duration: {dur_sec // 60}:{dur_sec % 60:02d}")
```

This pattern identifies 8+ videos in ~12 seconds with zero browser interaction. Use it whenever the user drops multiple YouTube links.

---

## Case Candidate Selection Framework ★

Not every video the user provides qualifies for a full case study. Classify candidates before committing to creation:

### Duration Viability

| Duration | Viability | Strategy |
|----------|-----------|----------|
| ≥3:00 | ★★★ 理想 | Easy to reach ≥200 lines, 15+ techniques, 5 role dimensions |
| 1:30–2:59 | ★★☆ 可行 | Achievable with thorough analysis (2 video_analyze passes) |
| 1:00–1:29 | ★☆☆ 挑战 | May struggle for 200 lines; combine with web research on production context |
| <1:00 (single) | ❌ 跳过 | Too short for meaningful technique extraction alone. Paired with another <1min video of same brand/formula → merge into dual-video comparative case (1 case covering both, 150-180+ lines). |

### Genre Classification

| Category | Include? | Examples |
|----------|----------|----------|
| Product intro film (手机/电脑/手表发布片) | ✅ Yes | iPhone Pro intro, MacBook intro, Galaxy Unpacked |
| Product detail short (3D renders, material close-ups) | ✅ Yes | Nothing Phone industrial design b-roll |
| Super-short product ads (<1:00, paired) | ✅ Yes (merged) | AirPods Pro 3 + MacBook Neo short → merged as APPLE-FLASH |
| Brand/value ad (品牌价值观/教育) | ✅ Yes (adjusted framework) | Apple Education — shift weighting to narrative/emotion/brand mission |
| Event highlight reel (发布会集锦) | ✅ Yes (adjusted framework) | Apple Sept Event Highlights — shift weighting to info density/multi-product pacing |
| Feature-specific ad (单一功能演示) | ⚠️ Maybe | AirPods ANC demo — only if visually rich |
| Narrative brand film (品牌故事短片) | ⚠️ Route to Round 1 | e.g. Huawei "Dream It Possible" — valid but different category than product detail |

### Pitfall: Chinese corporate videos on Polyv platform are essentially inaccessible (2026-06-16 discovered)

Many Chinese brands (NIO 蔚来, Xpeng, Li Auto, etc.) host their brand videos on **Polyv (保利威)** — a Chinese enterprise video platform that requires authentication and signed URLs. The video source ID is visible in the page's `__NEXT_DATA__` JSON (e.g., `"source":"b4b7a9a956d74819c29bc7d0d08de19e_b"` with `type:"Polyv"`), but the actual `.mp4` or `.m3u8` URL is never exposed to unauthenticated clients.

**Methods that failed (2026-06-16, NIO 蔚来icon设计理念):**
1. Browser navigation — blocked by anti-bot detection
2. yt-dlp on the page — unsupported URL
3. YouTube/Bilibili search — not cross-posted
4. CDN direct URL construction — 404/567 errors
5. Polyv API (v1/v2/v3) — all return 404 without auth token
6. NIO internal Next.js API — 404
7. cobalt.tools — blocked

**Recommendation:** After 2 failed attempts, report the blocker and ask the user for an alternative source (B站 link, direct download URL, local file). Do not spend more than 3 tool calls trying to crack Polyv — the platform is designed to prevent exactly this.

Apple does NOT post standalone product intro films for Mac mini, MacBook Pro, or iPhone on YouTube as separate videos. These films exist only:
- Embedded in **keynote recordings** (Apple Event videos, 60-120 min) — but extracting a 2-min segment is impractical for video_analyze
- Hosted on **apple.com** product pages as `.mp4` files — accessible via direct download from page source

When the user wants an Apple product film that isn't on YouTube:
1. Check apple.com product page source for `.mp4` URLs
2. Or: use the closest YouTube equivalent (e.g. keynote chapter timestamps)
3. Or: pivot to a different brand with a comparable product film on YouTube

---

## Case File Quality Standard

Each case file must meet:
- ≥200 lines
- ≥12 unique techniques (not counting duplicates merged into existing INDEX rows)
- 5 role dimensions covered (Writer/DP/Art Director/VFX/Sound Designer)
- Hex color codes in the color/art direction table
- 适用提示 section with 最佳匹配/不适用/引用优先级
- For commercial/advertising cases: creative strategy section required
