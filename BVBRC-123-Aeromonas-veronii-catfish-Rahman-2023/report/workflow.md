# Workflow — BVBRC-123 Replication

## Overview
This is a bacterial WGS bioinformatics replication. The paper deposits a single Illumina-MEGAHIT contig-level assembly + PATRIC/BV-BRC pipeline annotation. The replication is entirely reproducible from public REST APIs + widely-available open-source tools.

## Effort estimate
- **Wall clock**: ~30 minutes end-to-end on CherryRd (macOS, homebrew tools).
- **Human-hours if manually driven**: ~2-3h (paper reading, accession triangulation, tool wrangling, MLST fallback).
- **Compute**: negligible (single-machine, no GPU required; abricate ~1 min per DB, skani/fastANI ~5 sec per pair).

## Tools + codes

| Step | Tool | Version | License |
|---|---|---|---|
| PDF fetch | curl | 8.x | MIT |
| Text extraction | pdftotext (Xpdf/Poppler) | homebrew | GPL |
| FASTA parsing | Python 3.14 stdlib | 3.14.6 | PSF |
| Accession search | NCBI Entrez eutils REST | v3 | public |
| Assembly download | NCBI Datasets v2 REST | v2 | public |
| Assembly stats | custom Python | | — |
| Annotation parsing | awk, grep | | — |
| AMR/virulence | abricate | 1.4.0 | GPLv2 |
| CARD | via abricate | 2026-07-03 build | Academic |
| ResFinder | via abricate | 2026-07-03 build | Apache-2.0 |
| NCBI AMRFinder | via abricate | 2026-07-03 build | Public domain |
| VFDB | via abricate | 2026-07-03 build | Academic |
| PlasmidFinder | via abricate | 2026-07-03 build | Apache-2.0 |
| ANI | skani | 0.3.2 | MIT |
| ANI (verification) | fastANI | 1.34 | Apache-2.0 |
| MLST | pubMLST REST API | live | CC-BY-NC-SA |
| Prophage proxy | grep on PGAP GFF | | — |
| LLM judge | argo:gpt-5.4 via cherryrd litellm aggregator :4000 | live | Argo (free) |

## Pipeline (linear, single-machine)

```
1. fetch_paper_pdf
   └─ curl https://europepmc.org/articles/PMC10636080?pdf=render -o paper.pdf

2. extract_paper_text
   └─ pdftotext -layout paper.pdf work/paper.txt

3. triangulate_accessions
   ├─ eutils esearch db=assembly term="Alim_AV_1000"  → uid=14736231
   ├─ eutils esummary db=assembly id=14736231         → GCA_026738955.1
   └─ note paper's PRJNA810265 is WRONG (Pasteurella project); real = PRJNA827572

4. download_query_and_refs
   ├─ ncbi_datasets v2 /genome/accession/GCA_026738955.1/download (query)
   ├─ ncbi_datasets v2 /genome/accession/GCF_026738955.1/download (annotated)
   ├─ ncbi_datasets v2 /genome/accession/GCF_001593245.1/download (TH0426)
   ├─ ncbi_datasets v2 /genome/accession/GCF_000204115.1/download (B565)
   └─ ncbi_datasets v2 /genome/accession/GCF_008693705.1/download (FDAARGOS_632)

5. recompute_assembly_stats
   └─ python parse-fasta → 93 contigs, 4494464 bp, N50=150337, L50=12, GC=58.87%

6. annotation_counts
   └─ awk on PGAP GFF → 4099 CDS, 102 tRNA, 28 rRNA, 59 pseudogene

7. amr_virulence_plasmid
   ├─ abricate --db card refseq.fna    → 3 hits
   ├─ abricate --db resfinder ...       → 2 hits
   ├─ abricate --db ncbi ...            → 2 hits
   ├─ abricate --db vfdb ...            → 130 unique
   └─ abricate --db plasmidfinder ...   → 0 replicons

8. mlst_scheme1
   ├─ POST base64(FASTA) → pubmlst_aeromonas_seqdef/schemes/1/sequence
   ├─ compare to ST 492 expected profile → complete mismatch
   └─ scan all 2756 profiles for ≥3-allele overlap → 0 matches → CONTRADICTED

9. ani_phylogeny
   ├─ skani triangle query + 3 refs   → 96.34, 96.34, 96.47%
   └─ fastANI query vs refs.txt        → 96.24, 96.34, 96.38%

10. prophage_proxy
    └─ grep phage-family products in PGAP GFF, group by contig → 2 dense + 1 sparse cluster

11. llm_judge
    └─ POST evidence.json → argo:gpt-5.4 (cherryrd litellm :4000) → PARTIAL

12. write_artifacts
    └─ REPORT.md, REPORT.tex, brief.md, attempt_log.md, artifact_harvest.md,
       open_questions.json, workflow.md (this file), artifacts_summary.md,
       failure_analysis.md, extraction/marker.md, extraction/nougat.mmd
```

## What would extend this replication further (out of scope for this pass)
- Re-annotate with Bakta or Prokka to compare against paper's RAST 4,229 CDS count on same annotator basis.
- Rerun PHASTER (needs web submission) or PHASTEST (has REST API) for exact prophage-region count/coordinates.
- Compute pan-genome with Roary/Panaroo across A. veronii genomes to place Alim_AV_1000 in the pan-core-shell distribution.
- Full RaxML phylogeny reconstruction with the paper's tool chain (PATRIC PGFam alignment + MUSCLE + RaxML fast bootstrap) to validate the "TH0426 is closest" tree topology.
- OrthoFinder or proteinortho between Alim_AV_1000 and NZ_CP044060.1 to verify ≥95% conserved-proteome claim.
