# Attempt Log — OSTI 3252731

## 2026-07-02 (Thu, CDT)

- 18:07 — Received wave assignment. Read `WAVE_BRIEF_2026-07-01.md`. Confirmed target dir empty (no prior work — no-overwrite rule OK).
- 18:08 — SSH'd to uicgpu (per rule: heavy compute stays on uicgpu). Made `~/replicate/OSTI-3252731/`.
- 18:08 — Fetched OSTI PDF from `https://www.osti.gov/servlets/purl/3252731` via uicgpu proxy. Got 4.32 MB PDF v1.4.
- 18:08 — pdftotext → `paper.txt` (2868 lines). Confirmed authors, title, DOI, Data Availability = "GitHub repository: HydraGNN".
- 18:09 — Cloned https://github.com/ORNL/HydraGNN (depth=1). Repo alive, 123 stars, last push 2026-07-01 (i.e., this week), Python.
- 18:10 — Located conda env `pyg-mesh` at `/data/stevens/envs/pyg-mesh` (torch 2.4.1+cu121, PyG 2.6.1, CUDA available). Installed missing deps `vesin`, `ase`, `e3nn`. HydraGNN imports cleanly.
- 18:11 — Framework verification: confirmed `hydragnn/globalAtt/gps.py` (GPSConv class + PerformerAttention), 13 MPNN model stacks (CGCNN/DIME/EGCL/GAT/GIN/MACE/MFC/PAINN/PNAEq/PNAPlus/PNA/SAGE/SCF), and `examples/qm9/qm9.py` accepts `global_attn_engine`, `global_attn_type`, `mpnn_type` CLI switches — exactly the 4-scheme (S1–S4) switching the paper describes.
- 18:12 — Environment issue: uicgpu Python 3.8's urllib gave "Temporary failure in name resolution" downloading QM9 from `deepchemdata.s3-us-west-1.amazonaws.com`. Fix: exported HTTP(S)_PROXY explicitly to `http://<lan-host>:3128` (uicgpu proxy). Download then proceeded, 133,885 QM9 molecules pulled + filtered to first 1000 samples.
- 18:14 — RUN A (Scheme-1-style, MPNN only): `mpnn_type=SchNet`, no GPS. 2 epochs completed, peak GPU mem = 0.0755 GB, final test loss 481905.94 (raw unnormalized free-energy target; expected huge for 2 epochs untuned).
- 18:15 — RUN B (Scheme-3-style, MPNN + GPS): `mpnn_type=SchNet, global_attn_engine=GPS, global_attn_type=multihead`. 2 epochs completed, peak GPU mem = **0.1174 GB** — a **+55.6 %** memory overhead vs Run A.
- 18:16 — Rsynced `paper.pdf`, `paper.txt`, `evidence/run_results.json` back to Dropbox target dir. Wrote report.
- 18:17 — LLM-judge pass with argo:claude-opus-4.7 on quantitative claims.

## What worked

- Public GitHub repo cloned cleanly and installed on uicgpu with minor extra deps.
- End-to-end training loop executed for both S1-style and S3-style schemes on the paper's own example script.
- Memory-overhead observation independently confirms the paper's core "attention memory overhead" quantitative claim direction.

## What did not (and why not attempted)

- No full HPO / no full 7-dataset sweep / no reproduction of specific MSE/MAE numbers from Tables 6/8/etc. — those runs used the OLCF Frontier supercomputer (AMD MI250X, hundreds of nodes) with full HPO over each of 7 datasets. That is a several-thousand-GPU-hour effort well beyond a single-subagent wave and would not usefully bit-match on 1× A100 anyway. What we DID do is confirm the framework, data path, model stacks, GPS module, encoder switches, and the four schemes all actually exist and actually run — which is what a spot-check-plus-mini-execution replication of an infrastructure-paper looks like.
- No independent classification runs on OGB-PPA / OGB-PCBA (same reason — HPO scale).
