import re

raw = open('body_raw.md').read()
tex = open('/home/claude/repo/manuscript/frontier_minds_v2.tex').read()

# ---------- 1. abstract from tex (minimal, faithful inline conversion) ----------
m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)
abs = m.group(1)
abs_paras = []
for para in re.split(r'\n\s*\n', abs.strip()):
    p = para.replace('\\noindent','').strip()
    p = re.sub(r'\\textit\{(.*?)\}', r'*\1*', p)
    p = p.replace('---','—').replace('\\&','&').replace('~',' ')
    p = re.sub(r'\s+', ' ', p).strip()
    if p: abs_paras.append(p)
abstract_yaml = '\n'.join('  ' + l for l in abs_paras)  # indented block scalar

# ---------- 2. slice body: from AI Disclosure to end ----------
start = raw.find('# AI Assistance Disclosure')
body = raw[start:]

# ---------- 3. cross-reference links -> Quarto @refs ----------
# [N](#sec:name){reference-type="ref" reference="sec:name"} -> @sec-name
body = re.sub(
    r'\[[^][]*\]\(#(sec|fig):([A-Za-z0-9_-]+)\)\{reference-type="ref"\s+reference="(?:sec|fig):[A-Za-z0-9_-]+"\}',
    lambda m: '@%s-%s' % (m.group(1), m.group(2)),
    body)
# strip redundant leading words now duplicated by @ref (Quarto adds "Section"/"Figure")
body = re.sub(r'(Sections?|Figures?)~?\s*(?=@(?:sec|fig)-)', '', body)

# ---------- 4. figure includes: .pdf->.svg, fig:->fig-, drop width ----------
def figfix(m):
    cap, name = m.group(1), m.group(2)
    return '![%s](figures/%s.svg){#fig-%s}' % (cap, name, name)
body = re.sub(r'!\[(.*?)\]\(figures/([a-z]+)\.pdf\)\{#fig:[a-z]+[^}]*\}', figfix, body, flags=re.S)

# ---------- 5. remaining id attributes: sec:/fig: -> sec-/fig- ----------
body = body.replace('{#sec:', '{#sec-').replace('{#fig:', '{#fig-')

# ---------- 6. callout/insight/mdframed divs -> Quarto callouts ----------
def box(divname, calloutcls, default_title):
    global body
    pat = re.compile(r'^::: %s\n(.*?)^:::\s*$' % divname, re.S | re.M)
    def repl(m):
        inner = m.group(1).strip('\n')
        title = default_title
        # lift a leading **Label:** or **Label** as the callout title
        lm = re.match(r'\s*\*\*(.+?):?\*\*\s*(.*)', inner, re.S)
        if lm:
            title = lm.group(1).strip()
            inner = lm.group(2).lstrip()
        return '::: {.%s title="%s"}\n%s\n:::' % (calloutcls, title, inner)
    body = pat.sub(repl, body)

box('callout', 'callout-important', 'Central Thesis')
box('insight',  'callout-tip',       'Key Insight')
box('mdframed', 'callout-note',       'A Final Reflection')

# ---------- 7. tables: clean ****x**** -> **x**, add ids ----------
body = body.replace('****', '**')
# give the two table captions Quarto ids (by their caption text)
body = re.sub(r'(:\s*Summary of mission parameters[^\n]*)', r'\1 {#tbl-missions}', body)
body = re.sub(r'(:\s*Comparison of alignment-relevant[^\n]*)', r'\1 {#tbl-conditions}', body)

# ---------- 8. assemble YAML + epigraph + body ----------
yaml = f'''---
title: "Minds at the Final Frontier"
subtitle: "Deep Space Exploration as a Laboratory for AI Alignment and the Conditions of Artificial Life"
author:
  - name: "Donglai Gong"
    affiliations:
      - name: "Virginia Institute of Marine Science, William & Mary"
date: "April 2026"
keywords: [AI alignment, deep space exploration, philosophy of mind, artificial life, autonomous systems, AI safety, existential risk]
abstract: |
{abstract_yaml}
bibliography: references.bib
number-sections: true
crossref:
  fig-title: Figure
  tbl-title: Table
format:
  html:
    toc: true
    toc-depth: 3
    theme: cosmo
    fig-cap-location: bottom
    css: styles.css
  pdf:
    documentclass: article
    papersize: letter
    geometry: margin=1.1in
    toc: true
    number-sections: true
    fig-cap-location: bottom
    colorlinks: true
---

> "The question is not whether intelligent machines can have any emotions, but whether machines can be intelligent without any emotions."
> — Marvin Minsky

> "Exploration is not a choice, really; it's an imperative."
> — Carl Sagan

> "I want to live, however briefly, knowing that my life is finite. Mortality gives meaning to human life. Peace, love, friendship. These are precious because we know they cannot endure."
> — Lt. Cmdr. Data, *Star Trek: Picard*, "Et in Arcadia Ego, Part 2"

'''

open('index.qmd','w').write(yaml + body)

# ---------- report ----------
print("=== assembly report ===")
print("abstract paras:", len(abs_paras))
print("@sec/@fig refs:", len(re.findall(r'@(?:sec|fig)-', body)))
print("remaining colon refs (should be 0):", len(re.findall(r'#(?:sec|fig):', body)))
print("figure includes (.svg):", len(re.findall(r'figures/\w+\.svg', body)))
print("Quarto callouts:", len(re.findall(r'::: \{\.callout-', body)))
print("leftover raw divs (should be 0):", len(re.findall(r'^::: (callout|insight|mdframed|titlepage)', body, re.M)))
print("tbl ids:", len(re.findall(r'#tbl-', body)))
print("index.qmd bytes:", len(open('index.qmd').read()))
