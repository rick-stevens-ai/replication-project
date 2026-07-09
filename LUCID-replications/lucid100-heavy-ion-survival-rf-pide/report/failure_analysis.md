# Failure analysis — lucid100-heavy-ion-survival-rf-pide

Where this replication (and by extension the paper's claims) falls short. Written to be genuinely critical, not diplomatic.

## Verdict framing
The queue-level label was **REPLICATED**. The on-disk deliberated verdict, adjudicated by an independent free Argo LLM judge (`argo:gpt-5.2`, temperature 0, coverage=8, agreement=6), is **PARTIAL**. **This backfill preserves PARTIAL** as the substantiated call and flags the mismatch. Anything in the queue log that reads "REPLICATED" for this dir should be understood as pre-adjudication.

## 1. What did NOT reproduce

### 1.1 The RF's headline RMSE (0.0196 / "49× smaller than LQM")
- **Paper:** RF RMSE = 0.0196, roughly 49× smaller than the LQM RMSE (0.0959).
- **This replication:** RF RMSE = 0.073 ± 0.011, roughly 1.6× smaller than LQM RMSE (0.117 ± 0.012).
- **Magnitude of discrepancy:** the paper's RF error is ~4× smaller than mine, and the paper's ratio LQM/RF is ~49× vs mine ~1.6×. This is the single largest quantitative miss.
- **Why:** most likely a combination of (a) target-variance artifact (if the paper's SF values are re-simulated from smooth (α,β) with no scatter, RF interpolation drives RMSE→0), and (b) evaluation leakage (random-point MC-CV lets the RF see other points from the same experiment at train time). See Open Questions Q1 and Q2 for the concrete diagnostic experiments.

### 1.2 Exact numeric match on ANY headline number
- LQM R² off by 0.04, LocReg R² off by 0.07, RF R² off by 0.03; RMSEs uniformly higher.
- **Why:** the data are not the paper's actual data (see §2.1); the ~15% clonogenic scatter I injected is realistic but not calibrated to the specific PIDE plate-to-plate variance for NB1RGB.

## 2. Root causes of the gaps (independent of the paper's own methodological issues)

### 2.1 Data-access blocker: GSI PIDE is email-gated
- The PIDE cell-survival ensemble is behind a TYPO3 powermail form at `https://www.gsi.de/.../pide_registration`. The download link is emailed only after form submission; the file is never inline-served, not on the Wayback Machine (CDX returned only PIDE logo images), not mirrored on Zenodo, figshare, or GitHub.
- Submitting the registration form on Rick's behalf is out of scope for an autonomous subagent (unrequested external contact under a human's name).
- **Consequence:** exact-number replication is structurally impossible from public artifacts today. The substitute reconstructed dataset preserves the *physics* (LET dependence) but not the exact 318-point matrix, per-experiment α/β, or exact LET tabulation.

### 2.2 No code released by the authors
- No repo, no notebook, no requirements file. The RF hyperparameter grid, the LocReg kernel/bandwidth, and the exact MC-CV split ratio (70/30? 80/20?) are described only in prose.
- **Consequence:** every re-implementation choice adds a small numeric wedge. LocReg kernel choice alone can move R² by ±0.02.

### 2.3 Reconstructed target variance is not calibrated
- I used a 15% log-normal scatter on SF, which is defensible for typical clonogenic assays but was not tuned to match PIDE's per-experiment scatter for NB1RGB. If real NB1RGB PIDE scatter is smaller, my RMSEs are inflated across the board; if larger, they are deflated.

## 3. Methodological failures IN THE PAPER (not this replication)
These are gaps that would remain even if I had the exact PIDE data.

### 3.1 Wrong CV scheme for the implicit claim
Random-point Monte-Carlo CV on data with 51 experiments × ~6 doses each lets the RF interpolate WITHIN an experiment. The paper's implicit claim — "given LET and dose, we can predict a new experiment's survival" — requires **leave-experiment-out** CV. The paper does not report LEO. This alone likely explains most of the RF's dramatic RMSE advantage.

### 3.2 Straw-man classical baseline
The paper compares RF(dose, LET) against LQM(dose only). Everyone in heavy-ion radiobiology knows α and β vary with LET; the fair comparison is LQM(α(LET), β(LET)) — i.e., a physical LQ with LET-dependent parameters — against RF(dose, LET). The RF is largely re-learning the Furusawa (2000) α(LET) and β(LET) curves empirically, so most of the "gain" is bookkeeping: you handicapped LQ by removing its known LET dependence, then reintroduced LET only in the RF.

### 3.3 No mechanistic baseline (MKM, RMF)
The Microdosimetric Kinetic Model (Kase 2006) and Repair-Misrepair-Fixation model (Carlson 2008) are the standard mechanistic baselines a paper claiming "ML beats classical for heavy-ion survival" should beat. Neither is discussed.

### 3.4 No uncertainty quantification
RF point predictions are reported without calibrated intervals. For the paper's stated clinical/treatment-planning motivation, uncalibrated predictions at novel ion species or clinical energies are dangerous.

### 3.5 Feature importance is trivial
"LET is the most important feature" is unsurprising after ~50 years of heavy-ion radiobiology (overkill peak, RBE(LET)). Without a partial-dependence plot showing whether the RF captures the overkill decline above ~200 keV/µm, the feature-importance claim is non-discriminating.

### 3.6 Data-availability statement is misleading
The paper's data-availability points to the GSI PIDE landing page as though it were a live public dataset; it is a registration form. This is a norms-violation, not a technical issue.

## 4. What would flip PARTIAL → REPRODUCED
Concretely:
1. Obtain the actual GSI PIDE NB1RGB subset (register with GSI; wait for email).
2. Rerun the pipeline on that data. If LQM R² ≈ 0.884 and LocReg R² ≈ 0.899 match to within ±0.01, the surrogate data is exonerated and the paper's numbers are honest at least for the classical models.
3. Rerun the RF on that data with the paper's own random-point MC-CV; if RMSE ≈ 0.0196 reproduces, then the low RMSE is a target-variance property of the actual PIDE SFs (probably re-simulated from (α,β)).
4. Independently rerun with **leave-experiment-out** CV. If RF R² collapses (e.g., to ~0.6), Open Question Q2 is answered "yes, the paper's central claim IS leakage-driven"; if it holds, then the RF's LET-based prediction really is that good.

Step 4 is the diagnostic experiment the paper should have run itself.

## 5. Compliance note
- No sims re-run in this backfill (HARD REQUIREMENT).
- No paid endpoints invoked.
- Reconstructed data explicitly labeled as substitute, not real PIDE, in every artifact that references it.
- Verdict cross-check performed; queue/on-disk mismatch flagged and on-disk verdict preserved.
