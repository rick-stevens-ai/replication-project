# Workflow — BVBRC-42 Bosma et al. (2016) *B. smithii* DSM 4216ᵀ genome replication

Analyst: Ollie (OpenClaw AI). Date: 2026-07-01. Verdict: PARTIAL (strong, independently confirmed 2026-07-03).

All steps use free / public endpoints. No paid APIs. All commands rerunnable on a local laptop.

## 0. Inputs (pinned)
- Paper: Bosma et al., *Standards in Genomic Sciences* 11:52 (2016), DOI 10.1186/s40793-016-0172-8, PMC PMC4995803 (CC BY 4.0 open access).
- Genome assembly: `GCA_001050115.1` (2015 GenBank submission, RAST-era annotation — matches paper era) and `GCF_001050115.1` (2026 RefSeq PGAP re-annotation — used for annotation-drift cross-check).
- Replicons: chromosome `CP012024.1` (3,368,778 bp) + plasmid `CP012025.1` (12,514 bp).
- BioProject `PRJNA258357`, BioSample `SAMN03246763`, locus tag `BSM4216`.

## 1. Paper full-text ingest
```
GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4995803/fullTextXML
  -> work/paper_fulltext.xml
```
Parse JATS XML to extract Tables 1–6 and the central-metabolism narrative section directly (no PDF OCR needed).

## 2. Genome download
```
datasets download genome accession GCA_001050115.1 --include genome,protein,gff3,rna,cds
datasets download genome accession GCF_001050115.1 --include genome,protein,gff3,rna,cds
```
Unpack to `work/genome/GCA_001050115.1/` and `work/genome/GCF_001050115.1/`. Deterministic, no auth.

## 3. Genome statistics (tests C2–C5)
Pure-Python `work/genome_stats.py`:
- Per-replicon length + GC from the genome FASTA.
- Feature counts (CDS, tRNA, rRNA, pseudogene, gene biotypes, coding bp) from `genomic.gff`.
- Output: `evidence/genome_stats.json`.

Compare vs paper Tables 3/4:
- Total size EXACT (3,381,292).
- Chromosome EXACT (3,368,778).
- Plasmid EXACT (12,514).
- GC 40.75% (rounds to 40.8%).
- CDS 3,619 vs 3,627 (within 0.2%).
- rRNA 33 EXACT (11 operons × 3).

## 4. Metabolic gene name-scan (orthogonal to tblastn)
`work/func_scan.py` greps GFF `product=`, `gene=`, `Note=` fields across BOTH GCA (2015) and GCF (2026 RefSeq) annotations for the Fig. 4 gene panel: `phosphotransacetylase`, `phosphate acetyltransferase`, `acetate kinase`, `pyruvate formate`, `pyruvate decarboxylase`, `pyruvate:ferredoxin`, `L-lactate dehydrogenase`, `pyruvate dehydrogenase`. Result: zero hits in either annotation for the ABSENT panel; positive hits for Ldh + PDH.

Output: `evidence/func_scan.json`.

## 5. Rigorous present/absent tblastn (tests C7–C10)
```
python work/fetch_refs.py            # 8 curated UniProt refs -> blast/refs.faa
makeblastdb -in <genome.fna> -dbtype nucl -out work/blast/bsmithii_db
tblastn -query work/blast/refs.faa -db work/blast/bsmithii_db \
        -evalue 10 -outfmt 6 -out work/blast/refs_tblastn.tsv
```
Presence rule: `pident ≥ 40 AND qcov ≥ 70 AND e ≤ 1e-20`. Positive controls (Ldh, PdhA) score deep unambiguous orthologs; negatives (pta, ackA, PflB, Pdc, PFOR) fall well below threshold.

Output: `evidence/metabolic_tblastn.tsv`.

## 6. COG functional-category re-run (tests C6)
```
COGclassifier -i <protein.faa> -o work/cog_out
```
Auto-downloads NCBI COG/CDD DB; runs `rpsblast`; assigns COG categories to all 3,619 GCA proteins in ~31 s. Compare paper Table 5 vs re-computed distribution:
- Pearson r = 0.615 (all 22 categories) → 0.912 (excl. D, R, S).
- Spearman ρ = 0.660 → 0.919.

Explained residuals in D (COGclassifier-v2 over-assignment quirk) and R/S (DB-era drift 2015 IMG/RAST → 2026 NCBI COG; R shrank 382→133, S 236→98).

Outputs: `evidence/cog_compare.json`, `evidence/cog_count.tsv`, `evidence/cog_count_barchart.png`.

## 7. LLM-judge (independent scoring)
```
POST http://127.0.0.1:44497/v1/chat/completions
  model: argo:gpt-5.2   temperature: 0   response_format: JSON
```
Free Argo proxy (key=stevens). Structured JSON verdict: coverage 8/10, agreement 9/10, verdict PARTIAL.

Output: `work/judge_result.json`.

## 8. Independent reproduction (2026-07-03)
Fresh subagent, no reuse of original scripts:
1. Fresh NCBI Datasets download of both GCA + GCF into `evidence/independent_reproduction/downloads/`.
2. Own `indep_genome_stats.py` (pure stdlib) — does NOT read the original `genome_stats.py`.
3. Own `indep_fetch_refs.py` — re-downloads 7 UniProt enzymes fresh.
4. Fresh `makeblastdb` on newly-downloaded genome + fresh `tblastn -evalue 10`.
5. Orthogonal name-scan (`grep`) on GCA + GCF GFFs.

Result: **15/15 checkable metrics MATCH, 0 MISMATCH**. tblastn numbers bit-identical (BLAST is deterministic on same query+DB); name-scan zero-hits decade-independent (2015 GCA + 2026 GCF).

Artifacts: `report/evidence/independent_reproduction/{downloads/, code/, indep_summary.json, comparison.md, tool_versions.txt}`.

## 9. Not attempted (out of scope, honestly reported in GENUINE CRITIQUE)
- RAST manual-curation pipeline (C11) — paper-specific, not reproducible without paper's curator notes.
- antiSMASH secondary-metabolite clusters.
- CRISPR-finder CRISPR/cas inventory.
- InterPro domainome EC-rescue.
- Table 6 comparative-genomics against 14 other Bacillus/Geobacillus genomes.
- Fig. 4 manual metabolism-map redraw.
- Wet-lab phenotype validation (55 °C growth, L-lactate production, sporulation).

## 10. Tool versions
- NCBI `datasets` CLI (local install).
- BLAST+ `makeblastdb` / `tblastn` — /usr/local/bin.
- `COGclassifier` v2 (pip venv, auto-fetches NCBI COG/CDD DB).
- Python 3.
- Argo proxy `argo:gpt-5.2` for LLM-judge.
Detailed versions: `report/evidence/independent_reproduction/tool_versions.txt`.

## 11. Compute budget
- ~2 min CPU (genome stats + 8-query tblastn) + 31 s COGclassifier + fresh redownloads for independent reproduction.
- Local laptop (CherryRd). Zero paid endpoints.
