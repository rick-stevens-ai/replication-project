# Artifacts Summary — BVBRC-40 S. thermophilus ACA-DC 2

**Paper:** Alexandraki et al. (2017), *Standards in Genomic Sciences* **12**:18 — PMID 28163827
**Genome:** GCA_900094135.1 / GCF_900094135.1 · ENA LT604076
**Verdict:** PARTIAL (strong) · Coverage 10/10 · Agreement 7/10

---

## Report directory (`report/`)

| Artifact | Purpose |
|---|---|
| `REPORT.md` | Canonical Markdown replication report (11 KB). |
| `REPORT.tex` | LaTeX build with dedicated GENUINE CRITIQUE section. |
| `open_questions.json` | 5 structured open questions grounded in dairy-starter S. thermophilus biology. |
| `workflow.md` | End-to-end pipeline (endpoints, tools, provenance). |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest failure mode inventory. |
| `evidence/judge_output.txt` | LLM-judge verdict (argo:gpt-5.2). |

---

## Work directory (`work/`) — real data pulled + recomputed

### Paper text
| File | Description |
|---|---|
| `work/paper_text.txt` | OA plain text from Europe PMC `PMC5282782/fullTextXML`. Table 3 + ENA/BioProject accessions extracted. |

### Genome assemblies (NCBI Datasets REST, free)
| File | Description |
|---|---|
| `work/genomes/GCA_900094135.1/` | Author GenBank deposit: genome FASTA, protein FASTA, GFF, CDS FASTA. |
| `work/genomes/GCF_900094135.1/` | RefSeq PGAP re-annotation: genome FASTA, protein FASTA, GFF, CDS FASTA. |

### Statistics recompute
| File | Description |
|---|---|
| `work/genome_stats.py` | Pure-stdlib recompute script (length, GC bp/%, contigs, CDS, tRNA/rRNA/pseudogene, gene-biotype breakdown). |
| `work/genome_stats.json` | Machine-readable output — matches paper Table 3 to the digit for GCA. |

### De-novo re-annotation
| File | Description |
|---|---|
| `work/prokka_out/` | Prokka 1.12 run on uicgpu (bvbrc28 env): GFF, GBK, TSV, .txt summary. |
| — CDS count | 1,818 (uncurated); reconciles as ≈ 1,556 curated + 224 pseudo + ~38 small ORFs. |
| — tRNA count | 56 (EXACT match to paper). |
| — rRNA count | 15 (paper: 14; +1). |
| — Function-assigned | 653 (35.9%; paper multi-tool + manual: 63.89%). |

### CRISPR detection
| File | Description |
|---|---|
| `work/minced_default.txt` | minced at default minNR=3 → 0 arrays (corroborates single-spacer claim). |
| `work/minced_nr2.txt` | minced at minNR=2 → 6 candidates; one at ~849,603–849,704 bp matches STACADC2_0849 cas-flanked array. |

### LLM-judge scoring
| File | Description |
|---|---|
| `work/judge_input.txt` | Claims table + real recomputed results (fed to Argo). |
| `work/judge_output.txt` | argo:gpt-5.2 verdict: coverage 10/10, agreement 7/10. |

---

## Reproduced numbers (paper vs replication)

### Table 3 core stats — GCA (record fidelity)
| Attribute | Paper | Recomputed | Match |
|---|---:|---:|:--:|
| Genome size (bp) | 1,731,838 | 1,731,838 | ✅ |
| DNA G+C (bp) | 679,104 | 679,104 | ✅ |
| G+C % | 39.21 | 39.21 | ✅ |
| DNA scaffolds | 1 | 1 | ✅ |
| Protein-coding | 1,556 | 1,556 | ✅ |
| RNA genes | 70 | 70 | ✅ |
| tRNAs | 56 | 56 | ✅ |
| rRNAs | 14 | 14 | ✅ |
| Pseudogenes | 224 | 224 | ✅ |
| Total genes | 1,850 | 1,850 | ✅ |

### PGAP cross-check (GCF, independent re-annotation of same sequence)
| Attribute | Paper | PGAP | Note |
|---|---:|---:|---|
| Protein-coding | 1,556 | 1,490 | within pipeline variance |
| Pseudogenes | 224 | 226 | within variance |
| tRNA | 56 | 56 | EXACT |
| rRNA | 14 | 15 | +1 |
| extra ncRNA | — | 1 tmRNA + 1 RNase_P + 1 SRP + 4 riboswitch | PGAP calls more ncRNA |

### Prokka de-novo (RASTtk-analog)
| Feature | Paper | Prokka 1.12 |
|---|---:|---:|
| CDS | 1,556 (curated) | 1,818 (uncurated) |
| tRNA | 56 | 56 (EXACT) |
| rRNA | 14 | 15 |
| Function assigned | 1,182 (63.89%) | 653 (35.9%) |

### CRISPR (minced)
| Setting | Result |
|---|---|
| Default (minNR=3) | 0 arrays (positive evidence for single-spacer claim) |
| minNR=2 | 6 candidates; one at ~849,603–849,704 bp matches paper's STACADC2_0849 |

---

## Endpoint inventory (all free, no auth)

| Endpoint | Purpose |
|---|---|
| Europe PMC REST `fullTextXML` | OA paper + accessions |
| NCBI Datasets v2alpha REST | BioProject → assembly resolve + FASTA/GFF download |
| Python 3 stdlib | Genome-stats recompute |
| Prokka 1.12 (+ Prodigal/Aragorn/barrnap) on uicgpu | De-novo re-annotation |
| minced 2.x on uicgpu | CRISPR arrays |
| Argo proxy `argo:gpt-5.2` (localhost:44497) | LLM-judge scoring |

---

## Verdict summary line

```
WAVE_RESULT set=BVBRC-40 paper=Sthermophilus-ACADC2-genome-2017 verdict=PARTIAL
dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-40-Sthermophilus-ACADC2-genome-2017/
one_line=Deposited assembly (GCA_900094135.1/LT604076) reproduces paper Table 3 to the digit
(1,731,838 bp, 39.21% GC, 1,556 CDS, 56 tRNA, 14 rRNA, 224 pseudo, 1,850 genes);
PGAP+Prokka re-annotation within variance (tRNA exact); CRISPR presence + single-spacer/cas-adjacency
confirmed via minced; function-% and exact CRISPR count workflow-dependent
→ PARTIAL (strong), coverage 10/10 agreement 7/10.
```
