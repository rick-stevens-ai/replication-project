# Artifact Harvest

| Artifact | Source | Access | Notes |
|---|---|---|---|
| Paper abstract + intro/theorem text | https://arxiv.org/abs/1806.02048 ; https://ar5iv.org/abs/1806.02048 | Open Access (arXiv) | Full HTML pulled via `curl` (ar5iv, 3.47 MB). Used to extract Eq.1, Eq.2, Theorem 1, gateset examples. NOT the paid `pdf` tool. |
| Published version | npj Quantum Information **5**, 71 (2019), DOI 10.1038/s41534-019-0182-7 | OA | Cross-reference for claim wording. |
| Author reference code | The paper references analysis in Python; no single canonical repo pinned. Replication built independently from the equations. | — | Independent re-implementation (no code copied). |

## Locally produced artifacts
- `work/rb_replicate.py` — full pure-numpy replication (Clifford & Pauli groups from generators, PTM formalism, exact twirl + Monte-Carlo RB, single/double-exp fits, irrep counting).
- `work/make_figure.py` — figure generator.
- `report/evidence/results.json` — all numerical outputs.
- `report/evidence/rb_replication_figure.png` — C1 single-exp vs C2 multi-exp figure.

## Tool versions
- Python 3, numpy 2.4.3, scipy 1.18.0 (fits), matplotlib (figure, via venv).
- No GPU / no external RB library (qiskit-experiments not used — core built from scratch for full independence).
- Free endpoints only. LLM judge: Argo gpt-5.2 (localhost:44497).
