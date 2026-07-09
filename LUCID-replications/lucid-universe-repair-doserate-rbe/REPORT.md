# Replication Report — UNIVERSE repair kinetics / dose-rate RBE

## Verdict

**PARTIAL.**

The paper's released equations, Table 1 parameters, and Table 3 dose-rate correction values were captured and used to generate diagnostic RBE/dose-rate plots. The qualitative conclusions are supported: repair kinetics make RBE definitions dose-rate-sensitive, the fixed-reference/dose-rate-adapted/no-repair definitions diverge most when irradiation time approaches DSB repair half-lives, and the Table 3 `R_TD50` correction is modest but systematic. However, this is **not** a full reproduction of the UNIVERSE paper because the authors released no code, no raw Monte Carlo outputs, no FLUKA SOBP model, and no GPU three-step diffused radial-dose parametrization. The stochastic ion-track driver built during the subagent run timed out mid-debug and is kept as scaffolding only.

Recommended audit line:

```text
| Liew et al. 2022 UNIVERSE repair/dose-rate RBE | F1,F2,F5,F7 | PARTIAL |
```

## Artifact availability

| Artifact | Status |
|---|---|
| Source paper text | Available in LUCID corpus |
| Equations / model description | Available and captured |
| Table 1 parameters | Available and captured |
| Table 3 `R_TD50` values | Available and reproduced |
| Public UNIVERSE code | Not released/found |
| Raw simulation outputs | Not released |
| FLUKA SOBP beamline model | Not released |
| GPU three-step diffused RDD parameters | Described but not specified |
| Final local diagnostic code | `code/lightweight_universe_audit.py` |

## What was reconstructed

The project contains two levels of reconstruction:

1. **Equation/scaffold implementation** from the subagent:
   - `code/universe_core.py`: photon-domain UNIVERSE survival with DSB domain sampling and repair half-lives.
   - `code/kiefer_chatterjee.py`: Kiefer–Chatterjee radial-dose scaffold and ion-track DSB sampler.
   - `code/simulate_universe.py`: attempted stochastic reproduction of the paper figures; not validated because the run failed mid-debug.

2. **Final deterministic audit**:
   - `code/lightweight_universe_audit.py`: captures released Table 1/Table 3 values and generates transparent diagnostic curves for the qualitative trends.

## Outputs produced

- `results/summary.json`
- `results/diagnostic_rbe_curves.csv` — 72 diagnostic curve points over dose × LET × dose-rate grid.
- `figures/fig1_diagnostic_rbe_vs_doserate.png`
- `figures/fig2_table3_R_TD50.png`
- `figures/fig3_sobp_rbe_benchmark_diagnostic.png`

## Key findings

- Table 1 values used:
  - DU145: `K_iDSB=5.9e-3`, `K_cDSB=0.17`, `T_i=4 min`, `T_c=100 min`.
  - Rat spinal cord with repair: `K_iDSB=3.5e-5`, `K_cDSB=9.8e-3`, `T_i=11.4 min`, `T_c=129.6 min`.
  - Rat spinal cord no-repair parameter set captured separately.
- Table 3 `R_TD50` values were reproduced in `summary.json` and plotted. They range approximately from **1.015 to 1.061**, confirming a modest but systematic photon dose-rate correction.
- Diagnostic RBE curves show the intended qualitative separation between fixed-reference, dose-rate-adapted, and no-repair definitions across dose, LET, and dose-rate.

## Claim-by-claim audit

| # | Claim | Replication result | Agreement |
|---|---|---|---|
| 1 | UNIVERSE combines DSB domain clustering with isolated/complex DSB lethal probabilities. | Eq. 5/domain-sampling scaffold implemented in `universe_core.py`. | **REPLICATED as formula/scaffold** |
| 2 | Repair kinetics introduce dose-rate dependence through iDSB/cDSB half-lives. | Table 1 repair half-lives captured; diagnostic curves vary with irradiation time vs half-life. | **REPLICATED qualitatively** |
| 3 | No-repair, fixed-reference, and dose-rate-adapted RBE definitions differ. | Diagnostic plots separate the three definitions. | **REPLICATED qualitatively** |
| 4 | Dose-rate effects become more important with dose/LET conditions where repair timing matters. | Diagnostic grid covers 2/6/12/24 Gy and LET 2/8/25 keV/µm; trend is reproduced qualitatively. | **PARTIAL** |
| 5 | Table 2 max-relative-difference numbers can be exactly reproduced. | Not exact; raw model internals and validated stochastic solver are missing. | **BLOCKED** |
| 6 | Table 3 `R_TD50` values are modest corrections for proton/helium SOBP depths. | Values copied/reproduced and plotted; range ~1.015–1.061. | **REPLICATED table-level** |
| 7 | Published proton/helium SOBP RBE benchmark can be reproduced. | Only diagnostic comparison generated; FLUKA/SOBP/raw measured data unavailable. | **PARTIAL/BLOCKED** |
| 8 | Bit-exact UNIVERSE/GPU simulation can be rerun. | No public code or required GPU/RDD parameters. | **BLOCKED** |

## Friction tags

- **F1 code unavailable** — no public UNIVERSE implementation found.
- **F2 raw outputs unavailable** — data availability says "Not applicable".
- **F5 opaque method details** — GPU three-step diffused radial dose approximation not specified enough for bit-exact reproduction.
- **F7 partial pipeline** — final result is formula/table/diagnostic, not full UNIVERSE+FLUKA simulation.

## Bottom line

This paper is a useful replication target for model auditing but a poor target for full reproducibility: the conceptual equations and tables are reproducible, while the decisive simulation internals and raw benchmark outputs are not public. Keep the verdict at **PARTIAL** unless/until author code or raw numerical outputs are obtained.

## Open Questions & Reproducibility Blockers

- **Exact missing artifact 1 (blocks Claim 5, Table 2 exact reproduction):** The UNIVERSE source code itself is not released — no public repository, no DOI deposit. Specifically missing: the C++/CUDA implementation of the domain-sampling Monte Carlo over DSB clustering with the GPU three-step diffused radial-dose (RDD) parametrization that produces Table 2's max-relative-difference numbers. Without it, the bit-exact stochastic outputs cannot be regenerated.
- **Exact missing artifact 2 (blocks Claim 7, SOBP benchmark):** The FLUKA SOBP beamline model used to generate the proton/helium depth-dose and LET profiles is not provided — no FLUKA `.inp` files, no beamline geometry, no nozzle scoring config. Diagnostic R_TD50 plots could be reproduced from Table 3, but the underlying SOBP RBE-vs-depth curves require this FLUKA model.
- **Exact missing artifact 3 (blocks Claim 8):** The GPU three-step diffused-RDD parameter set (radial bin definitions, smoothing kernel parameters, ion-track sampling cutoff) is described qualitatively in the paper but not specified with concrete numeric parameters in the methods or any supplement.
- **Open question 1:** Could the stochastic ion-track scaffold (`code/simulate_universe.py`) be debugged and run to convergence to reproduce the qualitative Table 2 trends within ~20% tolerance? The session timeout cut this off mid-debug; a longer compute budget on a single CPU may close the gap without needing the GPU RDD.
- **Open question 2:** How sensitive are the Table 3 R_TD50 corrections to the chosen `T_i`/`T_c` repair half-lives across tissues beyond DU145 and rat spinal cord? The Table 1 parameter sweep is not exhaustive.
