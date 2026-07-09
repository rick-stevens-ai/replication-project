# Artifact Harvest — PDE-Sato-VQA-poisson-2021

| Artifact | Source | Local path | Size | Notes |
|---|---|---|---|---|
| Paper PDF (arXiv v2, dated 25 Apr 2022) | https://arxiv.org/pdf/2106.09333 | `work/sato_2021.pdf` | 785 930 B | 27 pp, includes Appendices A-D. Same content as PRA 104 052409. |
| Paper text (pdftotext -layout) | derived | `/tmp/sato_2021.txt` (transient) | 1224 lines | Used for equation & hyperparameter extraction. |
| Authors' reference code | https://github.com/ToyotaCRDL/VQAPoisson (Apache-2.0) | `work/VQAPoisson/` | 3 files, 15 308 lines total | Requires Qiskit 0.23 + qiskit-aqua (retired). Consulted for interface only; independent numpy reimplementation used for the actual replication. |
| Our replication | new (this work) | `work/vqa_poisson_replicate.py` | ~9.9 kB | Pure numpy + scipy; no Qiskit dependency. |
| Full trial results, Dirichlet BC | this run | `report/evidence/results_dirichlet.json` | 17.3 kB | 40 trials (n=2..5, 10 each). |
| Run log, Dirichlet BC | this run | `report/evidence/run_dirichlet.log` | 3.4 kB | stdout of the driver script. |
| Full trial results, Periodic BC | this run | `report/evidence/results_periodic.json` | ~2.5 kB | 5 trials at n=5 (spot check). |
| LLM-judge verdict | Argo Opus 4.7 | `report/evidence/judge_response.json` | see file | Final verdict decision. |

Provenance URLs (all public, all free):
- arXiv:2106.09333 — free preprint of PRA 104 052409.
- github.com/ToyotaCRDL/VQAPoisson — Apache-2.0 reference implementation by paper authors.
- All compute local (CherryRd), no LLM inference required for the replication itself; LLM used only for the final verdict judgment (Argo Opus, free).
