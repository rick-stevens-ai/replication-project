# Artifact Harvest

Every public artifact pulled or used for this replication.

| Artifact | Source / URL | Type | Notes |
|---|---|---|---|
| Paper abstract page | https://arxiv.org/abs/2009.04417 | HTML (45.6 KB) | Title/abstract confirmation → `work/arxiv_abs.html` |
| Paper full text (HTML) | https://ar5iv.labs.arxiv.org/html/2009.04417 | HTML (655 KB) | Rendered LaTeX; stripped to `work/paper_text.txt` (95 KB) for claim/number extraction |
| Mitiq package | PyPI `mitiq` | Python pkg | Installed v**1.0.0** (the actual software artifact under replication) |
| Cirq | PyPI `cirq-core` | Python pkg | v**1.6.1**; provides `DensityMatrixSimulator`, `depolarize` noise |

## Published-record / code artifacts (referenced, not re-downloaded)
- Mitiq GitHub: https://github.com/unitaryfund/mitiq (open-source, Apache-2.0). We installed the released PyPI build rather than building from source.
- Journal version: Quantum 6, 774 (2022), DOI 10.22331/q-2022-08-11-774.

## Generated evidence (in report/evidence/)
| File | Contents |
|---|---|
| `evidence_pec.json` | Single-run Fig-5 PEC: unmitigated 0.062222 vs paper 0.0622; PEC value + improvement factor |
| `evidence_pec_multiseed.json` | 10-seed PEC distribution at 1000 samples (mean/std/min abs err, frac-better, improvement factor) |
| `evidence_zne.json` | 20-circuit ZNE run: per-circuit + aggregate unmitigated/mitigated errors |
| `evidence_llm_judge.txt` | Free-Argo (gpt-5.2) LLM-judge verdict: REPLICATED |
| `paper_pec_claim_excerpt.txt` | Verbatim paper text of the PEC + ZNE-H2 claims (source of the 0.0622 / 0.0071 numbers) |

## Reproduction code (in work/)
- `rep_pec.py` — Fig 5 PEC toy example (exact paper setup).
- `rep_pec_multiseed.py` — PEC stochastic characterization over seeds.
- `rep_zne.py` — ZNE on RB benchmark circuits.
- `run_judge.py` — LLM-judge caller (free Argo proxy).
- `venv/` — mitiq 1.0.0 + cirq 1.6.1 (python3.12).

Checksums (sha256, key evidence):
```
6d5dab00052d47a62453753a4439091245f7c562a0cef76c6c96df11d074d520  evidence_pec.json
3b2c2e552f916cd2b5b6f5f90d25937f4f5597a1035735acd41d18d1f020ce42  evidence_pec_multiseed.json
bde168155fe843763a1807c5ebe2d0176912c596cacdb673e2a85d018c1f42b0  evidence_zne.json
```
