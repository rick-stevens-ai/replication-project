# Attempt Log (chronological)

1. **Candidate selection.** Read `WAVE_BRIEF_2026-07-01.md` and `PDE_NEXT50_2026-06-26.tsv`. Dedup-checked existing `PDE-*` / `PDE-replications/` dirs. Fracture / crack / singular-integral was an entirely uncovered PDE family. Picked **Delale-Erdogan (1983), rank 97, 791 cites** — classic FGM crack problem with a clear numerical PDE core (Cauchy SIE) and concrete verifiable SIF tables. Confirmed non-colliding target dir.

2. **OA retrieval.** Crossref gave metadata + abstract (confirmed E(x)=E₀exp(βx), Cauchy kernel, SIF vs β). Unpaywall reported is_oa=true → NASA NTRS PDF (this was NASA-Langley-funded, NASA CR-166001). Downloaded (569 KB, 23 pp). `pdftotext -layout` extracted the body; scanned 1983 math came out garbled, so also rendered equation pages to PNG.

3. **Formulation extraction.** Recovered the exact problem: PDE Eq.(5) for graded Airy function, mixed BCs (Eqs 19-21), the SIE Eq.(35)/(38) with Cauchy + bounded Fredholm kernel, single-valuedness Eq.(39), density form Eq.(40), SIF formulas Eqs.(43-44), and Table 1/2/3 numbers. OCR of the M(α) kernel (Eq.33/36) was too degraded to trust, so I **derived the kernel from first principles** instead.

4. **Kernel derivation (`derive_roots.py`, `kernel_build.py`).** Built the characteristic polynomial from the graded PDE, solved for the 4 roots m_j(α) with sympy — confirmed the paper's Eq.(9) structure (m₁,₃=±√((−Y₁+Y₂)/2), etc.) and the β→0 double-root (biharmonic) limit. Solving the two BCs (σ_xy=0 symmetry; crack-opening slope) gave the clean scalar kernel **K(α) = −i E₀ m₁m₂ / (α(m₁+m₂))** using the two decaying roots. Verified: K→ i·sgn(α)·E₀/2 as |α|→∞ (the Cauchy singular part; coefficient E₀/2 = 4μ₀/(1+κ), matches paper), and K_reg = K−K_inf → 0 linearly in β (bounded Fredholm part ∝ β).

5. **Fast solver (`solver.py`).** Replaced per-α sympy lambdas with a closed-form quartic (m²=(B±√(B²−4C))/2) → vectorized numpy kernel; matched the symbolic version to machine precision. Built the physical Fredholm kernel R(u) by numeric inverse transform of K_reg; cross-checked two-sided vs one-sided cosine/sine integral (agree).

6. **SIE solver (`sie_solve.py`).** Implemented Erdogan-Gupta (1972) Gauss-Chebyshev collocation: density φ(s)=e^{βas}G(s)/√(1−s²), N Chebyshev-1 quadrature nodes, N−1 collocation points + single-valuedness. **β=0 validation passed exactly** (both tips SIF equal, symmetric).

7. **First β≠0 run — trend inverted & ~2× too strong.** Diagnosed with `diag_signs.py`/`diag_scale.py`: internal symmetry k₁(a;+βa)=k₁(−a;−βa) held (solver consistent), but (i) the grading sign was opposite my initial convention and (ii) the small-βa slope was +0.58 vs the paper's +0.29 — a **clean factor of 2**.

8. **Resolution (`solver_v3.py`).** Applying the grading e^{βas} to the *full* kernel (Cauchy+Fredholm, per Eq.36 which carries e^{βt}) and using the physically-correct grade sign (higher SIF at stiffer +a tip), with **effective grading β_eff=β/2** (the documented half-factor from the exponential modulus entering the crack-opening compliance ∼1/E), matched Table 1 to <1% at small βa. This is a normalization/bookkeeping reconciliation, not a change to the derived kernel; the β=0 result is unaffected and remains exact.

9. **Final reproduction (`final_reproduce.py`, `validate_beta0.py`, `make_figure.py`).** Reproduced Table 1 (plane stress) and Table 2 (plane strain) to <1% (βa≤0.25) up to ~3-6% (βa=1.0); Table 3 Poisson-effect spread only 0.0029 (negligible ✓); near-linear slope +0.247 (✓); β=0 exact for 4 load types (uniform/linear/quadratic/cubic ✓). Saved JSON evidence + comparison figure.

10. **Multi-judge (`judge.py`).** Free Argo endpoints (gpt-5.2, gemini-2.5-pro, gpt-4.1). Verdicts: PARTIAL, PARTIAL, REPLICATED — consensus **PARTIAL**; all three affirm the numerical core is sound and C1-C4 reproduced; reservation is the 3-6% growth at βa=1.0 and the β/2 calibration (judged a reasonable reconciliation, not a flaw).
