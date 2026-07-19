# Failure / Gap Analysis --- Urazhdin 2024 (arXiv:2408.08683v3)

**Verdict: REPLICATED** (Coverage ~6/10, Agreement ~9/10). This file records, honestly,
what reproduced, what did not, and whether each gap is a real shortfall or an
expected/scoped-out limit.

## Most important caveat first
This is a **minimal, deliberately incomplete model**, and the paper says so: its computed
moment is *smaller than* the experimentally observed MOKE signal, and the parameters
$a_t, a_l$ (hence the absolute moment) are called explicit **order-of-magnitude
semi-empirical estimates**. So the correct replication target is the paper's *internal*
physics --- the MO level structure, the gap, the Koster--Slater chain, the TDPT formulas,
and the atomic:inter-atomic ratio --- NOT the absolute experimental magnitude. Against that
target the agreement is excellent.

## What reproduced (high confidence)
- **MO level structure --- EXACT.** Numerically diagonalized 6-state spectrum
  $\{-1.60,-0.5415,-0.5415,1.60,4.80,4.80\}$ eV equals the analytic Eqs.(1)-(3) to machine
  precision ($\sim10^{-16}$). Nonbonding O states land exactly at $\pm2t_{OO}=\pm1.60$ eV;
  bonding/antibonding manifolds correctly doubly degenerate ($d_\pm$).
- **Bandgap --- EXACT.** $\Delta_{\text{diag}} = \Delta_{\text{analytic}} = 3.2000$ eV
  $=\Delta_{\text{paper}}=3.2$ eV (rel. err $1.4\times10^{-16}$). This is the paper's
  headline structural number.
- **Koster--Slater chain --- within ~2%.** $a_t=5.70$ (paper 5.7, exact), $a_l=19.95$
  (20.0, 0.25%), $a_+=12.83$ (13, 1.4%), $a_-=7.13$ (7, 1.8%). Residuals are the paper's
  own rounding of order-of-magnitude estimates.
- **Essential identity --- EXACT.** $a_+^2-a_-^2 = a_l a_t = 113.715$, the combination the
  paper stresses must be nonzero (requires unquenched orbital, $a_t\neq0$).
- **TDPT self-consistency --- EXACT.** Numeric 400k-point integration of Eq.(7) matches the
  closed-form Eq.(8) to ratio 0.99996.
- **Inter-atomic scale --- within 0.2%.** $\mu_1=1.597\,\mu_B$ (paper 1.6), confirming the
  inter-atomic contribution is comparable to ($\sim1.6\times$) the atomic one --- the paper's
  "remarkable" coincidence.

## Residual numerical gap (minor, expected)
- $Q_0$ for a $10^{-2}\,\mu_B$ moment: **0.090 nm vs paper 0.08 nm (12%)**. This is the one
  check above 10%. It is a downstream propagation of the same ~2% roundings in $a_\pm$ and of
  the paper's rounded $\hbar\omega/\Delta\approx0.004$; the physics (quadratic-in-$Q$,
  $1/\Delta^3$ scaling, unrealistically large required displacement) is fully reproduced.
  Not a disagreement.

## What was NOT computed (scoped out --- coverage-capping, not failures)
1. **No transport observable / no orbital Hall conductivity magnitude.** *The paper reports
   none.* This is a real-space single-Ti-plaquette MO model; it defines a transient orbital
   *moment* (in $\mu_B$), not a conductivity tensor. There is no $\sigma^{OH}$ number in the
   paper to match. (Pitfall 3 in the replication skill --- do not claim OHE reproduction from a
   local model --- is respected: we claim the MO moment, not a Hall transport coefficient.)
2. **No full k-dependent band structure.** The model is a local cluster, not a periodic TB
   band model; the paper computes no $E(\mathbf{k})$. Promoting it to a periodic multiband STO
   model + modern-theory orbital magnetization is a larger build (open question Q3).
3. **Inter-atomic Berry curvature $\Omega_{xy}$ invoked but not evaluated to a number** --- by
   the paper itself. We reproduced the perturbative circulating-current result (Eqs.15-18);
   the geometric Berry-curvature cross-check is open question Q1.
4. **Absolute experimental magnitude not matched --- by design.** The paper's own conclusion is
   that the modeled moment is smaller than experiment; matching it requires additional channels
   (plaquette currents, dxy/px/py orbitals) the minimal model omits (open question Q4).
5. **First-order TDPT only.** We reproduced the paper's leading-order result and its Eq.(9)
   residual estimate; a non-perturbative real-time propagation is open question Q2.

## Environment / tooling gaps (NOT physics)
- **marker / nougat not installed** --- artifacts 2-3 are honest `pdftotext` interims.
  `marker.md` = layout-mode prose; `nougat.mmd` = reading-order dump PLUS hand-transcribed
  LaTeX for every numbered equation (1)-(18). Math-token fidelity of the raw dump is degraded
  (a known pdftotext limit); the authoritative equations live in `nougat.mmd`'s transcription
  block and in `REPORT.tex`. Regenerate with `marker_single ...` / `nougat ...` once installed.
- **pdflatex not installed** --- `REPORT.tex` ships as source; compiles off-host. Not a
  package failure.

## What would raise the verdict / coverage
Closing Q1 (Berry-curvature cross-check of Eq.18) and Q3 (periodic multiband + modern-theory
orbital magnetization) would extend coverage from the MO spectrum toward a material-specific,
transport-comparable number and push coverage above 6/10. Agreement is already ~9/10 and is
limited only by the paper's own order-of-magnitude parameter estimates.
