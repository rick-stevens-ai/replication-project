# Failure Analysis — chen2023 (arXiv:2312.10473)

## What failed / friction
1. **Chern = 0 everywhere (fixed).** First model added the Haldane DMI term with a sign structure that
   did NOT open a topological gap (the sum sin(k.b1)+sin(k.b2)+sin(k.b3) gave the wrong valley parity),
   so every band was trivial. Fix: use the valley-odd combination sin(b1)-sin(b2)+sin(b3) so the DMI
   mass has opposite sign at K vs K' (genuine Haldane topological gap C=+/-1).
2. **kappa_xy exploded to ~1e+225 (fixed).** The hand-rolled dilogarithm power series for Li2(-rho)
   diverges for rho>1 (small energies), and the flux/dk^2 bookkeeping double-counted. Fix: use
   scipy.special.spence for a stable Li2, clip the Bose factor, and accumulate kappa directly from the
   plaquette flux F with the c2 weight (no dk^2 round-trip).
3. **m sweep too narrow (fixed).** Initial |m|<=1.2 never crossed the DMI gap (~3*sqrt3*D~2.08), so no
   transition appeared; widened to |m|<=4.
4. **LLM-judge endpoint.** opus-4.x aggregator parse error 2026-07-19; used free sonnet-4.6.

## Residual gaps (=> PARTIAL, reduced-model)
- **18-band TmX not built.** The paper's full Kitaev-Gamma triple-meron-crystal LSWT (18 sublattices,
  bosonic BdG) is out of scope; we use a 2-band reduction. The SUCCESSIVE multi-Chern transitions and
  their specific fields are therefore NOT reproduced (Open Q1-Q2).
- **C4 edge modes not computed** (Open Q4). Nonreciprocal magnons not addressed.
- **Kitaev-Gamma vs DMI source** not distinguished (Open Q3); we used a generic DMI mass.
- **Model-normalized units.**

## What's needed to close
Full 18-sublattice bosonic BdG LSWT vs field; per-band Chern over all gaps; kappa_xy(T,field) multi-
sign-change map; nanoribbon edge spectrum. See open_questions.json.

## Honesty note
Verdict PARTIAL is correct: the UNIVERSAL mechanism (topological magnon -> Chern transition -> thermal
Hall sign change) is reproduced with a proper Berry-curvature + magnon-THE calculation, but the paper's
specific 18-band TmX results (multi-transition sequence, edge modes) are reduced/out of scope.
