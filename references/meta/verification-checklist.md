# 产出验证清单 — Verification Checklist

> **用途**：Phase 7 组装完成后、交付用户前的最终验证。Director 逐项检查。
> **执行时机**：`prompt_assembler.py` 运行后，导出前。

---

## 必须通过（CRITICAL — 任一失败则不可交付）

- [ ] Project State JSON 完整——所有 phase 的 `_meta.director_approved` = true
- [ ] 每个角色产出有 `_meta` 追溯（role + revision）
- [ ] 无缺失字段——所有必填字段已填写，无 `TODO` 占位符
- [ ] 案例引用已加载（如果用户提到了风格参考）

## 应该通过（SUGGESTION — 影响质量但不阻塞交付）

- [ ] Director 全程参与审核，无跳过阶段
- [ ] 色调全局一致性——所有场景主色色相偏差 ≤ 30°
- [ ] 分镜 panel 数量覆盖所有关键场景
- [ ] 角色对白风格与 character_bible[].voice 一致（如有角色）

## 按需检查（NITPICK）

- [ ] 导出格式已按用户需求生成（HTML / Excel）
- [ ] Creative Pack 文件路径可访问
