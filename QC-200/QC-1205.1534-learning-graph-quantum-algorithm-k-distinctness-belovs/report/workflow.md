# Workflow — Belovs 2012 k-distinctness replication

**Paper:** arXiv:1205.1534, Belovs, "Learning-Graph-Based Quantum Algorithm
for k-distinctness" (2012, v2 = 9 Aug 2012).

**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1205.1534-learning-graph-quantum-algorithm-k-distinctness-belovs/`

## Step-by-step

| # | Step | Command / File | Notes |
|---|------|---------------|-------|
| 1 | Create target dir | `mkdir -p work extraction report/evidence` | |
| 2 | Fetch paper | `curl -sL https://arxiv.org/pdf/1205.1534 -o paper.pdf` | 19 pages, 434 KB. First attempt returned HTML (arXiv redirect page) because no User-Agent; had to add `-A Mozilla/5.0`. |
| 3 | Extract text | `pdftotext -layout paper.pdf work/paper.txt` | 1194 lines. Poppler 25.10.0. Math-heavy sections come through readable but with Unicode subscripts. |
| 4 | Skim + identify headline claim | manual read of §Abstract, §1, §5.2 | Headline: `O(N^{1-2^{k-2}/(2^k-1)})`. Most-checkable single number: k=3 exponent = 5/7 ≈ 0.7143. |
| 5 | Set up Python env | `python3 -m venv work/venv; pip install numpy scipy matplotlib` | Python 3.13.9, NumPy 2.5.1, SciPy 1.18.0. |
| 6 | Implement Eq. (12) | `report/evidence/belovs_kdist.py::belovs_complexity` | Direct translation of the paper's Eq. 12. No approximations. |
| 7 | Optimize per (k, N) | `optimize_belovs()` in same file | 12 restarts of Nelder-Mead in log-space per point; 6 warm-started from paper's asymptotic ρ_i, 6 fully random. Wall clock: ~3 s for the full 4×13=52-point sweep. |
| 8 | Ambainis baseline | `ambainis_baseline()` — closed-form | Analytic minimum of `r + sqrt(N^k/r^{k-1})`, giving Ambainis's Table-1 curve exactly. |
| 9 | Random-weight baseline | `random_weight_baseline()` | 200 samples of log-uniform r_i. Confirms Belovs's weights are non-trivial. |
| 10 | Fit exponent | `loglog_slope()` — `numpy.polyfit(log N, log C, 1)` | 13 N-values (6..256). |
| 11 | Save results | `report/evidence/belovs_results.json` | Full table of C_opt, C_amb, C_rand_best, C_rand_mean, r_opt per (k,N). |
| 12 | Plot | `report/evidence/plot_results.py` → `belovs_replication_plot.png` | 2100×900 PNG. Left panel: log-log complexity curves. Right panel: paper vs fitted exponents. |
| 13 | Write REPORT.tex | manual | 12.7 KB, section-by-section. Includes claims table, method, results-vs-paper table, verdict. |
| 14 | Extraction stubs | `extraction/marker.md`, `extraction/nougat.mmd` | Nougat/Marker not installed in sandbox; pdftotext fallback used and documented per REPLICATION_DIR_STANDARD_2026-07-05.md convention (same as BVBRC-* dirs that also stub pending central parses). |

## Tools & versions

| Tool | Version | Purpose |
|------|---------|---------|
| curl | (system) | Fetch arXiv PDF |
| pdftotext (Poppler) | 25.10.0 | Text extraction |
| Python | 3.13.9 | Numerical driver |
| NumPy | 2.5.1 | Linear algebra + polyfit |
| SciPy | 1.18.0 | `scipy.optimize.minimize` (Nelder-Mead) |
| matplotlib | (Agg backend) | Log-log + bar plot |
| macOS | Darwin 25.3.0 x64 (host CherryRd) | Runtime host |

No GPU used. No LLM called (no Argo / Sophia / CELS / paid API). Total
elapsed wall-clock end-to-end: ~90 s of which ~65 s was
`pip install matplotlib` (venv creation) and ~5 s was compute.

## Work estimate

- Reading (PDF skim + §2, §5.2 close read): ~15 minutes equivalent
- Coding (Eq. 12 + optimizer + plot): ~30 minutes equivalent  
- Report writing: ~25 minutes equivalent
- **Total effort:** ~70 minutes of a human researcher's time, ~90 s of
  agent wall clock.

## What could be added (out of scope for this pass)

1. Solve the actual adversary-bound LP (Definition 1) for small N to get
   the true quantum query complexity Q(f) and compare with C_opt.
2. Implement §6's fault-tolerant construction and re-fit rho_1.
3. Reproduce Theorem 7 (graph collision O(sqrt(N)·α^{1/6})) for a small
   graph family.
4. Round r_i to integers and re-fit rho_1 (test discretization bias).
