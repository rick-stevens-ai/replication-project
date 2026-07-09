# Workflow — BVBRC-26 (Vassallo et al. 2022, E. coli anti-phage defence)

End-to-end computational replication pipeline. All steps free/public (BV-BRC, NCBI Datasets v2, Europe PMC, Argo proxy). Wall-clock ~15 min from a clean checkout of the working directory.

## Pipeline DAG

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 0 — PAPER + SUPPLEMENT INGEST                                          │
│   Europe PMC PMC9519451 (JATS XML) ──► paper_fulltext.xml                    │
│   Supplementary xlsx (Tables S1–S8) ──► SupplementaryTables.xlsx             │
│           │                                                                  │
│           ▼ (openpyxl parse)                                                 │
│   paper_S5_source_strains.json   (71 strains + GCA accessions)               │
│   paper_S2_systems.json          (21 systems: source/contig/CDS/coords)      │
│   defense_representatives.fasta  (21 system reps, one per PD-*)              │
│   defense_proteins.fasta         (32 protein components)                     │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1 — CORPUS MAPPING  (C1)                                               │
│   map_bvbrc.py                                                               │
│     For each GCA in paper_S5_source_strains.json:                            │
│       curl --max-time 30 \                                                   │
│         "https://patricbrc.org/api/genome/?eq(assembly_accession,GCA_XXX)"   │
│       → parse JSON → extract genome_id (e.g. 562.33412)                      │
│   ──► bvbrc_genome_map.json  (71/71 GCA → BV-BRC genome_id)                  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2 — PROTEOME DOWNLOAD                                                  │
│   fetch_ncbi_proteomes.py                                                    │
│     For each of 71 GCAs:                                                     │
│       NCBI Datasets v2alpha REST download                                    │
│         (dataformat=protein-fasta)                                           │
│       → write ncbi_proteomes/<genome_id>.faa                                 │
│   ──► ncbi_proteomes/  (71 files, 348,507 proteins total)                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3 — DISTRIBUTION / PROVENANCE  (C2 + C3-panel)                         │
│   build_distribution.py                                                      │
│     1) Concatenate 71 proteomes, prefix headers with genome_id               │
│        → blast/all71_proteomes.faa                                           │
│     2) makeblastdb -dbtype prot -in blast/all71_proteomes.faa                │
│     3) blastp -query defense_representatives.fasta                           │
│                -db blast/all71_proteomes                                     │
│                -evalue 1e-5 -max_target_seqs 2000 -outfmt 6                  │
│        → blast/rep_vs_all71.tsv                                              │
│     4) Per system, best hit per strain; tier by pident/qcov/e:               │
│          self     : pident>=98, qcov>=90                                     │
│          ortholog : pident>=70, qcov>=70, e<=1e-30                           │
│          homolog  : pident>=30, qcov>=50, e<=1e-10                           │
│     5) source_recovered = (self-hit strain == paper-declared source strain)  │
│   ──► blast/distribution_summary.json                                        │
│         (per-system: n_homolog, n_ortholog, n_self, source_recovered bool,   │
│          carrier genome_id list)                                             │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4 — MGE / HOTSPOT CONTEXT  (C4)                                        │
│   mge_context.py                                                             │
│     For each of 21 systems (paper_S2_systems.json):                          │
│       1) Confirm BV-BRC accession field == Table S2 contig accession         │
│       2) BV-BRC genome_feature GET all CDS on that contig                    │
│       3) Locate system CDS by coordinate overlap with Table S2 start/stop    │
│       4) Take +/- 20-gene window                                             │
│       5) Keyword-scan neighbour product strings:                             │
│            MGE signatures:                                                   │
│              integrase, transposase, recombinase, phage,                     │
│              tail/capsid/portal/terminase, IS/insertion, mobile,             │
│              relaxase, conjug*, excisionase, plasmid                         │
│            Defence-like signatures:                                          │
│              restriction, methyltransferase, toxin/antitoxin, Abi,           │
│              nuclease, helicase, DUF, Cas/CRISPR, HEPN,                      │
│              NTPase/ATPase, deaminase, argonaute                             │
│       6) hotspot = (defence_like_neighbours >= 2)                            │
│   ──► mge_context_summary.json  (per-system: MGE nbrs, def-like nbrs, hot)   │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 5 — KNOWN-SYSTEM SURVEY (CRISPR + RM)                                  │
│   crispr_survey.py                                                           │
│     For each of 71 source genomes:                                           │
│       BV-BRC genome_feature GET all CDS with                                 │
│         product ~ /cas[0-9]|crispr|restriction|methyltransferase/i           │
│       Count canonical CRISPR-Cas and RM annotations                          │
│   ──► crispr_rm_survey.json  (per-genome CRISPR/RM presence)                 │
│   NOTE: BV-BRC returned dual RefSeq+PATRIC annotations → CDS counts          │
│         are roughly 2x; presence/absence signal unaffected                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 6 — NOVELTY  (C5)                                                      │
│   Parse Table S4 (already in SupplementaryTables.xlsx):                      │
│     count components with no Gao et al. 2020 seed-cluster match              │
│     record identity distribution of matched components                       │
│   → 18/32 no-match; 14/32 matched at 26–49% (majority <35%)                  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 7 — LLM-JUDGE VERDICT                                                  │
│   llm_judge.py                                                               │
│     POST to Argo proxy http://127.0.0.1:44497/v1/chat/completions            │
│       model = argo:gpt-o3                                                    │
│       auth  = Authorization: Bearer stevens                                  │
│     Prompt: paper claims + reproduced results per claim                      │
│     Request: per-claim + overall verdict from canonical vocabulary           │
│              + Coverage 1–10 + Agreement 1–10                                │
│   ──► llm_judge_verdict.txt  (Coverage 8/10, Agreement 9/10, PARTIAL)        │
└──────────────────────────────────────────────────────────────────────────────┘

  INDEPENDENT REPRODUCTION (2026-07-03, separate subagent, no reuse)
  ─────────────────────────────────────────────────────────────────
  Repeat Stages 0, 2, 4 from scratch via NCBI eutils (efetch) + NCBI Datasets v2
  (no BV-BRC). Coordinate-verify a random sample of 9 proteins across 6 systems
  by freshly downloading each contig FASTA and 6-frame translating the declared
  genomic region.
  → report/evidence/independent_reproduction/  (13/13 checkable numbers match)
```

## Runtime characteristics

| Stage | Wall-clock | Bottleneck | Failure mode |
|-------|-----------|------------|--------------|
| 0. Paper + supplement | <30 s | Europe PMC latency | Retry with backoff |
| 1. BV-BRC corpus map | ~2 min | 71 sequential BV-BRC API calls | curl --max-time bounds each |
| 2. NCBI proteomes | ~5–8 min | 71 sequential downloads | NCBI Datasets rate-limit |
| 3. BLASTP distribution | ~3–4 min | 348k-protein DB build + 21-query BLAST | disk (~500 MB temp) |
| 4. MGE / hotspot | ~1 min | 21 BV-BRC genome_feature calls | dual-annotation noise |
| 5. CRISPR/RM survey | ~1 min | 71 BV-BRC genome_feature calls | dual-annotation noise |
| 6. Novelty (Table S4) | <10 s | local xlsx parse | none |
| 7. LLM judge (Argo) | ~30 s | Argo proxy round-trip | Argo :44497 tunnel down → retry |

**Total: ~15 min** on CherryRd (or any node with the standard OpenClaw env).

## Data-flow contracts (per-stage inputs / outputs)

- **Corpus map (Stage 1):** input = 71 GCA accessions from Table S5; output = 71 BV-BRC `genome_id`s; contract = 71/71 (100% mapping required for downstream tier consistency).
- **Proteomes (Stage 2):** input = 71 GCAs; output = 71 `.faa` files named by BV-BRC `genome_id`; contract = header-prefixable so BLAST hits back-map to strain identity.
- **BLASTP distribution (Stage 3):** input = `defense_representatives.fasta` (21) + concatenated 348k proteome DB; output = per-system tier counts + source-recovery bool; contract = every system MUST self-hit somewhere at >=98/>=90; if not, either the FASTA or the source-strain proteome is wrong.
- **MGE context (Stage 4):** input = 21 (source_strain, contig, start, stop) tuples from Table S2 + BV-BRC feature dump; output = per-system MGE-neighbour count + defence-like-neighbour count + hotspot bool; contract = keyword-based, deterministic on input product strings.
- **Novelty (Stage 6):** input = Table S4 as parsed; output = 18/32 no-match, 14/32 matched at 26–49%; contract = pure re-read of paper table (this stage is a check, not a computation).
- **LLM-judge (Stage 7):** input = all preceding per-claim results as prompt; output = Coverage + Agreement + verdict; contract = judge sees the same information the human reviewer wrote (coherence check, not audit).

## Ordering / dependency rules

- Stages 0 → 1 → 2 must run sequentially; Stages 3, 4, 5 depend on 2 but are independent of one another (can parallelise on a multi-core host, but no speed gain in practice since Stages 4/5 are I/O-bound on BV-BRC).
- Stage 6 is pure paper-table parse; can run any time after Stage 0.
- Stage 7 must run last (needs all preceding outputs).
- **No writes to sibling `36123438-Anti-phage-defense-Ecoli/`** — that directory is read-only context.

## Free-endpoint invariant

Every stage uses only free/no-auth or free-with-user-key endpoints: BV-BRC data API (no auth), NCBI Datasets v2alpha REST (no auth), NCBI Entrez eutils (no auth, courtesy rate limit 3/s without API key), Europe PMC (no auth), Argo proxy (`Authorization: Bearer stevens`, ANL-internal free). No paid endpoint is used at any point.
