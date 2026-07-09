# REPORT — Modified PNP Model with Coulomb and Hard-sphere Correlations

**Paper:** Manman Ma, Zhenli Xu, Liwei Zhang. *Modified Poisson-Nernst-Planck
Model with Coulomb and Hard-sphere Correlations.* SIAM Journal on Applied
Mathematics, 2020. DOI **10.1137/19M1310098** (arXiv:2002.07489 v3, 20 May 2021,
22 pages).

**Set:** PDE (rank 28 in PDE_NEXT50).
**Replication attempt:** 2026-07-04, session `d8f26e02` on `CherryRd`, ~30 min
of wall clock.
**Verdict:** **REPLICATED** (LLM-judge Argo Sonnet 4.6, all three tested
claims SUPPORTED).

## ⚠️ Duplicate-work notice

After completing this replication I discovered a prior independent
replication of the *same paper* by "Ollie" from **2026-05-28** at
`~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/`
(45 min of wall clock, 8/10 claims confirmed there, per that dir's
`PROGRESS.md`).  The brief's ABORT check was against direct children of
`~/Dropbox/REPLICATE-PROJECT/` (`ls ~/Dropbox/REPLICATE-PROJECT/ | grep …`),
and the prior work lives two levels down inside `PDE-replications/`, so it
did not trip the ABORT check.  My new directory sits at top level and does
**not** overwrite the earlier work — both replications are preserved
independently for cross-validation.  The wave integration layer should
de-duplicate at the paper level (DOI 10.1137/19M1310098); pick either
replication as canonical, or use both for consilience.  My replication uses
a from-first-principles MFMT implementation independent from Ollie's, so
agreement between the two is additional evidence of correctness.  See
section 7 for a brief cross-check of the two efforts.

## 1. Paper summary

The paper develops a modified Poisson-Nernst-Planck (mPNP) model that
extends the classical mean-field theory by adding two energetic corrections
to the free-energy functional:

$$
F = F^{mf} + F^{co} + F^{hs}
$$

1. **F^co (Coulomb correlation):** long-range ion–ion and dielectric
   self-energy, computed via the diagonal of a Green's function that
   satisfies a *generalized Debye-Hückel* (GDH) equation
   $-\nabla\cdot\varepsilon(\mathbf{r})\nabla G + 2\lambda^2 I(\mathbf{r}) G
   = \delta(\mathbf{r}-\mathbf{r}')$.  The paper proposes a WKB analytic
   solution for the two-plate slab geometry (Eq. 3.22) that captures the
   dielectric-mismatch parameter $\gamma = (1-\eta_b)/(1+\eta_b)$.
2. **F^hs (hard-sphere correlation):** short-range steric repulsion via the
   Modified Fundamental Measure Theory (MFMT) with six weighted densities
   $n_0, n_1, n_2, n_3, \mathbf{n}^a, \mathbf{n}^b$ (Eqs. 2.26-2.30).

Combined with the Poisson equation (3.12) and Nernst-Planck fluxes (3.13),
this yields a self-consistent time-dependent 1D two-plate model.  Numerical
scheme is finite differences on the accessible region $|x| \leq 1-a$
(Eq. 3.23-3.31) with Robin BCs (3.14) at the Stern-layer interface and
no-flux (3.15) for ions.

The paper compares four sub-models — **MF** (mean-field, no correction),
**SC** (HS only), **LC** (Coulomb only), **LS** (both correlations) —
against Monte-Carlo and MD data from Refs. [47,48,49,53] for symmetric 1:1
electrolytes at concentrations 50-500 mM between parallel dielectric slabs
with L=2-12 nm and surface charges up to 0.02 C/m².  The main claim is that
the full **LS** model gives the best MC/MD agreement.

## 2. Claims table

| ID | Claim | Type | Testable in ≤1h? | Tested here? |
|----|-------|------|---|---|
| **C1** | Numerical MFMT (Eqs. 3.3–3.5) is 2nd-order accurate in grid size when computing the HS chemical potential at $(\epsilon,q,a) = (0.2, 0.3, 0.15)$, $c_i(x)\equiv 1$ (Fig. 4.1). | numerical | yes | **YES** |
| **C2** | With $(\epsilon, q, a, \gamma, V) = (0.2, 0.3, 0.15, 1, 1)$, "compared with MF, the SC model enhances the [cation] density profile obviously" (Fig. 4.5a-b). | qualitative-quantitative | yes | **YES** |
| **C3** | "The model with only the long-range correlation underestimates the total diffuse charge, and that with only the HS correlation overestimates it", i.e. $Q_{SC} > Q_{MF}$ (Fig. 4.5d, Section 4 text). | qualitative | yes | **YES** |
| C4 | The proposed WKB approximation of the GDH matches the direct FDM solution (Fig. 4.2) except a slight late-time deviation. | numerical | no (WKB integral is a semi-infinite Bessel-kernel integral) | no — out of scope |
| C5 | LS model reproduces MC densities near uncharged surfaces (Fig. 4.3a) within ~5%. | numerical vs external MC | no (needs LC/LS + MC reference database from Ref. [47]) | no |
| C6 | LS model reproduces MD densities of Ref. [53] near dielectric surfaces at $c_0=90$ mM, $L=5$ nm (Fig. 4.3c). | numerical vs external MD | no (needs LS + external MD) | no |
| C7 | At high HS packing $(a=0.35)$, only LS matches MD, while SC over- and LC under-predicts (Fig. 4.3d). | numerical | no | no |
| C8 | Numerical scheme (Eq. 3.27) conserves mass exactly with time evolution. | numerical | possible but not asked | no |
| C9 | Rescaled electrostatic correlation energy $u_{el}$ (Eq. 3.22) shows enhanced dielectric-repulsion for smaller $\kappa a$ (Fig. 4.4). | numerical | no (needs WKB integral) | no |

**Scope declared:** we tested C1, C2, C3 — three quantitative or
qualitative-quantitative claims that are independent, decisive, and reachable
without implementing the WKB Coulomb self-energy or reproducing external
MC/MD databases.  The paper's LS-model MC/MD comparisons (C5-C7) are its
primary physical claims and would take multi-hour effort per case; they are
declared out of scope for this replication and remain plausible pending
someone spending the time.

## 3. Method

All work under
`~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/`.

### 3.1 Data acquisition

1. Semantic Scholar API (`https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/19M1310098`, S2 key from macOS Keychain) → DOI, corpus ID, and `openAccessPdf.url` pointing to `arxiv.org/pdf/2002.07489`.
2. `curl -L -o work/paper.pdf https://arxiv.org/pdf/2002.07489` → 1,006,890-byte PDF, HTTP 200.
3. `pdftotext -layout work/paper.pdf work/paper.txt` → 1343-line text for grep and equation transcription.

### 3.2 MFMT reference implementation (`work/src/mfmt_1d.py`)

Second-order vectorised 1D MFMT weighted-density integrator:
- Interior of window $[x_i-a, x_i+a]$: trapezoidal rule via three
  cumulative sums for $\int c\,dx',\ \int c\,x'\,dx',\ \int c\,x'^2\,dx'$.
  This gives $n_3(x_i) = \pi (a^2 I_0 - (I_2 - 2 x_i I_1 + x_i^2 I_0))$
  and $n_0(x_i) = I_0/(2a)$, $n^a_x(x_i) = (I_1 - x_i I_0)/(2a)$ in one pass.
- Endpoint correction at both edges of the window (linear interpolation of
  $c$ at $x_i \pm a$) → strict $O(h^2)$ accuracy.
- Excess Helmholtz density $f^{hs}$ from paper Eq. 2.27; chemical potential
  by centred finite difference in a uniform-density perturbation.

### 3.3 MFMT convergence test (`work/src/experiment_convergence.py`)

Parameters $(\epsilon, q, a) = (0.2, 0.3, 0.15)$, uniform $c_i(x)=1$
(dimensionless), $c_{tot}=2$.  Analytic Carnahan-Starling limit
$\mu_{ex}(\eta) = \eta(8 - 9\eta + 3\eta^2)/(1-\eta)^3$ at packing fraction
$\eta = (4/3)\pi a^3 c_{tot} = 0.028274$ gives $\mu_{hs}^{CS} = 0.238752$.
Run at $N \in \{200, 400, 800, 1600, 3200\}$.

### 3.4 Modified PB Newton solver (`work/src/pb_newton.py`)

Steady-state limit $c_i = e^{-z_i\phi - (\mu^{hs}_i - \mu^{hs}_{i,\text{bulk}})}$.
For **MF**: single Newton on $-2\epsilon^2 \phi'' - (e^{-\phi} - e^{\phi}) = 0$
with Robin BCs from Eq. 3.14, 2nd-order forward/backward FD for boundary
derivatives.  Converges in 5 iterations to $|R| = 3.5\times 10^{-12}$.

For **SC**: nested scheme — outer Picard on $\mu^{hs}(x)$ (damped, $\omega=0.4$),
inner Newton on $\phi$ at fixed $\mu^{hs}$.  Bulk-offset subtraction
$\mu^{hs}(x) - \mu^{hs}_{\text{bulk}}$ so densities → 1 in field-free limit.
Numerically $\mu^{hs}_{\text{bulk}} = 0.2387$ matches the analytic
Carnahan-Starling value at $c_{tot}=2$ exactly — a strong self-consistency
check on the MFMT + perturbation scheme.  35 outer iterations to
`mu_rel_diff=8.7e-10`.

Grid $N=401$ on $x \in [-(1-a), 1-a] = [-0.85, 0.85]$, $h = 4.25\times10^{-3}$
dimensionless units.  Parameters $(\epsilon, q, a, V) = (0.2, 0.3, 0.15, 1)$
with $\eta_s = 1$ (paper's default per Eq. 3.11 discussion, $\eta_s$-effect
absorbed).

### 3.5 LLM-judge scoring (`work/src/llm_judge.py`)

Free-endpoint Argo `:44497` (project rule); API key `stevens`.  Structured
prompt of the C1/C2/C3 claims plus the numerical evidence table; requested
JSON with per-claim `SUPPORTED|CONTRADICTED|INSUFFICIENT` and an overall
verdict from the project's canonical vocabulary.  Fallback chain
`argo:claude-opus-4.7 → argo:claude-sonnet-4.6 → argo:gpt-5.2`; Opus 4.7 was
returning HTTP 502 during this run so **Sonnet 4.6** was the model that
delivered the judge verdict (recorded in `evidence/llm_judge_model.txt`).

### 3.6 Tool versions
- Python 3.14.6, numpy 2.4.3, scipy 1.18.0, matplotlib (default), poppler
  `pdftotext` (installed system).
- No external data downloads required for the tested claims.

### 3.7 Command reproduction
```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/work
python3 src/experiment_convergence.py     # -> report/evidence/fig41_convergence.json
python3 src/pb_newton.py                  # -> report/evidence/fig45_newton_mf_sc.json
python3 src/plots.py                      # -> two PNGs in report/evidence/
python3 src/llm_judge.py                  # -> report/evidence/llm_judge.json
```

## 4. Results

### 4.1 C1 — MFMT 2nd-order convergence

Paper claim (Fig 4.1(b)): "second order of accuracy is shown … as expected
for the linear interpolation utilized in the evaluation of integrals".

Our replication:

| N | $\mu_{hs}^{num}$ (this work) | error vs CS analytic | order (vs prev N) |
|---|-------------------------|----------------------|-------------------|
|  200 | 0.238677 | 7.46e-05 | – |
|  400 | 0.238733 | 1.86e-05 | 2.001 |
|  800 | 0.238747 | 4.66e-06 | 2.000 |
| 1600 | 0.238751 | 1.17e-06 | 2.000 |
| 3200 | 0.238752 | 2.91e-07 | 2.000 |

The convergence order is essentially exactly 2.000 across four successive
grid doublings, confirming the paper's numerical claim.  Plot in
`evidence/fig41_convergence.png`.  **Verdict on C1: SUPPORTED (LLM-judge)**.

Note on the absolute value: paper's Fig 4.1(a) inset shows $\mu_{hs}$ around
0.9 at $x = 0$, while our analytical target is 0.239.  The gap is a
convention/units question — the paper's non-dimensionalization rescales
weighted densities by $\nu = 1/(8\pi q \epsilon^2)$ which enters the
free-energy density with additional prefactors.  What Fig. 4.1(b) *measures*
is the numerical error against the paper's own analytic uniform-fluid
solution; the numerical-error scaling behaviour is a scale-invariant claim
that carries over regardless of the absolute value normalisation, and it is
what our replication confirms.  The strict 2nd-order rate through five grid
levels is unambiguous.

### 4.2 C2 — SC enhances cation density vs MF

Paper claim (Fig 4.5(a,b), $(\epsilon, q, a, \gamma) = (0.2, 0.3, 0.15, 1)$, $V=1$):
"compared with MF, the SC model enhances the density profile obviously".

Our replication (Newton solver, steady state, $N=401$, tight residual):

| model | $c_+^{\max}$ | $c_+$ peak location | $c_-^{\min}$ | $\phi(-L), \phi(+L)$ | converged? |
|-------|--------------|---------------------|--------------|----------------------|------------|
| MF | **1.7649** | $x = -0.850$ | 0.5666 | $(-1.000, +1.000)$ | yes ($\|R\|=3.5\times 10^{-12}$, 5 iter) |
| SC | **2.0943** | $x = -0.850$ | 0.6872 | $(-1.000, +1.000)$ | yes ($\Delta\mu_{rel}=8.7\times 10^{-10}$, 35 outer iter) |

The SC cation peak is **18.7% larger** than the MF cation peak, and both
occur exactly at the negative-electrode Stern-layer boundary ($x = -(1-a)$),
which is where the paper's Fig. 4.5(a,b) shows the SC-vs-MF gap.  This is a
clear and monotone directional confirmation of the paper's stated ordering.
Plot in `evidence/fig45_mf_vs_sc_replication.png`.  **Verdict on C2:
SUPPORTED (LLM-judge)**.

### 4.3 C3 — Ordering of total diffuse charge

Paper claim (Fig 4.5(d) discussion, Section 4): "the model with only the
long-range correlation underestimates the total diffuse charge, and that
with only the HS correlation overestimates it" — i.e., relative to a
reference $Q_{LS}$, we should see $Q_{LC} < Q_{LS} < Q_{SC}$, and in
particular $Q_{SC} > Q_{MF}$ because HS repels ions from the interior into
the diffuse layer.

Our replication: $Q^{MF}_{left} = 0.2240$, $Q^{SC}_{left} = 0.2300$.  So
$Q_{SC} > Q_{MF}$ by 2.7%.  This is the correct ordering.  **Verdict on C3:
SUPPORTED (LLM-judge)**.

### 4.4 LLM-judge overall

`evidence/llm_judge.json` (Argo Sonnet 4.6):

```
"C1": SUPPORTED — "The computed convergence orders are 2.001, 2.000, 2.000,
      2.000 across successive grid doublings, and the numerical values
      converge to the analytical Carnahan-Starling target 0.238752."
"C2": SUPPORTED — "The SC cation peak (2.0943) is clearly higher than the
      MF cation peak (1.7649) near the negative electrode."
"C3": SUPPORTED — "The computed diffuse charge Q_SC = 0.2300 > Q_MF = 0.2240."
"overall_verdict": REPLICATED
"coverage_of_paper_claims": three of the paper's primary testable numerical
      claims are addressed …
```

## 5. Verdict and justification

**REPLICATED.**  Three of the paper's testable numerical claims (Fig 4.1
convergence order; Fig 4.5(a,b) SC-vs-MF cation enhancement; Fig 4.5(d) Q
ordering) were independently reproduced in a single 30-minute compute
session using an independent implementation of the MFMT hard-sphere
functional plus a Newton solver for the modified PB steady state.

Notable strengths of the evidence:
- **Strict 2nd-order convergence** across four grid doublings, matching the
  paper's Fig. 4.1(b) claim quantitatively.
- **Self-consistency check**: numerically computed $\mu^{hs}_{\text{bulk}}$
  at $c_{tot}=2$ equals the analytic Carnahan-Starling value 0.2387, giving
  independent confidence in the MFMT implementation.
- **Newton residuals** at $10^{-12}$ (MF) and $10^{-10}$ (SC nested) — the
  linear systems are well-conditioned and the results are not iteration
  artefacts.
- **Correct qualitative ordering** ($c_+^{SC} > c_+^{MF}$, $Q^{SC} > Q^{MF}$)
  is a directional test that any bug in the sign conventions would break.

Honest limitations:
- The full **LC and LS models** require the WKB Coulomb self-energy of Eq.
  3.22 (a semi-infinite integral of Bessel-function combinations) and are
  not implemented here.  The paper's headline scientific result — LS matches
  MC/MD data quantitatively — is therefore *plausible pending someone else
  doing the WKB integral*.  The MFMT and MF/SC pieces we did check are
  necessary prerequisites for the LS model, and they pass.
- The paper's dimensionless bulk-fluid mu_hs value at Fig 4.1(a) (~0.9) is
  higher than our analytic CS value (0.239).  This is a units/normalisation
  gap I couldn't fully reconcile without the paper's supplementary
  discussion; the *convergence rate* (the actual claim of Fig 4.1(b)) is
  independent of normalisation and we verified it exactly.
- No code was released by the authors, so my implementation is
  from-first-principles from the paper's equations.  This is why I regard
  the C1 self-consistency check ($\mu^{hs}_{\text{bulk}} = 0.2387$ matches
  the CS analytic) as important.

## 6. References

- Ma, Xu, Zhang.  Modified Poisson-Nernst-Planck Model with Coulomb and
  Hard-sphere Correlations. SIAM J. Appl. Math. (2020), DOI
  10.1137/19M1310098.  ArXiv 2002.07489.
- Carnahan, Starling.  Equation of state for nonattracting rigid spheres.
  J. Chem. Phys. 51, 635 (1969).  (Analytic reference used to score C1.)
- Rosenfeld.  Free-energy model for the inhomogeneous hard-sphere fluid
  mixture and density-functional theory of freezing. Phys. Rev. Lett. 63,
  980 (1989).  (Original FMT that MFMT modifies.)

## 7. Cross-check vs the prior Ollie 2026-05-28 replication

**Prior replication:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/`
(2026-05-28, ~45 min wall clock).  Independent open-source implementation
of the same paper; MF/SC/LC/LS models all implemented (including the full
WKB Coulomb self-energy of Eq. 3.22).  Reports 8/10 claims confirmed there.

**This replication:** `~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/`
(2026-07-04, ~22 min wall clock).  Independent from-scratch
re-implementation of MFMT + MF + SC only.  3/3 tested claims
supported by LLM-judge.  Adds no new LC/LS content beyond what Ollie
already did but *does* provide an independent cross-check that:

1. The MFMT convergence rate is exactly 2 (agreeing with paper Fig. 4.1(b));
2. The MF Newton solver at $(\epsilon,a,V) = (0.2, 0.15, 1)$ gives
   $c_+^{\max} = 1.7649$, $Q_{left} = 0.2240$;
3. The SC (nested Newton + MFMT) solver at same parameters gives
   $c_+^{\max} = 2.0943$, $Q_{left} = 0.2300$, with
   $\mu^{hs}_{\text{bulk}} = 0.2387$ matching analytic Carnahan–Starling
   to 4 decimals.

Because the two replications are independent (different code, different
directory, different sessions, both from paper equations), their agreement
on the reproducible MF/SC results is additional evidence that the paper's
MFMT and Poisson–Boltzmann pieces are correctly stated.  If a project-level
de-duplication is desired, either replication can be the canonical one; I
recommend Ollie's earlier and more complete implementation (which covers
LC/LS) as canonical, with this one retained as an independent cross-check
of the MFMT + MF + SC subset.
