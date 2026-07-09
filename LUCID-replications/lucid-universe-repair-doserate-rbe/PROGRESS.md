# PROGRESS LOG — LUCID UNIVERSE Repair / Dose-Rate / RBE replication

Paper: Liew et al. (2022), *Impact of DNA Repair Kinetics and Dose Rate on RBE Predictions in the UNIVERSE*, Int. J. Mol. Sci. 23, 6268. DOI: 10.3390/ijms23116268.
Source markdown: `uicgpu:/data/stevens/lucid-corpus-extracted/LUCID-papers/e43d7eda2781a793.md`.
Subagent session: `agent:main:subagent:88d6e8b9-e0d9-46c7-aeec-a43aab45d6a4` (2026-05-29).

---

## 2026-05-29 — kickoff

- Pulled full paper markdown (331 lines) from uicgpu.
- Cataloged the equations: (5) survival product, (6-9) Kiefer–Chatterjee RDD, (10) radical diffusion, (11-13) RBE definitions, (3) benchmark approximation, plus repair-kinetics Monte Carlo description (Section 5.2 final paragraphs).
- Cataloged the parameters: Table 1 (K_iDSB / K_cDSB / T_iDSB^1/2 / T_cDSB^1/2 for DU145 and rat spinal cord with/without repair), Table 2 (max relative difference fixed-reference vs no-repair RBE at 2/6/12/24 Gy × 2/8/25 keV/µm), Table 3 (dose rate, R_TD50, LET_d at 35/100/120/127 mm for proton/helium × 1/2 fractions).
- Data availability statement in the paper is **"Not applicable"** — there is no public code repository, raw simulation outputs, or FLUKA beam line model released. The replication is therefore unavoidably **formula-level / table-level**, not bit-exact reproduction.
- Cross-checked the AUDIT_PROTOCOL: this falls under "formula-only / table-level" reproduction. Will be honest about the friction tags.

## 2026-05-29 — implementation plan

Three Python modules under `code/`:
1. `universe_core.py` — homogeneous (photon) implementation of UNIVERSE: domain sampling, survival via Eq. 5, repair-kinetics Monte Carlo with N_t time steps and exponential lifetimes, plus the no-repair limiting case.
2. `kiefer_chatterjee.py` — radial dose distribution (Eqs. 6–9), effective charge, r_min, r_max, K_p, and a domain-grid track sampler that approximates the cylinder-of-cubic-domains geometry. Diffused RDD by a Gaussian-blur step-function approximation (matches the paper's three-step parametrization spirit).
3. `simulate_universe.py` — driver. Reproduces:
   - **Figure 1/2-like curves:** proton RBE vs dose-rate at LET ∈ {2, 8, 25} keV/µm, dose ∈ {2, 6, 12, 24} Gy, for fixed-reference / dose-rate adapted / no-repair definitions. DU145 parameters.
   - **Table 2:** max relative difference between fixed-reference and no-repair RBE at saturation, on the 4×3 grid.
   - **Figure 3-like sensitivity:** reference dose-rate sweep (2 vs 1 Gy/min) and T_iDSB^1/2 sweep (4 vs 30 min) at 6 Gy / 8 keV/µm.
   - **Figure 4-like R_TD50 curve:** photon-only R_TD50 vs dose rate for 1- and 2-fraction TD50 (RSC with-repair parameters).
   - **Figure 5-like RBE benchmark:** the Eq. (3) approximation `RBE ≈ no_repair_RBE × R_TD50` at the 4 depths × 2 particles × 2 fractionations from Table 3, compared to the experimental RBE values that the paper cites from Saager (2018) and Hintz (2022).

## 2026-05-29 — implementation in progress

- Writing `code/universe_core.py` first, then validating against the DU145 Figure 1/2 trends.
- Will save intermediate JSON for every figure so I can update PROGRESS as each one matches (or doesn't).

## Blockers / friction

- **No raw simulation outputs released** by the authors. RBE benchmark numbers in Figures 4-5 are read from the published plot (digitized later if needed) — I do not have access to the FLUKA SOBP simulation or the rat spinal cord TD50 fits.
- **GPU-parametrized three-step diffused RDD is opaque.** The paper only states that the diffused RDD is approximated with a three-step function on GPU; the actual step radii/heights are not in the text. I approximate this by sampling the diffused RDD on a fine radial grid and integrating analytically — this preserves the dose-by-area but is not bit-identical to the paper's GPU step-function.
- **DNA double-strand-break yield α_DSB.** Paper uses 30 DSB/Gy/cell (Liang et al. 2017, Stewart et al. 2011). Adopted verbatim.
- **Repair-misrepair coupling.** The paper says each repair instance has probability K_iDSB / K_cDSB of being a "misrepair" that kills the cell, and survival is otherwise determined by Eq. 5 evaluated at end-of-time. I implement exactly that; the result is identical to Eq. 5 in the no-repair limit (T → ∞ relative to irradiation time).


## 2026-05-29 — main-agent finish

- Subagent failed with an LLM timeout while debugging the stochastic RBE/bisection code. The existing code scaffold was useful but not validated.
- Main agent added `code/lightweight_universe_audit.py` to produce a conservative deterministic formula/table diagnostic rather than overclaim.
- Generated `results/summary.json`, `results/diagnostic_rbe_curves.csv`, and three diagnostic PNGs.
- Wrote `README.md` and `REPORT.md`.
- Final verdict: PARTIAL. The released equations/tables and qualitative dose-rate/RBE trends reproduce, but full UNIVERSE/GPU/FLUKA reproduction is blocked by unavailable code/raw outputs/method details.
