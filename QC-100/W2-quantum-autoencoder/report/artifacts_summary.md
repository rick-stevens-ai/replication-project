# Artifacts Summary — W2-quantum-autoencoder

**Set:** QC-100
**Dir:** `QC-100/W2-quantum-autoencoder/`
**Verdict:** PARTIAL
**Standard:** 8-artifact backfill

## Files

| Path | Purpose |
|---|---|
| `REPORT.md` | Original top-level narrative report (preserved as-is). |
| `replicate.py` | Clean-room QAE implementation: hardware-efficient encoder, trash-fidelity cost, COBYLA training, compression sweep. Pure numpy + scipy. |
| `results.json` | Per-configuration training trash-F and reconstruction-F for latent sizes $k \in \{1,2,3\}$. |
| `report/REPORT.tex` | LaTeX version of the report with an expanded honest-critique section and `\input{open_questions_section.tex}` at the end. |
| `report/open_questions.json` | Machine-readable list of exactly 5 open questions (bare JSON array; each item has `q`, `basis`, `next_steps`). |
| `report/open_questions_section.tex` | LaTeX rendering of the same 5 questions, included by `REPORT.tex`. |
| `report/workflow.md` | Step-by-step account of the replication procedure and substitutions. |
| `report/artifacts_summary.md` | This inventory. |
| `report/failure_analysis.md` | Honest analysis of what was NOT exercised (paper-specific ensemble, classical baseline, noise, scale, optimization gap at max compression). |
| `extraction/nougat.mmd` | Placeholder stub — Nougat OCR not run; arXiv LaTeX source is authoritative and cited in the report. |

## Headline exercised?
**Partially.** The QAE mechanism (train encoder on trash-$\ket{0}$ fidelity, decode
with $U^\dagger$) was independently reimplemented and the proxy-cost + graceful
degradation claims were directly verified on a controlled low-rank ensemble.
The paper's specific molecular ($H_2$) demonstration was substituted, no
classical PCA/SVD baseline was drawn, and the maximum-compression case is
optimization-limited. Verdict PARTIAL is preserved from the original report.
