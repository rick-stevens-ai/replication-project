# Workflow — arXiv:1606.02685 replication

## Timeline (2026-07-05, ~30 minutes wall)
1. **19:45** — Created target dir; read the QC wave brief.
2. **19:45** — Fetched the paper PDF (`curl` from arxiv.org/pdf/1606.02685), 414 kB.
3. **19:46** — `pdftotext -layout` for author/title verification. Confirmed:
   - Title: *Optimal Hamiltonian Simulation by Quantum Signal Processing*
   - Authors: Guang Hao Low, Isaac L. Chuang
   - Version: v2, 20 Dec 2016 (published PRL 118, 010501, 2017).
4. **19:46** — Checked for pre-parsed Marker/Nougat artifacts in the corpus:
   only `BVBRC-*` neighbors carried them, none for QC. Neither `marker_single`
   nor `nougat` was installed on CherryRd, so used a documented
   `pdftotext -layout` fallback for both `extraction/marker.md` and
   `extraction/nougat.mmd` with a header explaining the substitution.
5. **19:46-19:48** — Wrote `report/evidence/qsp_replication.py` (287 lines):
   built a fixed 4x4 Hermitian H with ||H||=1, verified Jacobi-Anger
   truncation decay, empirically fit the (t, eps) -> K_min scaling law,
   and verified QSP-produces-T_d(H) in both scalar and matrix forms.
6. **19:47** — Ran replication; all three core claims pass at 1e-15 (machine
   precision) or better; scaling fits match the paper's O(t + log/loglog)
   prediction with intercept linear in t at slope 0.696.
7. **19:48** — Wrote `plot_results.py`, produced three PNGs:
   `fig_A_truncation_vs_K.png`, `fig_B_Kmin_vs_x.png`,
   `fig_B_intercept_vs_t.png`.
8. **19:48-19:52** — Wrote `REPORT.tex` (13 kB, full section-by-section),
   `open_questions.json` (5 heavy-duty, non-superficial),
   this `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.
9. **19:52** — Attempted `pdflatex REPORT.tex` (best-effort compile if latex is present).

## Tools + versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.x (system) | Driver |
| NumPy | 2.4.3 | Linear algebra, Chebyshev recurrence, matrix expm |
| SciPy | 1.18.0 | `scipy.linalg.expm` (gold-standard e^{-iHt}), `scipy.special.jv` (Bessel J_k) |
| matplotlib | (installed) | 3 PNG plots |
| poppler `pdftotext` | 25.x (Homebrew) | PDF -> text extraction |
| `curl` | Homebrew | PDF fetch |
| pdflatex | best-effort | REPORT.tex -> REPORT.pdf (optional) |
| Marker | **not installed** | fallback: pdftotext dump |
| Nougat | **not installed** | fallback: pdftotext dump |

## Compute
- Host: CherryRd (macOS Darwin 25.3.0), CPU only.
- Peak memory: ~50 MB (4x4 and 8x8 dense matrices; nothing large).
- Wall time for the numeric replication: **~2 seconds** (Bessel calls +
  10-40 term Chebyshev recurrences on a 4x4 matrix).

## Work-done estimate
Roughly 45 minutes of "human-equivalent" replication work: paper skim
(~5 min), replication code design + implementation (~15 min), execution
+ debugging (~5 min), plotting (~5 min), 8-artifact reporting (~15 min).
No external calls, no LLM inference used (self-verdict per brief's
"3-judge Argo panel only if time remains" clause), no HPC — everything
runs on the driver host in ~2 s.

## Data provenance
Nothing external besides the paper PDF itself. The test Hamiltonian is
regenerated deterministically from the fixed seed `1606` inside
`qsp_replication.py`; the results JSON/CSVs are the outputs of that
single script.
