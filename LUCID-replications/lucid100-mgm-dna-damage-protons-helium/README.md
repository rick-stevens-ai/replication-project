# LUCID100 slot 44 — MGM extension for DNA damage by protons & helium ions

**Paper:** Onecha, Schuemann, Paganetti, Bertolet (2025).
*"Extending the Microdosimetry Gamma Model (MGM) to estimate induced DNA damage and its complexity at macroscopic scale by protons and helium ions."*
**DOI:** 10.1088/1361-6560/ae117e
**Venue:** Physics in Medicine and Biology, 70(20)
**PMC:** PMC12905799 / PubMed 41067246
**Author manuscript (HHS Public Access) PDF used:** `artifacts/paper.pdf` (1.7 MB, 25 pp.)
**Wave / slot:** Wave 5 / slot 44 (LUCID100 max-rate backfill)

## TL;DR
This paper plugs an existing analytical microdosimetric model (MGM, Bertolet et al 2023) into the TOPAS Monte Carlo toolkit so DNA double-strand-break (DSB) yields and per-MDS complexity distributions can be evaluated at macroscopic (mm to cm, mono-energetic beams, Bragg peaks, RPT cell layers) scale ~10⁵× faster than the reference track-structure DNA-scale TOPAS-nBio. The novel pieces are (i) a track-length / mean-chord-length correction that lets the originally cell-scale MGM run inside a condensed-history macroscopic transport simulation and (ii) a TOPAS extension (TOPAS-MGM) wrapping it.

## Status
First-pass artifact harvest + replication scoping + minimal CPU smoke check.
**Smoke check: PASS** (analytical engine reproducible on CPU).
**Full TOPAS-MGM replication: NO-GO on CherryRd** (extension code not public; would need MC HPC even if it were).

## What is open / what is not
| Asset | Status | Where |
|---|---|---|
| 2025 paper (author manuscript) | Open via HHS Public Access | `artifacts/paper.pdf` (downloaded from EuropePMC PMC12905799) |
| Supplementary material | Referenced as "Sections 1.1.1 / 1.1.2", **only available via PMC web viewer** (recaptcha blocks bot fetch); not retrieved | not in artifacts |
| Bertolet 2023 predecessor (MGM theory) | Open access | `artifacts/mgm2023.pdf` (Frontiers in Oncology) |
| **MGM analytical engine (Python)** | **Public, MIT licence** | `artifacts/mgm-repo/` from `https://github.com/MGHPhysicsResearch/MGM` (was `mghro/mgm`) — v1.0.1 |
| **TOPAS-MGM extension (C++/TOPAS)** | **NOT released** anywhere we can find — no GitHub/Zenodo/figshare URL in paper, not in `MGHPhysicsResearch` org | n/a |
| TOPAS toolkit | Free for academic use after registration | not installed locally |
| Geant4-DNA (option 2) physics | Open via Geant4 | not installed locally |

## Smoke check (CPU only)
`scripts/smoke_mgm.py` loads the published MGM Python library and verifies two equations the 2025 paper cites:

1. **N_MDS(yF)** quadratic fit — paper quotes
   `N_MDS(yF) = 0.13·yF + 9.66×10⁻⁴·yF²`
   Library ships `0.12962·yF + 9.657×10⁻⁴·yF²` → max rel. error **< 0.3 %** over yF ∈ [2, 200] keV/μm. ✅
2. **Gamma complexity distribution** `f(C|yF)` evaluated at paper anchor energies (3 MeV proton ⇒ yF≈10.95; 4-MeV / 3-MeV alphas ⇒ yF≈100, 115.3 keV/μm). Mean complexity grows monotonically with yF from ~2.9 → ~6.3, bracketing the paper's Fig 4c reported range (~3.1 proton low-LET → ~4.5 helium high-LET). ✅

Output: `scripts/smoke_results.json` + three PNGs in `scripts/out/`.

## Why we did not run TOPAS-MGM
- The TOPAS extension `TOPAS-MGM` is the central new code contribution of the paper, but **no public URL is provided** (we searched the paper PDF and the authors' GitHub org `MGHPhysicsResearch`). Only the cell-scale Python MGM (engine inside the extension) is public.
- Even with the extension, the validation runs are full Monte Carlo: track-structure Geant4-DNA in TOPAS-nBio compared against condensed-history G4EmLivermore in TOPAS-MGM, on cell-monolayer + water-phantom geometries, with proton beams up to 170 MeV and helium up to 135 MeV/u, plus ²¹¹At/²²⁵Ac RPT. **Per AGENTS / TOOLS policy: heavy compute does not run on CherryRd.** An HPC job plan is sketched in `FIRST_PASS_REPORT.md`.

## Reproduce the smoke check
```bash
cd lucid100-mgm-dna-damage-protons-helium
python3 -m pip install --user numpy scipy matplotlib   # one-time
python3 scripts/smoke_mgm.py
ls scripts/out/                                        # plots
cat scripts/smoke_results.json                         # numbers
```

## Layout
```
artifacts/
  paper.pdf                 # Onecha 2025 author manuscript (EuropePMC)
  europepmc_meta.json       # EuropePMC core record
  europepmc.html            # search landing page
  mgm2023.pdf               # Bertolet 2023 MGM theory paper
  mgm2023.txt               # pdftotext dump
  mgm-repo/                 # MGHPhysicsResearch/MGM clone
scripts/
  smoke_mgm.py              # CPU smoke check
  smoke_results.json
  out/                      # plots
PROGRESS.md
README.md
FIRST_PASS_REPORT.md
NO_GO_REPORT.md             # for the unreleased TOPAS extension
artifact_manifest.json
notes/
```
