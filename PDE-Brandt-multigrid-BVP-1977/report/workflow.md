# Workflow — Brandt (1977) Multigrid Replication

Chronological workflow, from paper fetch to REPLICATED verdict. All work on `CherryRd` (macOS, local CPU), Python 3.14.6 + NumPy, no external multigrid library.

## 1. Paper acquisition
```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Brandt-multigrid-BVP-1977/work
curl -sL -A "Mozilla/5.0" -o brandt1977.pdf \
    "https://www.ams.org/journals/mcom/1977-31-138/S0025-5718-1977-0431719-X/S0025-5718-1977-0431719-X.pdf"
# Verify: SHA-256 d4f187bd5bcdb5262214598ab33a98d83affe390800e3b246964746d35089e5b, 6.1 MB
pdftotext -layout brandt1977.pdf brandt1977.txt
```

## 2. Claim extraction
Read paper (both PDF + text extraction). Identified 6 candidate claims C1–C6. Filtered to the 3 numerically testable core claims on the linear-elliptic model problem:
- **C1**: grid-independent V-cycle convergence factor
- **C2**: O(N) work to solution
- **C3**: 2nd-order spatial accuracy of 5-point Laplacian

Out-of-scope (documented but not tested): C4 domain-shape insensitivity (partial), C5 ∞-order adaptive refinement, C6 FAS for nonlinear/transonic.

## 3. Implementation
From-scratch V-cycle multigrid solver in `work/multigrid.py` (~330 LOC):
- Uniform N×N grid, `h = 1/(N-1)`, 5-point Laplacian
- Levels: `N_k − 1 = 2^k`, coarsest 3×3
- Smoother: red-black lexicographic Gauss–Seidel
- Restriction: full weighting (1-2-4 / 16 stencil)
- Prolongation: bilinear interpolation, zero Dirichlet on ∂Ω
- Coarse solve: `numpy.linalg.solve` on 3×3 interior
- Cycle: V(2,1) — 2 pre-smooth, recurse, 1 post-smooth

## 4. Experiments — three passes, one binary
`python3 multigrid.py` runs all three experiments in one shot:

### C1 — grid-independent factor
- Brandt Appendix B problem: `f = sin(3(x+y))`, `g = cos(2(x+y))` on unit square
- Grids: N ∈ {33, 65, 129, 257, 513}
- Solve to `‖r‖₂ < 10⁻¹⁰`, record per-cycle residual, compute ρ_∞ as geometric mean of tail

### C2 — O(N) work
- Same Appendix B problem
- Solve to relative residual reduction `10⁻⁶`, record cycle count and wall-clock
- Work Units: V(2,1) in 2D → 4 WU/cycle theoretical

### C3 — 2nd-order accuracy
- Manufactured solution: `u* = sin(πx) sin(πy)`, `f = −2π² u*`, zero Dirichlet
- Solve to `‖r‖₂ < 10⁻¹²` (iteration error << discretization error)
- Measure `‖u_h − u*‖_∞` and `‖u_h − u*‖_2`; least-squares fit `log ε` vs `log h`

## 5. Post-processing
```bash
python3 plot_results.py  # → report/evidence/brandt_replication_summary.png (3-panel figure)
```
Composite figure: (i) residual histories collapsing on one geometric-decay curve, (ii) ρ vs N with Brandt reference lines, (iii) ε_∞ vs h log-log with O(h²) reference.

## 6. LLM-judge scoring
```bash
python3 llm_judge.py  # → report/evidence/llm_judgment.json + llm_judge_raw.txt
```
Judge: `argo:claude-sonnet-4.6` via Argo free proxy (`127.0.0.1:44497`, key `stevens`), temperature 0.0.
- C1 → PARTIAL / qualitative (grid-independence yes; abs value differs, in predicted direction)
- C2 → REPRODUCED / excellent (5 cycles on every grid)
- C3 → REPRODUCED / excellent (fitted p = 2.000)
- Overall → **REPLICATED**

## 7. Report assembly
- `report/REPORT.md` — main narrative (this replication)
- `report/REPORT.tex` — LaTeX version with dedicated GENUINE CRITIQUE section
- `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md` — companion documents
- `report/open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` — this backfill
- All numerical evidence in `report/evidence/`

## 8. Verdict
**REPLICATED**, in the scope of C1–C3 on the linear-elliptic model problem.

## Compute budget
- Total wall-clock across all 5 grids × 3 experiments: **~2 seconds** on CherryRd CPU. The 513² grid alone solves in 0.236 s.
- No GPU, no external library, no cloud endpoint (except Argo for LLM judge).
- Reproducible from `work/multigrid.py` in one command.
