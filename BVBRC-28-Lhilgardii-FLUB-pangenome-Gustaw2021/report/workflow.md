# Workflow — Gustaw 2021 *L. hilgardii* FLUB Pangenome Replication (BVBRC-28)

**Target paper:** Gustaw K, Michalak M, Polak-Berecka M, Waśko A. *Int J Mol Sci* 22(7):3780 (2021). DOI: 10.3390/ijms22073780.
**Verdict:** PARTIAL REPLICATION (strong; borderline REPLICATED).
**Compute host:** uicgpu (8×A100; CPU-only used).
**Conda env:** `bvbrc28` (prokka 1.14, roary, fastani, ncbi-datasets-cli, prodigal, mmseqs2, mafft 7.526, fasttree, biopython 1.87).
**LLM judge:** Argo `argo:gpt-5.2` via `localhost:44497` (free).

---

## 0. Setup

```bash
mamba create -y -p ./env -c conda-forge -c bioconda \
    prokka roary fastani ncbi-datasets-cli \
    prodigal mmseqs2 mafft fasttree biopython
conda activate ./env
```

All inputs are free (NCBI Datasets v2alpha REST + ENA browser API); no auth required.

---

## 1. Genome retrieval (paper-era public *L. hilgardii* set)

Pulled 6 assemblies from NCBI Datasets:

| Accession | Strain | Level |
|---|---|---|
| GCF_009832765.1 | **FLUB** (subject) | Complete |
| GCF_004354795.1 | ATCC 8290 (paper reference) | Scaffold |
| GCF_001434655.1 | DSM 20176 (= ATCC 8290 deposit) | Contig |
| GCF_011765585.1 | LMG 07934 (NZ_CP050262) | Complete |
| GCF_000159175.1 | ATCC 27305 (= *L. brevis* gravesensis label) | Scaffold |
| GCF_008694025.1 | LH500 | Complete |

MGYG-HGUT-01333 FASTA pulled separately from ENA browser (no GCA sequence via NCBI).

```bash
for acc in GCF_009832765.1 GCF_004354795.1 GCF_001434655.1 \
           GCF_011765585.1 GCF_000159175.1 GCF_008694025.1; do
  curl -sS -o $acc.zip \
    "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/$acc/download?include_annotation_type=GENOME_FASTA"
  unzip -oq $acc.zip -d $acc
  cp $(find $acc -name '*.fna' | head -1) $acc.fna
done
```

---

## 2. Genome statistics (→ C1)

Pure-Python `gstats.py` computes total length, contig count, GC%, N50 per assembly.

- Output: `evidence/genome_stats.json`.
- **Cross-validation:** per-replicon parser `work/genome_stats.py` matches every chromosome/plasmid length against the paper's Table 1 to the base pair (CP047121–126.1).

---

## 3. Whole-genome ANI (→ C5)

```bash
fastANI --ql list --rl list -o ani.tsv    # all-vs-all over the 6 genomes
```

- Output: `evidence/fastani_all.tsv`.
- Anchor result: FLUB ↔ ATCC 27305 = 99.77% ANI (paper 99.909%).

---

## 4. Annotation (→ C2)

```bash
for a in *.fna; do
  prokka --genus Lentilactobacillus --species hilgardii \
         --prefix ${a%.fna} --outdir prokka/${a%.fna} $a
done
```

- Prokka 1.14 replaces the paper's PGAP+PATRIC combined annotation.
- Expected ~4% CDS delta vs. paper; qualitative "FLUB richest CDS" preserved.
- CDS counts: `evidence/cds_counts.txt`.

---

## 5. Pangenome pipeline 1 — Roary (→ C3, C4)

```bash
# 5-genome paper-equivalent set
roary -e -n -i 95 -f roary5 \
      prokka/{FLUB,ATCC8290,DSM20176,LMG07934,ATCC27305}/*.gff
# 6-genome set (adds LH500)
roary -e -n -i 95 -f roary6 prokka/*/*.gff
python3 uniq.py roary5    # FLUB singletons -> C4
python3 uniq.py roary6
```

- Outputs: `evidence/roary5_summary.txt`, `evidence/roary6_summary.txt`, `evidence/pangenome{5,6}_uniq.txt`.
- **Perl gotcha (documented in attempt_log):** Roary post-analysis initially crashed on a missing `File::Find::Rule` module — a perl-5.22-vs-5.26 include-path mismatch in the conda env. Fix: place the pure-Perl module on the 5.22 include path, re-run.

---

## 6. Pangenome pipeline 2 — Prodigal + mmseqs2 (cross-validation → C3, C4)

Fully independent; no reuse of Prokka/Roary intermediates.

```bash
# Uniform gene calling
for a in *.fna; do
  prodigal -i $a -a prodigal/${a%.fna}.faa -f gff -o prodigal/${a%.fna}.gff -p single
done
# Cluster at Roary-equivalent stringency: 95% identity, 0.7 coverage
mmseqs easy-cluster prodigal/*.faa mmseqs_out /tmp/mmseqs_tmp \
       --min-seq-id 0.95 -c 0.7 --cov-mode 0
```

- Outputs: `evidence/mmseqs_clusters.tsv`, `evidence/pangenome_result.json`.
- Analyzer: `work/pangenome_analyze.py` → per-strain singleton counts, core/accessory/singleton partition.
- Result brackets the paper: 4190 total clusters vs. paper 4181; FLUB singletons 260 vs. 266.

---

## 7. Core-genome ML phylogeny (cross-validation → C_phylo)

```bash
# Extract 400 single-copy core clusters from mmseqs output; MAFFT-align each; concat.
python3 work/coregenome_tree.py     # builds 125,120-aa supermatrix
FastTree -lg -gamma core_supermatrix.faa > core_genome.nwk
```

- Outputs: `evidence/core_genome.nwk`, `evidence/core_tree_result.json`.
- Recovered topology: `(LH500,DSM20176,(LMG07934,(FLUB,MGYG)));` — matches the paper's PATRIC Codon Tree.

---

## 8. LLM-judge scoring

Both passes' evidence bundles fed to Argo `argo:gpt-5.2` (free).

- Pass 1 (Roary only): PARTIAL, coverage 6/6, 2 agree / 4 partial / 0 disagree. `evidence/llm_judge_response.json`.
- Consolidated (pipelines 1+2 + core tree + ANI + per-replicon): REPLICATED, coverage 7/7, 4 agree / 3 partial / 0 disagree. `evidence/llm_judge_consolidated.json`.
- No regex scoring. Headline verdict kept at PARTIAL-strong per project's conservative-scoring rule while dDDH and wet-lab phenotypes remain unreproduced.

---

## 9. Wall-clock

~15 min total on uicgpu CPU (dominant costs: 6× Prokka annotation ~6 min; Roary 5-genome ~3 min; mmseqs2 clustering ~1 min; MAFFT alignments ~2 min; everything else <1 min).

---

## Data flow (one-page)

```
NCBI Datasets (6 GCF) + ENA (MGYG)
        │
        ▼
   *.fna files ─────────────────────────────────────┐
        │                                           │
        ├── gstats.py ────────► genome_stats.json (C1)
        ├── fastANI  ────────► fastani_all.tsv    (C5)
        │
        ├── Prokka ─► GFF3 ─► Roary(i=95) ─► roary{5,6}_summary + uniq (C2,C3,C4)
        │
        └── Prodigal ─► FAA ─► mmseqs2 ─► mmseqs_clusters ─► pangenome_result.json (C3,C4)
                                          │
                                          └── coregenome_tree.py ─► MAFFT ─► FastTree ─► core_genome.nwk (C_phylo)
                                                                                            │
                                                                                            ▼
                                                          all evidence ─► Argo gpt-5.2 judge ─► llm_judge_*.json
```
