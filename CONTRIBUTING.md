# 维护与检查 · Contribution and validation

先保持现有条目的事实边界与来源，再增加导航。更新研究状态或数值结论时，请链接原论文、作者或官方机构材料，区分陈述、已证特例、计算证据与作者解释。时间预算若是建议，请明确标为估计。

Keep factual qualifications and primary sources when editing. Distinguish a statement, a proved special case, computational evidence and interpretation. Label suggested time budgets as estimates.

## 本地命令 / Local commands

需要 Python 3.11 或更新版本，无需安装依赖。Requires Python 3.11+ with no additional packages.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_docs.py
```

检查器只读、不联网；有问题时输出源文件、行号（适用时）并以非零状态退出。CI 使用同样命令、只读内容权限且不保留 checkout 凭据。它不会发布或修改文档。

The checker reads files without modifying them or accessing the network. It exits nonzero for errors and reports source files and lines where applicable. CI runs the same commands with read-only repository permissions and checkout credential persistence disabled.

## 支持范围 / Supported scope

- All `.md` files are checked for inline Markdown links/images with bare balanced-parenthesis or angle-delimited destinations and optional titles; percent-encoded paths are decoded. Full, collapsed and shortcut reference uses are resolved through single-line reference definitions (unused definitions do not count as navigation). Explicit references without a definition fail.
- HTML `<a href>`, `<img src>`, `id` and anchor `name` attributes are supported. Fenced backtick/tilde blocks, matched backtick spans and HTML comments are ignored so examples can contain broken links.
- Local files and directories must exist and stay inside the repository after resolving symlinks. Markdown fragments must match an explicit HTML anchor or a **plain ATX heading** slug (letters/numbers, spaces, hyphens and underscores; repeated headings get numeric suffixes). SVG fragments use XML IDs. Prefer explicit stable anchors for navigation.
- Every `.svg` file, including unlinked assets, must parse as XML with an SVG root. The checker does not execute SVG or validate its visual content.
- `docs-check.json` declares exact inventories. A `glob` group compares actual file paths with `entries`; an `anchor_file` / `anchor_prefix` group compares book anchors. Every configured `navigation` page must link all entries in its group. Add an entry and update navigation and inventory together; unexplained additions, deletions or missing links fail.

这是针对本库写法的小型扫描器，不是完整 CommonMark/GitHub 渲染器。多行引用定义、Setext 标题、标题里的富文本/内联代码、复杂嵌套 HTML、HTML `srcset`/CSS 资源及 PDF 内部书签不在支持范围内；不承诺识别任意 Markdown。需要这些语法时应先扩展检查器及真实夹具测试，或使用明确锚点与受支持写法。

This is a small scanner for this repository's conventions, **not a full CommonMark or GitHub renderer**. Multiline reference definitions, Setext headings, rich/inline-code heading rendering, complex nested HTML, HTML `srcset`/CSS resources and internal PDF bookmarks are outside its scope. Extend the checker and real fixture tests before relying on additional syntax, or use supported syntax and explicit anchors.

外部 URL（含邮件、数据等 scheme）会跳过，不检查可用性、研究状态、事实、数学证明或译文等价性。片段验证仅适用于 Markdown 与 SVG；其他文件的内部片段不检查。通过只说明本地链接、资产格式与声明的目录结构满足上述规则。

External URLs and schemes are skipped. No check establishes website availability, current research status, factual accuracy, mathematical proof validity or translation equivalence. Fragments in formats other than Markdown/SVG are not inspected. A pass establishes only the documented local link, asset and inventory checks.
