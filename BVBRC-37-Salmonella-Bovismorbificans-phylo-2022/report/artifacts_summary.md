# Artifacts Summary — BVBRC-37 / Gopinath 2022 Bovismorbificans

**Report dir:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-37-Salmonella-Bovismorbificans-phylo-2022/`
**Verdict:** REPLICATED · coverage ≈ 0.92 (free Argo `gpt-5.2` judge).

---

## Report files (this directory)

| File | Type | Purpose |
|---|---|---|
| `REPORT.md` | Markdown | Human-readable canonical replication report (paper summary → claims → method → results → verdict). |
| `REPORT.tex` | LaTeX | Section-by-section formal write-up including dedicated **Genuine Critique** section. Compile with `pdflatex`. |
| `open_questions.json` | JSON | 5 truly open follow-up questions, each with `q`, `basis`, `next_steps`, grounded in the paper's biology. |
| `workflow.md` | Markdown | Ordered pipeline description (steps, tools, versions, effort estimate). |
| `artifacts_summary.md` | Markdown | (This file) inventory of everything produced. |
| `failure_analysis.md` | Markdown | Honest failure analysis: what didn't run, what was skipped, single-judge caveat, PDF-availability status, etc. |

## Data artifacts (referenced in report)

| Artifact | Location (relative to repo root) | Provenance / how to regenerate |
|---|---|---|
| Accession list (82 assemblies) | `work/acc.txt` | NCBI Datasets REST query on BioProject `PRJNA378379`, filtered to organism = "…serovar Bovismorbificans". |
| Genome FASTAs (82) | `work/genomes/*.fna` | `datasets download genome accession --inputfile acc.txt --include genome` → single 117 MB zip, flattened. |
| SeqSero2 results | `work/seqsero2/*/SeqSero_result.tsv` | `SeqSero2_package.py -m k -t 4` on each FASTA (uicgpu). |
| MLST results | `work/mlst/mlst.tsv` | `mlst --scheme senterica_achtman_2` per genome, concatenated. |
| Mash sketch + all-vs-all distance | `work/mash/all.msh`, `work/mash/dist.tsv` | `mash sketch -o all -s 10000` then `mash dist all.msh all.msh`. |
| Hierarchical-cluster labels (2-cluster cut) | `work/cluster/labels.tsv` | SciPy `linkage(method="average") → fcluster(maxclust=2)`. |
| BioSample metadata (source/host/geo) | `work/metadata/biosample.tsv` | Per-accession pull, `isolation_source`/`host`/`geo_loc_name`. |
| AMRFinderPlus per-genome outputs | `work/amrfinder/*.tsv` | `amrfinder -n <fna> --organism Salmonella --plus --database <dir>/latest`. |
| AMRFinderPlus DB pin | `work/amrfinder/DB.txt` | `2024-07-22.1` (recorded but not SHA-hashed). |
| Aggregated feature table | `work/amrfinder/all_hits.tsv` | pandas concat + group-by Element type/class/gene. |

## Figures / evidence

| Figure | File | Content |
|---|---|---|
| Dendrogram (mash + average-linkage, ST-colored leaves) | `evidence/dendrogram.png` | Two-cluster cut showing ST150 (n=2) isolated from ST142/377/1499/2640/8700 backbone (n=80). |
| Per-ST composition table | `evidence/st_table.tsv` | ST → count → clinical/food split. |
| LLM-judge verdict (free `gpt-5.2`) | `evidence/llm_judge_verdict.txt` | Full judge response text; per-claim assessments; coverage ≈ 0.92. |

## Traces / provenance

| Trace | Path |
|---|---|
| Dataset REST query response (paginated) | `work/traces/datasets_report_pgN.json` |
| `datasets download` invocation log | `work/traces/datasets_download.log` |
| Per-tool stdout/stderr (uicgpu fanout) | `work/traces/tool_logs/<tool>/<accession>.log` |
| LLM-judge request/response bundle (evidence bundle in, verdict out) | `work/traces/llm_judge_bundle.json`, `work/traces/llm_judge_response.json` |
| Opus 4.8 502-failure trace (why we fell back to `gpt-5.2`) | `work/traces/argo_opus_4_8_502.log` |

## Cross-references

- Paper (open access, CC BY): DOI [10.3390/microorganisms10061199](https://doi.org/10.3390/microorganisms10061199), PMC PMC9228720, PMID 35744717.
- NCBI BioProject (paper's own): [PRJNA378379](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA378379).
- NCBI Datasets CLI docs: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/command-line/datasets/
- SeqSero2 docs: https://github.com/denglab/SeqSero2
- mlst / pubMLST Achtman scheme (senterica_achtman_2): https://pubmlst.org/senterica/
- AMRFinderPlus: https://github.com/ncbi/amr

## What is NOT in the artifact set (see `failure_analysis.md` for why)

- The paper's bespoke **2690-locus custom cgMLST schema** — not rebuilt.
- The paper's **k-mer-binning survey of >260 strains** — not rerun.
- The paper's **digital DNA microarray / tiling-array SARA/SARB mining** — not rerun.
- A **bootstrapped ML/Bayesian core-genome phylogeny** with branch supports — not built (mash proxy used instead).
- **Plasmid replicon typing** (e.g. mob-suite) and **prophage prediction** (e.g. PHASTER) — not attempted.
- **Multi-judge / ensemble verdict** — only single free `gpt-5.2` judge, no self-consistency vote or human adjudication.
- **SHA-256 manifest** of input FASTAs — recorded tool versions but not per-artifact checksums.

## One-line summary
Pulled all 82 Bovismorbificans genomes from the paper's own BioProject (PRJNA378379), reproduced serovar (SeqSero2 82/82, `8:r:1,5`), MLST distribution (backbone `{142,377,1499,2640}` + separate `ST150`), the two-polyphyletic-cluster topology (mash + hierarchical), the mixed clinical/food multi-country sampling (CH/CA/US), and AMR/virulence feature classes (AMRFinderPlus, `spv` in 56/82) — free tools, uicgpu compute, LLM-judge REPLICATED coverage ~0.92.
