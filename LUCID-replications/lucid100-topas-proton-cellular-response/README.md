# LUCID100 W2-#16 — Cellular Response to Proton Irradiation (TOPAS-nBio)

**Target paper**
Zhu H, McNamara AL, McMahon SJ, Ramos-Mendez J, Henthorn NT, Faddegon B,
Held KD, Perl J, Li J, Paganetti H, Schuemann J.
*Cellular Response to Proton Irradiation: A Simulation Study with TOPAS-nBio.*
**Radiation Research 194(1): 9–21 (2020).**
DOI: [10.1667/RR15531.1](https://doi.org/10.1667/RR15531.1)

Local copy: `paper.pdf` (3.5 MB, fetched from Queen's University Belfast open
research portal: <https://pureadmin.qub.ac.uk/ws/files/231105855/i0033_7587_194_1_9.pdf>).

## What this folder is

LUCID100 Wave-2 max-rate backfill slot 16 — **first-pass artifact harvest and
replication scoping** for the Zhu et al. 2020 TOPAS-nBio + MEDRAS proton-
irradiation paper. No author contact, no paid endpoints, no heavy compute on
CherryRd.

## Verdict (first pass)

**PARTIAL — analytical/MEDRAS pathway feasible, TOPAS-nBio physics rerun
requires HPC.**

| Component                                                   | Status                                                                |
|-------------------------------------------------------------|-----------------------------------------------------------------------|
| Paper PDF + Table A1 (setup) + Table A2 (DSB/SSB/SB yields) | **HARVESTED** (`paper.pdf`, transcribed to `artifacts/table_A2.csv`)  |
| Public reference implementation of repair model (MEDRAS-MC) | **HARVESTED** (`artifacts/Medras-MC/`, Python, GitHub open)           |
| Public TOPAS-nBio extension code                            | **HARVESTED metadata** (`artifacts/topas_nbio_meta.json`)             |
| Sanity reproduction: total DSB/Gy at low-LET (X-ray analog) | **SANITY PASS** (~33 DSB/Gy/cell ≈ 5.4 DSB/Gy/Gbp ≈ Zhu's 6.5)        |
| Initial physics DSB yield reproduction vs Table A2          | **NOT ATTEMPTED** (requires TOPAS-nBio + Geant4-DNA on HPC; job plan) |
| Misrepair fraction trend with LET                           | **METHOD AVAILABLE** (MEDRAS-MC handles step 2 from SDD files)        |
| Chromosome aberration / micronuclei yields (Fig 7, 8)       | **METHOD AVAILABLE** via MEDRAS-MC; needs proper SDD inputs           |

## Worktype correction

Master TSV (rank 47, Wave 2 slot 16) currently labels this paper as
`omics/signature replication`. **This is wrong.** The paper contains **no omics
data and no signature**. It is a two-stage Monte Carlo simulation pipeline:

1. Initial DNA damage from proton tracks → TOPAS-nBio (Geant4-DNA);
2. Repair + chromosome aberrations + micronuclei → MEDRAS-MC.

**Recommended retag:** `simulation/model replication` (consistent with the
other TOPAS-nBio / MEDRAS-MC entries already in the master, e.g. ranks 53, 68,
72, 79, 93).

## Layout

```
lucid100-topas-proton-cellular-response/
├── README.md                 # this file
├── PROGRESS.md               # phase log
├── FIRST_PASS_REPORT.md      # full claim-by-claim verdict
├── paper.pdf                 # local PDF (QUB open-access mirror)
├── paper.txt                 # pdftotext extraction
├── ARTIFACT_MANIFEST.md      # one-page index of artifacts
├── HPC_JOB_PLAN.md           # what running the TOPAS-nBio step would cost
├── code/
│   └── sanity_dsb_yield.py   # minimal MEDRAS-MC X-ray DSB/Gy sanity check
├── results/
│   ├── table_A2.csv          # transcribed paper Table A2 (DSB/SSB vs LET)
│   └── sanity_dsb_yield.txt  # run log
├── figures/                  # placeholder (no figures in first pass)
└── artifacts/
    ├── Medras-MC/            # cloned open-source repo (Python, BSD-2-style)
    ├── topas_nbio_meta.json  # GitHub metadata for upstream TOPAS-nBio
    └── README_artifacts.md
```

## How to rerun the sanity check

```bash
cd lucid100-topas-proton-cellular-response
python3 code/sanity_dsb_yield.py
```

Dependencies: Python 3.10+, NumPy. Uses the vendored
`artifacts/Medras-MC/damagegenerator/` package only (no Geant4 / TOPAS).

## Why we did NOT run TOPAS-nBio here

The Zhu et al. damage-induction step is the heavy half of the paper. Each
proton energy point needs O(10) hours wall-clock per 1 Gy run in 10-thread
mode on Xeon-class CPUs (Table A1), and 12 energy points × 100 runs each
(stated in the paper) is in the range of **~12,000 CPU-hours** for full
reproduction of Table A2 alone. That is HPC-territory and explicitly out of
scope for this max-rate backfill subagent on CherryRd. See `HPC_JOB_PLAN.md`
for a uicgpu / Aurora job plan if/when we want to actually re-run it.

## Public sources used

* Paper PDF — Queen's University Belfast institutional open-access mirror
  (CC compliant; document explicitly labelled "Open Access" / "Publisher's PDF").
* MEDRAS-MC — <https://github.com/sjmcmahon/Medras-MC> (public; explicitly
  cited and linked in the paper, §Materials and Methods).
* TOPAS-nBio — <https://github.com/topas-nbio/TOPAS-nBio> (public, requires
  free-for-academic TOPAS license to build/run).
* Standard DNA Damage (SDD) format spec — Schuemann et al. 2019,
  Radiat. Res. 191:76–92 (cited; format definition only, no fetch needed).

No author contact, no paid endpoints.
