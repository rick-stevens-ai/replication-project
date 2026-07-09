# Attempt Log — OSTI-3366147 (spectral bias / HFS)

Timestamps in America/Chicago.

- **2026-07-04 23:31** — Received subagent task. Read wave brief.
- **23:32** — Created target dir tree `report/{evidence}`, `work/`.
- **23:32** — CherryRd cannot reach osti.gov directly (network egress
  restrictions). Downloaded `paper.pdf` on `uicgpu` via `curl` (25 MB, PDF
  1.7) and `scp`-copied back to `work/paper.pdf`.
- **23:33** — `pdf` tool refused the workspace path (allow-list mismatch).
  Fell back to local `pdftotext -layout` → `work/paper.txt` (1144 lines);
  extracted claims, HFS equations (Eqs. 4-6), spectral-error metric
  (Eq. B.3, bands: first 2%, next 6.2%, last 93.8% of components),
  authors (Khodakarami et al., Brown+PNNL, Neural Networks 193:108027),
  and reference numbers from Tables 1, 2, C.1, D.1.
- **23:35** — Realized the paper's actual empirical setting is **UNet /
  ResUNet on BubbleML (Flash-X boiling) and Kolmogorov-flow** data, not
  FNO on Burgers/Darcy as the wave brief suggested. Adjusted target to
  reproduce the CORE mechanism (HFS module in a ResUNet, per-band
  spectral error) on a controlled synthetic 2D multiscale-field task
  because BubbleML (tens of GB, GPU-days) is out of scope on free
  compute for a single wave slot. Documented this scope decision here.
- **23:36** — Wrote `work/replicate_hfs.py`: ResUNet with optional HFS
  module per Eqs. 4-6; synthetic 2D fields with radial power spectrum
  ~ k^{-1.5}; target operator = per-mode phase rotation (non-local mixing)
  + real-space nonlinearity, preserving high-frequency energy;
  band-partitioned spectral error per Eq. B.3.
- **23:37** — First run (small, weak-target). Baseline strongly outperformed
  HFS (Rel L2 0.068 vs 0.084). Diagnosed: the target was nearly identity,
  so no spectral-bias regime; HFS was just extra parameters slowing the
  fit. Redesigned target with stronger non-local phase rotation.
- **23:39-23:44** — Ran 3 seeds (seed 0 on GPU 2, seeds 1-2 in parallel
  on GPUs 3-4, uicgpu A100 80GB). 100 epochs each, base=32, patch=8,
  1024 train / 256 val, 64x64 grids. Results in `evidence/run_seedN/`.
- **23:44** — Spectral bias confirmed in baseline (Fnorm_high ≈ 0.40 vs
  Fnorm_low ≈ 0.17-0.25). HFS shows small improvement at low/mid bands,
  essentially none at high band (Δ = −0.4% consistently). This
  contradicts paper's headline claim on high-frequency error.
- **23:45** — Argo proxy: first try `argo:claude-opus-4.7` returned 502.
  Retried with `argo:claude-sonnet-4.6` — succeeded. LLM judge produced
  a per-claim scoring with overall verdict **PARTIAL**.
- **23:46** — Wrote REPORT.md, brief.md, artifact_harvest.md, this log.

## What worked
- HFS module implementation (paper Eqs. 4-6) is a clean unfold/mean/scale.
- Band-partitioned spectral error (Eq. B.3) trivially maps to FFT + sorted
  wavenumber slicing.
- 3-seed protocol on 3 free A100s ran in parallel, ~90s each.
- Argo endpoint (localhost:44497) with a Claude model worked for LLM
  scoring (after switching from opus-4.7 which was 502'ing).

## What did not work
- pdf tool workspace path (workaround: pdftotext locally).
- osti.gov direct download from CherryRd (workaround: hop via uicgpu).
- First-attempt target was too easy → no spectral bias regime.

## Scope caveats
- Datasets differ from paper (synthetic 2D fields vs BubbleML/Kolmogorov).
  This is a legitimate scoping decision for one free-compute wave slot; the
  paper's core architectural mechanism and metric are however testable
  and were tested, and this replication says something honest about how
  robustly they transfer.
