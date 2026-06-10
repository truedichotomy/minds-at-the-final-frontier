# Licensing

This repository contains two kinds of material under two different licenses.

## Content — CC BY 4.0

The manuscript text, figures, and all prose in this repository are licensed under the
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

SPDX identifier: `CC-BY-4.0`
License text: https://creativecommons.org/licenses/by/4.0/legalcode

You are free to share and adapt this material, including for commercial purposes,
provided you give appropriate credit, link to the license, and indicate if changes
were made.

**How to cite / attribute:**

> Gong, D. (2026). *Minds at the Final Frontier: Deep Space Exploration as a
> Laboratory for AI Alignment and the Conditions of Artificial Life.*
> Revision <N>, <date>. Available at <repository URL>. Licensed under CC BY 4.0.

## Code — MIT

The build tooling (the LaTeX-to-HTML converter pipeline and any scripts used to
produce the web edition) is licensed under the **MIT License**.

SPDX identifier: `MIT`

## Files

- `LICENSE` — full CC BY 4.0 text (governs content)
- `LICENSE-CODE` — full MIT text (governs the build scripts)

When a file could plausibly fall under either license, the controlling license is:
prose, figures, and `.tex`/`.md`/`.html` document sources → CC BY 4.0; `.py` build
scripts and tooling → MIT.

## Suggested README notice

```
## License

- Document content (manuscript, figures, prose): CC BY 4.0 — see LICENSE
- Build tooling (converter scripts): MIT — see LICENSE-CODE
```

## Rationale

CC BY 4.0 was chosen for the content because it enforces exactly the interest an
author has — attribution and traceable priority — while permitting the widest
possible reuse, translation, and redistribution. It is the license required by most
open-access mandates and the least likely to conflict with later journal submission.
NonCommercial (NC) and ShareAlike (SA) variants were considered and rejected: NC is
legally ambiguous and blocks legitimate reuse; SA imposes copyleft friction and can
complicate incorporation into a differently-licensed publication. MIT was chosen for
the code as a short, universally understood permissive license appropriate to small
utilities.

## Notes (verify before publishing)

- **Journal options:** CC BY is the most widely accepted preprint license, but
  confirm the prior-publication / preprint policy of any journal you may submit to.
- **Institutional IP:** University scholarly-works exceptions almost always leave
  copyright in papers with the faculty author; software can be treated differently.
  Confirm against the William & Mary IP policy, particularly for the code.
