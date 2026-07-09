# Workflow — Scott 2011 Epicellcom DSB Repair Kinetics Replication

## Overview
Closed-form analytical model. No simulation, no HPC, no wet-lab data
digitisation in this pass. Pure Python + NumPy + Matplotlib. Runtime <1 s.

## Steps executed (Wave 4, 2026-06-09)

1. **Paper acquisition**
   - Source: EuropePMC PMC3315173 (`https://europepmc.org/articles/PMC3315173?pdf=render`).
   - Sage DOI direct returned 403 from CherryRd; EuropePMC mirror is the
     free/open route. PDF stored under `data/paper.pdf` (if present).

2. **Scope audit**
   - LUCID-100 master TSV row 87 tagged this as `omics/signature replication`.
   - Read paper end-to-end. Confirmed no -omics data at all; the paper is a
     deterministic kinetic model with a worked parameterisation.
   - Retag recommended: `worktype = model / equations replication`.

3. **Equations transcribed (`code/multisig1.py`)**
   - Eq 3: `B(D) = B0 + alpha*D`
   - Eq 5: `BPM(D)` (Poisson mean per DNA molecule, D > T)
   - Eq 6: `phi_1(t)` (exponential density)
   - Eq 8: `phi_n(t)` (gamma density; n-fold convolution)
   - Eq 10: `Att_n(D)` (Poisson attribution percentages)
   - Eq 11: `Psi_n(t)` (cumulative repair)
   - Eq 12: `Cum(t, D)` (Poisson-weighted cumulative)
   - Eqs 13-14: `RB(t,D)`, `RBM(t,D)` (residual DSBs/cell and /molecule)

4. **Parameters (from paper, MRC-5 90 kV x-rays, confluent)**
   - beta = 2.5 h (mean repair time per DSB)
   - B_T = 0.10 foci/cell (baseline unrepaired)
   - alpha = 0.035 mGy^-1 (induction rate)
   - T = 1.4 mGy (low-dose threshold)
   - m = 46 DNA molecules per cell (paper's stated value)

5. **Figure regeneration (`code/replicate_figures.py`)**
   - Fig 1: phi_n(t) for n = 1..4 -> `figures/fig1_phi_n.png`
   - Fig 2: Att_n(D) attributions 0..1000 mGy -> `figures/fig2_attributions.png`
   - Fig 3: Psi_n(t) cumulative per-molecule -> `figures/fig3_Psi_n.png`
   - Fig 4: Cum(t,D) at 100 & 1000 mGy -> `figures/fig4_Cum.png`
   - Fig 5: RB(t,D) residual DSBs 0..200 mGy (log) -> `figures/fig5_residual_DSBs.png`
   - Figs 6-7 skipped (3D restylings of Fig 5; same math).

6. **Spot-check verification**
   - 8 numerical claims from the paper body text tested.
   - 7 reproduce to <=0.1% error.
   - 1 (Att_2 at 1000 mGy) revealed a paper labeling typo: the 46.7% in the
     body text is actually Att_1, not Att_2. Fig 2 in the paper is
     internally consistent with our re-derivation.

7. **Results summary** (`results/summary.json`)
   - All spot-check values persisted for downstream QA.

## Not done in this pass (deferred to open-questions follow-ups)
- Rothkamm & Lobrich 2003 raw-data digitisation.
- Bayesian refit of beta (paper Table 1 footnote suggests this).
- Eqs 15-16 (pathway-weighted beta/mu) implementation.
- Cross-comparison to LUCID-100 #57 doserate-RBE model.

## Runtime environment
- Host: CherryRd (macOS, Darwin 25.3.0).
- Python 3, NumPy, Matplotlib. No conda; standard environment.
- Wall time: <1 s. Memory: <1 MB.
- No paid endpoints. No LLM calls. No compute reservation.
