# Workflow — QC-2111.05451 (Shaydulin & Wild, QML kernel bandwidth)

## Human-readable summary

1. **Ingest.** Fetched arXiv 2111.05451 (v4, Sep 2022). PDF stored at `work/paper.pdf`; text extraction at `work/paper.txt`.
2. **Identify testable claims.** Parsed abstract + Fig. 1a/1b + Fig. 2 to identify 6 claims (C1–C6). C1–C4 = mechanism claims (small-sim testable); C5 = scaling extrapolation (expensive); C6 = dataset breadth.
3. **Environment.** Built `.venv` with `pennylane==0.45.1`, `scikit-learn==1.9.0`, `numpy==2.5.0`, `matplotlib`. CPU-only on CherryRd.
4. **Reimplement feature map from paper Eq. 5.** IQP-style, depth 2:
   `U(x) = ∏_{r=1..2} H^⊗n · exp[i(Σ λ x_j Z_j + Σ λ² x_j x_k Z_j Z_k)]`.
   Written in PennyLane as `RZ(-2λx_j)` + `IsingZZ(-2λ²x_jx_k)`. Verified no code copied from authors' repo.
5. **Data.** `sklearn.make_moons(80, noise=0.2)`, standardized, lifted 2→4d via `[x1, x2, sin x1, cos x2]`, restandardized, 40/40 stratified split.
6. **Single-seed sweep.** `code/run_bandwidth_sweep.py`, λ ∈ {0.01, 0.05, 0.1, 0.3, 1.0, 3.0, 10.0}. ~4s CPU. Output: `evidence/bandwidth_sweep.{csv,json}`.
7. **Multi-seed replication.** `code/multi_seed_confirm.py`, 5 seeds × 7 λ = 35 fits. ~25s CPU. Output: `evidence/bandwidth_sweep_multiseed.json`.
8. **Classical baselines.** Linear SVM + RBF SVM on same 40/40 split → both 0.875.
9. **Figure.** `figures/accuracy_vs_bandwidth.png` — train/test acc vs λ with classical-RBF and 0.5 reference lines; off-diagonal K on twin axis.
10. **LLM-judge check.** Argo GPT-5.2 (free, `127.0.0.1:44497`) → `{"verdict":"REPLICATED","confidence":0.84}`. Argo Opus 4.7 returned a validation error; single-judge deemed adequate given the unambiguous 0.510 ± 0.052 collapse.
11. **REPORT.md.** Written on 2026-07-03 documenting all 6 claims, replication outcome, and evidence artefact locations.
12. **8-artifact backfill (2026-07-05).** LaTeX report (`REPORT.tex`), open questions (`open_questions.json` + `.tex`), workflow (this file), artifact summary, failure analysis, and nougat stub added without re-running simulations.

## Machine-readable timeline

```
2026-07-03  arXiv PDF fetch                                          -> work/paper.pdf
2026-07-03  pdftotext + claim identification                         -> work/paper.txt, REPORT.md §2
2026-07-03  venv + deps                                              -> .venv/
2026-07-03  feature-map + kernel implementation                      -> code/run_bandwidth_sweep.py
2026-07-03  single-seed sweep (λ x 7)                                -> evidence/bandwidth_sweep.{csv,json}
2026-07-03  multi-seed (5 x 7)                                       -> evidence/bandwidth_sweep_multiseed.json
2026-07-03  classical baselines (linear/RBF)                         -> baked into JSON output
2026-07-03  figure                                                   -> figures/accuracy_vs_bandwidth.png
2026-07-03  Argo GPT-5.2 judge (Opus 4.7 fell back)                  -> REPORT.md §6
2026-07-03  REPORT.md (verdict = REPLICATED)                         -> report/REPORT.md
2026-07-05  8-artifact backfill (LaTeX, questions, workflow, ...)    -> report/*.{tex,json,md}
```

## Compute + endpoints

- **Sim:** PennyLane statevector, CPU-only, CherryRd. No GPU / cluster used.
- **LLM judge:** Argo (`http://127.0.0.1:44497/v1`), free per policy. Used `gpt-5.2` after `claude-opus-4.7` validation-errored.
- **NOT used:** paid endpoints (rule); CELS chicago-N vLLM (not needed for a single-shot judge); ALCF Sophia (not needed).

## Reproducibility recipe (verbatim)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2111.05451-qml-kernel-bandwidth
python3 -m venv .venv
.venv/bin/pip install --upgrade pip pennylane==0.45.1 numpy==2.5.0 scikit-learn==1.9.0 matplotlib
.venv/bin/python code/run_bandwidth_sweep.py       # single seed
.venv/bin/python code/multi_seed_confirm.py        # 5 seeds
# LaTeX (backfill artifacts, no sim rerun):
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
