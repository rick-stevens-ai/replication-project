# Artifact harvest

Every public artifact used in this replication.

| Artifact                     | Source                                                              | Size    | SHA-256                                                          |
|------------------------------|---------------------------------------------------------------------|---------|------------------------------------------------------------------|
| `paper.pdf`                  | https://arxiv.org/pdf/quant-ph/0001108 (arXiv v2, Feb 2000)         | 212 114 | `81da2bc2c9c7a99f9449493854ab1a6114ad2d4d8594e0ab1fcd95b54d94311e` |
| `extraction/paper.txt`       | `pdftotext -layout paper.pdf paper.txt` (poppler-utils, local)      | 60 239  | — (derived)                                                       |
| `extraction/marker.md`       | `pdftotext -layout` output (fallback for marker.md; see EXTRACTION_NOTE.md) | 60 447 | — (derived)                                                      |
| `extraction/nougat.mmd`      | same as above (fallback)                                            | 60 320  | — (derived)                                                       |

## LLM judge

- **Provider:** Argo (Argonne National Laboratory) proxy → LiteLLM aggregator on cherryrd `http://<tailnet-aggregator>:4000/v1`.
- **Model:** `argo:gpt-5.1` (free ANL endpoint).
- **Auth:** `Bearer stevens` (standing Argo-proxy convention).
- **Payload:** `work/judge_input.json` (4 141 bytes summary of numerical results).
- **Response:** `work/judge_response.json`, verdict-only text in `work/judge_verdict.txt`.

## Numerical code (this replication)

| File                              | LOC | Purpose                                                        |
|-----------------------------------|----:|----------------------------------------------------------------|
| `work/fkw_replication.py`         | 415 | Core FKW replication (C1..C7).                                  |
| `work/fkw_extras.py`              | 130 | Extra checks: Haar comparison, hillclimb Hadamard, unitarity stress. |
| `work/fkw_hadamard_deep.py`       |  70 | Depth-15 BFS Hadamard approximation.                            |
| `work/run_judge.py`               |  90 | Free-endpoint LLM judge.                                        |

## No external data other than the paper

Because FKW is a pure-theory paper, no accession IDs (BiGG, NCBI, Zenodo, GitHub) apply. The paper's inputs to the replication are its own equations (3), (4), (13), (14), (15), and Theorem 3.1(iv).
