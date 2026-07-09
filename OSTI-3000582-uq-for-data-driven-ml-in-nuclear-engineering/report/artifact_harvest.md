# Artifact Harvest

## Public artifacts pulled

| Artifact | URL | Size | Notes |
|---|---|---|---|
| Wu et al. 2025 full text PDF | https://www.osti.gov/servlets/purl/3000582 | 3,925,127 bytes (3.9 MB, PDF 1.5, 41 pp) | OSTI 3000582, DOI 10.1080/00295639.2025.2552500. Downloaded via `curl` on uicgpu (needs `HTTPS_PROXY=http://<lan-host>:3128` from `~/env.sh`). |
| pdftotext extraction | (derived) | 2368 lines | `pdftotext -layout paper.pdf paper.txt`, used for structured parsing since paid `pdf` analyzer was unavailable. |

## Public code / data referenced by the paper — status

| Referenced by paper | Available? | Notes |
|---|---|---|
| SAFARI-1 axial neutron flux measurement data | NO | Only mentioned in paper via prior-work refs [3,4] (Moloko et al.). No public dataset URL, no supplementary. Section IV.B not reproducible independently. |
| OECD/NEA AI/ML CHF benchmark [25,26] | Partial | Public benchmark exists (2023), 47 institutional submissions, but only referenced — the paper doesn't run it. Out of scope for this replication. |
| MC Dropout method [36], Gal & Ghahramani 2016 | YES | Well-known, we implemented in PyTorch. |
| Deep Ensemble [38], Lakshminarayanan et al. 2017 | YES | Well-known Gaussian-NLL formulation, we implemented in PyTorch. |
| BNN via variational inference [39-41] | YES | Implemented in Pyro (PyroModule + AutoDiagonalNormal + SVI). |
| GP with Matern 5/2 [42-46] | YES | Used analytically for data generation; sklearn RBF+White for GP model per paper's "different kernel than the one used to generate the data". |
| Split CP / SRCP [47,48] | YES | Standard rank-statistics implementation, coded from paper's Eqs. 1-7. |
| NNI hyperparameter search [54] | Skipped | Paper uses NNI for SAFARI-1 tuning; Section IV.A hyperparameters are fully specified so no search needed for the replication. |

## Software environment (uicgpu, on-node fresh env)

Conda env `osti3000582` @ `/home/stevens/miniforge3/envs/osti3000582/` created via mamba:

```
python 3.11.13
numpy 1.26.4
scipy 1.17.1
scikit-learn 1.9.0
torch 2.12.1 + CUDA 12.9 (cuda_count=8)
xgboost 3.2.0
pyro-ppl 1.9.1+ab0491a
matplotlib (pulled in transitively)
```

Compute: 1 A100 (of 8 available) used; total run wall time ≈ 56 s.

## Local artifacts produced

| Path | Bytes | Description |
|---|---|---|
| `work/paper.pdf` | 3,925,127 | Original paper PDF |
| `work/replicate_uq.py` | ~19 kB | End-to-end replication script |
| `work/make_figs.py` | ~3 kB | Figure generation script |
| `report/evidence/results.json` | 2,225 | Per-method coverage, width, adaptivity metrics |
| `report/evidence/bands.json` | 73,563 | Per-method predicted-mean and 95% CI bands on 100-point x grid + true μ(x), σ(x) |
| `report/evidence/replication_figure.png` | 487,793 | 6-panel replication of paper Fig 9(a,c) + Fig 10(a-d) |
| `report/evidence/dataset_true_only.png` | 80,989 | Paper Fig 8 analog: dataset generator visualization |
| `report/evidence/run.log` | 2,910 | stdout of the replication run |
| `report/evidence/llm_judge_verdict.json` | ~3 kB | Argo GPT-5 judge verdict + per-claim breakdown |
