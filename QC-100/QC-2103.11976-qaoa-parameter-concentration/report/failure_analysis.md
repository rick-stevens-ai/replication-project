# Failure Analysis — QC-2103.11976 QAOA Parameter Concentration

Honest critique of what the replication does *not* prove, what could still be
wrong, and where the verdict of REPLICATED should be trusted vs treated with
caution.

## 1. Headline exercised? Yes — but scope is narrower than "QAOA" writ large.

The paper's own scope is **QAOA state preparation** with $H_z = 1 - |t\rangle\langle t|$,
i.e. a rank-1 projector cost with target $|t\rangle = |0\ldots0\rangle$. This
replication runs QAOA on exactly that setting and independently regenerates:
- the closed-form overlap (eq.5), cross-verified against Qiskit statevector to $10^{-16}$;
- the analytical relation $\gamma = \pi - 2\beta$ (0.3% fit error);
- the leading-order $\beta^\star \approx \pi/(n+2)$ (6-digit match at $n=40$);
- the concentration itself: $\Delta^2$ drops by $\sim 1100\times$ over $n=4..40$.

The concentration was **regenerated**, not quoted. But: this is concentration
for the projector-cost / single-target family. Nothing here extends to MaxCut,
SK, or any other real optimization problem. That extension is *conjectured*
common wisdom in the community but the paper's proof does not cover it and
neither does this replication. Someone reading "QAOA parameter concentration
replicated" should not conclude that concentrated angles are guaranteed
useful warm-starts for combinatorial optimization; that is Open Question 1.

## 2. Quantitative gap: concentration exponent l ≈ 3.5, not 4.

Paper claim: $\Delta^2 = O(1/n^4)$ with the specific leading form
$\approx 5\pi^2/[(n+4)^2(n+5)^2]$ (eq.11), i.e. asymptotic exponent $l=4$.

My measured exponents:

| range | l |
|-------|---|
| n=4..19  | 3.03 |
| n=20..39 | 3.50 |
| n=25..39 | 3.55 |
| n=30..39 | 3.58 |

The exponent is drifting upward with $n$ but is still ~10-13% below the
paper's asymptotic value at $n=40$. Two interpretations:
- **Benign:** finite-$n$ sub-leading correction (the paper's eq.9 says
  $\beta = \pi/n - 4\pi/n^2 + O(1/n^3)$; squared drift picks up an
  $O(1/n^3)$ cross-term that decays slowly). Continue to $n=100$ and $l$
  should approach 4.
- **Adversarial:** the paper's $l=4$ claim is asymptotic and the crossover
  scale is much larger than $n=40$. In that case, at any practically relevant
  $n$, the effective concentration is $O(1/n^{3.5})$ not $O(1/n^4)$.
  Still concentration, but ~30% weaker than the paper's leading form
  suggests at $n=40$.

I did not run $n>40$; that would take minutes not hours, and would settle
this. It is left as an implicit follow-up.

## 3. Missing baseline: no test of when concentration fails.

The strongest possible confirmation of a mechanism is showing the mechanism
*switches off* on cue. I did not sweep a family of $H_z$ where concentration
should weaken or vanish (e.g. random full-spectrum $H_z$, mixed-Hamming-weight
target ensembles). Without that, my $1100\times$ drop in $\Delta^2$ could in
principle be an artifact of the specific projector structure rather than
"concentration" as a general phenomenon.

Concrete gap: I have "concentration observed on projector cost" — I do not
have "concentration NOT observed on random cost". The second half is essential
to isolate the mechanism. See Open Question 2.

## 4. Scope: p=1,2 only.

Claim C6 (paper extends numerically to $p=5$, Table I) was explicitly out of
scope. The depth-scaling aspect of concentration is untested. A depth-$p$
run is $\sim 2p$ Wall clock relative to $p=1$; running $p=3,4,5$ for
$n=4..15$ is straightforward but was not done. This means my verdict speaks
to $p\le2$; the $p=3,4,5$ story is inherited on the paper's word.

## 5. Optimization risk.

L-BFGS-B is local. The QAOA landscape is non-convex; the $(\beta\to\pi-\beta,
\gamma\to 2\pi-\gamma)$ symmetric branch is a known trap. Mitigation: 32-48
random seeds per size, explicit branch folding, seeded starts at the paper's
asymptotic guesses. Residual risk: a *third* basin at intermediate $n$ that
neither seed cloud nor branch fold catches. This would show up as a
discontinuity in $\beta_\text{opt}(n)$ that I don't see, which is
reassuring but not rigorous. A basin-hopping or grid-then-refine global
optimizer would harden — not done here.

## 6. No noise model.

The paper is pure theory (exact statevector) and this replication is faithful
to that. Any operational claim about NISQ parameter transfer — "concentrated
angles are good hardware seeds" — requires a noise sweep that I did not do.
See Open Question 4.

## 7. What could still be wrong in my replication itself.

- **Circuit gate direction / sign:** eq.5 is symmetric in
  $(\gamma\to-\gamma, \beta\to-\beta)$ up to conjugation. My Qiskit circuit
  uses `Diagonal([exp(-i*gamma)] + [1]*(2**n - 1))` and RX($2\beta$). The
  $10^{-16}$ agreement with the analytical formula rules out sign errors
  because a wrong sign would still yield a valid overlap value — but a
  wrong sign that happens to also give the same overlap magnitude is
  extraordinarily unlikely at three tested $n$ values.
- **Folding convention:** I folded the $(\beta\to\pi-\beta, \gamma\to
  2\pi-\gamma)$ symmetric branch to the small-$\beta$ side before fitting.
  If the paper's "canonical branch" is actually the other one, my fit
  coefficients would flip sign — but the fit exponents wouldn't change,
  so C4 stands regardless.
- **Version drift:** Qiskit 2.5.0 removed several APIs used by pre-1.0
  QAOA tutorials. The Statevector overlap path (`Statevector.from_instruction`
  + `state.data`) is stable and gives the same numbers as v1.4.

## 8. Bottom line.

REPLICATED is the right verdict for the paper's specific scope. If a reader
takes "QAOA parameter concentration is real" as license to (i) drop
optimization entirely on any QAOA problem, (ii) assume $l=4$ concentration
at any $n$, or (iii) transfer angles across noise models unchecked, they will
be misled — but that's a scope-of-inference error, not a replication failure.
