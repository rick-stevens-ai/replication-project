# Attempt Log — BVBRC-26 (Vassallo et al. 2022 anti-phage defence)

Analyst: Ollie (OpenClaw subagent) · Date: 2026-07-01 (night wave push) · Host: CherryRd (+ NCBI/BV-BRC APIs)

## Chronology

1. **Read brief + exemplar.** WAVE_BRIEF_2026-07-01.md and BVBRC-17 REPORT.md set the output contract and "real replication only / free endpoints / LLM-judge" rules.
2. **Surveyed existing sibling dir** `36123438-Anti-phage-defense-Ecoli/`. Found prior work (NCBI-nr BLASTP conservation, 4.3/5) with useful inputs: 21 representative + 32 total defence-protein FASTAs, a partial (18-strain) BV-BRC source-strain map, and the paper supplementary xlsx. Copied FASTAs + xlsx as inputs; did NOT overwrite the sibling. Decided the BVBRC-26 value-add = a **real BV-BRC Genome-Group / Proteome-Comparison + MGE-context + CRISPR-context** replication over the FULL 71-strain panel (prior work only had 18).
3. **Fetched paper OA full text** (Europe PMC JATS XML, PMC9519451). Extracted core claims and exact numbers (71 strains, 21,149 gene clusters, 257→131→43 clones→21 systems, prophage/MGE/hotspot thesis, Gao-et-al comparison).
4. **Parsed supplementary tables** (openpyxl). Table S5 = full 71-strain source list with **GCA assembly accessions** (ground-truth corpus). Table S2 = per-system source strain + contig accession + CDS + coordinates. Table S4 = Gao et al. 2020 comparison (novelty).
5. **BV-BRC connectivity.** `patricbrc.org/api/genome` works and is fast; the `bv-brc.org` mirror + FTP + protein+fasta bulk export were slow/timeouts. First mapper (urllib, 40s timeouts + 3× retry) hung → killed. Rewrote with curl subprocess + `--max-time` (failure-log lesson: always bound network calls).
6. **C1 corpus mapping.** `map_bvbrc.py`: queried BV-BRC `genome` by `assembly_accession` for all 71 GCA accessions → **71/71 matched** to BV-BRC genome_ids.
7. **Proteome fetch.** BV-BRC protein-FASTA bulk endpoint timed out (60s+). Pivoted to **NCBI Datasets REST** (`PROT_FASTA` by GCA accession) — fast, reliable; these are the *same* assemblies BV-BRC indexes (identity link preserved by naming each proteome file by its BV-BRC genome_id). Downloaded **71/71 proteomes = 348,507 proteins**.
8. **C2/C3 Genome-Group Proteome Comparison.** `build_distribution.py`: combined all 71 proteomes (genome_id-prefixed headers) → `makeblastdb` → BLASTP the 21 representatives (e≤1e-5, max_target_seqs 2000). Presence tiers (homolog / ortholog / self). **21/21 systems self-hit (≥98%) in exactly their Table-S2 source strain**; distribution within the panel is sparse (mean 2.9/71, max 11), consistent with accessory MGE-borne genes.
9. **C4 MGE / hotspot context.** `mge_context.py`: BV-BRC `accession` field exactly matches Table S2 contig accessions (verified). Pulled ±20-gene windows around each system's coordinates and scanned neighbour products. **16/21 have MGE/prophage neighbours; 14/21 in multi-defence hotspots.**
10. **CRISPR pipeline / known-system context.** `crispr_survey.py`: CRISPR-Cas + RM annotated in 71/71 source genomes (canonical machinery ubiquitous) — contrasts with the novel PD systems annotated as hypothetical/DUF, supporting the novelty framing. (Caveat: BV-BRC returned dual RefSeq+PATRIC annotation sets, inflating CDS counts ~2×; presence signal unaffected.)
11. **C5 novelty.** From Table S4: **18/32 components absent from Gao et al. 2020**; the 14 matches mostly 26–49% id (majority <35%) — matches the paper's own "14 of 32, often <35%" statement.
12. **LLM-judge.** `llm_judge.py` via Argo proxy (`argo:gpt-o3`, free). Verdict **PARTIAL**, Coverage 8/10, Agreement 9/10.
13. **Assembled report/ + evidence/.**

## What worked
- BV-BRC `genome` + `genome_feature` JSON APIs (via patricbrc.org) — fast, exact accession matching.
- NCBI Datasets for proteome bytes (BV-BRC bulk FASTA export was the weak link).
- Exact Table-S2 coordinate windows made MGE-context reproduction clean.

## What failed / pivots
- BV-BRC `protein+fasta` bulk export + FTP mirror: timeouts → used NCBI Datasets instead (same assemblies).
- urllib without hard timeouts hung → curl subprocess with `--max-time`.
- CDS-count doubling from dual annotation sets (RefSeq+PATRIC) — noted, did not affect presence/absence conclusions.

## Not done (honest gap)
- Wet-lab functional selection (tab/phage challenge, MOI, adsorption) — no deposited raw reads (no SRA); not computationally reproducible.
- Full cross-phyla (bacterial-class) distribution — prior sibling did the NCBI-nr breadth; here we scoped to the 71-strain BV-BRC group + provenance + context.
