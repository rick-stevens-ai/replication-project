# Artifacts Summary — BVBRC-76 (Carpi 2021 replication)

**Report date.** 2026-07-03
**Verdict.** PARTIAL REPLICATION
**Cohort.** 124 unique *Lactiplantibacillus plantarum* complete RefSeq assemblies (paper N=127; delta explained by 6-year NCBI curation churn).

All paths are relative to `~/Dropbox/REPLICATE-PROJECT/BVBRC-76-lplantarum-pangenome-carpi2021/` unless noted. Heavyweight intermediates (Prokka per-genome outputs and full Roary output tree) live on `uicgpu:/gpustor/stevens/bvbrc76-lp/` — they are too large for Dropbox and not needed to reproduce the top-level numbers.

---

## 1. Report deliverables (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Human-readable narrative report (this replication's canonical text). |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section. |
| `open_questions.json` | 5 open questions grounded in Carpi 2021's refined-taxonomy scope. |
| `workflow.md` | End-to-end computational workflow (this replication). |
| `artifacts_summary.md` | This file — full inventory. |
| `failure_analysis.md` | What didn't work and why (Wiley Cloudflare, Anthropic 502, etc.). |

---

## 2. Evidence (`report/evidence/`) — numerical outputs of the replication

| File | Bytes | Origin | Purpose |
|---|---:|---|---|
| `summary_statistics.txt` | 206 | Roary 3.13.0 on 124-genome pan-genome | The four-way partition (core / soft-core / shell / cloud / total). This is the direct counterpart of the paper's Table 1. |
| `rarefaction_summary.txt` | ~2 KB | Derived from Roary Rtabs | Per-N mean pan-genome size, mean core size, mean new-genes-per-step. Feeds the Heaps' Law fit (γ = 0.385). |
| `number_of_conserved_genes.Rtab` | 6,200 | Roary rarefaction (10 perms × 124) | Core trajectory as N grows. |
| `number_of_genes_in_pan_genome.Rtab` | 7,107 | Roary rarefaction (10 perms × 124) | Pan-genome trajectory as N grows — this is what Heaps' Law is fit on. |
| `number_of_new_genes.Rtab` | 4,064 | Roary rarefaction (10 perms × 124) | Marginal new genes per added genome — used to verify Claim C3b. |
| `number_of_unique_genes.Rtab` | 6,199 | Roary rarefaction (10 perms × 124) | Singletons per genome as N grows. |
| `blast_identity_frequency.Rtab` | 55 | Roary all-vs-all BLASTP identity histogram | Distribution of BLASTP percent-identity across all vs all — sanity check on clustering. |
| `gene_presence_absence.csv` | 14,812,417 | Roary per-cluster full annotation | 16,522 cluster rows × 124 genome cols + annotation columns. The full pan-genome matrix. |
| `judge_results.json` | ~5 KB | Three LLM judges (Argo, free) | Raw JSON responses + scores from `argo:gpt-5.2`, `argo:gpt-5.4`, `argo:gemini-2.5-pro`. Majority = PARTIAL (3/3). |

---

## 3. Working files (`work/`)

| File | Purpose |
|---|---|
| `lp_all124_accessions.txt` | 124 RefSeq GCF accessions used by the replication. |
| `lp_all124_meta.tsv` | 125 lines: accession → strain → release_date (header + 124 data rows). |
| `paper.pdf` | PMC OA copy of Carpi et al. 2021 (1.2 MB). Used as ground-truth reference during report writing. |

---

## 4. Off-Dropbox large artifacts (`uicgpu:/gpustor/stevens/bvbrc76-lp/`)

These sit on uicgpu because they are too large for Dropbox and are not required to reproduce the headline numbers. They are recoverable by rerunning the Prokka + Roary stages from `work/lp_all124_accessions.txt` (see `workflow.md`).

| Path | Size | Contents |
|---|---:|---|
| `prokka/` | ~1.8 GB | 124 per-genome Prokka annotation directories (each with GFF, GBK, FAA, FNA, TSV, TXT, ERR, LOG). |
| `roary/` | ~300 MB | Full Roary output tree including all pan-genome matrices, per-cluster FASTAs, core-genome alignment, tree files. |
| `gffs/` | ~200 MB | Flat directory of the 124 Prokka GFF3 files (input to Roary). |
| `lp124_pkg/` | ~400 MB | Rehydrated NCBI Datasets download package (source FASTAs). |

---

## 5. Key numerical results (paper vs replication)

| Quantity | Paper (N=127) | Replication (N=124) | Δ |
|---|---:|---:|---:|
| Core (≥99% strains) | 1,436 | 1,558 | +8.5% |
| Soft-core (95–99%) | 414 | 330 | −20.3% |
| Shell (15–95%) | 1,858 | 1,845 | −0.7% |
| Cloud (<15%) | 13,203 | 12,789 | −3.1% |
| **Total pan-genome** | **16,911** | **16,522** | **−2.3%** |
| **Core + soft-core** | **1,850** | **1,888** | **+2.1%** |
| Heaps' γ | <1 (open, qualitative) | **0.3854** | independently open |
| New genes/step at N=100 | >0 (qualitative) | **43.8** | replicated |
| New genes/step at N=124 | not reported | **44.4** | consistent with continued openness |

---

## 6. LLM-judge scores (Argo, free endpoint)

| Judge | Verdict | Coverage | Agreement | Confidence |
|---|---|---:|---:|---:|
| argo:gpt-5.2 | PARTIAL | 0.75 | 0.78 | 0.72 |
| argo:gpt-5.4 | PARTIAL | 0.82 | 0.86 | 0.88 |
| argo:gemini-2.5-pro | PARTIAL | 0.85 | 0.90 | 0.95 |
| **Mean** | **PARTIAL (3/3)** | **0.81** | **0.85** | **0.85** |

Argo Anthropic (opus-4.7 / opus-4.8) 502'd; replaced with gpt-5.4 + gemini-2.5-pro to keep three independent families.

---

## 7. What is NOT in the artifact set (and why)

- **Wiley supplementary Table S5** — needed for Claim C4 (PMG core fraction). Cloudflare CAPTCHA blocks the ZIP fetch. See `failure_analysis.md`.
- **Parsnp core-SNP phylogeny (paper Fig 4)** — reproducible with the same GFF/FASTA set but outside the scope of a "headline claims" replication.
- **OrthoFinder / FastANI sanity plots (paper Figs 1, 2)** — same rationale.
- **Plasmid / prophage / CRISPR / bacteriocin counts** — downstream analyses that need the paper's own tool zoo (PlasmidFinder, PHASTER, BAGEL4, CRISPRCasFinder, RAST); not required for the top-level pan-genome verdict.

---

## 8. Reproducibility

See Appendix B of `REPORT.md` for the copy-paste one-liner script that reproduces the numbers in Section 4 of `REPORT.md`. Expected wall time on a 24-core box: ~1 hour end-to-end.
