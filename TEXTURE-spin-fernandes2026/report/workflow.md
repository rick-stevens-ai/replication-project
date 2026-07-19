# Workflow --- fernandes2026 (arXiv:2606.26239) Hall viscosity replication

## Pipeline
`acquire -> parse -> extract-recipe -> build -> run -> compare -> report`

## 1. Acquire
- Source PDF already in corpus: `textures-spin-fernandes2026.pdf` (2.0 MB, arXiv:2606.26239v1, 24 Jun 2026).

## 2. Parse (text extraction)
- **Tool used:** `pdftotext` (poppler) --- both `-layout` and raw reading-order.
- **marker / nougat NOT installed** on this host. Per the
  `computational-replication-execution` skill, pdftotext is the documented interim
  fallback for artifacts 2+3. The `extraction/marker.md` and `extraction/nougat.mmd`
  files carry explicit headers noting this, with the exact regeneration commands.
- Equation rendering is degraded (Unicode math breakage is a known pdftotext limit);
  the authoritative equation transcriptions (Eqs. 1-13, SM parameters) were done by
  hand into `report/REPORT.tex`.

## 3. Extract recipe (method + parameters)
Read by hand from the paper body (no LLM extraction call needed --- the model,
Hamiltonian, and parameters are fully stated in the main text + Fig. 2 caption):
- **Method:** adiabatic (quasi-static) Kubo, strain-space Berry curvature. Eqs. (5)-(6).
- **Model:** tetragonal d-wave altermagnet, Lieb lattice, 4x4 tau(sublattice) x sigma(spin).
- **Params (SM, Fig. 2; t1=1):** t2=t1/2, td=2t1, lambda=2t1, J=t1, phi=phi_c/2=4,
  phi_c=4td/J=8, coupling constants g_i = alpha*hopping with alpha=8.
- **Headline claim:** eta^H ~ order 10 hbar/v_uc -> 8.15 uPa*s (v_uc = (5 A)^3).

## 4. Build (from-scratch code)
- `work/fernandes2026_replicate.py` (also in `report/evidence/`). numpy only, ~125 lines.
- Kronecker-product tau x sigma Hamiltonian + A1g/B2g strain-coupling matrices;
  band-basis rotation; strain-space Berry curvature with near-degeneracy masking
  (|dE| < 1e-9); Fermi-weighted BZ average.
- No public author code exists --- this is an independent reimplementation.

## 5. Run
- **Host:** local spark node (small 4x4 matrices --- theory/model lane, no GPU/HPC needed).
- **Python:** `/home/stevens/comfyui-env/bin/python` (numpy).
- **Cost:** converges instantly; full run (N=24->160 + mu sweep + phi sweep) ~3 s wall.
- SAVE-EARLY discipline: JSON written after every grid size.

## 6. Compare
- eta^H(mu=0) = 8.41 hbar/v_uc = 7.10 uPa*s  vs  paper 8.15 uPa*s (order 10). Within ~13%.
- Conversion anchor: conv = hbar/a0^3/1e-6 = 0.8437 uPa*s per (hbar/v_uc), a0 = 5 A.
- Qualitative cross-checks: eta^H proportional to phi (Fig. 2f); insulating-window peak
  (Fig. 2e); equal-sign d-wave relation eta_xxxy = eta_yyxy (vs FM opposite sign).

## 7. Report
- 8-artifact package (this directory). Verdict REPLICATED, Coverage 7/10, Agreement 9/10.

## Tools / versions
| Tool | Version / note |
|------|----------------|
| pdftotext (poppler) | system `/usr/bin/pdftotext` (interim for marker/nougat) |
| Python | `/home/stevens/comfyui-env/bin/python` |
| numpy | stack in comfyui-env |
| marker / nougat | NOT installed --- pdftotext fallback used |
| compute | local spark node (CPU, 4x4 matrices) |

## Effort estimate
- Physics build + run + convergence: ~2-3 hours (already complete before this packaging pass).
- Packaging (8 artifacts + report): ~1 hour.
- Total replication: ~half a day of focused work for a clean quantitative match.
