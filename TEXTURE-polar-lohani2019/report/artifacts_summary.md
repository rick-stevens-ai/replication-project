# Artifacts Summary — Lohani et al. 2019 (arXiv:1901.03343)

Replication of *Quantum skyrmions in frustrated ferromagnets* (PRX 9, 041063).
**Verdict: REPLICATED** — core ED claim (many-magnon bound state, $E_0^B<0$) + quantitative anchor
($C_\perp=0.73 \in [0.6,0.8]$). Coverage ~6–7/10, Agreement ~8/10.

## 8-artifact completion bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-lohani2019.pdf` | present (2.2 MB) |
| 2 | Marker extraction | `extraction/marker.md` | **interim** (pdftotext -layout; marker absent) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | **interim** (pdftotext raw + hand LaTeX; nougat absent) |
| 4 | Detailed report | `report/REPORT.tex` | complete |
| 5 | Open questions | `report/open_questions.json` | 5 heavy Qs + next_steps |
| 6 | Workflow | `report/workflow.md` | complete (tools/versions/effort) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| — | Evidence | `report/evidence/` | result JSON + ED code |
| — | Work / scratch | `work/` | ED code + result JSON |

## Evidence traces

| File | What it is |
|------|-----------|
| `report/evidence/lohani2019_result.json` | Full numeric output: 7-site field sweep, binding analyses ($J_2=0.5,0.7$), 19-site flake up to $N_f=6$, per-sector $E_0^B$ and $C_\perp$, verdict block. |
| `report/evidence/lohani_ed.py` | From-scratch ED code (frozen copy). Fixed-$S_z$ basis, sparse H, `eigsh`, binding + $C_\perp$ + chirality probes. |

## Key numbers (from evidence JSON)

| Quantity | Value | Paper | Match |
|----------|-------|-------|-------|
| Min binding $E_0^B$, 7-site $J_2{=}0.5$ | $-0.599$ | $<0$ (bound) | ✓ |
| Min binding $E_0^B$, 7-site $J_2{=}0.7$ | $-0.700$ | $<0$ (bound) | ✓ |
| Min binding $E_0^B$, 19-site $J_2{=}0.5$ | $-0.217$ | $<0$ (bound) | ✓ |
| Max $C_\perp$, 19-site ($N_f{=}4$) | **0.73** | 0.6–0.8 (Figs. 2,5) | ✓ |
| Raw scalar chirality $\langle\chi\rangle$ | 0 (exact) | not used (Sz degeneracy) | expected-zero |
| Runtime | ~9.2 s | — | — |

## Reproduce
```
/home/stevens/comfyui-env/bin/python work/lohani_ed.py   # writes lohani2019_result.json (~9 s)
```

## Notes
- `marker`/`nougat` unavailable on host → artifacts 2,3 are pdftotext-based interim extractions,
  clearly flagged in-file. Regenerate when the binaries are installed.
- `.gitignore` in the replication repo tracks `report/`, `extraction/`, `report/evidence/` but not
  `paper.pdf` or `work/` — the deliverables above are the tracked set.
