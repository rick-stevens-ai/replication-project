# Artifact harvest

## Source paper
| Item | URL | Size | Notes |
|---|---|---|---|
| `paper.pdf` | https://www.osti.gov/servlets/purl/2583708 | 1,304,946 B | OSTI open-access mirror; SHA already-integrity-checked by OSTI |
| Publisher HTML | https://iopscience.iop.org/article/10.1088/1361-651X/ade176 | ~200 KB | Used for table structure recovery |
| Publisher suppdata | https://iopscience.iop.org/article/10.1088/1361-651X/ade176/suppdata | ~14 KB | **Blocked** by Radware Bot Manager captcha; direct CDN link `https://content.cld.iop.org/journals/0965-0393/33/5/055010/suppdata/` returns 403. This is the location where the paper says "input scripts, tabulated binding energies, and representative FHI-aims input script" live. Not retrievable through automated fetch. |

## Public code artifacts
| Item | URL | Notes |
|---|---|---|
| `tdjanic-snl/spparks` — master | https://github.com/tdjanic-snl/spparks | Fork of spparks/spparks; last commit 2025-03-31 |
| Branch `nonorth` | https://github.com/tdjanic-snl/spparks/tree/nonorth | Commit `82a9083` — non-orthogonal / HCP additions |
| Branch `resveratrol` | https://github.com/tdjanic-snl/spparks/tree/resveratrol | Commit `f6bcc3b` — merges nonorth + adds `create_sites` 3D-random-deposition; **does NOT** contain the `diffusion/disphere` app style or `resv` lattice style promised in the paper |
| Upstream SPPARKS | https://github.com/spparks/spparks | Parent project. Used only for diff basis. |

## Diff of `resveratrol` branch vs `master`
```
 src/app.cpp              |   1 +
 src/app_diffusion.cpp    | 227 +++++++++++++++++++++++++++++++++++++----------
 src/app_diffusion.h      |   1 +
 src/app_lattice.cpp      |  19 +++-
 src/app_lattice.h        |   1 +
 src/create_box.cpp       |   9 +-
 src/create_sites.cpp     |  91 +++++++++++++------
 src/create_sites.h       |   8 +-
 src/diag_cluster.cpp     |   4 +-
 src/domain.cpp           |  83 ++++++++++-------
 src/domain.h             |   3 +-
 src/dump.cpp             |   2 +-
 src/dump.h               |   2 +-
 src/dump_sites.cpp       |   1 +
 src/dump_text.cpp        |   9 +-
 src/lattice.cpp          |  22 ++++-
 src/lattice.h            |   1 +
 src/read_sites.cpp       |   5 ++
 src/region.cpp           |   1 +
 src/region.h             |   3 +-
 src/region_hex.cpp       | 107 ++++++++++++++++++++++
 src/region_hex.h         |  54 +++++++++++
 src/region_intersect.cpp |   1 +
 src/region_union.cpp     |   2 +
 src/style_app.h          |  25 ++++++
 src/style_command.h      |   5 ++
 src/style_diag.h         |   9 ++
 src/style_dump.h         |   4 +
 src/style_pair.h         |   1 +
 src/style_region.h       |   6 ++
 src/style_solve.h        |   3 +
 31 files changed, 577 insertions(+), 133 deletions(-)
```

## Local build artifacts (uicgpu)
| Path | Size | Notes |
|---|---|---|
| `~/replicate/osti-2583708/spparks-resv/src/spk_uic` | 895,386 B text | GCC 12 / mpicxx / -O2 -std=c++17 |
| `~/replicate/osti-2583708/runs/sweep/dump.s{1..10}` | ~3 MB each | 10-seed KMC dump text (id x y z i1) |
| `~/replicate/osti-2583708/runs/sweep/log.s{1..10}` | ~2 KB each | SPPARKS stdout logs |

## Local mirror in this report dir
| Path | Notes |
|---|---|
| `paper.pdf` | 1.3 MB OSTI PDF |
| `work/spparks-resv/` | Shallow clone of `resveratrol` branch |
| `work/spparks-nonorth/` | Shallow clone of `nonorth` branch |
| `work/paper_layout.txt`, `work/paper_plain.txt` | pdftotext output |
| `work/runs/in.hcp_test` | Smoke input file |
| `work/runs/in.paper_scale` | 48×16×24 KMC input |
| `work/runs/in.sweep_seed1` | Sweep input (representative) |
| `work/runs/sweep.sh` | 10-seed driver |
| `extraction/marker.md` | Marker-flavored text extraction (from pdftotext + IOP HTML) |
| `extraction/nougat.mmd` | Nougat-flavored LaTeX extraction |
| `report/evidence/dump.sweep_seed1.txt` | Seed-1 KMC dump (evidence copy) |
| `report/evidence/log.sweep_seed1.txt` | Seed-1 KMC log (evidence copy) |
| `report/evidence/aspect_ratio_sweep.json` | Aspect-ratio measurements (10 seeds) |

## Public-artifact provenance summary
- **Available**: OSTI PDF (open), publisher HTML (paywalled but scraped for structure), two GitHub feature branches (`nonorth`, `resveratrol`).
- **Missing / blocked**: (a) publisher supplementary bundle (captcha-blocked); (b) the disphere/resv extensions the paper says are on the `resveratrol` branch — these are simply not in the repo; (c) the 74-entry DFT binding-energy library; (d) the FHI-aims input scripts.
