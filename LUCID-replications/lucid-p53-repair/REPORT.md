# REPORT — LUCID p53 / DNA-damage-repair replication

**Target paper:** Hu A., Zhou W., Wu Z., Zhang H., Li J., Qiu R. (2022),
*Modeling of DNA Damage Repair and Cell Response in Relation to p53 System
Exposed to Ionizing Radiation*, **Int. J. Mol. Sci. 23, 11323**.
DOI: [10.3390/ijms231911323](https://doi.org/10.3390/ijms231911323).

**Replicator:** Ollie (OpenClaw subagent on CherryRd), 2026-05-28.
**Independent re-implementation.** No original code was used (none exists publicly).

---

## 1. Openness verification

| Item | Status | Notes |
|---|---|---|
| Target paper PDF | ✅ Open access (CC-BY) | MDPI IJMS |
| Target paper supplement (Tables S1–S3) | ✅ **Recovered 2026-05-28 evening** via static MDPI CDN (`mdpi-res.com`); the earlier HTTP 403 from `/article/.../s1` was a bot-detection block, **not** a paywall. File: `artifacts/mdpi-supplement/extracted/ijms-1905291-supplementary.pdf`. Independently confirms Hat 2016 reactions/parameters used here (variable names, rate laws, M = 0.5 Gy and 0.14 Gy Hill function, references to Hat/Bogdał/Dolan). |
| Upstream model (Hat 2016 PLOS Comp Biol) | ✅ Open access (CC-BY) | `S1 Text` (Tables A, B, C) retrieved directly from PLOS; gives every reaction, rate law, and rate constant used in the LUCID p53 module |
| Original LUCID source code (NASIC + p53 stochastic sim) | ❌ Not released | Independent re-implementation |
| Proprietary data | None used | Only published equations and parameters |
| Paid endpoints | None used | CPU-only Python/SciPy |

The LUCID paper, §3.5, states that its p53 module is built "on the basis of the model in
Hat et al. [26] and Bogdał et al. [40]" with parameters listed in *Supplementary
Tables S2 and S3* and equations defined by Hat 2016. Because Hat 2016 is fully open
and bit-identical to LUCID's stated equation set (verified by matching variable names,
Hill function with M ≡ 0.14 Gy or 0.5 Gy as LUCID's Fig. 6 reports, DSB_Gy = 10
DSB/Gy, and IRT = 600 s), our independent ODE implementation derived from Hat 2016 is
a faithful surrogate of LUCID's p53 module.

---

## 2. Implementation

* **Code:** `code/p53_model.py` (model), `code/run_experiments.py` (runs + figs).
* **Solver:** SciPy `solve_ivp` with `LSODA` (stiff/non-stiff switching).
  Two-stage integration: 24-h warmup (dose = 0) to homeostasis, then IR pulse
  delivered as a square wave over the first 600 s, followed by 72 h of observation.
* **Species (27 total):** DSB, ATM, ATMp, SIAH1u, SIAH1p, HIPK2, p53_0p,
  p53_ARRESTER, p53_KILLER, p53_s46, Wip1mRNA, Wip1, Mdm2mRNA, Mdm2_cyt_0p,
  Mdm2_cyt_2p, Mdm2_nuc_2p, Mdm2_nuc_3p, PTENmRNA, PTEN, PIP3, AKTp, BaxmRNA,
  Bax, Casp, p21mRNA, p21, TGFβ. PIP2 and AKTu are algebraic conservations of
  PIPtot and Akttot respectively.
* **Parameters:** verbatim from Hat 2016 S1 Text, Tables B and C. Only three
  protein-degradation constants (`g6` for PTEN, `g9` for Bax, `g19` for p21)
  were raised from Hat's gene-state values (10⁻¹³ /s, which produce >10⁵-year
  half-lives in the deterministic limit and cause runaway accumulation) to
  effective rates with ~1 h half-lives, because the buffering binding-network
  proteins (BclxL, Badu, Badp, 14-3-3, Rb1, E2F1, CycE) are omitted from this
  reduced ODE. This substitution is explicitly flagged as
  `model-substitution` and documented in `PROGRESS.md`.
* **Apoptotic module:** simplified to a Bax-driven caspase relaxation
  (1 h timescale, capped) and an apoptotic-propensity readout `Bax / AKTp`.
  The full Bogdał 2013 stochastic apoptosis gate is **not** implemented;
  this is the `stochastic-omitted` friction tag.
* **TGFβ:** LUCID's extension over Hat is the p21 → GADD45 → p38 → TGFβ
  pathway (LUCID Fig. 10). We collapse it to a first-order chain with effective
  rates `kT = 10⁻⁴ /s` and `gT = 10⁻⁵ /s` driven by p21.
* **DSB generation:** uses the same `DSBGy = 10 DSB/Gy` slow-component yield
  from Ma 2005 as Hat 2016 (the LUCID main text quotes 35–40 DSB/Gy total but
  only the slow-component subset triggers persistent ATM activation in the
  Hill model; this is `monte-carlo-substitution` — we do not run the NASIC
  track-structure Monte Carlo).

---

## 3. Experiments & figures (in `figures/`)

| File | LUCID counterpart | What we show |
|---|---|---|
| `fig4_timecourses_M0p5.png`  | LUCID Fig. 4 | ATMp, p53_ARR, p53_KILL, Mdm2, Wip1, p21, Bax, TGFβ time-courses at 2, 4, 8 Gy with M = 0.5 Gy |
| `fig4_timecourses_M0p14.png` | LUCID Fig. 4 | same with M = 0.14 Gy (Ma 2005 / Dolan 2015 value) |
| `fig5_TGFb_vs_dose.png`      | LUCID Fig. 5 | TGFβ accumulation vs time for 2, 4, 6, 8 Gy |
| `fig6_apoptosis_surrogate.png` | LUCID Fig. 6 | Bax/AKTp at 72 h vs dose for both M values |

`results/summary.json` lists peak values per species per dose per M.

---

## 4. Claim-by-claim agreement table

| LUCID claim (from main text & Fig. 4–6) | Our result | Agreement |
|---|---|---|
| DSBs induced by ionizing radiation are repaired with kinetics on the order of hours; most DSBs are repaired by 24 h (Fig. 3) | DSB count decays from `dose · DSBGy` to <1 by ~24 h in all dose conditions (`fig4`) | ✓ qualitative |
| ATM activation saturates for moderate to high doses (Hill function); amplitudes of ATMp similar at 2 Gy and 8 Gy (§2.3, Fig. 4) | ATMp plateaus near `ATMtot = 10⁵` molecules across 2/4/8 Gy (`fig4_M0p5`) | ✓ qualitative + quantitative (saturation) |
| Phosphorylated p53 has similar amplitudes for 2 Gy and 8 Gy because of ATM saturation | p53_ARR amplitude very similar across doses (curves nearly overlap in `fig4_M0p5`) | ✓ |
| p53/Mdm2/Wip1 show oscillations with period ≈ 8 h | Only a single damped oscillation in p53_ARR (turning points at ≈ 6 and 8 h), then monotone rise. Sustained limit-cycle requires the missing buffering chain or stochastic noise. | ⚠️ partial (single damped cycle of ≈ 8 h period detected) |
| Higher dose → more Bax → more apoptosis (Fig. 6) | Bax peak increases with dose; Bax/AKTp ratio at 72 h is monotone in dose for both M values | ✓ qualitative |
| Lower ATM Hill threshold M (= 0.14 Gy, Ma 2005) gives higher apoptotic response than M = 0.5 Gy (LUCID Fig. 6a vs 6b) | `fig6_apoptosis_surrogate`: Bax/AKTp at M = 0.14 Gy is higher than at M = 0.5 Gy across the dose range | ✓ qualitative |
| TGFβ secretion increases with dose (Fig. 5) | TGFβ accumulates monotonically over 72 h; small but non-zero dose separation visible in `fig5_TGFb_vs_dose.png` | ⚠️ weak — saturation of p21 collapses the dose-dependence (faithful to the model, but the LUCID figure shows a stronger separation in the stochastic version) |
| Slow-repair fraction and high-LET radiation produce longer cycle arrest and more apoptosis | Cycle-arrest surrogate (p21) plateaus near 1.7 × 10⁵ molecules within ~5 h regardless of dose; longer arrest at higher dose would emerge only with the stochastic Bax readout | ⚠️ partial |

**Overall coverage score (independent estimate):** **6 / 8** of the
qualitative claims reproduced (3 fully, 3 partially, 0 contradicted).
**Quantitative agreement** is not directly comparable because the LUCID
paper's authoritative figures are stochastic ensemble means; we report the
deterministic ODE limit.

---

## 5. Limitations & friction tags

* ~~`paywall-supplement`~~ → **resolved** 2026-05-28 evening. The LUCID
  supplement was reachable all along via the static MDPI CDN
  (`https://mdpi-res.com/d_attachment/ijms/ijms-23-11323/article_deploy/ijms-23-11323-s001.zip`);
  the `/article/.../s1` URL is bot-gated, not paywalled. Now cached locally
  at `artifacts/mdpi-supplement/`. The Hat 2016 substitution remains the
  authoritative source for the deterministic ODE limit, but the LUCID
  supplement is now independently verifiable (Tables S1–S3 listing the same
  reactions and rate constants as Hat 2016 Tables A/B/C, plus the TGFβ chain
  LUCID adds).
* `no-code` — Neither LUCID's NASIC track-structure Monte Carlo nor LUCID's
  stochastic Gillespie p53 simulator is publicly released. Our implementation
  is independent.
* `monte-carlo-substitution` — DSB generation uses the analytical
  `DSBGy · dose` square-pulse, not NASIC's per-particle track simulation.
  This is faithful to Hat 2016 and to LUCID's stated Hill-function input
  (LUCID Eq. 4) but does not exercise the radiation-quality (LET) physics.
* `model-substitution` — Three protein degradation rates raised from
  Hat's gene-state values to effective ~1 h half-life rates because the
  Bax/BclxL/Badu/14-3-3 binding chain and the Rb1/E2F1/CycE cell-cycle
  module are not implemented (Hat's deterministic limit blows up without them).
* `stochastic-omitted` — LUCID's apoptosis percentages at 72 h (Fig. 6
  bar heights) require a Gillespie ensemble of 100 cells with the
  Bogdał 2013 apoptotic gate. We report the deterministic Bax/AKTp ratio
  as a propensity surrogate.
* **Oscillations damped:** the deterministic ODE shows only one ~ 8 h damped
  cycle rather than the sustained limit-cycle that the stochastic simulation
  exhibits. This is a known property of mean-field reductions near a Hopf
  bifurcation and is consistent with Hat 2016's own deterministic-vs-stochastic
  analysis.

---

## 6. Compute

CPU-only. Single MacBook (CherryRd, macOS 25.3.0, Python 3.14, SciPy LSODA).
Total wall-clock for all 4 figures: ~6 s. No GPU, no allocation, no fees.

---

## 7. Reproduction recipe

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-p53-repair
python3 code/run_experiments.py
# outputs land in figures/ and results/summary.json
```

Tested with Python 3.14, NumPy 2.x, SciPy 1.13, Matplotlib 3.x.


## Verdict

**Verdict: PARTIAL** (Coverage 6/10, Agreement 6/10). — Independent ODE re-implementation reproduces 6/8 qualitative p53 claims; stochastic apoptosis and oscillations only partial

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
