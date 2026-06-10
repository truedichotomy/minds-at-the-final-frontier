# Minds at the Final Frontier — Quarto edition

*Deep Space Exploration as a Laboratory for AI Alignment and the Conditions of Artificial Life*

📖 **Read the web edition:** <https://truedichotomy.github.io/minds-at-the-final-frontier/>

This repository is the **Quarto edition** of the manuscript. It holds a single
semantic source (`minds-at-the-final-frontier.qmd`) from which both a web edition (HTML) and a
print edition (PDF) are rendered by [Quarto](https://quarto.org). It is a
standalone repository, deliberately separate from the original hand-rolled
LaTeX→HTML build, so the two toolchains never entangle.

The design goal is clean separation of the three layers:

- **content** — prose, structure, cross-references, citations live in `minds-at-the-final-frontier.qmd`;
- **figures** — standalone vector assets in `figures/`, generated from authentic
  TikZ/pgfplots sources in `figures-src/`;
- **presentation** — per-format options in `_quarto.yml` / the document front
  matter, plus `styles.css` and the HTML title-block partial (`partials/`) for
  the web edition, and the LaTeX title page (`tex/`) for print.

The HTML and PDF editions are intended to be **identical in content** while free
to differ in presentation.

## Repository structure

```
minds-at-the-final-frontier.qmd              The manuscript (Quarto Markdown) — the single source of truth
_quarto.yml            Project metadata + output directory
references.bib         Bibliography (BibLaTeX/BibTeX; 28 entries, 24 cited)
styles.css             HTML reading-column styling
partials/
  title-block.html       custom HTML title block (subtitle, disclaimer)
tex/
  titlepage.tex          custom LaTeX title page for the PDF edition
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
.github/workflows/
  publish.yml            CI: render HTML + PDF and deploy to GitHub Pages on push to main
CLAUDE.md              Orientation notes for AI coding assistants
LICENSE                CC BY 4.0 (content)
LICENSE-CODE           MIT (code/tooling)
LICENSING.md           dual-license rationale
_output/               Render target (HTML + PDF) — git-ignored, built on demand
```

Rendered output (`_output/`) and Quarto's caches are git-ignored — the source is
the source of truth, and the published site is rebuilt by CI (see **Publishing**).
The committed vector files in `figures/` are the one deliberate exception: they
are slow to regenerate, so they are versioned as a build-of-record.

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

## Publishing

The manuscript is published to **GitHub Pages** automatically. On every push to
`main`, `.github/workflows/publish.yml` renders both editions and deploys them to:

<https://truedichotomy.github.io/minds-at-the-final-frontier/>

The web page is served as `index.html` (so the URL above resolves with no
redirect — see the `output-file` override in the front matter), with a
"Download PDF" link to the print edition, published alongside as
`minds-at-the-final-frontier.pdf`. Building the PDF needs a LaTeX toolchain
(TinyTeX) and an SVG rasteriser (librsvg), both installed by the workflow; expect
builds of ~2–3 min.

The deployment uses GitHub's native Pages action (no `gh-pages` branch). It is
enabled once under **Settings → Pages → Source: GitHub Actions**; after that,
publishing is fully automatic.

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
the living source is `minds-at-the-final-frontier.qmd`.

## Citation

> Gong, D. (2026). *Minds at the Final Frontier: Deep Space Exploration as a
> Laboratory for AI Alignment and the Conditions of Artificial Life.* Preprint.

## License

Content (`minds-at-the-final-frontier.qmd`, figures, prose) — **CC BY 4.0** (`LICENSE`).
Code and tooling (`figures-src/`, `conversion/`, scripts) — **MIT**
(`LICENSE-CODE`). See `LICENSING.md` for the rationale.
