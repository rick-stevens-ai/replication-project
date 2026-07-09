# Workflow: Zheng et al. 2017 (BVBRC-58) Replication

**Paper:** Zheng B et al., *Sci. Rep.* 7:17885 (2017). PMID 29263349 / PMCID PMC5738369 / DOI 10.1038/s41598-017-18273-2.
**Set:** BVBRC-58 · **Wave:** night push 2026-07-01/02 · **Analyst:** Ollie · **Verdict:** PARTIAL (strong).

Free-only stack: NCBI efetch, Biopython, mlst, AMRFinderPlus, blastn+PlasmidFinder DB, Argo `gpt-5.2` (free LLM judge).

---

## 0. Substrate

Actual GenBank accessions from the paper: **CP021202 – CP021210** (2 chromosomes + 7 circular plasmids).

- EC1002 (ST405): CP021202 (chr), CP021203 (pEC1002-1), CP021204 (pEC1002-4), CP021205 (pEC1002-MCR), CP021206 (pEC1002-NDM).
- EC2474 (ST131): CP021207 (chr), CP021208 (pEC2474-3), CP021209 (pEC2474-MCR), CP021210 (pEC2474-NDM).

No wet-lab or raw-read reprocessing; the paper's central claims are verifiable on the deposited closed sequences.

---

## Step 1 — Paper full text

Fetch Europe PMC XML for PMC5738369.
- Output: `work/paper_fulltext.xml` (82 KB).
- Parse Table 1: accessions, sizes, GC%, MLST STs, per-replicon resistance genes, replicon types.

## Step 2 — Genome download (NCBI efetch, no auth)

For each accession `ACC` in {CP021202..CP021210}:

```
efetch.fcgi?db=nuccore&id=<ACC>&rettype=fasta  ->  work/genomes/<ACC>.fasta
```

- Also build per-strain concatenations: `strains/EC1002.fasta` (chr + 4 plasmids), `strains/EC2474.fasta` (chr + 3 plasmids).

## Step 3 — Genome statistics (Biopython 1.87)

Script: `work/genome_stats.py`.
- For each replicon: length (bp), GC%.
- Compare to paper Table 1 (Δbp, ΔGC).
- Output: `evidence/evidence_genome_stats.json`.

Tests C1 (accessions live) and C2 (sizes/GC match to 0–8 bp; GC ≤0.5%).

## Step 4 — MLST (mlst 2.35.0 on uicgpu, env `~/micromamba/envs/amr`)

Scheme: PubMLST `ecoli_achtman_4` (7 loci: adk, fumC, gyrB, icd, mdh, purA, recA).

```
mlst --scheme ecoli_achtman_4 strains/EC1002.fasta strains/EC2474.fasta
```

- Output: `evidence/mlst_results.tsv`.
- Expected per paper: EC1002 = ST405; EC2474 = ST131.
- Result: exact match on both STs and all 7 alleles per strain.

Tests C3.

## Step 5 — Acquired resistance (AMRFinderPlus 3.12.8, DB 2024-07-22.1)

```
amrfinder -n strains/<S>.fasta --organism Escherichia --plus -d <db>
```

- Outputs: `evidence/EC1002_amr.tsv`, `evidence/EC2474_amr.tsv`.
- Map each gene hit to its host contig via the `Contig id` column; join to plasmid names.
- Compare per-plasmid gene lists to paper Table 1 (which used ResFinder 2.1 / 2017).

Tests C4. Result: core resistance genes match on every plasmid; allele/nomenclature drift explained by 2017-ResFinder vs 2024-AMRFinderPlus database versioning.

## Step 6 — Plasmid replicon typing (PlasmidFinder DB + blastn)

- Download `enterobacteriales.fsa` (159 replicon references) from PlasmidFinder DB repo.
- `makeblastdb -dbtype nucl -in enterobacteriales.fsa`.
- `blastn -perc_identity 95 -query <plasmid>.fasta -db enterobacteriales -outfmt 6`.
- Filter: coverage ≥ 60% AND pident ≥ 95%.
- Output: `evidence/plasmidfinder_results.tsv`.

Tests C5. Result: 7/7 plasmids typed to expected Inc-family (IncA/C2 accepted as modern IncC rename; IncF refined to IncFII).

## Step 7 — Central conclusion (C6) — separate-plasmid check

Cross-reference AMRFinderPlus contigs carrying `mcr-1.1` with contigs carrying `blaNDM-1`:

- EC1002: mcr-1.1 on CP021205 (IncI2), blaNDM-1 on CP021206 (IncA/C2). ✅ separate.
- EC2474: mcr-1.1 on CP021209 (IncHI2), blaNDM-1 on CP021210 (IncF/FII). ✅ separate.

AMRFinderPlus additionally confirms `blaNDM-1 + rmtC + ble` co-located on CP021206, consistent with paper's `rmtC-ISKpn14-blaNDM-1-bleMBL` context.

Tests C6. Central claim reproduced.

## Step 8 — LLM-judge scoring (Argo `gpt-5.2`, free tier)

- Input: `evidence/llm_judge_input.md` (paper claims + per-claim replication outputs).
- Judge prompt: per-claim verdict, coverage %, agreement %, canonical PARTIAL/FULL/STRUCTURAL verdict.
- Output: `evidence/llm_judge_gpt52.md`.
- Judge canonical verdict: **PARTIAL** (coverage 83.3%, agreement ~85–90%).

## Step 9 — Reporting

- Assemble `report/REPORT.md` (this replication's canonical narrative).
- Emit `WAVE_RESULT` one-liner for wave-tracker.

---

## Databases + versions (frozen)

| Component | Version / date |
|---|---|
| NCBI efetch | 2026-07-01/02 (live) |
| Biopython | 1.87 |
| mlst | 2.35.0 |
| PubMLST scheme | `ecoli_achtman_4` |
| AMRFinderPlus | 3.12.8 |
| AMRFinderPlus DB | 2024-07-22.1 |
| PlasmidFinder DB (`enterobacteriales.fsa`) | 159 refs, mid-2024 snapshot |
| Argo LLM judge | `gpt-5.2` (free) |

## Compute

- Local venv (Biopython, orchestration): CherryRd.
- MLST / AMRFinderPlus / blastn: **uicgpu** (`~/micromamba/envs/amr`).
- No paid endpoints, no BV-BRC job submission (analysis is public-data-only on already-closed genomes).
