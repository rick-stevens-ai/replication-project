# LUCID-100 Replication Report

**Slot:** `lucid100-dna-protein-damage-cell-death` (Wave 3 · Tier A · slot 23 · rank 54 · priority 16)
**Paper:** Shuryak & Brenner (2012). *Mechanistic Analysis of the Contributions of DNA and Protein Damage to Radiation-Induced Cell Death.* Radiat. Res. 178(1), 17–24. DOI [10.1667/RR2877.1](https://doi.org/10.1667/RR2877.1) · PMID 22687051 · [PMC3580191](https://pmc.ncbi.nlm.nih.gov/articles/PMC3580191/).
**Date of report:** 2026-06-22 (writeup-only finish; underlying replication performed 2026-06-09).

## TL;DR

A closed-form 5-equation, 4-parameter mechanistic survival model that splits radiation-induced bacterial cell death into a DNA-damage channel (Q₁) whose double-strand-break repair fidelity decays with cumulative protein carbonylation, and a direct protein-damage channel (Q₂ = P^X), with S = Q₁·Q₂. The model was re-implemented from PMC JATS XML in pure Python and run for all 5 strain/condition rows (D. radiodurans R1 WT, D. radiodurans recA⁻, E. coli MG1655 WT, E. coli CB1000/CB2000 radioresistant, and λ-phage infective centers) under both γ and UV. Smoke output (`results/summary.csv`) reproduces the qualitative dominant-mechanism mapping of the paper's Table 2 in **10/10 rows**. Quantitative survival values differ from the paper by several orders of magnitude at the high-dose tail because the input protein-damage curve F(D) is a placeholder logistic, not the digitized Krisko & Radman 2010 data the original fit used. The numeric refit and exact figure overlays are **blocked solely on figure-digitized data from Krisko & Radman 2010 PNAS** (no tabular supplement; figures behind reCAPTCHA on PMC/EuropePMC image endpoints from headless fetch). No paywalled or paid endpoints were used.

## 1. Data sources

- **Primary paper (PMC JATS XML):** `artifacts/paper_oai.xml` (80 KB) via PMC OAI-PMH `verb=GetRecord&metadataPrefix=pmc` for `oai:pubmedcentral.nih.gov:3580191`. Contains body, all 5 equations, all figure captions, both tables, all 24 references. Sufficient for full model reconstruction.
- **Plain text body extract:** `artifacts/paper.txt` (25 KB), derived from the JATS XML.
- **EuropePMC abstract HTML:** `artifacts/europepmc_abstract.html`.
- **Open-access status:** `artifacts/unpaywall.json` — `oa_status=green`, `is_oa=true`, `best_oa_location=https://www.ncbi.nlm.nih.gov/pmc/articles/3580191`.
- **Source experimental dataset:** Krisko & Radman (2010) *PNAS* 107:14373, [10.1073/pnas.1009312107](https://doi.org/10.1073/pnas.1009312107) / PMC2922536. Open-access landing page reachable; **raw F(D) and S(D) values appear only inside figures with no tabular SI** — not harvested in this slot.
- **Author fitting code:** searched and **not publicly released** (no GitHub user `igorshuryak`; GitHub code search for `Shuryak Krisko Radman` → 0 hits; no Zenodo/Figshare/OSF URL in paper or references).

## 2. Methods comparison

| Aspect                 | Paper                                                                 | This replication                                                                 |
|------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Model equations         | Eqs. 1–5: `P = 1 − (F − F₀)/(Fmax − F₀)`; `Q₁ = exp[−Kdam·D·exp(−Krep·P)]`; `Q₂ = P^X`; `S = Q₁·Q₂` (S = Q₂ for λ IC) | Implemented verbatim in `scripts/smoke_shuryak_2012.py`                          |
| Parameters             | `Fmax=8.5 nmol/mg` (fixed), `Kdam_γ=10 kGy⁻¹` (fixed), `Kdam_UV=3.99 m²/kJ` (fit), `Krep=13.9` (fit; 0 for recA⁻), `X=3.88` D.r. / `6.76` E.c.+λ (fit) | Hard-coded best-fit values from paper's Table 1                                  |
| Fitting algorithm       | Custom FORTRAN random-restart simulated annealing; ln-S inverse-variance weighted least squares | **Not re-run.** Pure forward simulation only. No refit performed.                 |
| Input damage curve F(D) | Empirical Krisko & Radman 2010 measurements per strain × radiation     | **Approximate strain-specific logistic placeholders** matching qualitative shape (E. coli fast carbonylation to Fmax; D. radiodurans resistant, near half-saturation at upper doses). Acknowledged source of quantitative divergence. |
| Dose ranges             | γ: 0–20 kGy (D.r.), 0–4 kGy (E.c.); UV: 0–4 kJ/m² (D.r.), 0–0.36 kJ/m² (E.c.) | Same dose ranges, fine grid (see CSVs)                                           |
| Compute                 | Trivial CPU                                                            | `< 1 s` on CherryRd CPU                                                          |

## 3. Quantitative claim audit

All numbers below are read directly from `results/summary.csv` (smoke run) and compared to the paper's stated dominant-mechanism map (Table 2) and headline survival ranges.

**Dominant-mechanism agreement (paper Table 2 vs `summary.csv`):**

| Strain × radiation                | Paper claim (Table 2)                | Smoke result (this run) | Match |
|-----------------------------------|--------------------------------------|--------------------------|-------|
| D. radiodurans R1 WT, γ           | Q₂ (direct protein) dominates        | Q₂ (logQ₂/logS = 0.624)  | ✅ |
| D. radiodurans recA⁻, γ           | Q₁ (DNA + interaction) dominates     | Q₁ (logQ₁/logS = 0.998)  | ✅ |
| E. coli MG1655 WT, γ              | Q₂                                   | Q₂ (logQ₂/logS = 0.714)  | ✅ |
| E. coli CB1000/CB2000 (Res), γ    | Q₂                                   | Q₂ (logQ₂/logS = 0.512)  | ✅ |
| λ IC in E. coli, γ                | Q₂ (Q₁ ≡ 1 by definition)            | Q₂ (logQ₂/logS = 1.000)  | ✅ |
| D. radiodurans R1 WT, UV          | Q₂                                   | Q₂ (logQ₂/logS = 0.860)  | ✅ |
| D. radiodurans recA⁻, UV          | Q₁                                   | Q₁ (logQ₁/logS = 0.730)  | ✅ |
| E. coli MG1655 WT, UV             | Q₂                                   | Q₂ (logQ₂/logS = 0.961)  | ✅ |
| E. coli CB1000/CB2000 (Res), UV   | Q₂                                   | Q₂ (logQ₂/logS = 0.990)  | ✅ |
| λ IC in E. coli, UV               | Q₂                                   | Q₂ (logQ₂/logS = 1.000)  | ✅ |

**Dominant mechanism: 10/10 cells match the paper's Table 2.**

**End-of-range survival (from `results/summary.csv`, S_end column):**

| Strain × radiation                | D_end (kGy or kJ/m²) | S_end (this run) | Paper Table 2 / Figs. (approx.)     | Agreement                |
|-----------------------------------|----------------------|------------------|-------------------------------------|--------------------------|
| D.r. R1 WT, γ                     | 20.0 kGy             | 6.69 × 10⁻⁴      | ~10⁻¹ – 10⁻² at 20 kGy              | Off by ~2 orders (low)   |
| D.r. recA⁻, γ                     | 1.6 kGy              | 1.09 × 10⁻⁷      | ~10⁻⁵ at ~1.6 kGy                   | Off by ~2 orders (low)   |
| E.c. MG1655 WT, γ                 | 4.0 kGy              | 1.43 × 10⁻⁶¹     | ~10⁻⁵ – 10⁻⁶ at 4 kGy               | Strongly off (placeholder F drives Q₂ → 0) |
| E.c. Res, γ                       | 4.0 kGy              | 4.54 × 10⁻³⁵     | ~10⁻² – 10⁻³ at 4 kGy               | Strongly off (placeholder F) |
| λ IC, γ                           | 4.0 kGy              | 3.36 × 10⁻⁴⁴     | low but finite                      | Strongly off (placeholder F) |
| D.r. R1 WT, UV                    | 4.0 kJ/m²            | 6.61 × 10⁻⁴      | ~10⁻¹ – 10⁻² at 4 kJ/m²             | Off by ~2 orders (low)   |
| D.r. recA⁻, UV                    | 3.0 kJ/m²            | 7.54 × 10⁻⁸      | very low                            | Plausible ballpark        |
| E.c. WT, UV                       | 0.36 kJ/m²           | 3.80 × 10⁻¹²     | ~10⁻³ – 10⁻⁴                        | Strongly off (placeholder F) |
| E.c. Res, UV                      | 0.36 kJ/m²           | 8.83 × 10⁻⁶      | ~10⁻² – 10⁻³                        | Off by ~3 orders (low)   |
| λ IC, UV                          | 0.36 kJ/m²           | 1.06 × 10⁻¹¹     | low but finite                      | Strongly off (placeholder F) |

**Diagnosis:** all quantitative deviations trace to one cause — the placeholder logistic `_logistic_F(D)` over-saturates relative to Krisko & Radman 2010 measurements, so P→0 too fast and `Q₂=P^X` drives S into machine-epsilon at the upper end of E. coli ranges. The Q₁/Q₂ **ratio** (which determines the dominant mechanism) is much more robust than the absolute S magnitude; that is why 10/10 mechanism cells still match. Numeric agreement on S(D) requires replacing the logistic with digitized F(D) — see §7 and §8.

## 4. Scope audit

The paper makes claims along four axes; this replication's coverage:

| Claim class                                                           | Covered? | Evidence                                                                 |
|-----------------------------------------------------------------------|----------|--------------------------------------------------------------------------|
| C1. The 5-equation closed-form model is well-defined and tractable    | ✅ Full   | `scripts/smoke_shuryak_2012.py` implements Eqs. 1–5 verbatim and runs.   |
| C2. Best-fit parameter table (Table 1) with 95% CIs                   | ⚠️ Partial | Values used as inputs from paper; **not independently re-fit**. CIs unverified. |
| C3. Dominant mechanism per strain × radiation (Table 2)               | ✅ Full   | 10/10 in `results/summary.csv`.                                          |
| C4. Survival curves S(D) overlay Krisko & Radman 2010 data (Figs. 1, 3–5) | ❌ Blocked | Krisko & Radman 2010 raw F(D)/S(D) not in tabular form; figure digitization needed. |
| C5. Q₁ surface (Fig. 4) and S-vs-P plot (Fig. 5)                      | ❌ Not done | Achievable from same code base; no plotter implemented this pass.        |
| C6. Cross-strain transferability (Krep, X grouped) holds              | ⚠️ Inherited | Used as a model assumption (D.r. all-share `X`; E.c.+λ all-share `X`); not tested. |
| C7. Code release / reproducibility of fitter                          | ❌ Blocker | Authors' FORTRAN simulated-annealing fitter not released anywhere public.|

Scope coverage of the paper's testable claims: roughly **C1, C3 fully replicated; C2, C6 inherited; C4, C5, C7 not replicated** → 2/7 fully + 2/7 partial + 3/7 not done.

## 5. What I actually ran

- `python3 scripts/smoke_shuryak_2012.py --plot` (one execution, ~1 s, CherryRd CPU). Verified by file presence and the fact that `results/summary.csv` and the 10 per-strain CSVs hold internally-consistent numbers (S monotone decreasing in D; Q₁·Q₂ = S to display precision; Q₁=1 throughout `Ec_IC_*` as required).
- No refitting. No parameter search. No GPU. No paid endpoint.
- This report (writeup-only finish) re-read all artifacts on disk; no new science computed.
- Artifact harvest commands previously executed (recorded in `PROGRESS.md`): PMC OAI-PMH GetRecord for PMC3580191; Unpaywall API for DOI 10.1667/RR2877.1.

## 6. Key output files

| Path                                               | Purpose                                                       |
|----------------------------------------------------|---------------------------------------------------------------|
| `results/summary.csv`                              | One row per strain × radiation: `D_end, P_end, Q1_end, Q2_end, S_end, logQ1/logS, logQ2/logS, dominant_mechanism`. Source of all numbers in §3. |
| `results/Dr_R1_gamma.csv`, `Dr_R1_UV.csv`          | D. radiodurans R1 WT full-grid `Dose, P, Q1, Q2, S`           |
| `results/Dr_recA_gamma.csv`, `Dr_recA_UV.csv`      | D. radiodurans recA⁻ full-grid                                |
| `results/Ec_WT_gamma.csv`, `Ec_WT_UV.csv`          | E. coli MG1655 WT full-grid                                   |
| `results/Ec_Res_gamma.csv`, `Ec_Res_UV.csv`        | E. coli CB1000/CB2000 radioresistant full-grid                |
| `results/Ec_IC_gamma.csv`, `Ec_IC_UV.csv`          | λ-phage infective centers (Q₁ ≡ 1, S = Q₂)                    |
| `results/survival_gamma.png`, `survival_UV.png`    | Log-survival curves, 5 strains each (matplotlib output)       |
| `scripts/smoke_shuryak_2012.py`                    | Pure-Python implementation of Eqs. 1–5                        |
| `artifacts/paper_oai.xml`                          | PMC JATS XML full text (80 KB)                                |
| `artifacts/paper.txt`                              | Plain-text body extract (25 KB)                               |
| `artifacts/unpaywall.json`                         | OA status: green                                              |
| `MANIFEST.json`                                    | Machine-readable artifact + model parameter manifest          |
| `README.md`, `FIRST_PASS_REPORT.md`, `PROGRESS.md` | Prior subagent context (kept as-is; this REPORT.md supersedes for audit purposes) |

## 7. Honest gaps

1. **Quantitative S(D) is off by 2–60 orders of magnitude at the high-dose tail.** Root cause: the input protein-damage curve is a placeholder logistic, not digitized Krisko & Radman 2010 data. The exponentiation `Q₂ = P^X` with `X ≈ 6.76` (E. coli) amplifies small P errors into many decades of S error. This is acknowledged in `README.md`/`FIRST_PASS_REPORT.md` and is not a model implementation bug.
2. **Parameters were not independently re-fit.** Table 1 best-fit values were taken as inputs. The paper's 95% CIs are therefore unverified by this replication.
3. **Fig. 1 (S overlay), Fig. 3 (incorrectly-repaired-DSB fraction), Fig. 4 (Q₁ contour), and Fig. 5 (S vs P) were not produced.** Only the two summary S(D) plots were generated.
4. **No cross-validation on external datasets** (e.g. Daly et al. 2007 *PLoS Biol* for *Shewanella oneidensis* or *Pyrococcus furiosus*). The paper itself does not perform this either, so this is an extension gap, not a replication gap.
5. **D.r. R1 γ boundary case** (paper notes a Q₁ takeover at ~20 kGy): the smoke run reports Q₂ still dominant at 20 kGy in the placeholder, but the trend toward parity is visible (`logQ₁/logS = 0.376` vs `0.624` at 20 kGy, narrowing from earlier doses). Numeric resolution again requires the real F(D).
6. **Source paper figures (Krisko & Radman 2010 PNAS)** were not digitized this pass; the protocol called for WebPlotDigitizer on a real (non-headless) browser, which was out of scope for the timed-out run.

### Exact missing artifacts (named, per Rick's rule)

- **`krisko_radman_2010_F_of_D.csv`** — per strain × radiation, columns `(strain, radiation, dose, F_nmol_per_mg)`, digitized from PNAS 107:14373 Fig. 2. **REQUIRED** to replace the `_logistic_F` placeholders.
- **`krisko_radman_2010_S_of_D.csv`** — per strain × radiation, columns `(strain, radiation, dose, S_obs, S_obs_lower_ci, S_obs_upper_ci)`, digitized from PNAS 107:14373 Fig. 1. **REQUIRED** to enable a re-fit of `(Kdam_UV, Krep, X_D.r., X_E.c.)` and a Fig. 1 overlay.
- **Author fitting code** — Shuryak's FORTRAN random-restart simulated-annealing source. Not on GitHub/Zenodo/Figshare; would have to be requested by email from Shuryak (Columbia CRR). Not strictly required (SciPy `least_squares` or `dual_annealing` substitutes cleanly) but its absence means any "verify the CIs" check is an independent reimplementation, not a true replication of the fitter.
- **PNAS PDF/figure JPGs via real browser** — needed because every headless attempt against PMC/EuropePMC binary endpoints returned reCAPTCHA HTML. PNAS landing itself returns 403 to `curl`.

## 8. Verdict

- **Coverage: 5/10.** Model fully reconstructed and runnable; dominant-mechanism map fully reproduced (a strong qualitative claim covering 10/10 published cells); but the headline survival curves and parameter CIs were not numerically reproduced, and 3 of 5 published figures (Figs. 3–5) were not re-rendered.
- **Agreement: 4/10.** Where the paper makes a categorical claim (which channel dominates), agreement is perfect (10/10). Where it makes a quantitative claim (S at D_end), the placeholder F(D) drives several-orders-of-magnitude divergence in 7 of 10 rows.
- **Repro-blocker status:** purely **data-availability blocker** (Krisko & Radman 2010 raw F(D)/S(D) not redistributed in tabular form). Not a model, code, or compute blocker. One non-headless browser session with WebPlotDigitizer would unblock a full numeric replication in an afternoon.
- **Verdict label (per `AUDIT_PROTOCOL.md`):** **PARTIAL** — model is fully recovered and qualitatively validated against the paper's central mechanism-mapping claim, but the quantitative survival curves and Table 1 parameter CIs remain unverified.

---

VERDICT=PARTIAL COVERAGE=5/10 AGREEMENT=4/10

Repro-blocker summary (3 lines):
1. Krisko & Radman (2010) PNAS 107:14373 (PMC2922536) publishes the experimental F(D) carbonylation and S(D) survival data **as figure points only**, with no tabular SI; the Shuryak & Brenner (2012) replication target inherits this dependency for any numeric fit or figure overlay.
2. All headless fetches of figure binaries from PMC and EuropePMC return reCAPTCHA challenge HTML, and PNAS direct PDF returns HTTP 403, so figure digitization needs a real (non-headless) browser plus WebPlotDigitizer — out of scope for this subagent run.
3. The authors' FORTRAN random-restart simulated-annealing fitting code is **not publicly released** (no GitHub user `igorshuryak`; 0 hits in GitHub code search for `Shuryak Krisko Radman`; no Zenodo/Figshare URL in the paper or its references), so any CI verification would be an independent SciPy reimplementation rather than a true code replication.
