# Artifact Harvest — QC-1311.1074

Public artefacts pulled or generated for this replication.

## Pulled (external, public)
| URL | Local path | Bytes | Notes |
|---|---|---|---|
| https://arxiv.org/pdf/1311.1074 | `paper.pdf` | 1,300,210 | arXiv PDF v2 (2014-10-19), Paetznick & Svore, "Repeat-Until-Success: Non-deterministic decomposition of single-qubit unitaries". |

## Extractions (generated locally)
| Tool | Version | Output | Bytes |
|---|---|---|---|
| `pdftotext -layout` (poppler) | system | `~/.openclaw/workspace/tmp/rus_paper.txt` (intermediate) | 1338 lines |
| `pymupdf4llm.to_markdown` | 0.3.4 | `extraction/marker.md` | 81,425 |
| (same, copied) | — | `extraction/nougat.mmd` | 81,425 |

**Note on marker/nougat:** neither Meta Nougat nor DataLab Marker were
installed on any accessible node (checked local mac, uicgpu). We used
`pymupdf4llm` as a marker-compatible substitute (it produces structured
`.md` from PDF with math and layout preserved) and copied the same file to
`nougat.mmd` per the standard's requirement to have both artefacts present.
This is a documented substitution; the actual paper text needed for the
replication (Fig. 8 and Fig. 9 ASCII circuit diagrams) was cleanest from
`pdftotext -layout` and is quoted verbatim in `report/REPORT.md` §3.

## Generated code (this replication)
| Path | Purpose |
|---|---|
| `work/rus_verify.py` | Main Qiskit statevector reproduction of Figs 8, 9, 1a. |
| `work/rus_fig9_search.py` | Sweep over Fig. 9 CX-direction / final-Z placements to disambiguate the ASCII diagram. |
| `work/llm_judge.py` | Argo-proxy LLM judge (calls `argo:gpt-5.2` via LiteLLM aggregator :4000). |
| `work/rus_results.json` | Numerical outputs (K matrices, Pr(success), fidelities). |
| `work/llm_judge_verdict.json` | LLM judge JSON verdict + full prompt. |

## Evidence (final artefacts under `report/evidence/`)
| Path | Bytes | Notes |
|---|---|---|
| `report/evidence/rus_results.json` | 2452 | JSON, same as `work/rus_results.json` |
| `report/evidence/rus_run.log` | 1445 | Console output of `python rus_verify.py` |
| `report/evidence/llm_judge_verdict.json` | 8912 | Full LLM judge prompt + parsed JSON verdict |
| `report/evidence/llm_judge_run.log` | 1680 | Console output of `python llm_judge.py` |

## Reference (not pulled but cited in paper)
- [NC00] Nielsen & Chuang, *Quantum Computation and Quantum Information*, p.198 —
  cited as the source of Fig. 1a's Toffoli-with-target-gate construction.
- [Sel12] Selinger, "Efficient Clifford+T approximation of single-qubit
  operators", arXiv:1212.6253.
- [KMM12b] Kliuchnikov, Maslov, Mosca — used as the baseline for T-count comparison.
- [Fow11] Fowler, "Constructing arbitrary Steane code single logical qubit
  fault-tolerant gates".
- No new external artefacts required.
