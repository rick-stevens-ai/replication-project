# Artifacts summary — BVBRC-121

Every artifact produced by this replication, with what/where/why.

## Top-level
| file | purpose | size |
|---|---|---|
| `paper.pdf` | The paper itself, from Europe PMC | ~2 MB |
| `README.md` (this dir) | not present — omitted; see `report/brief.md` | — |

## `extraction/`
| file | purpose | size |
|---|---|---|
| `marker.md` | prose-form extraction of paper (marker unavailable locally; produced by pdftotext + parsing) | ~4 KB |
| `nougat.mmd` | pointer to `work/paper.txt` (system pdftotext output); nougat is not installed on cherryrd/uicgpu | small |

## `report/`
| file | purpose |
|---|---|
| `brief.md` | 1-paragraph what/why/result |
| `REPORT.md` | full markdown report: claims table, method, results-vs-paper, verdict, open questions, reproduction commands |
| `REPORT.tex` | LaTeX version of the report |
| `attempt_log.md` | chronological log of everything tried |
| `artifact_harvest.md` | every public artifact pulled (URLs, sizes, notes) |
| `open_questions.json` | 5 open questions with `q` + `basis` + `next_steps` each |
| `workflow.md` | tools, effort, code+data locations, re-run cost |
| `artifacts_summary.md` | this file |
| `failure_analysis.md` | what didn't work and why |

## `report/evidence/`
| file | purpose |
|---|---|
| `ani_matrix_final.tsv` | 19×19 symmetric ANI matrix from skani, strain-labeled, produced by `analyze_ani.py` |
| `tree_heatmap.png` | 2-panel figure: UPGMA dendrogram (left), ANI heatmap with annotations (right) |
| `upgma_tree.nwk` | Newick-format UPGMA tree (average linkage on 1 - ANI/100) |
| `claim_verification.json` | per-claim numerical checks (heuristic, before LLM judge correction) |
| `llm_judge_verdict.json` | LLM-judge output: verdict=PARTIAL, coverage=60%, agreement=75%, per-claim tested/reproduced booleans, surprising findings, what-missing, justification, confidence |

## `work/`
Scripts and raw intermediates. Everything needed for exact re-run.

| file | purpose |
|---|---|
| `accession_list.txt` | initial 15-accession target list (with 7 later dropped for wrong taxon) |
| `fetch_genomes.sh` | first-pass fetcher (bug-fixed for env.sh `set -e` issue) |
| `fetch_missing.sh` | second-pass fetcher — added `.1` version handling |
| `fetch_by_taxon.sh` | third-pass fetcher — replaced wrong-taxon accessions via `datasets summary genome taxon` |
| `analyze_ani.py` | main analysis: assemble matrix, run per-claim checks, build UPGMA tree, plot heatmap |
| `llm_judge.py` | LLM-judge script (Argo :4000 aggregator, model `argo:gpt-5.2`) |
| `paper.txt` | raw pdftotext output of paper.pdf |
| `fetch.log` | log of all genome-download attempts (includes the failures + retries) |
| `*.fna` | 19 downloaded Neisseria genome FASTAs (mirror of uicgpu:`~/khoder2022/genomes/`) |
| `results/ani_matrix.tsv` | raw skani full-matrix output |
| `results/ani_triangle.tsv` | raw skani triangle-mode output |
| `results/mash_dist.tsv` | mash all-vs-all distances (k=21, s=10000) |
| `results/all_genomes.msh` | mash sketch |
| `results/genome_list.txt` | file-of-filenames used as skani/mash input |

## Reproducibility
Everything in `work/` is either public data (downloaded fresh from NCBI) or scripted (deterministic given the same input FASTAs). skani is deterministic (learned-ANI mode); mash is deterministic with the seed sketch. The Python analysis is deterministic. The LLM-judge is called with `temperature=0.0`; verdict text may vary slightly between calls but the numeric scores are stable in practice for well-grounded prompts.
