# Artifact harvest — OSTI 3021513

| Artifact | Source | URL | Size | MD5 | Notes |
|---|---|---|---|---|---|
| Paper PDF | OSTI | https://www.osti.gov/servlets/purl/3021513 | 11,588,723 B (11.05 MB) | c5e2dcc35a48894d8f8fbf4cae6bb914 | Downloaded from `uicgpu` (has DNS/proxy), scp'd back to workspace. arXiv preprint 2509.07326v1 (Sep 10 2025). |
| CASM (Van der Ven group cluster-expansion / kMC toolkit — explicitly named in the paper's citation list, ref [55]) | GitHub `prisms-center/CASMcode` | https://github.com/prisms-center/CASMcode | (verified live 200 OK 2026-07-02) | — | Open source, LGPL. Would drive VASP-based enumeration, cluster generation, and fitting in a full rerun. Not exercised in this wave (VASP is licensed, ~10^4 CPU-hr of DFT). |
| VASP | www.vasp.at | https://www.vasp.at | — | — | Licensed proprietary DFT code used for all 630 Li-Mg + up to 901 Li-Al configurations. Cannot be independently rerun without a paid license and HPC allocation. |
| scikit-learn | pip | 1.8.0 installed locally (paper cites `sklearn`, ref [57]) | — | — | Provides `BayesianRidge` (= paper's "Bayesian Ridge" evidence approximation with common alpha) and `ARDRegression` (= paper's Relevance Vector Machine, RVM). Used in our methodological replication. |
| Independent methodological replication result | this workspace | `work/replicate_bayesian_ce.py` + `report/evidence/replication_results.json` | 9,233 B + ~4 KB | — | Runs BR/RVM/RidgeCV on a synthetic BCC cluster-expansion dataset. |

**Data/code availability statement in the paper:** None found. The paper points at CASM (the Van der Ven group's own open-source tool) but does not deposit the specific Li-Mg / Li-Al DFT dataset or the fitting scripts in a public repository (Zenodo/GitHub/OSTI supplement).
