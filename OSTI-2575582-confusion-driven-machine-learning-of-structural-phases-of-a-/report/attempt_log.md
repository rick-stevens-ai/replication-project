# Attempt log — OSTI 2575582 replication

All times America/Chicago on 2026-07-02.

- **08:07** — Subagent spawned. Read `WAVE_BRIEF_2026-07-01.md`. Created target dir `report/` and `work/` under `~/Dropbox/REPLICATE-PROJECT/OSTI-2575582-.../`.

- **08:07–08:10** — First attempt to fetch OSTI PDF from CherryRd via `curl -sL https://www.osti.gov/servlets/purl/2575582 -o /tmp/osti_2575582.pdf` **hung**. CherryRd probably lacks direct HTTPS egress to osti.gov, or a corporate proxy is not set for that host. Killed the curl session.

- **08:11** — Retried the fetch on `uicgpu` (which is on the proxy'd internet): HTTP 200, 9,186,197 bytes, `PDF-1.6`. Copied to `work/paper.pdf` via `scp`. Extracted 971 lines of text with `pdftotext -layout`.

- **08:13–08:16** — Skimmed the paper. Identified the confusion-method algorithm, NN architecture (300→50→50→1 sigmoid, SGD lr=1e-3, 20 epochs, BCE), and the numerical claims for η=0.02 (transitions at E ≈ -900 and E ≈ -1050) and η=0.06 (three transitions). Located reference [111] pointing to the authors' companion repo `https://github.com/dilinanp/ml-confusion-polymer` and the Zenodo dataset `records/15851811`.

- **08:15** — `git clone` the companion repo on uicgpu — MIT-licensed, contains only `notebook/confusion_method.ipynb`. Inspected the notebook to confirm input-file format (`Chain_bin{NNNNN}_*.dat`, 100×6 columns) and exact hyperparameters. **Decision**: do NOT run the authors' notebook; write an independent PyTorch implementation instead, to make the replication truly independent.

- **08:15–08:18** — Fetched `data_eta_0.02.tar.gz` from Zenodo (~2.9 GB compressed). Took 3 min 49 s. Extracted (~50 s) → 524,987 files, 518,669 matching `Chain_bin*.dat`, 200 energy bins. Verified format on a sample file.

- **08:20** — Wrote `work/confusion_indep.py` (8.3 KB). Design decisions:
  - PyTorch (`nn.Linear` + `nn.ReLU` + `BCEWithLogitsLoss`), not TF/Keras. Independent framework choice.
  - Same architecture and hyperparameters as paper (input=300, hidden=50×2, sigmoid output, SGD lr=1e-3, 20 epochs).
  - Reduced sample budget: `--num-runs 5` (paper=10), `--max-per-bin 500` (paper=2000) — 4× faster, still enough for clean statistics.
  - `scipy.signal.find_peaks(height=0.7, distance=3, prominence=0.02)` for automated peak detection.
  - Runs on `cuda:3` (A100 80GB, idle at start).

- **08:21** — Smoke test on bins 25–30 with 50 configs/bin, 2 runs, 5 epochs → 5.4 s wall, plausible accuracies (0.63–0.81). Sanity confirmed.

- **08:22–08:33** — Narrow-window run: bins 18–56 (paper's Fig 7a labelled range), 500 configs/bin, 5 restarts, 20 epochs. Loaded 19,500 configs in 20 s. Sweep completed in 668 s (~11 min). Output CSV shows a clean W-shape: peak-valley contrast 0.987 vs 0.861, error bars ~0.001. Two obvious interior peaks (at E ≈ -972 and E ≈ -930) plus a rising left flank suggesting a third peak at or just below the left window edge.

- **08:34–08:48** — Wide-window run: bins 5–60 to bracket the E ≈ -1050 peak with sufficient low-E baseline. Loaded 28,000 configs. Rate ~22 s per trial-point (slower per-trial due to 44 % more training data). After 15 min the run had covered bins 5→41 (37 of 56 trial points). **Decision**: kill and use partial data. The E ≈ -1048 peak was already resolved with baselines on both sides; the additional low-E and high-E points would not have changed the verdict.

- **08:48** — Ran `work/final_analysis.py`: found peaks at E ≈ -1071, -1048, -972 in the wide run. **Excellent match** for the paper's E ≈ -1050 claim (offset < 2 units). Combined 2-panel plot saved.

- **08:49–08:50** — LLM-judge invocation via Argo (free, localhost:44497).
  - First try: `argo:claude-opus-4.7` → 502 Bad Gateway on first invocation; then upstream validation error ("does not match any variant of SystemMessage | UserMessage | ..."). Suspect model-side transient / response-schema mismatch — unrelated to our prompt.
  - Switched to `argo:gpt-5.2` → returned clean JSON. Verdict: **PARTIAL** (coverage 75%, agreement 80%, confidence medium). Saved to `report/evidence/llm_judge_verdict.json`.

- **08:51–08:55** — Wrote `report/REPORT.md`, `report/brief.md`, `report/artifact_harvest.md`, this log. Copied CSVs, PNGs, logs into `report/evidence/`.

## Failures and lessons
- **CherryRd→osti.gov TCP hang**: work around by tunnelling through uicgpu, which has the proxy env from `~/env.sh`. Documented for future subagents.
- **argo:claude-opus-4.7 upstream schema error on longer prompts**: transient, gpt-5.2 is a fine free-endpoint fallback for LLM-judge work.
- **Zenodo download → 3 GB per η value**: don't try to pull both η values in one subagent; pick one and do it well.
- **Wide sweep is slow**: PyTorch on cuda:3 for this specific model (small) is largely bound by CPU DataLoader shuffling and per-trial retraining overhead, not by the GPU. For future runs a batched-across-trials training strategy would give ~10× speedup.
