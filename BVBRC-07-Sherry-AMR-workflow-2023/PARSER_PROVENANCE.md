# PARSER_PROVENANCE.md — Re-pass 2026-06-23

## Sources Parsed in This Re-pass
Goal: lift COVERAGE from 7 → ≥8 by attempting previously-skipped claims C15 (LOD) and C16 (precision/repeatability) via computational read simulation.

### Source artifacts (already on disk from pass 1)
| File | Bytes | Role |
|---|---|---|
| `paper/supplementary.pdf` | 1,656,596 | Methods + Tables S1–S15 (LOD/precision sections) |
| `paper/source_data.xlsx` | 111,939 | Per-figure source data (Fig 1–6) |
| `paper/supp_data1.xlsx` | 22,829 | Allele list (415 entries) |
| `paper/supp_data2.xlsx` | 313,429 | Salmonella phenotype calls |
| `paper/supp_data3.xlsx` | — | Synthetic per-allele results |
| `data/assemblies/*.fna` (74) | — | NCBI Assembly reference genomes |
| `results/amrfinder/*.tsv` (60) | — | Pass-1 AMRFinderPlus 4.2.7 calls (truth set for re-pass) |

### New parsers / tools used in re-pass
| Tool | Version | Source | Purpose |
|---|---|---|---|
| `wgsim` | 0.3.2 | /usr/local/bin (Heng Li) | Simulate paired-end Illumina reads at controlled coverage |
| `spades.py` | already-installed system binary | /usr/local/bin | De novo assembly of simulated reads (`--only-assembler --isolate`) |
| `amrfinder` | 4.2.7 (DB 2026-03-24.1) | miniforge env `amrfinder` | AMR gene calling — same version/DB as pass 1 for direct comparability |
| Python 3 `openpyxl` | — | (system) | Read `.xlsx` source data when needed for cross-check |

### Reference truth definition for LOD/precision tests
For each test genome, the **pass-1 AMRFinderPlus call set on the reference assembly** is treated as ground truth (`results/amrfinder/<acc>.tsv`). LOD = fraction of those AMR gene calls recovered after simulating reads at coverage X, assembling, and re-calling with the identical AMRFinderPlus version + DB.

This is a **computational LOD**, not a wet-lab LOD; the paper's C15 (40X–150X = 99.9%) is the wet-lab claim using real MiSeq reads downsampled. Our replication tests whether AMRFinder gene-recall is stable across the same coverage range when applied to wgsim-simulated reads — i.e. the *informatic* component of the LOD claim.

Likewise C16 (precision/repeatability) in the paper is wet-lab inter-replicate. Our replication tests **computational precision**: repeat the simulate→assemble→AMRFinder pipeline at fixed coverage with different RNG seeds and measure call-set agreement.

### Selected genomes for re-pass (chosen for size + AMR richness)
| Accession | Size | Pass-1 AMR gene hits | Notes |
|---|---|---|---|
| `GCA_000145595.1` | 2.96 MB | 43 | S. aureus JKD6008 — small, mecA-positive |
| `GCA_000814165.3` | 4.11 MB | 10 | mid-size Enterobacterales |
| `GCA_000284595.1` | 4.83 MB | 7 | Enterobacterales — multiple bla genes |

### Coverages tested (matches paper Fig 4 / Table S6 range)
40X, 80X, 120X, 150X. Read length 150 bp paired-end (matches MiSeq v3 used in paper). Mean fragment 500 bp.

### Replicate design for C16
At 80X coverage (mid-range, well above LOD floor), 3 wgsim seeds (1, 2, 3) per genome → run identical pipeline → measure pairwise gene-set Jaccard.

### Parser fidelity notes
- Re-pass uses the SAME AMRFinderPlus version (4.2.7) and SAME DB (2026-03-24.1) as pass 1, so newer-DB drift is controlled out: any deltas seen reflect coverage/assembly effects, not DB churn.
- `wgsim` defaults: base error 2%, mutation rate 0.1% — these are higher than MiSeq real-world (~0.5% error) but represent a stress test; if AMRFinder recall holds here, it should hold on cleaner data.
- SPAdes invoked with `--only-assembler --isolate -t 4` — skips error correction (BayesHammer) to keep wall-clock tractable on iMac; this is the most aggressive (least friendly to LOD) setting.

### Provenance script
`code/repass/run_lod_precision.sh` is the single runnable script that drives the entire re-pass. Outputs land in `results/repass/`. Re-runnable end-to-end.
