# Artifacts summary — oh2026 p-wave OAM texture (tight-binding surrogate)

**Paper:** Oh et al., "p-wave orbital angular momentum texture in a chiral
crystal" (TaSe₄)₂I, arXiv:2605.15544v1 (2026).
**Replication type:** tight-binding / k·p model surrogate (DFT skipped).
**Verdict:** **REPLICATED** — 6/6 falsifiable checks pass.
**Self-score:** Coverage 8/10, Agreement 10/10.

## Artifact map (8-artifact bar)

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Runnable code | `work/oh2026_pwave_oam.py` | ✅ runs in ~0.4 s (numpy) |
| 2 | Extraction (prose) | `extraction/marker.md` | ✅ pdftotext -layout + provenance header (marker not installed) |
| 3 | Extraction (math) | `extraction/nougat.mmd` | ✅ hand-transcribed eqs + pdftotext appendix (nougat not installed) |
| 4 | Report | `report/REPORT.tex` | ✅ ships as source (pdflatex may be absent) |
| 5 | Open questions | `report/open_questions.json` | ✅ 5 heavy Qs {question, why_it_matters, next_step} + next_steps |
| 6 | Workflow | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |
| + | Evidence | `report/evidence/` | ✅ result JSON + code + kernel + figure |
| + | Result JSON | `work/oh2026_result.json` | ✅ SAVE-EARLY |
| + | Figure | `work/figs/oh2026_pwave_oam.png` | ✅ 6-panel texture summary |

## Headline numbers (traced to `work/oh2026_result.json` keys)

| Quantity | Value | JSON key |
|---|---|---|
| Verdict | REPLICATED | `verdict` |
| Checks passed | 6 / 6 | `n_passed` / `n_checks` |
| C1 odd-parity residual (kx) | 7.6e-15 | `checks.C1_pwave_odd_parity_Lx.odd_parity_residual_kx` |
| C1 ⟨Lx⟩ +kx / −kx | −0.866 / +0.842 | `checks.C1...mean_Lx_pos_kx / mean_Lx_neg_kx` |
| C2 enantiomer residual | 0.0 | `checks.C2_enantiomer_sign_reversal.max_\|LxA+LxB\|_over_max\|LxA\|` |
| C3 Mx / My residual | 7.6e-15 / 5.3e-15 | `checks.C3_mirror_relations.Mx_residual / My_residual` |
| C4 \|Ly\|/\|Lx\| ; \|Lz\|/\|Lx\| | 0.049 ; 0.0 | `checks.C4...` |
| C5 m=1 harmonic dominance | 4.14× ; 2 nodes | `checks.C5...m1_over_max_others / sign_nodes_around_loop` |
| C6 net OAM / net SAM | 3.27e4 | `checks.C6_OAM_gg_SAM_weak_SOC.net_OAM_over_net_SAM` |
| C6 SOC splitting | 0.019 (units of t) | `checks.C6...band_splitting` |

## Kernel credit
Occupied-state OAM-expectation workflow adapted from
`gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (A. Göbel et al., "Topological orbital
Hall effect from skyrmions," arXiv:2410.00820). Copy in `report/evidence/`.

## Reproduce block
```bash
cd ~/textures-100/corpus/textures-orbital-oh2026/work
~/comfyui-env/bin/python oh2026_pwave_oam.py
# -> work/oh2026_result.json : {"verdict":"REPLICATED","n_passed":6,"n_checks":6}
# -> work/figs/oh2026_pwave_oam.png
```

## Self-score rationale
- **Agreement 10/10** — every checked feature of the headline claim (p-wave
  oddness, enantiomer flip, mirror relations, component structure, dipolar
  harmonic, OAM≫SAM) matches the paper's qualitative predictions, and a
  physically-wrong first parameterization genuinely failed two checks (the tests
  are falsifiable, not rigged).
- **Coverage 8/10** — the reproducible symmetry-dictated model core is fully
  covered, but (a) no DFT → no material-specific node positions/band energies,
  (b) no CD-ARPES matrix-element forward model, (c) no strong-SOC OAM→SAM sweep.
  These are captured as open questions Q1/Q4/Q3.
