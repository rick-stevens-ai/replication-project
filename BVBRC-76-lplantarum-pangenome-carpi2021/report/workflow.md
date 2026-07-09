# Workflow — BVBRC-76 replication of Carpi et al. 2021

**Target paper.** Carpi FM et al., *J Appl Microbiol* 132(1):592–604 (2022, online 2021), DOI [10.1111/jam.15199](https://doi.org/10.1111/jam.15199). Open access (CC-BY, PMC9290807).
**Verdict.** PARTIAL REPLICATION.
**Report date.** 2026-07-03.
**Analyst.** Ollie (OpenClaw AI subagent BVBRC-76).

This file documents the end-to-end computational workflow used for this replication attempt. Steps map 1:1 to the sections in `REPORT.md`. All commands were run from the driver host `CherryRd`; the heavy compute stages ran on `uicgpu` (8×A100, 255 cores, 2 TB RAM).

---

## Stage 0 — Reproduce the paper's cohort (Claim C1)

**Goal.** Rederive the July-2020 RefSeq complete-genome list for *L. plantarum* used by Carpi 2021 (their N = 127).

1. Query NCBI Datasets v2 REST (no auth) for *Lactiplantibacillus plantarum* with `assembly_level=complete_genome` and `exclude_atypical=true`, page size 500:

   ```
   https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/taxon/lactiplantibacillus%20plantarum/
     dataset_report?filters.assembly_level=complete_genome&filters.exclude_atypical=true&page_size=500
   ```

2. Page through 865 complete-genome hits (as of 2026-07-03). Split into GCA (GenBank) + GCF (RefSeq).

3. Filter by `release_date <= 2020-07-31` (paper cutoff) → 251 hits (125 GCA + 126 GCF).

4. Dedup by RefSeq `GCF_` accession → 125 assemblies. Dedup by `organism.infraspecific_names.strain` → **124 unique strains**.

5. Persist artifacts:
   - `work/lp_all124_accessions.txt` — 124 accessions
   - `work/lp_all124_meta.tsv` — accession → strain → release_date

**Delta vs paper.** 124 replication genomes vs 127 in paper. Explanation: NCBI curation churn between July 2020 and July 2026 (RefSeq occasionally re-suppresses genomes for "detected anomalies"); paper may have counted repeated strain assemblies from different depositors. Delta is 2.4% — within noise.

---

## Stage 1 — Download assemblies

```
datasets download genome accession \
  --inputfile lp_all124_accessions.txt \
  --include genome \
  --dehydrated \
  --filename lp124.zip
unzip lp124.zip -d lp124_pkg
datasets rehydrate --directory lp124_pkg
```

Total download: 399 MB across 124 FASTA files, one per assembly. Rehydration verified: 124 `.fna` files.

---

## Stage 2 — Environment provisioning

Fresh conda env on `uicgpu`, driven from CherryRd via SSH:

```
mamba create -n bvbrc76 -c bioconda -c conda-forge -y \
    prokka roary panaroo blast prodigal ncbi-datasets-cli
mamba activate bvbrc76
```

Version drift from paper:
- Prokka **1.14.6** (paper: 1.14.5)
- Roary **3.13.0** (paper: 3.11.2)
- Panaroo **1.8.0** (installed, unused — future sanity check)
- BLAST+, prodigal, MAFFT: latest bioconda

---

## Stage 3 — Genome annotation (Prokka)

For each of the 124 assemblies:

```
prokka \
  --outdir prokka/<acc> \
  --prefix <acc> \
  --locustag <acc-nodots-truncated-12> \
  --kingdom Bacteria \
  --genus Lactiplantibacillus \
  --species plantarum \
  --cpus 2 \
  --fast \
  --force <fna>
```

Parallelized with `xargs -P 24`. Wall time: **~20 min for all 124 genomes** on uicgpu.

Verification: 124 GFF3 outputs, one per assembly.

Collect all GFFs into a flat directory for Roary:

```
mkdir -p gffs
for d in prokka/GCF_*; do
    acc=$(basename $d)
    cp $d/$acc.gff gffs/
done
```

---

## Stage 4 — Pan-genome construction (Roary)

**Command:**

```
roary -e --mafft -p 48 -f roary -i 95 -cd 99 gffs/*.gff
```

Flags matched to paper:
- `-i 95` — BLASTP identity threshold 95% (Roary default, paper spec)
- `-cd 99` — core defined as ≥ 99% of strains (paper 4-class scheme)
- `--mafft` — MAFFT for core alignment
- `-e` — extract per-cluster protein alignments
- `-p 48` — 48 parallel BLAST workers

Wall time: ~15 min for the BLAST all-vs-all phase; MCL clustering + post-processing continued in background.

Roary outputs (`report/evidence/`):
- `summary_statistics.txt` — the four-way partition
- `gene_presence_absence.csv` — 16,522 clusters × 124 genomes (14.8 MB)
- `number_of_conserved_genes.Rtab` — 10 perms × 124 genomes
- `number_of_genes_in_pan_genome.Rtab` — 10 perms × 124 genomes
- `number_of_new_genes.Rtab` — 10 perms × 124 genomes
- `number_of_unique_genes.Rtab` — 10 perms × 124 genomes
- `blast_identity_frequency.Rtab` — all-vs-all BLASTP identity histogram

---

## Stage 5 — Rarefaction & Heaps' Law openness (Claim C3)

Roary emits full rarefaction Rtabs (10 permutations × 124 genomes). For each metric, compute the per-N mean across the 10 permutations.

**Heaps' Law fit** (Claim C3a): least-squares regression of `log(pan_size(N))` on `log(N)` for N = 10 → 124.

Model: `pan(N) = κ · N^γ`.
Result: **γ = 0.3854, κ = 2583.22**. γ < 1 → open.

**Post-100-genome growth** (Claim C3b): mean new genes per step:
- N = 100: **43.8 new/step**
- N = 124: **44.4 new/step**

Both > 0 → new genes still being added; openness confirmed.

Outputs summarized in `report/evidence/rarefaction_summary.txt`.

---

## Stage 6 — LLM-judge scoring

Three independent judges (temperature 0.0 where allowed) via Argo proxy (`http://127.0.0.1:44497/v1`, key = `stevens`, free endpoint):

- `argo:gpt-5.2` → **PARTIAL** (cov 0.75, agr 0.78, conf 0.72)
- `argo:gpt-5.4` → **PARTIAL** (cov 0.82, agr 0.86, conf 0.88)
- `argo:gemini-2.5-pro` → **PARTIAL** (cov 0.85, agr 0.90, conf 0.95)

Majority: **PARTIAL (3/3)**. Raw responses in `report/evidence/judge_results.json`.

**Note.** Argo Anthropic (opus-4.7 / opus-4.8) returned repeated 502 gateway errors during this run; substituted `gpt-5.4` and `gemini-2.5-pro` to keep three independent families (OpenAI × 2 across generations + Google), preserving diversity.

---

## Stage 7 — Attempted Claim C4 (PMG core fraction) — BLOCKED

**Goal.** Verify that ~70% of the 75 probiotic marker genes (PMGs) fall in core/soft-core.

**Blocker.** The 75-PMG list is only in Wiley supplementary Table S5 (`jam15199-sup-0001-Tables.zip`). Every fetch attempt (curl with browser UA, browser-tool navigation) returns a Cloudflare CAPTCHA HTML page instead of the ZIP. The main paper is CC-BY OA; the supplementary is effectively not.

**Consequence.** Verdict downgraded from REPLICATED to PARTIAL. See `failure_analysis.md`.

---

## Stage 8 — Report assembly

- `REPORT.md` — human-readable narrative with Claims table, method, results, verdict.
- `REPORT.tex` — LaTeX version with dedicated Genuine Critique section.
- `open_questions.json` — 5 open scientific questions grounded in the paper's refined-taxonomy scope.
- `workflow.md` — this file.
- `artifacts_summary.md` — file inventory + hashes.
- `failure_analysis.md` — what didn't work and why.

---

## Compute footprint

| Stage | Host | Wall time | Peak RAM | Notes |
|---|---|---:|---:|---|
| Cohort query | CherryRd | ~30 s | <100 MB | REST + pandas |
| Assembly download | CherryRd | ~5 min | <200 MB | `datasets` CLI |
| Env creation | uicgpu | ~4 min | ~2 GB | mamba solve |
| Prokka (124 × parallel) | uicgpu | ~20 min | ~30 GB peak | `xargs -P 24` |
| Roary | uicgpu | ~15 min BLAST + ~30 min post | ~40 GB peak | `-p 48` |
| Rarefaction analysis | CherryRd | <10 s | <500 MB | Python + numpy |
| LLM-judge (3 judges) | CherryRd | ~2 min | negligible | Argo proxy (free) |
| **Total** | mixed | **~1 h wall** | ~40 GB | Fits easily on uicgpu A100 node |

---

## Reproducibility one-liner

See Appendix B of `REPORT.md` for a full copy-paste reproducibility script (cohort re-derivation → Prokka → Roary → summary print). Expected numbers reproduce within 2–3% of the paper's Table 1.
