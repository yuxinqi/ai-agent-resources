## 描述

请简要描述此 PR 的内容和动机。

## 类型

- [ ] `[new]` 新增内容
- [ ] `[update]` 更新内容
- [ ] `[verify]` 验真更新
- [ ] `[fix]` 错误修正
- [ ] `[restructure]` 结构重组

## 变更范围

<!-- 列出此 PR 涉及或影响的文档路径和目录 -->

## 证据等级

<!-- 此 PR 涉及内容的证据等级 -->
- [ ] L0 — 基于官方文档直接验证
- [ ] L1 — 实际操作验证
- [ ] L2 — 交叉验证
- [ ] L3 — 理论推导
- [ ] L4 — 待验证

## 验真说明

<!-- 如果涉及验真，请说明验真流程和方法 -->

## 影响的层级

<!-- 此 PR 影响的知识库层级 -->
- [ ] docs/getting-started
- [ ] docs/concepts
- [ ] docs/patterns
- [ ] docs/playbooks
- [ ] docs/case-studies
- [ ] verification/
- [ ] benchmarks/
- [ ] visualization/
- [ ] scripts/

## 检查清单

- [ ] 文档包含完整的 frontmatter 元信息（含 evidence_level 和 rating）
- [ ] 已添加或更新相关验真报告
- [ ] INDEX.md 已同步更新（或已运行 `python3 scripts/generate-index.py`）
- [ ] 内部链接检查通过（`python3 scripts/check_links.py`）
- [ ] Frontmatter 验证通过（`python3 scripts/validate_metadata.py`）
- [ ] 拼写和语法检查无误
