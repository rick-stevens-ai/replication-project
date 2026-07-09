# Workflow — BVBRC-49 (Szmolka et al. 2023, mcr-1 duck E. coli Hungary)

**Target paper:** Szmolka et al., *Antibiotics* 12(10):1519 (2023), PMC10604428, DOI 10.3390/antibiotics12101519.
**Isolate:** Ec45-2020 (Hungarian duck E. coli, mcr-1+).
**Deposited assembly:** GCF_038709795.1 / GCA_038709795.1 (ASM3870979v1).
**Verdict:** PARTIAL REPLICATION (strong).

---

## Stage 0 — Paper acquisition and claim extraction

1. **Retrieve full text** via Europe PMC REST:
   - Endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10604428/fullTextXML`
   - Cost: free; no auth required.
2. **Extract claims** from full text into a 7-row claims table (C1–C7 in REPORT.md §2):
   - C1 architecture (chromosome + 5 plasmids)
   - C2 mcr-1 on 33,541 bp IncX4, exclusively
   - C3 ST162 MLST
   - C4 254 kb IncH plasmid + resistance gene set
   - C5 AMR phenotype Amp-Chl-Cip-Col-Sul-Tet-Tmp; colistin MIC = 8 µg/mL
   - C6 APEC virulence genes astA, fyuA, hlyE, lpfA
   - C7 Serotype H10:O55
3. **Recover accessions** from full-text XML mining:
   - BioProject: **PRJNA1012593**
   - Replicons: **CP134085–CP134090** (chromosome + 5 plasmids)

## Stage 1 — Assembly resolution and download

1. **Resolve BioProject → assembly** via NCBI Datasets v2alpha REST:
   - `GET https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/bioproject/PRJNA1012593/dataset_report`
   - Result: GCF_038709795.1 (RefSeq) / GCA_038709795.1 (GenBank).
2. **Download the assembly bundle** (FASTA + protein FASTA + GFF):
   - `GET .../datasets/v2alpha/genome/accession/GCF_038709795.1/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF`
   - Size: ~3.2 MB zip.
   - No authentication required.

## Stage 2 — Genome statistics

1. **Per-replicon length + GC** computed with a small Python script (`work/genome_stats.py`) using Biopython SeqIO to iterate through the assembly FASTA.
2. Output: `report/evidence/genome_stats.json` — one row per replicon (accession, length, GC%).

## Stage 3 — Typing tools on uicgpu

Host: **uicgpu** (8×A100, conda env `bvbrc14`). All three tools invoked on the unpacked RefSeq FASTA.

1. **mlst 2.33.1** with scheme `ecoli_achtman_4`:
   - `mlst --scheme ecoli_achtman_4 <FNA>` → sequence type + allele profile.
   - Output: `report/evidence/mlst.tsv`.
2. **AMRFinderPlus 4.2.7** (database version 2026-03-24.1):
   - `amrfinder -n <FNA> -O Escherichia --plus`
   - Modules used: acquired AMR, point mutations (QRDR), stress, virulence.
   - Output: `report/evidence/amrfinder.tsv`.
3. **abricate 1.4.0** with three databases (all vintage 2026-Apr-3):
   - `abricate --db resfinder <FNA>` → acquired ARGs.
   - `abricate --db plasmidfinder <FNA>` → plasmid replicons.
   - `abricate --db vfdb <FNA>` → virulence genes (124 hits total).
   - Outputs: `report/evidence/abricate_{resfinder,plasmidfinder,vfdb}.tsv`.

Wall clock: ~2 min (mlst + abricate) + 63 s (AMRFinder) = ~3 min total.

## Stage 4 — Claim-by-claim scoring

Cross-walk the tool outputs against C1–C7:

| Claim | Instrument(s) | Verdict |
|---|---|---|
| C1 architecture | genome_stats.json | ✅ 5 plasmids, chromosome bp exact within ±100 (RefSeq trim) |
| C2 mcr-1 IncX4 exclusive | abricate plasmidfinder + resfinder on CP134089; AMRFinderPlus | ✅ EXACT |
| C3 ST162 | mlst.tsv | ✅ EXACT allele profile |
| C4 IncH + gene set | abricate plasmidfinder + resfinder on CP134088 | ✅ replicon + all named genes |
| C5 phenotype | AMRFinderPlus + abricate on all replicons | ⚠ genotype only; MIC not re-measured |
| C6 APEC virulence | AMRFinderPlus --plus + abricate vfdb | ✅ all four |
| C7 serotype H10:O55 | (no serotyper available) | ❌ not tested |

## Stage 5 — LLM-judge scoring

- **Endpoint:** free Argo proxy, `argo:gpt-5.2` at `http://localhost:44497/v1`.
- **Prompt:** structured C1–C7 claims table + full evidence outputs; asked for `coverage` (0–10) and `agreement` (0–10) scores with reasoning.
- **Verdict:** coverage 8/10, agreement 9/10.
- Output: `report/evidence/llm_judge_gpt52.md`.
- Rationale for using LLM-judge: avoids brittle regex verdict logic; produces a natural-language justification that can be re-audited.

## Stage 6 — Report authoring

- `REPORT.md` — the canonical markdown report (this stage's core deliverable).
- `REPORT.tex` — LaTeX rendering with an added GENUINE CRITIQUE section.
- `open_questions.json` — 5 domain-specific open questions with basis + next steps.
- `workflow.md` (this file) — the end-to-end procedure.
- `artifacts_summary.md` — inventory of files produced.
- `failure_analysis.md` — honest accounting of what didn't work / wasn't done.

## Reproducibility (one-command core)

```bash
curl -sS -o GCF_038709795.1.zip \
 "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_038709795.1/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF"
unzip -q GCF_038709795.1.zip -d GCF_038709795.1
FNA=GCF_038709795.1/ncbi_dataset/data/GCF_038709795.1/*_genomic.fna
mlst $FNA
amrfinder -n $FNA -O Escherichia --plus
abricate --db plasmidfinder $FNA
abricate --db resfinder    $FNA
abricate --db vfdb         $FNA
```

Total resource cost: **all free / public**; ~3 min wall clock on uicgpu.
