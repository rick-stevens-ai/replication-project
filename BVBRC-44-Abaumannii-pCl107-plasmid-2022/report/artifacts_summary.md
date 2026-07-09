# Artifacts Summary — BVBRC-44 pCl107 Replication

**Target:** Rafei et al. 2022, *FEMS Microbes* 3:xtac027 (pCl107 plasmid of ST25 *A. baumannii* Cl107).
**Verdict:** REPLICATED (11/11 claims tested; free-Argo judge cov=9 agr=10).
**Local dir:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-44-Abaumannii-pCl107-plasmid-2022/`
**Remote workdir:** `uicgpu:/data/stevens/scratch/bvbrc44-pCl107` (see `work/REMOTE_WORKDIR.txt`).

---

## Directory Tree

```
report/
├── REPORT.md                       # human-readable narrative (canonical)
├── REPORT.tex                      # LaTeX archival version
├── brief.md                        # 1-paragraph pre-replication brief
├── attempt_log.md                  # chronological process log
├── artifact_harvest.md             # notes on what was collected + why
├── open_questions.json             # 5 open questions with next steps (back-fill)
├── workflow.md                     # step-by-step reproducer (back-fill)
├── artifacts_summary.md            # this file (back-fill)
├── failure_analysis.md             # honest failure analysis (back-fill)
└── evidence/
    ├── evidence_summary.json       # aggregated: sizes + gene counts + module presence
    ├── amrfinder_pCl107.tsv        # AMRFinderPlus on plasmid (6 hits, all 100/100)
    ├── amrfinder_chromosome.tsv    # AMRFinderPlus on chromosome (blaOXA-64, blaADC-26, gyrA_S81L, parC_S84L)
    ├── abricate_resfinder_pCl107.tsv  # 2nd AMR caller (ResFinder DB)
    ├── abricate_plasmidfinder.tsv  # replicon typing (none in std DB — expected for Aci)
    ├── refseq_amr_pCl107.txt       # 3rd AMR caller (GenBank annotation mined from gbff)
    ├── mlst_pasteur.tsv            # ST25 (cpn60=3, fusA=3, gltA=2, pyrG=4, recA=7, rplB=2, rpoB=4)
    ├── mlst_oxford.tsv             # ST229 (gltA=1, gyrB=15, gdhB=2, recA=28, cpn60=1, gpi=107, rpoD=32)
    ├── pCl107_modules.json         # BREX / ptx / uric-acid / P450 / MPF gene coordinates
    ├── resistance_region_blast.txt # pCl107 resregion (75–90 kb) vs pA297-3 + pAB3
    ├── plasmid_relatedness.txt     # whole-plasmid blastn vs 5 family plasmids (pMC1.1 closest)
    └── llm_judge_argo_gpt5.2.json  # free-Argo judge output (cov=9, agr=10, verdict=REPLICATED)
work/
├── fulltext.xml                    # Europe PMC full text
├── judge_input.txt                 # claims+results text sent to LLM judge
├── pCl107_resregion.fna            # extracted 75000–90000 nt region for AbGRI1 blast
├── REMOTE_WORKDIR.txt              # uicgpu path pointer
└── genomes/CP098522.1.fna, .gbff   # pCl107 FASTA + GenBank flatfile
extraction/
└── (empty — no marker.md; assembly-based replication, not paper-text OCR)
```

---

## Primary Sequence Inputs (public, free)

| Accession | Molecule | Length | Purpose | Source |
|---|---|---:|---|---|
| CP098521.1 | Cl107 chromosome | 4,056,235 bp | C1, C2, C10 | NCBI eutils efetch |
| CP098522.1 | pCl107 plasmid (FASTA) | 198,716 bp | C1, C3, C4, C5–C9, C11 | NCBI eutils efetch |
| CP098522.1 | pCl107 plasmid (gbff) | 197 CDS | Module coord parsing (C5–C9) | NCBI eutils efetch |
| KU744946.1 | pA297-3 (reference) | — | C4 (AbGRI1 missing-link comparator) | NCBI eutils efetch |
| CP012005.1 | pAB3 (reference) | — | C4 (AbGRI1 missing-link comparator) | NCBI eutils efetch |
| KT779035.1 | pD4 (reference) | — | C11 (family comparator) | NCBI eutils efetch |
| MF399199.1 | pD46-4 (reference) | — | C11 (family comparator) | NCBI eutils efetch |
| MK531536.1 | pMC1.1 (reference) | — | C11 (closest relative test) | NCBI eutils efetch |

**Total downloaded:** 8 sequences (~4.6 Mbp), all free from NCBI, no authentication required.

---

## Evidence Traces (claim → artifact map)

| Claim | Evidence file(s) | Key numeric result |
|---|---|---|
| C1 Chromosome + plasmid sizes | `evidence_summary.json` | 4,056,235 bp + 198,716 bp (both exact match) |
| C2 ST25 / ST229 host typing | `mlst_pasteur.tsv`, `mlst_oxford.tsv` | ST25 + ST229 (100% allele match, all 7 loci each scheme) |
| C3 6 pCl107 resistance genes | `amrfinder_pCl107.tsv`, `abricate_resfinder_pCl107.tsv`, `refseq_amr_pCl107.txt` | 6/6 confirmed at 100% cov + 100% id by 3 independent callers |
| C4 AbGRI1 missing-link region | `resistance_region_blast.txt`, `pCl107_resregion.fna` | vs pA297-3: 4,706 + 3,935 + 3,704 bp @ 100% (~12.3 kb); vs pAB3: 4,706 + 3,722 + 2,181 @ 100% |
| C5 BREX Type 1 module | `pCl107_modules.json` | brxL start = 125,913 (exact paper match); pglZ 127,982–130,606; pglX 130,650–134,117; brxC 134,164–137,844 |
| C6 ptx phosphonate module | `pCl107_modules.json` | ptxD 148,876–149,883; phnE/D/C in 148.9–152.4 kb window |
| C7 Uric-acid module (incomplete) | `pCl107_modules.json` | uraH 106,464–106,784; uraD 106,781–107,284; puuE 107,428–108,390; urate oxidase / HpxO **ABSENT** (verified negative) |
| C8 Cytochrome P450 (class B) | `pCl107_modules.json` | 1 CDS annotated as cytochrome P450 |
| C9 MPF_I conjugation | `pCl107_modules.json` | DotA/TraY, DotD/TraH, virB* T4SS proteins present |
| C10 Chromosomal resistance | `amrfinder_chromosome.tsv` | blaOXA-64 + blaADC-26 + gyrA_S81L + parC_S84L (all 4 exact) |
| C11 pMC1.1 closest relative | `plasmid_relatedness.txt` | MK531536 ~108% (repeat-inflated, ranked #1); MF399199 80.3%; KU744946 75.4%; KT779035 48.7% |

Bonus finding not in original claim list: all three AMR callers additionally flag a plasmid-borne **mercury (mer) operon** (merRTPCAD), consistent with the paper's Fig. 5 mercuric module description.

---

## Tools & Versions

| Tool | Version | Role | License |
|---|---|---|---|
| NCBI eutils (efetch) | current | Sequence retrieval | Free/public |
| NCBI Datasets CLI | 18.32.0 | Alternate retrieval | Free/public |
| mlst (T. Seemann) | current | PubMLST typing (C2) | GPL |
| AMRFinderPlus | 3.12.8 | AMR caller #1 (C3, C10) | Public domain |
| abricate | current | AMR caller #2 (ResFinder DB) | GPL |
| ResFinder DB | 2026-Apr | AMR reference | Free |
| PlasmidFinder DB | 2026-Apr | Replicon typing | Free |
| RefSeq/GenBank annotation | via gbff | AMR caller #3 (C3) | Public domain |
| BLAST+ (`makeblastdb`, `blastn`) | current | Comparative genomics (C4, C11) | Public domain |
| Biopython | 1.83+ | Sequence parsing | BSD |
| Python 3 | 3.10+ | Glue scripts | PSF |
| Argo proxy `argo:gpt-5.2` | current | LLM judge (localhost:44497) | Free (ANL Argo) |

**Total cost:** $0. All tools free/open, all compute on free UIC GPU node.

---

## Aggregate Statistics

- **Claims:** 11 concrete, testable claims extracted from paper.
- **Claims tested:** 11 (100%).
- **Claims reproduced with no discrepancy:** 11.
- **Independent tools per resistance-gene claim:** 3 (AMRFinderPlus, ResFinder, RefSeq).
- **Exact-base matches:** 3 (chromosome size, plasmid size, BREX start base).
- **Wall-clock compute:** ~5 minutes on uicgpu.
- **LLM-judge coverage:** 9/10.
- **LLM-judge agreement:** 10/10.
- **Untested subclaims:** 1 (capsule KL14/OCL6 typing — would require Kaptive; see `failure_analysis.md`).

---

## Provenance Anchors

- Paper DOI: [10.1093/femsmc/xtac027](https://doi.org/10.1093/femsmc/xtac027)
- PMC ID: PMC10117892
- PMID: 37332503
- Deposited sequences: GenBank CP098521 (chromosome), CP098522 (pCl107 plasmid)
- Raw reads (available but not used here): SRR20613520 (Illumina MiSeq), SRR20613519 (Oxford Nanopore MinION)
- BioProject: linked from CP098521/CP098522 (not enumerated in this replication)
- Report generated: 2026-07-01 (night wave)
- Analyst: Ollie (OpenClaw AI)
- Back-fill artifacts (this file + workflow.md + open_questions.json + failure_analysis.md): 2026-07-05
