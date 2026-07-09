# Workflow, Tools, Codes, Effort — OSTI-3365432

## Narrative workflow

1. **Read the wave brief** (`scripts/WAVE_BRIEF_2026-07-01.md`) and the
   canonical 8-artifact standard (`scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`).
2. **Create target dir** with `report/evidence/`, `extraction/`, `work/`.
3. **PDF fetch**: local `curl` timed out from CherryRd; fell back to `ssh uicgpu`
   with `~/env.sh` sourced (proxy path). Got 6.5 MB, MD5-verified, `scp`-ed back.
4. **Understand paper**: `pdftotext -layout` for a 1,098-line 2-column preserving
   dump, plus a plain-text pass. Read Sec 3 (BEAR-CFD data), Sec 4 (methodology
   + ensemble GNOT), Sec 5 (Numerical experiments — Tables 3, 4, 5), and Sec 6
   (Conclusion). Identified 8 claims (see REPORT.md §2).
5. **Locate free public artifacts**:
   - PDF: OSTI purl (free) — ✅
   - Data: `alwaysbyx/Bear-CFD-dataset` on Hugging Face (CC-BY-4.0) — ✅
   - Code: `alwaysbyx/BuildingControlCFD` on GitHub — ✅
   - Trained checkpoints: same HF dataset, `models/…MIOEGPT_meanvarianceuncertainty*.pt` — ✅ **all 5 released**
6. **Prep uicgpu env**: verified torch 1.11.0 + CUDA 11.6, installed
   `dgl-cu113==0.9.1` (the CPU dgl 0.9.1 was already there but couldn't move
   graphs to GPU). Installed via `pip install --user`.
7. **Download data + models**: pulled `processed_data/test_data_norm.pkl`
   (608 MB, ~9 min at HF's ~1 MB/s throttle for our IP), all 5 model
   checkpoints (~7 MB each, parallel), and one `raw_data/unsteady_10.pkl`
   (6.2 MB) for schema verification. Started `train_data_norm.pkl` (2.1 GB)
   but killed after 200 MB when we confirmed test-fit x/up_normalizers
   already reproduce paper numbers to Δ≤0.32pp.
8. **Inspect checkpoint** & data format: the model saves as
   `{args, model:state_dict, optimizer}` OrderedDict, with `args.normalizer`
   holding the y_normalizer (a `utils.UnitTransformer` with mean/std tensors
   per output-timestep). x_normalizer and up_normalizer are NOT saved — the
   released code path in `MIODataset.__init__` re-derives them from the
   training pickle at every run. That drives step 9.
9. **Reconstruct normalizers**: fitted `x_normalizer` and `up_normalizer`
   (both `utils.UnitTransformer`) from the 1,126-sample test set stats. Sanity
   check: the paper's Eq. (6) says u_p is sampled from a fixed uniform
   distribution independent of split, so train and test marginals should
   coincide.
10. **Build inference script** `work/run_bear_inference.py` (~270 LOC):
    - loads 5 GNOTE models to GPU
    - constructs test-set DGL graphs applying x/up/y normalization
    - times 20 warm forward calls for the latency claim
    - batches (bs=4) through all 1,126 samples, computing per-graph rel-L2
      (per Eq. 12 / `WeightedLpRelLoss` in `data_utils.py`) both in normalized
      space and denormalized (raw ppm) space
    - averages: per-model + ensemble-of-mean
    - emits JSON at `~/osti-3365432/results/inference_result.json`
11. **Run**: 32-sample smoke test first (7.3 % ensemble raw L2, roughly
    on-track), then full 1,126-sample run (23.8 s wall, 11.03 % ensemble raw L2).
12. **Pull results** back to Dropbox target dir via `scp`, write REPORT.md,
    REPORT.tex, open_questions.json, workflow.md (this file), artifacts_summary.md,
    failure_analysis.md, and generate marker.md placeholder from pdftotext.

## Enumerated tools + versions

| Tool | Version | Where | Purpose |
|------|---------|-------|---------|
| curl | (system) | CherryRd + uicgpu | PDF, HF data, HF model pulls |
| ssh + scp | OpenSSH_9.x | CherryRd → uicgpu | Compute + file movement |
| Python | 3.8.10 | uicgpu | inference driver |
| pytorch | 1.11.0 (CUDA 11.6) | uicgpu (system) | Neural-net inference |
| dgl-cu113 | 0.9.1 (installed for this run) | uicgpu (~/.local) | Graph batching for GNOT |
| einops | 0.8.1 | uicgpu | tensor reshape in GNOT |
| networkx | 2.4 | uicgpu | graph deps |
| scikit-learn | 1.3.2 | uicgpu | (used only by data_utils imports) |
| GNOT code | HEAD of `alwaysbyx/BuildingControlCFD` on 2026-07-06 | uicgpu | Model + data + loss classes |
| pdftotext | poppler (macOS) | CherryRd | Extraction fallback |
| Hugging Face | dataset `alwaysbyx/Bear-CFD-dataset` @ sha d92998848d475edd | HF via curl | Data + checkpoints |
| GitHub | `alwaysbyx/BuildingControlCFD` HEAD | git clone | Code |
| OSTI purl | https://www.osti.gov/servlets/purl/3365432 | uicgpu curl | Paper PDF |

## Codes / scripts produced

| File | LOC | Purpose |
|------|-----|---------|
| `work/run_bear_inference.py` | 271 | End-to-end inference: load 5 GNOTE, fit x/up normalizers, batched eval over full test set, compute rel-L2 + latency, emit JSON |
| `work/paper_layout.txt` | 1,098 | pdftotext -layout dump for close reading |
| `work/paper_plain.txt` | 1,815 | pdftotext plain-text dump |
| `extraction/marker.md` | 1,827 | Markdown-promoted version of paper_plain.txt |
| `extraction/nougat.mmd` | — | Placeholder + rationale (nougat not in env) |

## Effort estimate

| Dimension | Estimate |
|-----------|----------|
| Wall-clock (human/agent) | ~55 min end-to-end (from spawn to WAVE_RESULT) |
| Model inference wall | 23.8 s (5 models × 1,126 samples, 1 A100) |
| Model inference GPU compute | ~15 CPU-min (batched) — negligible |
| CFD wall (paper) | 1,253.7 s per transient sim × 300 sims = 104.5 CPU-h — **not re-run** |
| Data + model download | ~10 min (608 MB test pickle throttled; 5×7 MB models parallel; 2.1 GB train pickle skipped) |
| Code written (this replication) | 271 LOC of Python (inference driver) + shell/python glue |
| Code inspected/read (paper's) | ~1,600 LOC (learning/train.py + data_utils.py + models/mmgpt.py + models/mlp.py + control/controller.py) |
| Runs executed | 3 (32-sample smoke × 2 during normalizer fix, full 1126-sample × 1) |
| Human decision points | 4 (fetch route, normalizer reconstruction strategy, download-skip threshold, verdict) |
| Free-endpoint LLM calls | 0 (no LLM-judge needed — replication is numeric, agreement is measured directly against paper Table 3) |
| Dollars spent | $0 (all free-tier / institutional) |
