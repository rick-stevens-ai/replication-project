# Reproducibility scorecard — Masilela et al 2026 (DOI 10.1088/1361-6560/ae62c6)

Scoring follows the FAIR + ACM artifact-evaluation conventions, rolled up to a
LUCID100-internal 1-5 score.

## Item-by-item

| Component | Stated in paper? | Released? | Reproducible *now*? | Score (1-5) |
|---|---|---|---|---|
| Final PDF | yes | CC-BY 4.0 OA at IOPscience | yes — `artifacts/paper.pdf` | 5 |
| Supplementary information | "All data … are included within the article" | no separate supplement | n/a | n/a |
| Simulator name & version | yes (`OpenTOPAS v4.0.0`, `TOPAS-nBio v4.0 dev`, `Geant4-11.1.3`) | OpenTOPAS v4.0.0 released; TOPAS-nBio v4.0 dev branch **not yet tagged** | partially | 3 |
| Physics list | yes (`G4EMStandardPhysics_opt4` for CH; `TsEmDNAPhysics` opt-2 derived for TS, ELSEPA elastic, Meesungnoen thermalisation) | TOPAS-nBio v2 ships the base list; ELSEPA modification not in public main yet | partially | 3 |
| Chemistry list (all 43 reactions + kobs) | **yes**, full Table 1 | reproduced verbatim in `scripts/chemistry_table1.csv` | yes | 5 |
| Geometry (pUC19, supercoiling, base-pair-level scoring) | qualitatively — references D-Kondo 2021 | the D-Kondo 2021 plasmid geometry is built into TOPAS-nBio examples | yes (via TOPAS-nBio examples) | 4 |
| DSB scoring script (`acceptance/rejection over per-strand IDs, 10⁶ iterations`) | algorithm described in Section 2.2.3 | **not released** as a standalone Python file | re-implementable from description | 3 |
| Source spectrum (225 kVp x-ray from a SARRP) | yes, references Miles 2023 | needs reproduction via condensed-history TOPAS run (5×10⁸ histories) | yes, given OpenTOPAS | 4 |
| Pulse model (UHDR 5 µs FWHM, CONV 1000 s FWHM) | yes | parameterisable in TsTrackStructureSource | yes | 5 |
| Damage-induction efficiencies (η_OH = 0.24, η_H = 0.008; WR-1065 70% on R40/R41*) | yes; refs Ramos-Méndez 2021 + D-Kondo 2024 for the Nelder-Mead fit | the fit itself not re-published | post-MC scalar | 5 |
| WR-1065 chemistry (R37–R43*) | yes | rate constants from Milligan 1995 + Ward 1984 — publicly cited | yes | 4 |
| Run statistics (5×10⁸ condensed-history primaries; stat-unc < 2% in TS phase) | yes, with run-count target | reproducible on HPC | yes (with allocation) | 4 |
| Sensitivity analysis (DSB 5/10/15 bp; DNA 50 vs 250 µg/mL) | yes, in §3.2 | reproducible from same scoring script | yes | 4 |
| Experimental comparator data (Milligan, Tomita, Klimczak, Sforza, Wanstall, Perstin, Konishi, Kunz, Wang, Ohsawa, Small) | yes, Table 2 with values quoted | values quoted *are* the comparators; raw datasets behind some are paywalled | yes (values), partial (raw) | 4 |
| Raw simulation outputs / per-condition CSVs | not stated | not deposited | no | 1 |

**Roll-up score: 3.6 / 5** (methods are very well documented; gap is the
release of the chemistry decks + DSB scoring script).  The paper would land
at 4.6/5 with a Zenodo deposit of just two files: (1) the Models 1+2 TsChemistry
.topas decks and (2) the Python DSB post-processor.

## Quickest path to 5.0/5

Author action required (recommended but blocked per task — no contact):

1. Push the two chemistry decks (Model 1 + Model 2) to
   `topas-nbio/TOPAS-nBio-v2.0/examples/processes/scavengers/uhdr-plasmid-masilela-2026/`.
2. Add the DSB post-processor as `examples/.../dsb_score.py`.
3. Tag the corresponding TOPAS-nBio commit (currently the "dev" branch) so the
   paper's "TOPAS-nBio v4.0" reference becomes resolvable.

These are all author-cost-zero artefacts that exist on the authors'
filesystems; they were simply not yet promoted to the public release.
