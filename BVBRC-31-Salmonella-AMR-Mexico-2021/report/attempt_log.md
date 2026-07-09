# Attempt Log — BVBRC-31 (Salmonella AMR Mexico 2021)

**Analyst:** Ollie (OpenClaw subagent), Replication Wave 2026-07-01. Heavy compute on uicgpu (8×A100, 255 cores).

## Chronology

1. **Dedup** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i salmonella` → none. Clear to proceed.
2. **Read brief + exemplar** (BVBRC-17 E. coli report) to mirror structure.
3. **Paper metadata (Europe PMC)** — resolved PMID 33951039 → DOI 10.1371/journal.pone.0243681, PMCID PMC8099073, PLoS ONE 2021, open access (CC0). Pulled abstract + full-text XML (297 KB).
4. **Accession discovery** — full text names BioProject **PRJNA480281** and points to S1 File for per-isolate accessions. Downloaded supplementary bundle (`supplementaryFiles` zip). S1 (`s001.xlsx`) = the 77 study isolates with BioSample + SRR + serovar + isolation source + host + assembly stats. S2 = the 2400 public Mexico NTS genomes; S3 = Typhimurium MX set.
5. **Parsed S1** → 77 isolates: 48 Lymph nodes + 29 Ground beef; serovars Anatum 23, Reading 22, Typhimurium 10, London 9, Kentucky 6, Fresno 4, others. **Exactly matches paper.**
6. **BioSample → assembly mapping** — queried NCBI Datasets v2alpha `genome/biosample/<SAMN>/dataset_report` for all 77. **68/77 had a GenBank (GCA) assembly**; 9 (mostly a newer Reading batch SAMN158727xx + 2 others) had no assembly at query time → analyzed the 68.
7. **uicgpu setup** — no bioinformatics tools present; bootstrapped micromamba 2.8.1, created env `amr` with `ncbi-datasets-cli 18.32.0`, `ncbi-amrfinderplus 3.12.8`, `seqsero2 1.3.2`, `mlst 2.35.0` (bioconda). `amrfinder -u` → DB 2024-07-22.1.
8. **Genome download** — `datasets download genome accession --inputfile assembly_list.txt --include genome` → 68 FASTAs (97 MB), flattened to `assemblies/<GCA>.fna`.
9. **AMRFinderPlus** — `amrfinder -n <fna> --organism Salmonella --plus` for each (16-way parallel). 68/68 completed.
10. **SeqSero2** (`-m k -t 4`, kmer/assembly) 68/68; **MLST** (`mlst assemblies/*.fna`) 68/68.
11. **rsync results back**, ran local `analyze.py` (Python venv, scipy).
12. **Bug fixes:** (a) initial `has_gene` matcher failed on `tet(G)` vs `tetG` formatting → normalized symbols (strip parentheses); after fix, SGI1 penta-set correctly detected in 6/7 Typhimurium. (b) Confirmed AMRFinder emitted **zero curated POINT mutations** across all 68 (mutation search ran per logs — "AMRFinder translated nucleotide and mutation search" — but no resistance-conferring SNPs met the curated catalog); this is a real tool/catalog difference from the paper's custom mutation calling.
13. **LLM judge** — Argo `argo:gpt-5.2` (free, localhost:44497). argo:claude-opus-4.8 also worked but used gpt-5.2 to avoid any proxy parse risk. Verdict PARTIAL, coverage 7/10, agreement 5/10.

## What worked
- NCBI assemblies existed for 88% of study isolates → skipped de-novo assembly; ran the paper's exact genotyping tools on the paper's exact genomes.
- Serovar (67/68), MDR% (23.5 vs 26), Typhimurium MDR fraction (37.5 vs 40), and the SGI1 penta gene set (6/7) all reproduced.

## What didn't
- 9/77 isolates lacked assemblies (would need de-novo assembly from SRR reads to reach full 77 and recover the missing 3 Typhimurium → paper's 9/10).
- MDR-by-source significant in paper (χ²=12.0) but only directional on the 68-subset (GB 33.3% > LN 18.2%, χ²=1.98, p=0.16) — power lost from the 9 missing isolates + phenotype-vs-genotype MDR definition.
- Point mutations (QRDR gyrA/parE, ramR) not flagged by AMRFinder's curated Salmonella catalog; the paper's "100% QRDR mutations" reflects raw reference comparison, not curated resistance SNPs.
