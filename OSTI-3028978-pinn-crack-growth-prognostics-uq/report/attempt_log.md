# Attempt log — OSTI 3028978 X-TFC crack-growth prognostics replication

## 2026-07-04 (subagent session)

### 18:57 Started
- Read wave brief. Confirmed constraints: free endpoints only, LLM-judge
  scoring (not regex), write only inside target dir.

### 18:58 PDF download failed from CherryRd
- Direct `curl` to `https://www.osti.gov/servlets/purl/3028978` from CherryRd
  hung with HTTP 000 (connection blocked/dropped).
- Tried `https://www.osti.gov/api/v1/records/3028978` and biblio page — same.
- Switched to `uicgpu` (which has ANL/UIC proxy egress via `~/env.sh`): PDF
  download succeeded in ~1s (200, 7,451,125 bytes).
- rsync'd back to local target dir.

### 19:03 Paper text extraction
- `pdftotext -layout work/paper.pdf work/paper.txt` → 842 lines.
- OpenClaw `pdf` tool failed with "Anthropic credit balance too low";
  fallback direct text extraction fine.
- Read paper end-to-end: identified X-TFC algorithm (Eq 17-25), Head's
  theory ODE (Eq 9, 15), Table 1/2 quantitative claims, and the crucial
  data availability statement.

### 19:06 Prerequisite paper (Bechhoefer & Dubé 2020)
- Downloaded from PHM Society open-access (via uicgpu again). Confirmed:
  raw HI dataset is proprietary (GPMS Inc.), not public.
- Concluded: exact numerical replication impossible without the raw HI
  stream. Chose to (a) re-implement X-TFC from paper equations, (b)
  synthesize a physics-consistent HI trajectory that satisfies the exact
  ODE in the paper's physics loss.

### 19:10 X-TFC implementation v1 (`work/xtfc_replication.py`)
- Coded from paper equations: TFC constrained expression (Eq 21), ELM
  random projections (Eq 19), linear LSQ solver (Eq 25).
- Initially used `anchor='left'` (only x(t_min)=a0=0.05 fixed via
  constrained expression).
- First run: 100%-data lp=1 error was 57 h, not 0 h. Debugged: my
  synthetic data used `a(t) = a0 + (af-a0)*xi^p` (shifted power law) which
  does NOT satisfy Head's ODE exactly. Head's ODE `da/dN = a*K1/N` has
  pure power-law solution family `a = C*N^K1` with a(N=0)=0.

### 19:25 Fixed synthetic data
- Changed to `a_true = af * xi^K1 + baseline` (baseline≈0.05 to reflect
  nonzero starting HI seen in Fig 2a, then rescaled so a(t=0)=af=1).
- Also added `anchor='both'` (two-endpoint TFC constrained expression)
  and `anchor='right'` variants for testing.
- Realized: paper's TASK is prognostic — model predicts when HI will hit
  1 given early data — so `anchor='right'` (which pins x(0)=1) would be
  cheating. Correct choice = `anchor='left'` (only IC at start of window
  is fixed; extrapolation is genuinely controlled by physics vs data
  trade-off).

### 19:35 Ran full replication (`xtfc_replication.py main`)
- Table 1 reproduced: 100%data lp=1 → 0.00 h; errors grow monotonically
  with less data and (mostly) with less physics weight.
- Table 2: MC ensemble UQ trends reproduced (ME magnitude grows, SDE
  grows, CIs widen with less data).
- Wall time: sub-millisecond per single fit, ~0.1 s for 100-member MC
  ensemble.
- Saved evidence: `report/evidence/table1_rul_error.json`,
  `report/evidence/table2_mc_uq.json`,
  `report/evidence/physics_regularization_sweep.json`,
  `report/evidence/fig_replication_fits.png`,
  `report/evidence/fig_replication_uq.png`,
  `report/evidence/synthetic_hi_dataset.npz`,
  `report/evidence/run_log.txt`.

### 19:55 LLM judge (Argo `argo:gpt-5`, free)
- First tried `argo:claude-opus-4.7` — HTTP 502 (Argo intermittent).
- Fell back to `argo:gpt-5` — succeeded.
- Judge gave PARTIAL verdict with per-claim scoring:
  - C1 (algorithm implementable) REPRODUCED
  - C2 (ground-truth 0h) REPRODUCED
  - C3 (data-availability trend) REPRODUCED
  - C4 (physics-weight trend) PARTIAL (75% row weak)
  - C5 (>10x low-data gain) NOT REPRODUCED (only ~2.6x)
  - C6 (calibrated CIs) NOT REPRODUCED (wider than paper)
  - C7 (ME grows) PARTIAL (dips at 25%)
  - C8 (SDE/CI widen) REPRODUCED
  - C9 (sub-ms fits) REPRODUCED
  - C10 (SCADA extension) N/A
- Full raw response: `report/evidence/llm_judge.json`.

### What worked
- Downloading via uicgpu (ANL proxy) for CherryRd-blocked OSTI/PHM URLs.
- Pure NumPy X-TFC implementation from paper equations only, no external
  reference code.
- pdftotext for reading the paper when Anthropic-backed pdf tool was down.
- Argo gpt-5 as fallback for judge when Argo Claude was 502'ing.

### What didn't
- Vision tools (image, pdf) all failed with "Anthropic credit too low" or
  "gemini-3-flash-preview unknown" — could not use LLM vision to digitize
  Fig 2a HI curve. Fell back to physics-consistent synthetic data.
- Getting the exact Table 1 magnitudes — physically impossible without the
  proprietary Bechhoefer & Dubé HI stream (paper's own admission).
- The physics regularization sweep at 25% data with `abs(err)` gave
  paradoxical results because the low-physics-weight fits often fail to
  cross HI=1 within domain and get clipped to +/-500 h. The Table 2 signed
  errors give a more honest UQ picture.
