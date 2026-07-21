# Artifacts Summary — Lohani et al. 2019 (arXiv:1901.03343)

Replication of *Quantum skyrmions in frustrated ferromagnets* (PRX 9, 041063).
**Verdict: REPLICATED** — core ED claim (many-magnon bound state, $E_0^B<0$) + quantitative anchor
($C_\perp=0.73 \in [0.6,0.8]$) + the paper's headline dynamical claim (exponentially small
skyrmion↔antiskyrmion **tunneling splitting**, $\Delta_{\rm tun}$ down to $\sim10^{-14}$, shown by
finite-size scaling to $N=37$). Coverage ~7/10, Agreement ~8/10.

## 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-lohani2019.pdf` | present (2.2 MB) |
| 2 | Marker extraction | `extraction/marker.md` | **interim** (pdftotext -layout; marker absent) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | **interim** (pdftotext raw + hand LaTeX; nougat absent) |
| 4 | Detailed report | `report/REPORT.tex` | complete |
| 5 | Open questions | `report/open_questions.json` | 5 heavy Qs {question, why_it_matters, next_step} + next_steps |
| 6 | Workflow | `report/workflow.md` | complete (tools/versions/effort) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| — | Evidence | `report/evidence/` | result JSON + ED code |
| — | Work / scratch | `work/` | ED code + result JSON |

## Evidence traces

| File | What it is |
|------|-----------|
| `report/evidence/lohani2019_result.json` | Full numeric output: 7-site field sweep, binding analyses ($J_2=0.5,0.7$), 19-site flake up to $N_f=6$, per-sector $E_0^B$ and $C_\perp$, **plus the `finite_size_tunneling_splitting` FSS section** (N=7,19,37 low-lying spectra, tunneling splitting, C_perp, binding), verdict block. |
| `report/evidence/lohani_ed.py` | From-scratch ED code (frozen copy). Fixed-$S_z$ basis, sparse H, `eigsh`, binding + $C_\perp$ + chirality probes. |
| `report/evidence/lohani_fss.py` | COVERAGE-FLIP FSS driver: larger-flake sparse-Lanczos ED (N up to 37), $k>1$ low spectra for the tunneling splitting, vectorized $C_\perp$. |
| `report/evidence/lohani_fss_result.json` | Raw FSS output: per-flake per-$N_f$ low spectra, $\Delta_{\rm tun}$, $C_\perp$, binding; the $N_f=4$ splitting-vs-$N$ table. |

## Key numbers (from evidence JSON)

| Quantity | Value | Paper | Match |
|----------|-------|-------|-------|
| Min binding $E_0^B$, 7-site $J_2{=}0.5$ | $-0.599$ | $<0$ (bound) | ✓ |
| Min binding $E_0^B$, 7-site $J_2{=}0.7$ | $-0.700$ | $<0$ (bound) | ✓ |
| Min binding $E_0^B$, 19-site $J_2{=}0.5$ | $-0.217$ | $<0$ (bound) | ✓ |
| Max $C_\perp$, 19-site ($N_f{=}4$) | **0.73** | 0.6–0.8 (Figs. 2,5) | ✓ |
| **Tunneling splitting $\Delta_{\rm tun}$, N=7 (no skyrmion)** | $\sim0.23$ | generic spacing | ✓ (no skyrmion) |
| **Tunneling splitting $\Delta_{\rm tun}$, N=19/37 skyrmion sectors** | **$\sim10^{-2}$ → $10^{-14}$** | exponentially small (abstract) | ✓ |
| **$N_f\bmod3$ selection rule** | $N_f{=}2\bmod3$ exactly degenerate; else finite split | Figs. 7–8 | ✓ |
| Largest flake reached | **N=37** (dim ≈ 436k) | 31-site cluster | ✓ (larger) |
| Raw scalar chirality $\langle\chi\rangle$ | 0 (exact) | not used (Sz degeneracy) | expected-zero |
| Runtime (base + FSS) | ~9.2 s + ~74 s | — | — |

## Reproduce
```
/home/stevens/comfyui-env/bin/python work/lohani_ed.py    # base binding + Cperp (~9 s)
/home/stevens/comfyui-env/bin/python work/lohani_fss.py   # larger-flake FSS + tunneling splitting (~74 s)
```

## Notes
- `marker`/`nougat` unavailable on host → artifacts 2,3 are pdftotext-based interim extractions,
  clearly flagged in-file. Regenerate when the binaries are installed.
- `.gitignore` in the replication repo tracks `report/`, `extraction/`, `report/evidence/` but not
  `paper.pdf` or `work/` — the deliverables above are the tracked set.
