# Artifact manifest — lucid100-neutron-rbe-pre-post-dna-repair

DOI: 10.1088/1361-6560/ae36e1
Harvested: 2026-06-09 (CDT) on CherryRd
Distribution rights: paper PDF CC-BY (IOP); code/data MIT (Zenodo 10.5281/zenodo.17087505)

## Local artifacts (in `artifacts/`)

| Path                                                  | SHA-256 (truncated)               | Size  | Source URL                                                                                                  | License |
| ----------------------------------------------------- | --------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------- | ------- |
| `paper.pdf`                                           | `bd2b7771…d4e4b239`               | 1.3 M | https://iopscience.iop.org/article/10.1088/1361-6560/ae36e1/pdf                                             | CC-BY   |
| `paper.txt`                                           | `b1c2cd15…6c98730d2cd4`           | 56 K  | pdftotext extraction of paper.pdf                                                                            | derived |
| `zenodo_record.json`                                  | `d8edfd44…63a2df1f`               | 8 K   | https://zenodo.org/api/records/17087505                                                                     | CC-BY   |
| `topas_clustered_dna_damage-SDD-Scorer.zip`           | `983f5478…faa17c649`              | 4.7 M | https://zenodo.org/api/records/17087505/files/topas_clustered_dna_damage-SDD-Scorer.zip/content             | MIT     |
| `code_SDD-Scorer/`                                    | (unzipped contents of above)      | 8.4 M | —                                                                                                            | MIT     |

## Equations and parameters extracted from `paper.txt`

* **Eq. 3** — RBE = α_i / α_r (general LQ linear-component ratio)
* **Eq. 4** — RBE = Y_i / Y_r when D_i = D_r (linear regime)
* **Eq. 5** — Y_P = Σ_S Y_S · d_S / D_S  (per-secondary-species weighted sum)
* **Eq. 6** — RBE(E) = Y_n(E) / Y_X
* **Table 1** — TSMC parameters
  * Physics: `G4EmDNAPhysics_hybrid2and4` (option 2 + option 4 combo)
  * Strand-break energy threshold: 17.5 eV
  * Base-lesion energy threshold:  17.5 eV
  * P(HO• → damage): 40 %
  * DSB max length: 10 bp
  * Target dose: 1 Gy
  * Repeats: 100 neutron secondaries, 950 photon
* **Table 2** — endpoint definitions
  * DSB site (≥ 2 lesions counted, 1 DSB minimum)
  * Complex DSB lesion (≥ 1 DSB + ≥ 1 other lesion within 40 bp of nearest neighbour; min 3)
  * DSB cluster (Baiocco 2016) — ≥ 2 DSBs within 25 bp; min 4
  * Nearby DSB pair — 2 DSBs with centre-to-centre Euclidean distance ≤ d_max; min 4
  * Misrepair (DaMaRiS NHEJ) — 2 DSB ends from distinct DSBs that joined
* **Headline RBE values** (Section 3, paper)
  * DSB site max RBE: **2.54(3)**
  * Complex DSB max RBE: **4.78(8)**
  * DSB cluster max RBE: **16(1)**
  * Misrepair max RBE: **23(1)** at **0.5 MeV neutron**
* **Best-matching Euclidean distances for misrepair yields**: **18 nm** (0.5 MeV neutrons), **60 nm** (250 keV photons)

## Inside `code_SDD-Scorer/` (highlights)

* `payload/ComplexDSbCounter.py`
  – functions: `read_after_header`, `Count_ComplexClusters`, `Count_BaioccoCluster`,
    `GeoCluster(SDDFilePath, eps)`, `clusterer(SDD_file_path, eps)`.
  – `clusterer` returns `[N_Baiocco_input_DSBs, N_complex_DSB_lesions,
    N_Baiocco_DSB_clusters, *N_geo_clusters_per_eps]`.
* `payload/supportFiles/relative_doses/reldose_n{ENERGY}_{inner|inter|outer}_{electron|proton|alpha}.txt`
  – 165 files = 18 neutron energies × 3 scoring volumes × 3 species (minus a few not deposited).
  – Format: a single TOPAS-style line  `u:Sc/ClusterScorer/RelativeDose = <float>`.
  – Outer-sphere triplets (used in this paper) sum to ≈ 1.000 per energy.
* `geometry/`  TOPAS extension C++ for the 30 cm ICRU-4 sphere and the human nucleus model (`GeoCalculationV2.{cc,hh}`, `VoxelizedNuclearDNA.{cc,hh}`).
* `topas_mods/`, `physics/`, `scoring/`  TOPAS user classes.
* `payload/supportFiles/damaris/`  pathway and motion control files (`pathwayNHEJ.txt`, `pathwayHR.txt`, `motion.txt`, `TOPASChemistry.txt`).
* `payload/DNAParameters.txt`, `payload/damage_static_top_params.txt`,
  `payload/damage_xray_static_top_params.txt`, `payload/repair_static_top_params.txt`
  — fully-specified TOPAS parameter files for damage and repair runs.

## Not harvested (intentional)

* **`zenodo:17087505/Data.zip` (690 MB)** — raw SDD outputs for all
  18 neutron energies and 250 keV photon reference. Contains thousands of
  per-run `*_SDDOutput.txt`, `*_AllEvents.txt`, `rd_*.txt`. We skipped the
  full download per LUCID100 "no heavy compute on CherryRd" rule and
  because re-clustering against it (Step 3 of pipeline) is what an HPC
  re-run targets. A targeted single-energy slice (≈40–80 MB) can be
  fetched if a follow-up wants to validate the clusterer end-to-end.
* **TOPAS / TOPAS-nBio / Geant4 / Geant4-DNA / DaMaRiS source builds** —
  these are external simulator dependencies, deferred to the HPC plan
  (`docs/HPC_JOB_PLAN.md`).
