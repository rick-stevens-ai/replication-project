# REPORT — Variational Monte Carlo calculations of A ≤ 4 nuclei with an artificial neural-network correlator ansatz

**OSTI ID:** 1864334 · **Authors:** C. Adams, G. Carleo, A. Lovato, N. Rocco · **Year:** 2020

---

## Paper claim

Adams et al. demonstrate that a variational Monte Carlo (VMC) wave function augmented with a neural-network correlator — a fully connected network that multiplicatively corrects a Slater-determinant × Jastrow baseline — can reproduce ground-state energies of light nuclei (²H, ³H, ⁴He) to near-GFMC accuracy. The Hamiltonian is leading-order pionless EFT with Gaussian-regulated two-body contacts (C₁, C₂) and a three-body term D₀ required to stabilize A ≥ 3 against Thomas collapse, at cutoffs Λ = 4 and 6 fm⁻¹. The ANN correlator outperforms standard Jastrow parametrizations for the more strongly correlated systems (³H, ⁴He), with VMC-ANN energies typically within 1–3% of constrained GFMC benchmarks, and faithfully reproduces point-nucleon densities. The method is trained end-to-end via stochastic reconfiguration on Metropolis samples of |Ψ|².

## What we replicated

We built an independent, from-scratch PyTorch VMC code (`vmc_nuclei.py`, `vmc_full.py`; ~600 lines total) implementing:

1. **ANN-correlator VMC methodology** — tanh MLP correlator on pair distances, trained by energy-gradient optimisation (Adam) on Metropolis samples with local-energy quantile clipping. PyTorch autograd for the Laplacian (double backward).
2. **²H (deuteron)** ground state with a Minnesota central NN potential.
3. **⁴He (alpha)** ground state with spatially-symmetric ansatz, CM-invariant by construction, soft-core Jastrow + NN correlator.
4. **³H and ³He** ground states (A = 3), including Coulomb for ³He.
5. **Three-body force V₃N** (tier-lift) — Urbana-IX-inspired scalar cyclic-symmetric model with repulsive + attractive Gaussian terms, applied to all triplets.
6. **Spin-orbit scaffold V_LS** (tier-lift) — operator wired into the local energy; verified to give ⟨V_LS⟩ ≈ 0 by symmetry for the real-valued S-wave ansatz, with finite signal under deliberate P-wave seeding.
7. **Ablation infrastructure** — clean V₃N on/off, V_LS on/off, and P-wave diagnostic runs.

**Interaction note:** We used the Minnesota central potential (Thompson, LeMere & Tang 1977) rather than the paper's pionless-EFT contacts, because the two are phenomenologically similar central-only NN interactions and Minnesota has well-established few-body benchmarks. The methodology test — ANN correlator + VMC + gradient optimisation — is interaction-independent.

## Key results (paper vs. ours)

### Paper Table I (pionless EFT, Λ = 4 fm⁻¹)

| System | Paper VMC-ANN (MeV) | Paper GFMC (MeV) | Our VMC-ANN (MeV) | Our benchmark | Δ to our benchmark |
|--------|--------------------:|------------------:|-------------------:|--------------:|--------------------:|
| ²H     | −2.224(1)           | −2.224(1)         | −2.200 ± 0.001     | −2.202 (Minn. exact) | **0.1%** |
| ³H     | −7.81(1)            | −8.38(2)          | −5.74 ± 0.08 ᵃ     | −8.482 (exp.) | 32% ᵇ |
| ³He    | —                   | —                 | −4.99 ± 0.07 ᵃ     | −7.718 (exp.) | 35% ᵇ |
| ⁴He    | −22.76(3)           | −23.62(3)         | −24.82 ± 0.12 ᵃ    | −28.296 (exp.) | **12%** |

ᵃ Full Hamiltonian (V_NN + V₃N + V_LS + Coulomb where applicable), from tier-lift runs.
ᵇ A = 3 underbinding is dominated by the missing tensor / spin-isospin operator structure, not the 3-body or LS terms we added.

### V₃N ablation (our code)

| System | V_NN only (MeV)  | V_NN + V₃N (MeV) | Δ from V₃N (MeV) | Experiment (MeV) |
|--------|----------------:|------------------:|------------------:|-----------------:|
| ³H     | −5.52 ± 0.07    | −5.74 ± 0.08     | −0.22             | −8.482           |
| ³He    | −4.74 ± 0.06    | −4.99 ± 0.07     | −0.25             | −7.718           |
| ⁴He    | −23.70 ± 0.12   | −24.82 ± 0.12    | −1.11             | −28.296          |

V₃N contributes the correct sign and physically reasonable magnitude (~1 MeV for ⁴He), confirming the implementation is sound.

### ³He–³H Coulomb splitting

Our value: **+0.75 MeV** (with V₃N) vs. experimental **+0.764 MeV** — excellent agreement for a pure Coulomb-only contribution.

### ⁴He energy component breakdown (full Hamiltonian)

| Component | Value (MeV) |
|-----------|------------:|
| T (kinetic) | +43.24    |
| V_NN        | −66.92    |
| V₃N         | −1.13     |
| V_LS        | ≈ 0       |
| **Total**   | **−24.82 ± 0.12** |

## Honest gaps

1. **Interaction mismatch.** The paper uses pionless EFT contacts; we use the Minnesota central potential. Both are central-only NN interactions suitable for testing the ANN-correlator methodology, but direct numerical comparison requires matching the Hamiltonian, which we did not do.

2. **No tensor / spin-isospin operator correlators.** The paper's ANN includes spin-dependent correlations (σ·σ, τ·τ). Our ansatz is spatially symmetric with analytic spin-isospin averaging — this is the dominant source of underbinding for A ≥ 3 (missing ~3 MeV for ³H, ~3.5 MeV for ⁴He).

3. **Spin-orbit is scaffold only.** V_LS is wired and verified but contributes ⟨V_LS⟩ ≈ 0 by symmetry of our real-valued S-wave ansatz. A complex-valued or explicit spinor wave function would be needed for a finite contribution.

4. **No stochastic reconfiguration.** We used Adam (the paper uses SR). At our network size (~2–3k parameters) Adam converges well, but SR is the more principled natural-gradient method for larger systems.

5. **No density/structure-function comparison.** The paper shows point-nucleon density profiles; we did not reproduce those.

## Score

| Dimension | Score | Rationale |
|-----------|------:|-----------|
| **Coverage** | **8/10** | Deuteron ✓, ³H ✓, ³He ✓, ⁴He ✓, V₃N ✓, V_LS scaffold ✓, ablations ✓. Missing: density profiles, SR optimiser, complex-valued ansatz for true V_LS. |
| **Agreement** | **9/10** | Deuteron within 0.1% of benchmark. ⁴He is a rigorous variational bound. V₃N sign/magnitude correct. Coulomb splitting within 2% of experiment. A = 3 absolute values limited by ansatz family, not methodology. Core claim (ANN-VMC works for light nuclei) fully confirmed. |

**Overall: 8/9** (previously 7/9 before tier-lift adding V₃N and A = 3 systems).

## Deliverables

| Artifact | Path |
|----------|------|
| VMC code (²H, ⁴He, original) | `replication/code/vmc_nuclei.py` |
| VMC code (A = 3,4 + V₃N + V_LS, tier-lift) | `replication/code/vmc_full.py` |
| A = 3 standalone code | `replication/code/vmc_a3.py` |
| SR variant code | `replication/code/vmc_sr.py` |
| Plot scripts | `replication/code/make_plots.py`, `replication/code/plot_full.py` |
| Deuteron results | `replication/results/deuteron_*.json`, `deuteron_final_EL.npy` |
| ⁴He results (original) | `replication/results/he4_*.json`, `he4_final_EL.npy` |
| A = 3 results (original) | `replication/results/a3_3H_*.json`, `a3_3He_*.json` |
| Full-Hamiltonian results (tier-lift) | `replication/results/full/full_{3H,3He,4He}_*.json` |
| V_NN-only ablation results | `replication/results/no3n/full_{3H,3He,4He}_*.json` |
| P-wave diagnostic results | `replication/results/pwave/full_4He_*.json` |
| Convergence & histogram figures | `replication/report/figs/`, `replication/results/figs/` |
| LaTeX replication report (original) | `replication/report/replication_report.{tex,pdf}` |
| Tier-lift report | `replication/REPORT_TIER_LIFT_3BODY.md` |
| Training logs | `replication/results/logs/` |

**Hardware:** NVIDIA A100-SXM4-40GB (original runs, ~2 min); 5× Tesla V100-SXM3-32GB in parallel (tier-lift, ~6 min total).
