# LJZ-COFFEE 拉片分析 — 重做 handoff

> 视频：`D:\hermes workspace\muse video skill\temp_videos\海辛和阿文视频参考\微缩模型艺术视频.mp4`
> 案例：`references/cases/LJZ-COFFEE.md`（陆家嘴咖啡文化节十周年宣传片，310行，已录入无拉片附录）
> 目标：第一次案例拉片分析，写入 §拉片附录

## 上次失败教训

video_analyze 返回的时间码和实际视频画面有显著偏差，导致 9 张帧有 7 张内容-描述错位。修复越补越乱，已全部 revert。

## 改进方案：先校准时间码再抽帧

1. **video_analyze 两遍照常跑**（第一遍整体、第二遍逐镜头）
2. **拉片表展示给用户校准**时，不仅校准 AI 理解，更要**请用户逐镜头确认时间码**
3. **先不抽帧**——等用户确认拉片表（含时间码）无误后，再按确认的时间码批量抽帧
4. 抽帧后**逐张 vision_analyze 验证**内容与描述匹配，再写入案例文件

## 核心信息

- 视频：37.5s, H.264, 1080p, 9.2MB
- 15 镜头 / 5 场景组
- 核心技法：微缩模型+移轴摄影、咖啡器具×城市地标融合（6处）
- 颜色体系：咖啡棕/牛奶白/樱花粉/中国红
- 先加载 `references/cases/_TEMPLATE.md` §拉片附录 了解格式
- 先加载 `references/media/case-study-workflow.md` 了解视频分析工作流
