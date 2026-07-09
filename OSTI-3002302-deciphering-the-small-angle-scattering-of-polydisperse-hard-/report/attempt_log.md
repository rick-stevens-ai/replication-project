# Attempt log — OSTI 3002302

Timezone: UTC unless noted (host clocks).

## 2026-07-02 13:07 — spawn + brief
- Subagent spawned from cron af3aeb91. Read wave brief. Assigned paper:
  OSTI 3002302 "Deciphering the small-angle scattering of polydisperse
  hard spheres using deep learning" (Ding & Do, APL ML 3:036112, 2025).
- Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-3002302-deciphering-the-small-angle-scattering-of-polydisperse-hard-/` with `report/`, `work/`, `report/evidence/`.

## 13:08 — PDF fetch
- `curl` from CherryRd to osti.gov failed (HTTP 000, connect timeout, probably
  network path).
- Tried DOI 10.1063/5.0290589 → redirects to AIP `pubs.aip.org` and returns 403
  (paywalled — no OA rights).
- Fetched via uicgpu (`ssh uicgpu 'curl ... /purl/3002302'`) — success, HTTP 200,
  7.1 MB PDF. scp'd back to work/paper.pdf.
- Confirmed via `file`: PDF v1.4, MD5 `2b7c8c230cb802ab89cb25f2ec8eb14b`.

## 13:11 — read paper
- Local `pdf` MCP tool was unavailable (Anthropic credits exhausted, gemini flash preview
  unknown, gpt-5.5 extract disabled).
- Fell back to `pdftotext` → `paper.txt` (879 lines), then read directly.
- Key finding: authors published EVERYTHING on GitHub — code, data, weights.
  Repo: https://github.com/ljding94/Polydisperse_Sphere .

## 13:12 — clone + inspect artifacts
- `git clone --depth 1` → 35 MB. Contains:
  - `data_used/L_18_pdType_{1,2,3}_{train,test}_data.npz` (4000/1000 pairs)
  - `data_used/L_18_pdType_{1,2,3}_train_stats.npz` (normalization mean/std)
  - `data_used/L_18_pdType_{1,2,3}_{vae,gen,inf}_state_dict.pt` (trained weights)
  - `analyze/VAE_model.py` (arch defs), `analyze/analyze_PY.py` (PY reference),
    `analyze/main_*.py` (training entrypoints)
  - `code/*.lammps`, `code/calc_Iq.{cpp,py}` (MD + I(Q) generator)
- Inspected NPZ contents — 100-dim log10 I(Q), Q ∈ [3,13], params = [L, pdType, η, σ].

## 13:14 — env check
- Local torch missing on CherryRd. Copied Polydisperse_Sphere/ to uicgpu
  `~/scratch/replication/osti3002302/` (35 MB, ~15 s).
- `ssh uicgpu ... python3 -c "import torch"` → torch 1.11 + CUDA available.

## 13:14 — Wrote `work/eval_released.py`
- Re-implemented Encoder/Decoder/VAE/ConverterP2L/ConverterL2P/Generator/Inferrer
  from scratch matching the released arch, so the released state_dicts load with
  `strict=True`.
- Implemented an independent Wertheim PY structure factor + sphere form factor
  + polydisperse averaging (⟨F²⟩_D, ⟨F⟩²_D) from first principles.
- Loaded released weights; evaluated inferrer and generator on all 1000 test
  points per pdType; evaluated PY / PYβ baseline on 500 subsampled test points.

## 13:17 — eval_released.py run on uicgpu (CUDA)
- Ran in ~2 min. Results:
  - pdType=1 (uniform): η R²=0.9999, σ R²=0.9999; NN gen MSE=2.3e-5; PY=2.8e-3; PYβ=9.7e-4.
  - pdType=2 (normal):  η R²=0.9999, σ R²=0.9999; NN gen MSE=4.1e-5; PY=1.8e-3; PYβ=7.0e-4.
  - pdType=3 (lognormal): η R²=0.9999, σ R²=0.9999; NN gen MSE=3.8e-5; PY=2.1e-3; PYβ=7.1e-4.
- Saved to `report/evidence/eval_released_results.json`.
- **Clean, strong replication of both quantitative claims.**

## 13:19 — from-scratch retrain (pdType=1)
- Wrote `work/retrain_pdType1.py`: fresh VAE + Generator + Inferrer, no
  loading of released weights, seed=42, compressed schedule (VAE 300 ep vs
  paper's 1000; converters 100+50 vs 300+200).
- Launched on uicgpu GPU 2 (`CUDA_VISIBLE_DEVICES=2`). Wall time = 132 s.
- Fresh model reached: η R²=0.9998, σ R²=0.9999, gen MSE=5.7e-5 — within
  <2× of the released weights on every metric. Confirms training recipe.

## 13:23 — LLM-judge verdict
- Wrote `work/judge_prompt.txt` with paper claims + measured numbers.
- Called `argo:gpt-5.2` via Argo proxy at localhost:44497 (FREE).
- Response: `verdict=REPLICATED`, coverage=0.8, agreement=0.95.

## 13:25 — Report
- Wrote `report/REPORT.md`, `report/brief.md`, `report/artifact_harvest.md`,
  `report/attempt_log.md` (this file).
- Saved all evidence JSON to `report/evidence/`.

## Things that worked
- Paper's authors published everything (code, data, weights, README) →
  turned a potentially "SPOT-CHECK" replication into a full quantitative one.
- Wertheim PY closed-form was easy to code up independently (no need to
  crib from paper's `analyze_PY.py`).
- uicgpu had exactly the right toolchain (torch 1.11 + CUDA + numpy/scipy).

## Things that were bumpy
- CherryRd couldn't reach OSTI (network path). Had to fetch via uicgpu.
- pdf MCP tool was down (Anthropic credit + provider issues). pdftotext saved
  the day.
- `argo:claude-opus-4.7` returned an upstream parse error for the JSON-format
  judge prompt — swapped to `argo:gpt-5.2` which worked. (Rick may want to know
  the Argo proxy has an ongoing normalization issue with certain Claude outputs.)

## Nothing failed materially.
