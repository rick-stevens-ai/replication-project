# Workflow — BVBRC-122 Replication

## Pipeline diagram

```
┌────────────────┐    ┌────────────────────┐    ┌───────────────────┐
│ PubMed/PMC     │───►│ NCBI Assembly      │───►│ CBW1002/1006 fna+ │
│ 33528491       │    │ (esearch/esummary) │    │ gff+faa (~4MB ea) │
└────────────────┘    └────────────────────┘    └────────┬──────────┘
                                                          │
                       ┌──────────────────────────────────┼────────────┐
                       ▼                                  ▼            ▼
              ┌────────────────┐                ┌─────────────┐  ┌─────────────┐
              │ 9 reference    │                │ Length + GC │  │ CDS/gene/   │
              │ genomes (FTP)  │                │ + N50 QC    │  │ pseudogene  │
              │ CB0101, BS55D, │                └─────────────┘  │ counts, +   │
              │ WH8102, PCC..., │                                 │ cspA/B/C/G │
              │ Cyanobium,     │                                 │ inventory   │
              │ Prochlorococcus│                                 └─────────────┘
              └────┬───────────┘
                   │
       ┌───────────┼──────────────┐
       ▼           ▼              ▼
  ┌─────────┐ ┌──────────┐  ┌────────────────┐
  │ 16S     │ │ Reciproc │  │ Proteome sizes │
  │ extract │ │ best     │  │                │
  │ +MAFFT  │ │ BLASTP   │  │                │
  │+FastTree│ │ 6 pairs  │  │                │
  └────┬────┘ └────┬─────┘  └────────────────┘
       │           │
       ▼           ▼
  ┌─────────┐ ┌──────────┐
  │ 11-taxon│ │ RBH      │
  │ tree +  │ │ counts   │
  │ % ID    │ │ Fig 2    │
  │ matrix  │ │ replic.  │
  └─────────┘ └──────────┘
       │           │
       ▼           ▼
  ┌────────────────────────┐
  │ evidence/summary_...   │
  │  → Argo GPT-4o judge   │
  │  → verdict JSON        │
  └────────────────────────┘
```

## Tools and codes

| Tool | Version | Purpose | Location |
|---|---|---|---|
| curl | any | NCBI Entrez + FTP | uicgpu |
| Biopython | 1.83 | FASTA/GFF parsing | bvbrc56 conda env |
| BLAST+ blastp / makeblastdb | 2.16.0 | reciprocal-best-hit homolog counts | bvbrc56 |
| MAFFT | 7.526 | 16S multiple sequence alignment | bvbrc56 |
| FastTreeMP | 2.1.11 | 16S GTR+Γ ML tree | bvbrc56 |
| Argo litellm proxy | LiteLLM | free LLM inference | cherryrd :4000 |
| Argo GPT-4o | (via Argo) | LLM-judge grading | Argo |
| pdftotext | poppler | paper text extraction | CherryRd |

Full computation log: `report/attempt_log.md`.

## Effort estimate

| Phase | Wall-clock | Human effort |
|---|---:|---:|
| Paper discovery + PDF fetch + accession lookup | 3 min | ~2 min |
| Genome + reference panel download (11 genomes, ~120 MB total) | 5 min | ~5 min |
| Genome-stat / GC / CDS / cold-shock inventory | 2 min | ~5 min |
| 16S extraction, MAFFT alignment, FastTree | 1 min | ~10 min |
| 6-pair reciprocal-best-BLASTp (mostly network-bound blastp runs) | ~12 min | ~10 min |
| LLM-judge grading | ~20 s | ~5 min |
| Report drafting (this replication) | — | ~30 min |
| **TOTAL** | **~25 min compute** | **~65 min effort** |

## Provenance / free-endpoint compliance

- All data: public NCBI (RefSeq/GenBank), no auth required.
- All compute on uicgpu (Rick's institutional free resource), except LLM-judge on Argo (free ANL LLM proxy, key `stevens`).
- No paid APIs (Anthropic direct, OpenAI direct, OpenRouter) touched.
- No external data leaked outside the ANL network.
