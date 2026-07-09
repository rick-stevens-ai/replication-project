# Artifact Harvest — OSTI 3252731

| Artifact | Source URL | Size / detail | Notes |
|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3252731 | 4,320,795 B, PDF v1.4 | Full open-access text, `work/paper.pdf` |
| Paper text extract | (from PDF) | 2,868 lines | `work/paper.txt` |
| HydraGNN source repo | https://github.com/ORNL/HydraGNN | git clone depth=1 (~11 MB), 123 stars, last push 2026-07-01 | Public, BSD-3-Clause, actively maintained by ORNL |
| GPS / global-attention module | HydraGNN `hydragnn/globalAtt/gps.py` | `GPSConv` class with `PerformerAttention` support | Referenced repeatedly in paper as the core switch |
| MPNN stacks | HydraGNN `hydragnn/models/*Stack.py` | 13 model families | CGCNN, DIME, EGCL, GAT, GIN, MACE, MFC, PAINN, PNAEq, PNAPlus, PNA, SAGE, SCF |
| QM9 example driver | HydraGNN `examples/qm9/qm9.py` + `qm9.json` | Accepts `mpnn_type`, `global_attn_engine`, `global_attn_type` CLI switches | Matches paper's four-scheme (S1–S4) toggle taxonomy |
| QM9 dataset | https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/molnet_publish/qm9.zip | 133,885 molecules (used first 1000 for smoke) | Auto-downloaded by torch_geometric.datasets.QM9 |
| Run evidence | (local) | JSON | `report/evidence/run_results.json` |
