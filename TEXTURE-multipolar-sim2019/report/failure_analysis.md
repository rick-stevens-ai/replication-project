# Failure analysis — Sim et al. 2019 (arXiv:1911.13224)

## Verdict: PARTIAL — Coverage 6/10, Agreement 6/10

## The single most important caveat (leads)
The paper's headline is a **sign-of-q2** statement: the time-reversal-breaking eg=(1,i)=
d_{x2-y2}+i d_{3z2-r2} is the weak-coupling ground state **iff the Ginzburg-Landau quartic
invariant q2 > 0**. Our from-scratch BdG **condensation-energy proxy at fixed gap magnitude gives
q2 < 0** (quartic coefficients: B_(1,i)=3.35e5 > B_real≈2.87e5 on the Fermi-surface shell), which
would select a *real* nodal eg state, **contradicting** the specific TR-breaking selection.

Why the proxy flips the sign — this is understood, not a coding bug:
- The TR-breaking (1,i) state fully gaps most of the Fermi surface but opens **16 Bogoliubov
  Fermi-surface pockets** (the paper's own topological signature). At **fixed** Delta those gapless
  pockets cost condensation energy relative to a real nodal state, so the naive energy comparison
  favors the real state.
- The correct discriminator is the **exact one-loop q2 coefficient computed with two-band
  *projected* gaps** at E_F (Boettcher–Herbut PRL 120,057002; Sim SI Sec. I), and/or a **fully
  self-consistent multi-gap** free energy where the TR-breaking state's larger self-consistent Delta
  can overcompensate the pocket cost. Neither was built under this budget.

## What DID reproduce (raises confidence the model is correct)
1. **eg-over-t2g irrep selection** — Part A pairing susceptibility gives lambda_eg=0.897 >
   lambda_t2g=0.798, exactly the paper's r_eg < r_t2g for |c_eg|>|c_t2g|. The Delta1/Delta2
   (cubic eg doublet) degeneracy is reproduced to machine precision.
2. **Strong-coupling trend** — whole-BZ integration favors a *real* TR-symmetric eg d-wave,
   consistent with the paper's weak→strong transition to real d_{3z2-r2} via band flattening.
3. **Structural checks** — Clifford algebra {gamma_i,gamma_j}=2 delta_ij passes; O20=3Jz^2-J^2
   matches the reused kernel's Stevens convention.

## Residual / scope not built (coverage-capping, expected)
- 16-pocket Bogoliubov Fermi surface + Chern ±2 (topological headline) — separate larger build.
- Full J_K<O20> vs g phase diagram (Fig.1), including the t2g dyz+idzx region.
- Microscopic projected Kondo coupling Eq.(7) derivation from SI form factors.
- Self-consistent nonlinear gap solve (used fixed-Delta condensation energy instead).

## Extraction tooling (degraded, NOT a physics gap)
`marker`/`nougat`/`pdflatex` are not installed. Text extraction fell back to `pdftotext`
(equations degraded). Equations are hand-transcribed authoritatively in REPORT.tex and
extraction/nougat.mmd. REPORT.tex ships as source (no pdflatex).

## What would raise the verdict to REPLICATED
Implement the one-loop q2 quartic-coefficient derivation with two-band projected gaps (or a
self-consistent multi-gap BdG free-energy minimization). If that yields q2>0 selecting (1,i),
Agreement would rise to ~9/10; adding the Chern-number computation would raise Coverage to ~8/10.
