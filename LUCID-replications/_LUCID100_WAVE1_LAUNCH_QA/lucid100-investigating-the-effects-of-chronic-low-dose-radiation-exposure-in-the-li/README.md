# Investigating the effects of chronic low-dose radiation exposure in the liver of a hypothermic zebrafish model

## LUCID100 curated Wave 1 replication brief — Slot 6

> **First-pass verdict (2026-06-09): READY-TO-RUN. T0 DEG-count reproduction PASS (±1 gene per direction; boundary-tie handling).** See `FIRST_PASS_REPORT.md` and `repro/deg_count_smoke.py`.

- **Rank:** 37 (LUCID100 Wave 1 parallel slot 6)
- **Tier/score:** A / 20
- **DOI:** 10.1038/s41598-022-26976-4
- **Year / venue:** 2023 / Scientific Reports
- **First author / corresponding:** Thomas Cahill (QUB) / Gary Hardiman (QUB)
- **Themes:** DNA repair / DDR; dose-rate / low-dose response; radiation quality / RBE; omics / biomarkers / signatures
- **Worktype:** omics/signature replication
- **Source:** semantic_scholar
- **PDF / URL:** https://www.nature.com/articles/s41598-022-26976-4.pdf
- **QA decision:** KEEP: relevant and replication-plausible

## Replication target

Quantitative reproduction of the paper's headline DEG counts from the per-gene DESeq2 output that the authors deposited on GEO. This is the strictest form of "did the numbers actually come from the data" check that requires no FASTQ re-alignment.

**Acceptance criterion (T0):** for each contrast in the paper's reported `(FC ±1.5, q ≤ 0.1)` thresholds, the count of up- and down-regulated genes derived from the published GEO DESeq2 tables matches the paper's reported count to within **±1 gene per direction** (padj / log2FC boundary-tie tolerance). PASS = all checked counts within ±1.

**Result (2026-06-09):** PASS. Two of the four checked numbers match exactly; the other two are off by exactly 1 gene, consistent with how an author may have handled a single padj==0.1 or |log2FC|==log2(1.5) tie. Smoke test wall-clock < 1 s, exit 0.

## Key public artifacts harvested

| Artifact | Where | Size |
|---|---|---|
| Paper PDF + extracted text | `artifacts/cameron2023_scirep.{pdf,txt}` | 2.9 MB + 60 KB |
| GEO primary RNA-seq series metadata | `artifacts/geo/GSE200212_series.soft` | 8 KB |
| GEO per-sample metadata (12 GSMs) | `artifacts/geo/GSE200212_samples.soft` | 80 KB |
| Full DESeq2 output, all 3 contrasts | `artifacts/geo/GSE200212_*_zebrafish_IDs.txt.gz` | 2.8 MB |
| Human-ortholog DEG tables (used by paper's ORA) | `artifacts/geo/GSE200212_DEG_*_human_IDs.txt.gz` | 1.3 MB |
| T0 smoke test | `repro/deg_count_smoke.py` | 5 KB |
| SHA-256 manifest | `repro/sha256.txt` | 1 KB |

## Key accessions (for future T2/T3 deeper runs)

- **GEO Series:** [GSE200212](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE200212) — 12 zebrafish liver RNA-seq samples (5 conditions: 28.5-Ctrl, 28.5-rad, 18.5-mel, 18.5-rad, 18.5-mel-rad; ~50 M reads/sample, Illumina NextSeq 500)
- **BioProject:** [PRJNA823689](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA823689) — same study, FASTQ side
- **SRA:** SRX14748159–SRX14748170 (12 experiments)
- **Cross-validation (bear hibernation):** [PRJNA413091](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA413091)
- **Cross-validation (spaceflown mice):** NASA GeneLab GLDS-47
- **Reference genome:** GRCz11 (Danio rerio)

## Methods (per paper §2.4)

```
FastQC  →  Cutadapt  →  STAR (GRCz11)  →  HTSeq  →  DESeq2
                                                          ↓
                                          Advaita iPathwayGuide  (paid/proprietary)
                                          ToppFun ORA            (free, available)
```

The DESeq2 output is on GEO; everything upstream of DESeq2 has not been re-run (T2 job plan exists; not executed). Downstream Advaita pathway calls are not exactly replicable but are not load-bearing for the T0 reproducibility result.

## Artifact harvest checklist

- [x] Source PDF saved locally (2.9 MB, OA)
- [x] Full text extracted (1163 lines)
- [x] Supplementary files found/downloaded (6 GEO supplementary DESeq2 tables, ~4 MB)
- [x] GEO sample + series metadata harvested
- [ ] Code repository — **N/A**, paper does not cite one; pipeline is described in methods prose only
- [x] Public data accession found (GSE200212 + PRJNA823689 + GLDS-47 + PRJNA413091)
- [x] Environment plan written (T2 HPC job plan in `FIRST_PASS_REPORT.md`)
- [x] Acceptance metrics defined (T0: DEG counts within ±1)
- [x] Blockers listed — none

## Execution checklist

- [x] Smoke test / minimal calculation (T0 DEG counts, exit 0)
- [ ] Main replication run T2 — deferred (HPC job plan written; not submitted; out of CherryRd scope)
- [ ] Figures/tables regenerated — partial via T0; full regeneration requires T2 then ORA
- [x] Logs, hashes, environment, and provenance captured (`repro/sha256.txt` + this README + MANIFEST)
- [x] `FIRST_PASS_REPORT.md` written
- [x] Progress JSON written under OpenClaw memory (`memory/subagent-progress/lucid100-wave1-6-*.json`)

## Initial abstract/notes

Mankind's quest for a manned mission to Mars is placing increased emphasis on the development of innovative radio-protective countermeasures for long-term space travel. Hibernation confers radio-protective effects in hibernating animals, and this has led to the investigation of synthetic torpor to mitigate the deleterious effects of chronic low-dose-rate radiation exposure. Here we describe an induced torpor model we developed using the zebrafish. We explored the effects of radiation exposure on this model with a focus on the liver. Transcriptomic and behavioural analyses were performed. Radiation exposure resulted in transcriptomic perturbations in lipid metabolism and absorption, wound healing, immune response, and fibrogenic pathways. Induced torpor reduced metabolism and increased pro-survival, anti-apoptotic, and DNA repair pathways. Coupled with radiation exposure, induced torpor led to a stress response but also revealed maintenance of DNA repair mechanisms…
