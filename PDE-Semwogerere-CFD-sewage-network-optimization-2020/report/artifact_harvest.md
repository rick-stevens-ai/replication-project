# Artifact Harvest

## Paper (primary source)
- URL: https://doi.org/10.24297/jam.v18i.8345
- Direct PDF: https://rajpub.com/index.php/jam/article/download/8345/7894
- Local: `work/paper.pdf` (406 604 bytes, 10 pages, PDF 1.7)
- Text extraction: `work/paper.txt` (`pdftotext -layout`)
- Access: OA-PDF via Journal of Advances in Mathematics (RAJPUB / Cloudflare)
- Fetched 2026-07-04

## Code / data mentioned in paper
- OpenFOAM (open-source, C++ CFD library). Paper cites version implicitly
  as "the open source CFD package OpenFOAM".  We used OpenFOAM 1906 on uicgpu.
- interFoam solver (multiphase VOF).  Standard OpenFOAM binary
  (`/usr/bin/interFoam`, package `openfoam` 1906.191111+dfsg1-2build1 on
  Ubuntu-based uicgpu).
- No case files, no mesh, no source code, no numerical output tables and no
  supplementary data are released by the paper.  Reproduction requires
  independently setting up the OpenFOAM case from the equations and geometry
  parameters given in text (L = 20 m, D = 0.5 m, k-ε RAS, VOF, `interFoam`).

## Independent inputs
- Manning's equation constants: n = 0.013 (concrete/UPVC), v_min = 0.60 m/s
  (Metcalf & Eddy / EPA sanitary-engineering standard self-cleansing velocity).
- Fluid properties: water ν = 1e-6 m²/s, ρ = 1000 kg/m³; air ν = 1.48e-5 m²/s,
  ρ = 1 kg/m³; σ = 0.07 N/m; g = 9.81 m/s².

## Runtime environment
- Local (CherryRd): Python 3 stdlib only.
- uicgpu (Ubuntu, 8×A100): OpenFOAM 1906 apt package.  Case at
  `~/replicate/pde-semwogerere-2020/pipe_case/`.
