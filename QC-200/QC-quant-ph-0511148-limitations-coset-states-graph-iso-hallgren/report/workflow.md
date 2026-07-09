# Workflow, Tools, and Effort — quant-ph/0511148

## Narrative

1. **Fetch & read paper** (5 min).
   - `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0511148` — 270 KB, 24 pp.
   - `pdftotext paper.pdf work/paper.txt` — locate main theorem statement.
   - Identified **Theorem 12** as the one central, closed-form,
     computable inequality:
     `|| E_g sigma_{H^g}^{⊗t} - sigma_{{1}}^{⊗t} ||_tr < (2^t/|G|) sum_τ d_τ |χ_τ(h)|`.
   - Identified **Corollary 14** (`t = Ω(n log n)` for GI-relevant
     hidden subgroup in `S_n ≀ S_2`) as the scaling claim to test.

2. **Extract Marker/Nougat surrogates** (2 min).
   - Neither Marker nor Nougat is installed on CherryRd; used the QC-200
     convention (see sibling `QC-0704.3628-.../extraction/README.md`)
     of PyMuPDF (fitz) and `pdftotext -layout` as surrogates. Full paper
     body preserved in both files. `extraction/README.md` notes the
     substitution.

3. **Implement Murnaghan–Nakayama character algorithm** (30 min).
   - `report/evidence/coset_state_sim.py::_remove_border_strip` and
     `chi_lambda_on_mu` implement the standard border-strip recursion.
   - Sanity-checked against tabulated `S_2`, `S_3`, `S_4`, `S_5`
     character tables:
     - dim(S_4) = [1,3,2,3,1], sum = 24 = |S_4| ✓
     - χ(transposition, S_4) = [1,1,0,-1,-1] ✓
     - dim(S_5) = [1,4,5,6,5,4,1], sum^2 = 120 ✓
     - χ(transposition, S_5) = [1,2,1,0,-1,-2,-1] ✓

4. **Compute Theorem-12 RHS Δ_char(n,t)** (0.3 s).
   - Grid: n=2..8 × t=1..6 for S_n setting; n_graph=2..6 × t=1..8 for
     the GI setting G = S_{2n}, h = cycle type 2^n.
   - Output: `results.json`, `results_wreath_pgm.json`.

5. **Build density matrices ρ_H, ρ_{1} on ℂ[G] and their tensor powers**
   (30 s).
   - Regular representation dim = n!; feasible up to n=5 for t=1 (dim 120)
     and n=4 for t=2 (dim 576).
   - Compute conjugate-averaged mixed state
     `avg_a rho_{H^a} = (1/|G|) sum_a rho_{a H a^{-1}}` explicitly.
   - Compute `||·||_1` via Hermitian eigendecomposition
     (`numpy.linalg.eigvalsh`); numerically stable.

6. **Verify Theorem 12 inequality LHS ≤ RHS** (already in step 5 loop).
   - All 7 tested (n,t) pairs pass strictly. Ratio LHS/RHS in [0.16, 0.35].

7. **Extract scaling constant** (algebra, no run cost).
   - t*(n) := log₂(|G|/Σ d|χ|) fit vs n·log₂(n) → slope = 0.475,
     ratio flat at 0.47–0.51 across n_graph=2..6.

8. **Make figures + LaTeX report** (5 min).
   - `make_plots.py` produces 3 figures: Δ_char vs t, t* scaling, exact
     LHS-vs-RHS.
   - Wrote `REPORT.tex` (mirrors QC-200 sibling structure).

## Tools & versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.13.7 | driver |
| numpy | 2.4.3 | dense linalg (tensor powers, eigvalsh) |
| sympy | 1.14.0 | partition enumeration (only) |
| PyMuPDF (fitz) | 1.27.2.3 | marker.md surrogate |
| pdftotext (Poppler) | system | nougat.mmd surrogate + paper.txt |
| matplotlib | (system) | 3 figures |
| curl | system | fetch arXiv PDF |
| No LLM inference used | — | (Argo etc. not required for this replication) |

## Code inventory

- `report/evidence/coset_state_sim.py` — 460 LOC, main sim + character tables + tensor-power trace distance.
- `report/evidence/wreath_and_pgm.py` — 220 LOC, extends to GI wreath setting + Helstrom P_succ + n=5 exact.
- `report/evidence/make_plots.py` — 75 LOC, 3 figures.

## Effort estimate

| Task | Wall time |
|------|-----------|
| Read paper + locate testable claim | ~5 min |
| Implement Murnaghan-Nakayama + validate | ~30 min |
| Build density matrices + tensor powers + validate | ~20 min |
| Run character sweep n=2..8, t=1..8 | 0.3 s |
| Run exact trace distance n=2..5, t=1..2 | 30 s |
| Figures | <5 s |
| Write REPORT.tex + open_questions + workflow + failure + summary | ~30 min |
| **Total** | **~1.5 h agent wall clock, <1 min compute** |

- LOC written: ~760 (Python) + ~15,700 bytes LaTeX + ~4,200 bytes JSON.
- No external data ingested beyond the arXiv PDF (270 KB).
- Runs executed: 3 (`coset_state_sim.py`, `wreath_and_pgm.py`, `make_plots.py`), all under 30 s each.

## Reproducibility

Deterministic (no RNG anywhere). Given Python + numpy + sympy, `python3 coset_state_sim.py && python3 wreath_and_pgm.py && python3 make_plots.py` regenerates every JSON, PNG, and inequality check byte-for-byte.
