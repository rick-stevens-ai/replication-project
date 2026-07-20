# Artifacts Summary — arXiv:1404.5920

| Artifact | Path | Description |
|---|---|---|
| Paper | `paper.pdf` | arXiv:1404.5920 (Chandra, Coleman, Flint, Phil. Mag. 2014) |
| Extraction | `extraction/marker.md` | Title/authors/venue, claims, Eqs. 1–31, quantitative anchors, chosen claims |
| Code | `code/chandra2014_replication.py` | Analytic replication of C1–C5 (numpy/scipy/matplotlib) |
| Results | `work/results.json` | Per-claim computed values + pass flags (5/5 PASS) |
| Fig C1/C3 | `figs/spin_zeros.png` | Onsager index ladder + dHvA envelope zeros at half-integers |
| Fig C4 | `figs/landau_softmode_gap.png` | √(Pc−P) longitudinal soft-mode gap |
| Fig C5 | `figs/chi3_cos4.png` | χ3(θ) numeric vs analytic cos⁴θ |
| Report | `report/REPORT.tex` (+`.pdf`) | Section-by-section write-up |
| Open questions | `report/open_questions.json` | Exactly 5 {q, basis, next_steps} |
| Workflow | `report/workflow.md` | Step-by-step method |
| Failure analysis | `report/failure_analysis.md` | Tooling gaps + scope decisions |
| Metadata | `META.json` | Machine-readable summary/verdict |

## Key results (from work/results.json)
- **C2** Δ bound: computed **0.6717 K** vs paper **0.67 K** → 0.3% error. PASS.
- **C1** Onsager index α₀ = g*m*/2m_e = **16.9** → 17 predicted spin zeros vs **16** observed. PASS (±2).
- **C3** dHvA envelope zeros at half-integer α, max deviation **0.0059**. PASS.
- **C4** spin-flop basal(HO)↔c-axis(AFM) reproduced; soft-mode gap log-log slope **0.5000**. PASS.
- **C5** χ3 ∝ cos⁴θ: numeric vs analytic RMS **1.1×10⁻⁷**. PASS.

**Score: Coverage 6/10, Agreement 10/10. Verdict: successful analytic replication (5/5 claims).**

## Out of scope (flagged, not faked)
- Full two-channel Anderson-lattice mean-field consistency curves (Figs. 3, 7).
- Resonant-nematicity LDOS prediction (Fig. 8b).
- Transverse-moment magnitude reconciliation (~0.01 μB predicted vs <0.0011 μB bound).
- No DFT (paper is analytic; DFT explicitly out of remit).
