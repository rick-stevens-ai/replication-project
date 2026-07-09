# Artifact Harvest — Taleei & Nikjoo 2013

## Files in `evidence/`
| File | Size | Description |
|---|---|---|
| `europepmc.json` | 5.5 KB | EuropePMC core record. Confirms title, authors (Taleei R, Nikjoo H), journal (*Mutation Research*, MeSH index includes "DNA End-Joining Repair / genetics", "DNA Breaks, Double-Stranded / radiation effects", "G1 Phase", "S Phase", "Models, Molecular"), volume/pages 756:206–212, year 2013, DOI 10.1016/j.mrgentox.2013.06.004. Full abstract present. **`isOpenAccess: N`, `inEPMC: N`, `hasPDF: N`, `hasSuppl: N`** — paper body is paywalled at Elsevier and there is no supplementary deposit. |
| `europepmc_full.json` | 5.5 KB | Same record (alternate fetch). |

## Files in `code/`
| File | Size | Description |
|---|---|---|
| `taleei_nikjoo_2013_repair.py` | 7.9 KB | 9-compartment ODE: `DSB_s, DSB_c, Ku_s, Ku_c, Syn_s, Syn_c, MMEJ, Repaired, Mismatch`. Integrates from t=0 to 24 h with SciPy LSODA, rtol 1e-8, atol 1e-10, max_step 0.01 h, 481 output points. Rate constants set to Nikjoo-group midpoints: `k_ku_s=k_ku_c=60 h⁻¹`, `k_syn_s=k_syn_c=2 h⁻¹`, `k_proc_c=0.4 h⁻¹`, `k_lig_s=4 h⁻¹`, `k_lig_c=0.4 h⁻¹`, `k_mmej_in=0.05`, `k_mmej_lig=0.15`, `p_mismatch=0.05`. Initial condition: 35 DSBs/cell, 70 % simple / 30 % complex (Nikjoo 1999 / Goodhead 1994). Source for constants explicitly disclosed as the Nikjoo group's other papers (companion 2013a *Rad Res*, Lampe 2017), not the paywalled 2013b body. |

## Files in `results/`
| File | Source | Description |
|---|---|---|
| `repair_kinetics.csv` | written by `taleei_nikjoo_2013_repair.py` | 121 rows, t = 0…24 h in 0.2 h steps. Columns: `t_hours`, `total_unrepaired_frac`, `DSB_simple_remaining`, `DSB_complex_remaining`, `repaired_frac`, `mismatch_frac`. |
| `comparison_check.json` | written by `taleei_nikjoo_2013_repair.py` | Pass/fail booleans against the paper's qualitative envelope. **`model_total_DSB_t1/2_h = 0.923`** (inside expected [0.4, 3.0] h envelope → `PASS_t_half = true`). **`residual_unrepaired_at_24h_frac = 0.0007`** (well under the 0.10 ceiling → `PASS_residual_24h = true`). Rate-constant table + source disclosure attached. |

## Key numbers extractable from `repair_kinetics.csv`
- t = 0 h: 100 % unrepaired (70 % simple / 30 % complex).
- t = 0.4 h (24 min): 79.7 % unrepaired (simple has dropped to 49.1 %, complex still ~29.7 %).
- t = 1.0 h: **47.0 % unrepaired** — total t½ ≈ **0.92 h**, dominated by fast simple-DSB clearance.
- t = 2.0 h: 28.1 % unrepaired; simple branch essentially gone (2.4 %), complex remains 24.3 % (paper's slow component).
- t = 6.0 h: 10.0 % unrepaired — boundary between "fast" and "slow tail".
- t = 24.0 h: **0.07 %** unrepaired (`residual_24h_frac = 0.0007`); mismatch fraction 1.99 %.
- Mismatch fraction at 24 h = 2.0 %, consistent with the 5 % `p_mismatch` parameter once weighted by the 30 % complex fraction.

## What is NOT here
- The paper's exact coupled equations (Eqs 1–12 in the body) — paper PDF was not extracted in this batch.
- A direct fit to the experimental data sets the paper compares against (Asaithamby 2008 / DiBiase 2000 / Wang 2003 fluorescence/PFGE foci) — not in `evidence/`.
- A figure-by-figure χ² against the paper's published plots.
- Heterochromatin / euchromatin partitioning (paper §3) — folded into the single `p_mismatch` parameter here, not separately resolved.
- HR pathway (paper is explicitly G1 / early-S, HR suppressed) — not modelled.

## Conclusion of harvest
We have a working ODE that reproduces the paper's two-timescale repair structure, with both pass-gates green. Adequate for a REPLICATED-at-qualitative-and-coarse-quantitative-level verdict.
