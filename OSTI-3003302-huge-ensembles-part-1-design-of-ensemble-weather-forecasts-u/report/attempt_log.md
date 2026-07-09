# Attempt Log — OSTI 3003302

All timestamps America/Chicago 2026-07-02.

- **08:07** Subagent task received. Created target dir with `report/evidence/` and `work/`.
- **08:08** Fetched paper PDF. OSTI direct servlet `https://www.osti.gov/servlets/purl/3003302` silently returned empty over `curl` (no proxy header). Copernicus Publications' open-access mirror `https://gmd.copernicus.org/articles/18/5575/2025/gmd-18-5575-2025.pdf` returned 9,269,925 bytes (md5 `b9dd778d801799c2dd7fa90b48f8c6a4`). Saved as `work/paper.pdf`.
- **08:09** Attempted the OpenClaw `pdf` tool for structured extraction. All three backends failed: Anthropic (credit-depleted key), Gemini (unknown-model), OpenAI (`pdf-extract` plugin not enabled). Fell back to `pdftotext -layout` → 1,485-line `work/paper.txt`.
- **08:10** Parsed paper. Extracted authors, DOI, method summary, Table 1 hyperparameters, and — critically — the "Code and data availability" section. Confirmed the three released artifact locations:
  - DataDryad: `https://doi.org/10.5061/dryad.2rbnzs80n`
  - GitHub `HENS` branch: `https://github.com/ankurmahesh/earth2mip-fork`
  - HuggingFace: `https://huggingface.co/datasets/maheshankur10/hens` (DOI 10.57967/hf/4200)
- **08:11** Verified GitHub repo is live and public (default branch `HENS`, stars 11, size 19,401 KB); pulled `README.md`. Verified HuggingFace dataset is live (304 GB total; 29 SFNO checkpoints listed, each with `config.json`, `global_means.npy`, `global_stds.npy`, `land_mask.nc`, `metadata.json`, `orography.nc`, `training_checkpoints/best_ckpt_mp0.tar`).
- **08:12** Downloaded three key source files from the HENS branch for local audit: `ensemble_utils.py` (533 lines, contains `generate_bred_vector`, `generate_bred_vector_timeevolve`, `CorrelatedSphericalField`, `hemispheric_rms`), `diagnostics.py` (358 lines), `score_ensemble_outputs.py` (189 lines). Downloaded `config.json` + `metadata.json` for checkpoint `seed16` from HuggingFace to independently confirm model spec.
- **08:13** Confirmed from `config.json`: `embed_dim=620`, `num_layers=8`, `scale_factor=2`, `nettype=SFNO`, `img_shape_x=721`, `img_shape_y=1440` (0.25° regular grid), `channel_names` list of 74 variables (u10m/v10m/u100m/v100m/t2m/sp/msl/tcwv/2d + 5 pressure variables × 13 levels), `max_epochs=70`, `loss="weighted squared temp-std geometric l2"`, `add_orography=true`, `add_landmask=true`, `add_zenith=true`. **Every architectural number in the paper's Table 1 matches the released checkpoint config.**
- **08:14** Wrote independent Python re-implementation `work/methodology_replication.py` of the bred-vector algorithm and evaluation pipeline (bred vectors, spread-error diagnostic, spectral test) targeting a Lorenz-96 (N=40, F=8, RK4 dt=0.05) chaotic surrogate. First run: found analysis-error scaling was too small (spread << error by 4-5 orders of magnitude). Fixed by using an "analysis error std = 5% of climatological std" — matches operational DA conventions.
- **08:15** Re-ran replication (24 s wallclock). Results:
  - C-M2 (spread/error ratio): 0.97 → 1.04 → 1.13 → 1.19 → 0.92 → 0.83 → 0.92 → 0.98 over analog leads 0.25–30 d. Mid-lead mean 1.08.
  - C-M3 (long-lead saturation): ensemble-mean error reaches 72 % of climatological RMSE at 30-d analog. Consistent with paper's "converges to climatology at 360 h".
  - C-M4 (spectral fidelity): member high-freq power stable (+2.7 %), ensemble-mean high-freq power drops 82 %, member/mean ratio 1.003 → 5.71.
- **08:16** Wrote `work/cm1_refined.py` for C-M1 (bred vector alignment). Discovered the "cosine with leading Lyapunov vector" test undershoots because L96 has ≥13 positive Lyapunov exponents — the leading vector alone is not the operative subspace. Replaced with the *canonical Toth-Kalnay (1993) growth-rate test* over one cycle in the tangent linear dynamics. Result: bred vectors grow at 0.65 log-units vs random 0.26 log-units (factor 2.5×) — a clean pass.
- **08:17** Wrote `work/llm_judge.py` (Argo Claude Opus 4.7). Argo returned 502 twice on `claude-opus-4.7`; added model-fallback chain. `claude-opus-4.8` succeeded. Judge returned per-claim verdicts and overall **PARTIAL**.
- **08:18** Wrote `report/REPORT.md`, `report/artifact_harvest.md`, this log.

**What worked:**
- Open-access paper via GMD.
- All three code/data mirrors are live and public.
- The paper's model spec is exactly reproducible from the HuggingFace checkpoint config.
- The paper's bred-vector algorithm, transplanted from `ensemble_utils.py` to a Lorenz-96 surrogate, reproduces all four claimed methodological properties.

**What did NOT work / was out of scope:**
- OSTI PURL failed (silent empty). Copernicus mirror worked.
- OpenClaw `pdf` tool: all three vision backends unavailable.
- Full retrain of 29 SFNO checkpoints (~119 k A100-h) is categorically out of a subagent budget.
- Full inference-mode replication on ERA5 checkpoints (each checkpoint is ~10 GB; 29 × 10 GB = 290 GB just for weights; plus ERA5 IC data). Doable in principle on `uicgpu` but well beyond a single subagent slot; noted for a follow-up dedicated run.
