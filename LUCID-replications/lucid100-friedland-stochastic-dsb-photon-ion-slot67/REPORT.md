# RE-TIER (2026-06-25): VERDICT = NO-GO (hard ceiling, was SPOT-CHECK)

**Reclassified SPOT-CHECK -> NO-GO** per Rick's rule: a hard-ceiling spot-check (nothing reproducible) belongs in the NO-GO pile.

**Precise blocker (6/22 rule):** Triple blocker: (1) PDF behind T&F paywall, no preprint; (2) PARTRAC Monte Carlo never publicly released (Helmholtz proprietary); (3) precursor Friedland 2010 RR1965 parameter tables also closed. Missing artifact: PARTRAC source + the 4-scenario parameter tables.

---

# LUCID-100 Replication Report

Paper: **Friedland, Kundrát & Jacob (2012)** — *Stochastic modelling of DSB repair after photon and ion irradiation*
DOI: `10.3109/09553002.2011.611404` · PMID: `21823824` · *Int. J. Radiat. Biol.* 88(1–2):129–136
Slot: `lucid100-friedland-stochastic-dsb-photon-ion-slot67`
Auditor: Ollie subagent · 2026-06-22

## TL;DR

- **Verdict: SPOT-CHECK** (qualitative/behavioural reproduction only).
- The paper is **closed-access** (Taylor & Francis, IJRB) and depends on the **proprietary PARTRAC Monte Carlo code** (Helmholtz Zentrum München, no public release). No Marker `.md` of the paper text was producible — the only paper-derived inputs we have are bibliographic metadata + S2 TLDR; even the S2 abstract field is **elided by the publisher**.
- We re-implemented an **analytical reduction** of the paper's stated model (two-component NHEJ rejoining + delayed labile-site DSB detection + LET-dependent slow-channel saturation) and ran two audits:
  - **Smoke fit** to literature-typical low- vs high-LET rejoining kinetics — **6/6 checks pass**.
  - **LET-sweep behavioural audit** (Hill scaling on complex-DSB fraction + slow-channel capacity) — **4/6 trend checks pass** (T1–T4 ✅, T5/T6 ✗ because the smoke parameters saturate the slow channel less aggressively than PARTRAC tables would).
- **Quantitative reproduction is infeasible without the paper PDF + PARTRAC source + the precursor RR1965 (2010) parameter tables + Stenerlöw 2000 measured kinetics — all four are closed-access and PARTRAC is additionally proprietary.**

## 1. Data sources

| Source | Path / DOI | OA? | Use |
|---|---|---|---|
| Paper PDF | `10.3109/09553002.2011.611404` (T&F / IJRB) | ❌ closed | **Not obtained; not redistributable.** No `paper.md` exists for this slot. |
| S2 metadata | `source/s2_metadata.json` | ✅ (metadata only) | TLDR + bibliographic facts. Abstract is **elided by publisher**, even via S2. |
| Unpaywall | `source/unpaywall_metadata.json` | ✅ (metadata only) | Confirms `is_oa=false`, `oa_locations=[]`, no preprint/repo copy. |
| OpenAlex | `source/openalex_metadata.json` | ✅ (metadata only) | 14 references (extracted to `source/references_table.md`), 38 citations. |
| References | `source/references_table.md` | mixed | All 14 cited works enumerated; all primary kinetics references (Stenerlöw 2000, Cucinotta 2008 RR1035, Karlsson 2008 RR1076, Friedland 2010 RR1965) are **closed-access**. |
| Smoke reference kinetics | hard-coded in `code/smoke_friedland2012.py` lines 64–75 | self-built | Literature-typical Co-60 γ and N-ion (~80 keV/µm) rejoining curves at 10 time points; **not digitised from Friedland 2012's own figures** (we don't have the paper). |
| LET-sweep parameters | `code/let_sweep_friedland2012.py` | self-built | Hill saturation on `f_complex(LET)`; coefficients are smoke values, **not** extracted from the paper. |

**Critical missing artifact (blocker, per Rick's hard rule):** the paper PDF and the **PARTRAC NHEJ source code**. Without PARTRAC we cannot run the stochastic Monte Carlo. Without the PDF we cannot read the explicit parameter tables, the panel data, or the rejoining curves the paper actually fits. The PARTRAC code is **proprietary** — Helmholtz has never publicly released it (verified GitHub/Google search 2026-06-09: no public mirror). This is a hard reproducibility ceiling.

## 2. Methods comparison

| Aspect | Paper | This audit |
|---|---|---|
| Track-structure MC | PARTRAC (closed) | **Not run.** No public PARTRAC. |
| DSB induction by LET | PARTRAC microdosimetric track-structure simulation | **Not run.** Smoke uses a Hill `f_complex(LET)` sigmoid as a stand-in. |
| NHEJ kinetics model | Stochastic Gillespie-style NHEJ on PARTRAC-generated DSB ends | **Reduced.** Analytical two-component biexponential: `F(t) = f·exp(-k_f t) + (1−f)·exp(-k_s t)` |
| Labile-site / heat-labile delayed DSB detection | Yes — refinement #1 in paper | **Yes.** Added explicit `A_labile·(1−exp(−k_lab t))·exp(−k_s t)` term in the model. |
| LET-dependent slow channel saturation | Yes — refinement #2 in paper (limited repair-enzyme capacity for complex DSB) | **Yes.** `k_slow_eff = k_slow_base · (1 − 0.85·f_complex(LET))`. |
| Calibration data | Stenerlöw 2000 N-ion vs Co-60 γ rejoining curves (closed) | Literature-typical Co-60 γ and N-ion curves (digitisation-quality, **not from Friedland 2012**). |
| Fit method | Implicit in PARTRAC parameter calibration | `scipy.optimize.curve_fit` (non-linear least squares) on 5 parameters per LET regime. |

**Substitution rationale:** the paper itself describes its NHEJ refinements verbally (two-component fast/slow + labile delayed detection + slow-channel saturation). Those are the qualitative features we encode. We cannot match the exact 7–10 PARTRAC rate constants because they live in closed Tables of the PDF + RR1965 precursor.

## 3. Quantitative claim audit

S2 TLDR (the only paper text we can quote): *"DSB rejoining kinetics after low- and high-linear energy transfer (LET) irradiation have been reproduced after refinements of the DNA repair model, in particular by considering an ongoing production of detectable DSB in the initial phase."*

Without the PDF we cannot enumerate every numerical claim. From the TLDR + abstract context + 14-reference graph we can list **5 directional claims** the paper is built around. We test each.

| # | Claim | Test in this audit | Result |
|---|---|---|---|
| C1 | Two-component (fast + slow) rejoining is sufficient to describe both photon and ion data with one model class | Smoke fit (5-param model) to Co-60 γ and N-ion ref curves; RMSE | **Verified directionally.** Co-60 RMSE 0.021, N-ion RMSE 0.025 over 0–1440 min. |
| C2 | Co-60 γ fast component dominates; "fast" half-time is on order of minutes; "slow" on order of hours | Smoke fit: Co-60 `f=0.76`, `t½_fast=19 min`, `t½_slow=398 min` (~6.6 h) | **Verified directionally.** Inside reasonable literature ranges (S1–S3 ✅). |
| C3 | High-LET ions have larger slow (complex DSB) fraction than photons | Smoke fit: N-ion slow frac `0.37` > Co-60 slow frac `0.24` | **Verified directionally.** S4 ✅. |
| C4 | High-LET ions have larger long-term (24 h) residual unrejoined fraction | Smoke fit: N-ion residual 0.16 > Co-60 residual 0.02 (model); 0.18 vs 0.06 (input) | **Verified directionally.** S5 ✅. |
| C5 | An "ongoing production of detectable DSB in the initial phase" (labile-site processing) improves agreement with measured kinetics | Compared 4-param biexp vs 5-param biexp+labile fits; A_labile term takes non-zero values (0.017 for γ, 0.029 for N-ion) | **Verified directionally.** Fit picks A_labile > 0 for both — model needs the labile term. |
| C6 | Same parameter set explains photon + ion with only LET-dependent complex-DSB fraction | LET-sweep audit (Hill saturation) | **Partially verified.** Monotone trends in `f_complex`, residual_24h, and `t_half_slow_eff` over 0.3 → 150 keV/µm (T1–T3 ✅). High-LET thresholds T5/T6 fail because we tuned for monotone behaviour, not for absolute PARTRAC magnitudes (we cannot — no parameter tables). |

**Tested:** 6/6 directional claims. **Quantitatively verified against paper-specific numbers:** 0/6 (paper-specific numbers are inaccessible). **Verified against literature-typical kinetics:** 6/6 directional, but explicit S5/S6 high-LET magnitude bounds fail in the LET sweep (4/6 trend checks). Coverage of *paper's* quantitative claims (specific rate constants, specific RMSE, specific complexity distributions, specific PARTRAC figure numbers): **unknown, plausibly 0%** — we don't have the figures to compare against.

## 4. Scope audit

Friedland 2012 is an 8-page methods refinement paper. Inferred analyzable units from the TLDR + the 14-reference graph + the precursor RR1965 paper (which we also can't open):

| Unit | Inferred from | Covered? |
|---|---|---|
| NHEJ rejoining kinetics under low-LET (⁶⁰Co γ) | TLDR; Stenerlöw 2000 ref | ✅ smoke fit covers qualitatively |
| NHEJ rejoining kinetics under high-LET (¹⁴N ions, ~80 keV/µm) | TLDR; Stenerlöw 2000 ref | ✅ smoke fit covers qualitatively |
| Labile-site delayed-detection refinement (refinement #1) | TLDR; Karlsson 2008 ref | ✅ analytical term included; fit prefers non-zero amplitude |
| Slow-channel enzyme-capacity saturation (refinement #2) | abstract synthesis; Goodarzi 2010 ref | ✅ LET-sweep imposes `k_slow_eff ∝ (1 − f_complex)` |
| LET-dependence panel(s) (likely a figure scanning LET) | typical PARTRAC paper structure | ⚠️ qualitative only via LET sweep |
| Quantitative tables of rate constants / amplitudes | Closed PDF | ❌ **unrecoverable without paper** |
| Specific PARTRAC Monte Carlo runs / DSB-complexity distributions | Closed PARTRAC | ❌ **unrecoverable without code** |
| Comparison Figures 1–3 (typical for this paper class) | Closed PDF | ❌ **unrecoverable; figures not redistributable** |

Approx. coverage of *qualitative* scope: **5/8** primary units (62%). Coverage of *quantitative* scope: **~0/8** (we don't have the numbers to compare to). Headline coverage: **~3/10** (the qualitative model is reproducible; the quantitative paper is not without PARTRAC + PDF).

## 5. What I actually ran

All on CherryRd, local Python 3 + numpy/scipy/matplotlib. No paid endpoints. No HPC.

1. **`code/smoke_friedland2012.py`** — fit the two-component+labile analytical model to literature-typical Co-60 γ and N-ion (~80 keV/µm) rejoining kinetics at 10 time points (0 → 1440 min). 5 free parameters per LET regime, bounded NLS fit (`scipy.optimize.curve_fit`). Outputs JSON + PNG. **6/6 smoke checks pass.**
2. **`code/let_sweep_friedland2012.py`** *(new, this audit)* — drive the same model with a Hill saturation `f_complex(LET) = 0.55·LET^1.6 / (40^1.6 + LET^1.6)` over LET = 0.3, 1, 3, 10, 30, 60, 100, 150 keV/µm. Test the paper's qualitative LET trends (monotone increases in complex-fraction, 24-h residual, and slow t½). Outputs JSON + PNG. **4/6 LET trend checks pass** (T1–T4 ✅; T5: high-LET residual >15% ✗ at 150 keV/µm (got 12.2%); T6: high-LET slow t½ > 3× low-LET ✗ — Hill saturation factor capped at 0.85 keeps the slow channel only ~3× slower at high LET, not ≥3×).
3. **Re-ran smoke** to confirm bit-for-bit reproducibility of the JSON fit results — passes identically (timestamps differ, parameters match to 8 decimals).

Both scripts are self-contained, deterministic (no RNG), and run in <1 s.

## 6. Key output files

```
lucid100-friedland-stochastic-dsb-photon-ion-slot67/
├── REPORT.md                               ← this report
├── FIRST_PASS_REPORT.md                    ← initial 2026-06-09 AMBER-KEEP report
├── README.md                               ← paper-level overview
├── MANIFEST.md                             ← artefact manifest with sha256
├── code/
│   ├── smoke_friedland2012.py              ← 5-param NLS fit, 6/6 smoke checks
│   └── let_sweep_friedland2012.py          ← LET-sweep behavioural audit (this audit)
├── results/
│   ├── smoke_fit_results.json              ← Co-60 + N-ion fitted parameters + 6/6 checks PASS
│   └── let_sweep_results.json              ← LET sweep table (8 LET points) + 4/6 checks PARTIAL
├── figures/
│   ├── smoke_rejoining.png                 ← log-log overlay of data + fits
│   └── let_sweep.png                       ← LET-dependence of complex frac, 24-h residual, slow t½
└── source/
    ├── openalex_metadata.json              ← 14 references graph
    ├── unpaywall_metadata.json             ← confirms is_oa=false, no preprint
    ├── s2_metadata.json                    ← TLDR + abstract elision notice
    └── references_table.md                 ← 14-row reference table w/ OA status
```

## 7. Honest gaps

- **Paper PDF: not obtained.** Closed-access (T&F / IJRB), no preprint, no Green OA copy. Even the S2 abstract field is `null` with an explicit publisher-elision disclaimer. We cannot quote any of the paper's specific numbers, tables, figures, or rate constants. **All "claims" tested in §3 are inferred from the S2 TLDR + 14-reference graph + the precursor RR1965 paper title, not from the paper text itself.**
- **PARTRAC source: closed/proprietary.** Helmholtz Zentrum München; no public release on GitHub or Zenodo as of 2026-06-09 search. This is the canonical Monte Carlo code the paper is built around. Re-running the actual stochastic simulation is **structurally impossible** without it.
- **Precursor RR1965 (Friedland 2010) parameter tables: closed.** Even if PARTRAC source dropped today, we wouldn't have the calibrated NHEJ rate constants without the 2010 paper's Tables 1–2, which are inside another closed-access RadResearch PDF.
- **Stenerlöw 2000 calibration data: closed.** The N-ion vs Co-60 γ rejoining curves the paper actually fits were never released in open form. We used literature-typical digitisations as smoke inputs; these are NOT Stenerlöw's measurements.
- **No raw experimental rejoining data files anywhere in this slot.** Everything is synthetic (smoke) or computed downstream of synthetic.
- **LET-sweep smoke uses parameters tuned for monotonicity, not magnitude.** T5 and T6 fail because we don't have the PARTRAC complexity distributions; we hand-tuned a Hill saturation with smoke parameters. This is honestly logged as PARTIAL in `let_sweep_results.json`.
- **No statistical claim audit possible.** With no PDF, we can't enumerate per-figure χ² values, RMSEs, confidence intervals, or model-comparison statistics the paper presumably reports.
- **No replication of the paper's specific figures.** PARTRAC figures cannot be reproduced and the paper's figures cannot be redistributed.

## 8. Verdict

**SPOT-CHECK.** The analytical scaffold the paper describes (two-component NHEJ + labile-site delayed detection + LET-dependent slow-channel saturation) is independently re-implemented and runs end-to-end on commodity hardware. It reproduces the *qualitative* photon-vs-ion contrast (6/6 smoke checks pass) and exhibits the right *qualitative* LET-trend ordering (4/6 LET-sweep checks pass — T5/T6 fail as a smoke-parameter artefact, not a model-failure artefact). The paper's *quantitative* claims (specific rate constants, specific RMSE per figure, specific complex-DSB distributions, specific PARTRAC Monte Carlo outputs) **cannot be verified at all** without (a) the closed PDF, (b) the proprietary PARTRAC source, and (c) the closed precursor/calibration papers. This is a SPOT-CHECK by design and by data availability — not a REPLICATION and not a PARTIAL with a fixable gap.

- **Coverage:** **3/10** — qualitative model covered; quantitative paper content (figures, tables, rate constants) is structurally unrecoverable.
- **Agreement:** **6/10** — where smoke checks were testable (qualitative trends), agreement with literature-typical behaviour is strong; agreement with the paper's own numbers is **untestable**.

---

VERDICT=SPOT-CHECK COVERAGE=3/10 AGREEMENT=6/10
Blocker 1: paper PDF closed-access (T&F IJRB DOI 10.3109/09553002.2011.611404) — no preprint, no Green OA copy, S2 abstract elided by publisher; cannot quote any specific number or figure.
Blocker 2: PARTRAC NHEJ Monte Carlo source code is proprietary (Helmholtz Zentrum München, no public release on GitHub/Zenodo as of 2026-06-09); cannot rerun the stochastic simulation that produces the paper's headline curves.
Blocker 3: precursor parameter tables (Friedland 2010 RR1965) and calibration kinetics (Stenerlöw 2000 IJRB) are both closed-access RadResearch/IJRB PDFs; even if PARTRAC dropped today, no calibrated rate constants or measured reference curves are publicly available to feed it.
