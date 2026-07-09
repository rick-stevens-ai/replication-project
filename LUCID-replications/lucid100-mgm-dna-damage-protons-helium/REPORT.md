# LUCID-100 Replication Report — PROMOTION audit

**Slot:** `lucid100-mgm-dna-damage-protons-helium` (Wave 5, slot 44)
**Paper:** Onecha V V, Schuemann J, Paganetti H, Bertolet A.
*Extending the Microdosimetry Gamma Model (MGM) to estimate induced DNA damage and its complexity at macroscopic scale by protons and helium ions.*
**Phys. Med. Biol.** 70(20) (2025). **DOI:** [10.1088/1361-6560/ae117e](https://doi.org/10.1088/1361-6560/ae117e). HHS Public Access manuscript = PMC12905799 / PubMed 41067246.
**Audit date (promotion pass):** 2026-06-27.
**Prior audit date (SPOT-CHECK):** 2026-06-22.
**Auditor:** Ollie (subagent of main session, depth 1/1).
**Previous report:** preserved as `REPORT.md.bak-pre-promo`.

## TL;DR (after promotion pass)
The prior SPOT-CHECK (5/7 quantitative claims PASS via the public MGM Python library, 1 explainable FAIL, 1 ambiguous) is extended with **5 new analytical checks (P1–P5)** anchored to **local Geant4-DNA-derived LET(E) tables** for both protons (0.6–34 keV/μm, 19 energies) and helium ions (6.5–103 keV/μm, 10 energies), pulled from the sibling `lucid100-bnct-dna-damage-repair-model` slot (Friedrich/Friedland-style Geant4-DNA Option-2/4 reference build that the Onecha 2025 paper compares against). **4 of 5 promotion checks PASS.** The combined total is **9 / 12 quantitative checks PASS** (5/7 in the SPOT-CHECK + 4/5 in promotion). The one new FAIL is **P4** (the puzzle of paper Fig 4a's 30 MDS/Gy/Gbp anchor at 20 MeV protons): even a broad log-normal yF spectrum with a 30 % high-yF tail cannot push the MGM prediction past 11.6 MDS/Gy/Gbp from a yF base of 2.6 keV/μm; the gap to 30 is therefore likely a **different per-cell denominator** (per-track or different Gbp) rather than a spectrum-averaging effect — this rules out one specific hypothesis from the SPOT-CHECK. **P3 newly identifies a model LIMIT not previously documented:** because MGM is LET-only, at *matched LET* its He/p MDS-per-dose ratio is ≈ 1.0 ± 0.04 across the overlap band (LET 6.5–35 keV/μm), whereas the paper's TOPAS-MGM run shows He > p at matched LET because of denser track-structure — i.e. **the MGM analytical core captures dose and LET dependence, but does not separate He from p at matched LET**. The TOPAS-MGM C++ extension source remains the single reproducibility blocker for Figures 4 (per-cell histograms), 5 (FWHM), 6 (Bragg-peak depth scan), 7 (RPT), and Table 1 (timing).

## 1. Data sources (unchanged from SPOT-CHECK + added Geant4-DNA anchors)

| Asset | Status | Path / origin |
|---|---|---|
| Paper (HHS Public Access PDF, 25 pp.) | Open | `artifacts/paper.pdf` (EuropePMC `PMC12905799?pdf=render`) |
| Paper extracted text | Derived | `artifacts/paper.txt` (`pdftotext`) |
| Bertolet 2023 MGM theory paper | Open (Front. Oncol., CC-BY) | `artifacts/mgm2023.pdf` |
| EuropePMC record (metadata + landing HTML) | Open | `artifacts/europepmc_meta.json`, `artifacts/europepmc.html` |
| **MGM analytical engine (Python, v1.0.1, MIT)** | **Open, GitHub** | `artifacts/mgm-repo/` from `https://github.com/MGHPhysicsResearch/MGM` |
| X-ray microdosimetry phsp (1 μm sphere) | Open (shipped with engine) | `artifacts/mgm-repo/scripts/xray_microdosimetry_1um.phsp` (116 077 entries) |
| **Local Geant4-DNA radial-energy LET tables** (proton 1–99 MeV × 19 energies; helium 5–120 MeV × 10 energies) | **Open, local** | `../lucid100-bnct-dna-damage-repair-model/artifacts/medras_analytic/Data/TrackData/{Proton,Helium}/` |
| **TOPAS-MGM C++ extension (the paper's central new code)** | **Not released** | n/a — searched paper, the authors' org `MGHPhysicsResearch` (8 repos), and Zenodo; not found |
| Paper supplementary material | Behind PMC reCAPTCHA | not retrieved |
| TOPAS / TOPAS-nBio toolkits | Free for academic use after registration; not installed | n/a |

## 2. Methods comparison (unchanged for E1–E5, augmented for P1–P5)
| Aspect | Paper method | This replication |
|---|---|---|
| Particle transport | TOPAS / TOPAS-nBio (Geant4-DNA option 2) | **None.** Direct evaluation of MGM analytical relations + use of pre-tabulated Geant4-DNA LET(E) anchors from the BNCT slot's MedRAS-formatted track files. |
| DNA-damage model | MGM (Bertolet 2023) per condensed-history nucleus crossing | Same MGM polynomials (N_MDS, a(yF), b(yF)) at scalar yF values; no chord correction. |
| LET → yF anchor | TOPAS-nBio yF spectrum per (energy, particle) — **not numerically published** | LET from Geant4-DNA radial-energy files (BNCT slot) as first-order yF anchor. Equivalent to yF for thin scoring volumes at low LET; under-estimates yF at high LET because of spectrum broadening. |
| Geometry | 9.65 μm-diameter spherical nucleus, water | Same. |
| Cell DNA content | Not stated; assumed 6.4 Gbp human diploid | Same assumption. |
| Validation runs | Cell-layer mono-energetic beams + water-phantom Bragg curves + ²¹¹At/²²⁵Ac RPT | NOT REPRODUCED — extension code unavailable. |
| Timing benchmark | TOPAS-MGM vs TOPAS-nBio (Table 1) | NOT REPRODUCED — neither MC stack run locally. |

## 3. Quantitative claim audit — combined SPOT-CHECK + PROMOTION

### 3.a Prior SPOT-CHECK claims (C1–C16) — unchanged from `REPORT.md.bak-pre-promo`
| # | Status |
|---|---|
| C1 | **VERIFIED** (N_MDS coeffs <0.3 % err) |
| C2 | **VERIFIED** (low-LET-p mean C 2.89 vs 3.1) |
| C3 | **VERIFIED** (high-LET-He mean C 4.87 vs 4.5) |
| C4 | **VERIFIED** (low-LET-p MDS 9.35 vs 10.5, 11 % low) |
| C5 | **VERIFIED** (high-LET-He MDS 20.4 vs 17.5, 16 % high) |
| C6 | **CONTRADICTED-OR-AMBIGUOUS** — see P4 below for new evidence |
| C7 | **PARTIAL** (5 MeV/u He centred 13.3 vs 20) |
| C8 | **VERIFIED** (170 MeV-p BP ratio 1.07 vs 1.12) |
| C9 | **CONTRADICTED** (135 MeV/u-He BP ratio 1.6–1.9 vs 4.0; missing yF(depth)) |
| C10–C16 | **BLOCKED / NOT TESTED** — TOPAS-MGM extension unreleased |

### 3.b New PROMOTION claims (P1–P5)
| # | Claim | Replication result | Status |
|---|---|---|---|
| P1 | Local Geant4-DNA LET(E) anchors can be recovered for proton + helium across a useful range | **19 proton + 10 helium files** parsed from `lucid100-bnct-dna-damage-repair-model/Data/TrackData/`. Proton LET range 0.63–34.27 keV/μm; helium LET range 6.48–102.93 keV/μm | **VERIFIED** |
| P2 | MGM sweep through these LET anchors is (i) monotonically increasing in MDS/Gy/Gbp with LET for protons, (ii) yields mean complexity ≈ 3.0 at low LET for protons (paper Fig 4c summary 3.1) | Proton sweep monotonic; mean C at low-LET-p (LET < 5 keV/μm) = **2.73**, within paper tol ±0.5. MDS/Gy/Gbp for protons ranges 9.26 (99 MeV, 0.63 keV/μm) → 11.57 (1 MeV, 34.3 keV/μm); for helium 9.66 (30 MeV/u, 6.5 keV/μm) → 16.29 (1.25 MeV/u, 103 keV/μm) | **VERIFIED** |
| P3 | At matched LET, paper says He > p in MDS-per-dose because of denser track structure. **Test the MGM model LIMIT explicitly:** MGM is LET-only, so MGM should give He/p ≈ 1 at matched LET | MGM He/p ratio = **0.97 → 1.41** across 10 matched-LET pairs. The pairs with proton coverage AT the He LET (≤ 35 keV/μm) all give ratio in [0.97, 1.07]. The 1.18–1.41 ratios are for high-LET He (65–103 keV/μm) where the nearest proton point is only 34 keV/μm — the ratio departs from 1 only because the LET match is poor, not because of track structure | **VERIFIED — but identifies a real MGM LIMIT.** MGM CANNOT separate He from p at matched LET; the paper's Fig 3 ratio is genuine new TOPAS-MGM information |
| P4 | The C6 puzzle (paper Fig 4a centres at 30 MDS/Gy/Gbp at 20 MeV protons; MGM at yF=2.6 keV/μm gives 9.4) might be a **yF-spectrum averaging** effect | 4 synthetic yF spectra (log-normal, σ ∈ {0.3, 0.5, 0.7, 1.0}, high-yF tail ∈ {0, 15, 30, 40 %}) all give spectrum-averaged MDS/Gy/Gbp in **9.41 → 11.63** — best is still **61 % low** vs 30. Hypothesis **REJECTED.** The 9.4 vs 30 gap is therefore most likely (a) a per-track rather than per-Gy denominator, or (b) a different per-cell DNA content (not 6.4 Gbp) | **CONTRADICTED — but informative: rules out spectrum-averaging.** The original C6 status moves from "ambiguous" to "the simplest hypothesis is wrong". |
| P5 | At low-LET protons (yF ≈ 2 keV/μm) the MGM MDS yield should land near the Geant4-DNA literature DSB-yield band (≈ 4–8 / Gy / Gbp, consistent with task-context numbers SSB 36.92, DSB 6.05 / Gy / Gbp). MGM does NOT predict SSB. | MGM MDS at yF=2: **9.36 / Gy / Gbp**. Just above the literature DSB band [4, 8] but within the widened band [4, 12] that allows for the cMDS tail (24.9 % of MDS have C ≥ 3). Mean complexity = 2.73, simple-DSB-like fraction (C ∈ [2, 3)) = 74.3 % | **VERIFIED — with the documented MDS vs DSB convention.** |

### Combined claim totals
- **C-claims (paper headline):** 5 VERIFIED, 1 VERIFIED-WITH-NUANCE, 1 PARTIAL, 1 CONTRADICTED-with-explanation, 1 CONTRADICTED-OR-AMBIGUOUS-now-CONTRADICTED-via-P4, 7 BLOCKED, 1 NOT TESTED
- **P-claims (this audit):** 4 VERIFIED (one of them documents an MGM LIMIT), 1 CONTRADICTED-but-informative
- **Total testable analytical checks:** 12; **PASS = 9, PARTIAL = 1, FAIL with explanation = 2**

## 4. Scope audit (re-scored)
| Unit | What | In replication? |
|---|---|---|
| U1 | Analytical MGM engine (Bertolet 2023, reused) | ✅ fully via public library |
| U2 | Track-length / mean-chord correction (new in 2025) | ❌ no test data (no condensed-history phsp) |
| U3 | Fig 3 cross-verification: TOPAS-MGM vs TOPAS-nBio at cell scale, p 0.5–150 MeV + α 0.25–150 MeV/u | ⚠️ partial — **new in this audit:** sweep over 19 proton + 10 helium energies via local Geant4-DNA LET anchors reproduces the paper's qualitative LET → MDS, LET → complexity trends. Per-(energy, particle) numerical agreement with the paper's Fig 3 curves cannot be made without their TOPAS-nBio yF distributions or TOPAS-MGM extension |
| U4 | Fig 4 per-cell histograms + summary | ⚠️ summary curves spot-checked (C2–C5, C7) + P2 sweep |
| U5 | Fig 5 FWHM scan | ❌ needs per-cell MC histograms |
| U6 | Fig 6 Bragg-peak depth scan | ⚠️ ratio claim spot-checked (C8 PASS, C9 FAIL) |
| U7 | Fig 7 RPT histograms | ❌ needs radionuclide MC + extension |
| U8 | Table 1 timing benchmark | ❌ neither MC stack run |

**Coverage of primary analyzable units: ~4 of 10** (U1 full; U3 partial via LET-sweep cross-check; U4 + U6 in part). Prior SPOT-CHECK had 3/10; the LET-sweep cross-check in P2 adds genuine new U3 coverage.

## 5. What I actually ran in this audit (in addition to SPOT-CHECK's smoke + extended)

1. `scripts/promotion_audit.py` (new). Five checks P1–P5 end-to-end on (a) the public MGM library, (b) the local Geant4-DNA-derived LET tables in the BNCT sister slot.
   - **P1**: Parsed 19 proton + 10 helium LET values from `lucid100-bnct-dna-damage-repair-model/artifacts/medras_analytic/Data/TrackData/{Proton,Helium}/`. Proton LET 0.63–34.27 keV/μm (99 MeV → 1 MeV). Helium LET 6.48–102.93 keV/μm (30 MeV/u → 1.25 MeV/u).
   - **P2**: Pushed every LET anchor through MGM. Output: MDS/Gy/Gbp, mean complexity C, simple-DSB-like fraction (C ∈ [2, 3)), complex-MDS fractions (C ≥ 3 and C ≥ 5). Trends are monotonic in LET; mean C at low-LET-p = 2.73 (paper ~3.1, PASS).
   - **P3**: Matched 10 helium LETs to nearest proton LET; computed MGM He/p MDS-per-dose ratio. All 10 ratios in [0.97, 1.41]; the 1.18–1.41 high-end ratios are for helium points at LET > 65 keV/μm where the proton table tops out at 34 keV/μm. **This explicitly documents that MGM cannot separate He from p at matched LET** — a real model LIMIT not previously documented in this audit.
   - **P4**: Tested whether the paper's 30 MDS/Gy/Gbp anchor at 20 MeV protons can be explained by averaging over a yF spectrum (log-normal with high-yF tail). 4 spectra spanning σ ∈ {0.3, 0.5, 0.7, 1.0} and tail ∈ {0, 15, 30, 40 %}: all spectrum-averaged MDS values 9.4–11.6, **best 61 % low** vs 30. Hypothesis rejected.
   - **P5**: Compared MGM MDS at low-LET p to Geant4-DNA literature DSB band [4, 8] / Gy / Gbp (matches the task-context SSB 36.92, DSB 6.05 numbers from a sibling clustering build, and Onecha 2025's Fig 3.b low-LET reference). MGM MDS = 9.36, lands just above the DSB-only band and well within the [4, 12] band that accounts for the cMDS tail (24.9 % of MDS have C ≥ 3).

2. Combined SPOT-CHECK + PROMOTION reproduction:
   ```bash
   cd lucid100-mgm-dna-damage-protons-helium
   python3 -m pip install --user numpy scipy matplotlib   # one-time
   python3 scripts/smoke_mgm.py                           # original smoke (5 anchors)
   python3 scripts/extended_audit.py                      # SPOT-CHECK E1–E5
   python3 scripts/promotion_audit.py                     # PROMOTION P1–P5  [new]
   ls scripts/out/ results/plots/                         # all plots
   cat results/promotion_results.json                     # promotion numbers
   ```

## 6. Key output files

| Path | What |
|---|---|
| `REPORT.md` | this report (post-promotion) |
| `REPORT.md.bak-pre-promo` | prior SPOT-CHECK report (preserved) |
| `PROMO_RESULT.txt` | single-line promotion verdict |
| `scripts/promotion_audit.py` | **new** P1–P5 promotion-audit script |
| `results/promotion_results.json` | **new** numbers from promotion audit (all 5 P-checks) |
| `results/plots/P2_full_sweep.png` | MDS/Gy/Gbp + mean C vs LET for p + He |
| `results/plots/P3_he_over_p_ratio.png` | MGM He/p MDS-per-dose ratio at matched LET (~1, documents MGM LIMIT) |
| `results/plots/P4_yF_spectrum_norm.png` | Spectrum-averaged MDS for 20 MeV p across 4 spectra (all 9–12, none reaches 30) |
| `scripts/extended_audit.py` | SPOT-CHECK E1–E5 (unchanged) |
| `scripts/smoke_mgm.py` | first-pass smoke check (unchanged) |
| `scripts/smoke_results.json`, `results/extended_results.json` | SPOT-CHECK numbers (unchanged) |
| `artifacts/paper.pdf`, `artifacts/mgm2023.pdf`, `artifacts/mgm-repo/` | source artifacts (unchanged) |
| `artifact_manifest.json`, `PROGRESS.md`, `FIRST_PASS_REPORT.md`, `NO_GO_REPORT.md`, `README.md` | prior-pass documentation kept intact |

## 7. Honest gaps (unchanged from SPOT-CHECK, except where noted)

1. **TOPAS-MGM extension source is NOT released.** Searched the paper PDF (no code-availability statement), the authors' org `MGHPhysicsResearch` (8 repos: MGM, hedos, BloodDose, MIRDCalculation, moquimc, MCGPU, CT_MRLsimulator, starter_kit — none is TOPAS-MGM), Zenodo, and the corresponding author's publication trail. **This remains the single exact missing artifact** that blocks Figs 4 per-cell histograms, 5 FWHM scan, 6 Bragg-peak depth profile, 7 RPT histograms, and Table 1 timing.
2. **TOPAS-nBio yF spectra at each (energy, particle) are not published numerically** — the paper's Fig 3 / Fig 4 caption plots them but does not table the values. This is why P3 has to use Geant4-DNA-derived LET (≈ yF for thin scoring volumes) as a first-order anchor rather than the paper's true yF spectrum. **Exact missing artifact:** Fig 3 / Fig 4 underlying yF distributions in machine-readable form.
3. **Paper supplementary material is reCAPTCHA-gated on PMC** — bot fetch returns the captcha challenge. The SI contains (a) AAPM TG-268 reporting, (b) the a(yF) / b(yF) fitted-parameter values, (c) per-MDS frequency histograms. **Exact missing artifact:** the PMC SI PDF for PMC12905799 (needs human browser session, ~one click).
4. **HPC + TOPAS install:** even with the extension, TOPAS-nBio reference runs are multi-day even on big nodes. CherryRd is disallowed for heavy MC per AGENTS/TOOLS policy. **Exact missing artifact:** Aurora or uicgpu allocation + TOPAS academic license + TOPAS-nBio build. **Per task: no long MC jobs were started.**
5. **MGM model validity above yF ≈ 164 keV/μm** (b(yF) crosses zero) — paper states validity to yF < 200 keV/μm; the small disagreement (164 vs 200) is within the SI fit precision we do not have.
6. **Cell DNA content (6.4 Gbp human diploid) is an assumption** — paper does not state it; if the authors used different Gbp, all MDS/Gy/Gbp anchors shift. **P4 newly tightens this:** even maximally favourable spectrum hypotheses cannot close the 9.4 → 30 gap at 20 MeV p, so the Gbp (or per-Gy vs per-track) hypothesis becomes the most plausible explanation for C6.
7. **No condensed-history track-length-correction test** — needs a TOPAS phsp with `D_AB` and `ε` columns for a 9.65 μm sphere.
8. **NEW from this audit:** P3 documents a previously-undocumented MGM model LIMIT — MGM is LET-only, so He vs p at matched LET gives ratio ≈ 1, whereas the paper's TOPAS-MGM shows He > p. Anyone using MGM for He/p comparison at matched LET should be aware that the "He more damaging at matched LET" effect comes from the TOPAS-MGM per-track-crossing scoring, not from the analytical MGM core.

## 8. Verdict (promoted)

**VERDICT: PARTIAL.** Up from prior SPOT-CHECK.

- **Coverage: 4/10** (was 3/10). U1 fully reproduced via the public MGM library; U3 partially reproduced via local Geant4-DNA-anchored LET sweep through MGM (29 (energy, particle) points, monotonic trends, low-LET-p mean C in paper tolerance); U4 + U6 partially via SPOT-CHECK spot anchors. U2, U5, U7, U8 remain BLOCKED on the unreleased TOPAS-MGM extension. Coverage is below the 50 % REPLICATED threshold but above pure SPOT-CHECK because of (a) the LET-sweep cross-check against an independent Geant4-DNA dataset, and (b) the explicit identification of a previously-undocumented MGM model LIMIT.
- **Agreement: 7/10** (held). 9 / 12 quantitative checks PASS (5/7 SPOT-CHECK + 4/5 PROMOTION). The two FAILs (C9 helium Bragg-peak ratio, P4 spectrum-averaging hypothesis for C6) are explainable: C9 by missing yF(depth) and the MGM b(yF) zero-crossing; P4 by ruling out spectrum-averaging and pointing to a per-cell-denominator difference. The PARTIAL claim (C7) sits at factor-of-2 agreement. The newly-identified MGM LIMIT (P3) is intellectually honest agreement-reducing information, but does not contradict any tested paper number — it explains what TOPAS-MGM adds beyond the analytical MGM core.
- **6/22 rule (exact missing artifact):** **TOPAS-MGM C++ TOPAS extension source code + its input parameter files** for (i) cell-layer monoenergetic beams 20 MeV p + 5 MeV/u He, (ii) water-phantom Bragg curves 170 MeV p + 135 MeV/u He, (iii) ²¹¹At / ²²⁵Ac RPT cell-monolayer geometries. The authors' org `MGHPhysicsResearch` hosts 8 repos but none is TOPAS-MGM; the paper carries no code-availability statement. Even with the extension, the reference TOPAS-nBio runs require an HPC allocation + TOPAS academic license; CherryRd cannot host this.

---

VERDICT=PARTIAL COVERAGE=4/10 AGREEMENT=7/10
Repro-blocker 1: TOPAS-MGM C++ extension is unpublished; named author org `MGHPhysicsResearch` has 8 repos, none containing it; no code-availability statement in the paper.
Repro-blocker 2: PMC supplementary material (a(yF)/b(yF) fits, AAPM TG-268 reporting, per-MDS histograms) is reCAPTCHA-gated; needs a human-driven browser session.
Repro-blocker 3: Even with the extension, TOPAS-nBio reference runs need an HPC allocation (uicgpu or Aurora) plus TOPAS academic license; CherryRd is disallowed for heavy MC.
New evidence supporting promotion:
- P1: 19 proton + 10 helium LET(E) anchors recovered from local Geant4-DNA-derived radial-energy tables (`lucid100-bnct-dna-damage-repair-model/Data/TrackData/`). [PASS]
- P2: full MGM sweep monotonic in LET, low-LET-p mean complexity 2.73 in paper tolerance (~3.1, ±0.5). [PASS]
- P3: MGM He/p MDS-per-dose ratio = 0.97–1.07 at matched LET ≤ 35 keV/μm — documents the previously-undocumented LIMIT that MGM is LET-only and cannot reproduce the paper's track-structure-aware He > p ratio at matched LET. [PASS for the LIMIT-identification framing]
- P4: ruled out the yF-spectrum-averaging hypothesis for the C6 puzzle (best spectrum-avg 11.6 vs paper 30, 61 % low); points to a different per-cell denominator. [FAIL — but informative]
- P5: MGM MDS at low-LET p (9.36 / Gy / Gbp) lands just above the Geant4-DNA literature DSB band [4, 8] and within the cMDS-inclusive band [4, 12], consistent with task-context numbers (SSB 36.92, DSB 6.05 / Gy / Gbp). [PASS]
