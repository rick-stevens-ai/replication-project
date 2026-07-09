# LUCID-100 Replication Report

**Paper:** Hartzell S, Guan F, Magro G, Taylor P, Taddei PJ, Peterson CB, Kry S.
*Contribution of Nuclear Fragmentation to Dose and RBE in Carbon-Ion Radiotherapy.*
**Radiation Research** 203(2):96–106 (Feb 2025). DOI [10.1667/rade-24-00164.1](https://doi.org/10.1667/rade-24-00164.1) · PMID 39862066 · OpenAlex W4406825186.

**Slot:** lucid100-nuclear-fragmentation-carbon-rbe (Wave 4, backfill slot 39, master rank 70).
**Worktype:** simulation / model replication.
**Date of audit:** 2026-06-22.

---

## TL;DR

The paper is **closed-access** (Allen Press / Sheridan PubFactory / BioOne; Unpaywall
`is_oa=false`, no preprint, no PMC copy, no Zenodo deposit, no GitHub code from the
authors). Source `.md` parse referenced in the protocol is **not staged** for this
slot — only the abstract (OpenAlex / S2 / Europe PMC) and metadata are accessible
free. Three **qualitative** headline claims from the abstract (>30% secondary-fragment
dose fraction in the SOBP; large inter-model RBE spread; secondary C the highest-RBE
fragment in every model) are reproduced with an open-equation re-implementation of
MKM, SMKM, RMF and LEM-I driven by a published Schardt 2010 / Inaniwa 2010 /
Tessonnier 2017 reference SOBP fragment dose-fraction table. **Absolute numerical
agreement is not achievable**: the paper's Monte Carlo (TOPAS/Geant4-DNA-class)
microdosimetric input spectra, exact reference α/β, and per-figure tables are inside
the paywalled article body that this audit cannot read.

**Verdict: SPOT-CHECK.** Coverage 3/10, Agreement 5/10 (qualitative-only).

---

## 1. Data sources

| Source | Type | Status | File |
|---|---|---|---|
| OpenAlex W4406825186 | Bibliographic / abstract | ✅ harvested | `artifacts/metadata/openalex_W4406825186.json` (27.9 KB) |
| Semantic Scholar (`f69a78d56...`) | Abstract + TLDR | ✅ harvested (refs elided) | `artifacts/metadata/semanticscholar.json` (3.7 KB) |
| Unpaywall | OA / repository status | ✅ harvested — `is_oa=false`, `oa_status=closed`, `has_repository_copy=false` | `artifacts/metadata/unpaywall.json` (2.7 KB) |
| Europe PMC | PMID 39862066 record | ✅ harvested — no OA URL, subscription required | `artifacts/metadata/europepmc.json` (6.7 KB) |
| Publisher PDF (BioOne / Allen Press) | Full text | ❌ Cloudflare 403 to scripted clients; subscription required | n/a |
| Preprint (bioRxiv / medRxiv / arXiv) | Pre-publication | ❌ no preprint deposited (Unpaywall + Europe PMC + manual DOI search) | n/a |
| Author code (GitHub) | Source | ❌ 0 author-attributable hits for plausible queries (`Hartzell carbon RBE`, `MKM SMKM RMF LEM carbon fragmentation`, `MCsquare carbon RBE`) | n/a |
| Author data deposit (Zenodo / Figshare / OSF) | Tables / spectra | ❌ none found (Cloudflare also blocks scripted Zenodo browse; checked OpenAlex `datasets` field) | n/a |
| Companion paper Hartzell 2026 (`10.1002/pro6.70059`, *Precision Radiation Oncology*) | Gold-OA follow-up using same 4-model framework | metadata only; PDF also Cloudflare-blocked | metadata in same dir |
| Reference SOBP fragment composition (Schardt 2010 *Rev. Mod. Phys.* 82:383; Inaniwa 2010 *Med. Phys.* 37:5378; Tessonnier 2017 *PMB* 62:6579) | Surrogate input for our re-derivation | ✅ rounded values baked into local CSV | `data/fragment_spectrum_reference.csv` (2.1 KB, sha256 `0df9ac1f…ee730f44`) |

**No paid endpoint used.** All metadata is from free APIs (OpenAlex / S2 with our
`S2_API_KEY` / Unpaywall / Europe PMC).

---

## 2. Methods comparison

| Aspect | Paper (Hartzell 2025) | This audit |
|---|---|---|
| Primary beam | 290 MeV/u carbon, water phantom; monoenergetic + SOBP | Same beam assumed; SOBP fragment composition only (no MC re-run) |
| Particle transport | Monte Carlo (TOPAS / Geant4-DNA class; exact code not stated in abstract) | **None.** Fragment spectrum from open published surrogate (Schardt/Inaniwa/Tessonnier) |
| Fragment species scored | H, He, Li, Be, B, secondary C, primary C, electrons, "other" | Identical 9-species partition; CSV columns match |
| Microdosimetric input | MC-scored y, z*, kinetic-energy spectra per fragment | Closed-form `z*_{1D}(LET) = 0.204 · LET / R_d^2` (Kase 2006) per fragment LETd |
| RBE model 1: MKM | Kase 2008 with tissue-specific α/β | Same formula (`α = αx + βx · z*1D`, `β = βx`); generic chordoma-like `αx=0.10, βx=0.05` |
| RBE model 2: SMKM | Sato & Furusawa 2012 | Closed-form approximation: `α_SMKM = α_MKM + βx · z*1D · (R_d/R_n)^2`, `β = βx` |
| RBE model 3: RMF | Carlson 2008 / Frese 2012 | Closed-form: phenomenological `Σ_p(LET)`, `α = z_F·(αx/Σx)·Σp + θ·βx·(Σp/Σx)^2`, `β = βx·(Σp/Σx)^2` |
| RBE model 4: LEM-I | Scholz & Kraft 1996 / Elsässer 2007 | Closed-form low-fluence surrogate (Krämer 2000 style): `α = αx·(1 + k·LET)·sat + …` with `k=0.012` and a 150 keV/μm saturation cap |
| RBE definition | LQ at fixed prescription dose | LQ at **D = 2 Gy**; isoeffect dose from `αx D + βx D^2 = αp D + βp D^2`, then `RBE = D_x / D` |
| Reference α/β | Tissue-specific (paywalled — not visible to us) | Generic `αx = 0.10 Gy⁻¹`, `βx = 0.05 Gy⁻²` (documented in `rbe_models.py`) |
| Regions analysed | entrance / SOBP / tail | Same |
| Code language | Not stated in abstract | Python 3, numpy + matplotlib only; <1 s wall on CPU |

**Substitution justifications:** Every model uses the canonical open primary
reference for that model. None of them is the *exact* implementation Hartzell 2025
used (which is inaccessible). They are documented surrogates; this is a
qualitative-trends audit, not a tables-match audit.

---

## 3. Quantitative claim audit

Claims pulled from the abstract (the only Hartzell text we can legally read). Headline
*tables* and figure-level numbers are inside the paywalled body and cannot be
quoted/tested.

| # | Claim (verbatim or paraphrase from abstract) | Tested? | This-audit result | Status |
|---|---|---|---|---|
| C1 | "Contributions from secondary fragments were found to exceed 30% of the total physical dose." | ✅ | Secondary-fragment dose fraction in mid-SOBP = **0.330** (entrance 0.195, tail 0.810) using our surrogate composition table. Surrogate-dependent but qualitatively confirms >30% at SOBP. | **VERIFIED (qualitative)** |
| C2 | "Using identical beam parameters, the four models produced not only different RBE values but also different RBE trends." | ✅ | Dose-averaged total RBE at SOBP, 2 Gy: MKM=3.46, SMKM=3.47, RMF=5.31, LEM-I=1.15. Range ≈ 4.2 in absolute units → models clearly disagree. Per-fragment rank orders also differ between models (e.g. RMF puts B>He>H near sec_C; LEM-I compresses everything). | **VERIFIED (qualitative spread)** |
| C3 | "In all models, RBE was highest for secondary carbon ions." | ✅ | All four models return `sec_C` as the highest-RBE fragment (MKM 4.54, SMKM 4.55, RMF 7.47, LEM-I 1.26). | **VERIFIED** |
| C4 | "Beyond secondary carbons, the RBE magnitude typically increased with the atomic number of the fragment, but RBE trends differed dramatically by model and beamline region." | ✅ partial | Our MKM/SMKM produce monotonic RBE-vs-Z up to sec_C (H<He<Li<Be<B<sec_C). RMF and LEM-I deviate from monotonicity, consistent with the abstract's "differed dramatically by model" wording. | **PARTIAL** (we cannot benchmark *region-dependence* of trend rankings against the paper figures we cannot see) |
| C5 | "Variations in fragment RBE were large enough to be apparent in biological dose predictions." | ❌ | Biological-dose maps are figure-level outputs in the paper; we cannot benchmark a number we cannot read. | **NOT TESTED** (paywalled) |
| C6 | Exact RBE values per model per fragment per region (Table 2/3-equivalent of Hartzell) | ❌ | Paywalled. Our absolute numbers (especially LEM-I≈1.15 and RMF≈5.3) almost certainly disagree with the published values; LEM-I closed-form lacks the track-structure integral and RMF closed-form lacks calibrated Σ(LET). | **NOT TESTED** (paywalled) |
| C7 | Exact monoenergetic-beam Bragg peak depth, SOBP width, prescription dose, reference cell line / α/β pair | ❌ | Inside paywalled methods section. | **NOT TESTED** (paywalled) |

**Score on testable abstract-level claims:** 3 fully verified (qualitative), 1
partial, 3 not testable due to paywall.

---

## 4. Scope audit

What the paper covers vs what this audit covers:

| Analyzable unit | Paper | This audit | Coverage |
|---|---|---|---|
| RBE models compared | 4 (MKM, SMKM, RMF, LEM-I) | 4 (same set, closed-form surrogates) | 4/4 |
| Beam configurations | monoenergetic + SOBP carbon at 290 MeV/u, water phantom | SOBP only (no MC, no monoenergetic Bragg curve) | 1/2 |
| Beamline regions | entrance / SOBP / tail | entrance / SOBP / tail | 3/3 |
| Fragment species | 9 (H, He, Li, Be, B, sec C, prim C, e⁻, "other") | 9 (identical labels) | 9/9 |
| Per-fragment inputs (Monte Carlo) | MC-scored microdosimetric spectra, DSB yields, KE spectra, dose fractions | Single LETd value per fragment + dose fractions from open published surrogate | weak — input-quality blocker |
| RBE figures in the paper | Unknown number of figures (closed-access) | 2 figures (per-fragment RBE bar plot; total RBE vs model bar plot) | not directly comparable |
| RBE tables in the paper | Unknown table count (closed-access) | 1 CSV + 1 JSON of full per-fragment numbers | not directly comparable |
| Biological-dose / DSB-yield maps | Yes (per abstract) | Not produced | 0% |
| Statistical analysis (uncertainty propagation) | Not described in abstract | Not done | n/a |

**Honest coverage:** about 30 % of the paper's analyzable scope — qualitative claims
and per-fragment RBE structure replicated, all MC + biological-dose output not
attempted. Full coverage would require the article body and either the original MC
output spectra or a TOPAS/Geant4-DNA re-run (documented in `reports/JOB_PLAN_heavy_MC.md`).

---

## 5. What I actually ran

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-nuclear-fragmentation-carbon-rbe
python3 code/smoke_replication.py
```

Wall time < 1 s on CherryRd CPU (Apple M-class). Pure numpy + matplotlib. No GPU,
no MC, no internet.

Re-verified 2026-06-22 19:00 CDT — output identical to the 2026-06-09 first-pass run:

```
[smoke] dose fractions per region: {'entrance': 1.0, 'sobp': 1.0, 'tail': 1.0}
[smoke] secondary-fragment dose fraction per region: {'entrance': 0.195, 'sobp': 0.33, 'tail': 0.81}
[smoke] total RBE  entrance  MKM=3.539  SMKM=3.552  RMF=5.438  LEM-I=1.159
[smoke] total RBE  sobp      MKM=3.456  SMKM=3.468  RMF=5.308  LEM-I=1.151
[smoke] total RBE  tail      MKM=2.927  SMKM=2.937  RMF=4.427  LEM-I=1.108
[smoke] highest-RBE fragment (MKM):   sec_C  RBE=4.538
[smoke] highest-RBE fragment (SMKM):  sec_C  RBE=4.554
[smoke] highest-RBE fragment (RMF):   sec_C  RBE=7.474
[smoke] highest-RBE fragment (LEM-I): sec_C  RBE=1.261
[claim] claim_1_secondary_fragment_dose_gt_30pct_in_SOBP: passes=True
[claim] claim_2_intermodel_RBE_spread_gt_zero: passes=True
[claim] claim_3_secondary_C_is_highest_RBE_fragment: passes=True
```

What was **not** run on this host (per CherryRd compute policy): TOPAS-nBio /
Geant4-DNA Monte Carlo of a 290 MeV/u carbon beam in a water phantom. That job
plan is in `reports/JOB_PLAN_heavy_MC.md`; recommended host **uicgpu** (no GPU
needed; large RAM for phase-space scoring), wall-time estimate ~3 days for the
full 4-model × 3-region × 4-energy matrix.

---

## 6. Key output files

| Path | Bytes | sha256 | What it is |
|---|---|---|---|
| `data/fragment_spectrum_reference.csv` | 2097 | `0df9ac1f78809e5dea6d796b0e49465b2214c89f26c8cc12eed08815ee730f44` | Reference SOBP fragment composition (Schardt/Inaniwa/Tessonnier surrogate) |
| `code/rbe_models.py` | 7982 | `b7e3d87c8769095d670ebca57e837928288d8ef84d466653cad717109cc9f3dc` | MKM, SMKM, RMF, LEM-I closed-form implementations + LQ-RBE solver |
| `code/smoke_replication.py` | 8566 | `293225dd206179f2f0686a94d14946f9cf49188229225ae202740440defead05` | Driver: per-fragment α/β/RBE per model, dose-averaged totals, figures, JSON |
| `figures/per_fragment_rbe.png` | 32854 | `d09a4a1e129f9bce25d6416b85241febedf47ce8164d2062ed7a7ca2d47da003` | Per-fragment RBE₂Gy by model |
| `figures/total_rbe_vs_model.png` | 22848 | `2b267e7f5852f707eb3d4f94ac6ae1c6747b86fbfc6a30963500530fb415a6e1` | Dose-averaged total RBE per region × model |
| `reports/smoke_results.json` | 8602 | `d539a1aa07682498ac7732f750e26d35e174844a391c1198363ade195d600e50` | Full numerical output + claim-check pass/fail + provenance |
| `reports/smoke_results.csv` | 1239 | `78322a58fb8de695e1ae7397c13c565321176701254fe7b0cd0bfe24060aa274` | Long-form (model, fragment, α, β, RBE) table |
| `reports/FIRST_PASS_REPORT.md` | 5430 | `818a7b0d8823a8662a555747a4e58e5f19e96aa9ba2b2a8b714ca6935f1ce749` | Narrative first-pass report (predecessor to this REPORT.md) |
| `reports/JOB_PLAN_heavy_MC.md` | 4162 | `7793f7bdbf2f055e7adfd3bf8e69c7cc2926613719a33824168f1da7a56ba957` | Resource plan for a real TOPAS/Geant4-DNA reproduction |
| `artifacts/metadata/{openalex,semanticscholar,unpaywall,europepmc}.json` | 27.9 / 3.7 / 2.7 / 6.7 KB | (see `ARTIFACT_MANIFEST.md`) | All free-API bibliographic / OA-status records used |

---

## 7. Honest gaps

1. **No paper body.** Hartzell 2025 is closed-access (Unpaywall `is_oa=false`, no
   preprint, no PMC, no Zenodo). The protocol's "source .md (Marker parse)" was not
   staged for this slot; we only have the abstract. Everything below "the abstract
   says X" is unverified against the paper's actual tables/figures.
2. **No Monte Carlo.** Hartzell ran a full MC pipeline; we did not. Fragment
   composition is a Schardt/Inaniwa/Tessonnier-style surrogate. Numeric LETd values
   per fragment are rounded literature midpoints, not the paper's MC-scored values.
3. **No microdosimetric spectra.** MKM/SMKM in the paper consume scored y- or
   z*-distributions; we substitute a single `z*_{1D}(LET)` closed form. This loses
   stochastic-variance content that matters for the M→SM differences.
4. **No real LEM-I track integral.** Our LEM-I closed form is a low-fluence
   surrogate; it badly underpredicts absolute LEM-I RBE (≈1.15 vs published ≈2–4).
   Qualitative trend is preserved, absolute number is not.
5. **No real RMF DSB-yield surface.** Σ(LET) is a phenomenological monotonic fit;
   the paper presumably uses Carlson's calibrated MCDS-driven yields. Our absolute
   RMF RBE (≈5.3) is high.
6. **Reference α/β.** Generic `αx=0.10, βx=0.05` substituted; the paper's
   tissue-specific values are paywalled.
7. **Biological-dose / DSB-yield maps not attempted.**
8. **Region trends only spot-checked.** "Entrance vs SOBP vs tail" trend ordering
   is checked at one set of dose-fraction values per region; no depth scan.

---

## 8. Verdict

**SPOT-CHECK** of qualitative claims only. The three abstract-level headline claims
(>30 % secondary-fragment dose in the SOBP, large inter-model RBE spread, secondary
C the top fragment in every model) are reproduced with open-equation, free-tool
re-derivations and a published reference fragment spectrum. Every quantitative
table/figure-level claim is locked behind the paywall and was not testable.

| Metric | Score | Justification |
|---|---|---|
| **Coverage** | **3 / 10** | 4/4 models, 3/3 regions, 9/9 fragments at the *label* level; but only the SOBP beam is touched, no MC, no microdosimetric spectra, no biological-dose maps, no per-figure replication. ~30 % of the paper's analyzable scope. |
| **Agreement** | **5 / 10** | All three qualitative abstract claims reproduce in direction; absolute numbers for LEM-I (~1.15 vs published 2–4) and RMF (~5.3 vs published 2–4) clearly diverge from clinical literature, and we cannot benchmark MKM/SMKM absolute numbers against the paper's tables. Mid score reflects "trends right, magnitudes ballpark or worse, tables not benchmarked." |

---

VERDICT=SPOT-CHECK COVERAGE=3/10 AGREEMENT=5/10

Repro-blocker summary (3 lines):
1. Paper body is closed-access (BioOne / Allen Press; Unpaywall `is_oa=false`); no preprint, no PMC, no Zenodo, no GitHub from the authors — exact MC-scored fragment spectra, reference α/β, and per-fragment RBE tables are unreadable from this audit. Missing artifact: Hartzell 2025 full-text PDF or supplementary spectra CSV / Geant4-DNA macro.
2. The work is a TOPAS-nBio / Geant4-DNA-class Monte Carlo pipeline; no author code repository exists, so the MC re-run must be re-implemented from scratch. Missing artifact: author TOPAS macro + Geant4-DNA scoring tally definitions (likely sitting on an MD Anderson internal share).
3. LEM-I and RMF require a full track-structure integral / calibrated DSB-yield surface (MCDS-driven Σ) to reach absolute-RBE agreement; our closed-form surrogates intentionally trade absolute accuracy for runtime. Missing artifact: the paper's stated reference α/β per region and exact Σ(LET) parameterization — both buried in the paywalled methods section.
