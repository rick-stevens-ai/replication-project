# Inventory of equations, parameters, and quantitative claims
Paper: Ngcezu & Rabus (2021), *Investigation into the foundations of the track-event theory of cell survival and the radiation action model based on nanodosimetry*, Radiat Environ Biophys 60:559-578, https://doi.org/10.1007/s00411-021-00936-4.

This is a **theoretical / critical-analysis paper**. It does NOT fit any new cell-survival curves to experimental data. It re-derives the math of TET (Besserer & Schneider 2015a/b) and RAMN (Schneider et al. 2020), and performs nanodosimetric simulations using proton-track data taken from Braunroth et al. (2020) and Rabus et al. (2020). The original proton-track datasets are NOT included in the article or its supplementary material and are not (to public knowledge) deposited in an open archive — they are an explicit reproducibility blocker for Figs. 3–9.

## Equations the authors derive themselves and use as headline claims

| # | Equation | Where | Meaning |
|---|----------|-------|---------|
| 1 | p1 = (1/nt) · (1/A) ∫∫ p^{c,1}(r) Φ(r|D) d²r | Eq. 1 | fluence-averaged probability of a sublethal one-track effect |
| 2 | p2+ = (1/nt) · (1/A) ∫∫ p^{c,2+}(r) Φ(r|D) d²r | Eq. 2 | fluence-averaged probability of a lethal one-track effect |
| 3 | nt(D) = ∫∫ Φ(r|D) d²r | Eq. 3 | expected number of tracks crossing area A |
| 4 | Pc(n1, n2+ | n) = multinomial(n; n0,n1,n2+; p0,p1,p2+) | Eq. 4 | conditional multinomial |
| 5 | P(n1,n2+) = Σ_n Pc(·|n) Pt(n) | Eq. 5 | mixture over track number |
| 6 | P(n1,n2+) = (nt p1)^{n1}/n1! · (nt p2+)^{n2+}/n2+! · e^{-nt(p1+p2+)} | Eq. 6 | factorises into two independent Poissons when Pt is Poisson |
| 7 | S = [1 + nt p1] e^{-nt(p1+p2+)} | Eq. 7 | survival = P(0,0) + P(1,0) at the single-CV / cellular level |
| 8 | p = nt p2+ / D ,  q = nt p1 / D | Eq. 8 | model parameters in Gy^-1 |
| 9 | **S = (1 + qD) e^{-(p+q)D}**  | Eq. 9 | fundamental TET survival equation |
| 10 | S = (1 + N nt pSL) e^{-N nt (pSL+pCL)} | Eq. 10 | RAMN single-CV form (Schneider et al. 2020 Eq. 1) |
| 11 | **S = (1 + nt pSL)^N · e^{-N nt (pSL+pCL)}** | Eq. 11 | corrected N-target survival, when at most one SL is allowed cell-wide |
| 12 | (1 + nt pSL)^N ≈ exp[N nt pSL − (nt pSL)² / 2 · N ] (note: paper writes N pSL nt − (nt pSL)²/2 inside the exponent; cf. text) | Eq. 12 | large-N Taylor approximation |
| 13 | **S ≈ exp[ −pD − (qD)² / (2N) ]** | Eq. 13 | implies almost-pure-exponential survival for realistic N |
| 14 | S = P(0,0) + P(1,0) + R[P(0,1) + P(2,0)] | Eq. 14 | survival with repair |
| 15 | **S = {1 + qD + R[pD + (qD)²/2]} e^{-(p+q)D}** | Eq. 15 | corrected repair model (TET-original-flavor) |
| 16-19 | extended model with 4 categories (nonlethal/sublethal/potentially-lethal/definitely-lethal); ends with S = {1 + qD + R[p'D + (qD)²/2]} e^{-(p+q)D} | Eqs. 16–19 | adds 4th parameter p' |
| 20 | p' = nt(D) p2 / D | Eq. 20 | definition of the new parameter |
| 21 | P*(k1,k2+) = (1-R1)^{k1}(1-R2+)^{k2+} ΣΣ C(n1,k1) C(n2,k2) R1^{n1-k1} R2+^{n2-k2} P(n1,n2+) | Eq. 21 | RAMN persistent-lesion distribution |
| 22 | **S' = (1+qD) e^{-(p+q)D} + R [ 1 − (1+qD) e^{-(p+q)D} ] = R + (1−R)(1+qD)e^{-(p+q)D}** | Eq. 22 | alternative single-repair-parameter model |
| 23-24 | mean CL/SL = (1−R) · φ · σ · P_{CL/SL} | Eqs. 23/24 | RAMN re-expressed |
| 25-28 | PSL ≈ F2·n;  PCL ≈ nt · n(n−1) · F2² | Eqs. 27–28 | corrected single-track conditional probabilities for SL/CL inside a CV |
| 29 | P(k1,k2+|n1,n2+) = B(k1|n1,pd) · B(k2+|n2+,pd) | Eq. 29 | binomial thinning by DNA-density factor pd |
| 31 | P(DSB|IC) = (1/F2) Σ_{k≥2} (1/2^{k-1}) F_k | Eq. 31 | combinatorial DSB-from-IC model |

## Concrete numerical claims (independently checkable)

C1. **Eq. 9 reduces to LQ at low dose**: small-D expansion gives S ≈ exp(-αD - βD²) with α=p, β=q²/2 to second order in D (and a residual cubic term −q³D³/6). Verify symbolically/numerically.

C2. **Eq. 9 → essentially exponential at high dose**: (1+qD) prefactor is dominated by exp(-(p+q)D) for D ≫ 1/q. Verify on plot.

C3. **Eq. 13: large-N approximation makes survival nearly pure exponential** when N is of the order of the number of possible CVs in a nucleus.
   – Paper says: "If N is the number of possible CVs, i.e., on the order of 5 × 10^8, and if 40 DSBs are produced per Gy, then the quadratic term would be unity for a dose on the order of 500 Gy."
   – Quantitative check: with N = 5e8 and qD = 40 (i.e., 40 DSB/Gy × 1 Gy =40 at D=1 Gy, scales linearly), find D such that (qD)²/(2N) = 1.
     (40·D)² / (2·5e8) = 1  →  D² = 1e9/1600 = 625000  →  D ≈ 790 Gy. Paper says "on the order of 500 Gy". This is an order-of-magnitude claim — confirm to within a factor of 2.
   – Up to D = 80 Gy, the quadratic correction should be tiny — confirm.

C4. **Eq. 15 vs. Eq. 7 of Besserer & Schneider 2015b**: the authors claim Eq. 15 lacks (a) a mixed p×q term and (b) an R²·D³ term that the B&S 2015b version has. This is a structural / symbolic claim — verifiable by expanding both formulas and showing the term-by-term differences.

C5. **Eq. 22**: alternative single-R model has the limit S' → 1 as R → 1 (perfect repair), and S' → (1+qD) e^{-(p+q)D} as R → 0. Verify both limits.

C6. **Eq. 27/28 vs. Schneider et al.'s expressions**: PSL ≈ F2·n (same as Schneider at leading order) but PCL ≈ nt·n(n−1)·F2² differs from Schneider's by an extra nt factor that drives PCL many orders of magnitude smaller. Confirm relative magnitudes for representative numbers (n≈ 6 BIVs in a CV; F2 ≈ 0.01 for low-energy proton; nt ≈ 1e-5).

C7. **Quadratic term in (1+nt pSL)^N becomes unity at ~500 Gy**: same as C3 phrased differently.

## Things explicitly NOT in this paper that would normally be checked
- No new cell-survival measurements.
- No fits of (p,q) to specific cell lines.
- The Table 1 of Besserer & Schneider 2015a (with parameter values) is referenced but not reproduced in this paper.

## Figures 3-9 (nanodosimetry of proton tracks)
These rely on raw proton-track simulation data from:
- Braunroth, Nettelbeck, Ngcezu, Rabus 2020 (Radiat Phys Chem 176:109066) – 50,000 simulated proton tracks, 1, 3, 10, 50 MeV; 650 nm track segment.
- Rabus, Ngcezu, Braunroth, Nettelbeck 2020 (Radiat Phys Chem 166:108515)
- BioQuaRT-project track data (Alexander et al. 2015) – 10 µm tracks, 50 tracks at 3 MeV, 250 at 50 MeV.

These datasets are NOT distributed with the article's Supplementary Material 1 — the supplementary describes the *methodology* (annular scoring, Wigner–Seitz scoring) but not the raw track-point lists.

**→ Reproducibility blocker for Figs. 3, 4, 5, 6, 7, 8, 9**: the raw ionization-point lists from the Braunroth-2020 and BioQuaRT proton-track simulations (Geant4-DNA / PTra). Without them, the cumulative F2 distributions, p1/p2+ multi-event distributions, and bivariate (single-DSB CV, multi-DSB CV) frequencies cannot be recomputed.

What CAN be reproduced from scratch on CPU in seconds:
- Eq. 9 dose-response curves and their LQ low-dose limit (C1, C2).
- Eq. 11 → Eq. 13 large-N exponential limit (C3, C7).
- Comparison of Eq. 15 with Besserer & Schneider 2015b Eq. 7 (C4).
- Eq. 22 limits (C5).
- Relative magnitudes of PSL and PCL under Eqs. 27/28 vs. Schneider's (C6).
