# Workflow & Effort Estimate — Thakur 2022 (T. pyogenes) Replication

## 1. Workflow (chronological)

### Pass-1 (May 2026)
1. **Paper acquisition** — DOI `10.3390/antibiotics12010024`, MDPI Antibiotics 2023 12(1):24. Open-access PDF (`paper/thakur2022.pdf`).
2. **Genome pull** — 19 T. pyogenes assemblies from NCBI Assembly (accessions in `data/genomes.tsv`). Downloaded via `datasets` CLI.
3. **Annotation** — Prokka 1.14.6 per strain, output to `analysis/prokka/<strain>/`.
4. **Pan-genome** — Roary 3.13.0 on Prokka GFFs → `analysis/roary/`. FastTree core-genome phylogeny.
5. **ANI** — FastANI 1.34 all-vs-all → `analysis/ani/`.
6. **Virulence factors** — BLASTN of `plo` and `nanH` references vs. all 19 assemblies.
7. **AMR** — `abricate` with the CARD database.
8. **Pass-1 report** — verdict REPLICATED (11/15 verified, 4/15 partial).

### Pass-2 (June 2026, coverage lift)
9. **Re-read paper** — extracted 16 additional testable claims from Table 1 and §3.6–3.10 text.
10. **Full Table-1 comparison** — `code/repass/01_table1_full_compare.py` parses Prokka `.txt` summaries for rRNA/tRNA/tmRNA/repeat_region and compares to the paper's Table 1 transcription. 76/76 cells match exactly.
11. **Full VF panel** — `code/repass/02_full_vf_blast.py` BLASTNs all 8 paper-listed VFs (plo, nanH, nanP, cbpA-as-cna, fimA/C/E/J proxied by 4 TP6375 fimbrial subunit CDS) at ≥ 60% pid / ≥ 30% qcov.
12. **PhiSpy prophage** — `code/repass/03_phispy_prophage.sh` runs PhiSpy 5.0.10 on each Prokka GenBank (free substitute for the paper's PHASTER web tool).
13. **IslandPath-DIMOB genomic islands** — `code/repass/04_islandpath_gi.sh` (single-tool free substitute for the paper's IslandViewer4 4-tool ensemble).
14. **CAZyme proxy** — `code/repass/05_cazyme_pfam_proxy.py` regex-matches Prokka product strings for carbohydrate keywords (coarse proxy for eggNOG COG-G).
15. **Extended AMR sub-claims** — `code/repass/06_amr_extended_compare.py` tests tet(W*) carriage, ermX carriage, no-ARG strain identity, top-3 carrier identity.
16. **Pass-2 report** — verdict REPLICATED (lifted; 21/31 verified, 6/31 partial, 4/31 not-reproducible-with-free-tools, 0/31 contradicted).

### Backfill pass (July 2026, this pass)
17. **Marker extraction** — `extraction/marker.md` (136 KB) already present from the central Eagle corpus.
18. **Nougat extraction** — `extraction/nougat.mmd` header-only (897 B) — pending central Nougat parse (GPU-only tool; deferred to corpus sweep).
19. **Report artifacts** — LaTeX report (`REPORT.tex`), open-questions JSON (`open_questions.json`), workflow narrative (this file), artifact inventory (`artifacts_summary.md`), failure analysis (`failure_analysis.md`).

## 2. Tools + Codes + Versions

| Tool | Version | Purpose | License |
|---|---|---|---|
| Prokka | 1.14.6 | Gene prediction + annotation | GPL v2 |
| Roary | 3.13.0 | Pan-genome (Pass-1 substitute for EDGAR 3.0) | GPL v3 |
| FastANI | 1.34 | ANI (Pass-1 substitute for EDGAR ANI) | Apache 2.0 |
| FastTree | 2.1.11 | Core-genome phylogeny | GPL v2 |
| BLASTN | 2.15.0 | VF panel + custom searches | Public domain |
| abricate | 1.0.1 | AMR (substitute for CARD/RGI) | GPL v3 |
| CARD (abricate DB) | 3.2.6 | AMR reference | CC BY-SA |
| PhiSpy | 5.0.10 | Prophage (free substitute for PHASTER) | GPL v3 |
| IslandPath-DIMOB | 1.0.6 | Genomic islands (partial substitute for IslandViewer4) | GPL v3 |
| pdftotext (poppler) | 24.02.0 | PDF → marker.md (fallback path) | GPL v2 |
| Marker | (Eagle corpus) | Primary PDF extraction | GPL v3 |
| Nougat | (pending) | Formula/table extraction | MIT |
| pdflatex (TeX Live 2026) | 3.141592653 | REPORT.tex compilation | LPPL |
| Python | 3.11 (bioconda `tpyo` env) | Comparison scripts | PSF |

**Repo-local custom code** (`code/repass/*.py|*.sh`, 6 scripts, ~450 total LOC).

**External refs used verbatim** (no bespoke code):
- NCBI Assembly (genomes)
- CARD database v3.2.6 (AMR)
- VFDB references (VF FASTAs)

## 3. Effort Estimate

| Category | Estimate |
|---|---|
| **Wall-clock** — Pass-1 (assembly, annotation, initial claim tests) | ~6 h interactive |
| **Wall-clock** — Pass-2 (coverage lift, 6 new scripts, PhiSpy + DIMOB runs) | ~4 h interactive |
| **Wall-clock** — Backfill (this pass, 5 report artifacts) | ~30 min autonomous |
| **Compute** — Prokka × 19 strains | ~40 min single-CPU total |
| **Compute** — Roary + FastTree | ~15 min single-CPU |
| **Compute** — FastANI all-vs-all | ~3 min single-CPU |
| **Compute** — PhiSpy × 19 | ~10 min single-CPU |
| **Compute** — IslandPath-DIMOB × 19 | ~10 min single-CPU |
| **Compute** — BLASTN VF panel + AMR | ~5 min single-CPU |
| **Peak RAM** | < 4 GB (largest step: Roary on 19 GFFs) |
| **Disk footprint** (analysis/ + results/) | ~2.1 GB |
| **Custom lines-of-code** | ~450 LOC (6 repass scripts + earlier Pass-1 helpers) |
| **Agent turns** | Pass-1: ~40; Pass-2: ~25; Backfill: ~10 |
| **Claim count** | 31 tested (15 Pass-1 + 16 Pass-2) |

## 4. Compute Host

All local: MacBook + external SSD, bioconda `tpyo` env at `/usr/local/Caskroom/miniforge/base/envs/tpyo`. No HPC, no GPU. No paid API calls (Argo `localhost:44497` was not required for any analytical step; PDF parsing done with free tools).

## 5. Reproducibility Notes

- Every result cell in REPORT.md is traceable to a file under `results/` or `results/repass/`.
- Every command line is captured in `code/repass/*.sh` or committed script headers.
- Substitute tools (Roary↔EDGAR, PhiSpy↔PHASTER, IslandPath-DIMOB↔IslandViewer4, abricate↔RGI) are **named + versioned + rationale-documented**, per the standing honesty rule.
- Missing-artifact registry maintained in REPORT.md §5 (6 items) so a future paid-tool pass can close specific gaps.
