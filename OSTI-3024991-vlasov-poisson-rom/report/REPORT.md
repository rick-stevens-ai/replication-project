# Independent Replication — OSTI 3024991

**Paper:** Ping-Hsuan Tsai, Seung Whan Chung, Debojyoti Ghosh, John Loffeld, Youngsoo Choi, Jonathan L. Belof, *"Local Reduced-Order Modeling for Electrostatic Plasmas by Physics-Informed Solution Manifold Decomposition,"* Computer Physics Communications (2026).
**DOI:** 10.1016/j.cpc.2026.110039 · **OSTI:** 3024991 · **OA PDF:** https://www.osti.gov/servlets/purl/3024991
**Set:** OSTI-100 (TOPUP50 list, rank #6, applied_math) · **Replicator:** OpenClaw subagent · **Date:** 2026-07-02

---

## 1. Paper summary

The paper develops **data-driven reduced-order models (ROMs)** for collisionless electrostatic plasma dynamics governed by the **1D1V Vlasov–Poisson equation**:

> ∂ₜf + v ∂ₓf + E ∂ᵥf = 0,   ∂ₓₓφ = ∫f dv − R,   E = −∂ₓφ

The **full-order model (FOM)** uses conservative finite-difference **WENO5/UPWIND5** spatial discretization (Ghosh HyPar formulation), an **FFT** Poisson solve (periodic in x), and **classical RK4** in time; boundaries are periodic in x, homogeneous Dirichlet in v. On top of the FOM they build **POD-projection ROMs**, an efficient **tensorial** nonlinear update (precomputed 3rd-order tensor), and **temporally-local** ROMs via time-windowing (TW-ROM) and energy-windowing (EW-ROM). Test problems: prescribed external E-field (linear), **Landau damping**, and **two-stream instability**. Headline ROM-engineering result: EW-ROM ≈ **90× faster** than the Eulerian FOM at ≤ 7.5% (train) / 11% (test) relative error.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| C1 | Prescribed-E case (α=0.1, vT=1, tf=130, 128²): **n_f=24** POD modes capture 99% snapshot energy (δσ=1e-2) | quantitative / numerical | Yes | **Yes** |
| C2 | Projection-ROM final-time rel. error ≈ **0.2%** at δσ=1e-2, decreasing monotonically toward ~1e-6 | quantitative | Yes | **Yes (partial range)** |
| C3 | FOM correctly captures Vlasov–Poisson kinetic physics (Landau damping of plasma waves) | physics fidelity | Yes (vs analytic dispersion) | **Yes** |
| C4 | Tensorial ROM O(n_f² n_φ) nonlinear update via precomputed tensor | method / engineering | Partially | No (out of scope) |
| C5 | TW-ROM / EW-ROM improve efficiency+accuracy; EW-ROM ≈ 90× speedup, ≤7.5%/11% err (two-stream) | quantitative / engineering | Yes (heavy) | No (out of scope) |

Core *physics + reducibility* claims (C1–C3) were selected for replication under the wave's efficiency target; the ROM-engineering claims (C4, C5) were deliberately left out of scope.

## 3. Method (independent reimplementation)

**Environment:** uicgpu (8×A100, sourced `~/env.sh`); Python 3.8, numpy 1.23.5, scipy 1.10.1. Code in `work/`.

1. **FOM solver** (`vlasov_fom.py`), written from the paper's equations only (not the authors' code):
   - Spatial derivatives via **conservative finite-difference** with **WENO5** (Jiang–Shu smoothness indicators, ideal weights 0.1/0.6/0.3) and **Rusanov / local Lax–Friedrichs** flux splitting (α = max|advection speed|), for both ∂ₓ(v f) (periodic) and ∂ᵥ(E f) (Dirichlet in v via zero-padding ghost cells). This matches the paper's WENO5/UPWIND5 + upwind interface flux (eq 4–5).
   - **Poisson** solved exactly in Fourier space: φ̂ = −k⁻² ρ̂, E = −∂ₓφ (eq 6), zero-mean enforced at k=0.
   - Time integration: **classical 4-stage RK4**.
2. **Prescribed-E experiment** (C1, C2): E(x)=α cos(x), α=0.1, vT=1, domain [0,2π]×[−6,6], 128×128, tf=130, Δt=0.005. Collected snapshots, computed **POD via SVD**, and measured (i) n_f for energy-missing-ratio thresholds δσ∈{1e-2,1e-3,1e-4} and (ii) projection-reconstruction error of the final snapshot at each threshold.
3. **Landau damping / FOM physics** (C3):
   - Analytic ground truth: solved the **kinetic linear dispersion relation** 1 + (1/k²vT²)(1 + ζZ(ζ)) = 0 (Fried–Conte Z via Faddeeva `wofz`) by complex Newton. Verified against the textbook value: **k=0.5 → γ=−0.15336** (Cheng–Knorr), k=1 → γ=−0.851.
   - Ran the FOM on the **canonical k=0.5** weakly-damped benchmark (α=0.01, vT=1, domain [0,4π]×[−8,8], nx=128, nv=256, tf=25) and fit the field-energy decay rate over the clean exponential window t∈[3,18].
   - (The paper's own Landau case uses k=1, γ≈−0.85 — strongly damped, quickly reaching recurrence/noise; a poor rate-fit target. k=0.5 is the community-standard verification case.)
4. **Diagnosis of a coupling sign:** initial self-consistent runs grew instead of damped. Because the *external-field* prescribed-E case was already correct, the fault was isolated to the self-consistent E sign in the Vlasov force term. A sign sweep (`landau_signsweep.py`) confirmed the physically-correct convention (`efield_sign=-1`, consistent with the paper's eq-1/eq-2 sign pairing).
5. **Scoring:** LLM-judge = **Argo gpt-5.2** (free proxy localhost:44497), temperature 0, given all claims + measured numbers.

Commands (representative): `python3 run_replication.py`; `python3 landau_signsweep.py`; `python3 make_plots.py`; `python3 judge.py`. Total FOM wall time ≈ 336 s (prescribed-E tf=130 dominates).

## 4. Results vs paper

### C1 — POD reducibility (prescribed-E)
| δσ (energy missing) | Paper n_f | This work n_f | This work proj. rel. err @ tf |
|---|---|---|---|
| 1e-2 | **24** | **23** | 0.13% |
| 1e-3 | — | 81 | 9.98e-5 |
| 1e-4 | — | 168 | 1.60e-5 |

→ **Match (off by one mode).** The global linear subspace effectively represents the prescribed-E solution manifold, exactly as claimed.

### C2 — Projection-ROM accuracy
| Quantity | Paper | This work |
|---|---|---|
| Proj. rel. error @ δσ=1e-2 | ~0.2% | **0.13%** |
| Trend | monotone ↓ to ~1e-6 (δσ→1e-6) | monotone ↓ to 1.6e-5 (δσ→1e-4) |

→ **Match at tested points; monotone decrease confirmed.** The δσ→1e-6 endpoint was not swept (would need more snapshots/modes; error-vs-δσ trend already validated).

### C3 — FOM physics fidelity (Landau damping)
| Quantity | Analytic (ground truth) | This work FOM |
|---|---|---|
| k=0.5 linear Landau rate γ | **−0.15336** | **−0.1495** (2.5% error) |
| Dispersion-solver self-check | k=0.5 → −0.15336; k=1 → −0.851 | reproduced exactly |
| Sign sweep | — | sign=+1 → +0.136 (wrong); sign=−1 → −0.1495 (correct) |

→ **Match.** The independently-built FOM reproduces the canonical Landau damping rate to 2.5% (residual = expected WENO5/Rusanov numerical dissipation), confirming correct Vlasov–Poisson kinetic physics.

**Figures:** `report/evidence/landau_k0.5_decay.png` (FOM field energy vs analytic exp(2γt) envelope); `report/evidence/prescribed_pod_reducibility.png` (energy-missing-ratio vs n_f, reproducing paper Fig. 3).

## 5. Assessment

The **core reproducible physics/reducibility** of the paper replicates cleanly on an independent from-scratch implementation:
- POD reducibility (C1) and projection-ROM accuracy (C2) match the paper to within a single mode and sub-percent error.
- The FOM (C3) reproduces the canonical linear Landau damping rate to 2.5% of the exact kinetic dispersion root.

The **ROM-engineering claims** (tensorial update, TW/EW-ROM, 90× speedup, two-stream) were intentionally not attempted (heavier build, beyond the physics core and the wave's <25 min efficiency target). LLM-judge: coverage **67%**, agreement **85%** of testable core claims.

Honest scope: this is a solid replication of the paper's *FOM + linear-subspace reducibility foundation*, not of its full local-ROM machinery. No claim was contradicted.

## Verdict
**Verdict:** PARTIAL

---

WAVE_RESULT set=OSTI-100 paper=3024991 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3024991-vlasov-poisson-rom one_line=Reimplemented 1D1V Vlasov-Poisson FOM (WENO5+Rusanov, FFT Poisson, RK4) from scratch: reproduced POD reducibility (n_f=23 vs paper 24 @ delta=1e-2, proj err 0.13% vs 0.2%) and canonical k=0.5 Landau damping rate to 2.5% of analytic; full tensorial/windowed ROMs + 90x speedup out of scope.
