# RE-TIER (2026-06-25): VERDICT = NO-GO (hard ceiling, was SPOT-CHECK)

**Reclassified SPOT-CHECK -> NO-GO** per Rick's rule: a hard-ceiling spot-check (nothing reproducible) belongs in the NO-GO pile.

**Precise blocker (6/22 rule):** Review/opinion piece in a predatory-adjacent venue with NO primary data, NO code, NO parameter tables - nothing to reproduce. Missing artifact: the paper contains no original quantitative model or dataset by design.

---

# LUCID-100 Replication Report

**Paper:** Anders Brahme, "New Radiation Oncology Optimization Principles Based On In-Vivo Predictive Assay and Recent Developments in Molecular Radiation Biology"
**Venue:** *Annals of Case Reports* 9:1625, 2024 (Gavin Publishers)
**DOI:** [10.29011/2574-7754.101625](https://doi.org/10.29011/2574-7754.101625)
**Slot:** LUCID-100 Wave 6 / slot 60 / master-TSV rank 91 (`candidate_curated`, tier B, score 13)
**Auditor:** Ollie subagent, 2026-06-22, host CherryRd (CPU-only, no paid endpoints).

## TL;DR

This is a single-author **review / opinion / synthesis** in a venue (Gavin
Publishers' *Annals of Case Reports*) that is widely flagged as predatory.
It contains **no Methods section, no new data, no code, no supplementary
material, no parameter tables, and no original figures** — all 38 figures
are conceptual diagrams or replots of the author's own prior publications
(refs [1-3, 5-6, 19-21, 23, 34, 45, 51-55]). There is *nothing* to
re-fit. What the paper *does* present explicitly is **Eq. (1)** — the
complication-free-cure formula
`P+ = PB − PI + δ(1 − PB) PI`, δ ≈ 0.2 — together with several
qualitative claims about its behaviour as δ and the tumor dose-response
slope γ_C vary. We re-implemented Eq. (1) on canonical Brahme/Källman
Poisson sigmoid PB / PI, swept δ, and varied γ_C to mimic the high-LET
microdosimetric-heterogeneity penalty the paper describes. We additionally
proved six algebraic limits of Eq. (1) numerically (19/19 checks PASS).
Outputs reproduce the *direction* of the paper's qualitative claims about
δ and γ_C. There is no clinical or population-level claim that can be
*quantitatively* validated because no patient-level data are released.
**Verdict: SPOT-CHECK (formalism only). Coverage 4/10, Agreement 7/10**
on what is analytically checkable.

## 1. Data sources

### Used
- `paper.pdf` (4.69 MB, PDF 1.7) — fetched from
  `gavinpublishers.com/assets/articles_pdf/New-Radiation-Oncology-Optimization-Principles--Based-On-In-Vivo-Predictive-Assay-and-Recent-Developments-in-Molecular-Radiation-Biology.pdf` (OA).
- `paper.txt` (2,159 lines) — `pdftotext -layout` extraction (used because
  the in-house `pdf` tool was unavailable: Anthropic credits, Gemini model
  name, and OpenAI extract plugin were all unusable on the run date).

### Not available (paper-side, this is the reproducibility verdict)
- **No data availability statement.** No raw data; no DOI/URL to a deposited
  data set; no Zenodo/Dryad/GitHub link.
- **No code availability statement.** No code; no language; no repo.
- **No supplementary material.**
- **No numerical parameter tables.** The only tabular content is a small
  insert inside Figure 15 (γ_C, σ_D/D̄, RBE per modality) reported as
  rendered text in the figure, not as a machine-readable table.
- **No patient-level data** for the single illustrative IVPA / PET-CT lung
  case (Figure 11).
- **No RHR / RCR / LQ parameter values** in this paper. The author refers
  the reader to his earlier work (refs [1-3, 23, 34, 45]) for the
  parameters that would be needed to refit cell-survival or TCP/NTCP
  curves.

### Exact missing artifacts (per Rick's hard rule)
1. Per-voxel `D0,eff` maps for the IVPA / BIOART workflow.
2. Patient-level FDG-PET-CT data underlying Figure 11.
3. RHR / RCR cell-survival parameter table (a / b / repair rates, NHEJ vs
   HR partitioning) — needed to reproduce Figure 7/8.
4. Lionel Cohen neutron-vs-photon DRR raw points (Figure 16) and NIRS
   chordoma 5-year local-control table.
5. γ_C, σ_D/D̄, RBE tabular insert from Figure 15 as a machine-readable
   table.
6. A code repository implementing any of the optimization workflows the
   paper sketches (none exists).

The honest description is: there is no original quantitative artifact in
this paper to replicate. The Eq. (1) smoke we ran is an audit of
*formalism* only.

## 2. Methods comparison

| Step | Paper's approach | This audit's approach |
|---|---|---|
| Cell-survival model | LQ → RCR → RHR (Fig 7/8); parameters cited to refs [1-3, 23, 34, 45]. | Not re-implemented (parameters not in paper). |
| TCP / NTCP form | Brahme/Källman Poisson-derived sigmoid (implicit). | Explicit `P(D) = 2 ** (−exp(e·γ50·(1−D/D50)))` per Källman/Brahme convention. |
| Biological objective | **Eq. (1):** `P+ = PB − PI + δ(1 − PB) PI`, δ ≈ 0.2. | Re-implemented verbatim. |
| Optimum dose D* | Stated qualitatively, never tabulated. | Numerically located on a 1001-point dose grid. |
| LET / microdosimetry | γ_C drops with rising LET because of microscopic relative variance (Figs 13-18); table-in-figure values. | Mimicked by halving γ_C from 3.0 to 1.8 (illustrative, not a refit of the Fig 15 insert). |
| IVPA / BIOART | PET-CT before vs after ≈18 Gy → per-voxel D0,eff. | Not re-implementable (no images, no D0,eff maps). |
| Statistical / clinical claims | Asserted from earlier Brahme papers and cited series. | Not re-tested (no data). |

## 3. Quantitative claim audit

Listing all testable quantitative / analytic claims and the audit result.

| # | Claim (paper) | Type | Tested? | Result |
|---|---|---|---|---|
| C1 | Eq. (1) `P+ = PB − PI + δ(1 − PB) PI` is algebraically well-formed (δ ∈ [0,1], PB,PI ∈ [0,1]). | analytic | yes | **PASS** — 19/19 limit checks (L1-L6) PASS in `smoke/eq1_internal_consistency.py`. |
| C2 | δ = 1 (statistical independence) reduces Eq. (1) to `PB·(1−PI)`. | analytic | yes | **PASS** — algebraic identity verified, max\|err\|=1.1e-16 across 20k random (PB,PI). |
| C3 | δ ≈ 0.2 is the clinically realistic regime; δ = 1 over-estimates achievable cure (text near l. 693, l. 1028). | qualitative direction | yes | **DIRECTION CONFIRMED.** In our smoke, δ=1 gives P+_max = 0.554 vs δ=0.2 → 0.512 vs δ=0 → 0.503. P+ is monotone non-decreasing in δ (L6 PASS). Whether 0.2 is the right *value* is a clinical claim we cannot test without patient data. |
| C4 | Increasing LET reduces γ_C via microdosimetric heterogeneity, lowering peak P+ and the therapeutic window (Figs 13-18). | qualitative direction | yes | **DIRECTION CONFIRMED.** Reducing γ_C from 3.0 to 1.8 (δ=0.2) drops P+_max from 0.512 to 0.474 (−3.8 pp) and pulls D* from 63.1 → 61.4 Gy. |
| C5 | γ_C ≈ 4 for neutron/carbon vs ≈ 5–6 for photons/lithium (Figure 15 tabular insert). | quantitative | no | **NOT TESTED.** Values appear inside Figure 15 only as rendered text; no machine-readable source and no underlying TCP fits provided. |
| C6 | Optimal fraction size ≤ 2.3 Gy/Fr; ½ Gy threshold for full DNA repair onset. | quantitative | no | **NOT TESTED.** No model parameters or per-fraction repair-kinetics data in the paper. |
| C7 | Light-ion advantage (He–B) retains fractionation window in plateau; lost for carbon and heavier. | qualitative | no | **NOT TESTED** here; would require depth-LET / depth-dose tables not in paper. |
| C8 | TP53-intact normal tissues are LDHS / LDA. | mechanistic | no | **NOT TESTED.** No per-tissue dose-survival points in paper. |
| C9 | RHR > LQ for describing LDHS. | model-comparison | no | **NOT TESTED.** RHR parameters not given. |
| C10 | Tumor cure ∝ `e^(−N)`; γ_C ≈ ln(N)/e low-LET asymptotic slope. | analytic | yes (recall only) | **TRIVIALLY CONSISTENT** with Poisson eradication; numerical N not pinned in this paper. We did not re-derive. |
| C11 | δ ≈ 0.2 specifically (numerical value, not just regime). | empirical | no | **NOT TESTED.** No clinical fit deposited. |
| C12 | BIOART workflow yields per-voxel D0,eff after ≈18 Gy. | clinical | no | **NOT TESTED.** No images. |
| C13 | Prostate cancer biochemical relapse-free control improves conformal → IMRT → IMPT (Figs 37, 38). | clinical | no | **NOT TESTED.** Cited series not re-analysed. |

**Score:** 4 of 13 claims have a testable analytic / qualitative form
that this audit could touch; 4/4 of those are confirmed in the directions
the paper states. **9 of 13 are not testable from this paper alone**
because the parameters / data live in cited Brahme papers, in clinical
series, or are simply not deposited.

## 4. Scope audit

The paper has **no primary analyzable units** in the dataset sense (no
organisms, no treated cohort with deposited outcomes, no parameter table).
Treating the unit of analysis as "named equations explicitly written
down in this paper that have enough information to evaluate":

| Unit | Re-implemented? |
|---|---|
| Eq. (1) `P+ = PB − PI + δ(1 − PB) PI` | YES |
| Poisson eradication `~ e^{−N}` | trivial; not re-derived |
| `γ_C ≈ ln(N)/e` low-LET asymptote | not re-derived |
| RHR survival form (Fig 7/8) | NO — parameters not in paper |
| LQ / RCR for comparison | NO — parameters not in paper |

**Coverage of the one analytically-complete equation in this paper: 1/1 = 100%.**
**Coverage of the paper's broader scientific scope (38 figures, multiple
clinical/mechanistic claims): well under 50%, since the underlying data
are not in the paper.** The honest single number is **Coverage 4/10**.

## 5. What I actually ran

All on CherryRd (Darwin 25.3.0, CPU-only), Python 3, numpy + matplotlib.
Total wall time < 2 s.

1. `python3 smoke/p_plus_smoke.py` — implements Eq. (1) on canonical
   Brahme/Källman Poisson sigmoid PB (D50=60 Gy, γ_C ∈ {3.0, 1.8}) and PI
   (D50=70 Gy, γ_N=4.0); sweeps δ ∈ {0, 0.2, 1}; also sweeps δ on
   [0,1] in 41 steps; writes `figs/p_plus_smoke.png` (4-panel) and
   `figs/p_plus_smoke.csv` (1001-row dose grid).
2. `python3 smoke/eq1_internal_consistency.py` — proves 6 algebraic limits
   of Eq. (1) (L1-L6) on 20,000 random (PB, PI) draws and verifies the
   smoke's headline numbers from scratch. **19/19 PASS.**

Reproducer:
```bash
cd lucid-brahme-radiobio-optimization-review/smoke
python3 p_plus_smoke.py
python3 eq1_internal_consistency.py
```

### Headline numbers (this run, 2026-06-22, identical to 2026-06-09 run)
```
D50_T = 60 Gy   gamma_C(low LET) = 3.0   gamma_C(high LET) = 1.8
D50_N = 70 Gy   gamma_N          = 4.0
delta = 0.00  ->  P+_max = 0.503  at D* = 62.9 Gy
delta = 0.20  ->  P+_max = 0.512  at D* = 63.1 Gy
delta = 1.00  ->  P+_max = 0.554  at D* = 63.9 Gy
high LET, delta=0.2 -> P+_max = 0.474  at D* = 61.4 Gy
```

## 6. Key output files

```
lucid-brahme-radiobio-optimization-review/
├── REPORT.md                              (this file)
├── README.md
├── FIRST_PASS_REPORT.md                   (earlier 2026-06-09 pass)
├── PROGRESS.md                            (chronological log)
├── paper.pdf                              (source, 4.69 MB)
├── paper.txt                              (pdftotext extract, 2159 lines)
├── artifacts/MANIFEST.md
├── smoke/p_plus_smoke.py                  (Eq.1 reproduction)
├── smoke/eq1_internal_consistency.py      (analytic limit checks, 19/19 PASS)
├── figs/p_plus_smoke.png                  (4-panel plot, 171 KB)
└── figs/p_plus_smoke.csv                  (1001-row dose grid, 71 KB)
```

## 7. Honest gaps

What this audit did **not** and **cannot** do from the paper alone:

1. **No quantitative dataset to refit.** There is no test set, no
   training set, no patient cohort with deposited outcomes, no per-voxel
   image data, no cell-survival data points. Every quantitative
   claim that goes beyond Eq. (1)'s algebra is either restated from a
   cited Brahme paper or shown only graphically.
2. **No code from authors.** No baseline to diff against.
3. **No parameter tables.** RHR / RCR / LQ a/b/repair/NHEJ-HR partitioning
   are not given numerically here; the values live in refs [1-3, 23, 34, 45].
4. **γ_C ≈ 4 vs 5–6 claim (C5) is untested.** The Figure 15 tabular
   insert is not machine-readable from `pdftotext` output, and the
   underlying TCP fits are not in this paper.
5. **Clinical claims (C12-C13) are untouchable.** No images, no cohort
   data; rendered figures only.
6. **δ ≈ 0.2 numerical value (C11) is asserted, not derived.** We can
   only confirm the *qualitative* role of δ in Eq. (1), not that 0.2 is
   the right empirical value.
7. **Venue concern.** *Annals of Case Reports* (Gavin Publishers) is
   widely listed as predatory; we found no peer-review trail. Replication
   value of any individual quantitative claim should be evaluated against
   the primary Brahme refs, not this synthesis.
8. **Tooling.** Internal `pdf` tool was unusable on the run date
   (Anthropic credits, Gemini model name, OpenAI plugin all blocked).
   Worked around with `pdftotext -layout`; this is sufficient for text
   but not for figure-embedded tables (see C5).

## 8. Verdict

**SPOT-CHECK (formalism only).** This is a review/perspective paper with
no new model, no new data, and no code; nothing in it can be *replicated*
in the data-refit sense. What *can* be audited — the single explicitly-
written Eq. (1) and the qualitative claims it underwrites — was audited:
the equation is algebraically consistent (19/19 limit checks PASS), and
the qualitative directions for δ and γ_C reproduce the way the paper
describes them. Recommend retag from `candidate_curated` to
`NO_GO_REVIEW_ONLY` in the LUCID-100 master TSV; if the underlying
science is wanted, the right LUCID slots are the primary Brahme refs
[1-3, 23, 34, 45], not this 2024 synthesis.

**Coverage: 4/10** — 1/1 of the paper's analytically-complete equations
fully audited; 4/13 of the listed testable claims tested. The rest are
unreachable from the paper alone (no data, no code, no parameters).

**Agreement: 7/10** — on the narrow band that *is* testable, the
formalism is internally consistent and the qualitative directions
(δ↑ ⇒ P+↑; γ_C↓ ⇒ P+↓ and D*↓) match the paper. Numerical agreement on
clinical quantities (e.g. δ ≈ 0.2 specifically, γ_C ≈ 4 for n/C vs 5–6
for photons) cannot be established from this paper and is not claimed.

---

**VERDICT=SPOT-CHECK COVERAGE=4/10 AGREEMENT=7/10**

Repro-blocker summary (3 lines):
1. **No original dataset / no patient-level data / no code repository** — the paper is a review of the author's own prior work and contains no new artifact that could be re-fitted.
2. **No parameter tables** for the RHR / RCR / LQ cell-survival comparisons (Figs 7-8) or the γ_C / σ_D/D̄ / RBE per-modality values (Figure 15 insert); they live in cited Brahme refs [1-3, 23, 34, 45], not in this paper.
3. **Venue + provenance risk** — Gavin Publishers' *Annals of Case Reports* is widely flagged as predatory and the figures are non-original; any genuine replication effort should target the primary refs, not this synthesis.
