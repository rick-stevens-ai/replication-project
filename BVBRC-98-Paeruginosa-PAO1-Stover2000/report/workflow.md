# Workflow — BVBRC-98 · Stover et al. 2000 (PAO1) Replication

**Target paper:** Stover et al., *Nature* 406:959–964 (2000), doi:10.1038/35023079
**Assembly used:** RefSeq `NC_002516.2` (assembly `ASM676v1`, `GCF_000006765.1`)
**Host:** CherryRd · macOS · Python 3.13 stdlib only · wall-clock ~2 min
**Verdict:** PARTIAL (LLM-judge canonical)

---

## Overview

Reproduce the three numerically-testable claims of the Stover 2000 PAO1 reference-genome paper (genome size, G+C content, predicted ORF count) directly from the current public RefSeq record for the same isolate, using stdlib-only parsing plus an LLM-judge for verdict assignment. Two additional paper claims (C4 largest-bacterial-genome-at-publication, C5 exceptional regulatory-gene richness) are historical/comparative and were not testable from a single FASTA — recorded as context-only.

## Step-by-step

1. **Fetch the reference assembly (free, NCBI `datasets` CLI, no auth).**
   ```
   datasets download genome accession GCF_000006765.1 \
       --include genome,gff3,protein
   unzip ncbi_dataset.zip
   ```
   Artifacts landed:
   - `GCF_000006765.1_ASM676v1_genomic.fna` (~6.3 MB)
   - `genomic.gff` (~3.2 MB)
   - `protein.faa` (~2.3 MB)
   MD5s captured in `report/artifact_harvest.md`.

2. **FASTA parse (`work/analyze.py`).** Concatenate all sequence lines, uppercase, count A/C/G/T, compute total length and `gc% = 100 * (G+C) / (A+C+G+T)`. Confirm single contig / zero ambiguous bases.

3. **GFF3 parse (`work/analyze.py`).** Tally features by type (`gene`, `CDS`, `rRNA`, `tRNA`, `ncRNA`, `tmRNA`); extract `gene_biotype` and `protein_id`; collect gene/CDS length distributions; count unique protein IDs.

4. **Protein-FASTA sanity check.** Count `>` header lines in `protein.faa` and cross-check against unique-protein-IDs recovered from the GFF (both = 5,572; CDS features = 5,573).

5. **Provenance.** MD5 every downloaded file.

6. **LLM-judge scoring (`work/llm_judge.py`).** Free Argo endpoint `http://127.0.0.1:44497/v1/chat/completions`, model `argo:gpt-4o`, `temperature=0.0`. Send paper claims + observed numbers, receive per-claim `reproduced / agreement / notes` JSON and overall verdict from the canonical vocabulary. Full request+response cached to `report/evidence/llm_judge.json`.

7. **Report assembly.** Write `report/REPORT.md`, `report/REPORT.tex`, `report/evidence/genome_stats.json`, `report/evidence/llm_judge.json`, plus this workflow, `artifacts_summary.md`, `failure_analysis.md`, and `open_questions.json`.

## Data flow

```
NCBI datasets CLI
    │
    ▼
work/genome/ncbi_dataset/data/GCF_000006765.1/
    ├── ...ASM676v1_genomic.fna   (FASTA)
    ├── genomic.gff               (GFF3)
    └── protein.faa               (protein FASTA)
    │
    ▼
work/analyze.py  ─►  report/evidence/genome_stats.json
    │
    ▼
work/llm_judge.py  ─►  report/evidence/llm_judge.json  (verdict = PARTIAL)
    │
    ▼
report/REPORT.md, REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json
```

## Constraints honored

- **Free endpoints only:** NCBI `datasets` CLI (no auth) + Argo local proxy `127.0.0.1:44497` (free `argo:gpt-4o`). No Anthropic / OpenAI / OpenRouter calls.
- **LLM-judge, not regex,** supplies the final verdict.
- **All writes stay inside the target directory** `~/Dropbox/REPLICATE-PROJECT/BVBRC-98-Paeruginosa-PAO1-Stover2000/`.
- **Real replication on real bytes** (6.3 MB FASTA + 3.2 MB GFF + 2.3 MB protein FASTA); no shortcut / cached-numbers replay.

## Reproduction recipe (one-shot)

```
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-98-Paeruginosa-PAO1-Stover2000/
mkdir -p work/genome && cd work/genome
datasets download genome accession GCF_000006765.1 \
    --include genome,gff3,protein
unzip -o ncbi_dataset.zip
cd ../..
python3 work/analyze.py        # writes report/evidence/genome_stats.json
python3 work/llm_judge.py      # writes report/evidence/llm_judge.json
```

Expected outputs match those in `report/REPORT.md` (C1 = 6,264,404 bp; C2 = 66.556%; C3 = 5,573 CDS; verdict PARTIAL).
