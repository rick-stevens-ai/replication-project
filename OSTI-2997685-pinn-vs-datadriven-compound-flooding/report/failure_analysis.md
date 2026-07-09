# Failure analysis — OSTI-2997685

## Overall

Verdict = REPLICATED, but three friction / caveat categories are worth documenting.

## 1. Genuine failures (none — but near-misses)

No hard failure. Two attempted paths that had to be worked around:

- **PDF-tool provider failure**: the local `pdf` extractor tool errored on `paper.pdf` with a
  "credit balance too low" (Anthropic) plus "model unknown / plugin unavailable" for Google and
  OpenAI paths. Worked around by (a) running `pdftotext` on uicgpu to get raw layout text,
  (b) running `marker_single` in the local `marker` conda env on uicgpu, and (c) running `nougat`
  from the `/gpustor/stevens/anaconda3/envs/nougat` env. All three succeeded.
- **Marker relative-path bug**: `marker_single` internally does `open(path, 'rb')` from the CWD it
  was launched from, ignoring `cd`. First attempt failed with `FileNotFoundError: 'osti_2997685.pdf'`
  when invoked with a bare filename. Fixed by passing an absolute path.

## 2. Partial / soft mismatches

- **C2 (best data-driven balance)** — Paper says "CNN-LSTM = best balance". Verified metrics table
  places LSTM (R^2 = 0.9905) and GRU (R^2 = 0.9901) *ahead* of CNN-LSTM (R^2 = 0.9882) at
  comparable training time on the Ne=800 Irene event. Not a contradiction, but the "best balance"
  ranking is a soft judgement rather than a strict Pareto dominance. This is captured as Open
  Question Q2 with concrete next steps.
- **C4 (FD-PINN across noise)** — Paper implies FD-PINN "matches or improves" vanilla-PINN accuracy
  across noise levels. Verified: FD-PINN strictly wins at 0% and 10% noise but is nominally worse
  (by 1e-3 to 2e-3 R^2, which is within single-seed variance) at 0.1%, 0.5%, 1%, 5%. Score PARTIAL
  in the strict sense, but consistent with the qualitative claim; averaged across the sweep the
  gap is +0.001 R^2 in favor of FD-PINN with 6.5x training-time win. See Open Question Q1 for the
  seed-variance follow-up.
- **C3 (data efficiency)** — PINN and data-driven models are validated on different held-out sets
  (PINN on same-channel test; data-driven on Hurricane Irene). A rigorous "same-observations, same
  metric" comparison is not possible from the released artifacts alone. Reported PARTIAL.

## 3. Residual gaps not resolved by this replication

- Full retraining of vanilla PINN (~15 GPU-hours) not performed: would establish seed-level
  reproducibility (would answer Q1) but not required to verify the paper's headline number, which
  is baked into the released `.out` logs.
- Data-driven training-ensemble sensitivity (Q4): no seed exposed in `myearth.py`, so we cannot
  quantify ranking stability under resampling. Would need code changes to reproduce.
- 2-D / multi-reach generalization (Q3, Q5): out-of-scope for this paper's own release; separate
  study.
- Large binary payloads (Telemac ensembles + high-res .slf) staged on uicgpu but not archived to
  Dropbox for this replication because (a) they are 700 MB combined and (b) the numerical claims
  are verifiable from the released `.csv` metric aggregates. They remain retrievable via the
  Figshare API at any time.

## 4. What would be needed to close the residual gaps

- Retrain vanilla PINN and FD-PINN under >=5 seeds per noise level -> ~450 GPU-hours (~1 GPU-week
  on uicgpu) to close Q1 with proper error bars.
- Instrument `myearth.py` for controlled resampling -> low-cost code change + 8 x 6 = 48 model
  retrains (~2 GPU-days) to close Q4.
- Extend FD-PINN to 2-D coastal patch -> non-trivial code fork of `SVE_module_dynamic_uh_mff_ts_l2_FDM.py`
  (~500 LOC + validation vs an established 2-D SW solver) to close Q3.

## 5. Assumptions used in this replication

- Trusted the paper's own training-time log line `PINN Time elapsed: <sec>` as the ground-truth
  timing measure. Not independently retimed (would have required GPU-hours we did not spend).
- Trusted the per-Ne metric arrays and metrics CSVs in the release as faithful outputs of the
  released `train_*.py` scripts. Not re-derived from the trained-weight `.pickle` files.
- Assumed "CNN" in the released code = "CNN-FC" in the paper (confirmed by inspection of
  `plot_data_driven_comparison_Irene.py` which explicitly labels `metrics_CNN_Irene.csv` as
  "CNN-FC" in its subplot legend).
- Grouped LSTM, GRU, CNN-LSTM as "sequence-aware" and CNN-Conv, U-Net, U-Net-tiny as
  "non-sequence" for the C5 verification. CNN-FC excluded from both groups because its
  fully-connected readout blurs the taxonomy (it consumes time-stacked inputs but has no
  recurrence or 1-D-time convolution).
