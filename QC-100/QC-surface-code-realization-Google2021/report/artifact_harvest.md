# Artifact harvest

## Papers (public, arXiv)
| File | Source URL | Bytes | SHA-256 | What |
|---|---|---|---|---|
| `work/google2023_surface_code.pdf` | https://arxiv.org/pdf/2207.06431 | 12,405,361 | 38e1fc02adb0737b72a48fe329b994d536157508473e05d2fe74907f31922896 | **Scientific target** — Google, "Suppressing quantum errors by scaling a surface code logical qubit", Nature 2023 (Λ₃/₅=1.10) |
| `work/zhao2021_zuchongzhi.pdf` | https://arxiv.org/pdf/2112.13505 | 1,479,812 | 90e713aa90fbf07811a675341f6082f6b55eaa025b6dbb192a644daa4648a767 | The arXiv ID the task *cited* — Zhao et al., Zuchongzhi-2.1 distance-3-only (verified NOT the d3-vs-d5/Λ paper) |
| `work/arxiv_abs.html` | https://arxiv.org/abs/2112.13505 | 47,862 | — | Abstract page used for identity check |
| `work/arxiv_google.html` | https://arxiv.org/abs/2207.06431 | — | — | Abstract/title page for the Google paper |
| `work/google_fulltext.txt` | (pypdf extraction of the Google PDF) | 160,898 chars | — | Extracted text used to pull exact paper numbers |

## Software (PyPI, pinned; full list in evidence/requirements.txt)
- stim 1.16.0
- pymatching 2.4.0
- numpy 2.5.0
- scipy 1.18.0
- pypdf (text extraction only)
- Python 3.14.6, host CherryRd (macOS)

## Generated results (real Monte-Carlo)
| File | SHA-256 | What |
|---|---|---|
| `work/results_c1.json` (=evidence/) | ac16f80f3811cb276cf37ebf24e5e52046a3a04b4c736931c0dd248dfbff2dec | LEC d3/d5 at p∈{.001,.002,.003,.005}, 500k shots, 25 rounds |
| `work/results_c34.json` (=evidence/) | 0d91b776bc3a588323345722e7728a56c3a16bb5653e1ca82f9bf21fb4bf714a | Λ(p) sweep d3/d5/d7, 14 p-points, 150k shots, 25 rounds; crossover + Λ=1.10 interpolation |

## LLM judge
- Endpoint: Argo proxy `http://127.0.0.1:44497/v1` (FREE), model `argo:gpt-4.1`, temp 0.1.
- `report/evidence/judge_prompt.txt`, `report/evidence/judge_verdict.txt` → FINAL_VERDICT: PARTIAL.

## Not harvested (out of scope / unavailable)
- Sycamore device calibration data, raw stabiliser measurement records (not part of the reproducible core; hardware).
- Google's approximate-max-likelihood decoder implementation (used MWPM/PyMatching baseline instead).
