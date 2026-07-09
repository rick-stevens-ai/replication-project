# Artifacts pulled

| Artifact | URL | Size | Purpose |
|---|---|---|---|
| DeepXDE paper PDF | https://arxiv.org/pdf/1907.04502 | 1.12 MB | Ground-truth for claims + hyperparams |
| Burgers reference solution `burgers_shock.mat` | https://raw.githubusercontent.com/maziarraissi/PINNs/master/appendix/Data/burgers_shock.mat | ~200 KB (256×100 grid) | High-quality ν=0.01/π reference used by the paper (via ref [47] Raissi 2019) |

No paywalled data, no proprietary code. All computation done on ANL UICGPU (A100),
CUDA_VISIBLE_DEVICES=2, PyTorch 2.4.1+cu121. No external LLM calls for
computation; only the local Argo proxy at 127.0.0.1:44497 (FREE) used for LLM
judgment.
