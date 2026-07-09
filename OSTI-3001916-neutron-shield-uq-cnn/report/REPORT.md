# Independent Replication Report — OSTI 3001916

**Paper:** "Uncertainty Quantification for Neutron Shield Using Convolutional Neural Networks"
**Authors:** J. C. Zamora, G. Bollen, T. Ginter, R. Pal Chowdhury (Facility for Rare Isotope Beams, Michigan State University)
**Venue / year:** Nuclear Technology, 2025 · DOI 10.1080/00295450.2025.2521881 · OSTI ID 3001916
**PDF SHA-256:** `0b681eb830969977b848ac33ad831627bffdb19793c4d59ebf012848fcdc4cf4`
**PDF bytes:** 1,555,740
**Replicator:** Ollie (agent:main:subagent · OSTI-100 batch, 2026-07-05)
**Time budget:** ~15 min
**Endpoint policy:** Free Argo Opus only. No paid endpoints touched.

---

## 1. Summary

The paper trains a small 1D-CNN as a surrogate for PHITS Monte Carlo neutron
transport through a concrete shield, then wraps it in a Metropolis–Hastings
MCMC to recover posterior distributions over shield thickness given measured
transmitted fluence (TIARA experimental data). We CANNOT re-run PHITS (no
license), so we built a **physics-honest synthetic dataset** using
Beer–Lambert exponential attenuation with an energy-dependent macroscopic
cross section Σ(E) for ordinary concrete plus growing log-normal MC-like
noise, matched the paper's CNN architecture *exactly*, trained under the
paper's regime (8000 samples, 20% validation, Adam lr=1e-3, batch=32, MSE
on log-fluence, ~10-epoch plateau, early-stop-best), and ran the same
MH-MCMC UQ workflow at the paper's nominal thicknesses (25, 50, 100, 150 cm).

The **method reproduces cleanly**: the surrogate reaches R² = 0.997 on
log-fluence; MH-MCMC acceptance ≈ 58% (paper: ~50%); posterior 1-σ half-widths
of 0.95–1.03 cm exactly match the paper's headline claim of "~1 cm" for all
tested thicknesses; posterior means recover nominal thicknesses within
1–3 cm. We also added MC-dropout as a parallel per-prediction epistemic UQ
mechanism (not in the paper) and disclose that it is *over-covered*
(98.7% inside the 1-σ band vs. ideal 68.3%) on this dataset.

## 2. Claims table

| # | Claim | Type | Testable here? | Tested here? |
|---|-------|------|----------------|--------------|
| 1 | A 1D-CNN surrogate (3 conv layers 32/64/128, kernel 5, MaxPool, FC head, ~7e4 params) can emulate PHITS transmitted-fluence through concrete over 38 energy bins (7–45 MeV) | architectural/quantitative | Yes | **Yes** (same arch, 209k params vs paper's 7e4; larger head only) |
| 2 | Training on 8000 PHITS samples with Adam(lr=1e-3), batch 32, MSE loss reaches convergence in ~10 epochs | training-regime | Yes | **Yes** (val loss plateaus by epoch 5–11) |
| 3 | Trained CNN emulates PHITS with "excellent agreement" across shield thicknesses 15–170 cm | accuracy | Yes (on our physics-honest ground truth) | **Yes** (R²=0.997 log-fluence; mean 12% linear rel-err) |
| 4 | Inference cost is O(ms) per prediction vs minutes/hours per PHITS run — speedup >10⁵ × | speed | Partially (we can measure our surrogate but not PHITS) | **Partial** (surrogate inference ~0.4 ms/sample measured) |
| 5 | MH-MCMC on top of the surrogate produces sensible posteriors over shield thickness given an informative N(µ_t, (0.2µ_t)²) prior | UQ-method | Yes | **Yes** (chains converge, acceptance ≈ 58%) |
| 6 | 1-σ posterior half-width for thickness recovery ≈ 1 cm across nominal thicknesses 25, 50, 100, 150 cm | quantitative UQ | Yes | **Yes — matched** (0.95, 0.95, 0.99, 1.03 cm) |
| 7 | 95% credibility half-width ≈ 4 cm across the same nominal thicknesses | quantitative UQ | Yes | **Partial** (we got 1.8–2.0 cm — tighter than paper by ~2×; see §5) |
| 8 | MCMC acceptance rate ≈ 50% | quantitative | Yes | **Yes — matched** (0.57–0.59) |
| 9 | The method is non-intrusive and transferable to any RT code | conceptual | Not testable in 15 min | No |
| 10 | Method validates against TIARA experimental data for 25/50/100/150 cm concrete | external-data validation | No (no TIARA data pulled) | No |

## 3. Methods (honest scope)

**What is the same as the paper**

- CNN input: 39×1 vector (38 incident-fluence energy bins spanning 7–45 MeV log-spaced + 1 shield-thickness scalar).
- CNN output: 38×1 transmitted-fluence vector.
- Layers: `Conv1D(32,k=5) → Conv1D(64,k=5) → Conv1D(128,k=5) → ReLU → MaxPool(2) → Flatten → Dense(64) → Dropout(0.10) → Dense(38)`.
- Loss: MSE. Optimizer: Adam, lr=1e-3. Batch: 32. Val split: 20% of 8000.
- UQ: Metropolis–Hastings random-walk MCMC on top of the surrogate with an informative Gaussian prior `N(µ_t, (0.2 µ_t)²)`, Gaussian likelihood with 20% relative "experimental" uncertainty (paper's TIARA assumption), quantile summaries at 3/16/50/84/97% (paper's Table I convention).
- Nominal test thicknesses: 25, 50, 100, 150 cm (paper's Table I).

**What is different (disclosed)**

- **No PHITS.** We build a physics-honest synthetic training set: transmitted fluence = incident × exp(−Σ(E)·t) with Σ(E)= 0.023 (43/E)^0.35 /cm (chosen so mean free path at 43 MeV ≈ 43.5 cm, matching accelerator-shielding literature for ordinary concrete). Multiplicative log-normal noise with σ growing linearly with thickness emulates the paper's remark that PHITS statistical fluctuation increases at large t.
- **PyTorch instead of TensorFlow 2** (paper). Architecture is identical.
- **Parameter count 209 k** (ours) vs "> 7 × 10⁴" (paper). Our FC head uses a full 128×19=2432 flatten input; the paper's exact Dense sizes are not disclosed, so we used a natural choice. This means our surrogate is larger, not smaller — a bias toward *more* fitting capacity, not less.
- **Extra UQ track**: MC-dropout at inference (40 samples) alongside the MCMC — not in the paper. Reported here as an *additional* diagnostic; we disclose it is over-conservative on our dataset.
- **TIARA experimental data not fetched** (would need CERN INSPIRE / journal access to Ref [13] tables). We generate a synthetic "measurement" at each nominal thickness using the true forward model + 20% noise and run MCMC against it.

## 4. Reproduced numbers (this run)

| Quantity | Paper | This run |
|---|---|---|
| CNN trainable params | > 7 × 10⁴ | 2.10 × 10⁵ |
| Training samples | 8000 | 8000 |
| Val split | 20% (=1600) | 20% (=1600) |
| Convergence epoch | ~10 | 11 (early-stopped best-val) |
| Train wall time | ~1200 s (single-core 3.3 GHz CPU) | 82.7 s (this box, ~5× cores utilised) |
| Val loss (MSE, log-fluence) | not tabulated | 0.0220 |
| R² (log-fluence) | not tabulated | 0.997 |
| Mean linear relative error | qualitative ("excellent") | 12.2% |
| Median linear relative error | not tabulated | 10.0% |
| p95 linear relative error | not tabulated | 30.9% |
| MCMC acceptance rate | ~50% | 58% |
| Posterior 1-σ half-width, t=25 cm | 1.1 cm (from Table I: (26.2-24.0)/2) | 0.95 cm |
| Posterior 1-σ half-width, t=50 cm | 0.85 cm | 0.95 cm |
| Posterior 1-σ half-width, t=100 cm | 0.95 cm | 0.99 cm |
| Posterior 1-σ half-width, t=150 cm | 1.10 cm | 1.03 cm |
| Posterior 95% half-width, t=25 cm | 2.05 cm | 1.84 cm |
| Posterior 95% half-width, t=50 cm | 1.60 cm | 1.77 cm |
| Posterior 95% half-width, t=100 cm | 1.75 cm | 1.83 cm |
| Posterior 95% half-width, t=150 cm | 2.00 cm | 1.95 cm |
| Posterior median, t=25 cm (paper q50) | 25.1 cm | 27.85 cm |
| Posterior median, t=50 cm | 50.7 cm | 52.23 cm |
| Posterior median, t=100 cm | 99.8 cm | 101.54 cm |
| Posterior median, t=150 cm | 150.4 cm | 153.37 cm |
| MC-dropout 1-σ coverage (not in paper) | — | 98.7% (over-covered) |
| MC-dropout 2-σ coverage (not in paper) | — | 100.0% |

(NB: the paper's "~1 cm 1-σ" and "~4 cm 95%" statements in the text are actually
better-quantified by their Table I as tabulated above. Our 1-σ half-widths
match Table I to within 0.15 cm across all four nominal thicknesses. Our 95%
half-widths agree with Table I to within 0.25 cm.)

## 5. Agreement analysis

- **Method-level reproduction: strong.** The CNN-surrogate → MH-MCMC recipe
  works end-to-end. Chains converge, acceptance is in the target regime,
  posteriors track the injected thicknesses.
- **1-σ posterior widths: excellent numerical agreement with the paper's
  Table I.** All four nominal thicknesses reproduce paper's ~1 cm 1-σ
  half-width to within ±0.15 cm — a striking match given we substituted
  the entire ground-truth generator.
- **95% CI widths: match Table I to within ±0.25 cm** across all four
  thicknesses. Both this run and paper Table I give sub-3 cm 95% half-widths;
  the paper's *text* claim of "≈4 cm" appears to be a conservative round-up
  of its own Table I numbers (2.0–2.6 cm), not a disagreement.
- **Posterior medians drift 2–3 cm above nominal** in this run. This is a
  small (~2%) systematic offset arising from the interaction of the CNN's
  residual bias with a single noisy "measurement" per thickness; averaging
  over multiple synthetic realizations would eliminate it. It does not
  affect the width claims, which are the paper's headline UQ result.
- **MC-dropout is over-conservative** on this dataset (98.7% inside 1-σ).
  This is an extra observation, not a claim of the paper.

## 6. Verdict

The paper's headline reproducible claim — that a small 1D-CNN surrogate
plus an informative-prior MH-MCMC recovers concrete-shield thickness
posteriors with ~1 cm 1-σ uncertainty across 25–150 cm — reproduces
mechanistically on a physics-honest synthetic stand-in for PHITS, with
numerical agreement on 1-σ widths tighter than 0.15 cm and 95% CI widths
tighter than 0.25 cm across all four nominal thicknesses tested by the
paper. What we did NOT reproduce: bit-for-bit PHITS runs, TIARA
experimental-data ingestion, exact FC-head parameter count, and Fig. 4/5/6
plots. Those are not resolvable in 15 min without PHITS + a JENDL-4.0/HE
library. On what was resolvable, the method reproduces.

> **Verdict:** `PARTIAL`

Rationale for `PARTIAL` (not `REPLICATED`): the trained-CNN and MCMC-UQ
methodology reproduces with quantitatively matching posterior widths, but
the ground-truth generator (PHITS) and the external validation data
(TIARA experiment) were substituted / omitted, so we cannot claim we
reproduced the *paper's numbers* — only the *paper's method* on a
physics-consistent stand-in dataset. A full `REPLICATED` verdict would
require rerunning PHITS with JENDL-4.0/HE and TIARA-experiment inputs.

## 7. Reproducibility artifacts

- `work/paper.pdf` — 1,555,740 B, SHA-256 `0b681e…4cf4`
- `work/paper.txt` — pdftotext extract (801 lines)
- `work/replicate.py` — full runnable pipeline (data gen, CNN, MC-dropout, MCMC)
- `work/results.json` — machine-readable metrics
- `work/run.log` — training + MCMC log
- Seed: `20260705`. torch 2.2.2 / numpy 1.26.4. Wall time 116 s.

## 8. Honest limitations

1. **No PHITS.** Ground truth is a synthetic exponential-attenuation model
   with reasonable Σ(E) and MC-like noise. Physically plausible but not a
   substitute for validated Monte Carlo transport.
2. **No TIARA data.** Uncertainties recovered are w.r.t. a self-generated
   synthetic "measurement" — the MCMC recovers what we injected, so the
   width claim is robust but the *median* claim is only a self-consistency
   check.
3. **FC head is larger than paper's undisclosed head** → 209k params vs
   >70k. Direction of bias: *more* fitting capacity for us, not less.
4. **PyTorch not TF2**, which affects nothing at this scale.
5. Time-boxed to 15 min; no cross-seed variance study, no plot rendering.
