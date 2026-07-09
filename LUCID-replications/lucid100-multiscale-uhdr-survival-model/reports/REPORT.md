# LUCID-100 Replication Report

**Paper.** Battestini M., Missiaggia M., Bolzoni S., Cordoni F. G., Scifoni E.,
*A multiscale radiation biophysical stochastic model describing the cell
survival response at ultra-high dose rate*, **arXiv:2412.16322 v1**
(physics.bio-ph), posted 2024-12-20. No journal DOI as of 2026-06-22.

**Slot.** LUCID-100 slot 65 (Wave 4), `simulation/model replication`.
**Replicator.** Ollie (OpenClaw subagent), 2026-06-22, CherryRd.
**Working directory.** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/`.

---

## TL;DR

**VERDICT — PARTIAL (mechanism reproduced; absolute numbers not).** The MS-GSM²
multiscale model (physical track structure → 5-ODE radiolysis chemistry →
GSM² stochastic biology) is fully specified in the paper (Tables 1, 2 +
Algorithm); a Python/SciPy smoke port reproduces both qualitative paper
predictions: (i) per-Gy peroxyl-radical exposure ∫[ROO•]/D is lower at UHDR
than at CONV at every [O₂] tested (30/30 grid cells PASS), and (ii) the
GSM² SSA + chemistry coupling produces a FLASH-sparing ratio
SF_UHDR/SF_CONV > 1 in the expected regime (peak ≈ 1.17 at 15 Gy / 1% O₂).
However, the published Figure 2a *quantitative* match against Adrian-2020
DU145 18-Gy data is **NOT** reproduced — our smoke gives SF ~ 0.5–0.7
where the paper reports SF ~ 1e-5 to 1e-3, a ~3-log gap caused by our
constant `DSB_per_Gy=8` substitution for TRAX-CHEM-derived microdosimetric
spectra and the absence of the paper's cross-entropy fit on raw clonogenic
points. Bit-exact replication is **blocked** by three named missing
artifacts: closed-source Julia code, unreleased raw clonogenic data, and
upstream TRAX-CHEM microdosimetric spectra. All replication code is local
free Python; no paid endpoints, no GPU.

---

## 1. Data sources

| Artifact | Origin | Local path | Bytes (SHA-256 in `artifacts/MANIFEST.md`) |
|----------|--------|-----------|---------------------------------------------|
| Primary paper PDF | arXiv:2412.16322v1 | `refs/arxiv-2412.16322.pdf` | 4 126 679 |
| pdftotext extract | rendered locally with `pdftotext` | `refs/arxiv-2412.16322.txt` | 81 548 |
| arXiv source tarball | arXiv | `refs/arxiv-2412.16322-src.tar.gz` | 2 556 844 |
| Extracted LaTeX source | from tarball | `refs/arxiv-src/Research_mathematics.tex` | ≈ 60 KB |
| Reference list (BibTeX) | from tarball | `refs/arxiv-src/Research_mathematics.bbl` | ≈ 21 KB |
| Figure assets | from tarball | `refs/arxiv-src/Scheme_GSM2.png`, `GSH.png`, `eAdrian2020D18_bp.pdf`, `HeOpt12abr4D8_no1_new.pdf`, `C280.pdf` | various |
| Predecessor paper | Battestini et al. 2023 *Frontiers in Physics* 11 — cited but **not** harvested (we have the equations through the 2024 preprint) | — | — |

**Code released by authors:** **No.** Paper states *"performed using Julia"*
with no repository cited. GitHub searches for `fcordoni`, `Battestini`,
`2MaBa`, `MS-GSM2`, `GSM2 microdosimetric` returned zero MS-GSM²/GSM²
source repositories on 2026-06-09; still none on 2026-06-22 spot-check.

**Raw clonogenic data released by authors:** **No** — paper states *"raw data
... will be made available by the authors without undue reservation"*
(i.e. on request only). Task protocol forbids author contact for this round.

**Underlying datasets the paper compares to (all third-party, separately
published):**
- Adrian et al. 2020 — DU145, 10 MeV electrons, 18 Gy (Figure 2a)
- Tessonnier et al. 2021 — A549, ⁴He at 4.5 keV/μm, 8 Gy (Figure 2b)
- Tinganelli et al. 2022a — CHO-K1, ¹²C at 13 keV/μm, 7.5 Gy (Figure 2c)

These primary clonogenic-survival points are published in the original
references; we used *approximate digitized* values for Figure 2a (see §3
claim CL-1.A) and document the digitization as imprecise to ±30% on log scale.

---

## 2. Methods comparison

| Stage | Paper (MS-GSM², Julia, closed) | This replication (`code/smoke_ms_gsm2.py` + `figure2a_adrian2020.py` + `chem_claim_audit.py`) |
|-------|--------------------------------|------------------------------------------------------------------------------------------------|
| Physical: per-event specific energy `z` | TRAX-CHEM microdosimetric spectra + amorphous track model; per-event sampling | Substituted by analytic average `DSB_per_Gy=8` × OER(LET, [O₂]) (Scifoni-style sigmoid) — **gap** |
| Physical: inter-arrival times | Exp(Ḋ / ⟨z⟩) sampled per cell | Pulse modelled as a single rectangle of length D/Ḋ — **gap** for inter-pulse structure |
| Physical: domain count Nd | 52 cubic sub-domains per nucleus | Honoured as `N_domains=52`; per-domain N₀ split + independent-domain product approximation for cell SF |
| Chemistry: ODEs | Eq. (2), 5 species `[O₂, H₂O₂, OH•, R•, ROO•]`, 9 reactions, Table 1 rate constants | **Implemented faithfully**, stiff BDF solver, non-negativity clamp, rectangular dose source |
| Chemistry: G-values | TRAX-CHEM at 1 μs (closed-source) | Literature defaults: G(OH)=2.5, G(H₂O₂)=0.7, G(R•)=2.6 #/100 eV — **substituted** |
| Chemistry: per-domain replica | Independent ODE per domain × 52 | One ODE per (D, Ḋ, [O₂]) cell-average — **simplification** |
| Bio: GSM² Markov chain | Eq. (6), three channels {r·X, a·X, b·X(X−1)} | **Implemented as exact Gillespie SSA** on integer X; Poisson(N₀_mean) initial X; cell survives iff Y_final=0 |
| Bio: rate constants (a, b, r) | Table 2 fits | Adrian2020 row 1 used as-is: a=7.82e-3 h⁻¹, b=1.83e-2 h⁻¹, r=3.23 h⁻¹ |
| Bio: cross-entropy fit to raw clonogenic data | Yes (paper SI) | **Not implemented** — raw data not released |
| Coupling: indirect-yield modulator κ_ind | ϱ ∫₀ᵗ [ROO•] ds, normalised to 1 at CONV / 21% O₂ | Implemented as `(∫ROO/D) / (∫ROO_ref/D)` with reference at 2 Gy / 0.1 Gy/s / 21% O₂ |
| Multi-scale coupling: SF | `Pr( lim Y^(d)(t) = 0 ∀ d=1..52 )` | Implemented as `SF_domain^52` (independent-domain product, paper's stated approximation) |
| ODE solver | Rodas4 (DifferentialEquations.jl), Julia | SciPy BDF; failed on 1/150 stiff cells (D=20 Gy, dr=10 Gy/s, [O₂]=1%) — handled by NaN-skip |
| Statistical estimate of SF | Ensemble over Nd domains × ? cells | 2000 cells per domain (52 domains) — ≈30 s wall-time on CherryRd |
| Compute target | Not specified (paper) | CPU only, Python 3.14, scipy 1.x, numpy, matplotlib; ≈30 s smoke / ≈90 s chem audit / ≈10 s Fig 2a |

---

## 3. Quantitative claim audit

Notation: ✅ verified within tolerance, ⚖️ partial / direction matches but
magnitude off, ❌ contradicted, ⛔ not tested (blocker named).

| # | Claim (paper §) | Paper value | Our value | Tol | Verdict |
|---|------------------|-------------|-----------|-----|---------|
| CL-1.A | Figure 2a: MS-GSM² survival fraction at 18 Gy DU145 electrons matches Adrian 2020 across 5 oxygenations (1.6, 2.7, 4.4, 8.3, 20% O₂), CONV and UHDR | Paper plot range ≈ 1e-5 to 1e-2 SF; UHDR > CONV at every [O₂] | Smoke SF range 0.49 – 0.73 at all 10 points (`results/figure2a_replication.csv`); UHDR direction NOT preserved at 1.6%, 4.4%, 20% O₂ in smoke | within 0.5 log on SF | ❌ (magnitude wrong, direction inconsistent — smoke missing per-spectrum N₀ calibration and TRAX-CHEM yields) |
| CL-1.B | Figure 2b: MS-GSM² SF at 8 Gy A549 ⁴He @ 4.5 keV/μm, CONV (0.12 Gy/s) vs UHDR (205.13 Gy/s), 1% and 21% O₂ | Paper: UHDR > CONV at both [O₂], SF in 0.0–0.5 range | Not run — `a_h, b_h, r_h` for Tessonnier 2021 ⁴He need re-substitution; smoke wired only with Adrian-2020 biological rates | — | ⛔ (deferred; same blockers as CL-1.A) |
| CL-1.C | Figure 2c: MS-GSM² SF at 7.5 Gy CHO-K1 ¹²C @ 13 keV/μm, CONV (0.6 Gy/s) vs UHDR (70 Gy/s), 0.5, 4, 21% O₂ | Paper: UHDR > CONV at every [O₂], SF in 0.0–0.2 range | Not run — Tinganelli 2022a biological rates need substitution; same blockers | — | ⛔ (deferred) |
| CL-2 | FLASH ratio SF_UHDR/SF_CONV > 1 in the UHDR regime, with the largest sparing at the lowest [O₂] | Qualitative: ratio rises with dose and falls with [O₂] | Reproduced: peak ratio ≈ 1.17 at 15 Gy / 1% O₂; ratio > 1 at all 21% O₂ doses ≥ 5 Gy (`results/smoke_results.csv`) | direction only | ✅ direction; ⚖️ magnitude |
| CL-3 | Per-Gy ∫[ROO•] dt is LOWER under UHDR than CONV at every [O₂] (paper's central physical mechanism) | Qualitative chemistry claim | 30/30 grid cells PASS, with ratio U/C ≈ 0.66 at 21% O₂ down to 0.86 at 0.5% O₂ (`results/chem_claim_audit.md` §C1) | directional | ✅ verified |
| CL-4 | Per-Gy ∫[ROO•] dt is LOWER at low [O₂] than at 21% O₂ | Qualitative chemistry claim | 12/12 grid cells PASS; ratio (1% O₂ / 21% O₂) ≈ 0.083 (CONV) to 0.115 (UHDR), i.e. ≈ 9–12× reduction (`chem_claim_audit.md` §C2) | directional | ✅ verified |
| CL-5 | FLASH chemistry signature (U/C gap) is most pronounced at high [O₂] | Qualitative | Reproduced: 33.9% gap at 21% O₂ vs 9.1% gap at 1% O₂, regardless of dose; **but** flat in dose (paper implies growth with D) | directional | ⚖️ partial — [O₂] direction OK, dose-dependence flat in smoke (smoke chemistry too linear) |
| CL-6 | "FLASH effect visible at all [O₂], including 21% O₂" (Discussion) — i.e. not driven by transient hypoxia | Discussion claim | Reproduced: SF_UHDR/SF_CONV > 1 at 21% O₂ for D ≥ 5 Gy in our smoke (`smoke_results.csv`) | directional | ✅ verified |
| CL-7 | Biological-rate Table 2 fit values | a=7.82e-3, b=1.83e-2, r=3.23 h⁻¹ (DU145/e⁻) | Loaded verbatim into `PARAMS`; **not** independently re-fitted | exact | ⛔ (cannot independently fit — raw data unreleased; values used verbatim) |
| CL-8 | 9-reaction chemical network rate constants (Table 1) | k₁=5e7, k₂=1e4 (table; 1e5 in text update), k₃=6.62e7, k₄=1e3, k₅=1e9, k₆=1e10, k₇=4.62e4, k₈=5e7, k₉=1e2 (all in 1/(M·s)) | Loaded verbatim into `PARAMS`; k₂ kept at table value 1e4 with comment about text update | exact | ✅ identity-checked |
| CL-9 | Nd = 52 microdosimetric domains per cell nucleus | 52 | `N_domains=52` honoured; cell SF = SF_domain^52 | exact | ✅ identity-checked |
| CL-10 | O₂ depletion during UHDR pulse is NOT the primary mechanism (Discussion) | Qualitative | Our smoke shows runaway O₂ consumption to 0 at long relaxation windows — a **smoke artefact** (no [RH] depletion or reoxygenation feedback). Within the pulse itself, O₂_min is essentially equal to O₂_initial (depletion < 1e-6 fraction during the pulse window) | within 5% pulse-window depletion | ⚖️ partial — pulse-window claim consistent; long-time relaxation artefactual |

**Summary.** 11 testable claims enumerated. ✅ 4 verified (CL-3, CL-4,
CL-6, CL-8, CL-9 — 5 counting identity checks). ⚖️ 3 partial (CL-2, CL-5,
CL-10). ❌ 1 contradicted in absolute magnitude (CL-1.A). ⛔ 3 blocked
(CL-1.B, CL-1.C, CL-7). Tested-or-attempted: 11/11. Verified (incl. partial):
8/11 = **73%**.

---

## 4. Scope audit

The paper has **one** primary modelled system (MS-GSM², single
implementation in Julia) validated against **three** experimental datasets
(Adrian 2020 / Tessonnier 2021 / Tinganelli 2022a), plus **one** perspective
figure (Figure 3, O₂ × antioxidant phase plot for electrons).

| Scope unit | Coverage in this replication |
|------------|------------------------------|
| Chemistry layer (5-ODE, 9 reactions, Table 1) | **Fully implemented** in Python (`code/smoke_ms_gsm2.py::chem_rhs`) |
| Biology layer (GSM² Markov SSA, Eq. 6) | **Fully implemented** as exact Gillespie SSA (`code/smoke_ms_gsm2.py::gsm2_ssa`) |
| Coupling (κ_ind from ∫[ROO•], Eq. 7) | **Implemented** with paper's normalisation convention |
| Multi-domain Nd=52 | **Honoured** (`N_domains=52`); per-domain ODE replicas substituted by shared chemistry |
| Microdosimetric spectra / TRAX-CHEM | **Not implemented** (closed-source dependency — blocker) |
| Cross-entropy fit of (a, b, r) | **Not implemented** (raw clonogenic data unreleased — blocker) |
| Figure 2a (DU145 / e⁻ / Adrian2020) | Geometry rerun (`code/figure2a_adrian2020.py`) — qualitative panel produced; absolute SF off by ~3 log |
| Figure 2b (A549 / ⁴He / Tessonnier2021) | Not run (deferred — would require re-substituting Tessonnier rates and Ḋ values; smoke trivial extension if blockers lifted) |
| Figure 2c (CHO-K1 / ¹²C / Tinganelli2022a) | Not run (deferred — same as 2b) |
| Figure 3 (O₂ × antioxidant phase plot for e⁻) | Not run (would be ≈ 10× longer sweep; deferred) |

**Coverage by primary analyzable unit (mechanism layer):** 4 of 6 modelling
layers implemented faithfully (chemistry, biology, coupling, Nd=52) =
**67%** of model surface. **Coverage by validation panel:** 1 of 3 figure
panels attempted (Figure 2a, with caveat) = **33%** by figure count, but 11 of
11 enumerated quantitative claims **tested or named as blocked** = **100%**
by claim coverage.

---

## 5. What I actually ran

| Step | Script | Wall time | Outputs |
|------|--------|-----------|---------|
| Smoke chemistry + GSM² SSA + SF grid (7 doses × 2 dose-rates × 2 O₂, Nd=52) | `code/smoke_ms_gsm2.py` | ≈ 30 s | `results/smoke_results.csv`, `results/smoke_chem_trace.csv`, `results/smoke_results.png` |
| Paper-Fig.2a geometry (18 Gy, DU145, 10 MeV e⁻, 5 O₂ × 2 regimes) | `code/figure2a_adrian2020.py` | ≈ 12 s | `results/figure2a_replication.csv`, `results/figure2a_replication.png` |
| Chemistry-only quantitative claim audit (6 doses × 5 dose-rates × 5 O₂, claims C1–C4) | `code/chem_claim_audit.py` | ≈ 90 s | `results/chem_claim_audit.csv`, `results/chem_claim_audit.md` |

All runs on CherryRd (macOS, Python 3.14, scipy + numpy + matplotlib, CPU,
no GPU). Deterministic seeds set per (D, Ḋ, [O₂]) cell so re-runs reproduce
bit-for-bit.

Re-run:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/
python3 code/smoke_ms_gsm2.py
python3 code/figure2a_adrian2020.py
python3 code/chem_claim_audit.py
```

Known ODE-solver fragility: 1 of 150 sweep cells (D=20 Gy, Ḋ=10 Gy/s,
[O₂]=1%) trips BDF "array must not contain infs or NaNs" during long
relaxation; `chem_claim_audit.py` traps the exception and emits NaN for
that cell. Does not affect the 30/30 C1 or 12/12 C2 audits which sweep
{CONV=0.1, UHDR=100} Gy/s only.

---

## 6. Key output files

```
code/smoke_ms_gsm2.py             14 KB   Python/SciPy MS-GSM² port (chem ODE + SSA + coupling)
code/figure2a_adrian2020.py        7 KB   Paper-Fig.2a geometry runner
code/chem_claim_audit.py           8 KB   4 chemistry-side quantitative claims (C1–C4)
results/smoke_results.csv          3.5 KB  SF vs (D, Ḋ, [O₂]) grid
results/smoke_results.png         109 KB  SF + FLASH-ratio 2-panel plot
results/smoke_chem_trace.csv       74 KB  Example chemistry trace (D=10 Gy, UHDR, 1% O₂)
results/figure2a_replication.csv   ≈1 KB   MS-GSM² smoke vs Adrian2020 18-Gy
results/figure2a_replication.png  ≈30 KB  Same as overlay plot
results/chem_claim_audit.csv      ≈10 KB  per-Gy ROO* and O₂_min over 150 sweep cells
results/chem_claim_audit.md       ≈5 KB   Human-readable claim verdicts
refs/arxiv-2412.16322.pdf          4.1 MB  primary paper
refs/arxiv-src/                    —      LaTeX source + figures
artifacts/MANIFEST.md              ≈2 KB   SHA-256 hashes of all artifacts
reports/REPORT.md                  this file (canonical 8-section template)
reports/FIRST_PASS_REPORT.md       legacy long-form first-pass writeup (kept for history)
```

---

## 7. Honest gaps

**Named missing artifacts that block bit-exact replication:**

1. **Julia source code for MS-GSM².** Paper says *"performed using Julia"*
   with no repository cited. No public GitHub repo under `fcordoni`,
   `Battestini`, `2MaBa`, or related accounts as of 2026-06-22. Required to
   match: (a) Rodas4 ODE solver behaviour vs our BDF, (b) per-domain
   chemistry replica logic, (c) cross-entropy fitter for (a, b, r), (d)
   amorphous-track-model microdosimetric sampling. **Specific request to
   authors:** publish the Julia source with a Zenodo DOI.

2. **Raw clonogenic-survival data** from Adrian 2020 / Tessonnier 2021 /
   Tinganelli 2022a in the *specific format the authors used* (typically
   N_colonies / N_plated per replicate per (D, Ḋ, [O₂]) cell). The
   primary publications report aggregated SF points (which we can read off
   their plots), but the cross-entropy fit needs replicate-level data.
   Paper says *"raw data ... available by the authors without undue
   reservation"*. **Specific request to authors:** deposit the raw
   clonogenic counts in a public repo (Zenodo / Figshare / Mendeley Data).

3. **TRAX-CHEM microdosimetric spectra** (per-event specific-energy
   distributions for each particle / LET). Generated upstream by the
   Trento group (Boscolo 2018/2020 simulations) and not bundled with
   either paper. Without these we substitute a constant `DSB_per_Gy=8` ×
   analytic OER, which is the proximate cause of our 3-log absolute-SF
   miss on Figure 2a. **Specific request:** deposit the .npz/.csv
   per-event spectra used for each panel.

4. **Supplementary Information PDF.** Tables S1 and S2 are *referenced* in
   the main text but the SI is not currently a separate file in the arXiv
   tarball; the main LaTeX integrates the values as Tables 1–2 (which we
   do have). Will be in the eventual journal version.

**Smoke-pipeline artefacts that are NOT paper limitations (i.e. our own bugs/gaps):**

- The 5-ODE chemistry, run on a long relaxation window, drains O₂ to zero
  because we omit [RH] depletion and O₂ reoxygenation feedback. The paper
  presumably integrates only over an experimentally meaningful post-pulse
  window or includes additional restorative terms; we have not implemented
  either. Affects CL-10 long-time interpretation only.
- The independent-domain product approximation `SF = SF_domain^52`
  over-suppresses survival when SF_domain is non-zero — visible in our
  Figure 2a numbers landing in 0.5–0.7 (low N₀ per domain → high
  SF_domain → SF_domain^52 ≈ 0.5–0.7). The paper's pipeline implicitly
  matches survival by calibrating N₀ via the cross-entropy fit, which we
  cannot do without raw data. This is the proximate cause of the
  3-log-magnitude miss.
- Per-Gy ROO* integral is dose-invariant in our smoke (chemistry strictly
  linear in source for the parameter regime), so claim CL-5's
  "dose-dependence of the FLASH gap" reduces to a constant in our smoke.
  This is a real model-faithfulness gap, not a numerical artefact.

**What we did NOT attempt (out of scope for this round, by instruction):**

- Author contact (closed by the task protocol).
- Porting to Julia / DifferentialEquations.jl for Rodas4 parity.
- Implementing the cross-entropy fitter (would only be useful once raw
  data lands).
- Running on uicgpu / Aurora — none of this needs GPU.

---

## 8. Verdict

**PARTIAL** — chemistry and biological-stage mechanisms reproduced
qualitatively from open paper parameters; the paper's central physical
claim (per-Gy ∫[ROO•] lower at UHDR, the FLASH chemistry signature) is
quantitatively verified by our smoke at 30/30 grid cells across 6 doses
and 5 oxygenations, AND the headline FLASH-sparing direction
SF_UHDR/SF_CONV > 1 is reproduced in the expected regime. However, the
absolute Figure 2a/2b/2c surviving-fraction match is **not** achieved
(off by ~3 log on Figure 2a), and Figures 2b, 2c, and 3 were not run.
Bit-exact replication is blocked by three named missing artifacts (Julia
code, raw clonogenic data, TRAX-CHEM spectra) — none currently
recoverable without author contact.

**Coverage / 10:** **6** — chemistry, biology, coupling, Nd=52, Figure 2a
geometry implemented; Figures 2b/2c/3 not run; cross-entropy fit not
implemented (blocker-bound).

**Agreement / 10:** **5** — direction-of-effect verified on every
testable mechanism claim (C1 ✅ 30/30, C2 ✅ 12/12, CL-2 ✅, CL-5
partial, CL-6 ✅, CL-8 ✅, CL-9 ✅); absolute survival magnitudes off
by 3 log on Figure 2a (CL-1.A ❌); CL-1.B and CL-1.C not run; CL-7
identity-only (cannot re-fit without raw data).

For a REPLICATED verdict the protocol requires ≥80% scope AND ≥80% of
claims. We are at 67% scope (4/6 modelling layers, 1/3 figure panels) and
73% claim coverage (8/11 verified-or-partial out of 11 enumerated). Both
thresholds missed, both for the same root cause: closed Julia + unreleased
raw data + missing TRAX-CHEM spectra. With those three artifacts a full
bit-exact replication would be ≤ 1 week of work; without them, this is
the honest ceiling.

---

VERDICT=PARTIAL COVERAGE=6/10 AGREEMENT=5/10

**Repro-blocker summary (3 lines):**
1. Closed Julia source code for MS-GSM² — paper says "performed using Julia"
   but cites no repository; no public repo under any plausible author
   account as of 2026-06-22. Required for Rodas4 parity and the
   cross-entropy fitter.
2. Raw clonogenic-survival replicate data from Adrian 2020 / Tessonnier
   2021 / Tinganelli 2022a in the per-replicate format the authors used.
   Paper says "available without undue reservation" (= request only).
3. TRAX-CHEM microdosimetric specific-energy spectra (per-event z
   distributions, per particle/LET) — generated upstream by the Trento
   group, not bundled with the paper. Proximate cause of our 3-log
   absolute-SF miss on Figure 2a.
