# Artifact Harvest — OSTI 3018489 (wa-hls4ml)

All artifacts pulled from public sources on 2026-07-04 by this subagent.

## Paper PDF
| Item | URL | Size | Notes |
|------|-----|------|-------|
| Paper PDF (OSTI) | https://www.osti.gov/servlets/purl/3018489 | 234.6 MB | 29 pages; downloaded via uicgpu (CherryRd cannot reach osti.gov directly) then scp'd back. ACM TRETS 19(2) Art. 20. |

## Code repository
| Item | URL | Size | Notes |
|------|-----|------|-------|
| Paper code repo | https://github.com/fastmachinelearning/wa-hls4ml-paper | 1.7 MB (repo) | Referenced but NOT cloned for this replication — reproduction is text-only from the paper description, cleaner as an independent check. |

## HuggingFace dataset (fastmachinelearning/wa-hls4ml, CC-BY-NC 4.0)
| Split file | HF path | Size | Samples |
|------------|---------|------|---------|
| test_2_20_merged.json | test/ | 21.9 MB | 1,432 |
| test_2layer_merged.json | test/ | 41.7 MB | 9,797 |
| exemplar_models.json | exemplar/ | 5.98 MB | 887 (886 with valid targets) |
| train_2_20_merged.json | train/ | 103.6 MB | 6,677 |
| train_2layer_merged.json | train/ | 194.8 MB | 45,716 |

Not downloaded (out of scope for this pass): train/test/val {3layer, conv1d, conv2d, latency, resource}_merged.json — an additional ~3 GB of training data used by the paper.

Base URL pattern: `https://huggingface.co/datasets/fastmachinelearning/wa-hls4ml/resolve/main/<split>/<file>`

## Provenance of numbers we compare against
| Reference | Location in paper | What we use it for |
|-----------|-------------------|--------------------|
| Table 4 "Test-All" MLP row | p. 20:18 | Compare paper baseline MLP R²/SMAPE/RMSE vs our reproduction. |
| Table 4 "Test-Dense" MLP row | p. 20:18 | Closer scope match to our dense-only reproduction. |
| Table 5 exemplar per-model rows | p. 20:20 | Compare exemplar-generalization gap trend. |
| §4.1 Baseline MLP description | p. 20:15 | Basis for our feature and training recipe. |
| §3.2 Benchmark Metrics (Eqs 1–3) | p. 20:12–13 | Exact R², SMAPE (ε=1), RMSE formulas. |
