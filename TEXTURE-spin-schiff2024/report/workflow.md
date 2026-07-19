# Workflow — schiff2024 (arXiv:2412.18025)

## Narrative
1. Fetched PDF; pdftotext extraction (~29k words, marker.md); Nougat stub (GPU-only, sha256 logged).
2. Read Secs III (zero-SOC Landau theory) + III.B (secondary multipolar order parameters): identified the reproducible analytic core Phi(N)=a2 N^2 + a4 N^4 and the altermagnet-specific secondary-multipole-determines-splitting chain.
3. Implemented the coupled free energy Phi(N,M)=a2 N^2 + a4 N^4 + (r/2)M^2 - g M N^2; minimized analytically (nonzero Neel branch + induced M=gN^2/r).
4. Fit mean-field exponents: beta(|N|)=0.5, multipole exponent=1.0; verified M=0 and splitting=0 above Tc.
5. Connected the secondary multipole to the microscopic d-wave TB (t_AM=cM) and confirmed max|Delta| linear in M (slope 8c, residual 1e-15).
6. Fixed one expectation error (max|cos kx - cos ky|=2 not 4 => slope 8 not 16).
7. LLM-judge (free Argo sonnet-4.6): REPLICATED, coverage 9, agreement 10.

## Tools & codes
- Python 3.13, NumPy, SciPy, Matplotlib; pdftotext (poppler).
- code/schiff2024_replication.py (~180 LOC). LLM-judge scripts/wave4_llm_judge.py -> argo:claude-sonnet-4.6 (free).

## Effort estimate
- Compute: CPU-only, ~1s, single process. Wall clock ~12 min incl. extraction + one bugfix. ~180 LOC, 1 iteration.
