# 视频封面设计规范

> **用途**：Muse Video 扩展——项目产出后自动生成视频号/小红书封面 HTML
> **调用时机**：Phase 7 确认门禁通过后（步骤 7 导出交付物），用户显式选择生成
> **数据来源**：`project.*`（标题/标签） / `visual_dev.*`（配色/mood） / `storyboard[]`（配图帧）——全部在 Phase 7 确认时就绪
> **不依赖**：`model_compilation`（Phase 7.5 编译产物）
> **不修改原有管线结构**

---

## 封面类型

| 类型 | 规格 | 适用平台 | 布局 |
|------|------|---------|------|
| 竖版封面 | 1080×1440（3:4） | 视频号主页 | 标题→配图→标签（纵向） |
| 横版封面 | 1440×1080（4:3） | 视频号列表 | 标题区→配图（上下布局） |

---

## 配色系统

参考大地色系 / 莫兰迪粉彩，与视频情绪基调对齐：

| 视频情绪 | 封面底色 | 标题色 |
|---------|---------|--------|
| 温暖/诗意 | `#D5C8BD`（灰粉） | `#ffffff` |
| 冷峻/科技 | `#2C2C32`（炭灰） | `#ffffff` |
| 自然/清新 | `#C5D0C0`（鼠尾草绿） | `#ffffff` |

---

## 字体规范

```
字体族: "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif
标题: 700 weight, 96-108px
副标题: 400 weight, 36-42px
标签: 600 weight, 30-44px, 格式 < 标签名 >
```

---

## 内容模板

### 标题
- 格式：`实测 {模型名} {核心卖点}` 或 `{项目名}——{一句话概括}`
- 行数：竖版 3 行 / 横版 2 行
- 每个 `<br>` 前的内容不超过一行宽度

### 副标题
- 格式：`配合 muse video skill` 或自定义
- 与标签同行时：副标题左对齐，标签右对齐

### 标签
- 格式：`< 标签1 > < 标签2 >`
- 来源：从 project 信息自动提取（模型名、分辨率、项目类型）

### 配图
- 来源：Phase 6 分镜图 或 视频关键帧截图
- 位置：竖版居中 / 横版下半幅
- 圆角：4px

---

## HTML 结构模板

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{类型} 视频号封面</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    display: flex; justify-content: center; align-items: center;
    min-height: 100vh; background: #1a1a1a;
  }
  .card {
    width: {宽}px; height: {高}px;
    background: {底色};
    font-family: "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
  }
  .title { font-size: {标题字号}px; font-weight: 700; color: #ffffff; }
  .subtitle { font-size: {副标题字号}px; font-weight: 400; color: rgba(255,255,255,0.70); }
  .tag { font-size: {标签字号}px; font-weight: 600; color: #ffffff; }
</style>
</head>
<body>
<div class="card">
  <!-- 按布局类型填充 -->
</div>
</body>
</html>
```

---

## 调用方式

在 Creative Package 组装完成后：

1. 从 `project.*` 提取标题、标签信息
2. 从 Phase 6/7 选取配图帧
3. 根据 `project.tone` 匹配底色
4. 渲染 HTML → 浏览器截图 → 交付

---

## 验证清单

- [ ] 标题行数正确，无中途断行
- [ ] 配色与视频情绪一致
- [ ] 配图清晰，无人物干扰（如需要）
- [ ] 标签格式 `< 标签 >` 
- [ ] 截图尺寸精确（1080×1440 或 1440×1080）
- [ ] 无黑边或多余区域

---

## 参考案例

- 见筑 Uookarch 视频号封面：极简大地色 + 白色大字 + `< 标签 >` 格式
- 本文件基于 2026-06-23 实测 Seedance-2.0 项目验证
