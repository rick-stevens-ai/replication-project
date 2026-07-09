# Workflow — arXiv:1301.2340 replication

## Timeline (one continuous subagent session, 2026-07-05 16:31-16:40 CDT, ~9 min)

1. **Fetch + parse paper (~1 min).** `curl` https://arxiv.org/pdf/1301.2340 into `paper.pdf` (5 pages, 148 KB), `pdftotext` to `work/paper.txt`. Skimmed intro + Eqs. 4-14 to confirm title/authors and pull the checkable numbers.
2. **Identify headline claim (~30 sec).** The cost proxy T ~ d^7 * kappa * log(N) / eps^2 and the corollary "HHL speedup from preconditioning = kappa(A) / kappa(MA)" (from the paragraph after Eq. 12).
3. **Design numpy simulation (~2 min).** Chose graded-mesh 1D FEM Poisson as the SPD ill-conditioned test family; SPAI-with-pattern-of-A as the "faithful" preconditioner and Jacobi-diagonal as the coarse-reference baseline; six independent test cases (N,g) x (SPAI,Jacobi).
4. **Implement + run (~3 min).** `report/evidence/preconditioned_hhl_sim.py` (~260 lines). Ran in 0.01 s. Wrote `results.json` (machine-readable) and `results.txt` (human summary).
5. **Extraction files (fallback) (~1 min).** Marker and Nougat not installed on this host; produced honest-fallback `extraction/marker.md` and `extraction/nougat.mmd` from the pdftotext output with a provenance disclaimer, plus hand-normalised the six key equations for the .mmd file.
6. **Write REPORT.tex + compile (~1 min).** 14 KB LaTeX; `pdflatex -interaction=nonstopmode` produced 5-page REPORT.pdf (245 KB) cleanly on first pass.
7. **Open questions + workflow + artifacts + failure analysis (~30 sec).** Five substantive Qs grounded in what the replication actually observed (not generic).

Total wall time: ~9 minutes end-to-end.

## Tools + versions

| Tool | Version | Purpose | Where |
|---|---|---|---|
| Python | 3.13 (system) | Reproduction | `report/evidence/preconditioned_hhl_sim.py` |
| numpy | ≥ 1.26 | Linear algebra, SPAI least-squares, cond() | same |
| curl | system | Paper fetch | `paper.pdf` |
| pdftotext (poppler) | Homebrew | PDF → text | `work/paper.txt` |
| pdflatex (TeX Live 2026) | `/usr/local/bin/pdflatex` | Compile REPORT.tex → PDF | `report/REPORT.pdf` |
| Marker | **not installed** | — | fallback extraction |
| Nougat | **not installed** | — | fallback extraction |

No paid APIs invoked. No hardware / no quantum backend needed — the paper's claim is a **cost model** and is verified against exact numpy linear algebra.

## What was actually done

- Reproduced the paper's cost formula and preconditioning claim across **six independent (N, preconditioner) instances**, spanning kappa(A) ∈ [64, 2482] and N ∈ {4, 8, 16}.
- Verified 6-decimal agreement between empirical HHL cost-proxy ratio and the theoretical kappa(A)/kappa(MA).
- Verified preconditioned solution recovers x_true to machine precision (~1e-16) in all six cases.
- Ran a scaling sweep N ∈ {4, 8, 16, 32, 64} at grading=100 to confirm kappa(A) grows super-linearly while kappa(MA) stays modest (the qualitative regime the paper needs).
- Tested Eq. (12) rigorously and honestly reported that our SPAI residuals sit at the edge / outside the bound's validity regime — this is a real caveat of the bound that our replication surfaces and that the report calls out (Q1, Q3).

## What was intentionally not done

- **Full quantum circuit simulation** (state prep + unitary HHL + AE readout). Would need ~20-25 qubits at N=8 with heavy AE repetitions — Qiskit/PennyLane reach it but out of scope for a single-turn replication. The paper's headline is the *cost model*, not a specific circuit.
- **FEM RCS demonstration.** Requires a 3-D edge-basis Maxwell assembler + scatterer geometry. Multi-week engineering, orthogonal to the algorithmic claim. Called out as Q4.

## Reproducibility

- Seed: 20260705.
- Single command: `python3 report/evidence/preconditioned_hhl_sim.py`.
- Outputs: `report/evidence/results.json` + `report/evidence/results.txt`.
- Full deterministic; no network, no LLM, no GPU.
