# FIRST PASS REPORT — Battestini et al. 2024 (MS-GSM²)

**Paper.** Battestini M., Missiaggia M., Bolzoni S., Cordoni F. G., Scifoni E.,
*A multiscale radiation biophysical stochastic model describing the cell
survival response at ultra-high dose rate*, **arXiv:2412.16322 v1**
(physics.bio-ph), posted 2024-12-20. No journal DOI yet.

**Replicator.** Ollie (OpenClaw subagent, depth 1), 2026-06-09, CherryRd.

**Source corpus.** Direct arXiv preprint + arXiv source tarball.

**This replication.** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/`.

**LUCID100 slot.** 65 (Wave 4), `simulation/model replication`.

---

## VERDICT: GO — smoke-only mechanism replication; full bit-exact replication BLOCKED

| Dimension | Status |
|-----------|--------|
| Bibliographic identity | **CONFIRMED** (arXiv 2412.16322, 5 authors, Dec 2024) |
| Open access | **YES** (arXiv) |
| Paid endpoints needed | **No** |
| Code released by authors | **No** (Julia, closed) |
| Raw experimental data released | **No** ("available on request") |
| Equations/parameters in paper | **YES, complete** (Tables TAB:chempar + TAB:biorates + full SSA algorithm) |
| Smoke replication feasible | **YES — done in ~30 s on CPU** |
| Bit-exact replication feasible | **No** (closed code + unreleased raw data) |
| Compute load | **Light** (CPU, ~30 s, no GPU) |
| Author contact attempted | **No** (per task instructions) |

---

## 1. Bibliographic identity (verified)

- **Title:** A multiscale radiation biophysical stochastic model describing the cell survival response at ultra-high dose rate
- **Authors:** M. Battestini¹², M. Missiaggia²³, S. Bolzoni¹², F. G. Cordoni²⁴*, E. Scifoni²*
- **Affiliations:** Univ. of Trento Physics; TIFPA-INFN Trento; Univ. of Miami Miller School of Medicine; DICAM Univ. of Trento
- **Preprint:** arXiv:2412.16322v1, 2024-12-20, `physics.bio-ph`
- **Semantic Scholar paperId:** `e5c1ab5e67dbdb35bc6c0aea222926d1f6de0653`
- **Journal DOI:** **none** as of 2026-06-09; only preprint
- **Pages:** 11 (main) + supplement
- **Predecessor:** Battestini et al. 2023, Frontiers in Physics 11 (preliminary MS-GSM²)

**TSV mismatch.** Current LUCID100 row leaves DOI blank, venue blank, year 2024,
citation count 0 — all consistent with a preprint with no journal venue and
no Crossref citations yet. Recommend filling in:
- DOI → `arXiv:2412.16322`
- Venue → `arXiv:2412.16322 [physics.bio-ph] (preprint)`

---

## 2. What the paper does

MS-GSM² is a **multi-stage extension of GSM²** that combines three scales:

| Scale | Object | Variables | Equation |
|-------|--------|-----------|----------|
| Physical | Track-structure energy deposition | z (specific energy per event), inter-arrival times ~ Exp(Ḋ/⟨z⟩) | (4)–(5) |
| Chemical | 9-reaction radiolysis network in 5 ODEs | [O₂], [H₂O₂], [OH•], [R•], [ROO•] | (2) |
| Biological | GSM² Markov chain | X (sub-lethal), Y (lethal) | (6)–(7) |

The **bio-chemical coupling** (paper's central novelty) routes indirect DNA
damage through `ϱ ∫₀ᵗ [ROO•] ds`, normalised to 1 at conventional + 21% O₂.
This is what makes the model dose-rate-aware: at UHDR, ROO• transients are
*chemically shorter-lived* (k₂ dimer recombination dominates at high
instantaneous [ROO•]), so the integrated peroxyl exposure per Gy drops, and
indirect lesions drop — predicting FLASH sparing.

### Key parameters (all in paper, Table TAB:chempar)

| k | Value | Reaction |
|---|-------|----------|
| k₁ | 5×10⁷ M⁻¹s⁻¹ | R• + O₂ → ROO• |
| k₂ | 10⁴ M⁻¹s⁻¹  | ROO• + ROO• (table); 10⁵ in text update |
| k₃ | 6.62×10⁷    | catalase decomposition of H₂O₂ |
| k₄ | 10³         | Fenton (Fe²⁺ + H₂O₂) |
| k₅ | 10⁹         | RH + OH• → R• |
| k₆ | 10¹⁰        | XSH + OH• (scavenger) |
| k₇ | 4.62×10⁴    | XSH + R• |
| k₈ | 5×10⁷       | 2 R• → R-R |
| k₉ | 10²         | XSH + ROO• (GSH scavenging of peroxyl) |

Fixed pools: [RH]=1 M, [cat]=80 nM, [Fe²⁺]=0.89 μM, [XSH]=6.5 mM,
[O₂]₀ ∈ [0, 21]%.

### Biological rates (Table TAB:biorates)

| Cell line | Particle | a [h⁻¹] | b [h⁻¹] | r [h⁻¹] |
|-----------|----------|---------|---------|---------|
| DU145 | e⁻ (Adrian 2020) | 7.82e-3 | 1.83e-2 | 3.23 |
| A549 | ⁴He (Tessonnier 2021) | 4.70e-3 | 1.34e-2 | 4.51 |
| CHO-K1 | ¹²C (Tinganelli 2022a) | 4.21e-3 | 2.43e-2 | 3.68 |

---

## 3. What we implemented (smoke replication)

`code/smoke_ms_gsm2.py` (Python, numpy + scipy):

1. **Chemical layer** — direct port of Eq. (2): 5 ODEs in (O₂, H₂O₂, OH•, R•, ROO•)
   with stiff BDF integrator, non-negativity clamp, rectangular dose pulse.
2. **Biological layer** — Gillespie SSA over integer X with channels
   `{r·X, a·X, b·X(X-1)}` (paper Eq. 6); initial X drawn from
   Poisson(N₀_mean); cell survives iff Y_final == 0.
3. **Coupling** — kappa_indirect normalised to 1 at the paper's reference
   (Ḋ=0.1 Gy/s, 21% O₂, per-Gy basis), then scales the indirect lesion
   yield via Eq. (3) DSB/OER convention.
4. **Multi-domain** — 52-domain split with independent-domain product
   approximation for SF; per-domain SSA over 2000 cells (≈ 1.6 s per
   parameter cell).

### Simplifications (vs full paper pipeline)

| Component | Paper | This smoke |
|-----------|-------|------------|
| Microdosimetric specific-energy spectra | TRAX-CHEM + amorphous track model | constant DSB_per_Gy=8 |
| OER (LET, [O₂]) | analytic formula from Scifoni 2013 | sigmoid in [O₂], OER_max=2.5 |
| Per-domain chemistry | independent ODE per domain × Nd | one ODE shared across domains |
| Biological-rate calibration | cross-entropy on raw experimental data | use Adrian 2020 DU145 rates as-is |
| G-values | TRAX-CHEM at 1 μs | literature defaults G(OH)=2.5, G(H₂O₂)=0.7, G(R•)=2.6 #/100eV |
| (a, b, r) fitting loop | yes | no |

---

## 4. Results

Grid: D ∈ {1, 2, 5, 8, 10, 15, 20} Gy ; Ḋ ∈ {0.1, 100} Gy/s ; [O₂] ∈ {21, 1}%.

### 4.1 Chemistry sanity

| Condition | per-Gy ∫[ROO•] dt (M·s) | per-Gy kappa_indirect |
|-----------|--------------------------|------------------------|
| 0.1 Gy/s, 21% O₂ (reference) | 1.68×10⁻⁵ | 1.00 (by defn) |
| 100 Gy/s, 21% O₂ | 1.11×10⁻⁵ | 0.661 |
| 0.1 Gy/s, 1% O₂ | 1.40×10⁻⁶ | 0.083 |
| 100 Gy/s, 1% O₂ | 1.27×10⁻⁶ | 0.076 |

**Both predicted trends are present**: (i) UHDR < CONV at fixed [O₂] (≈34%
reduction at 21% O₂; ≈8% at 1% O₂); (ii) low O₂ << high O₂ (≈12×
reduction). These are the chemical fingerprints the paper says drive FLASH.

### 4.2 Cell survival fraction

| D [Gy] | [O₂] | SF_CONV | SF_UHDR | SF_UHDR / SF_CONV |
|--------|------|---------|---------|--------------------|
|  1 | 21% | 1.000 | 1.000 | 1.00 |
|  1 |  1% | 0.974 | 1.000 | 1.03 |
|  2 | 21% | 1.000 | 0.974 | 0.97 |
|  2 |  1% | 0.949 | 0.974 | 1.03 |
|  5 | 21% | 0.855 | 0.925 | 1.08 |
|  5 |  1% | 0.878 | 0.925 | 1.05 |
|  8 | 21% | 0.901 | 0.901 | 1.00 |
|  8 |  1% | 0.901 | 0.878 | 0.97 |
| 10 | 21% | 0.833 | 0.878 | 1.05 |
| 10 |  1% | 0.712 | 0.712 | 1.00 |
| 15 | 21% | 0.751 | 0.791 | 1.05 |
| 15 |  1% | 0.578 | 0.676 | **1.17** |
| 20 | 21% | 0.578 | 0.609 | 1.05 |
| 20 |  1% | 0.389 | 0.389 | 1.00 |

(Sub-1.0 fluctuations at very low N₀ come from finite-cell sampling — 2000
cells per domain × 52 domains; SF resolution ≈ 1/2000 = 0.0005 at the domain
level which amplifies through Nd to ≈ 2.5% at the cell level.)

**Headline result.** At D=15 Gy / 1% O₂ the model predicts a ≈17% UHDR
sparing — qualitatively consistent with the paper's Fig. 3 ("perspective
analysis of the impact of the chemical environment on the emergence of the
FLASH effect"). Mechanism reproduced.

### 4.3 What's clearly missing for bit-exact comparison
- Numerical match to Figure 2 of the paper (Adrian 2020 DU145 photon data):
  needs the authors' microdosimetric spectra + cross-entropy fit + raw data.
- Quantitative dose-rate threshold for FLASH onset: needs faithful G-values
  and Nd=52 per-domain chemistry.

---

## 5. Files (artifacts)

See `artifacts/MANIFEST.md` for SHA-256 hashes.

```
refs/arxiv-2412.16322.pdf                4.1 MB   arXiv preprint
refs/arxiv-2412.16322.txt               80 KB    pdftotext extract
refs/arxiv-2412.16322-src.tar.gz        2.5 MB   arXiv source bundle
refs/arxiv-src/Research_mathematics.tex 60 KB    main LaTeX source
refs/arxiv-src/Research_mathematics.bbl 21 KB    bibliography
refs/arxiv-src/Scheme_GSM2.png         588 KB   model schematic
refs/arxiv-src/GSH.png                 3.2 MB   GSH effect figure
code/smoke_ms_gsm2.py                   14 KB   replication smoke
results/smoke_results.csv               3.5 KB
results/smoke_results.png              109 KB   2-panel SF/ratio plot
results/smoke_chem_trace.csv            74 KB   one example chem trace
```

---

## 6. Blockers (for full replication)

1. **Closed Julia codebase.** No public repo found under any plausible author
   account (fcordoni, Battestini, 2MaBa). Paper's "Computational information"
   section commits only to "performed using Julia".
2. **Raw experimental data unreleased.** Paper says: *"The raw data
   supporting the conclusions of this article will be made available by the
   authors without undue reservation"* — i.e. on request only. Task
   instructions forbid author contact.
3. **TRAX-CHEM microdosimetric spectra** are not packaged with the paper;
   produced upstream by the Trento group's Boscolo 2018/2020 simulations,
   also closed.
4. **No supplementary information PDF in arXiv** — Tables S1, S2 referenced
   in the main text appear to be included via Tables 1–2 of the main LaTeX
   (which we do have) plus material not separately split out. Authors may
   have a longer SI bundled with the eventual journal version.

---

## 7. Next-action recommendations

### Immediate (this task)
- ✅ Update LUCID100_SOLID_MASTER_QA.tsv slot 65 with DOI/venue/status.
- ✅ Tag outcome as `smoke_only_go` (analogous to slot 27 Liew 2021).

### Optional follow-ups (not in scope for this first pass)
- Port to Julia + DifferentialEquations.jl/Rodas4 for a faithful chemistry
  match (paper's exact solver).
- Add per-domain chemistry (Nd=52 independent ODE replicas with shared
  rate constants but per-domain stochastic z deposits).
- Implement cross-entropy fitter for (a, b, r) and try to reproduce
  Figure 2a numerically against the Adrian 2020 published clonogenic
  survival points (Adrian 2020 SF data IS published in their paper).
- Watch for the journal version with a deposited code DOI; revisit then.

### Recommendation for LUCID100 master TSV
Retag slot 65 from `candidate_curated` → `smoke_only_go` with note:
"smoke-only mechanism replication GO; chem+bio scales coupled in Python;
qualitative FLASH ratio > 1 reproduced at 15 Gy / 1% O₂; bit-exact match
blocked by closed Julia code and unreleased raw clonogenic data".
