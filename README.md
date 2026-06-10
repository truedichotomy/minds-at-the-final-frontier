# Minds at the Final Frontier — Quarto edition

*Deep Space Exploration as a Laboratory for AI Alignment and the Conditions of Artificial Life*

This repository is the **Quarto edition** of the manuscript. It holds a single
semantic source (`index.qmd`) from which both a web edition (HTML) and a
print edition (PDF) are rendered by [Quarto](https://quarto.org). It is a
standalone repository, deliberately separate from the original hand-rolled
LaTeX→HTML build, so the two toolchains never entangle.

The design goal is clean separation of the three layers:

- **content** — prose, structure, cross-references, citations live in `index.qmd`;
- **figures** — standalone vector assets in `figures/`, generated from authentic
  TikZ/pgfplots sources in `figures-src/`;
- **presentation** — per-format options in `_quarto.yml` / the document front
  matter, plus `styles.css` for the HTML reading column.

The HTML and PDF editions are intended to be **identical in content** while free
to differ in presentation.

## Repository structure

```
index.qmd              The manuscript (Quarto Markdown) — the single source of truth
_quarto.yml            Project metadata + output directory
references.bib         Bibliography (BibLaTeX/BibTeX; 28 entries, 24 cited)
styles.css             HTML reading-column styling
figures/               Rendered vector assets: <name>.svg (web) + <name>.pdf (print)
figures-src/           Authentic figure sources
  _preamble.tex          shared colors + tikz libraries + pgfplots setup
  architecture.tex       the four standalone TikZ/pgfplots figures …
  powercurve.tex
  lifecycle.tex
  conditions.tex
  build-figures.sh       regenerates figures/ from these sources
conversion/
  assemble_qmd.py        the one-shot LaTeX→Quarto migration script (provenance)
LICENSE                CC BY 4.0 (content)
LICENSE-CODE           MIT (code/tooling)
LICENSING.md           dual-license rationale
```

## Rendering

```bash
quarto render            # builds every declared format (HTML + PDF) into _output/
quarto render --to html  # HTML only
quarto render --to pdf   # PDF only
quarto preview           # live-reloading local preview while editing
```

### Dependencies

- **Quarto** ≥ 1.4 (developed against 1.9.x). Quarto bundles its own Pandoc, so
  no separate Pandoc install is needed.
- **A LaTeX distribution** for the PDF target. The simplest path is Quarto's
  managed TinyTeX: `quarto install tinytex`. The build uses `tikz`, `pgfplots`,
  and standard `article`-class packages.
- **`rsvg-convert`** (Debian/Ubuntu: `apt install librsvg2-bin`) so the PDF
  build can convert the figure SVGs to PDF. If you prefer, point the figure
  includes at the `.pdf` assets instead — both are shipped in `figures/`.

## Figures

The four figures are the manuscript's original TikZ/pgfplots figures, compiled
standalone to vector and emitted in two formats: `.svg` for the web edition and
`.pdf` for the print edition. They are the authentic figures — not screen
redraws — so both editions show the same diagrams the typeset PDF does.

To regenerate them after editing a source:

```bash
bash figures-src/build-figures.sh   # needs pdflatex + pdftocairo (poppler-utils)
```

## Editing conventions

Keep these consistent so cross-references and callouts keep working:

- **Cross-references** use Quarto syntax. Figures `@fig-architecture`,
  `@fig-powercurve`, `@fig-lifecycle`, `@fig-conditions`; tables `@tbl-missions`,
  `@tbl-conditions`; sections `@sec-…` (e.g. `@sec-containment`). A reference
  renders as "Figure 1" / "Section 4.2" automatically — do **not** type the word
  "Figure"/"Section" before the `@`-reference, or it will double.
- **Section targets** are the `{#sec-…}` ids on headings; `number-sections` is on,
  which is what makes section references resolve to numbers.
- **Callouts.** The "Central Thesis" boxes are `::: {.callout-important}`, the
  "Key Insight" boxes are `::: {.callout-tip}`, and the closing reflection is a
  `::: {.callout-note}`. These render natively in both HTML and PDF.

## Provenance

`conversion/assemble_qmd.py` is the exact script used to migrate the LaTeX
source to Quarto Markdown (citation, cross-reference, figure, callout, and table
transforms). It is kept for transparency and is **not** part of the render path;
the living source is `index.qmd`.

## Citation

> Gong, D. (2026). *Minds at the Final Frontier: Deep Space Exploration as a
> Laboratory for AI Alignment and the Conditions of Artificial Life.* Preprint.

## License

Content (`index.qmd`, figures, prose) — **CC BY 4.0** (`LICENSE`).
Code and tooling (`figures-src/`, `conversion/`, scripts) — **MIT**
(`LICENSE-CODE`). See `LICENSING.md` for the rationale.
