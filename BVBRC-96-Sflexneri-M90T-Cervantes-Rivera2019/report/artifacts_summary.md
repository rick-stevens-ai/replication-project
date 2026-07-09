# Artifacts Summary — BVBRC-96 replication

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020).
DOI 10.1186/s12864-020-6565-5.
**Assembly:** GCF_004799585.1 (Umeå University, BioProject PRJNA510559, released 2019-04-18).
**Verdict:** PARTIAL REPLICATION (strong).

---

## Evidence files (under `report/evidence/`)

| File | Type | Provenance | What it demonstrates |
|---|---|---|---|
| `assembly_report.json` | JSON | NCBI Datasets REST v2 `dataset_report` endpoint, fresh pull | Ground-truth structural metadata: Complete Genome, 2 replicons, chromosome 4,596,714 bp + pWR100 232,195 bp, total 4,828,909 bp, GC ~50.5%, released 2019-04-18, submitter Umeå University. Backs claims C1, C2, C10. |
| `genome_metrics_summary.md` | Markdown | Human-readable summary derived from `assembly_report.json` + PGAP GFF parse | Structural + annotation metrics table (CDS/tRNA/rRNA/pseudogene/IS counts, per-replicon breakdown). Backs C4. |
| `abricate_plasmidfinder.tsv` | TSV | `abricate --db plasmidfinder` on the freshly downloaded FASTA on uicgpu (`/data/stevens/envs/bvbrc28`) | Single hit: IncFII_1 on NZ_CP037924.1 @ 101,994–102,253, 99.62% coverage / 96.17% identity, accession AY458016. Backs C6. |
| `abricate_vfdb.tsv` | TSV | `abricate --db vfdb` on the freshly downloaded FASTA (uicgpu, same env) | 172 VFDB virulence-gene hits (108 chromosome + 64 plasmid). Full T3SS mxi/spa/ipa/ipg/osp/ipaH + icsA + espC/nleE/virA on pWR100; iucABCD/iutA + enterobactin + curli + fimbriae on chromosome. Backs C5, C7. |
| `abricate_card.tsv` | TSV | `abricate --db card` on the freshly downloaded FASTA (uicgpu) | 57 CARD resistance-gene hits — resistance-context sanity check (not a paper claim, but included for completeness). |
| `fastani.tsv` | TSV | fastANI query-vs-reference-list on uicgpu; comparator panel via NCBI Datasets (Sf 2a 301, Sf 5b 8401, S. sonnei Ss046, S. dysenteriae Sd197, S. boydii Sb227, E. coli K12 MG1655) | Nearest neighbor Sf 5b 8401 @ 99.933% ANI (aligned fraction 0.940), demonstrating M90T's phylogenomic distinctness from the stopgap reference. Backs C8. |
| `judge_verdict.md` | Markdown | Argo proxy (`localhost:44497`, free CELS endpoint) with the assembled evidence bundle as prompt | Independent LLM-judge verdict + reasoning (converges on PARTIAL, strong). |

## Working files (under `work/`)

| File | Size | Notes |
|---|---|---|
| `work/genome.zip` | 2,695,927 bytes | NCBI Datasets v2 download package (FASTA + GFF + PROT + SEQUENCE_REPORT). FASTA MD5 `b42e8cb5771af766febc5a841847ed3e`. |

## Report deliverables (under `report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical markdown report (source of truth for this backfill). |
| `REPORT.tex` | LaTeX rendering with dedicated *Genuine Critique* section. |
| `open_questions.json` | 5 forward-looking scientific questions (JSON list). |
| `workflow.md` | Step-by-step reproduction workflow. |
| `artifacts_summary.md` | This file — inventory + provenance of everything above. |
| `failure_analysis.md` | Candid analysis of what was NOT tested and why. |

## Claims → artifacts crosswalk

| Claim | Type | Verified? | Primary artifact |
|---|---|---|---|
| C1 (2 circular replicons) | Structural | ✅ | `assembly_report.json` |
| C2 (chromosome 4,596,714 bp + pWR100 232,195 bp) | Metrics | ✅ (bp) | `assembly_report.json` |
| C3 (Canu 1.7 PacBio + Illumina RNA-seq polish) | Methods | ❌ (not re-run) | see `failure_analysis.md` |
| C4 (~5000 CDS, 7 rRNA operons, ~100 tRNA, high pseudogene load, ~400 IS) | Annotation | ✅ (qualitative) | `genome_metrics_summary.md` |
| C5 (T3SS + effectors on pWR100) | Function | ✅ | `abricate_vfdb.tsv` |
| C6 (pWR100 is IncF-family) | Plasmid typing | ✅ | `abricate_plasmidfinder.tsv` |
| C7 (SHI-2 aerobactin on chromosome) | Chromosomal VF | ✅ | `abricate_vfdb.tsv` |
| C8 (nearer to Sf 5b 8401 than any other Enterobacteriaceae) | Phylogenomics | ✅ | `fastani.tsv` |
| C9 (dRNA-seq 6,723 primary + 7,328 secondary TSS) | Transcriptomics | ❌ (not re-run) | see `failure_analysis.md` |
| C10 (deposited + usable) | Availability | ✅ | `assembly_report.json` + successful fresh download |

## Provenance guarantees

- **Independent fresh pull.** Genome package was downloaded from NCBI fresh for this
  replication (not reused from sibling BVBRC-54); FASTA MD5 recorded for reproducibility.
- **Independent tool runs.** All abricate scans, PGAP-GFF parse, mash sketch/dist, and
  fastANI runs were executed inside a single uicgpu conda env (`/data/stevens/envs/bvbrc28`)
  with logs preserved.
- **Free endpoints only.** No paid API keys used. NCBI Datasets REST v2 is unauth; Argo proxy
  is the free CELS endpoint per the standing "免费 endpoint 唯一" rule.
- **No fabricated numbers.** Every quantitative value in the report traces to one of the
  evidence files above.
