# Workflow — QC-2504.01077 Double-Bracket QSP replication

## Goal
Independently reproduce the four numerically testable claims of Suzuki et al. 2025 (arXiv:2504.01077v3) on a free CPU-only stack (numpy/scipy state vectors), no fabrication.

## Timeline / actions
1. **Fetch paper.** `curl -sL -o work/paper.pdf https://arxiv.org/pdf/2504.01077` → 1.3 MB, PDF v1.7, 2 physical pages (with dense continuation → 4187 pdftotext lines).
2. **Parse.** `pdftotext -layout work/paper.pdf work/paper.txt`; `pdftotext -raw ... work/paper_raw.txt`. Identified:
   - Lemma 1 / Eq. (12)-(16): closed-form linear polynomial synthesis via `exp(iθΨ)·exp(s[Ψ,H])`.
   - Theorem 2 / Alg. 1: recursive DB-QSP for degree-K polynomial with per-step (s_k, θ_k) from energy E_k and variance V_k.
   - Eq. (19): group-commutator formula, error O(s^{3/2}/√N).
   - Prop. C.1: overall approximation error `||Ψ - ω_K|| ≤ (4/3)√(ζ/N)(1+6ξ)^K`.
3. **Environment.** Python 3.14.6 venv at `.venv/` with `numpy==2.5.1`, `scipy==1.18.0` — only pip-installable, wheel-only deps; no build-from-source.
4. **Marker/Nougat extraction — attempted, failed.** `pip install marker-pdf` and `pip install nougat-ocr` both blocked on Python 3.14 (no numpy≤2.0 wheels, no torch wheels for 3.14 yet). Substituted `pdftotext` outputs and documented the substitution in-file and in `failure_analysis.md`.
5. **Implement `report/evidence/db_qsp.py`.** ~350 LOC, four experiments R1–R4, deterministic RNG seed `20260705`.
6. **Run.** `python report/evidence/db_qsp.py` — 0.016 s wall time (4×4 matrices, ~10^4 matrix exponentials total).
7. **Verify.** Piped output to `run.log`; parsed structured results into `results.json`.
8. **Report.** Authored `REPORT.tex` (11 KB, section-by-section per-claim comparison); compiled with `pdflatex -interaction=nonstopmode REPORT.tex` → `REPORT.pdf` (4 pages, 259 KB).
9. **Open questions.** 5 heavy-duty follow-on research questions, each grounded in a specific number from the replication, in both narrative (REPORT.tex) and machine-readable (`open_questions.json`) form.

## Tools + versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 | interpreter |
| numpy | 2.5.1 | linear algebra, RNG |
| scipy | 1.18.0 | `scipy.linalg.expm` (matrix exponential) |
| pdftotext (poppler) | system | PDF → text (as Marker/Nougat substitute) |
| pdflatex (TeX Live 20260301) | system | REPORT.tex → REPORT.pdf |
| curl | system | arXiv fetch |

## Instance size and cost
- All experiments at 4×4 (2-qubit-like) Hermitian matrices.
- R1: 20 random `z`'s × O(3) matrix exponentials each ≈ 60 expm.
- R2: 5 recursion steps × O(2) expm ≈ 10 expm.
- R3: 11 values of N × O(4·N) small expm + one `matrix_power`; asymptotically dominant.
- R4: 5 values of N × 3 recursion steps × O(4·N) expm.
- Total wall time on M-series Mac: **16 ms**. No paid resources, no LLM inference required for the numerical claims.

## Reproduction quickstart
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2504.01077-double-bracket-QSP-no-postselection
python3 -m venv .venv && source .venv/bin/activate
pip install numpy==2.5.1 scipy==1.18.0
python report/evidence/db_qsp.py    # writes report/evidence/{run.log, results.json}
cd report && pdflatex -interaction=nonstopmode REPORT.tex   # optional
```

## Effort estimate
~30 min end-to-end for a fluent numpy user: 5 min to read the algorithm out of the paper, 10 min to implement and cross-validate R1/R2, 5 min for the group-commutator sweep and O(1/√N) fit, 10 min for report and artifact packaging. Marker/Nougat install attempts + fallback added ~5 min.
