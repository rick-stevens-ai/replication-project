# Attempt Log — OSTI 1974586

Chronological, 2026-07-02 (all times CDT).

1. **02:28** — Read WAVE_BRIEF_2026-07-01.md + priority list. Enumerated done dirs (2997724, 2480245, 3007459, 3028840, 3001323 present). Ranks 32/33 (SIMULATeQCD, Nd-diffusion) either heavy multi-GPU or already done.
2. **02:29** — Candidate selection from rank 32+: sought a paper with **in-text scalar/equation claims, no heavy table OCR**. Shortlisted rank 47 (surrogate VQC, PNAS) and rank 50 (VQE critical Ising, PRA). Chose **rank 50 / OSTI 1974586** — its benchmark is the *exactly-solvable* critical TFIM whose ground-state energy density is an analytic scalar (`-4/π`), directly reproducible via free-fermion diagonalization with zero OCR.
3. **02:30** — CherryRd `curl` to osti.gov **timed out** (>60s, no bytes). Routed download through `ssh uicgpu` + `source ~/env.sh` proxy → both candidate PDFs fetched (1974586: 1.35 MB, 2349026: 5.0 MB).
4. **02:30** — `pdftotext -layout` on uicgpu (born-digital PDF, **no OCR required**). Grepped for quantitative anchors: confirmed Eq.(3) Hamiltonian, `-4/π` infinite-volume density (Fig. 2 caption), ~2-orders symmetry-averaging reduction, `<1e-7` at D=6, exact-prep threshold `2p` spins per `p` rounds.
5. **02:30** — Created target dir (collision-checked: none). Copied paper.pdf/txt into work/.
6. **02:31** — Wrote `replicate_tfim.py`: (C-core-1) infinite-volume density via free-fermion ABC spectrum; (C-core-2) finite-L density two ways — free-fermion vs dense spin diagonalization; (C-core-3) QAOA-style depth scan.
7. **02:33** — First run SIGKILLed: QAOA inner loop re-did `eigh(HC)/eigh(HB)` on every objective eval → too slow, and the piped `&& | tail` chain got killed. **Fix:** precompute HC/HB eigendecompositions once outside the objective. Reran unbuffered to `run.log`.
8. **02:36** — Full run completed, `results.json` written. **C-core-1 exact to 1.3e-13; C-core-2 machine-precision agreement + 1/L² convergence; C-core-3 QAOA 5.8%→machine-precision at p=4.**
9. **02:37** — Wrote + ran `symmetry_averaging.py`: verified the KW antiphase-cancellation mechanism → ~2.1 orders suppression at ~1° residual phase mismatch, matching the paper's ~2-order claim.
10. **02:38** — LLM-judge (free Argo `argo:gpt-5.2` via localhost:44497) scored the replication → **PARTIAL**.
11. **02:39** — Wrote report artifacts (brief, harvest, this log, REPORT.md); copied evidence.

**Efficiency note (per task directive):** Zero page-by-page OCR. Used `pdftotext` only; targeted-OCR fallback never triggered. Total wall time ~11 min.
