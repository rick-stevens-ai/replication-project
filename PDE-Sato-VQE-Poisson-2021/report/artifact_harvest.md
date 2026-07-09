# Artifact Harvest

| Artifact | Source | Local path | Size / count | Notes |
|---|---|---|---|---|
| Paper PDF (correct) | `https://arxiv.org/pdf/2106.09333` | `paper.pdf` | 785 930 B, 9 pages | arXiv preprint of PRA 104, 052409. |
| Paper PDF (initial wrong fetch) | `https://arxiv.org/pdf/2106.09400` | (deleted) | 255 785 B | Was Mörtsell et al. Hubble tension — wrong arXiv ID from task; caught by first-page grep. |
| pdftotext extraction | `pdftotext -layout paper.pdf` | `work/paper.txt` | 1 224 lines | Native PDF → clean text. |
| marker.md mirror | pdftotext fallback | `extraction/marker.md` | ~115 kB | marker binary not installed on this host. |
| nougat.mmd mirror | pdftotext fallback | `extraction/nougat.mmd` | ~115 kB | nougat-ocr not installed on this host. |
| Authors' reference code | ToyotaCRDL/VQAPoisson (Apache-2.0) | (referenced only, not run) | | Pins Qiskit 0.23 + retired qiskit-aqua; not runnable on modern Python. Available in sibling dir `PDE-Sato-VQA-poisson-2021/work/VQAPoisson/`. |
| Sibling replication (VQA-slug) | previous OpenClaw run | `~/Dropbox/REPLICATE-PROJECT/PDE-Sato-VQA-poisson-2021/` | | Independent prior attempt with the same verdict (REPLICATED). NOT overwritten per project rule; my target dir is the distinct VQE-slug. |
| Independent implementation | this replication | `work/vqe_poisson.py` | 7.4 kB, 156 lines | Pure-numpy circuit simulator, gate-by-gate. |
| Unit tests | this replication | `work/test_gates.py` | 3.6 kB | Endianness + CNOT + Poisson sanity. |
| Multistart deep-dive | this replication | `work/vqe_n5_deep.py` | 1.5 kB | Best-of-3 restarts at n=5. |
| Structural O(1) check | this replication | `work/verify_o1_cost.py` | 2.2 kB | Pauli-decomposition counting. |
| LLM judge harness | this replication | `work/judge.py` | 5.7 kB | Argo aggregator :4000, gpt-5.2 fallback. |
| Main results | | `report/evidence/results_summary.json` | ~2 kB | Per-n mean/max ε_tr, norms, iters. |
| n=5 best-of-3 results | | `report/evidence/n5_dirichlet_3restart.json` | ~1 kB | |
| n=5 full solutions | | `report/evidence/n5_full_solutions.json` | ~50 kB | Full ψ, u vectors per trial for Dirichlet+periodic. |
| O(1) analysis log | | `report/evidence/o1_cost_analysis.txt` | ~500 B | |
| Main sweep log | | `report/evidence/run.log` | ~1 kB | |
| Judge raw response | | `report/evidence/judge_raw.json` | ~5 kB | Full Argo aggregator response body. |
| Judge parsed verdict | | `report/evidence/judge_response.json` | ~800 B | REPLICATED, confidence 0.83. |

## Public artifact URLs

- Paper PDF: <https://arxiv.org/pdf/2106.09333v1>
- Paper abstract: <https://arxiv.org/abs/2106.09333>
- Published version: <https://doi.org/10.1103/PhysRevA.104.052409>
- Authors' code (reference only): <https://github.com/ToyotaCRDL/VQAPoisson>

## Data provenance

- No external datasets: this paper is a numerical-experiments-only quantum-algorithm paper.
- The Poisson matrix and step-function RHS are constructed from scratch per paper Eqs. (17) and (45).
- No LLM inference was used for the replication computations themselves; the LLM was
  used only for the final verdict judgment (Argo `gpt-5.2`, free endpoint).
