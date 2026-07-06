# Replication Queue — Prioritized 2026-05-26
*Source: PDE-adjacency analysis vs AI ATLAS (see `~/Dropbox/XFER/replication-atlas/PDE_PRIORITY_2026-05-26.md`)*
*Owner: Ollie | Decision: Rick (additions/swaps)*

## Why this queue exists
The AI ATLAS has 10 PDE-core problems. Our 23 PDE/Fluids replications heavily back 3 of them (P076 turbulence closures, P071 fusion plasma, P078 reactor thermal-hydraulics) and **leave 4 with zero direct replication backing**:
- P021 Ice-sheet basal friction
- P007 GRMHD / EHT black-hole imaging
- P001 Dark-matter / galaxy-bias cosmological emulator
- P080 Tsunami / storm-surge hazard reanalysis

This queue puts those 4 gap-fills first, plus 2 medium-gap reinforcements.

---

## Tier 1 — PDE Gap-fills (HIGH PRIORITY)

### Q1: Ice-sheet basal friction inversion (→ AI ATLAS P021)
- **Candidate paper**: Brinkerhoff et al. 2021, "Constraining subglacial processes from surface velocity observations using surrogate-based Bayesian inference" (*The Cryosphere*, DOI: 10.5194/tc-15-1731-2021), OR Jouvet 2023, "Inversion of a Stokes glacier flow model emulated by deep learning" (*Journal of Glaciology*, DOI: 10.1017/jog.2022.41)
- **Why**: First closes a 0-replication gap; both papers have public code (Brinkerhoff: `pism`-coupled emulator; Jouvet: IGM glacier-flow framework with NN, https://github.com/jouvetg/igm).
- **Replication path**: Run IGM on a small Antarctic catchment (Pine Island or Thwaites subdomain, ~10 km grid). Single A100 on uicgpu, ~6–8 h.
- **Effort tier**: Medium (6–10 h subagent).
- **Original-effort estimate (when this paper is replicated)**: ~200–500 GPU-hr, ~50–200 GB.

### Q2: GRMHD black-hole imaging (→ AI ATLAS P007)
- **Candidate paper**: Porth et al. 2019, "The Event Horizon General Relativistic Magnetohydrodynamic Code Comparison Project" (*ApJS* 243, arXiv:1904.04923), OR a single-code KORAL or HARMPI benchmark paper (Sadowski/Chael KORAL papers, https://github.com/achael/koral; or Chatterjee+Liska 2024 BHEX).
- **Why**: GRMHD is the modeling backbone of every EHT science paper. Code comparison paper is the perfect anchor — small reproducible test problems.
- **Replication path**: Build HARMPI (https://github.com/atchekho/harmpi), run the standard Fishbone-Moncrief torus test in 2D, then 3D MAD test. CPU-side OK for 2D; 3D needs GPU. uicgpu single A100, ~8–12 h.
- **Effort tier**: Medium-Heavy (8–14 h subagent).
- **Original-effort estimate**: 10,000–50,000 GPU-hr per full M87 image library, ~1–10 TB.

### Q3: Cosmological emulator (→ AI ATLAS P001)
- **Candidate paper**: Villaescusa-Navarro et al. 2022, "The CAMELS Multifield Data Set: Learning the Universe's Fundamental Parameters with Artificial Intelligence" (*ApJS* 259, DOI: 10.3847/1538-4365/ac5ab0), OR a Quijote emulator paper.
- **Why**: Closes the dark-matter / large-structure emulator gap. CAMELS data is fully public (https://camels.readthedocs.io). Emulator architectures are mid-sized CNN / GAN.
- **Replication path**: Download 1 CAMELS LH-set realization (~50 GB), train a small CNN emulator for ΩM/σ8 inference, compare to paper's accuracy. uicgpu single A100, ~4–6 h.
- **Effort tier**: Light-Medium (4–8 h subagent).
- **Original-effort estimate**: 200–1000 GPU-hr (CAMELS sim suite is enormous — paper-side training is moderate, but generating CAMELS itself is large).

### Q4: Tsunami / storm-surge surrogate (→ AI ATLAS P080)
- **Candidate paper**: Makarynskyy 2024 (egusphere preprint 2026-1909), "A Factorized Fourier Neural Operator Surrogate for Basin-scale Tsunami Simulations", OR Lee et al. 2025 (*Coastal Engineering*, S0378383925000729), "Neural network-based surrogate for probabilistic tsunami inundation".
- **Why**: Closes the only PDE-core gap with score>0. F-FNO is in the FNO family we already understand from PDE-jax-cfd / PDE-koopman-no work.
- **Replication path**: Use a small-region COMCOT or GeoClaw dataset (the F-FNO paper uses synthetic basin sims). Train F-FNO on ~100 scenarios, evaluate generalization. uicgpu single A100, ~4–6 h.
- **Effort tier**: Light (4–6 h subagent).
- **Original-effort estimate**: 500–2000 GPU-hr training + 100–500 simulator-hr for data, ~10–100 GB.

---

## Tier 2 — Reinforcement picks (MEDIUM PRIORITY)

### Q5: Cloud/convection parameterization (→ AI ATLAS P018, currently medium-only coverage)
- **Candidate paper**: Yuval & O'Gorman 2020 (*Nat. Commun.* 11, 3295), "Stable machine-learning parameterization of subgrid processes for climate modeling at a range of resolutions", OR Rasp et al. 2018 (*PNAS*) "Deep learning to represent subgrid processes in climate models".
- **Why**: Direct domain match. Currently P018 only has indirect support from PDE-latent-spectral and 2587579 (architecture reuse).
- **Replication path**: Yuval/O'Gorman code is on GitHub (https://github.com/janniyuval/keras_matlab_compatible). Standard TF/PyTorch port + small train run.
- **Effort tier**: Light-Medium (4–8 h subagent).

### Q6: Wind-farm LES + control (→ AI ATLAS P077, currently medium-only coverage)
- **Candidate paper**: A SOWFA-based LES paper, e.g., Stevens, Gayme & Meneveau 2014/2015 (*JRSE*) or a Munters 2018 wake-control paper.
- **Why**: Direct domain match. P077 currently has zero wind-farm-specific replication.
- **Replication path**: SOWFA needs OpenFOAM 8 + custom solvers — heavier setup. May be better as a surrogate-only paper (LES → NN surrogate, smaller scope).
- **Effort tier**: Heavy (10–16 h subagent, OpenFOAM dependency chain).

---

## Tier 3 — Out of PDE-priority scope (DO NOT pick from this round)

Already-saturated AI ATLAS problems — adding more replications here yields diminishing returns until the gap-fills land:
- **P076 turbulence closures** — 14 replications already
- **P071 fusion plasma** — 3 strong replications (plus 2587945 ELM forecaster pending)
- **P078 reactor thermal-hydraulic** — anchored by 1559043

---

## Suggested execution order

| Order | Paper | Reason |
|---|---|---|
| 1 | **Q3 CAMELS** | Lightest effort, immediate dark-matter-emulator gap fill |
| 2 | **Q4 F-FNO tsunami** | Light effort, only PDE-core gap with any backing today |
| 3 | **Q1 IGM ice-flow** | Medium effort, totally new domain for the corpus |
| 4 | **Q2 HARMPI / KORAL** | Medium-heavy, but fills a strategically important EHT gap |
| 5 | **Q5 Yuval-O'Gorman climate** | Reinforce P018 once gap-fills land |
| 6 | **Q6 wind-farm LES** | Heavy setup — only after Q1–Q5 |

Estimated total subagent budget (Q1–Q4): **~22–36 h** of compute across 4 papers. Tier-2 (Q5+Q6) adds another ~14–24 h.

---

## After this round
Once Q1–Q4 are done, **all 10 AI ATLAS PDE-core problems will have ≥1 direct replication match**. That's the point at which the Atlas re-estimation pass (the A/B/C question from this morning) becomes most valuable — every PDE-core entry has a defensible per-paper original-effort number from a read paper, not a heuristic.

## Decisions log
- **2026-05-26 15:45 CDT — Rick approved the 6-paper queue as-is.** Execution order Q3→Q4→Q1→Q2→Q5→Q6 confirmed.
- **Sub-decisions (Ollie's defaults, override anytime):**
  - Q1 → **Jouvet 2023 IGM** (simpler infra, single A100, public Python codebase at https://github.com/jouvetg/igm). Override to Brinkerhoff PISM if you want deeper inverse-Bayesian methodology.
  - Q2 → **Single-code HARMPI benchmark** (https://github.com/atchekho/harmpi) — Fishbone-Moncrief torus tests, 2D then 3D MAD. Override to Porth 2019 code-comparison if you want breadth over depth.
  - Q6 → **Hold until Q1–Q5 land** AND check whether existing Aurora OpenFOAM builds make wind-farm SOWFA feasible without a new dependency stack.

## Still-open questions
- (none blocking — proceeding with defaults)

## Decision update — 2026-05-28 09:32 CDT
Rick: "lets skip the climate papers."

Operational interpretation:
- Do **not** pursue further climate-paper follow-up work from this queue unless explicitly reopened.
- Yuval-O'Gorman 2020 stays closed as PARTIAL / DATA-BLOCKED; do not send the author data-request email by default.
- Rasp 2018 stays closed as REPLICATED methodology / PARTIAL magnitude; no upgrade run on full climate-data variants.
- Future replication batches should prefer non-climate themes unless Rick says otherwise.
