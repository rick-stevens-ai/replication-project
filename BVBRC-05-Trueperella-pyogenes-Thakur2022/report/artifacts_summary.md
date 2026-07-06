# Artifact Inventory & Trace — Thakur 2022 (T. pyogenes)

Root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022/`

## 1. Paper + Extraction (8-artifact items 1–3)

| # | Path | Kind | Notes |
|---|---|---|---|
| 1 | `paper.pdf` → `paper/thakur2022.pdf` | PDF | MDPI Antibiotics 2023, 12(1):24. DOI 10.3390/antibiotics12010024. Open-access. |
| 2 | `extraction/marker.md` | Markdown | 136,127 B — full body extracted via Marker (Eagle central corpus). |
| 3 | `extraction/nougat.mmd` | Nougat MMD | 897 B header-only — pending central Nougat re-parse (Nougat is GPU-only). Contains sha256 placeholder for later corpus sweep. |

## 2. Report (8-artifact items 4–8)

| # | Path | Kind | Notes |
|---|---|---|---|
| 4 | `report/REPORT.tex` (+ `report/REPORT.pdf` if compiled) | LaTeX | Detailed per-claim, per-critique, per-open-question. |
| 4a | `report/REPORT.md` | Markdown | Pass-2 (coverage-lift) report (primary human-readable). |
| 4b | `report/REPORT.pass1.md` | Markdown | Pass-1 report preserved verbatim. |
| 5 | `report/open_questions.json` | JSON | 5 heavy-duty open questions with basis + next_steps. |
| 6 | `report/workflow.md` | Markdown | Workflow narrative + tools + effort estimate. |
| 7 | `report/artifacts_summary.md` | Markdown | This file. |
| 8 | `report/failure_analysis.md` | Markdown | Honest failure + evidence-strength critique. |

## 3. Genome Data (input)

- `data/genomes.tsv` — 19 strains × (accession, host, geography). All from NCBI Assembly.
- Assemblies live under `data/assemblies/<strain>/<strain>.fna` (not tracked in Git; ~450 MB total).
- Standard NCBI accessions (illustrative): TP6375 = NZ_CP007519.1, TP1 = NZ_CP033902.1, Bu5 = draft (Indian buffalo, first Indian isolate).

## 4. Analysis Directories

| Path | Producer | Purpose |
|---|---|---|
| `analysis/prokka/<strain>/` | Prokka 1.14.6 | Per-strain gene predictions (GFF, GBK, TXT summaries). |
| `analysis/roary/` | Roary 3.13.0 | Pan-genome matrix, core alignment, gene presence/absence. |
| `analysis/ani/` | FastANI 1.34 | All-vs-all ANI matrix. |
| `analysis/phylogeny/` | FastTree | Core-genome ML tree (Newick). |
| `analysis/virulence/` | BLASTN | VF search inputs + outputs. |
| `analysis/virulence/ref_cna.fasta` | Custom (Pass-2) | TP6375-derived cna reference (cbpA proxy). |
| `analysis/amr/` | abricate | ARG hits per strain. |

## 5. Code (custom)

| Script | Purpose | LOC (approx) |
|---|---|---|
| `code/pass1/*` | Assembly download, Prokka wrapper, Roary post-processing, ANI matrix parse, VF/AMR summarizers | ~250 |
| `code/repass/01_table1_full_compare.py` | Table-1 (rRNA/tRNA/tmRNA/RR) reproduction | ~80 |
| `code/repass/02_full_vf_blast.py` | Full 8-VF BLASTN panel + stringency filter | ~110 |
| `code/repass/03_phispy_prophage.sh` | PhiSpy run + summary aggregation | ~40 |
| `code/repass/04_islandpath_gi.sh` | IslandPath-DIMOB run + summary | ~40 |
| `code/repass/05_cazyme_pfam_proxy.py` | Prokka-product keyword CAZyme proxy | ~50 |
| `code/repass/06_amr_extended_compare.py` | tet(W*), ermX, no-ARG, top-3 sub-claim tests | ~130 |

## 6. Results / Traces

### Pass-1
- `results/pass1/genome_stats.tsv` — bases/GC/CDS per strain (claim #1–3).
- `results/pass1/roary_summary.json` — pan/core/singleton counts (claim #4–6).
- `results/pass1/heaps_gamma.json` — γ = 0.247 (claim #7).
- `results/pass1/ani_matrix.tsv` — pairwise ANI (claim #9).
- `results/pass1/vf_plo_nanH.tsv` — plo/nanH presence (claim #10, 11).
- `results/pass1/amr_counts.tsv` — total ARG per strain (claim #12).
- `results/pass1/phylogeny.newick` — 3-clade tree (claim #13–15).

### Pass-2
- `results/repass/table1_full_compare.tsv` — 76/76 cells (claim #16–19).
- `results/repass/vf_full_panel.tsv` + `vf_full_summary.json` — 8-VF matrix (claim #20–23).
- `results/repass/amr_extended_compare.tsv` — tet(W*)/ermX/no-ARG/top-3 flags (claim #24–27).
- `results/repass/phispy/summary.tsv` + per-strain `prophage_coordinates.tsv` (claim #28–30).
- `results/repass/islandpath/summary.tsv` + per-strain `<strain>_gis.txt` (claim #31).
- `results/repass/cazyme_proxy_counts.tsv` — carbohydrate-CDS proxy.

## 7. External Reference Data

| Reference | Source | Version / DOI |
|---|---|---|
| CARD (abricate DB bundled) | McMaster CARD | 3.2.6 |
| VFDB reference FASTAs (plo, nanH, nanP, cna) | VFDB core dataset | Downloaded 2026-05 |
| Prokka HMM/DB set | Prokka bundle | 1.14.6 default |
| PhiSpy training set | PhiSpy bundle | 5.0.10 default |

## 8. Provenance & Sizes

| Artifact | Size | Checksum (SHA-256, first 12) |
|---|---|---|
| `paper.pdf` → `paper/thakur2022.pdf` | (see `ls -la paper/`) | (recompute on demand) |
| `extraction/marker.md` | 136,127 B | (present; not re-hashed for backfill) |
| `extraction/nougat.mmd` | 897 B (header only) | (placeholder) |
| `report/REPORT.md` | 22,497 B | (Pass-2) |
| `report/REPORT.pass1.md` | 12,153 B | (Pass-1 preserved) |
| `PARSER_PROVENANCE.md` | 2,879 B | (Pass-2 parse provenance) |
| `PROGRESS.md` | 3,290 B | (agent notes) |

Checksums can be recomputed with `find . -type f -not -path './.git/*' -exec sha256sum {} + > CHECKSUMS.txt` when a formal snapshot is needed.

## 9. Missing / Deferred Artifacts (registered)

Per REPORT.md §5:

1. **SIGI-HMM** standalone binary — for IslandViewer4 GI ensemble replication.
2. **Islander** web-service DB — for IslandViewer4 GI ensemble replication.
3. **PHASTER** offline standalone or curated phage DB — for incomplete-prophage comparison.
4. **eggNOG-mapper v2 + eggnog.db (~50 GB)** — for the 139-CDS core-genome COG-G claim.
5. **Bisinotto 2016 (ref [13])** fim gene accession numbers — for exact paper-name fim mapping.
6. **CARD/RGI** strict+perfect category, local install — for the exact "40 ARGs" total.
7. **Nougat MMD** re-parse — pending central Nougat corpus sweep (GPU-required).
