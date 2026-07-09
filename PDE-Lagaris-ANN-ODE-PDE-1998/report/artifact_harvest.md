# Artifact Harvest

## Paper (public preprint)

| Item | URL | Local | Bytes |
|---|---|---|---|
| Lagaris, Likas, Fotiadis 1998 preprint (physics/9705023 v1, 19 May 1997) | https://arxiv.org/pdf/physics/9705023 | `work/lagaris_1998.pdf` | 330 206 |
| Plaintext extraction (`pdftotext -layout`) | (derived) | `/tmp/lagaris_1998.txt` | ~90 KB, 1377 lines |

Journal version: IEEE Trans. Neural Networks 9(5):987–1000 (Sept 1998). arXiv
preprint is functionally identical (same authors, same problem set, same trial
solutions); we cite the arXiv preprint since it is the public, downloadable
copy.

## Data

No external datasets were required — the paper's test problems are analytic
(source terms + BCs + closed-form exact solutions given in the paper). We
generated the training and test collocation grids ourselves.

## Software

- Python 3.12, PyTorch 2.2.2 (CPU wheels), NumPy 1.26.4, Matplotlib
  (venv at `work/venv`). All pip-installable, all free.
- Optimizer: `torch.optim.LBFGS` (Wolfe line search, history 50, tolerance
  1e-14). The paper used Merlin's BFGS; both are quasi-Newton second-order
  methods.
- LLM judge: Argo proxy at `127.0.0.1:44497`, model `argo:gpt-5`, temperature
  omitted (reasoning family). Key `stevens`. Free endpoint per project rules.

## Compute

All runs performed locally on CherryRd (Darwin 25.3.0, x86_64). Total wall
clock: ~30 s across the three problems + LLM scoring.
