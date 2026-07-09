# Artifact Harvest

| Artifact | Source | Access | Size | Notes |
|---|---|---|---|---|
| Target paper (rank 75) | DOI 10.1006/JCPH.2001.6900 (Elsevier JCP) | PAYWALLED | — | "A Cartesian Grid Embedded Boundary Method for the Heat Equation on Irregular Domains", McCorquodale, Colella, Johansen 2001 |
| OA companion tech report | https://www.osti.gov/servlets/purl/878684 | OPEN (via uicgpu proxy; CherryRd blocks OSTI direct) | 702 KB, 6 pp | Schwartz, Barad, Colella, Ligocki — "A Cartesian Grid Embedded Boundary Method for the Heat Equation and Poisson's Equation in Three Dimensions" (LBNL). Same discretization family; contains the exact test problems Eq.(21)-(24) reproduced here. Saved as `work/osti878684_embedded_boundary.pdf` |
| eScholarship record (2D paper) | https://escholarship.org/uc/item/2c9253pn | metadata only (PDF 403) | — | abstract confirms method lineage |
| Extracted text | `work/osti.txt` | local (pdftotext) | 43 KB | full method + test-case equations |

## Method sources used (from the OA report)
- **Discrete FV Laplacian**, Eq. (1): divergence of face fluxes weighted by apertures.
- **Dirichlet gradient stencils**: higher-order normal-plane quadratic, Eq. (8); lower-order least-squares gradient, Eq. (10).
- **L0-stable time discretization**, Eq. (16)-(17) with the Twizell–Gumel–Arigu split (`a = 2 - sqrt(2)`).
- **Poisson test problem**, Eq. (21)-(22): `f = sin(x)sin(2y)sin(3z)` on a sphere (we use the 2D analogue `sin(x)sin(2y)` on a disk, `Delta psi = -5 psi`).
- **Heat test solution**, Eq. (23): Gaussian heat-kernel form; we use the exact 2D heat kernel `psi = 1/(4 pi (t+1)) exp(-(x^2+y^2)/(4(t+1)))` (satisfies `psi_t = Delta psi`, `f=0`), Dirichlet BC from exact, `dt = 0.5 h`, `T = 0.1875` (matching the report's moving-sphere run parameters `dt/h=0.5`, `T=0.1875`).

## Tooling
- Python 3.14, numpy 2.4.3, scipy 1.18.0, matplotlib (Agg).
- LLM judge: Argo proxy `http://127.0.0.1:44497/v1` (free), models `argo:gpt-5.2`, `argo:gpt-5.1`, `argo:claude-sonnet-4.5`, `argo:gpt-4o` (opus-4.8 returned transient 502).
