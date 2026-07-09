# Workflow — BVBRC-114 (Khajanchi et al. 2017)

## Full workflow narrative
1. **Paper acquisition.** Fetched PMID 28768482 (BMC Genomics, CC BY 4.0) via the BMC track/PDF endpoint (PMC PDF gate now returns an HTML redirect). pdftotext-layout extraction parsed Table 1 to recover the 7 focal-strain WGS accessions and BioProject PRJNA312617.
2. **Assembly retrieval on uicgpu.** Two-path retrieval: (a) `datasets download genome` filtered to PRJNA312617 for 4/7 (SE163A, SE696A, SE710A, SE819); (b) direct FTP fetch of `GCF_001729025/035/045.1_ASM172902-4v1_genomic.fna.gz` for SE397/SE452/SE478 (the three whose WGS master accessions were not directly resolvable via `datasets search`). Total: 7 complete or draft assemblies (4.9–5.4 Mb, 230–856 contigs).
3. **In-silico serotyping (C2).** SeqSero2 v1.3+ in k-mer mode (`-m k -t 4 -i <asm> -p 8`) per assembly. Reproduced paper Table 1: 6 Typhimurium + 1 Heidelberg (SE819).
4. **7-gene MLST orthogonal check.** `mlst` v2.35.0 with `salmonella` PubMLST scheme. 6 Typhimurium → identical ST19, 1 Heidelberg (SE819) → ST15. Corroborates SeqSero + supports monophyletic-6 hypothesis.
5. **PlasmidFinder-style rep-gene detection (C4).** Cloned CGE PlasmidFinder DB (488 rep sequences). `makeblastdb -dbtype nucl` per assembly. `blastn -evalue 1e-20 -perc_identity 80` with post-filter `coverage ≥ 60%`. **6/6 Typhimurium** hit `IncFIB(AP001918)_1` at 98.09% ID, full 682/682 coverage. **SE819** hit no IncFIB rep. Extra Inc replicons (IncFIA, IncFII variants, IncA, IncX4, IncI1, IncC, ColRNAI, ColpVC) also detected, consistent with the multi-replicon nature described in the paper.
6. **Sit + aerobactin operon detection (C4, C5).** Extracted sitABCD + iucABC + iutA + iroB CDS translations from CP001122.1 (pCVM29188_146 IncFIB(K)) via GenBank CDS parsing. tblastn each query into each of the 7 genomes. Rule: gene PRESENT iff best-hit %identity ≥ 90 AND alignment coverage ≥ 90%. **All 6 Typhimurium strains carry the complete sitA-D + iucA-C at 99.65–100% AA identity**, each colocalised on a single assembly contig (14–23 kb, distinct from the IncFIB rep contig — consistent with the plasmid being fragmented across ~3 contigs per draft assembly at ~140 kb). **SE819** carries the chromosomal *sit* homologue at 68–86% ID (paper explicitly notes chromosome + plasmid encode distinct sit loci) and NO detectable *iuc* — matching the paper's SE819-as-IncFIB-deficient-recipient design.
7. **SNP/phylogenetic subclade check (C3).** `mash sketch -k 21 -s 1000` on 7 focal + 5 reference genomes, all-vs-all `mash dist`, Biopython `DistanceTreeConstructor.nj`. 5 Typhimurium strains form a tight subclade (mean intra-cluster d = 1.5–1.8×10⁻³); SE397 has 2.5× higher mean intra-Typhimurium distance (d = 4.29×10⁻³) and branches separately in the NJ tree — matches the paper's 5+1 topology (paper Fig 1b). Mash is lower-resolution than the paper's core-genome SNP alignment, so this replication reproduces the *direction* of the finding (5 tight + 1 outlier) but not the specific outgroup attachment.
8. **Wet-lab claims not testable.** C6 (Caco-2 persistence of SE819::IncFIB transconjugant vs SE819 recipient) and C7 (qRT-PCR of sit/iuc genes in iron-rich vs iron-depleted media) require live-culture manipulation and RNA extraction — flagged "not testable in silico", not "failed".

## Enumerated tools + versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.8.10 (uicgpu system) | Scripts |
| BLAST+ | 2.15.0 (`bvbrc56` env) | makeblastdb, blastn, tblastn |
| NCBI E-utilities (esearch/efetch) | 22.4 | Reference genome/protein retrieval |
| NCBI Datasets CLI | 16.x (`bvbrc56` env) | Assembly retrieval |
| SeqSero2 | v1.3+ (`amr` micromamba env) | Serotype prediction (k-mer mode) |
| mlst | 2.35.0 (`amr` env) | 7-gene MLST |
| mash | 2.3 (`amr` env) | Pairwise distance |
| amrfinder | latest (`amr` env) | Available but not applied (paper didn't focus on AMR beyond CFSAN AMR calls) |
| Biopython | 1.87 | GenBank CDS parsing, NJ tree |
| pdftotext (poppler) | latest | Paper text extraction fallback |
| PlasmidFinder DB | git HEAD 2026-07-05 | 488 rep sequences |
| curl / rsync / ssh | latest | Transport |
| Argo proxy (localhost:44497) | live | LLM judge (argo:claude-opus-4.7) |

## Scripts / codes written (this replication)
- `fetch2.sh` (32 LOC) — datasets-based assembly retrieval, 4/7 resolved
- `fetch4.sh` (37 LOC) — direct-FTP fallback for the other 3
- `analyze2.sh` (35 LOC) — SeqSero2 + mlst driver
- `plasmid.sh` (53 LOC) — PlasmidFinder DB clone + blastn matrix
- `iron2.sh`/`iron3.sh` (~120 LOC combined) — CDS extraction + tblastn iron operon matrix
- `phylo.sh` (~130 LOC) — reference fetch + mash + NJ tree
- Total: ~410 LOC + inline Python (~150 LOC embedded).

## Effort estimate
- **Wall clock:** ~30 min (12:10–12:40 CDT, 2026-07-05).
- **Compute:** All work on uicgpu (single AMD64 core per BLAST job; no GPU used — bioinformatic BLAST/mash operations are CPU-bound and fit comfortably on uicgpu without contending with GPU jobs).
- **Total core-seconds:** ~600 s (14 blastn + 63 tblastn hits, 7 SeqSero2 k-mer runs, 12-genome mash sketch).
- **Human/agent turns:** ~40 (Ollie subagent turns).
- **Data volume pulled:** ~35 MB assemblies + PlasmidFinder DB clone (~2 MB) + 5 reference genomes (~24 MB).
- **LLM inference:** 1 judge call to Argo Opus (free); ~2k tokens.
