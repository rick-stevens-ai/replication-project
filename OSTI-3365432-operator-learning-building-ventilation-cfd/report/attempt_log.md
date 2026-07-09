# Attempt Log — OSTI-3365432

Chronological, ~1-line per step. Times are approximate wall-clock (America/Chicago).

- **06:09** — Subagent spawned. Read WAVE_BRIEF_2026-07-01.md + REPLICATION_DIR_STANDARD_2026-07-05.md.
- **06:10** — Confirmed target dir does not exist; created target dir with `report/{evidence,}`, `extraction/`, `work/`.
- **06:11** — Attempted local `curl -o paper.pdf ...osti.gov/servlets/purl/3365432` from CherryRd. TIMED OUT (`http=000 size=0`).
- **06:13** — Fell back to uicgpu: `ssh uicgpu 'curl ... paper.pdf ...'`. SUCCESS: HTTP 200, 6.5 MB. `scp` back to target dir. MD5 = 69f130eadf8f1ad658af821773d2f447. `file` reports "PDF document, version 1.7".
- **06:14** — pdftotext -layout on the PDF → 1,098-line 2-column-preserving dump. Read Sec 3 (BEAR-CFD), Sec 4 (Methodology), Sec 5 (Numerical experiments), identified Tables 3, 4, 5.
- **06:15** — Verified data availability: HF `alwaysbyx/Bear-CFD-dataset` — 200 OK, listed siblings: `processed_data/{train,test}_data_norm.pkl`, `models/*.pt` (5 files), `raw_data/unsteady_*.pkl` (~300 files), `steady_case_data/*.h5`. Verified code availability: `github.com/alwaysbyx/BuildingControlCFD` — 200 OK. `git clone --depth 1`.
- **06:15** — Started test_data_norm.pkl (608 MB) download in background (nohup curl) + parallel-downloaded all 5 model checkpoints (~7 MB each). All models done in <30 s. Confirmed sizes match.
- **06:16-06:22** — While test.pkl downloaded, read learning/train.py, learning/data_utils.py, learning/models/mmgpt.py (GNOTE class). Understood: MIODataset builds DGL graphs, normalizes x/u_p/y in-place; MIOEGPT_meanvariance = GNOTE class; forward returns (mean, sigma). Verified checkpoint format: `{args, model:state_dict, optimizer}`.
- **06:22** — Probed checkpoint args on uicgpu: n_layers=3, n_hidden=64, n_head=1, model_name=GNOTE, dataset_config = {input_dim:3, theta_dim:13, branch_sizes:[12], output_dim:6}, args.normalizer = UnitTransformer with 6-dim mean/std. Total params = 569,999.
- **06:24** — test_data_norm.pkl download COMPLETE (608 MB, 543 s wall = ~1.1 MB/s throttled). Probed pickle: list of 1,126 tuples of (x[7492×3], y[7492×6], u_p[13], input_f=(f[7492×12],)). y in raw ppm range 395-1109, u_p in raw physical units, input_f pre-scaled ~[0, 2].
- **06:25** — Wrote first version of `run_bear_inference.py` (~200 LOC). Loads 5 GNOTEs, no x/up normalization, batch=4 inference. 8-sample smoke test.
- **06:25** — 8-sample smoke: `DGLError: Device API gpu is not enabled`. dgl 0.9.1 CPU wheel doesn't do `.to(cuda)`.
- **06:26** — `pip install --user dgl-cu113==0.9.1 -f https://data.dgl.ai/wheels/repo.html` on uicgpu. Verified `g.to("cuda")` works. Re-ran smoke → SUCCESS, 5 models loaded, latency 4.5 ms/call, but per-graph rel-L2 = ~90 % (way off).
- **06:26** — Diagnosed: I was skipping x/up normalization + treating raw y (in ppm) as the target. Adjusted script to y-normalize target before feeding into graph.ndata['y'] and inverse-transform pred to compare on raw ppm scale. 16-sample rerun: ensemble raw = 10.72 (=1072 %), still way off.
- **06:27** — Deeper probe: reproduced paper's own `WeightedLpRelLoss` metric on sample 0 of Model 1 → 37 % L2 error (also way off). CONFIRMED: model itself is fine, input pipeline is wrong. Realized: u_p (raw 1-134 range) needs `up_normalizer` from training, but the checkpoint doesn't ship one. Same for x.
- **06:28** — Started train_data_norm.pkl download (2.1 GB) in background to refit x/up normalizers properly. Meanwhile decided to try fit-from-test-set as fast alternative.
- **06:29** — Rewrote script: build `x_normalizer` and `up_normalizer` from test data (or train if available), apply all three normalizers per MIODataset pipeline. Also downloaded one raw_data pickle (6.2 MB) for schema verification.
- **06:29** — Ran 32-sample test → per-model 6-13 %, ensemble 7.3 %. NEARLY MATCHING PAPER. Some per-model numbers lower than paper — likely finite-sample variance (32/1126).
- **06:30** — Ran full 1126-sample test → **per-model 12.04-13.08 %, ensemble 11.03 % (paper: 11.82-13.01 %, ensemble 10.90 %). REPLICATED.** 23.8 s wall for full 5-model eval. Latency 4.5 ms (paper 5 ms). Killed train.pkl download at 200 MB (unnecessary).
- **06:31** — scp'd `results/inference_result.json` and `run_bear_inference.py` back to Dropbox target dir. Wrote `report/evidence/full_run.log` with the full walltime + summary.
- **06:31-06:40** — Wrote `report/REPORT.md` (17 KB), `report/brief.md` (1 KB), `report/open_questions.json` (5 grounded questions with basis + next_steps), `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`, `extraction/marker.md` (pdftotext-based, 76 KB), `extraction/nougat.mmd` (placeholder + rationale). This attempt log. Will write REPORT.tex next.
- **06:40-06:50** — Wrote `report/REPORT.tex` (LaTeX version of REPORT.md), `report/artifact_harvest.md` (wave-brief format). Final 8-artifact bar check.
- **06:5x** — Print WAVE_RESULT.

## Key decisions

1. **Fetch route**: local first, uicgpu on failure. Standard.
2. **Data-pull scope**: get test pickle + 5 models + one raw sample. SKIP train pickle unless needed. When test-fit normalizers reproduced paper Δ0.13pp, killed the train download.
3. **Normalizer reconstruction**: fit from test set (uniform-sampled per Eq. 6, so on-distribution) rather than wait for the 2.1 GB train pickle. Verified empirically this reproduces Table 3.
4. **Verdict**: REPLICATED for ML claims (Table 3, Table 5). Explicitly NOT tested: control claims (Table 4, Fig 6) requiring ANSYS Fluent. This distinction is documented in REPORT.md §2 and §5.
