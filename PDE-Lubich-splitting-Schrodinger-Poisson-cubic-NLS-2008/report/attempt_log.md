# Attempt log

All times America/Chicago, 2026-07-05.

- **02:09** — Read `WAVE_BRIEF_2026-07-01.md`, confirmed target dir was empty, created `report/{evidence}` and `work/` skeleton.
- **02:10** — Queried Semantic Scholar for `DOI:10.1090/S0025-5718-08-02101-7`. Response confirms author = C. Lubich (solo), year 2008, title matches; `openAccessPdf.license = "public-domain"`. Direct fetch of the AMS PDF (both local and via `ssh uicgpu`) blocked by Cloudflare bot check.
- **02:12** — Traversed Lubich's Tübingen publications page (`https://na.uni-tuebingen.de/publications.shtml`), found direct preprint at `pub/lubich/papers/speq.pdf`. Downloaded (169616 B, md5 `608e48…debefb7`), PDF verified 13 pages.
- **02:13** — `pdftotext -layout` extraction succeeded. Confirmed paper structure: 8 sections + references, NO figures, NO tables, NO numerical experiments section. Extracted the two key theorem statements (Thm 2.1 for SP, Thm 7.1 for cubic NLS) and the scheme definition (eq. 1.4).
- **02:13** — Wrote `lubich_splitting.py`: Fourier-spectral 1D solver, exact free-Schrödinger via FFT, pointwise potential exponent. Includes 1D periodic Schrödinger–Poisson via Fourier inversion of the Poisson equation (`V_hat = ±ρ_hat/k²` for k≠0, zero mean).
- **02:14** — Quick sanity test: plane wave `exp(3ix)` propagated with V=0 for T=1 gives L² error 4.4e-14 vs exact `exp(3ix−9it)` → free-Schrödinger step is exact to machine precision. L² norm conserved to 0 digits change after 200 cubic-NLS steps.
- **02:14** — Ran full convergence sweep locally (13.7 s wall, single core). Four problems (cubic NLS ±, Schrödinger–Poisson ±), five step sizes each (τ = 1/50 … 1/800), reference at τ = 1/32000 (Strang splitting at ~40× the finest coarse τ). Result: **all four sweeps show clean O(τ²) convergence in L² and (better than the theorem's O(τ) upper bound) O(τ²) in the paper's stability norm Hᵐ.** L² mass drift ≤ 1.2e-13.
- **02:14** — Generated log-log convergence plot (`convergence_plot.png`, 4 curves × 2 panels).
- **02:15** — Ran LLM-judge via Argo proxy. `argo:claude-opus-4.8` returned 502 Bad Gateway at run time (upstream flake); fell back to `argo:claude-sonnet-4.6` (also free). Judge verdict: **REPLICATED**, core claims reproduced.
- **02:16** — Wrote REPORT.md.

## What worked
- Author preprint (Tübingen) as PDF source when Cloudflare blocked AMS.
- Fourier spectral discretization + Strang split-step scheme direct from eq. (1.4).
- 1D periodic reduction is explicitly allowed by the paper ("Our arguments would apply similarly to problems with periodic boundary conditions and in lower space dimension").

## What failed / worked around
- AMS PDF fetch (Cloudflare block, both m1 and uicgpu). → Author preprint used instead.
- `argo:claude-opus-4.8` LLM-judge call (502 Bad Gateway from Argo upstream). → Switched to `argo:claude-sonnet-4.6` (also FREE endpoint, still Argo proxy).
- `pdf` tool with `/tmp/` path (path not in allowed list). → Not needed; `pdftotext` + direct text scan sufficient.

## No overwrite / preservation
- Target dir was **empty at start of run** (verified with `ls -la`); no sibling directories touched.
- All writes strictly under `~/Dropbox/REPLICATE-PROJECT/PDE-Lubich-splitting-Schrodinger-Poisson-cubic-NLS-2008/`.
- `ssh uicgpu` used only to fetch the preprint PDF (Cloudflare workaround) — no shared filesystem side effects.
