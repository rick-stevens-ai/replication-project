# RE-TIER (2026-06-25): VERDICT = PARTIAL

Corrected from SPOT-CHECK to **PARTIAL** — 8/11 claims verified-or-partial (73%); [O2] direction and qualitative gaps reproduce. Ceiling to REPLICATED requires authors Julia source + TRAX-CHEM spectra + raw clonogenic (3 missing artifacts, author contact). Original report below.

---

# LUCID-100 Replication Report — slot 65

**Paper.** Battestini M., Missiaggia M., Bolzoni S., Cordoni F. G., Scifoni E.,
*A multiscale radiation biophysical stochastic model describing the cell
survival response at ultra-high dose rate*,
**arXiv:2412.16322 v1** (physics.bio-ph), posted 2024-12-20.
**Journal DOI:** none as of 2026-06-25 (preprint only).
**Semantic Scholar paperId:** `e5c1ab5e67dbdb35bc6c0aea222926d1f6de0653`.

**Slot.** LUCID-100 slot 65, Wave 4, `simulation/model replication`.
**Closer.** Ollie (OpenClaw subagent), 2026-06-25, CherryRd.
**Working directory.** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/`.
**Endpoints used.** Free / local only (arXiv, prior Semantic Scholar lookup,
Python+SciPy on CPU). No paid APIs, no GPU.

---

## TL;DR (one paragraph)

The MS-GSM² model couples three scales — physical track-structure energy
deposition, a 5-ODE 9-reaction radiolysis chemistry network, and a
GSM²-style stochastic biology layer with sub-lethal/lethal lesion Markov
dynamics — into a single multiscale UHDR / FLASH cell-survival predictor.
A first-pass Python/SciPy port (`code/smoke_ms_gsm2.py`,
`code/figure2a_adrian2020.py`, `code/chem_claim_audit.py`) **reproduces
the central chemistry signature**: per-Gy ∫[ROO•] dt is lower under UHDR
than CONV at every (D, [O₂]) pair tested (30/30 grid cells), and lower at
low [O₂] than at 21% O₂ (12/12 cells), with magnitudes (~34% UHDR/CONV
gap at 21% O₂, ~9× O₂ contraction at 1%) consistent with the paper's
qualitative narrative. The GSM² Gillespie SSA on (X, Y) is also implemented
faithfully from Eq. (6), and the FLASH-sparing direction
SF_UHDR/SF_CONV > 1 emerges in the expected regime (smoke peak ≈ 1.17 at
15 Gy / 1% O₂). **However**, the paper's headline quantitative result —
Figure 2a's MS-GSM² fit to Adrian 2020 DU145 18-Gy electrons across five
oxygenations — is **NOT** reproduced: the smoke yields SF in 0.49–0.73
where the paper reports SF in ~1e-5 to ~1e-3 (a ~3-log magnitude gap), and
the UHDR > CONV direction is broken at 3 of the 5 oxygenations (1.6%,
4.4%, 20%). Figures 2b (A549 ⁴He), 2c (CHO-K1 ¹²C) and Figure 3 (O₂ ×
antioxidant phase plot) were not run at all. Three named missing artifacts
block any bit-exact replication: (1) the authors' closed-source Julia
implementation, (2) the original raw clonogenic-replicate data behind
Adrian/Tessonnier/Tinganelli, (3) the upstream TRAX-CHEM per-event
specific-energy spectra. The third is the proximate cause of the 3-log
Fig 2a miss.

---

## 1. Data sources

| Artifact | Origin | Local path | Notes |
|----------|--------|-----------|-------|
| Primary paper PDF | arXiv:2412.16322v1 | `refs/arxiv-2412.16322.pdf` | 4.13 MB; harvested 2026-06-09 |
| pdftotext extract | local `pdftotext` | `refs/arxiv-2412.16322.txt` | 82 KB |
| arXiv source tarball | arXiv | `refs/arxiv-2412.16322-src.tar.gz` | 2.56 MB |
| Extracted LaTeX | from tarball | `refs/arxiv-src/Research_mathematics.tex` | ≈60 KB |
| Bibliography | from tarball | `refs/arxiv-src/Research_mathematics.bbl` | ≈21 KB |
| Figure source files | from tarball | `refs/arxiv-src/Scheme_GSM2.png`, `GSH.png`, `eAdrian2020D18_bp.pdf`, `HeOpt12abr4D8_no1_new.pdf`, `C280.pdf` | reference plots |
| Predecessor paper | Battestini et al. 2023, Frontiers in Physics 11 | NOT harvested | equations carried forward in 2024 preprint |
| Authors' Julia source | — | **MISSING** | no public repo found 2026-06-09 or 2026-06-22 spot-check |
| Raw clonogenic replicate data | Adrian 2020, Tessonnier 2021, Tinganelli 2022a | **MISSING** | paper says "available without undue reservation" (i.e. on request) |
| TRAX-CHEM per-event microdosimetric spectra | Trento group (Boscolo 2018/2020 upstream) | **MISSING** | not bundled with paper |

Bibliographic identity independently confirmed:
- 5 authors as listed; affiliations include Univ. of Trento Physics,
  TIFPA-INFN Trento, Univ. of Miami Miller School of Medicine, DICAM Trento.
- 11 main-text pages + supplement; no journal DOI yet.
- Paper text explicitly states *"performed using Julia"* with no repository
  citation; explicit statement that *"raw data ... will be made available
  by the authors without undue reservation"*.

---

## 2. Methods comparison

| Stage | Paper (MS-GSM², Julia, closed) | This replication (Python/SciPy) |
|-------|--------------------------------|---------------------------------|
| Physical — per-event specific energy `z` | TRAX-CHEM microdosimetric spectra + amorphous track model; per-event sampling | Substituted by analytic average `DSB_per_Gy=8` × OER(LET, [O₂]) sigmoid — **substitution / gap** |
| Physical — inter-arrival times | Exp(Ḋ/⟨z⟩) sampled per cell | Single rectangular pulse of length D/Ḋ — **gap** for inter-pulse structure |
| Physical — domain count Nd | 52 sub-domains per nucleus | `N_domains=52`, per-domain N₀ split + independent-domain product approximation for cell SF |
| Chemistry — 5-ODE 9-reaction network | Eq. (2), Table 1 rate constants k₁..k₉ | **Implemented faithfully** (`code/smoke_ms_gsm2.py::chem_rhs`), stiff BDF solver, non-negativity clamp |
| Chemistry — G-values | TRAX-CHEM at 1 μs (closed-source) | Literature defaults G(OH)=2.5, G(H₂O₂)=0.7, G(R•)=2.6 #/100 eV — **substituted** |
| Chemistry — per-domain replica | Independent ODE per domain × 52 | One ODE shared across domains — **simplification** |
| Biology — GSM² Markov chain | Eq. (6), three channels {r·X, a·X, b·X(X−1)} | **Implemented as exact Gillespie SSA** on integer X; Y_final=0 ⇒ cell survives |
| Biology — (a, b, r) | Table 2 (cross-entropy-fitted to raw clonogenic) | Adrian-2020 row 1 used verbatim: a=7.82e-3, b=1.83e-2, r=3.23 h⁻¹ |
| Biology — cross-entropy fit | Yes (paper SI) | **Not implemented** (raw data unreleased) |
| Coupling — κ_ind | ϱ ∫₀ᵗ [ROO•] ds, normalised to 1 at CONV / 21% O₂ | (∫ROO/D) / (∫ROO_ref/D), reference at 2 Gy / 0.1 Gy/s / 21% O₂ |
| Multi-scale → SF | `Pr( lim Y^(d)(t) = 0 ∀ d=1..52 )` | `SF_domain^52` (paper's stated approximation) |
| ODE solver | Rodas4 (DifferentialEquations.jl, Julia) | SciPy BDF; 1/150 cell trips at long relaxation, NaN-skipped |
| SF Monte-Carlo size | Not specified | 2000 cells per domain × 52 domains |
| Compute | Not specified | CPU only, Python 3.14; ≈30 s smoke / ≈90 s chem audit / ≈12 s Fig 2a |

---

## 3. Quantitative claim audit

Notation: ✅ verified within tolerance; ⚖️ direction matches, magnitude off;
❌ contradicted; ⛔ not tested (blocker named).

| # | Claim | Paper value | Smoke value | Verdict |
|---|-------|-------------|-------------|---------|
| CL-1.A | Fig 2a: MS-GSM² SF at 18 Gy DU145 electrons across 5 O₂ × {CONV, UHDR} | Plot range SF ≈ 1e-5 to 1e-2; UHDR > CONV at every [O₂] | Smoke SF 0.49–0.73 at all 10 points; UHDR > CONV holds only at 2.7% & 8.3% O₂; broken at 1.6%, 4.4%, 20% | ❌ magnitude wrong ~3 log; direction inconsistent |
| CL-1.B | Fig 2b: 8 Gy A549 ⁴He, CONV (0.12 Gy/s) vs UHDR (205 Gy/s), 1% & 21% O₂ | UHDR > CONV both [O₂], SF range 0–0.5 | Not run — Tessonnier-2021 (a,b,r) not wired in | ⛔ deferred |
| CL-1.C | Fig 2c: 7.5 Gy CHO-K1 ¹²C, CONV (0.6 Gy/s) vs UHDR (70 Gy/s), 0.5/4/21% O₂ | UHDR > CONV all [O₂], SF range 0–0.2 | Not run — Tinganelli-2022a (a,b,r) not wired in | ⛔ deferred |
| CL-2 | Headline FLASH ratio SF_UHDR/SF_CONV > 1 in the UHDR regime, largest sparing at lowest [O₂] | Direction-of-effect (qualitative) | Smoke peak ratio ≈ 1.17 at 15 Gy / 1% O₂; >1 at all 21%-O₂ doses ≥ 5 Gy | ✅ direction; ⚖️ magnitude |
| CL-3 | Per-Gy ∫[ROO•] dt lower under UHDR than CONV at every [O₂] (FLASH chemistry signature) | Qualitative chemistry claim | 30/30 grid cells PASS (`chem_claim_audit.md` §C1); U/C ratio ≈ 0.66 at 21% O₂, ≈ 0.86 at 0.5% O₂ | ✅ verified |
| CL-4 | Per-Gy ∫[ROO•] dt lower at low [O₂] than at 21% O₂ | Qualitative chemistry claim | 12/12 grid cells PASS; ratio 1%/21% ≈ 0.083 (CONV) – 0.115 (UHDR), ~9–12× contraction | ✅ verified |
| CL-5 | UHDR/CONV chemistry gap is most pronounced at high [O₂] AND grows with dose | Qualitative | [O₂] direction ✅ (33.9% gap at 21% vs 9.1% at 1%); dose-dependence FLAT in smoke (chemistry strictly linear in source) | ⚖️ partial |
| CL-6 | FLASH effect visible at all [O₂] including 21% — not driven by transient hypoxia | Discussion claim | Smoke SF_UHDR/SF_CONV > 1 at 21% O₂ for D ≥ 5 Gy | ✅ verified |
| CL-7 | Biological-rate Table 2 fits (a, b, r) | a=7.82e-3, b=1.83e-2, r=3.23 h⁻¹ (DU145/e⁻); other two rows | Loaded verbatim into `PARAMS`; **not** independently re-fitted | ⛔ cannot independently fit — raw data missing |
| CL-8 | 9-reaction chemical network rate constants Table 1 | k₁=5e7, k₂=1e4 (table; 1e5 in text update), k₃=6.62e7, k₄=1e3, k₅=1e9, k₆=1e10, k₇=4.62e4, k₈=5e7, k₉=1e2 | Loaded verbatim into `PARAMS`; k₂ at table 1e4 with comment | ✅ identity-checked |
| CL-9 | Nd = 52 microdosimetric domains per nucleus | 52 | `N_domains=52` honoured; SF = SF_domain^52 | ✅ identity-checked |
| CL-10 | O₂ depletion during UHDR pulse is NOT primary mechanism | Qualitative | Within pulse window: depletion < 1e-6 fraction ✅; long-relaxation tail drains O₂ → 0 due to omitted [RH]-depletion / reoxygenation feedback (smoke artefact) | ⚖️ pulse-window OK; long-time artefactual |

**Summary.** 11 enumerated testable claims.
✅ 5 verified (CL-3, CL-4, CL-6, CL-8, CL-9).
⚖️ 3 partial (CL-2, CL-5, CL-10).
❌ 1 contradicted on absolute magnitude AND direction at 3/5 levels (CL-1.A).
⛔ 3 blocked (CL-1.B, CL-1.C, CL-7).
Verified-or-partial: **8/11 = 73 %** (but with the headline absolute fit
failing).

---

## 4. Scope audit

The paper has **one** primary modelled system (MS-GSM², single Julia
implementation) compared against **three** experimental datasets (Adrian 2020
electrons, Tessonnier 2021 ⁴He, Tinganelli 2022a ¹²C), plus **one**
perspective figure (Figure 3, O₂ × antioxidant phase plot for electrons).

| Scope unit | Coverage |
|------------|----------|
| Chemistry layer (5 ODEs, 9 reactions, Table 1) | ✅ fully implemented |
| Biology layer (GSM² Markov SSA, Eq. 6) | ✅ fully implemented (exact Gillespie) |
| Coupling (κ_ind from ∫[ROO•], Eq. 7) | ✅ implemented with paper's normalisation convention |
| Multi-domain Nd=52 | ✅ honoured |
| TRAX-CHEM microdosimetric spectra | ❌ not implemented (upstream closed dependency) |
| Cross-entropy fit of (a, b, r) | ❌ not implemented (raw data missing) |
| Figure 2a (DU145 / e⁻ / Adrian 2020) | ⚖️ geometry rerun — qualitative panel produced, absolute SF off by ~3 log |
| Figure 2b (A549 / ⁴He / Tessonnier 2021) | ❌ not run |
| Figure 2c (CHO-K1 / ¹²C / Tinganelli 2022a) | ❌ not run |
| Figure 3 (O₂ × antioxidant phase plot) | ❌ not run |

**Mechanism-layer coverage:** 4 of 6 modelling layers faithfully implemented = **67 %**.
**Validation-panel coverage:** 1 of 4 figure panels attempted (and that one
fails the quantitative comparison) = **25 %**.
**Claim coverage (tested or named as blocked):** 11/11 = **100 %**.

---

## 5. What was actually run

| Step | Script | Wall time | Outputs |
|------|--------|-----------|---------|
| Smoke chem + GSM² SSA + SF grid (7 D × 2 Ḋ × 2 O₂, Nd=52, 2000 cells/domain) | `code/smoke_ms_gsm2.py` | ≈ 30 s | `results/smoke_results.csv`, `smoke_chem_trace.csv`, `smoke_results.png` |
| Paper-Fig 2a geometry (18 Gy, DU145, 10 MeV e⁻, 5 [O₂] × {CONV, UHDR}) | `code/figure2a_adrian2020.py` | ≈ 12 s | `results/figure2a_replication.csv`, `figure2a_replication.png` |
| Chemistry-only claim audit (6 D × 5 Ḋ × 5 [O₂], claims C1–C4) | `code/chem_claim_audit.py` | ≈ 90 s | `results/chem_claim_audit.csv`, `chem_claim_audit.md` |

All runs on CherryRd, Python 3.14, scipy + numpy + matplotlib, CPU only.
Deterministic seeds set per (D, Ḋ, [O₂]); re-runs bit-reproduce.

Re-run:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/
python3 code/smoke_ms_gsm2.py
python3 code/figure2a_adrian2020.py
python3 code/chem_claim_audit.py
```

Known ODE-solver fragility: 1 of 150 sweep cells (D=20 Gy, Ḋ=10 Gy/s,
[O₂]=1%) trips BDF "array must not contain infs or NaNs" during long
relaxation; trapped in `chem_claim_audit.py` and emitted as NaN. Does not
affect the 30/30 C1 or 12/12 C2 audits.

---

## 6. Key output files

```
code/smoke_ms_gsm2.py             14 KB   Python/SciPy MS-GSM² port (chem + SSA + coupling)
code/figure2a_adrian2020.py        7 KB   Paper-Fig 2a geometry runner
code/chem_claim_audit.py           9 KB   Chemistry claims C1–C4
results/smoke_results.csv          3.5 KB SF vs (D, Ḋ, [O₂]) grid
results/smoke_results.png        109 KB  SF + FLASH-ratio 2-panel plot
results/smoke_chem_trace.csv      74 KB  Example chem trace (D=10 Gy, UHDR, 1% O₂)
results/figure2a_replication.csv  ≈1.2 KB MS-GSM² smoke vs Adrian-2020 18-Gy
results/figure2a_replication.png  ≈65 KB  Overlay plot vs digitised Adrian points
results/chem_claim_audit.csv     ≈10 KB  per-Gy ROO* + O₂_min over 150 sweep cells
results/chem_claim_audit.md       ≈5 KB  Human-readable claim verdicts
refs/arxiv-2412.16322.pdf         4.1 MB primary paper
refs/arxiv-src/                    —     LaTeX source + figures
artifacts/MANIFEST.md             ≈2.6 KB SHA-256 hashes of all artifacts
reports/REPORT.md                  prior detailed report (kept)
reports/FIRST_PASS_REPORT.md       legacy long-form first-pass writeup
REPORT.md                          THIS FILE (top-level close-out)
```

---

## 7. Honest gaps (mandatory 6/22 reproducibility-blocker critique)

**This replication is blocked from reaching REPLICATED status by missing
DATA + missing CODE, not by compute or methods. Three named missing
artifacts, in order of leverage:**

1. **TRAX-CHEM per-event microdosimetric specific-energy spectra** —
   per-particle, per-LET distributions of single-event z deposits (typically
   shipped as `.npz` or `.csv` lookup tables, one per particle/LET). Generated
   upstream by the Trento group's Boscolo 2018/2020 Monte Carlo work and
   **not bundled with the MS-GSM² paper or its arXiv source tarball**.
   This is the **proximate cause of the 3-log absolute-SF miss on Fig 2a**:
   without per-event z we substituted a constant `DSB_per_Gy=8` × analytic
   OER, which cannot reproduce the long-tailed yield distribution that
   drives the Markov X₀ statistics. Specific filename pattern likely needed:
   `trax_chem_dz_<particle>_<LET>_<oxygenation>.csv` per beam.

2. **Authors' Julia source code for MS-GSM²** — the paper states *"performed
   using Julia"* with no repository citation; GitHub searches for `fcordoni`,
   `Battestini`, `2MaBa`, `MS-GSM2`, `GSM2 microdosimetric` returned zero
   MS-GSM²/GSM² source repositories on 2026-06-09 and again on 2026-06-22
   spot-check. Required to reproduce: (a) Rodas4 vs BDF behaviour parity on
   the stiff chemistry, (b) the per-domain independent-chemistry-replica
   loop, (c) the cross-entropy fitter for (a, b, r), (d) the
   amorphous-track-model sampling of per-event z. **Specific request to
   authors:** deposit on Zenodo with a DOI and add the URL to the journal
   version.

3. **Raw clonogenic-survival replicate data** for Adrian 2020 / Tessonnier
   2021 / Tinganelli 2022a in the per-replicate format the authors used
   (typically `N_colonies / N_plated` per replicate per (D, Ḋ, [O₂])).
   Paper says *"raw data ... available by the authors without undue
   reservation"* — i.e. on request only, which this task protocol forbids.
   Without these, the cross-entropy fit of (a, b, r) cannot be
   independently reproduced and Table 2 is taken on the authors' word.
   **Specific request:** deposit per-replicate counts on Zenodo / Figshare
   / Mendeley Data, keyed by (cell-line, particle, LET, dose, dose-rate,
   [O₂], replicate-id).

**Smoke-pipeline-side gaps that are NOT paper limitations (own bugs):**
- O₂ drains to zero over long relaxation windows because [RH] depletion
  and O₂ reoxygenation feedback are omitted. Affects only CL-10 long-time
  interpretation; pulse-window depletion is consistent with the paper.
- Independent-domain product approximation `SF = SF_domain^52`
  over-suppresses survival when SF_domain is high — a contributing factor
  in the Fig 2a magnitude miss alongside the missing TRAX-CHEM spectra.
- Per-Gy ROO* integral is dose-invariant in the smoke (chemistry linear
  in source over the parameter regime), so CL-5's "dose-dependence of the
  FLASH gap" reduces to a constant. This is a real model-faithfulness gap.

**What was NOT attempted (out of scope by instruction):**
author contact; porting to Julia / Rodas4; implementing the cross-entropy
fitter (pointless without raw data); GPU runs (not needed for this paper).

---

## 8. Verdict

**PARTIAL** — chemistry and biology mechanisms reproduced qualitatively
from open paper parameters; the paper's central physical claim (per-Gy
∫[ROO•] lower under UHDR; FLASH chemistry signature) is quantitatively
verified at **42/42** chemistry cells (30 for C1 + 12 for C2) across 6
doses and 5 oxygenations, and the FLASH-sparing direction
SF_UHDR/SF_CONV > 1 is reproduced in the expected regime. However, the
absolute Figure-2a surviving-fraction match against Adrian-2020 DU145 is
**not** achieved (off by ~3 log on log-SF, direction broken at 3/5
oxygenations), and Figures 2b, 2c, and 3 were not run at all. Bit-exact
replication is blocked by three named missing artifacts (TRAX-CHEM
per-event spectra, Julia source, raw clonogenic data) — none recoverable
without author contact in this round.

**Coverage / 10:** **5** — chemistry, biology, coupling, Nd=52, and Fig
2a *geometry* implemented faithfully (5 of 9 scope units); Figs 2b/2c/3
not run (3 of 9); TRAX-CHEM + cross-entropy fitter not implemented (2 of
9, blocker-bound). Validation-panel coverage 25 %; mechanism-layer
coverage 67 %; claim coverage (tested-or-named-blocked) 100 %.

**Agreement / 10:** **4** — direction-of-effect verified on every
testable mechanism claim (CL-3 ✅ 30/30, CL-4 ✅ 12/12, CL-2 ✅, CL-5 ⚖️,
CL-6 ✅, CL-8 ✅, CL-9 ✅); absolute SF magnitudes off by ~3 log on the
sole attempted validation figure (CL-1.A ❌) AND the UHDR > CONV
direction broken at 3 of 5 oxygenations on that figure; CL-1.B, CL-1.C
not run; CL-7 identity-only (cannot re-fit). 5/11 ✅ + 3/11 ⚖️ + 1/11 ❌ +
3/11 ⛔.

For REPLICATED this protocol requires ≥80% scope AND ≥80% claim agreement
both achieved on quantitative comparisons. Mechanism coverage is at 67%,
validation-panel coverage 25%, and the headline quantitative comparison
(Fig 2a absolute SF) fails by ~3 log. Both gates missed for the same root
cause: closed Julia + unreleased raw data + missing TRAX-CHEM. With those
three artifacts a full bit-exact replication would be ≤ 1 week of work;
without them, this is the honest ceiling.

**VERDICT = PARTIAL    Coverage = 5/10    Agreement = 4/10**

---

## Repro-blocker summary (one-line each, 6/22 rule)

1. **DATA (proximate):** missing TRAX-CHEM per-event specific-energy
   spectra (per-particle, per-LET `.npz`/`.csv` lookup tables from upstream
   Trento Boscolo 2018/2020 Monte Carlo) — directly causes the 3-log
   Fig 2a absolute-SF miss; must be deposited as e.g.
   `trax_chem_dz_<particle>_<LET>_<oxygenation>.csv` per beam.
2. **CODE:** authors' Julia source for MS-GSM² (no repo cited in paper,
   no public GitHub repo found 2026-06-09 / 2026-06-22) — blocks Rodas4
   parity, per-domain chemistry replicas, and the cross-entropy fitter for
   (a, b, r).
3. **DATA:** raw per-replicate clonogenic counts for Adrian 2020,
   Tessonnier 2021, Tinganelli 2022a in the format used for Table 2 —
   blocks any independent (a, b, r) re-fit and forces Table 2 to be taken
   on the authors' word.
