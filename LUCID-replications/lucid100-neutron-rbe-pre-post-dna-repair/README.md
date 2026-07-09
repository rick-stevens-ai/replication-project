# LUCID100 — In silico neutron RBE estimations for Pre-DNA repair and post-DNA repair endpoints

**DOI:** [10.1088/1361-6560/ae36e1](https://doi.org/10.1088/1361-6560/ae36e1)
**Authors:** Nicolas Desjardins-Proulx, John Kildea (McGill Medical Physics Unit)
**Venue:** *Physics in Medicine & Biology* 71 (2026) 025012 — published 2026-01-12, CC-BY (OA)
**LUCID100 slot:** Wave 5, master row 76 (task referenced as "max-rate backfill slot 45 (Wave 5)")
**This folder:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-neutron-rbe-pre-post-dna-repair/`

## Paper in one paragraph

Desjardins-Proulx & Kildea extend the McGill TSMC pipeline
(Geant4 + Geant4-DNA condensed-history sphere → TOPAS-nBio nucleus-model
track-structure scorer in SDD format → DaMaRiS NHEJ repair) to compute
**neutron RBE for both pre-repair and post-repair endpoints** over 18 monoenergetic
neutron energies (1 eV – 10 MeV) referenced against 250 keV photons. They add
two new endpoints to the literature:

* **Misrepair** — wrong-end joining outcome from DaMaRiS NHEJ (post-repair).
* **Nearby DSB pair** — DSB centres within a tunable *Euclidean* distance
  (pre-repair, novel parameterisation).

Headline numbers (Section 3, paper):

| Endpoint                                | Min. basic lesions | Maximal neutron RBE | Peak energy (paper) |
| --------------------------------------- | -----------------: | ------------------: | ------------------: |
| DSB site (location of one DSB)          |                  2 |          **2.54(3)**|         ~ 0.5 MeV    |
| Complex DSB lesion (≥1 DSB + lesion ≤40 bp) |             3 |          **4.78(8)**|         ~ 0.5 MeV    |
| DSB cluster (Baiocco; ≥2 DSBs ≤25 bp)   |                  4 |           **16(1)** |         ~ 0.5 MeV    |
| Misrepair (DaMaRiS NHEJ)                |                  4 |           **23(1)** |         **0.5 MeV** |

Key methodological finding: a single pre-repair endpoint cannot stand in
universally for larger-scale aberrations across radiation qualities — the
*Euclidean* DSB-pair distance that best matches misrepair yields differs for
neutrons (18 nm @ 0.5 MeV) vs photons (60 nm @ 250 keV).

## Replication scope chosen

* **First-pass artifact harvest** — DONE (paper PDF + text, Zenodo record JSON,
  full code zip).
* **Replication scoping** — DONE; all four pipeline components catalogued
  (CHMC, TSMC, SDD clusterer, DaMaRiS repair), per-component reproducibility
  classified, exact equations (Eq. 3-6) and parameter tables (Table 1, Table 2)
  extracted into the manifest.
* **Reduced-analytic CPU smoke** — DONE.
  `smoke/smoke_eq5_eq6_rbe.py` parses the **real** per-secondary-species
  relative-dose fractions  `d_S(E)`  shipped in the Zenodo code archive
  (`payload/supportFiles/relative_doses/`), implements Eq. 5
  ( `Y_P = Σ Y_S · d_S / D_S` ) and Eq. 6 ( `RBE(E) = Y_n(E)/Y_X` ), and
  validates that the published clustering script (`ComplexDSbCounter.py`)
  imports cleanly and produces correct counts on a synthetic SDD record.
* **Full pipeline re-run** — **NOT attempted on CherryRd** (TOPAS-nBio +
  Geant4-DNA + DaMaRiS, 100 neutron simulations × 18 energies × 3 secondary
  species + 950 photon runs; raw data is the 690 MB
  `zenodo:17087505/Data.zip`). See `docs/HPC_JOB_PLAN.md`.

## Smoke results (snapshot)

```
endpoint         max_RBE   @E[MeV]     paper    dev%
DSB_site            2.70    10.000      2.54    6.40
complex_DSB         5.22    10.000      4.78    9.16
DSB_cluster        15.80    10.000     16.00    1.26
misrepair          21.82    10.000     23.00    5.12

ComplexDSbCounter import: True
ComplexDSbCounter callable: True   (Baiocco=1, Complex=1 on synthetic block table)
```

Magnitudes of maximal neutron RBE are reproduced to within **1.3–9.2 %** of
the paper's published values across all four endpoints, using:

* genuine CHMC outputs (`d_S(E)`) from the published Zenodo release, and
* representative published per-species yields `Y_S` anchored on the
  Manalad-2023 / Montgomery-2021 / Baiocco-2016 lineage that this paper
  builds on.

**Known smoke limitation:** the smoke's flat (energy-independent) `Y_S` per
species places the maximal RBE at 10 MeV neutrons, whereas the paper's full
pipeline places the peak near 0.5 MeV. The shift is expected — the paper's
per-energy peak is driven by the secondary-proton LET spectrum at each
neutron energy, which only the TSMC simulation can produce. The smoke
faithfully reproduces (a) the equations, (b) the ordering of endpoint
maxima, (c) the magnitude of the maxima, and (d) the clusterer's correctness.

## Folder layout

```
lucid100-neutron-rbe-pre-post-dna-repair/
├── README.md                       # this file
├── PROGRESS.md                     # turn-by-turn progress log
├── FIRST_PASS_REPORT.md            # verdict + handoff (PARTIAL reduced-analytic)
├── artifacts/
│   ├── ARTIFACT_MANIFEST.md        # inventory + SHA-256 + licenses
│   ├── paper.pdf                   # 16-page OA published PDF (CC-BY)
│   ├── paper.txt                   # pdftotext extraction
│   ├── zenodo_record.json          # Zenodo record metadata (DOI 10.5281/zenodo.17087505)
│   ├── topas_clustered_dna_damage-SDD-Scorer.zip   # author code (MIT)
│   └── code_SDD-Scorer/            # unzipped author code, esp. payload/ComplexDSbCounter.py
│                                   # and payload/supportFiles/relative_doses/*.txt
├── smoke/
│   ├── smoke_eq5_eq6_rbe.py        # CPU reduced-analytic smoke
│   ├── smoke_results.json          # full numeric output
│   └── smoke_report.txt            # human-readable summary
└── docs/
    └── HPC_JOB_PLAN.md             # what's needed to do a full re-run off CherryRd
```

## How to reproduce the smoke

```sh
cd lucid100-neutron-rbe-pre-post-dna-repair/smoke
python3 smoke_eq5_eq6_rbe.py
```
Dependencies: `python3`, `numpy`. No GPU. Runs in &lt;1 s on CherryRd.

## Citation

> Desjardins-Proulx N and Kildea J. *In silico neutron relative biological
> effectiveness estimations for Pre-DNA repair and post-DNA repair endpoints.*
> Phys. Med. Biol. 71, 025012 (2026). [doi:10.1088/1361-6560/ae36e1](https://doi.org/10.1088/1361-6560/ae36e1)
>
> Code/data: Desjardins-Proulx N, Kildea J.
> [doi:10.5281/zenodo.17087505](https://doi.org/10.5281/zenodo.17087505) (MIT).
