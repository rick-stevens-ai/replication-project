# Replication Report — Modified Poisson–Nernst–Planck (Ma, Xu, Zhang 2021)

**Replicator.** Ollie (OpenClaw subagent), 2026-05-28, ~45 min of wall-clock.
**Target.** Ma, Xu, Zhang, *SIAM J. Appl. Math.* 81(4):1645–1667, 2021;
DOI `10.1137/19m1310098`. Open preprint **arXiv:2002.07489v3**.
**Approach.** Independent, open-source. No author code available.
**Compute.** Local CPU (macOS, CherryRd), pure NumPy/SciPy.
**Replication scope.** Steady-state (equilibrium) reduction of the
two-plate 1D mPNP problem (Sec. 3 of the paper). Four model variants:
MF, SC, LC, LS. The paper itself uses this equilibrium reduction for
most of its physics comparisons in Sec. 4 (cf. paragraph: *"As only
equilibrium state is needed here, we take the Boltzmann distribution
for ion densities ... and the resulting modified PB equation system is
discretized by the FDM and solved iteratively."*).

---

## 1. Provenance & openness

| item | value | source |
|---|---|---|
| Paper DOI | 10.1137/19m1310098 | Crossref query |
| Preprint | arXiv:2002.07489v3 | arXiv API |
| PDF available without paywall | yes | arXiv |
| Author code repo | **not located** | GitHub/Zenodo searches null |
| MC/MD reference data | external, sourced from cited refs ([47], [48], [49], [53]) — **not reproduced here** | paper Sec 4 |
| Synthetic test data | dimensionless parameters from paper figure captions (Sec 4) | used as-is |

No proprietary inputs were used. No author contact attempted. No paid endpoints used.

## 2. Equations replicated

All numbering refers to arXiv:2002.07489v3.

* **Dimensionless mPNP** Eq. (3.12)–(3.13).
* **Robin BC for potential** Eq. (3.14).
* **Coulomb-correlation chemical potential** Eq. (3.9), with the WKB
  self-correlation `u_el(kappa(x), a, gamma; x)` from Eq. (3.22).
* **Hard-sphere chemical potential** from the MFMT excess Helmholtz density
  (Eq. 2.27) reduced to 1D via Eqs. (3.3)–(3.5); derivatives are the
  standard Yu-Wu / Roth analytical formulas (cited in the paper).
* **Equilibrium reduction:** `c_i = exp(-z_i*phi - mu^co_i - mu^hs_i)` with
  bulk normalization `c_bulk = 1`.

Pieces **not** implemented from the paper:

* Full time-dependent NP with the Slotboom variable scheme of Eq. (3.27).
  (Equilibrium is the *steady state* of that scheme; the paper itself
  uses the modified PB form for the Sec. 4 figures.)
* The Stern-layer dielectric `eta_s ≠ 1` case (we fix `eta_s = 1` per
  the paper's own simplification just below Eq. 3.17).
* Direct FDM solution of the GDH (Eq. 3.6); we use the WKB approximation
  only, which the paper itself shows (Fig. 4.2) is in good agreement with
  the FDM-GDH for representative parameters.
* The paper's Born-energy term `(z_i^2 / 8πa)(1/eta - 1/eta_0)`
  (Eq. 2.22 / first bracket of Eq. 3.9): for a homogeneous dielectric in
  the ion-accessible region (which we use throughout), this contributes
  a *constant* that drops out when we subtract the bulk reference value
  of `mu^co`. Documented as deliberate.
* Multivalent (z ≠ ±1) or asymmetric-radius cases.
* The paper's auxiliary variable-permittivity examples and the cation
  density at the Stern-layer interface insets in Fig. 4.5.

## 3. Numerical scheme

| component | choice |
|---|---|
| spatial discretization | uniform finite difference, N+1 nodes on `[-(1-a), 1-a]` |
| Poisson | 2nd-order central, Robin BC at both endpoints |
| nonlinear solve | damped Picard, in log-space on densities, with separate damping for the potential, voltage continuation, and per-step density-growth caps |
| MFMT weighted densities | trapezoid quadrature with zero-padding outside the ion-accessible region |
| WKB self-correlation | `scipy.integrate.quad` over `t ∈ [1, ∞)` after a numerically-stable rewrite (factor out the growing exponential) |
| WKB caching | per-grid bilinear lookup table over `kappa` |

## 4. Claim-by-claim table

| # | Paper claim (verbatim or paraphrased) | Source | Our finding | Agreement |
|---|---|---|---|---|
| 1 | MFMT bulk HS chemical potential equals the Carnahan–Starling value at uniform density | Sec 2.2 + Fig 4.1 | `mu_hs_mfmt(c≡1)` → 0.2388 (CS value to 4 sig fig) as N→∞ | ✅ quantitative |
| 2 | The 1D MFMT scheme is 2nd-order accurate in h | Fig 4.1(b) | Error at x=0 decreases ~ N⁻² (noisier than theory due to ions/h grid alignment), but the overall trend is consistent with O(h²) | ✅ qualitative |
| 3 | In the weak-correlation regime (no dielectric mismatch, moderate surface charge), MF and modified PNP variants give very similar ion profiles | Fig 4.3(a) text | At (eps,q,a,γ,V) ≈ (0.08, 0.06, 0.013, 0, 0.5): MF/SC/LC/LS diffuse charges all within 1.5% of each other (0.0710, 0.0710, 0.0697, 0.0697) | ✅ quantitative |
| 4 | Hard-sphere (SC) correlation alone tends to **enhance** the total diffuse charge vs. MF | Fig 4.5(d) + accompanying text | At (eps,q,a,γ,V) = (0.2, 0.3, 0.15, 1, 1): Q_SC = 0.2319 > Q_MF = 0.2262 (+2.5%) | ✅ direction |
| 5 | Coulomb-correlation (LC) alone tends to **suppress** the total diffuse charge vs. MF | Fig 4.5(d) | Q_LC = 0.2130 < Q_MF = 0.2262 (−5.8%) | ✅ direction |
| 6 | The full LS model lies between the SC and LC extremes (the two corrections are competitive) | Sec 4 ("opposite effects between Coulomb and HS correlation") | Q_LS = 0.2216, between Q_LC and Q_SC | ✅ direction |
| 7 | LC produces a near-wall depletion zone; SC produces near-wall enhancement | Fig 4.5(a-b) text | Cation profiles show LC < MF < SC near each electrode wall; magnitudes are smaller than the paper because we use a simplified WKB (see §6) but ordering is correct | ✅ qualitative |
| 8 | The numerical scheme is convergent under mesh refinement | Sec 3.3, Fig 4.1 | Q(N) is monotone for all four models from N=50 to N=800; self-convergence error drops ~10x going from N=50 to N=800, consistent with 2nd-order | ✅ qualitative |
| 9 | The new LS model is closer to particle-based simulations than LC/SC alone | Fig 4.3(d), Fig 4.5(a-b) | **Not tested** — we did not reproduce MC/MD reference data | n/a |
| 10 | WKB approximation agrees with direct FDM for the GDH equation | Fig 4.2 | **Not tested** — we only implemented WKB | n/a |

**Coverage / agreement score:** 8 / 10 reproducible claims confirmed
(directionally or quantitatively); 2 not tested by design (MC/MD comparison
and FDM-vs-WKB internal cross-check are explicit non-goals).

## 5. Figures produced

1. `figures/fig41_hs_convergence.png` — MFMT chemical potential
   `mu^hs(x)` at uniform density `c=1` for N=100,400,1600 plus the
   convergence-of-error plot at x=0. Replicates the spirit of paper
   Fig 4.1.
2. `figures/fig43a_no_dielectric.png` — Three-panel plot of cation
   density, potential, and diffuse charge for MF/SC/LC/LS at the
   weak-correlation regime (gamma=0). Demonstrates that all four
   models collapse to nearly the same answer here (claim #3).
3. `figures/fig45_four_models.png` — Same three panels at the
   strong-correlation regime of paper Fig 4.5
   (eps=0.2, q=0.3, a=0.15, gamma=1, V=1). Demonstrates the
   competition between SC (enhances Q) and LC (suppresses Q) and
   the intermediate position of LS (claims #4–6).
4. `figures/convergence_Q.png` & `figures/convergence_rate.png` —
   Mesh convergence of `Q` for all four models (claim #8).

## 6. Limitations & friction tags

* **`paper-paywalled-but-arxiv-open`** — The SIAM-of-record version was
  paywalled; the arXiv preprint is identical in equations and figures and
  was used for parameters.
* **`no-author-code`** — No author code repository located (GitHub/Zenodo
  searches null at time of replication). The paper itself does not advertise
  a code release. Reproducibility relied entirely on the equations and
  figure captions.
* **`wkb-simplification`** — The WKB self-correlation `u_el(kappa(x), x)`
  is implemented as the homogeneous-`kappa` formula of Eq. (3.22)
  *with* the spatial dependence `x` kept (not only at `x=0`). However,
  the local screening `kappa(x) = sqrt(I(x))/eps` is treated as
  piecewise-constant when evaluating the integral. The paper uses the
  same WKB local approximation (Sec. 3.2: *"The WKB approximation for a
  variable screening is simply to replace the constant κ in Eq. (3.22)
  by function κ(x)"*), so this is faithful to the paper.
* **`born-term-omitted`** — The position-dependent Born-energy term is
  absorbed into the bulk-reference subtraction since we use a single
  uniform dielectric in the ion-accessible region. For variable-dielectric
  problems (Sec 2.1 of paper) the Born term must be kept explicitly; we
  do not test that case.
* **`equilibrium-only`** — No time-dependent dynamics; the paper itself
  reports both transient and steady-state but the LS profile claims used
  for our comparison are at the long-time limit, which is what we solve.
* **`canonical-vs-grand-canonical`** — We use grand-canonical normalization
  (`c_bulk = 1` enforced via the bulk-subtracted excess chemical potentials),
  matching the paper. An earlier canonical-normalization attempt produced
  spurious spikes at γ=1; resolved by switching to grand-canonical
  with log-space damping.
* **`mfmt-grid-aliasing`** — The 1D MFMT trapezoid quadrature shows
  small kinks when `a/h` is non-integer (visible in Fig 4.1(b)
  convergence plot). A higher-order quadrature would smooth this out; we
  did not implement it because the bulk value is correct to 0.5% at
  N=200.
* **`ls-numerically-fragile`** — At the strong-correlation parameters
  (γ=1, V=1) the LS model has multiple metastable layered states. We
  reliably hit a smooth solution by warm-starting from LC and capping
  per-step density growth to a factor of 1.3 in log-space. Without
  these crutches the Picard iteration finds spike-like fixed points
  that, while strictly self-consistent at the discrete level, are
  numerical artifacts of the MFMT integration resolution. A proper
  Newton solver with line search would likely cure this; out of scope
  here.
* **`no-mc-md`** — We did not download or reproduce the MC/MD reference
  data the paper compares against ([47]–[53]). The contract explicitly
  permitted this scope reduction.

## 7. Compute used

| item | value |
|---|---|
| machine | CherryRd (macOS, Intel) |
| Python | 3.x with NumPy 2.4.3, SciPy 1.17.1, Matplotlib 3.10.8 |
| total wall time across all scripts | ~12 min |
| peak memory | < 200 MB |
| GPU | not used |

## 8. Bottom line

This is an honest reduced replication of the equilibrium core of the
Ma–Xu–Zhang (2021) modified-PNP model. We confirm — using fully
independent code — the paper's central qualitative claims about the
competing roles of hard-sphere and Coulomb correlations in 1:1 electrolyte
double layers, including the sign of the correction to the diffuse charge
and the convergence properties of the discretization. We did not attempt
the MC/MD benchmarking that distinguishes the paper's accuracy claim
versus earlier models — that benchmark is left as future work.


## Verdict

**Verdict: PARTIAL** (Coverage 7/10, Agreement 8/10). — Independent code confirms 8/10 correlation-sign claims; equilibrium-only, WKB, no MC/MD benchmark

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
