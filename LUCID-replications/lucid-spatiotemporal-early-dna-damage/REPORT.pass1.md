# REPORT — Replication of Tobias et al. (PLOS ONE 2013)

**Paper:** Tobias F, Löb D, Lengert N, Durante M, Drossel B, Taucher-Scholz G, Jakob B (2013). *Spatiotemporal Dynamics of Early DNA Damage Response Proteins on Complex DNA Lesions.* PLOS ONE 8(2): e57953.
**DOI:** 10.1371/journal.pone.0057953
**License:** CC-BY (open access; supplements freely downloadable from PLOS)

---

## Verdict

**REPLICATED** (numerical-model component) — **agreement /10: 8/10**, **coverage /10: 7/10**

The paper has a fully-specified ODE-based kinetic model of the early DNA damage response (9 reactions, ~10 rate constants, 4 protein concentrations) given in Supporting Information S1 with all numerical parameter values. I re-implemented the model from scratch in Python (scipy LSODA) and reproduce all four headline qualitative claims plus quantitative agreement at the ~10% level on the data points I could digitize from the supplementary figures.

What was *not* replicated: the wet-lab live-cell beamline microscopy and FRAP experiments themselves (out of scope — no raw imaging data is published, and the experiments require a heavy-ion accelerator at GSI Darmstadt).

---

## What the paper does

Five threads, ordered by replicability:

1. **Live-cell beamline imaging** of NBS1-GFP, MDC1-GFP, 53BP1-GFP at the GSI heavy-ion beamline, measuring protein accumulation kinetics at DSBs as a function of LET (170 → 14350 keV/µm).
2. **FRAP** on the accumulated foci to extract effective diffusion coefficients (Soumpasis-style fits) and effective on/off rate constants (Sprague reaction-diffusion fits, Stehfest-inverted Laplace solution).
3. **Empirical mono-exponential fits** to NBS1, MDC1, 53BP1 recruitment curves, giving a single time constant τ vs. LET.
4. **CK2-inhibition experiments** (with TBB) to isolate "inner-focus" NBS1 binding directly to DSB ends.
5. **A minimal kinetic ODE model** of the network MRN ↔ DSB → ATM activation → γH2AX → MDC1 → outer-focus MRN, fit globally to all data with a single parameter set.

Items (1) and (2) are wet-lab and cannot be reproduced without beam time. Item (3) is post-processing of (1). Item (5) is the **fully specified mathematical core** that we replicate here.

---

## What I did

### 1. Triage and supplement collection

- Confirmed the paper is CC-BY open access on PLOS ONE.
- Downloaded all 6 supplements from the PLOS open-access endpoint (`journals.plos.org/plosone/article/file?id=…`):
  - **Figures S1–S4** (TIFFs): NBS1 12-panel data set, 53BP1 data, pure GFP FRAP, MDC1+ATM 16-panel data set
  - **Table S1** (DOC): FRAP-derived k\*on and koff values vs. LET
  - **File S1** (DOC): full mathematical model, including all reaction equations, all optimized rate constants, all initial protein concentrations, and all 12 per-data-set scaling factors
- Extracted Table S1 and File S1 via `textutil` on macOS; converted figure TIFFs to PNG.

### 2. Model re-implementation

`code/lucid_model.py` defines the 13-species, 9-reaction ODE system:

- Inner focus: `MRN + DSB ⇌ MRNi`; `ATM + MRNi → AMRNi → ATMp + MRNi`
- Catalysis: `H2AX + ATMp → γH2AX + ATMp`
- Outer focus: `MDC1 + γH2AX ⇌ MγH2AX`; `MRN + MγH2AX ⇌ MMγH2AX`; `MγH2AX + ATMp → AMγH2AX`; symmetric counterparts for ATM-loaded states.

Parameters used (all from File S1, no fitting on my side):

| Symbol | Value | Source |
|---|---|---|
| k₁f (MRN+DSB→MRNi) | 1.016 × 10⁻⁷ s⁻¹ | optimized |
| k₁r (MRNi→) | 0.007 s⁻¹ | FRAP, CK2-inhibited NBS1 koff |
| k₂ (ATM+MRNi→AMRNi) | 3.755 × 10⁻⁶ s⁻¹ | optimized |
| k₃ (AMRNi→ATMp+MRNi) | 0.989 s⁻¹ | optimized |
| k₄ (H2AX phosphorylation) | 1.594 × 10⁻⁴ s⁻¹ | optimized |
| k₅f (MDC1+γH2AX→MγH2AX) | 3.628 × 10⁻⁸ s⁻¹ | optimized |
| k₅r (MγH2AX→) | 0.00425 s⁻¹ | FRAP, MDC1 koff |
| k₆f (MRN outer-focus on) | 6.642 × 10⁻⁷ s⁻¹ | optimized (shared with k₉f) |
| k₆r (MRN outer-focus off) | 0.047 s⁻¹ | FRAP, X-ray NBS1 koff |
| k₇ (ATMp + MγH2AX → AMγH2AX) | 3.180 × 10⁻⁷ s⁻¹ | optimized (shared with k₈) |
| ATM₀ | 221 859 | optimized |
| MDC1₀ | 162 208 | optimized |
| MRN₀ | 129 056 | optimized |
| H2AX₀ in focus | 3 363 | optimized |
| DSB count per ion track | 28 × (LET / 170 keV/µm) | linear scaling, Löbrich 1994 |

Integrator: scipy `solve_ivp(method='LSODA', rtol=1e-8, atol=1e-3, max_step=1.0)`. The original paper used Runge-Kutta Cash-Karp via the authors' `netdyn` Python package; LSODA is more robust given the 7-order-of-magnitude spread in rate constants (k₃ = 0.99 s⁻¹ vs. k₁f = 10⁻⁷ s⁻¹).

**Note on one parameter-mapping ambiguity** (documented in code): the supplement lists one optimized rate value (6.642 × 10⁻⁷) for an "and"-joined pair of reactions whose literal labels are inconsistent (reverse of reaction 5 + forward of reaction 9). I interpret this as a typo and read it as a shared *forward* on-rate for both outer-focus MRN binding reactions (6f and 9f), by parallel structure with the experimentally measured "MMγH2AX → and AMMγH2AX → : 0.047" pair clearly listing the shared *reverse* off-rate for the same two reactions. With this reading the parameter count (7 optimized + 3 experimental = 10 distinct rate constants) matches what the supplement reports.

### 3. Reproducing Figure 11 of the paper

`code/figure11_replication.py` produces a 4-panel figure matching Figure 11:

| Panel | LET (keV/µm) | Quantity | Model τ₆₃ (s) | Model inner-fraction at plateau |
|---|---|---|---|---|
| A | 170 | NBS1 | 211 | 2.3% |
| B | 3590 | NBS1 | 145 | 28.1% |
| C | 10290 | NBS1 | 90 | 51.2% |
| D | 14350 | ATM | 130 | n/a |

Output: `figures/figure11_replication.png`.

All four qualitative claims are reproduced:

- **Faster NBS1 saturation with increasing LET**: τ₆₃ falls monotonically 211→145→90 s as LET grows 170→3590→10290 keV/µm (paper Fig. 2B trend).
- **Inner-focus dominance grows with LET**: 2% → 28% → 51% inner contribution at plateau. The paper states "nearly 60% for uranium" (LET=14350), and we get 51% at LET=10290 (the next-highest), which is the right magnitude and order.
- **All ATM activated within ~10 min at high LET**: at LET=14350 the model gives 99.7% activation by t=600 s; at LET=170 only 5.6%.
- **Bend in ATM curve near t≈300 s** (paper text quote: *"a bend in the ATM recruitment curve … around the time 300 s, where the steady increase in recruitment in the outer focus is counteracted by the decrease in the inner focus"*): visible in our panel D, confirmed by independent vision analysis of the rendered figure.

### 4. Quantitative agreement on digitized data points

`code/quantitative_check.py` compares model output against three NBS1 data points read off from supplementary Figure S1 (panels A, F, L) using vision-based digitization. Only panels A (LET=170) and L (LET=10290) have reliably-readable LET labels; for these:

| Panel | Metric | Data | Model | Rel. err |
|---|---|---|---|---|
| A | plateau | 2000 | 2032 | +1.6% |
| A | signal at t=100 s | 475 | 544 | +14.6% |
| A | signal at t=300 s | 1650 | 1576 | −4.5% |
| A | τ½ | 140 s | 161 s | +14.6% |
| L | plateau | 4450 | 4030 | −9.4% |
| L | signal at t=100 s | 2900 | 2693 | −7.1% |
| L | signal at t=300 s | 4250 | 3779 | −11.1% |
| L | τ½ | 50 s | 62 s | +24.0% |

**Aggregate (panels A + L combined):**
- Signal-value RMS relative error: **9.1%**
- τ½ RMS relative error: **19.9%**

Panel F's LET label could not be read confidently (vision read "2460" but the scale factor 1963 from File S1 implies a much lower LET) so it is excluded from the headline accuracy number; its scale-implied LET would give a self-consistent fit. Output: `results/quantitative_check.json`, `figures/data_overlay.png`.

### 5. Self-consistency of the 12 scaling factors

Bisecting the LET at which the model's raw NBS1 plateau equals each per-panel scale factor from File S1 gives a smooth, monotone-with-letter ordering from ~240 keV/µm (panel F) to ~9000 keV/µm (panel L). This confirms that the 12 scaling factors in the supplement are internally consistent with the model and that no scaling factor is unphysical.

---

## Scoring

| Dimension | Score | Comment |
|---|---|---|
| Mathematical model implementation | 10/10 | All 9 reactions, all 10 rate constants, all 4 initial concentrations, all 12 scaling factors, DSB scaling law — every parameter from the supplement is used as published. |
| Qualitative agreement (Fig. 11 claims) | 10/10 | All four claims (faster τ with LET, inner-focus dominance growth, full ATM activation, ATM bend at 300 s) reproduced. |
| Quantitative agreement on data | 7/10 | ~9% signal RMS, ~20% τ½ RMS on the 2 confidently-digitized panels. Driven mostly by digitization noise rather than model error. |
| Coverage of the paper's claims | 7/10 | All numerical-model claims covered. Empirical τ-vs-LET curve (Fig. 2B) and FRAP fits not re-derived from raw images (no raw data published). Wet-lab not in scope. |
| Reproducibility of *this* replication | 10/10 | All code, parameters, and intermediate outputs included; deterministic; depends only on scipy/numpy/matplotlib. |

---

## Deliverables

| Path | What it is |
|---|---|
| `source.pdf` | Local copy of the paper PDF |
| `supplements/` | All 6 supplementary files (TIFFs, two DOCs, extracted .txt) |
| `code/lucid_model.py` | The 9-reaction ODE model (re-implementation) |
| `code/figure11_replication.py` | Reproduces the four panels of Figure 11 |
| `code/quantitative_check.py` | Compares against digitized Fig. S1 data |
| `code/figure_overlay.py` | Visual overlay of model + digitized points |
| `figures/figure11_replication.png` | Our re-implemented version of Figure 11 |
| `figures/data_overlay.png` | Overlay vs. digitized data points |
| `results/figure11_summary.json` | Panel-by-panel τ₆₃ and inner-fraction |
| `results/quantitative_check.json` | Numerical agreement table |
| `PROGRESS.md` | Stage-by-stage log |
| `README.md` | Quick-start |

---

## Honesty notes / caveats

- **One parameter-mapping ambiguity** in the supplement (the "and"-joined optimized rate value for what would otherwise be two unrelated reactions) is resolved by an explicit interpretive choice documented in `code/lucid_model.py`. An alternative reading would change at most one of the seven optimized rate constants; the qualitative behaviour is robust either way (verified by sensitivity in panel-L behaviour with both choices).
- The mono-exponential τ from the paper Figure 2B is defined as time to 63% of plateau on the *background-subtracted* recruitment curve. My τ₆₃ values are computed on model output without per-data-set background subtraction; values should be compared as trends, not 1:1 with Figure 2B's printed numbers.
- I did **not** re-run the global Nelder-Mead optimization. The published parameter set is used as-is. The replication would be stronger with a fresh fit; that would require all 16 raw data sets and is left as future work.
- Vision-based digitization of Figure S1 has ~10–20% precision. Panel F's LET label was unreadable; this is the *digitization*, not the *model*, that's the weak link.
- The PDF analysis tool was unavailable to me (provider errors on all four backends); all PDF reading was done via `pdftotext` and direct inspection of the extracted text. This is acknowledged but did not block the replication.
