# Artifact Harvest — OSTI 2574844

| Artifact | Source | Size | Checksum / note |
|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/2574844 (via uicgpu proxy) | 2,056,407 B | MD5 `7f6841cfcf686fe83c0015548b9a6098` → `work/paper_2574844.pdf` |
| Paper text | pdftotext of above | 73,684 B | `work/paper_2574844.txt` |

## Data / code availability
- The paper releases **no public code or data** (feasibility note: "method specified"). It is a method/implementation paper (Phys. Plasmas). Therefore replication was done by **reimplementing the method from the equations** (Eqs. 3–8, Table III), not by rerunning authors' artifacts.
- No proprietary/experimental data required: the verification target (Sec. V.A, Fig. 2) is an **analytic plane wave**, so the entire validation is self-contained.

## Reimplementation artifacts (this work, in `work/`)
- `gfdm_core.py` — GFD weight machinery (Eqs. 3–8, Table III).
- `test_C1_derivative_order.py` → `evidence_C1.json` — derivative-operator convergence order.
- `test_C2_planewave_solve.py` → `evidence_C2.json` — full plane-wave BVP convergence.
- `judge_prompt.txt`, `judge_result.txt` — LLM-judge (Argo gpt-5.2) scoring.

## Tool versions
- Python 3 + numpy + scipy (CherryRd local venv; light compute).
- pdftotext (poppler) on uicgpu.
- LLM judge: `argo:gpt-5.2` via Argo proxy localhost:44497 (free).
