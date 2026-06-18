# Batch INDEX.md Update Workflow

Adding a new case requires updating 10 cross-reference tables in INDEX.md. Doing this manually is slow and error-prone — use `execute_code` with batch `patch()` calls instead.

## Pattern

```python
from hermes_tools import patch

base = "D:\\hermes workspace\\muse video skill\\references\\cases\\INDEX.md"

# 1. Master Registry — insert after last row
patch(base,
    old_string="| LAST-CASE | ... |\n\n### 类型枚举",
    new_string="| LAST-CASE | ... |\n| NEW-ID | ... |\n\n### 类型枚举"
)

# 2-7. Technique tables — insert new entries at end of each subsection
#    Use the subsection boundary markers as anchors
patch(base,
    old_string="| last_entry_in_narrative | ... |\n\n### 镜头语言",
    new_string="| last_entry_in_narrative | ... |\n| new_technique | NEW-ID |\n| ... |\n\n### 镜头语言"
)

# 8-10. Scene/Style/Role tables — append NEW-ID to comma-separated lists
patch(base,
    old_string="| product-demo | ID1, ID2, ID3 | ... |",
    new_string="| product-demo | ID1, ID2, ID3, NEW-ID | ... |"
)

# Role dimension table — NO longer needs updates (post-Phase 13 refactor).
# All cases cover all 5 roles by default. See §五 of INDEX.md.
```

## Typical patch count per case

| Table | Patches |
|-------|---------|
| Master Registry | 1 |
| Narrative techniques | 1 (insert 3-5 entries) |
| Lens techniques | 1 (insert 3-5 entries) |
| Color/Art | 1 (insert 2-3 entries) |
| VFX | 1-2 (insert + merge with existing) |
| Sound | 1 (insert 2-3 entries) |
| Creative ad | 1 (insert 2-4 entries) |
| Scene → Case | 1-2 |
| Style/Emotion | 2-4 |
| **Total** | **10-14** |

## Key rules

- **Pipe consistency**: `read_file` displays `||` but actual bytes are `|`. Use `cat -A` to verify. All `old_string` values must use single `|`.
- **Technique dedup**: If a new technique name matches an existing one, merge with comma: `| 技法名 | OLD-ID, NEW-ID |`. Don't create duplicate rows.
- **Section anchors**: Use subsection boundary markers (e.g. `\n\n### 镜头语言`) in `old_string` to ensure unique matches.
- **10-14 patches in one `execute_code` call** — don't split across multiple calls; the unified script is atomic and debuggable.

### ★ CRITICAL PITFALL: execute_code `read_file()` content includes line-number prefixes — writing it back corrupts the file

When you use `from hermes_tools import read_file` inside an `execute_code` block, the returned `content` includes line-number display-layer prefixes in the format `NNN|` at the start of every line. For example, a file line that is actually:

```
| MACHINE-HALLUCINATION | 机器幻觉 | experimental |
```

Will be returned by `read_file()` inside execute_code as:

```
44|44|| MACHINE-HALLUCINATION | 机器幻觉 | experimental |
```

**If you modify this content and write it back with `write_file()`, the `44|44|` becomes literal content in the file.** This silently poisons every line with garbage prefixes that normal `read_file` display hides (because it prepends its own `NNN|`).

**Detection**: `cat -A INDEX.md | head -5` — if the first content line looks like `1|# 案例索引` instead of `# 案例索引`, the file is corrupted.

**Fix**: Strip with `re.sub(r'^(\d+\|)', '', content, flags=re.MULTILINE)` before writing back.

**Prevention — choose ONE:**
- **Option A (recommended)**: Use Python's built-in `open()` inside execute_code instead of `read_file()`. `open('INDEX.md', 'r', encoding='utf-8').read()` returns raw bytes without line numbers.
- **Option B**: Always strip `^\d+\|` as a post-processing step before any `write_file()` that originated from `read_file()` content.

**Real session example (2026-06-16)**: MACHINE-HALLUCINATION case creation — INDEX.md corrupted to 780 lines with literal `1|`, `2|`, `3|`... prefixes on every line. Required a regex strip script to recover.

### ★ CRITICAL PITFALL: Fuzzy patch matching can silently corrupt when anchors don't match exactly

The `patch()` tool uses 9 fuzzy-matching strategies. When an `old_string` does NOT match the actual file content, the tool may still find a "close enough" match and apply a PARTIAL replacement. This produces **silent corruption** — the patch reports "OK" but the file is damaged.

**Real session example (2026-06-17, Phase 14-17 batch)**:

```python
# Intended anchor: abstract → section header
patch(base,
    old_string="| abstract | MACHINE-HALLUCINATION |\n\n---\n\n## 五、角色维度 → 案例 Mapping",
    new_string="| abstract | MACHINE-HALLUCINATION |\n| luxurious | ... |\n\n---\n\n## 五、角色维度 → 案例 Mapping")
```

**What actually happened**: The file had `| futuristic | ... |` between `| abstract |` and `---`, so the anchor did NOT match literally. Fuzzy matching found a close match, consumed the `## 五` section header, but the new style entries (`luxurious/whimsical/sleek/charming`) were NOT inserted. Result:
- `## 五、角色维度 → 案例 Mapping` header lost (content survives but headless)
- 4 new style entries silently missing
- Patch reported "OK" — no error surfaced

**Prevention — DO THIS BEFORE EVERY execute_code PATCH BATCH:**

1. **Read the actual anchor region first** with `read_file()` to verify exact bytes
2. **Copy-paste the actual content** into `old_string` — do NOT compose from memory
3. **After all patches, run a verification script** that checks:
   - Section headers present: `grep "^## [一二三四五六]、" INDEX.md`
   - New IDs appear in expected tables: `grep -c "NEW-ID" INDEX.md`
   - No double pipes: `python3 -c "with open('INDEX.md') as f: ..."`
4. **If any check fails, do NOT commit** — fix the corruption first

**Do NOT trust `patch()` return value alone.** The tool may report "OK" for a fuzzy match that caused damage. Visual/script verification is mandatory.
