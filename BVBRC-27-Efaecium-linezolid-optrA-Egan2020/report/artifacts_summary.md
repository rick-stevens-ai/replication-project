# Artifacts Summary — BVBRC-27 Egan 2020 optrA/poxtA

**Paper:** Egan et al. 2020, JAC 75:1704–1711, PMID 32129849.
**Verdict:** PARTIAL REPLICATION (independent reproduction 2026-07-03 CONFIRMED, 36/36 numbers matched).

## 1. Inputs — public data (all free)

| Artifact | Source | Size | Purpose |
|---|---|---:|---|
| `PMC7303821/fullTextXML` | Europe PMC REST | ~120 KB | Full text; accession scrape |
| GenBank `MN831410`–`MN831419` (`.gb` + `.fasta`) | NCBI E-utilities `efetch` | ~2 MB total | 10 deposited plasmids/regions |
| pE394 `KP399637` | NCBI `efetch` | ~40 KB | C2 reference plasmid (true "pE349") |
| Canonical *optrA* `NG_048023` | NCBI `efetch` | ~2 KB | C4 variant baseline |
| NCBI AMRFinderPlus `AMR_CDS.fa` (9,712 alleles, original run) | NCBI Pathogen FTP | ~10 MB | Independent AMR reference (C1) |
| NCBI AMRFinderPlus DB (8,232 alleles, indep. rerun) + ResFinder (3,206) | via `abricate v1.4.0` | ~14 MB | Independent-tool cross-check (C1) |

**Total:** ~27 MB combined; all inputs free, no auth.

## 2. Deposited-sequence catalog (10 records)

| Accession | Description | Length | Species | Genes detected (C1) |
|---|---|---:|---|---|
| MN831410 | pM17/0149 | 36,331 bp | *Ec. faecalis* | **optrA (100%)**, fexA (99.65%) |
| MN831411 | pM16/0594 | 21,849 bp | *Ec. faecium* | **poxtA (100%)**, tet(M) (99.95%), tet(L) (99.56%) |
| MN831412 | pM18/0011 | 18,280 bp | *Ec. faecalis* | **poxtA (100%)**, fexB (100%) |
| MN831413 | pM17/0314 | 103,600 bp | *Ec. faecium* | **optrA (99.9%)**, **cfr(D) (100%)**, erm(B) (100%) |
| MN831414 | optrA_I | region | *Ec. faecalis* | optrA (99.95%), fexA (99.65%) |
| MN831415 | optrA_II | region | *Ec. faecalis* | optrA (99.85%), fexA (99.65%) |
| MN831416 | optrA_III | region | *Ec. faecium* | optrA (99.9%) |
| MN831417 | optrA_IV | region | *Ec. faecalis* | optrA (99.69%), fexA (99.72%), ant(9)-Ia (100%) |
| MN831418 | optrA_V | region | *Ec. faecium* | optrA (99.69%), fexA (99.72%) |
| MN831419 | optrA_VI | region | *Ec. faecalis* | optrA (99.9%), fexA (99.65%) |

## 3. Generated outputs — original run

```
work/
├── fulltext.xml
├── genbank/
│   ├── MN831410.gb / .fasta  ...  MN831419.gb / .fasta   (20 files)
│   └── pE394_KP399637.fasta
├── refs/
│   ├── AMR_CDS.fa                          (9,712 alleles)
│   ├── optrA.fasta                         (NG_048023)
│   ├── from_gb/optra_MN83141x.fasta        (8 extracted CDS)
│   └── *_db.{nhr,nin,nsq}                  (BLAST dbs)
├── amr_screen.py
├── amr_screen_results.json
└── llm_judge.py

report/
├── REPORT.md
├── REPORT.tex                              (this backfill)
├── brief.md, attempt_log.md, artifact_harvest.md
├── workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json  (backfill)
└── evidence/
    ├── amr_screen_results.json             (C1)
    ├── pM17-0149_vs_pE394.tsv              (C2, full-length HSPs)
    ├── poxtA_shared_regions.tsv            (C3, shared cassette blocks)
    ├── optrA_vs_canonical.tsv              (C4, allele nt-diffs)
    └── llm_judge_verdict.txt               (PARTIAL, 4/10, 4/4)
```

## 4. Generated outputs — independent reproduction (2026-07-03)

```
report/evidence/independent_reproduction/
├── downloads/                              (fresh efetch, SHA256 logged)
│   ├── MN831410..MN831419 .fasta/.gb
│   ├── pE394_KP399637.fasta
│   ├── optrA_NG_048023.fasta
│   └── optra_cds_all.fasta
├── code/
│   └── run_reproduction.sh                 (end-to-end script)
├── logs/
│   ├── seq_lengths.tsv
│   ├── downloads.sha256
│   ├── abricate_ncbi.tsv                   (C1 primary, different tool)
│   ├── abricate_resfinder.tsv              (C1 cross-check)
│   ├── c2_mn831410_vs_pE394.tsv            (C2)
│   ├── c3_poxtA_shared_blocks.tsv          (C3)
│   └── c4_optrA_vs_canonical.tsv           (C4)
├── indep_summary.json                      (structured all-claim summary)
├── comparison.md                           (36-row exact-match table)
└── tool_versions.txt                       (pinned versions)
```

## 5. Key numeric evidence (what the artifacts prove)

| Claim | Number | Artifact |
|---|---|---|
| C1: optrA detection | 8/10 records at ≥ 99.5 % id, full coverage | `amr_screen_results.json` + `abricate_ncbi.tsv` |
| C1: poxtA detection | 2/2 poxtA plasmids at 100 %, full cov | same |
| C1: cfr(D) detection | 1/1 co-carriage isolate (MN831413) at 100 % | same |
| C2: MN831410 length | 36,331 bp (exact) | `seq_lengths.tsv` |
| C2: MN831410 vs pE394 | **99.997 % weighted identity, 1 mismatch total over 36,331 bp** | `pM17-0149_vs_pE394.tsv` |
| C2: pE349 → pE394 correction | No plasmid literally named pE349 of size 36,331 bp; pE394 (KP399637) is exact match | independent finding |
| C3: MN831411 length | 21,849 bp (exact) | `seq_lengths.tsv` |
| C3: poxtA cassette | poxtA 17,064–18,693, flanking IS*1216E* tnpA 16,330–17,017 + 19,651–20,338 | Biopython feature parse |
| C3: shared blocks MN831411/MN831412 | ~4,109 bp @ 99.9 % + 4,426 bp | `poxtA_shared_regions.tsv` |
| C4: optrA nt-diff vector vs NG_048023 | {0, 1, 2, 2, 2, 3, 6, 6} = **6 distinct alleles** across both species | `optrA_vs_canonical.tsv` |
| Judge verdict | PARTIAL / Coverage 4/10 / Agreement 4/4 | `llm_judge_verdict.txt` |
| Independent re-verification | **36/36 numbers matched at 2-decimal precision** | `comparison.md` |

## 6. What was NOT produced (and why)

| Not produced | Reason |
|---|---|
| Prevalence re-derivation (22.7 %, C5) | Table S1 metadata for 154 isolates not machine-readable / not deposited |
| cgMLST / wgMLST clustering (CI–CVII, C6) | Per-isolate raw MiSeq reads never deposited (no SRA) |
| 23S G2576T copy-number (C7) | Same — no raw reads → cannot map to 23S rRNA copies |
| Assembly re-run from raw reads | Raw reads not public; can only validate deposited assemblies, not the assembly process |
| Livestock/food-reservoir attribution (OQ1) | Comparator sequences not part of Egan deposition |
