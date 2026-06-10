#!/usr/bin/env bash
# Regenerate the figure assets (PDF for print, SVG for web) from the authentic
# TikZ/pgfplots sources. Run from the repo root: bash figures-src/build-figures.sh
# Requires: pdflatex (TeX Live, with tikz + pgfplots), pdftocairo (poppler-utils).
set -e
cd "$(dirname "$0")"
mkdir -p ../figures
for f in architecture powercurve lifecycle conditions; do
  echo "building $f ..."
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
  pdftocairo -svg "$f.pdf" "../figures/$f.svg"
  cp "$f.pdf" "../figures/$f.pdf"
done
rm -f ./*.aux ./*.log
echo "done: ../figures/{architecture,powercurve,lifecycle,conditions}.{pdf,svg}"
