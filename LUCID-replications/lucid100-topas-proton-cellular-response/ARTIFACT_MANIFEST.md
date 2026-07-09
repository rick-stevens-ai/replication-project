# Artifact Manifest — LUCID100 W2-#16

Paper: Zhu et al. 2020, *Cellular Response to Proton Irradiation: A Simulation
Study with TOPAS-nBio*, Radiat. Res. 194(1):9–21. DOI 10.1667/RR15531.1.

## Local artifacts

| Path                                          | Type        | Size      | Provenance                                                           |
|-----------------------------------------------|-------------|-----------|----------------------------------------------------------------------|
| `paper.pdf`                                   | PDF         | 3.55 MB   | <https://pureadmin.qub.ac.uk/ws/files/231105855/i0033_7587_194_1_9.pdf> (Queen's University Belfast Open Access mirror; labelled "Publisher's PDF / Version of record") |
| `paper.txt`                                   | text        | 86 KB     | `pdftotext -layout paper.pdf paper.txt`                              |
| `results/table_A2.csv`                        | CSV         | 1.3 KB    | Hand-transcribed from paper Appendix Table A2 (12 energies × 11 cols)|
| `results/sanity_summary.md`                   | markdown    | 2.6 KB    | DSB counts derived from MEDRAS-MC `basicXandIon` SDD files           |
| `results/sanity_dsb_yield.txt`                | log         | ~2 KB     | stdout of `code/sanity_dsb_yield.py`                                 |
| `results/sanity_sdd/*.txt`                    | 23 SDDv1.0  | ~590 KB   | MEDRAS-MC empirical damage generator (runs=2, X/p/C)                 |
| `code/sanity_dsb_yield.py`                    | Python      | 4.2 KB    | Author: this subagent. Vendors MEDRAS-MC, runs runs=2 sanity dataset |
| `artifacts/Medras-MC/`                        | git clone   | ~4 MB     | `git clone --depth 1 https://github.com/sjmcmahon/Medras-MC` (commit pinned by clone time 2026-06-09) |
| `artifacts/topas_nbio_meta.json`              | JSON        | ~6 KB     | `https://api.github.com/repos/topas-nbio/TOPAS-nBio` snapshot        |

## Upstream public artifacts NOT downloaded (covered by URL / metadata only)

| Resource              | URL                                                         | Why we did not fetch                                            |
|-----------------------|-------------------------------------------------------------|------------------------------------------------------------------|
| TOPAS-nBio source     | <https://github.com/topas-nbio/TOPAS-nBio>                  | Builds against TOPAS + Geant4; needs HPC stack (see HPC_JOB_PLAN.md) |
| TOPAS                 | <http://www.topasmc.org/>                                   | Free-for-academic registration required; not needed for first pass   |
| Geant4 / Geant4-DNA   | <https://geant4.cern.ch/>                                   | Large dependency; pulled lazily on HPC                               |
| SDD format spec       | Schuemann et al. 2019, Radiat. Res. 191:76–92               | Format documented; SDD writer already in MEDRAS-MC                    |
| MEDRAS / MEDRAS-MC paper | McMahon 2017 Sci Rep 6:33290; McMahon-Prise 2021 Front Oncol 11:689112 | Already in `lucid-medras-mc` (PARTIAL → REPLICATED)              |
| Friedland 2017 cross-comparison | Sci Rep 7:45161                                  | Reference comparison data; would re-digitalize Fig 5 of Zhu only on demand |
| Edwards 1985 lymphocyte data     | Int. J. Radiat. Biol. 50:137–45               | Experimental anchor for Fig 7; digitized values already in Zhu       |

## Provenance & licensing notes

- **paper.pdf** carries the QUB "Open Access" banner and is the Publisher's
  Version of Record (Radiation Research Society 2020). Mirror is institutional,
  no paywall encountered.
- **MEDRAS-MC** has no `LICENSE` file at repo root, but individual `.py` files
  carry BSD-2-Clause headers (verified in our prior `lucid-medras-mc`
  replication). Treat as BSD-2-Clause; do not redistribute without checking.
- **TOPAS-nBio** repo has a `LICENSE` file (GitHub reports it as
  NOASSERTION — needs human review before redistribution; for use only,
  registration via topasmc.org gates TOPAS itself).

## How to verify provenance

```bash
cd lucid100-topas-proton-cellular-response

# Paper checksum
shasum -a 256 paper.pdf

# MEDRAS-MC commit
cd artifacts/Medras-MC && git rev-parse HEAD && git log -1 --oneline

# Refetch TOPAS-nBio metadata
curl -sSL https://api.github.com/repos/topas-nbio/TOPAS-nBio | python3 -m json.tool | head -20
```
