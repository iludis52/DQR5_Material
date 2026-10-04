# iludis Markdown-Ansicht: authoring rules for AI

Use only the syntax listed here. Anything else renders as raw text or is lost. Base: CommonMark via markdown-it 14 (raw HTML on, linkify on, typographer off, breaks off) + the extensions below. Write document content in the user's language; keep the keywords below verbatim.

## Core
- Headings, emphasis, `~~strike~~`, lists, blockquotes, `---`, inline/reference links, bare URLs auto-linked.
- GFM pipe tables with `:---:` alignment. No merged or multi-line cells (use `<br>` or an HTML table). Prefer ≤6 columns: wide tables scroll.
- Task lists `- [ ]` / `- [x]` at item start; display only.
- Single newline = space. Hard break: two trailing spaces, trailing `\`, or `<br>`.
- No smart typography: type „…“, –, … directly.
- Footnotes `[^id]` + `[^id]: text`, inline `^[text]`; keep them single-paragraph.

## Frontmatter
At byte 0, `---` … `---`. `titel`/`title` creates a header line: title left; `autor`/`author`, `datum`/`date`, `kurs`, `version` right. All other keys (and those, if no title) are shown violet-italic as `key: value`. Flat keys only; values are plain text (no Markdown, no nested objects).

## Callouts
`> [!TYP] optional title` + `> body`, or (unindented, nestable, not inside lists):
```
:::typ optional title
body
:::
```
TYP (case-insensitive): hinweis|note, konzept, warnung|warning, caution, tipp|tip, faustregel, merke|important, prompt, tool. Title on the same line, may contain inline Markdown. Other types render as an untyped box.

## Code
Fenced ``` or ~~~; first info word = language, shown as label. Highlighted: bash/sh, c, cpp, csharp, css, diff, go, graphql, ini, java, js, json, kotlin, less, lua, makefile, markdown, objectivec, perl, php, python, r, ruby, rust, scss, sql, swift, ts, vbnet, wasm, xml/html, yaml; others plain. No line numbers, line highlights or `title=` attributes. Nest fences with a longer outer fence.

## Mermaid 11.4
Fence language `mermaid`. Types: flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, gantt, pie, quadrantChart, requirementDiagram, gitGraph, C4Context, mindmap, timeline, sankey-beta, xychart-beta, block-beta, packet-beta, kanban, architecture-beta. Not: radar-beta, treemap. Quote labels with special chars: `A["f(x) = 2x"]`. Avoid fixed colors/`%%{init}%%` themes (a dark style exists). Prefer `TD` for wide flows; diagrams shrink only to 80 %, then scroll.

## Math (KaTeX, not MathJax)
- Inline `$…$` or `\(…\)`; display `$$…$$`, or `$$`/`\[` at line start, multi-line until `$$`/`\]`.
- `$…$` needs no space inside either delimiter and no digit right after the closing `$`. Write currency as `\$`.
- Formula content is protected from Markdown (`_ * \\` work as in LaTeX).
- KaTeX subset only: `aligned`, `cases`, `pmatrix`, `\tag`, `\text`, `\mathbb` ok; no `\label`/`\eqref`, auto-numbering, packages, TikZ.
- In tables `|` splits cells even inside math: use `\vert`, `\lvert…\rvert`, `\Vert`.

## Images
`![alt](rel/path.png "title")`: relative to the .md file, resolved only when the user opened the folder; absolute and `data:` URLs always work. An image alone in its paragraph becomes a figure captioned "Abb. n: <title or alt>"; inline images get no caption. Size only via `<img src="…" alt="…" width="320">`. Formats: png, jpg, gif, webp, svg, avif, bmp.

## Links and anchors
- External links open in a new tab.
- Relative `.md` links open in the viewer if the file is in the opened folder; `#anchor` after a filename is ignored. Other relative targets (PDF, folders) don't work: use absolute URLs.
- h1–h4 get IDs (h5/h6 don't): lowercase → ä/ö/ü/ß to ae/oe/ue/ss → drop all but `a-z0-9_-` and spaces → each run of spaces to one `-` → max 60 chars → duplicates `-2`, `-3`. Example: `## 3. Übersicht & Ziele` → `#3-uebersicht-ziele`. This differs from GitHub. Custom ID: `<h2 id="x">`.
- Use exactly one h1 and don't skip levels (outline shows h1–h4).

## Folder sets
The viewer opens `index.md`, `readme.md` or `start.md` first. A root-level `glossar.md` is treated as reference and hidden from the file list.

## Raw HTML
Allowed and unsanitized, `<script>` doesn't run. Useful: `<details>`, `<kbd>`, `<sub>`, `<sup>`, `<mark>`, `colspan`, print page break `<div style="break-before: page"></div>`. Markdown inside an HTML block needs blank lines around it. No fixed colors (a dark style exists).

## Page markers
`<!-- Seitenumbruch -->` / `<!-- pagebreak -->`, optional text (`<!-- Seitenumbruch: S. 47 -->`), are shown as a visible marker only and don't break pages in print. Other comments stay invisible.

## Unsupported → use instead
`==x==` → `<mark>` · `H~2~O`, `x^2^` → `<sub>`/`<sup>` or math · `:emoji:` → Unicode · definition lists → bold term list · abbreviations `*[X]:` → write out · `[TOC]` → none (sidebar outline) · `{#id .cls}` → HTML id · `[[wiki]]` → `[x](x.md)` · `!!! note`, `:::note[T]` → callouts above · `{width=}` → `<img width>` · PlantUML/DOT/Vega/Chart.js → Mermaid
