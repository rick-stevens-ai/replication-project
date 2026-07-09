# Attempt log — OSTI 2587616 (Reimer et al. 2025)

## 2026-07-02 (session A — prior)
- Pulled paper PDF from OSTI (id 2587616) into `work/paper.pdf`; extracted plain text.
- Identified data source: `github.com/CLEANit/EvoSys-Research-Data-Code`. Cloned to `uicgpu:~/replicate-osti-2587616/EvoSys-Research-Data-Code/` (19 MB, MIT, commit 767874e from 2025-08-24).
- Wrote `schema_probe.py` and `probe_trajs.py` / `probe_trajs2.py` to enumerate the pickle contents. Discovered 26 pickles containing transition events + per-state histograms, but **no per-event timestamps and no per-frame vacancy positions**. This means Tables IV/V (jump rate, ASD, diffusion coefficient) cannot be reproduced from released data alone.
- Wrote `replicate_tables.py` as a first-pass replication. It used `q_next_atoms` in bulk which mis-weights per-trajectory statistics; produced Table II percentages that were off by factors of 2-10 (`derived_%` in `replication_analysis.json`). This was a bug in the derivation, not the data.
- Wrote `final_replicate.py` correcting the derivation: iterate per-trajectory, bincount, normalize, then take mean±std over trajectories. Table I: **exact match** on all 8 numbers. Table II: **exact match** on all 20 numbers (max abs diff 0.005 pp).
- Wrote `make_fig.py` producing `fig_table_II_compare.png`.
- Session ended without writing `report/REPORT.md`; evidence JSONs were saved.

## 2026-07-03 (session B — finalization)
- Read the wave brief + BVBRC-17 exemplar report structure.
- Confirmed prior evidence files are all present and internally consistent.
- Re-ran `final_replicate.py` on uicgpu as an audit — reproduces bit-for-bit.
- Wrote `extra_analysis.py`:
  - Diagonal-dominance check of Fig-5-style crosstab across all 4 datasets (not just MD-train as in prior pass).
  - χ² homogeneity test of MD-train vs MD-base transition-atom histograms.
  - KL divergence and total variation of {MD-base, EvoSys-1NNI, EvoSys-2NNI} against MD-train.
- **Independently confirmed** the paper's qualitative claim that 2-NNI is closer to MD than 1-NNI: D_KL(2-NNI‖MD-train) = 0.0125 vs D_KL(1-NNI‖MD-train) = 0.0375 (~3× closer). Total variation gives the same ordering (0.060 vs 0.095).
- Copied `extra_analysis.py` into `work/` and `extra_analysis.json` into `report/evidence/`.
- Wrote `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`.
- Verdict: PARTIAL REPLICATION (strong). Every released-scope number reproduces exactly; two paper comparative claims independently verified; Tables III/IV/V correctly labelled as beyond-released-scope rather than fabricated.

## Compute + data locations
- Analysis host: uicgpu (`ssh uicgpu`), workdir `~/replicate-osti-2587616/`.
- Data: `uicgpu:~/replicate-osti-2587616/EvoSys-Research-Data-Code/` (git clone).
- Scripts + results mirror: this replication dir (`~/Dropbox/REPLICATE-PROJECT/OSTI-2587616-vacancy-diffusion-hea-ml-md/`).
- No LLM calls were required for this replication (numerical only). Free-endpoint rule respected — the KL/TV analysis, cross-tab validation, and figure generation are all deterministic numerical computations.
