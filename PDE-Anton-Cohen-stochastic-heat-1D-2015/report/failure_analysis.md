# Failure Analysis — Anton–Cohen–Quer-Sardanyons (2017/2020) SEXP Replication

A record of the significant *failures*, *near-misses*, and *ambiguities* encountered during
this replication, together with root cause, resolution, and lesson learned. The verdict
remains **REPLICATED**, but every replication has warts and this document is the honest log.

---

## F1 — Literal-symbol reading of Eq. (15) blew up the explicit scheme (Δt > 2⁻¹⁰)

### What happened
The paper writes $\Sigma(U) = \operatorname{diag}(\sqrt{M}\,\sigma(U_m))$ and
$\Delta W^n = W^M(t_{n+1}) - W^M(t_n)$, and defines
$W^M := \sqrt{M}\,(W(t,x_{m+1}) - W(t,x_m)) \sim \mathcal{N}(0, \Delta t)$. Taken literally,
this applies the $\sqrt{M}$ factor **twice**, giving per-node noise amplitude
$\sqrt{M}\sigma\sqrt{\Delta t}$.

At $M=512$ this amplifies the noise by a factor $M$. On the first stability sweep the
explicit SEXP scheme produced $\max|u| \sim 10^6$–$10^{13}$ for
$\Delta t > 2^{-10}$ — directly contradicting the paper's headline "no CFL-type restriction"
and its Fig-1 x-axis range ($10^{-5}$–$10^{0}$) where the error is $\le 0.1$.

### Root cause
Presentation ambiguity in the paper: the definition of $\Delta W^n$ as a *lattice-node*
increment (variance $\Delta t$) is incompatible with the $\Sigma = \sqrt{M}\sigma$ factor
that the same scheme requires. The consistent reading is that $\Delta W^n$ is the
space-time white-noise **cell** increment
$\sim \mathcal{N}(0, \Delta t \cdot \Delta x) = \mathcal{N}(0, \Delta t/M)$, so the net
per-node noise is $\sqrt{M}\sigma\sqrt{\Delta t/M}\,\xi = \sigma(u_m)\sqrt{\Delta t}\,\xi$
— the standard, physically-correct FD discretization of white noise.

### Resolution
- Switched to the cell-increment reading in `work/sexp_heat.py`. Scheme is now CFL-free
  (C1 recovered) and reproduces the Fig-1 order-$1/2$ behavior (C2).
- Documented the ambiguity and the reconciliation in `REPORT.md §5`.
- Submitted the reconciliation to three independent free-endpoint judges — all three
  accepted it as "the obvious reading" / "not a concern" / "reproducibility defect of the
  paper's presentation, not the method."

### Lesson learned
When an SPDE paper prescribes a discrete noise term, always check dimensional / variance
consistency with the noise it claims to be discretizing (here, space-time white noise on a
$\Delta x$-cell). Mismatch by a factor of $\sqrt{M}$ or $\sqrt{\Delta x}$ is one of the most
common bugs in the SPDE-numerics literature, and it will not surface until the sweep hits a
regime where the scheme is nominally supposed to be stable.

### Residual open question
See `open_questions.json` **Q3**: which reading did the authors' own implementation use?
The paper text does not unambiguously pin it down. This is a defect in the paper's
presentation, not in the scheme.

---

## F2 — Near-miss: implicit trust in Eq. (15) was avoided by validation-first discipline

### What happened
The natural mistake would have been to code Eq. (15) verbatim, launch the 96-worker Monte
Carlo, and only notice the blowup in the aggregated JSON output — wasting significant
`uicgpu` time.

### Root cause
The paper's own headline claim (CFL-freeness) is subtle enough that a small
noise-amplitude bug does not fire on visual inspection of one path — it looks noisy, then
diverges.

### Resolution
Deterministic validation was run FIRST (`work/validate_deterministic.py`), before any
stochastic experiment:

1. DST-diagonalization vs. dense `expm`: 3.3e-16 at $M=16$.
2. Linear-part time-exactness: 5.5e-15 across $\Delta t = 2^{-4}$ vs. $2^{-10}$.
3. Analytic-solution agreement: 1.7e-16.
4. FD spatial rate: 2.000 across $M = 32, 64, 128, 256, 512, 1024$.

Only after all four passed did we run the CFL sweep, and the CFL sweep is what caught F1.
Total wasted compute: 1 short local run, seconds of wall time.

### Lesson learned
**Deterministic validation before stochastic experiments.** This is a hard rule and it paid
off on this project. In SPDE numerics, the linear-part reproducibility is usually
machine-precision achievable, and any deviation from that is a bug worth chasing before
touching the noise term.

---

## F3 — The strong-order slope 0.558 vs. paper's 1/2 was not statistically tested

### What happened
The measured RMS strong-order slope is 0.558 across 8 successive Δt refinements. The paper
states 1/2. The 0.058 excess is small enough that all three judges accepted it as "clean
1/2 behavior," and the report does likewise, but we did not compute a bootstrap CI on the
slope.

### Root cause
Time budget + the qualitative fit is visually clean (RMS approximately halves per Δt
halving over 8 points). The point of the exercise was to check the paper's order, not to
push for tight CI-based statistical testing.

### Resolution
- Report says "measured RMS order 0.558 (paper: 1/2)" — no over-claim.
- `REPORT.tex` **GENUINE CRITIQUE** §5 explicitly names this as a caveat: 500-sample
  point estimate, no bootstrap, coarsest Δt is the noisiest estimator.
- Follow-up plan: `open_questions.json` **Q1**.

### Lesson learned
For strong-order estimation, always report slope $\pm$ 95% bootstrap CI. A single-number
slope invites over-interpretation in either direction (either "matches theory exactly" or
"suspiciously off"). This is a soft rule adopted for future PDE-100 SPDE replications.

---

## F4 — Only one test problem was probed

### What happened
Both the paper's Fig. 1 and our C2 use exactly one triple
$(u_0, f, \sigma) = (\sin(\pi x),\, u/2,\, 1-u)$. Robustness of the observed 1/2 rate to
nonlinear or nearly-non-Lipschitz $\sigma$ was not tested.

### Root cause
Fig. 1 in the paper uses this triple, and the goal of the replication was to reproduce Fig. 1.

### Resolution
- `REPORT.tex` **GENUINE CRITIQUE** §3 flags this explicitly.
- Follow-up in `open_questions.json` **Q5** (non-Lipschitz regime, Thm 3.1).

### Lesson learned
"Replicate Fig. X" is a legitimate scope but should not be conflated with "replicate all
claims of the paper." A follow-up publication-quality replication would sweep at least 3
distinct $(f, \sigma)$ triples spanning the paper's Sec. 2 (globally Lipschitz) and Sec. 3
(non-globally Lipschitz) regimes.

---

## F5 — Two-scheme comparison (SEXP vs. SEM vs. CNM) was NOT implemented

### What happened
Fig. 1 in the paper compares SEXP against semi-implicit Euler–Maruyama (SEM) and
Crank–Nicolson–Maruyama (CNM). We implemented and measured only SEXP.

### Root cause
Scope decision. The paper's *headline* is the SEXP order and CFL-freeness; the SEM/CNM
comparisons are supporting evidence for the *ranking* claim.

### Resolution
- `REPORT.tex` **GENUINE CRITIQUE** §6 explicitly notes: "The relative claim 'SEXP is
  competitive with / better than SEM, CNM' is therefore not independently verified by us."
- A follow-up would add `sem_heat.py` and `cnm_heat.py` and rerun the strong-order harness
  on all three under identical Brownian paths.

### Lesson learned
When a paper's Fig. X is a *comparison* plot, replicating only one of the compared schemes
covers the absolute-order claim but NOT the ranking claim. Flag this explicitly in the
verdict scope.

---

## F6 — Thm 2.3's proved $1/4^-$ rate was declared "out of scope"

### What happened
Row C5 of the claims table (proved $L^q(\Omega)$ rate $1/4^-$ of Thm 2.3) is marked
"proof-only, no." We reproduced only the empirical Fig-1 order $1/2$ under $\Delta x$-fixed
temporal-only refinement.

### Root cause
The proved rate uses a joint $(\Delta t, \Delta x)$ refinement in an
$L^q(\Omega; C([0,T]\times[0,1]))$ norm. Our strong-order experiment is temporal-only at
fixed $M=512$.

### Resolution
- REPORT says C5 is out of scope; the *empirical* Fig-1 order is what we reproduce (C2).
- Follow-up in `open_questions.json` **Q2**: design a joint-refinement grid
  $\Delta x_k = c\,\Delta t_k^{1/2}$ and measure the $L^q$-in-$\Omega$ rate for
  $q \in \{2,4,8\}$.

### Lesson learned
"Proof-level" vs. "numerical" rates are distinct objects. Do not implicitly claim to have
reproduced a proof by reproducing a matching-but-not-identical numerical rate.

---

## Standing discipline (adopted going forward)

1. **Deterministic validation FIRST.** Always. Machine-precision on the linear part before
   any stochastic run. (Saved us on F1.)
2. **Dimensional consistency of discrete noise** must be verified against the target
   continuous noise before running any SPDE strong-order sweep. (Would have caught F1
   earlier.)
3. **Slope reporting** should include a bootstrap CI, not just a point estimate. (F3.)
4. **Scope declaration**: distinguish "replicate Fig. X" from "replicate the paper." State
   the difference in the verdict. (F4, F5, F6.)
5. **Multi-judge with free non-opus endpoints** for verdict scoring. (Done here.)
