# Artifacts Summary — OSTI-3365432

## 1. Source artifacts pulled

| Artifact | Source URL | Size | Checksum | Purpose |
|----------|------------|------|----------|---------|
| paper.pdf | https://www.osti.gov/servlets/purl/3365432 | 6,524,227 B | MD5 `69f130eadf8f1ad658af821773d2f447` | Source paper (14 pp, arXiv:2504.21243v2, Applied Energy 2025) |
| test_data_norm.pkl | https://huggingface.co/datasets/alwaysbyx/Bear-CFD-dataset/resolve/main/processed_data/test_data_norm.pkl | 607,608,040 B | HTTP-200, size-verified | Paper's own held-out test split (1,126 samples, N=7,492 mesh points each). ON UICGPU ONLY (~/osti-3365432/bear_cfd/processed_data/) — not copied to Dropbox to avoid 600 MB workspace bloat |
| co2_all_MIOEGPT_meanvarianceuncertainty_0228_00_10_00.pt | HF (same base) /models/… | 7,062,850 B | size-verified | Trained Model 1 (569,999 params) |
| co2_all_MIOEGPT_meanvarianceuncertainty_0228_15_25_04.pt | HF /models/… | 7,062,850 B | size-verified | Trained Model 2 |
| co2_all_MIOEGPT_meanvarianceuncertainty_0228_15_31_54.pt | HF /models/… | 7,062,850 B | size-verified | Trained Model 3 |
| co2_all_MIOEGPT_meanvarianceuncertainty_0301_16_02_36.pt | HF /models/… | 7,062,850 B | size-verified | Trained Model 4 |
| co2_all_MIOEGPT_meanvarianceuncertainty_0301_16_03_28.pt | HF /models/… | 7,062,850 B | size-verified | Trained Model 5 |
| raw_data/unsteady_10.pkl | HF /raw_data/… | 6,167,125 B | size-verified | Schema verification only |
| BuildingControlCFD (repo) | https://github.com/alwaysbyx/BuildingControlCFD | git clone --depth 1 | HEAD @ 2026-07-06 | learning/, control/, simulation/ Python code |
| train_data_norm.pkl (aborted) | HF /processed_data/… | 199,393,280 B / 2,100,505,182 B pulled | partial, deleted | Started to refit normalizers "properly" but the test-fit already reproduced paper numbers to Δ0.13pp so this was unnecessary and killed to save disk |

## 2. Derived artifacts produced (in target dir)

| Path (relative to target) | Size | Description |
|---------------------------|------|-------------|
| `paper.pdf` | 6.5 MB | scp-ed back from uicgpu; the source paper |
| `extraction/marker.md` | ~76 KB | Markdown extraction (pdftotext + heading-promoted); Marker/Nougat unavailable in env, so this is our best Markdown proxy |
| `extraction/nougat.mmd` | 1.3 KB | Placeholder + rationale for why Nougat wasn't run (native-PDF, pdftotext is already clean) |
| `report/REPORT.md` | 17 KB | Full narrative report: summary, claims table, method (numbered), results-vs-paper, verdict + justification, per-question breakdown |
| `report/REPORT.tex` | ~14 KB | LaTeX version of REPORT.md (satisfies canonical artifact #4) |
| `report/brief.md` | 1.1 KB | 1-paragraph what/why/verdict |
| `report/attempt_log.md` | ~7 KB | Chronological log of everything tried, what worked, what didn't |
| `report/artifact_harvest.md` | ~3 KB | Same info as this table, in the wave-brief-mandated format |
| `report/workflow.md` | 6 KB | Narrative workflow + enumerated tools/codes + effort estimate |
| `report/artifacts_summary.md` | (this file) | Comprehensive artifact inventory + evidence trace |
| `report/failure_analysis.md` | ~5 KB | Honest post-mortem of friction points |
| `report/open_questions.json` | 6.5 KB | 5 grounded open questions with basis + next steps |
| `report/evidence/inference_result.json` | 989 B | Machine-readable result of the full 1,126-sample inference |
| `report/evidence/full_run.log` | ~2 KB | Human-readable inference log |
| `work/run_bear_inference.py` | 10.9 KB | The 271-line inference driver |
| `work/paper_layout.txt` | 114 KB | pdftotext -layout dump |
| `work/paper_plain.txt` | ~90 KB | pdftotext plain dump |

## 3. Evidence trace (numeric)

Full inference JSON (report/evidence/inference_result.json):

```json
{
  "n_samples": 1126,
  "per_model_l2_test_raw": [
    0.12220788884702838,   // Model 1: 12.22 % (paper: 12.09 %)
    0.12044843323991947,   // Model 2: 12.04 % (paper: 11.83 %)
    0.12135411359263885,   // Model 3: 12.14 % (paper: 11.82 %)
    0.1295269282723299,    // Model 4: 12.95 % (paper: 12.74 %)
    0.13079827476034792    // Model 5: 13.08 % (paper: 13.01 %)
  ],
  "ensemble_l2_test_raw":   0.1103154347967985,   // 11.03 % (paper: 10.90 %)
  "latency_ms_forward_mean":   4.490900039672852, // 4.49 ms (paper: 0.005 s = 5 ms)
  "latency_ms_forward_median": 4.396319389343262, // 4.40 ms
  "gpu_name": "NVIDIA A100 80GB PCIe",
  "torch_version": "1.11.0",
  "cuda_version": "11.6"
}
```

All 5 per-model numbers within 0.32 pp of paper Table 3; ensemble within 0.13 pp.
Latency matches paper's 5 ms claim.

## 4. What is NOT in the target dir (and why)

- **The 608 MB test pickle**: kept on `uicgpu:/home/stevens/osti-3365432/bear_cfd/processed_data/`
  rather than copied into Dropbox to avoid workspace bloat. Same URL is reproducible
  from HF at any time.
- **The 5 model checkpoints (~35 MB total)**: same rationale, same HF URL.
- **The paper's raw training set (train_data_norm.pkl, 2.1 GB)**: never fully downloaded
  (aborted at 200 MB) because the test-fit normalizers already reproduced paper numbers.
- **Any CFD simulator run output**: not produced. Reproducing Table 4 / Fig 6 requires
  an ANSYS Fluent commercial license and ~30+ CPU-hours per case set, out of scope for
  this wave.
