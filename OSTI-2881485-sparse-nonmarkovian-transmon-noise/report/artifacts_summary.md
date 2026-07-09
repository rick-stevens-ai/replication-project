# Artifacts Summary — OSTI 2881485

Inventory of every file produced or pulled during this replication, with sizes, provenance, and role.

## Inbound (pulled from the outside world)
| Path | Size | Source | Provenance |
|------|------|--------|------------|
| `paper.pdf` | 4 027 724 B | https://www.osti.gov/servlets/purl/2881485 | Primary paper PDF |
| `work/paper.pdf` | 4 027 724 B | same, copy | Local copy for reference |
| `work/code.zip` (on uicgpu, not mirrored here) | 8 423 674 B | https://zenodo.org/api/records/19695739/files/y-oda2/ibmq-noise-modeling-v0.0.2.zip/content | md5 f7b46bf4e11fe6ccdee67fa07c80a97b, CC-BY-4.0 |
| `work/y-oda2-ibmq-noise-modeling-f481da0/` (uicgpu) | ~9 MB | unpacked ZIP | 17 notebooks + `imports_IBM_NM.py` + all pickled data |

## Extractions (produced by us from paper.pdf)
| Path | Size | Tool | Notes |
|------|------|------|-------|
| `extraction/marker.md` | 1 352 lines | Marker | Full paper markdown |
| `extraction/nougat.mmd` | (see file) | Nougat | Math-aware markdown |
| `work/paper.txt` (staged in `tmp/osti/`) | 2 671 lines | pdftotext -layout | Working text used for LLM-guided comprehension |
| `work/nb9.txt` | 479 lines | custom nbformat dumper | Human-readable dump of `fig_09_vqe_H2.ipynb` cells |

## Replication scripts (produced by us)
| Path | Size | Purpose |
|------|------|---------|
| `work/verify_claim.py` | 5 392 B | Compute Δ(R) per paper Eq. (26) from released pickles; emit `verify_summary.json` |
| `work/rerun_ibm_sim_v2.py` | 5 506 B | Independent AerSimulator rerun with FakeHanoiV2; emit `rerun_ibm.json` |
| `work/llm_judge.py` | 4 550 B | Post replication numbers to Argo aggregator; parse structured verdict |
| `work/dump_nb.py` | 268 B | Helper to dump ipynb cells for reading |

## Evidence files (numerical output of the replication)
| Path | Size | Content |
|------|------|---------|
| `report/evidence/verify_summary.json` | ~7 KB | 54-point per-R table + summary: E_ideal, E_exp, E_IBM, E_NM, Δ_IBM, Δ_NM, θ_opt, match booleans, fold_improvement |
| `report/evidence/rerun_ibm.json` | ~4 KB | Fresh AerSimulator rerun output: per-R E_sim + Δ, Qiskit version, backend name, seed, shots |
| `report/evidence/llm_judge.txt` | ~1 KB | Structured JSON verdict from `argo:gpt-5.4` (verdict=PARTIAL, coverage=80, agreement=86) |

## Reports (produced by us)
| Path | Content |
|------|---------|
| `report/REPORT.md` | Full markdown replication report (paper summary, claims table, method, results, verdict, open questions) |
| `report/REPORT.tex` | LaTeX version of the report (section-by-section detailed, per REPLICATION_DIR_STANDARD_2026-07-05.md item 4) |
| `report/brief.md` | 1-paragraph what/why |
| `report/attempt_log.md` | Chronological log of what we did |
| `report/artifact_harvest.md` | Every public artifact pulled |
| `report/workflow.md` | Workflow + tools/codes + effort estimate |
| `report/artifacts_summary.md` | THIS file |
| `report/failure_analysis.md` | Honest failure analysis |
| `report/open_questions.json` | 5 heavy-duty open questions with `next_steps` |

## Traces / logs
- Marker log (uicgpu terminal): 166 s total, all 33 pages processed.
- Nougat log (uicgpu terminal): first attempt OOM on GPU 1 (35 GB pre-occupied by another process), retried on GPU 6 with `--batchsize 1` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, then succeeded.
- Qiskit rerun log (uicgpu terminal): 12 progress prints (every 5 R points), 57.9 s total.
- LLM-judge trace: first Opus 4.8 call → HTTP 502; retried once, still 502; fell back to GPT-5.4 (verified via pong probe) which returned clean JSON in ~5 s.

## Checksums (spot-check)
- `paper.pdf`: 4 027 724 B (matches OSTI Content-Length).
- Zenodo ZIP: md5 f7b46bf4e11fe6ccdee67fa07c80a97b (matches record metadata).

## Not included in this dir (documented for provenance only)
- Full unpacked Zenodo repo on uicgpu at `~/osti2881485/y-oda2-ibmq-noise-modeling-f481da0/` (kept there to keep the Dropbox mirror lean; can be re-pulled from Zenodo any time).
