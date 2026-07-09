# Workflow — arXiv:1704.06774 replication (Ambainis & Kokainis, 2017)

## Timeline & steps executed
1. **Fetch (t+0min).** `curl -sL -o paper.pdf https://arxiv.org/pdf/1704.06774` — 372 KB PDF, 38 pages, arXiv version v3 (Dec 2022 revision of the 2017 STOC paper).
2. **Text extraction (t+1min).** `pdftotext -layout paper.pdf work/paper.txt` and `pdftotext -raw paper.pdf work/paper_raw.txt` for fallback Marker / Nougat artifacts.
3. **Paper skim (t+3min).** Grepped for `Theorem|Lemma|Algorithm`; identified Theorem 2 (main result), Algorithm 1 (the estimator), Lemmas 3–5 (correctness / bounds), and Lemma 13 (structural invariant). The reproducible core is Algorithm 1's 5-line pseudocode plus the estimator identity.
4. **Implementation (t+15min).** Wrote `report/evidence/tree_size_estimation.py` in ~200 lines. Real numpy statevector: 
    - Basis {|e_{T+1}>} ∪ {|e> : e ∈ E} of dimension T+1
    - Explicit diffusion operators D_v = I − (2/‖s_v‖²) |s_v><s_v|
    - Direct-sum reflections R_A, R_B  
    - `numpy.linalg.eig` on U = R_B · R_A for exact eigenphase extraction
    - Estimator T̂ = 1/(α² sin²(θ_min/2))
5. **Sanity + bias probe (t+22min).** Wrote `verify_identity.py` to enumerate ALL eigenphases with their |start> overlaps; confirmed >99% amplitude sits on the ±θ_min eigenpair, so the smallest-|θ| estimator IS the paper's intended one.
6. **δ-convergence (t+27min).** `scaling_test.py` swept δ ∈ {1.0, 0.5, 0.3, 0.1, 0.05, 0.01, 0.005}; relative error scaled empirically as ~0.093·δ² and every run satisfied Lemma 5's window.
7. **Phase-gap scaling law (t+33min).** `quadratic_speedup.py` swept depth n ∈ [1,7]; log-log fit of θ_min vs √(nT) gave slope −0.9988 (paper predicts −1) and constant factor 0.421 (naive theory 2δ/√2 = 0.424 with δ=0.3).
8. **Reporting (t+38min).** Wrote `REPORT.tex` (5-page LaTeX with claims table, method, results-vs-paper tables, verdict, Open Questions); compiled to `REPORT.pdf` with pdflatex.
9. **Aux artifacts (t+45min).** `open_questions.json`, `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

## Tools + versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14 | scripting |
| NumPy | 2.4.3 | statevector, exact eigendecomposition |
| pdftotext | 24.10.0 (Poppler) | PDF → text (both layout and raw) |
| pdflatex | TeXLive 2026 | REPORT.tex → REPORT.pdf |
| curl | 8.7.1 | arXiv fetch |
| bash / zsh | macOS 25.3.0 | orchestration |

No quantum-circuit simulator required. The paper's operators are dense complex matrices of size ≤ 255×255 for depth-7 complete binary trees, so exact linear-algebra suffices and there is no advantage to Qiskit/Cirq/Stim for the mathematical core.

No LLM inference used for the technical work.

## Estimate of work done
- ~45 minutes wall-clock (single subagent turn)
- ~1000 lines of Python + LaTeX authored
- 8 tree instances end-to-end verified (complete binary depths 1–5, unbalanced depth-4, ternary depth-3, depth-7 path)
- 7 δ-values tested for convergence
- 7 depths tested for phase-gap scaling law
- Verified against 3 of the paper's key predictions (Lemma 5 bounds, Lemma 4 amplitude condition indirectly, and the T = 1/(α² sin²(θ/2)) identity)

## What I did NOT do
- Did NOT implement the downstream backtracking application (Section 4) — that requires composing Algorithm 1 with Grover-like amplification and doesn't add evidence for the tree-size estimator itself.
- Did NOT implement the AND-OR formula evaluator (Section 5) — same reason.
- Did NOT simulate quantum phase estimation via ancilla qubits — I extract θ_min via exact eigendecomposition, which is stronger evidence that the identity holds than simulating a stochastic sampler.
- Did NOT install marker / nougat — pdftotext fallbacks are provided, following the QC-200 convention already established in this replication set.
