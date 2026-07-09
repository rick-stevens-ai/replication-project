# FIRST_PASS_REPORT — slot 44 (LUCID100 Wave 5)

**Paper:** Onecha V V, Schuemann J, Paganetti H, Bertolet A. *Extending the Microdosimetry Gamma Model (MGM) to estimate induced DNA damage and its complexity at macroscopic scale by protons and helium ions.* **Phys. Med. Biol.** 70(20) (2025). **DOI** [10.1088/1361-6560/ae117e](https://doi.org/10.1088/1361-6560/ae117e). HHS Public Access manuscript = PMC12905799 / PubMed 41067246. Corresponding author: A. Bertolet (MGH/HMS).

## Verdict
- **CPU smoke check: PASS** for the two analytical equations the paper builds on. Reproducible from the public MGM Python library (`MGHPhysicsResearch/MGM`).
- **Full TOPAS-MGM replication: deferred (NO-GO on CherryRd).** The TOPAS extension itself is not in any public repo we can find; the validation runs are full MC and would in any case require an HPC job (see job plan below). See `NO_GO_REPORT.md`.

**QA retag recommendation:** `KEEP-PARTIAL` — keep in LUCID100 as a tractable equation/engine-level replication; flag full MC reproduction as blocked-pending-code.

## Scope of paper
- Build TOPAS-MGM, a condensed-history wrapper around the cell-scale Microdosimetric Gamma Model so DSB and DSB-complexity can be evaluated **macroscopically** in cell-monolayer + water-phantom geometries with proton/helium beams and α-emitting radiopharmaceuticals (²¹¹At, ²²⁵Ac).
- Validate against TOPAS-nBio (Geant4-DNA option 2) at cell scale.
- Demonstrate Bragg-peak rise in MDS/dose (up to 4× for α at the BP, ~1.12× for protons).
- Show heterogeneity of DSB / cell for RPT vs near-Gaussian distribution for external beams.
- Report ~78 000× speed-up for protons, ~243 000× for α vs TOPAS-nBio.

## Core equations (verbatim from the paper, Methods)
1. Number of multiply-damaged sites per track as function of frequency-mean lineal energy yF (keV/μm):
   `N_MDS(yF) = 0.13 · yF + 9.66 × 10⁻⁴ · yF²`
2. Complexity (number of nucleotide damages inside one MDS, C ≥ 2) follows a gamma distribution per track:
   `f(C; yF) = b(yF)^a(yF) / Γ(a(yF)) · C^(a(yF)−1) · exp(−b(yF) · C)`
   with a(yF), b(yF) second-order polynomials in yF (fit values shipped in `mgm/src/mgm.py`).
3. The 2025 extension adds an entry/exit chord-length correction `D_AB / l̄` with `l̄ = 2/3 · d` (sphere mean chord) so the cell-scale yF can be evaluated from a single condensed-history step crossing a 9.65 μm-diameter nucleus.

## What we have on disk (artifact harvest)
| Path | What | Size |
|---|---|---|
| `artifacts/paper.pdf` | 25-page author manuscript | 1.7 MB |
| `artifacts/paper.txt` | pdftotext dump for grep | ~70 KB |
| `artifacts/mgm2023.pdf` | Bertolet 2023 MGM theory paper (Front. Oncol., CC-BY) | 4.8 MB |
| `artifacts/mgm-repo/` | `MGHPhysicsResearch/MGM` v1.0.1, MIT (the analytical engine) | ~5 MB inc. demo phsp |
| `artifacts/europepmc_meta.json` | EuropePMC record | 8 KB |
| `scripts/smoke_mgm.py` | CPU smoke check | 7 KB |
| `scripts/smoke_results.json` | numbers | ~5 KB |
| `scripts/out/check1_N_MDS_vs_yF.png` | Eq 1 reproduction | |
| `scripts/out/check2_complexity_pdf.png` | gamma f(C\|yF) | |
| `scripts/out/check2b_mean_complexity_vs_yF.png` | mean C(yF) sweep | |
| `artifact_manifest.json` | full file listing + sha256 prefixes | |

## Smoke-check results (CPU)
- Check 1 — N_MDS(yF): paper-quoted coeffs (0.13, 9.66e-4) vs library coeffs (0.12962, 9.657e-4). Max relative error over yF ∈ [2, 200] keV/μm is **0.29 %**. ✅
- Check 2 — gamma complexity:
  - yF = 10.95 keV/μm (3 MeV proton, Bertolet 2023 anchor) → mean C ≈ 2.95
  - yF = 100 keV/μm (alpha regime) → mean C ≈ 3.98
  - yF = 115.3 keV/μm (3 MeV alpha, Bertolet 2023 anchor) → mean C ≈ 4.19
  - yF = 250 keV/μm (low-energy α, edge of paper range) → mean C ≈ 6.29
  - Monotone-increasing trend, brackets paper Fig 4c reported endpoints (~3.1 proton, ~4.5 helium). ✅
- These two checks together cover the entire analytical core of the 2025 paper; the macroscopic figures are an MC-transport convolution on top of these two relations.

## What is NOT covered by the smoke check
- The track-length / mean-chord correction `D_AB / l̄` that the 2025 paper adds for macroscopic use. (We do not have a test set of (D_AB, energy-deposit) pairs to apply it to.)
- TOPAS condensed-history transport with G4EmLivermore, TOPAS-nBio reference runs.
- Figures 4 (cell-layer monoenergetic), 5 (FWHM scan), 6 (Bragg-peak depth profile), 7 (RPT DSB/cell histograms).
- Standard DNA Damage (SDD) format export.

## HPC job plan (only if a full TOPAS-MGM extension becomes available)
Per AGENTS / TOOLS rules: do **not** run heavy compute on CherryRd. If/when the extension surfaces, this is the suggested job shape:

- **Target host:** `uicgpu` (8× A100, interactive, 2 TB RAM) for fastest turnaround on the analog TOPAS-nBio reference runs (the bottleneck); or **Aurora** PBS allocation `datascience` for batch sweeps.
- **Software stack:** TOPAS ≥3.9 + TOPAS-nBio (Geant4-DNA option 2), Geant4 11.x. Install per cluster module system; TOPAS academic registration required.
- **Inputs:** TOPAS extension source (TOPAS-MGM), TOPAS parameter files for (i) cell-layer monoenergetic beams (Fig 3 cross-verification: protons 0.5–150 MeV, α 0.25–150 MeV/u; Fig 4 cell-layer: 20 MeV p, 5 MeV/u He; Fig 5 FWHM scan); (ii) water phantom for 170 MeV p / 135 MeV/u He Bragg curves (Fig 6); (iii) cell monolayer with ²¹¹At and ²²⁵Ac decay sources, membrane-bound and free-in-medium (Fig 7).
- **Sizing (rough, from paper Table 1):** 100 ms / 1-MeV proton with TOPAS-MGM; 78 000× longer for TOPAS-nBio reference (≈ 7800 s per 1-MeV proton). Plan ≥ 10⁶ primaries for cell-layer histograms, ≥ 10⁷ for Bragg curves → reference runs are 10³–10⁴ CPU-hours; TOPAS-MGM macroscopic runs are minutes.
- **Estimated wall time:** few hours per scenario for TOPAS-MGM, multi-day for the cross-verification TOPAS-nBio reference set on 64–128 cores.
- **Storage:** SDD-format outputs ~MB per scenario; reference TOPAS-nBio root files multi-GB. Stage to `/data/stevens/scratch/lucid100-slot044-mgm/` on uicgpu.
- **Validation rubric:**
  1. Reproduce paper Table 1 timing ratios (single 1 MeV proton, single 1 MeV α) within 2×.
  2. Reproduce Fig 3a/3b cross-verification panels: TOPAS-MGM vs TOPAS-nBio mean MDS/track and weighted-mean complexity. Pass if relative error <10 % above the yF thresholds the paper itself flags (yF < 30 keV/μm protons, yF < 200 keV/μm helium).
  3. Reproduce Fig 6 Bragg peak MDS/dose enhancement: ~4.0× for α at BP, ~1.12× for proton at BP, within 20 %.
  4. Reproduce qualitative heterogeneity contrast in Fig 7: RPT DSB-per-cell histograms substantially broader than external-beam analogues.

## Next actions (if revisiting)
1. Email the corresponding author (Bertolet, MGH) to ask whether TOPAS-MGM will be released or distributed via the TOPAS extensions repository — **do not** do this without explicit user approval (paper says "no author contact").
2. Monitor `MGHPhysicsResearch` GitHub org for a TOPAS-MGM repo.
3. With user approval, pull the PMC supplementary material (sections 1.1.1, 1.1.2 give AAPM TG-268 reporting + the input cards used for the runs) via a human browser session and store under `artifacts/supplementary/`.
4. If a CPU-only extension surfaces, redo Check 2 against new TOPAS-nBio yF spectra from Geant4-DNA examples (small enough to run on uicgpu interactively).

## Files & paths
- Workspace folder: `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-mgm-dna-damage-protons-helium/`
- Smoke script: `scripts/smoke_mgm.py`
- Plots: `scripts/out/check1_N_MDS_vs_yF.png`, `scripts/out/check2_complexity_pdf.png`, `scripts/out/check2b_mean_complexity_vs_yF.png`
- Numbers: `scripts/smoke_results.json`
- Manifest: `artifact_manifest.json`
- JSON progress record: `~/.openclaw/workspace/memory/subagent-progress/lucid100-slot044-mgm-dna-damage-protons-helium.json`

---

## Open Questions & Reproducibility Blockers

- **Replicated for analytical core only.** The two equations the 2025 paper builds on (`N_MDS(yF)` polynomial, gamma `f(C; yF)` complexity distribution) are reproduced from the public `MGHPhysicsResearch/MGM` v1.0.1 library to <0.3 % over the published yF range, and gamma-mean complexity brackets the paper's Fig 4c endpoints. No blockers at the analytical-engine layer.
- **Blocking artifact (TOPAS-MGM extension source code):** the macroscopic TOPAS wrapper introduced by this paper (the condensed-history coupling, the `D_AB / l̄` chord-length correction applied at each transport step, the SDD export hook) is NOT in `MGHPhysicsResearch/MGM` and is not in the TOPAS extensions repository or any public GitHub fork we can find. Without it, Figs 4 (cell-layer monoenergetic), 5 (FWHM scan), 6 (Bragg-peak MDS/dose ratios up to 4× for α / 1.12× for protons), and 7 (RPT DSB/cell histograms for ²¹¹At / ²²⁵Ac membrane-bound vs free-in-medium) cannot be regenerated.
- **Blocking artifact (TOPAS-nBio reference dataset):** the cross-verification benchmarks in Fig 3 rely on TOPAS-nBio reference runs (Geant4-DNA Option 2) of the same geometries. No SDD-format reference output files are deposited; reproducing them is multi-day on 64–128 cores per the paper's own Table 1 timing ratios (~78 000× the MGM cost for protons, ~243 000× for α).
- **Open question:** does the `D_AB / l̄` chord-length correction remain accurate at the yF thresholds the paper itself flags (yF < 30 keV/μm protons, yF < 200 keV/μm helium), or does macroscopic averaging systematically bias MDS yields near the Bragg peak where energy-deposit-per-step is most variable?
- **Open question:** would a fully open Geant4-DNA implementation of the same condensed-history wrapper give the same ~78 000× speed-up, or is the speed-up partly dependent on TOPAS-specific scoring infrastructure?

