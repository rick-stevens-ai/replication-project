# Artifact harvest

## Primary source
| Item | URL | Size | SHA-256 |
|------|-----|------|--------|
| paper.pdf (quant-ph/9602016 v1) | https://arxiv.org/pdf/quant-ph/9602016 | 490,992 B | `a324785d35c27e7acda5beeac4c406122eaf3e50c787ba1f58256ed58ac4386c` |

## Derived text extractions
| Item | Producer | Path | Size |
|------|----------|------|------|
| paper.txt (layout mode) | pdftotext -layout | `work/paper.txt` | ~150 KB |
| paper_flow.txt (flow) | pdftotext | `work/paper_flow.txt` | ~140 KB |
| marker.md | pdftotext + light MD wrap (script) | `extraction/marker.md` | 138,579 B |
| nougat.mmd | pdftotext + light MMD wrap (script) | `extraction/nougat.mmd` | 138,428 B |

## Code (mirror at report/evidence/)
| Item | Purpose | SHA-256 |
|------|---------|--------|
| `work/shor_n15.py` | Main replication: build Eq. (7.5), verify lookup, run full "factor 15", run generic Shor QPE | `7294b9c7fe6ceef3626711a2dcd59a6cea38411c0c6c0c04e375fde88ad5f6d3` |
| `work/shor_n21.py` | N=21 extension using generic Shor QPE | `79bc48d17d1f26f9c2cedc9a7d44f3b6b27e1a034457734108b5bbeb0a6ade5a` |
| `work/resource_counts.py` | Gate-count vs Eq. (7.6); Cirac-Zoller pulse budget | `a586bc87ed15640e149bb8f283a363c7bfe7f3a2926110d916b0c326750cdd72` |
| `work/llm_judge.py` | Free-endpoint LLM-judge scoring | `7c81af8d4e76d3cfd25f7aa504912d55bd0961aeeecc725377380a896f89fabd` |
| `work/make_extractions.py` | Build marker.md / nougat.mmd from pdftotext | (in tree) |

## Simulator + judge outputs
- `report/evidence/evidence_shor_n15.json` — machine-readable evidence
- `report/evidence/shor_n15.log`, `shor_n21.log`, `resource_counts.log` — raw stdout captures
- `report/evidence/llm_judge_verdict.json` — LLM-judge scoring

## Free LLM endpoint(s) used
- `argo:gpt-5.4` via Argo aggregator `http://<tailnet-aggregator>:4000/v1/chat/completions`, `Authorization: Bearer stevens`. Per Rick's standing rule (free endpoints only).
- Local `localhost:44497` (Argo direct) attempted first; returned 502 for the larger judge payload — routed via aggregator successfully.

## Tools not used (documented for reproducibility)
- `marker`, `nougat`: not installed in current runtime (local or uicgpu, checked 2026-07-06). Substituted with pdftotext.
- Qualtran / OpenFermion: not needed; paper's Sec. VII target circuits are tiny and Qiskit primitives sufficed.
- uicgpu / GPU: not needed; 12-qubit statevector runs in <100 ms on the local CPU.
