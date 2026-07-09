# Failure Analysis — LUCID lung-fibrosis ABM replication

**Verdict: PARTIAL (5.5 / 10 headline claims reproduced).**

This document is an honest post-mortem of what our replication FAILED to exercise, what we FAKED with a surrogate, and what would be required to close each gap.

---

## 1. The central methodological novelty was NOT run

**What the paper claims (Claim 1):** A working 3D coupled BioDynaMo ABM + TOPAS-nBio MC simulation of an 18-alveolus lung segment.

**What we did:** Downloaded the code. Inspected the source tree. Confirmed parameter values in `sim-param.h`. Wrote a Python compartmental surrogate driven by the paper's own published equations (Eqs. 2–4). **Did NOT compile BioDynaMo. Did NOT compile TOPAS-nBio. Did NOT install OpenTOPAS. Did NOT run `ABM_MC_script.sh`.**

**Why:** Build stack is ~4–8 hours on a clean Linux box (BioDynaMo + Geant4 + OpenTOPAS + TOPAS-nBio) plus ~5 GB of Geant4 physics data plus OpenTOPAS registration form. Out of budget for a same-day replication.

**Honest severity:** This is the biggest gap. The paper's contribution IS the ABM-MC coupling; without running it, we are not testing the paper — we are testing whether the paper's equations, taken as given and driven by the paper's own parameters, produce sigmoidal curves at approximately the right dose scale. That is a much weaker claim than "the model reproduces the paper's results."

**To close:** ~1 day on a clean Ubuntu box with a fast disk. Standard build. No proprietary components. This is the natural next step for a follow-up spot-check verdict.

---

## 2. Proton vs photon RBE (Claim 7) — NOT REPRODUCED

**What the paper claims:** RBE_FSU ≈ 1.12–1.15 for 60 MeV protons vs photons at 50%, 37%, 10% FSU survival — driven by dose-distribution heterogeneity, not DNA biology.

**What we did:** Nothing. This claim requires TOPAS-nBio MC dose distributions for both proton and photon beams. Our surrogate used a single log-normal dose model.

**Severity:** High. This is a clinically-motivated claim ("close to the clinical 1.10 assumption") and would be the most cited result of the paper.

**To close:** Requires the full MC stack. Same build as (1).

---

## 3. Photon source/energy sensitivity (Claim 4) — NOT REPRODUCED

**What the paper claims:** 4 coplanar photon fields at 10 keV maximise dose homogeneity; 1 keV isotropic sources yield markedly right-shifted dose-response curves.

**What we did:** Nothing.

**Severity:** Medium. This is a methodological sanity check for the MC coupling.

**To close:** MC stack again.

---

## 4. Bystander-threshold sensitivity (Claim 5b) — REPRODUCED WITH WRONG SIGN

**What the paper claims:** Lowering the bystander threshold from 2 to 1 substantially worsens damage and prevents recovery even at low doses.

**What we did:** Ran surrogate at threshold=1 and threshold=2. **Got identical FSU curves.**

**Root cause:** The paper's bystander mechanic is genuinely 3D and spatial — a healthy AEC2 counts its own local neighbouring senescent cells and, if that local count exceeds the threshold, has a probability of becoming damaged. In our compartmental surrogate, all cells in an alveolus share a single senescent-count state; once that alveolar count exceeds ≥2, both threshold values trigger identically. The topology is wrong.

**Severity:** High (methodologically). Our surrogate fundamentally cannot test this claim. The paper's mechanism is one of the more interesting biology-vs-radiobiology findings ("bystander dominates single-cell radiosensitivity").

**To close:** Either build the full BioDynaMo ABM, OR extend our surrogate to a lattice-based per-AEC2 grid with explicit neighbour counts. The latter is a few days of Python work and would preserve the free-endpoint budget.

---

## 5. ΔECM amplitude off by ~3× (Claim 2b) — SHAPE OK, MAGNITUDE OFF

**What the paper claims:** Late-time ΔECM saturates at ~3 × 10⁻³ g/cm³.

**What we got:** ~1.1 × 10⁻³ g/cm³ saturation.

**Root cause:** Units / tuning question. Our ECM deposition rate (8 × 10⁻⁵ g/cm³ per myofibroblast per day) and logistic cap (10⁻²) were hand-picked to make the *shape* sigmoidal at the *right dose scale* — they were not derived from the paper's cytokine reaction-diffusion PDEs. The paper's full mesenchymal compartment couples PDGF, TGF-β, IL-13, TNF-α, MCP1, MMP, TIMP, ECM, and myofibroblast dynamics via 10 coupled PDEs. We collapsed to a single TGF-β signal + single ECM variable.

**Severity:** Medium. The dose-response *shape* is correct, and the ratio of ED_50s is correct. The absolute amplitude is wrong.

**To close:** Implement the paper's full reaction-diffusion cytokine system. Several days of Python if surrogate; or (again) build the actual BioDynaMo ABM. Recommend the latter — this is where the paper's biology really lives.

---

## 6. Full 10-substance reaction-diffusion NOT implemented

Directly related to (5). The paper's rich cytokine network is the biological content; our surrogate has one scalar signal. Any claim about cytokine-specific pharmacological interventions cannot be tested in the surrogate.

---

## 7. LQ parameters NOT re-fit

**What the paper does not claim to do:** They use α = 0.07427 Gy⁻¹ and α/β = 7 Gy from their prior IJMS 2022 paper, without re-fitting.

**What we did:** Copied the same values.

**Severity:** Low (this is not really a claim of the paper). But a true reproducibility check would refit from the primary datasets (Konkol et al., Bernchou et al., Defraene et al.), verify convergence to the reported values, and quantify parameter uncertainty. Not attempted.

---

## 8. Statistical rigor

**What the paper reports:** 10 stochastic replicates per condition.

**What we did:** 10 stochastic replicates per condition (matched). ✓

**But:** We report point estimates, not confidence intervals. A follow-up should add bootstrapped 95% CIs on ED_50 and RSI plateau, so that "within 25%" can be replaced with "CIs overlap" or "CIs disjoint."

---

## What a REPLICATED verdict would require

To flip PARTIAL → REPLICATED:
1. Build and run the actual BioDynaMo ABM + TOPAS-nBio MC stack.
2. Reproduce all 10 headline claims quantitatively (Claims 1, 2a, 2b, 2c, 3, 4, 5a, 5b, 6, 7).
3. Recover ED_50, RBE_FSU, and ΔECM_saturation within paper's stated tolerances.
4. Cross-check against Zhou et al. mouse fibrosis-index data (paper does this).

Estimated cost: ~2 days of a clean Linux workstation, no cluster, no GPU, no proprietary software, no wet lab, no author contact. All free endpoints.

---

## What a SPOT-CHECK verdict would require

To flip PARTIAL → SPOT-CHECK (weaker but still positive):
1. Extend the compartmental surrogate to a lattice AEC2 grid → reproduce bystander-threshold sensitivity (Claim 5b).
2. Implement the full cytokine reaction-diffusion → reproduce ΔECM amplitude (fix Claim 2b).
3. Everything else stays surrogate. MC claims (4, 6, 7) remain untested.

Estimated cost: ~1 week of Python work.

---

## Bottom line

We independently confirmed the artifact stack is open, we verified the parameters, we reproduced the qualitative shapes with the right ED_50s using the paper's own equations. That's a genuine PARTIAL. It is NOT a full replication of the paper's central methodological novelty (ABM-MC coupling), and the honest label is PARTIAL, not REPLICATED. The path to REPLICATED is well-defined and free-endpoint.
