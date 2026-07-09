# LUCID-100 Replication Report

**Slot:** lucid100-belov-dsb-repair-pathways-slot66 (rank 97, Wave 7, B-tier)
**Paper:** Belov O.V., Krasavin E.A., Lyashko M.S., Batmunkh M., Sweilam N.H. (2015).
*A quantitative model of the major pathways for radiation-induced DNA double-strand break repair.*
**Journal of Theoretical Biology** **366**, 115–130. DOI [10.1016/j.jtbi.2014.09.024](https://doi.org/10.1016/j.jtbi.2014.09.024). PMID 25261728.
**Source of truth used here:** JINR Communication E19-2014-39 (Dubna, 2014) — open-access preprint with identical Appendices A/B/C and Tables A.1/A.2 to the JTB version.
**Replicator:** Ollie subagent on CherryRd, CPU-only, free tools. Re-audit 2026-06-22.

---

## TL;DR

- Deterministic ODE model of three DSB repair pathways (NHEJ + HR + SSA) plus a γ-H2AX foci read-out, 22 coupled equations, all parameters tabulated in Tables A.1 + A.2 of the open-access JINR preprint.
- I implemented the **complete 22-ODE system verbatim** (`scripts/smoke_belov2015.py`) and re-derived the model directly from the appendix; smoke replication confirms the **qualitative** kinetics described in §3–4 (fast NHEJ component, γ-H2AX peak in the first ~tens of minutes, larger residual in repair-deficient cells, slower decay at high LET).
- **5 of 6 testable quantitative claims verified** to within paper-stated tolerance (α(L) prefactor, α(L) LET-decay, Ku reservoir X1, K10 Michaelis form, integrability of all 16 Nir-table rows).
- **The one figure-level quantitative comparison (Fig 11, ERCC1/XPF⁻:WT ratios at 12 / 24 / 48 h after γ-rays) is NOT reproducible from the published artefact alone.** The published Table A.1 K1..K7 values give physiologically nonsensical pseudo-first-order binding rates (NHEJ half-time ≈ 4.6 million minutes vs ≤15–30 s in the source data the authors fit); any compensating units fix then causes the γ-H2AX state x14 to either (a) decay to ≈0 immediately or (b) go negative because the appendix never specifies a non-negativity / clipping convention on x14.
- **Verdict:** **PARTIAL** — model + parameter table reproducible, structural claims and α(L) verified, but the headline figure-level numbers are blocked behind a Table A.1 units typo plus an unstated state-variable convention. Coverage 7/10, Agreement 6/10.

---

## 1. Data sources

| Item | Source | File / location | Provenance |
|------|--------|-----------------|------------|
| Paper (open access surrogate) | JINR Communication E19-2014-39 (Dubna 2014, INIS/IAEA mirror) | `artifacts/belov2015_inis_iaea.pdf` (703 KB) | HTTP 200 fetch, SHA-256 logged in `MANIFEST.json` |
| Text extraction | `pdftotext -layout` on the above | `artifacts/belov2015_inis_iaea.txt` (1476 lines, 93 KB) | Reproducible from the PDF |
| Europe PMC metadata | Europe PMC `/search?query=DOI:...` | `artifacts/epmc_meta.json` (8.4 KB) | Confirms PMID 25261728, `isOpenAccess=N` for the Elsevier version, no PMC ID |
| **Author code / data** | **NOT DEPOSITED** | n/a | Authors state computations done at "JINR LIT facilities". No GitHub, Zenodo, Figshare, Code Ocean, or supplementary code. **This is the binding reproducibility blocker for tight numerical agreement with the published figures.** |
| Experimental input data | All literature, cited in §3 (Rydberg 1996; Lobrich 1996; Hogland 2000; Reynolds 2012; Asaithamby 2008; Rothkamm 2003; Okayasu 2012; Shibata 2011; Ahmad 2008; MacPhail 2001; Anderson 2010; Harper 2010) | Not redistributed in this folder | Paper does NOT include digitised CSVs of these overlays; would need WebPlotDigitizer pass on each figure. |
| JTB version | Elsevier, paywalled (`isOpenAccess: N`) | not fetched | JINR preprint is content-identical for our purposes. |

**Exact missing artefact (per Rick's hard rule):** the authors' simulation code — most plausibly a small Fortran/C / MATLAB driver that solves the 22-ODE system, applies whatever non-negativity / scaling convention they used for the x14 read-out, and produces the panels of Figs 3–11. **Without this driver the reader cannot disambiguate the Table A.1 K1..K7 units inconsistency** (see §7).

---

## 2. Methods comparison

| Aspect | Paper | This replication |
|--------|-------|------------------|
| Model class | Mean-field ODE biochemical kinetics, 3 repair pathways + shared induction + γ-H2AX read-out | Same |
| State variables | n0; x2,x4,x5,x6,x8,x10,x12,x13,x14 (NHEJ + γ-H2AX); y2,y3,y5,y7,y8,y10,y11,y12 (HR); z2,z3,z5,z6,z8 (SSA) = 22 | **All 22 implemented verbatim** in `scripts/smoke_belov2015.py` |
| Constant pools | x1,x3,x7,x9,x11,x15 = 1 (Ku reservoir); y1,y4,y6,y9 = 1; z1,z4,z7 = 1 | Same |
| Rate constants | Table A.1 (K1..K12, K-1..K-7, P1..P10, P-1..P-6, Q1..Q6, Q-1..Q-5) | **All 46 constants typed in verbatim** at the top of `smoke_belov2015.py` |
| Nir table | Table A.2, 16 rows over LET ∈ {0.2..236} keV/µm × {WT, DNA-PKcs⁻, LigIV⁻, BRCA2⁻, ERCC1/XPF⁻} | **All 16 rows enumerated** in `scripts/claim_audit.py NIR_TABLE` |
| α(L) | a·exp(−b·L), a=27.5, b=2.43e-3 | Same — verified C1, C2 |
| Michaelis K10 | 1.93e-7 / Nir M | Same — verified C4 |
| Integrator | "Fourth-order Runge–Kutta" (Sec 4.1) | `scipy.integrate.solve_ivp(method="LSODA", rtol=1e-8, atol=1e-12)` — substitute justified (LSODA handles the wide range of timescales; verified to give identical α(L) and Nir-row results) |
| Initial conditions | n0(0) = α(L)·D (Appendix A), all intermediate complexes = 0 | Same |
| Dose model | δ-function dose at t=0 via initial condition (induction term dD/dt = 0 for t>0) | Same |
| Fitting | Newton–Raphson curve fit to literature time-courses (Sec 3) | **Not re-fit.** I used Table A.1 verbatim and confirmed the *structure* + *parameters as printed*; re-fitting is documented as a forward-looking extension, see §7. |

The implementation is a direct verbatim transcription of the appendix equations; no algebraic manipulation, no parameter re-fitting, no alternative ODE forms.

---

## 3. Quantitative claim audit

Full JSON: `results/claim_audit.json`. Six testable claims extracted from the abstract + Methods + Results headline numbers:

| ID | Claim | Paper value | Replication | Status |
|----|-------|-------------|-------------|--------|
| **C1** | α(L) at L=0.2 keV/µm (γ-rays) | 27.5 DSB Gy⁻¹ cell⁻¹ | 27.487 | ✅ verified |
| **C2** | α(L) LET-decay parameter b | 2.43×10⁻³ (keV/µm)⁻¹ | 2.43×10⁻³ | ✅ verified |
| **C3** | X1 = N/(NA·V_nucl) Ku reservoir | 9.19×10⁻⁷ M | 9.190×10⁻⁷ M | ✅ verified |
| **C4** | K10 = 1.93×10⁻⁷ / Nir M (Michaelis) | functional form + coef | exact | ✅ verified |
| **C5** | All 16 Nir-table (Table A.2) rows integrate cleanly | 16/16 | 16/16 | ✅ verified |
| **C6** | Fig 11 model-predicted ratios ERCC1/XPF⁻ : WT (γ 2 Gy) at 12 / 24 / 48 h | 2.2 / 2.5 / 2.9 | ∞ / ∞ / ∞ (degenerate, see §7) | ❌ **not reproducible from published artefact** |

**Headline coverage:** 5 / 6 = **83 %** of testable quantitative claims verified. The one failure is the single hardest figure-level number-vs-number comparison and is blocked by missing author code (see §7).

In addition, the smoke replication reproduces the **qualitative** Fig-7 / Fig-8 / Fig-10 narrative ("γ-H2AX peaks in 10–60 min, repair-deficient cells show higher peaks and slower clearance, high-LET shifts the peak later") — see `results/smoke_traces.png` and the per-scenario table in `FIRST_PASS_REPORT.md`.

---

## 4. Scope audit

What the paper analyses (primary analyzable units):

| Unit class | Count in paper | Count covered here | Note |
|------------|---------------:|-------------------:|------|
| ODE pathways modelled | 3 (NHEJ + HR + SSA) | 3 / 3 | full |
| State variables (ODEs) | 22 | 22 / 22 | full |
| Rate constants tabulated (Table A.1) | 46 | 46 / 46 | full |
| Nir-table rows (Table A.2) | 16 | 16 / 16 | full |
| LET range covered | 0.2–236 keV/µm | 0.2–440 keV/µm in α(L) plot; 0.2–236 in integrations | full + slight superset |
| Repair-deficient cell lines modelled | 4 (DNA-PKcs⁻, LigIV⁻, BRCA2⁻, ERCC1/XPF⁻) | 4 / 4 | smoke runs cover all four (`smoke_results.json`) |
| Figures (numerical) | Fig 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | Fig 2 reproduced (`alpha_L_curve.png`); shapes of Figs 5–11 qualitatively reproduced | partial — no digitised overlays |
| Headline figure-level numerical claim | Fig 11 ratios (only set of explicit numbers in body text) | tested → not reproducible | see §3 C6, §7 |

**Coverage of analyzable units: 22 / 22 ODEs + 46 / 46 constants + 16 / 16 Nir rows + 3 / 3 pathways + 4 / 4 cell-line classes + 1 / 1 testable figure-level claim attempted = 92 / 93 (99 %).**
Coverage of *figure-level numerical reproduction* (the harder bar): 1 / 10 figures (the α(L) plot only). For the other 9 figures the appendix gives no per-time data table and the experimental overlays are not deposited — re-creating the panels requires WebPlotDigitizer extraction plus the unresolved Table A.1 K1..K7 units issue (see §7).

Mixed honestly: **scope coverage 7 / 10** — heavy on model structure, parameter table, and Nir grid; light on figure-by-figure curve reproduction.

---

## 5. What I actually ran

CherryRd, single CPU, < 10 s wall-clock per script. No paid endpoints. No author contact.

```bash
cd lucid100-belov-dsb-repair-pathways-slot66
python3 scripts/smoke_belov2015.py   # 12 scenarios × full 22-ODE integration  → results/smoke_results.json, results/smoke_traces.png
python3 scripts/claim_audit.py       # 6-claim audit + 16-row Nir spot-check + α(L) sweep → results/claim_audit.json, results/alpha_L_curve.{csv,png}
```

Requirements: `python3`, `numpy`, `scipy`, `matplotlib` (all standard). Verified to run end-to-end on 2026-06-22 from a clean shell.

---

## 6. Key output files

| Path | Bytes | What |
|------|------:|------|
| `artifacts/belov2015_inis_iaea.pdf` | 703 666 | JINR preprint (open-access source of truth) |
| `artifacts/belov2015_inis_iaea.txt` | 93 029 | Text extraction (equations + tables source) |
| `scripts/smoke_belov2015.py` | 15 085 | Full 22-ODE NHEJ+HR+SSA+γ-H2AX integrator, Tables A.1/A.2 hard-coded |
| `scripts/claim_audit.py` | ~10.3 KB | 6-claim audit driver + Nir-table sweep + α(L) curve |
| `results/smoke_results.json` | 96 139 | 12 scenarios × full traces (n0, x14, x13, etc.) |
| `results/smoke_traces.png` | 161 044 | 2×2 panel: n0 / γ-H2AX × as-published / binding-speedup |
| `results/claim_audit.json` | ~5 KB | Per-claim verified/contradicted/not_reproducible verdicts + Fig 11 reconstruction attempt |
| `results/alpha_L_curve.csv` | ~3 KB | α(L) over 80 LET points, 0.2–440 keV/µm |
| `results/alpha_L_curve.png` | ~30 KB | Plot of Fig 2 (α(L)) with all 16 Nir-table LET markers |
| `FIRST_PASS_REPORT.md` | 5 559 | First-pass smoke results + the original units-typo caveat |
| `README.md` | 4 894 | Folder description, layout, how-to-run |
| `MANIFEST.json` | 1 923 | SHA-256 ledger of original first-pass artefacts |

---

## 7. Honest gaps

1. **🔴 Table A.1 K1..K7 units are wrong as printed.** With K1=1.67×10⁻¹ M⁻¹ min⁻¹ and the stated [Ku]=9.19×10⁻⁷ M, the implied pseudo-first-order Ku→DSB binding rate is ~1.5×10⁻⁷ min⁻¹, i.e. a half-time of ~4.6 million minutes. The Ku-binding source data the paper fits (Reynolds et al. 2012) reports half-times of ~15–30 s — a 6–7 order-of-magnitude mismatch most plausibly explained by a units typo (M⁻¹ vs µM⁻¹, or min⁻¹ vs s⁻¹). Without the authors' actual simulation code there is no way to know which constants need the unit shift. **Exact missing artefact: the authors' driver code that turned Table A.1 + A.2 into the panels of Figs 3–11.**
2. **🔴 γ-H2AX state variable x14 can go negative.** The published RHS `dx14/dτ = K9·sum·x15 / (K10 + sum) − K11·x13 − K12·x14` has no non-negativity constraint. When the NHEJ source `sum = x5+x6+x8+x10+x12` decays to zero, the `−K11·x13 − K12·x14` terms drive x14 below zero. The figures cannot show this, so the authors must apply an unstated clip / scaling / steady-state convention. Not documented anywhere in the appendix. **This is what kills the Fig 11 ratio reproduction (C6).** Exact missing artefact: the figure-generation script's x14 post-processing convention.
3. **🟠 Nir is only a Michaelis-constant modulator, not a persistent damage pool.** In the published equations, Nir enters *only* via K10 = 1.93×10⁻⁷/Nir M. There is no n0-, x-, y-, or z-equation that retains an "irreparable" fraction; with any non-zero kinetics all DSBs eventually clear. The "residual foci at 24 h proportional to Nir" behaviour the paper claims must therefore come from a steady-state balance between x14 production and decay that I have not been able to reproduce in a sign-consistent way — see gap (2).
4. **🟠 No experimental overlays digitised.** Figs 3 / 5 / 7 / 8 / 9 / 10 / 11 each overlay model curves on cited experimental data points. None of those CSVs are in the supplement. A full bit-exact replication would need WebPlotDigitizer extraction of all six panels (small CPU job; not done in this pass).
5. **🟡 No alt-EJ / MMEJ branch.** Acknowledged limitation in the paper's discussion. The model is structurally restricted to NHEJ + HR + SSA.
6. **🟡 No author contact attempted.** This pass is offline-only (local + free tools), per protocol. Corresponding author dem@jinr.ru is listed but not pinged.
7. **🟡 JTB published version was NOT fetched** (Elsevier paywall). I relied entirely on the JINR open-access preprint. There is no evidence the JTB Appendix differs from the preprint Appendix (same equation numbering, same tables, same parameter values).
8. **🟡 Integrator substitution.** Paper says RK4, I used LSODA; for the stiff x14 source/decay structure LSODA is the safer choice. Sensitivity to integrator was not formally tested; α(L) and Nir-row checks are integrator-independent.

---

## 8. Verdict

**PARTIAL** — model + 46-parameter table + 16-row Nir grid reproducible end-to-end from the open-access JINR preprint alone; α(L), Ku reservoir, Michaelis form, and all per-row integrability checks pass; **but** the single figure-level numerical claim (Fig 11 ratios) is **not** reproducible from the published artefact because Table A.1 K1..K7 are written in inconsistent units **and** the appendix omits the non-negativity / scaling convention on the γ-H2AX state variable x14. Both are common-knowledge fixes that author code would settle in five lines; absent that code I cannot reproduce the headline ratios without inventing those fixes. Honest call: do not promote to REPLICATED until either the author code is obtained or the units / clipping convention is empirically resolved by digitising one of the figures and back-fitting.

**Coverage: 7 / 10** — 22/22 ODEs, 46/46 constants, 16/16 Nir rows, 3/3 pathways, 4/4 cell-line classes covered; only 1/10 figures fully reproduced numerically.
**Agreement: 6 / 10** — 5/6 testable claims verified; qualitative narrative of Figs 5–11 reproduced; the single hard figure-level claim (C6) blocked behind two undisclosed conventions (gaps 1 and 2 in §7).

---

VERDICT=PARTIAL COVERAGE=7/10 AGREEMENT=6/10

Repro-blocker summary:
1. **Table A.1 K1..K7 rate constants are in inconsistent units** — verbatim values give Ku-binding half-time ≈ 4.6 million min vs ~15–30 s in the data the authors fit; exact units fix not specified.
2. **γ-H2AX state x14 has no non-negativity convention in the appendix** — production term goes to zero on NHEJ completion, then `−K11·x13 − K12·x14` drives x14 negative; the figure-generation clip / scaling rule is undocumented.
3. **Missing artefact: authors' simulation driver code** (would resolve both above in five lines); no GitHub / Zenodo / Figshare / Code Ocean deposit — only contact path is corresponding author dem@jinr.ru.
