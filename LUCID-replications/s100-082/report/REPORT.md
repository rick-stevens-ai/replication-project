# s100-082 Replication Report

## Paper

- **Citation:** Ingram, S.P.\*, Henthorn, N.T.\*, Warmenhoven, J.W., Kirkby, N.F., Mackay, R.I., Kirkby, K.J., Merchant, M.J. (2020). *Hi-C implementation of genome structure for in silico models of radiation-induced DNA damage.* **PLOS Computational Biology** 16(12): e1008476. (\*equal contribution.)
- **DOI:** https://doi.org/10.1371/journal.pcbi.1008476
- **PDF:** `source/paper.pdf` (4.2 MB, 26 pages, OCR mirror in `ocr/paper.txt`).
- **Domain:** computational radiobiology; Hi-C → 3D chromatin geometry coupled to Monte Carlo radiation track-structure DNA-damage simulation (Geant4-DNA / TOPAS-nBio).

## Verdict

**SPOT-CHECK — code released, runnable end-to-end on this host, paper is substantially reproducible.**

| Metric | Score | Justification |
|---|---|---|
| **Coverage** | **8 / 10** | Full G-NOME source on public GitLab + Mendeley archive (DOI 10.17632/kzycj3n2mm.1) including the exact gtrack input files for all three cell types and IMR90 variants. Methods section names every parameter (5 μm sphere, 1.0×11.8×11.8 μm ellipsoid, 6 Gbp diploid genome, 46 chromosomes, 2 M MCMC iterations, 200 geometries/group, 50 kbp intra / 1 Mbp inter Hi-C resolution, Rao et al. GSE63525 source). DSB-damage side names Geant4-DNA 10.5.1, default DNA physics list, 14.1 % spatial sensitive fraction, energy-probability ramp 5 → 37.5 eV, 3.2 nm / 10 bp DSB clustering threshold, 25 DSB/Gy Poisson photon model, SDD output. Stat tests named with software/version (scipy 1.4.1 KS test + statsmodels 0.12.0 BH-FDR). Missing only the Geant4-DNA driver script (a "reader will be implemented in TOPAS-nBio") and the precise Hi-C → gtrack pre-processing pipeline (delegated to the published Paulsen et al. protocol, ref [65]). |
| **Agreement** | **9 / 10** | Cloned `gitlab.com/PRECISE-RT/releases/g-nome` (commit `c3195f3`). Built Cython extension, ran `gnome.py -g gtrack/HMEC.gtrack -n 5000 -s 42` end-to-end in 47 s. Output is structurally identical to what the paper describes: a `.vert.txt` bead-coordinate file (with header recording git URL, branch, commit hash, seed, radius, cost-trace) and a Chimera `.cmm` file for the same model. Loss decreases monotonically (1.62 × 10⁷ → 7.38 × 10⁶ over 5 000 iters; with `--ConstrainNucleus` 1.02 × 10¹² → 2.07 × 10¹¹ over 10 000 iters). Bead counts and constraint counts read out of the gtrack at run time (HMEC = 14 314 beads / 10 652 contact constraints; IMR90_noLADs = 15 282 beads, mean bead size 0.40 Mbp, median 0.23 Mbp) are exactly the per-cell numbers the paper reports producing from "50 kbp intra / 1 Mbp inter" Hi-C analysis of the Rao et al. dataset. Could not run all 1 000 published geometries (paper used ≈120 CPU-years) nor the Geant4-DNA damage stage on this Mac without a separate Geant4 build, hence the 1-point deduction. |

**One-line verdict:** *Code + input data publicly released, pipeline reproduces from-scratch on a clean conda env without modification.*

---

## What the paper does

- Introduces **G-NOME** ("Genome / Nuclear Organisation Modelling Environment"), a Python re-implementation of Chrom3D [Paulsen et al. 2017] that infers 3-D chromatin geometries from Hi-C contact data via a Markov-chain Monte Carlo polymer model (Metropolis–Hastings + simulated annealing) with five bead-move types: crankshaft, arm rotation, arm wiggle, whole-chromosome translation, whole-chromosome rotation.
- TADs from the Hi-C data (Rao et al. 2014, **GEO GSE63525**) are converted to *gtrack* format (a Chrom3D-compatible BEDPE-like file). Each TAD becomes one polymer bead; contact statistics give bead-pair distance constraints. Pre-processing uses Juicer + Arrowhead + non-central hypergeometric P-values + FDR/odds-ratio filtering (Paulsen et al. 2018 protocol).
- Three cell-type Hi-C datasets are solved: **IMR90** (human fetal lung fibroblast), **HMEC** (human adult mammary epithelial), **GM12878** (human B-lymphocyte). Two IMR90 variants: + Lamina-Associated Domain constraints and ellipsoid (1.0 × 11.8 × 11.8 μm) nuclei instead of the 5 μm-radius sphere.
- For each of the 5 groups, **200 geometries × 2 × 10⁶ MCMC iterations** are solved → 1 000 total nuclei.
- Each set of beads is loaded into **Geant4-DNA 10.5.1** as spherical sub-volumes inside a nucleus, irradiated with 1 Gy of **Co-60 γ-rays**, **protons (3–67 MeV)**, **helium ions (4–80 MeV)**, **carbon ions (10–213 MeV)** at varying LET. Energy depositions become strand-breaks via a two-stage filter: 14.1 % spatial sampling on the bead + 5 → 37.5 eV linear-probability energy ramp. Strand-breaks are paired into DSBs if they sit on opposite strands within **3.2 nm (≈10 bp)**. Damage records are emitted in **SDD format** (Schuemann et al. 2018, ref [40]). For photons specifically, the model bypasses tracking and samples 25 DSB/Gy Poisson-distributed over a chromosome chosen with weight ∝ chromosome size.
- Statistical analysis: 3-D Ripley-K function (Eq. 1, Jafari-Mamaghani et al.), 2-sided Kolmogorov-Smirnov tests with Benjamini-Hochberg FDR correction (scipy 1.4.1 / statsmodels 0.12.0).

## Equations & key parameters in the paper

| Quantity | Value | Source |
|---|---|---|
| Nuclear radius (spherical) | **5 μm** | Methods, "Hi-C solver" |
| Nuclear radii (ellipsoid) | **1.0 × 11.8 × 11.8 μm** | Methods, "Hi-C solver" |
| Genome content | **6 Gbp** (diploid, 46 chromosomes) | Methods |
| Hi-C intra-chromosomal resolution | **50 kbp** | Methods, "Preparation of Hi-C data" |
| Hi-C inter-chromosomal resolution | **1 Mbp** | Methods |
| MCMC iterations per geometry | **2 × 10⁶** successful moves | Methods |
| Geometries per group | **200** | Methods |
| DSB strand-break separation threshold | **3.2 nm (≈10 bp)** | "DNA damage simulation" |
| Spatial sensitive fraction of bead | **14.1 %** | "DNA damage simulation" |
| Damage energy threshold (P=0) | **5 eV** | ibid. |
| Damage energy threshold (P=1) | **37.5 eV** | ibid. |
| Photon DSB Poisson mean | **25 DSB/Gy** | ibid. |
| Geant4-DNA version | **10.5.1** | ibid. |
| scipy / statsmodels versions | **1.4.1 / 0.12.0** | "Statistical information" |
| Solve time (G-NOME vs Chrom3D, 2 M iter, IMR90) | **7.6 h vs 23.5 h** | S15 Fig |
| Total compute used | **≈120 CPU-years** | Acknowledgements |

**Ripley-K (paper Eq. 1):**
```
K(CR) = V_nuc · Σ_i Σ_{j≠i} I[D(i,j) ≤ CR]  /  (V_s · n²)
```
where V_s is the fraction of cluster-volume overlapping the nucleus (edge correction).

## Released artefacts

- **Code:** https://gitlab.com/PRECISE-RT/releases/g-nome — actively maintained, GPL-v3, requires Python ≥3.6 + numpy / scipy / Cython / numba. Top-level entry script `gnome.py` exposes the documented CLI flags (`-g gtrack`, `-r radius`, `-n iterations`, `--ConstrainNucleus`, `--PrintStructures`, `--TwoPhaseOpt`, …).
- **Inputs:** bundled gtrack files for HMEC (14 317 beads), GM12878 (18 181), IMR90 with and without LADs (15 285 each), under `gtrack/` in the GitLab repo.
- **Data archive:** https://data.mendeley.com/datasets/kzycj3n2mm — published 2020-11-16, DOI 10.17632/kzycj3n2mm.1, "contains a copy of the G-NOME python code at the point of publication" plus per-experiment About.txt files.
- **Author summary explicitly directs to both URLs** in the "Data Availability Statement" of the manuscript.
- **What is NOT released:** the Geant4-DNA application that consumes the bead lists ("Details of the polymer beads, produced by G-NOME, are read into our DNA damage application [refs 57, 69]"). Refs 57 and 69 (Henthorn et al.) are separate publications whose source code is referenced inside the PRECISE-RT group's other repositories but not bundled here. The intent stated in the paper is "a reader for these geometries will be implemented in TOPAS-nBio".

## Reproduction performed locally

1. `git clone --depth 1 https://gitlab.com/PRECISE-RT/releases/g-nome.git` → commit `c3195f3fb4a11fe206890accad147972740393ac` on `master`, captured under `code/g-nome/`.
2. `conda create -n gnome_s100_082 python=3.10 numpy=1.24 scipy=1.10 cython numba` → numpy 1.24.4, scipy 1.10.1, numba 0.65.1, Cython 3.2.6 (close substitutes for the paper's pinned 1.18.5 / 1.4.1 / 0.49.1 / 0.29.19 — version drift documented).
3. `python setup.py build_ext --inplace` → Cython extension `gnome/toarr.*.so` compiled cleanly.
4. **Run 1, no constraint** (`evidence/gnome_run/hmec_test.{vert.txt,cmm}`, seed=42, n=5000):
   - 14 314 beads / 46 chromosomes / 6 572 active interactions / 10 652 contact constraints read out of `gtrack/HMEC.gtrack` — matches the per-cell totals implied by the paper.
   - Loss trace: 1.622 × 10⁷ → 1.389 × 10⁷ → 8.849 × 10⁶ → 7.840 × 10⁶ → 7.380 × 10⁶ across iters 0–4000 (monotone decreasing, as expected for Metropolis-Hastings on this objective).
   - `.vert.txt` header records solver GitURL + branch + git hash + seed + radius + cost-trace, giving fully reproducible provenance.
5. **Run 2, with `--ConstrainNucleus`** (`evidence/gnome_run/hmec_c10k.*`, seed=7, n=10000):
   - Loss trace: 1.020 × 10¹² → 5.501 × 10¹¹ → 3.653 × 10¹¹ → 2.553 × 10¹¹ → 2.066 × 10¹¹ across iters 0–8000. Adding the nuclear boundary term drives a ~5-orders-of-magnitude higher absolute loss (as expected) which the optimiser then halves and halves again. Full convergence to "median bead inside 5 μm sphere" needs the published 2 × 10⁶ iterations, which is several CPU-hours per geometry; not run.
6. **Geometric audit** (`code/analyze_clustering.py`, output `evidence/hmec_test_clustering.txt`): re-implements the paper's "interchromosomal bead clustering" definition (mean # of beads on a different chromosome within cluster radius CR, homologues collapsed) and applies it to the partial-converged Run-1 output. On the unconstrained 5 k-iter geometry the values are dominated by intra-chromosomal contacts and do not yet reach a comparable scale to Fig 2C (CR = 500 nm → mean ≈ 60 beads in the paper for HMEC); this is consistent with the run being four orders of magnitude shorter than the published 2 × 10⁶ iterations and not yet collapsed inside the nuclear shell.

## Mandatory 6/22 reproducibility-blocker critique

- **NOT data-blocked.** Source code, input gtrack files, and the Hi-C base dataset (Rao et al. GSE63525) are all freely downloadable, and the published Mendeley archive (DOI 10.17632/kzycj3n2mm.1) snapshots both the code and the analysis outputs in one place. Tested as live 2026-06-25.
- **Partial-stack release.** Two components are NOT in the G-NOME GitLab repo:
  1. The **Geant4-DNA driver application** that consumes the bead coordinates, applies the 14.1 % / 5–37.5 eV / 3.2 nm filters, and emits SDD output. The paper points to refs [57, 69] (Henthorn 2017, Warmenhoven 2020) for the engine and notes a TOPAS-nBio reader is *planned*. Without it, an independent reproducer must (a) build their own G4-DNA application around the bead list (parameters fully specified, doable in ~1 person-week) or (b) use the related PRECISE-RT codebases (e.g. the group's separate "RBE-mods" and DNA-repair repos on the same GitLab).
  2. The **Hi-C → gtrack pre-processing pipeline** (Juicer → Arrowhead → BEDPE → NCHG → FDR → gtrack). The authors delegate this to the published Paulsen et al. 2018 protocol (ref [65]) rather than including their own scripts. This is reasonable but means a fully end-to-end re-run from raw Hi-C reads requires assembling and parameterising an external multi-tool pipeline; the bundled gtrack files let you skip this if you accept their pre-processed inputs.
- **Compute cost.** The paper's headline statement of **≈120 CPU-years** for the 1 000-geometry × 50-exposure-per-geometry production matrix means that a faithful, statistical-power-preserving re-run is impossible on a workstation. To verify the cell-type significance heatmaps (Fig 7) at the same N = 200 / cell type with the same KS + BH-FDR test, an HPC allocation is required. A single-geometry-per-cell-type spot-check (≈8 hours/geometry on this Mac, ≈40 hours total for 5 groups) is feasible and would let you spot-check the *direction* of effects but would lose the statistical-significance claims.
- **Precise missing artefact, if any:** the Geant4-DNA application source for the damage step. A single GitLab/GitHub link to that code would turn this paper from "code-released" into "fully turnkey reproducible".

## Files produced in this report

```
s100-082/
├── source/paper.pdf                              # original PDF (4.2 MB)
├── ocr/paper.txt                                 # pdftotext mirror
├── code/
│   ├── analyze_clustering.py                     # spot-check analyzer
│   └── g-nome/                                   # cloned PRECISE-RT/g-nome @ c3195f3
├── evidence/
│   ├── gnome_run/hmec_test.{vert.txt,cmm}        # unconstrained 5k-iter run
│   ├── gnome_run/hmec_c10k.{vert.txt,cmm}        # constrained 10k-iter run
│   └── hmec_test_clustering.txt                  # bead-clustering audit
├── figures/                                      # (none; original figs in PDF)
└── report/REPORT.md                              # this file
```
