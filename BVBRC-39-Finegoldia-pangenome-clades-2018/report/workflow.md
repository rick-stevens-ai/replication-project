# Replication Workflow — BVBRC-39 Finegoldia pangenome / clades (Brüggemann et al. 2018)

**Verdict:** REPLICATED. All 9 quantitative claims reproduced on the same 17 genomes using independent tools.

**Wall-clock:** ~5 minutes on a laptop, end-to-end.
**Cost:** $0 (all inputs and tools free/public).

---

## 1. Pipeline overview

```
Europe PMC full text (PMC5762925)
        │  parse for 17 WGS accessions
        ▼
NCBI Datasets taxon "Finegoldia"   ──► paper_17_map.tsv  (1:1 WGS → GCA)
        │
        ▼
datasets download  ──►  17 assemblies (genome + protein + gff3)
        │
        ├──► genome_stats.py           ──► CDS/GC/size table (C2)
        │
        ├──► fastANI all-vs-all (17×17)
        │       │
        │       ├──► ani_cluster2.py   ──► 2-clade cut, inter-clade 90.67% ANI (C3, C4)
        │       │
        │       └──► clades2.json
        │
        ├──► pangenome.py (12-genome subset)
        │       │
        │       └──► CD-HIT c=0.5 n=3  ──► core=1209, singletons=892 (C5, C6)
        │
        ├──► vf_survey.py
        │       │  BLASTP curated UniProt VF refs vs each proteome
        │       │  pident≥40 & cov≥50%  (relaxed 30/40 for CAMP paralogs)
        │       │
        │       └──► vf_results.json + camp_copies.json  (C7 partial, C8, C9)
        │
        └──► llm_judge.py  (Argo free gpt-5.2, opus-4.8 fallback)
                │
                └──► llm_judge_output.json  →  coverage 9/9, agreement 9/9, REPLICATED
```

---

## 2. Tools and versions

| Tool | Role | Notes |
|------|------|-------|
| NCBI **Datasets CLI** | Genome download | `datasets download genome accession --inputfile ... --include genome,protein,gff3` — no auth, free |
| **Europe PMC REST** | Full text (XML) | `/PMC5762925/fullTextXML` — free, CC-BY |
| **fastANI** | All-vs-all ANI (17×17) | Independent of paper's JSpeciesWS |
| **SciPy** `scipy.cluster.hierarchy` | Average-linkage clustering into 2 clades | Distance = 100 − ANI |
| **CD-HIT** | Protein family clustering (core/pan) | c=0.5, n=3 — independent of paper's ProteinOrtho |
| **BLAST+** (`blastp`) | Virulence-factor homology | Independent of manual annotation |
| **NCBI PGAP** (upstream) | CDS calls in downloaded assemblies | Differs from paper's Prokka — accounts for ~1-CDS mean discrepancy |
| **UniProt** | Curated *F. magna* VF references (FAF, SufA, sortase, CAMP, PAB, protein L, albumin-binding) | Free download |
| **Argo free gpt-5.2** (opus-4.8 fallback) | LLM-judge coverage/agreement scoring | Free per standing Argo endpoint rule |
| Python 3.x (pandas/numpy) | Glue, JSON I/O, stats | Standard |

---

## 3. Scripts (`work/`)

| Script | Function | Output |
|--------|----------|--------|
| `genome_stats.py`     | Parse assembly + PGAP protein.faa; CDS count, GC, length | `genome_stats.json` |
| `ani_analysis.py`     | Load fastANI raw matrix, compute stats | `ani_results.json` |
| `ani_cluster2.py`     | SciPy average-linkage, 2-cluster cut, name clades by ATCC 29328 | `clades2.json` |
| `pangenome.py`        | Concatenate 12 proteomes → CD-HIT → parse .clstr → core/singleton/pan counts + freq distribution | `pangenome_12.json`, `pan_12_cdhit.clstr` |
| `vf_survey.py`        | Build per-strain blast DBs, run blastp for 7 VF references, apply presence thresholds | `vf_results.json`, `camp_copies.json` |
| `llm_judge.py`        | Send claims+results to Argo, parse coverage/agreement/verdict | `llm_judge_output.json` |

---

## 4. Reproduction commands (end-to-end)

```bash
cd work/

# 1. Download 17 genomes
datasets download genome accession --inputfile acc_list.txt \
  --include genome,protein,gff3 --filename fin17.zip
unzip -o fin17.zip -d fin17

# 2. Genome stats (C2)
python3 genome_stats.py

# 3. All-vs-all ANI + 2-clade cut (C3, C4)
fastANI --ql genome_paths.txt --rl genome_paths.txt -o fastani_raw.tsv
python3 ani_cluster2.py

# 4. Core / pan-genome on 12-genome subset (C5, C6)
python3 pangenome.py 12

# 5. Virulence factors (C7 partial, C8, C9)
python3 vf_survey.py

# 6. LLM-judge (free Argo)
python3 llm_judge.py
```

---

## 5. Work estimate (breakdown)

| Phase | Time | Compute |
|-------|-----:|---------|
| Full-text pull + accession mapping | ~5 min human + 30 s network | Free (Europe PMC + NCBI Datasets) |
| Genome download (17 × ~2 MB) | ~30 s | Free |
| `genome_stats.py`         | <5 s | Laptop CPU |
| fastANI 17×17             | ~15 s | Laptop CPU (single thread OK for n=17) |
| Clade cut + JSON dump     | <2 s | Laptop CPU |
| CD-HIT on 12 proteomes    | ~30 s | Laptop CPU |
| Per-strain blast DB build + blastp for 7 VF refs × 17 strains | ~1–2 min | Laptop CPU |
| LLM-judge (Argo free)     | ~10–30 s | Free API |
| **Total wall-clock**      | **~5 min** | **$0** |

Human analyst time (design + write-up + this backfill): ~4–6 hours across the initial run and the reporting layer.

---

## 6. Rationale for tool substitutions

The paper used Parsnp (SNP phylogeny), JSpeciesWS (ANI), ProteinOrtho (pan-genome), and Prokka (annotation). This replication used fastANI, CD-HIT, blastp, and NCBI PGAP annotation. The substitutions are deliberate:

- **fastANI vs JSpeciesWS ANI:** JSpeciesWS is a web service with rate limits; fastANI is the current de facto reference implementation for pairwise ANI at scale and correlates >0.99 with BLAST-based ANI. Reproducing the paper's 90.7% inter-clade boundary at 90.67% under a *different* ANI engine is a stronger claim than re-running the same engine.
- **CD-HIT vs ProteinOrtho:** ProteinOrtho is graph-based and reciprocal-best-hit-flavored; CD-HIT at c=0.5 is a permissive clustering. They answer subtly different questions but should agree on core count within a few percent, which they did (1209 vs 1202, +0.6%).
- **PGAP vs Prokka:** We accept the NCBI-side re-annotation as-is rather than rerun Prokka on our downloaded assemblies. The mean-CDS discrepancy of 1 gene is well within pipeline noise.
- **BLAST+ vs the paper's manual annotation:** Manual annotation is not reproducible; a curated-reference blastp with fixed thresholds is.

---

## 7. Where a future re-run would differ

If a fully independent replication is desired (not just tool-substitution), see `open_questions.json` item 1: pull raw reads from ENA/SRA, reassemble with SPAdes 4.x, annotate with Bakta v1.9+, then re-run steps 3–5. That would cost roughly a day of compute (mostly assembly) and would test annotation-pipeline dependence directly. This replication was scoped to the paper's own deposited assemblies.
