# Parser Provenance — Zhang SPDE DeepXDE Re-pass

## Date
2026-06-23

## Paper Identification (corrected this pass)
- **Title:** Quantifying total uncertainty in physics-informed neural networks for solving forward and inverse stochastic problems
- **Authors:** Dongkun Zhang, Lu Lu, Ling Guo, George Em Karniadakis
- **arXiv:** 1809.08327v1, submitted 21 Sep 2018
- **Published:** Journal of Computational Physics 397 (2019) 108850
- **DOI:** 10.1016/j.jcp.2019.07.048
- **Method introduced:** NN-aPC (Neural Network + arbitrary Polynomial Chaos), with dropout for approximation uncertainty and active learning for sensor placement.

## ⚠️ Pass-1 paper-identity error
Pass 1 (`report/REPORT_v2.md`) referenced this paper correctly in §C of the appendix, but then ran a **completely different method** (parametric PINN with parameters as NN inputs) on **completely different examples** (stochastic advection, Burgers, reaction–diffusion — those are from the *Modal Space* paper, arXiv:1905.01205, which has a separate replication at `PDE-replications/modal-space-stochastic-zhang-2019/`).
That is the root cause of the "low agreement" verdict: it was the wrong paper's examples being compared.

This pass restarts against the real arXiv:1809.08327 (NN-aPC) examples.

## Parser used
- Source: arXiv preprint PDF, downloaded 2026-06-23 12:58 CDT from `https://arxiv.org/pdf/1809.08327`.
- Local copy: `paper/zhang_1809.08327_quantifying_uncertainty.pdf` (4.31 MB, SHA verifiable via `shasum`).
- Text extraction: `pdftotext -layout` (Poppler), 1265 lines.
- Cross-check: numeric tables (Table 1, Table 2) and equation/parameter values pulled from the extracted layout text and quoted verbatim in `REPORT.md`.
- `pdf` Vision tool unavailable this session (Anthropic credits exhausted, Gemini/GPT PDF disabled).

## Tables actually present in paper
- **Table 1** (line 755 of extracted text): "Comparing the relative L2 error when using the 1st- and 2nd-order aPC expansion, and using data from 4 k-sensors and 7 u-sensors for training." — Inverse stochastic elliptic example (§4.1.2).
- **Table 2** (line 999): "Comparison of the relative L2 error at different steps" — Active learning for inverse stochastic elliptic (§4.3), Steps 0, 1, 2, 11.

No other numeric tables. Other quantitative content is in figures (Fig. 8b, 9, 16 — error-vs-#sensors curves) and inline text (DNN sizes, learning rates, etc.).
