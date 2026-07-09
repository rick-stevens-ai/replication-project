# Replication Workflow — BVBRC-41 (Lizárraga et al. 2022, *S. algae* 2NE11)

## Overview

End-to-end in-silico replication of a PacBio genome-announcement paper using
only free tools and free LLM endpoints. No paid PDF services, no paid LLM
tokens, no re-sequencing. Total analyst wall-clock: ~2–3 hours of active work
(mostly download + Prokka run).

## Workflow Stages

### Stage 1 — Paper acquisition (free)
- **Tool:** Europe PMC REST (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8816663/fullTextXML`)
- **Auth:** none
- **Cost:** $0
- **Output:** `work/fulltext.xml`, `work/fulltext.txt`
- **Est. time:** 1 min

### Stage 2 — Assembly resolution (free NCBI)
- **Tools:** NCBI `esearch` + `esummary` (Entrez EDirect)
- **Query:** `esearch db=assembly term=CP055159` → UID 7926261
- **Output:** RefSeq accession GCF_014263185.1, coverage metadata 231.29×
- **Est. time:** 2 min

### Stage 3 — Genome download (free)
- **Tool:** NCBI `datasets` CLI
- **Command:** `datasets download genome accession GCF_014263185.1 --include genome,protein,gff3,gbff,cds --filename g.zip`
- **Size:** 8.07 MB (md5-validated)
- **Output:** `work/dataset/ncbi_dataset/data/GCF_014263185.1/`
- **Est. time:** 1 min

### Stage 4 — Assembly-statistics recompute
- **Tool:** Pure Python 3 stdlib (no BioPython dependency)
- **Script:** `work/genome_stats.py`
- **Computes:** total length, GC%, contig count, contig lengths
- **Output:** `work/genome_stats.json`
- **Est. time:** 5 s

### Stage 5 — Feature-count recompute
- **Tool:** Pure Python (GFF parsing)
- **Inputs:** RefSeq `*_genomic.gff`, `assembly_data_report.jsonl`, `protein.faa`
- **Output:** `work/comparison_table.json` (paper Table 2 vs recompute)
- **Est. time:** 10 s

### Stage 6 — Targeted gene-content survey
- **Tool:** grep + Python
- **Approach:** search RefSeq GFF/faa by product string + paper's locus tags for each C6–C12 gene
- **Output:** `work/gene_content.json` (per-gene locus tag, bp length, aa length)
- **Est. time:** 10 min

### Stage 7 — Independent Prokka re-annotation
- **Host:** uicgpu (8× A100)
- **Env:** `/data/stevens/envs/bvbrc28` (conda)
- **Version:** Prokka 1.12
- **Command:**
  ```bash
  conda activate /data/stevens/envs/bvbrc28
  prokka --outdir prokka_out --genus Shewanella --species algae \
         --strain 2NE11 --cpus 8 /tmp/2NE11.fna
  ```
- **Output:** `work/prokka_out/2NE11.{txt,tsv,gff,faa,gbk,log}`
- **Est. time:** 15–20 min (single genome, 8 CPUs)

### Stage 8 — Independent genomic-island prediction
- **Tool:** Self-contained DIMOB-style detector (`work/gi_predict.py`)
- **Method:** sliding-window dinucleotide relative-abundance bias (Karlin δ*)
  + mobility-gene co-location (integrase / transposase / recombinase / T4SS /
  conjugative / relaxase)
- **Output:** `work/gi_prediction.json`
- **Est. time:** 30 s

### Stage 9 — LLM adjudication (free)
- **Endpoint:** Argo proxy `localhost:44497` (SSH tunnel from studio-ts)
- **Model:** `argo:gpt-5.2` (fallback `argo:claude-opus-4.8`)
- **Auth:** `Authorization: Bearer stevens`
- **Cost:** $0 (free Argo tier)
- **Driver:** `work/judge.py`
- **Input:** parsed evidence JSON (genome_stats + gene_content + comparison + gi + prokka summary)
- **Output:** `report/evidence/llm_judge.txt` (per-claim verdict + coverage + agreement + final verdict)
- **Est. time:** 30 s per pass

### Stage 10 — Report writeup
- **Format:** Markdown REPORT.md (primary) + LaTeX REPORT.tex (typeset)
- **Contents:** paper summary, claims table, method, results-vs-paper tables,
  LLM adjudication, coverage/agreement, limitations, artifact index
- **Est. time:** 45–60 min

## Tools & Codes Summary

| Category | Tool | Version | Cost | Purpose |
|---|---|---|---|---|
| Paper full text | Europe PMC REST | live | free | PMC XML fetch |
| Assembly resolution | NCBI EDirect (esearch/esummary) | live | free | CP055159 → GCF_014263185.1 |
| Genome download | NCBI `datasets` CLI | latest | free | assembly + annotations |
| Stats recompute | Python 3 stdlib | 3.10+ | free | length, GC, contigs |
| Feature counts | Python (GFF parser) | custom | free | Table 2 recompute |
| Gene survey | grep + Python | — | free | locus-tag + product-string search |
| Re-annotation | Prokka | 1.12 | free (conda) | independent pipeline vs PGAP |
| GI prediction | Custom Python (DIMOB-style) | custom | free | HGT island detection |
| LLM judge | Argo proxy | gpt-5.2 | free (Argo tier) | claim-by-claim scoring |
| Typesetting | LaTeX | — | free | REPORT.tex |

## Work Estimate (analyst hours)

| Stage | Wall-clock | Analyst-active |
|---|---|---|
| 1. Paper fetch | 1 min | 1 min |
| 2. Assembly resolution | 2 min | 2 min |
| 3. Genome download | 1 min | 1 min |
| 4. Stats recompute | 5 s + script write (10 min) | 10 min |
| 5. Feature counts | 10 s + script (10 min) | 10 min |
| 6. Gene survey | 10 min | 10 min |
| 7. Prokka | 20 min (background) | 5 min |
| 8. GI prediction | 30 s + script write (30 min) | 30 min |
| 9. LLM judge | 30 s + driver write (15 min) | 15 min |
| 10. Report writeup | — | 60 min |
| **Total analyst-active** | | **~2.5 h** |

## Reproducibility (one-shot)

```bash
# 1. Download genome
datasets download genome accession GCF_014263185.1 \
  --include genome,gff3,protein --filename g.zip
unzip -o g.zip -d dataset

# 2. Recompute stats
python3 genome_stats.py                 # -> 5,030,813 bp, 52.98% GC, 1 contig

# 3. Independent island prediction
python3 gi_predict.py                   # -> gi_prediction.json

# 4. Independent re-annotation (needs prokka in path)
prokka --genus Shewanella --species algae --strain 2NE11 \
       --outdir prokka_out 2NE11.fna    # -> ~20 min

# 5. LLM judge (needs Argo proxy running on localhost:44497)
python3 judge.py                        # -> report/evidence/llm_judge.txt
```

## Cost Summary

- **API cost:** $0 (Europe PMC + NCBI + Argo all free)
- **Compute:** uicgpu A100 idle time (Prokka is CPU-only, doesn't need GPU)
- **Storage:** ~8 MB genome + ~5 MB Prokka output
- **Analyst hours:** ~2.5 h
