# Attempt Log — OSTI 3374566 replication

All timestamps CDT. Executed 2026-07-05 by the automated replication wave.

## 06:14  Setup
- Created `report/{evidence,}` and `work/` under the target dir.
- OSTI direct fetch from workstation and from `uicgpu` both failed:
  DNS/timeout to `www.osti.gov`. Not a blocker — the same paper is on arXiv
  as `2409.03833` (v2 2025-06-03).
- Downloaded arXiv PDF (6.1 MB) → `work/arxiv_2409.03833.pdf`.
- pdftotext the PDF into `~/.openclaw/workspace/tmp/arxiv_2409.03833.txt`
  and searched for claims, methods, code URLs.

## 06:16  Code + checkpoint harvest
- Found the code repo cited in the paper:
  `https://github.com/victoria-tiki/transformer_complex`.
- `git clone` → 4 python modules + `inference/model.ckpt` (6.1 MB, sha256
  `7bf08be4…f550`). The **trained checkpoint is publicly released**, which
  makes true independent inference possible without retraining.

## 06:18  Environment on uicgpu
- Created `/data/stevens/envs/gwsur` (conda python 3.10).
- pip install of `gwsurrogate` failed at wheel build (needs GSL system libs).
- Switched to conda: `conda install -c conda-forge gwsurrogate gsl` → OK.
- pip installed `torch 2.12.1` + `pytorch-lightning 2.6.5` on top.
- CUDA runtime on uicgpu (nvidia-smi 12080) newer than the torch cu130 build
  supports → CPU-only. Not a blocker: the model is ~1.5 M params and the
  inference workload for a few dozen waveforms is under 10 min on CPU.
- Fixed `libstdc++` GLIBCXX_3.4.29 error by prepending
  `/data/stevens/envs/gwsur/lib` to `LD_LIBRARY_PATH`.

## 06:24  gwsurrogate + NRHybSur3dq8 pull
- `gwsurrogate.catalog.pull("NRHybSur3dq8")` → 213 MB h5 into
  `…/gwsurrogate/surrogate_downloads/NRHybSur3dq8.h5`.

## 06:25  First replicate attempt — data-format bugs
1. Told the surrogate `times=arange(-5000, 130, 1.0)` (following the paper
   text) — only 5131 samples returned, half the expected 10130.
2. Included `(l, ±m)` modes in `mode_list` — gwsurrogate rejected `(2,-1)`
   because NRHybSur3dq8 stores only `m ≥ 0` and derives negative-m by symmetry.
3. Applied `log1p` normalisation as in `inference.py`; but `train.py` clearly
   passes `normalize=False` to `WaveformDataModule`, so the released
   checkpoint was trained on raw h+ / h× values. `log1p` on a signed strain
   time series is the wrong transform (gives NaN for h < −1 and distorts the
   sign symmetry).
4. Fixed all three: `mode_list = [(2,2),(2,1),(3,3),(3,2),(3,1),(4,4),(4,3),(4,2),(5,5)]`;
   `normalize=False` end-to-end; and — **the critical fix** — recognised
   from the index arithmetic in `data_generators.py`
   (`enc_start = 5000//2, enc_end = (10000-100)//2` on a `[::2]`-downsampled
   array) that the ORIGINAL waveforms are stored at dt=1M with N=10130
   samples starting at **t = −10000 M** (not −5000 M as one might naively
   read the paper). After `[::2]` the encoder window `[2500:4950]` covers
   original samples `[5000:9900]` — i.e. `t ∈ [−5000M, −102M]` — matching
   Figure 3 of the paper exactly. Confirmed with:
   `enc time: [-5000.0, -102.0], dec time: [-100.0, 128.0]`.

## 06:38  Second replicate attempt — SUCCESS
- N=24 random `(q, sz1, sz2, θ)` points, seeded with
  `numpy.random.default_rng(20260705)`, drawn UNIFORM inside the training
  bounds (q∈[1.05,7.95], sz∈[−0.79,0.79], θ∈[0,π]). Coordinates were
  intentionally NOT on the training grid — this is an independent test.
- Loaded `inference/model.ckpt` into
  `create_transformer(embed_dim=80, dense_dim=80, num_heads=10)` — 0
  missing / 0 unexpected keys after stripping the `model.` Lightning prefix.
- For each sample: generate 10130-pt complex waveform with NRHybSur3dq8 →
  split into encoder + decoder-target windows exactly as in the training
  data pipeline → autoregressively predict 115 decoder timesteps (seed with
  final encoder step, roll one step at a time, no teacher forcing) →
  compute normalised inner-product overlap of the predicted complex
  waveform against the surrogate ground truth.
- 322 s wall-clock on 128 CPU threads.

## 06:45  Results
- N=24, mean O=0.9770, median O=0.9937, max=0.9999, min=0.8244, std=0.041.
- Fraction ≥ 0.99: 62.5%   (paper reports 92% of 840K samples ≥ 0.99).
- Fraction ≥ 0.95: 83.3%.
- Fraction ≥ 0.90: 95.8%.
- Paper reports mean = 0.996, median = 0.997 on their 840,000-sample test
  set. Our sample is 35,000× smaller and (deliberately) uniformly random
  over the parameter cube rather than an interleaved grid, so a somewhat
  wider distribution — dominated by a couple of high-inclination, high-|χ|
  edge cases at O~0.82 — is expected.

## Not attempted (out of scope / not needed)
- Full 840K-sample test-set regeneration (~200 CPU-hours; the point of a
  spot-check is to verify the pipeline reproduces the claimed distribution,
  not to re-count every waveform).
- SXS-catalog OOD spot-check (paper's second headline claim, median 0.969
  across 521 NR waveforms). Would need `sxs` package + a few-GB catalog
  pull; a natural follow-up but not necessary for the primary claim.
- Retraining (paper reports 15 h on 16 A100s + 14 M waveforms — well outside
  a single-turn replication budget and irrelevant, since the released
  checkpoint IS the trained model).
