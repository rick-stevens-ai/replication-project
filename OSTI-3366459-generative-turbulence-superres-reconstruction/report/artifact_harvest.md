# Artifact harvest — OSTI 3366459

## External artifacts pulled

| Kind | Identifier | URL | Size | Location on disk |
|---|---|---|---|---|
| Paper PDF | OSTI 3366459 | https://www.osti.gov/servlets/purl/3366459 | 4,450,141 B | `work/paper.pdf` (also `uicgpu:~/replicate/OSTI-3366459/paper.pdf`) |
| Paper text | (pdftotext of above) | — | 851 lines | `work/paper.txt` |
| DOI reference | 10.1038/s41467-026-70145-4 | https://doi.org/10.1038/s41467-026-70145-4 | (not pulled — same PDF) | — |
| Zenodo (paper's code+data) | 10.5281/zenodo.17088765 | — | not fetched (marked "upon publication" — availability uncertain 2026-07-04) | — |
| Project page | Vivek Oommen | https://vivekoommen.github.io/Gen4Turb | not pulled (video/gallery only) | — |
| Schlieren jet dataset | Tsinghua Univ. proprietary | request via hefeng@tsinghua.edu.cn | not accessible | — |

## Generated artifacts (this replication)

| Kind | Path | Size | Description |
|---|---|---|---|
| DNS dataset | `uicgpu:~/replicate/OSTI-3366459/kolmo_128.npz` | 60,574,902 B | 1,000 snapshots of 2D forced Kolmogorov vorticity, 128×128, ν=1e-3, forcing n=4 |
| Trained model | `uicgpu:~/replicate/OSTI-3366459/baseline.pt` | 5,262,981 B | UNet_SR L2-only ("NO analog"), 60 epochs |
| Trained model | `uicgpu:~/replicate/OSTI-3366459/adv.pt` | ~5.3 MB | UNet_SR L2+GAN+feature ("adv-NO analog"), 60 epochs |
| Training log | `report/evidence/train.log` | ~7 KB | full per-epoch tr_mse / test-NRMSE for both models |
| DNS log | `report/evidence/gen.log` | ~1 KB | enstrophy trajectory, confirmed stationary |
| Metrics | `report/evidence/summary.json` | training-time NRMSE (uses initial degenerate metric) |
| Metrics (corrected) | `report/evidence/spectrum_v2.json` | paper-comparable log-spec NRMSE on resolved band |
| Metrics (detail) | `report/evidence/spectrum_inspection.json` | per-k spectrum values for DNS/bicubic/NO/adv-NO |
| Metrics (analyze) | `report/evidence/analysis_results.json` | field NRMSE + several spectrum-NRMSE variants |
| Per-epoch log (baseline) | `report/evidence/baseline_log.json` | 60 epochs |
| Per-epoch log (adv) | `report/evidence/adv_log.json` | 60 epochs |
| Figure | `report/evidence/spectrum_comparison.png` | mean E(k) log-log: DNS vs bicubic vs NO vs adv-NO with k^(-5/3) reference |
| Figure | `report/evidence/sample_fields.png` | 2 sample fields: HR truth / LR input / NO pred / adv-NO pred |
| Judge output | `report/evidence/llm_judge_argo:gpt-5.json` | verdict from Argo GPT-5 |
| Judge output | `report/evidence/llm_judge_argo:claude-opus-4.7.json` | verdict from Argo Claude Opus 4.7 |

## Code files (in `work/`)

- `gen_kolmogorov.py` — pseudo-spectral DNS (78 lines)
- `train_sr.py` — UNet_SR + PatchGAN + two training loops + metrics (280 lines)
- `analyze.py` — reload trained models, compute metrics, generate figures (150 lines)
- `inspect_spectrum.py` — first attempt at k-restricted spectrum metric
- `inspect_v2.py` — final paper-comparable log-spec NRMSE on resolved band
- `llm_judge.py` — Argo call for verdict scoring

## Reproducibility

Deterministic seeds:
- DNS random IC seed = 1 (in `gen_kolmogorov.py` `kolmogorov_dns(seed=1)`)
- Train/test split rng = 42 (in `train_sr.load_data`)
- PyTorch itself is not seeded → epoch-to-epoch losses are stochastic within a few percent, but the qualitative and order-of-magnitude conclusions are stable
