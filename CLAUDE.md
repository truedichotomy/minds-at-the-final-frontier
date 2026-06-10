# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project** — it is a single academic manuscript ("Minds at the Final Frontier") authored in [Quarto](https://quarto.org). One semantic source, `index.qmd`, renders to both a web edition (HTML) and a print edition (PDF). There is no application, test suite, or package to install. "Building" means rendering the document. `README.md` is the canonical onboarding doc and covers dependencies, editing conventions, and licensing in detail — read it.

## Commands

```bash
quarto render             # build all formats (HTML + PDF) into _output/
quarto render --to html   # HTML only (fast; no LaTeX needed)
quarto render --to pdf     # PDF only (needs a LaTeX distribution)
quarto preview            # live-reloading local preview while editing
bash figures-src/build-figures.sh   # regenerate figures/ from TikZ sources
```

- HTML rendering is the fast iteration loop; reach for `--to html` unless a change touches the PDF (LaTeX/titlepage) path.
- The PDF target needs a LaTeX install (`quarto install tinytex`) plus `rsvg-convert` (librsvg) to convert figure SVGs. `build-figures.sh` separately needs `pdflatex` + `pdftocairo` (poppler).

## Architecture: one source, two editions

The design principle is strict separation of **content** / **figures** / **presentation**, so the HTML and PDF editions stay *identical in content* while *free to differ in presentation*:

- **Content** lives only in `index.qmd` (Quarto Markdown) — prose, section structure, cross-references, citations. This is the single source of truth.
- **Figures** are authentic TikZ/pgfplots sources in `figures-src/`, compiled standalone to `figures/<name>.{svg,pdf}` (SVG for web, PDF for print). The `.svg`/`.pdf` files in `figures/` are committed build artifacts — regenerate them with `build-figures.sh` after editing a `.tex` source, never hand-edit them. `figures-src/_preamble.tex` holds shared colors/libraries pulled in by each figure.
- **Presentation** is split by format and lives outside the prose:
  - `_quarto.yml` is intentionally minimal (just project type + output dir); the real config is the **YAML front matter at the top of `index.qmd`** (`format: html:` / `format: pdf:` blocks).
  - `styles.css` styles the HTML reading column.
  - `partials/title-block.html` overrides Quarto's HTML title block (renders `tertiary-subtitle` + `disclaimer`).
  - `tex/titlepage.tex` is the PDF title page; the front matter suppresses the default `\maketitle` and injects this instead.

### How the same source produces format-specific output

Because one source feeds two very different presentations, `index.qmd` contains format-conditional blocks — recognize and preserve these:

- Raw LaTeX blocks (```` ```{=latex} ````) for PDF-only typesetting (epigraph page, manual `\tableofcontents`, page breaks). These are inert in HTML.
- `::: {.content-visible when-format="html"}` divs for HTML-only content (e.g. the "LIVING DOCUMENT" badge and cite-this-revision block).
- The PDF disables the auto TOC (`toc: false`) and places it manually via a `{=latex}` block; HTML uses Quarto's built-in TOC.

## Editing conventions (these break silently if ignored)

- **Cross-references** use Quarto `@`-syntax: `@fig-architecture`, `@fig-powercurve`, `@fig-lifecycle`, `@fig-conditions`; `@tbl-missions`, `@tbl-conditions`; `@sec-…` (heading `{#sec-…}` ids). Quarto auto-renders these as "Figure 1" / "Section 4.2" — **do not** type the word "Figure"/"Section"/"Table" before the reference or it doubles. `number-sections: true` is what makes section refs resolve to numbers.
- **Callouts** map to specific classes: "Central Thesis" → `::: {.callout-important}`, "Key Insight" → `::: {.callout-tip}`, closing reflection → `::: {.callout-note}`. Keep these consistent — they render natively in both formats.
- **Figure includes** point at the `.svg` assets with a `{#fig-…}` id.

## Provenance (not part of the build)

`conversion/assemble_qmd.py` is the one-shot script that migrated the original LaTeX manuscript to `index.qmd`. It is kept for transparency only and is **not** in the render path — it reads paths that no longer exist on this machine. Do not run it; edit `index.qmd` directly.

## Licensing

Dual-licensed: content (`index.qmd`, figures, prose) is **CC BY 4.0**; code/tooling (`figures-src/`, `conversion/`, scripts) is **MIT**. See `LICENSING.md`.
