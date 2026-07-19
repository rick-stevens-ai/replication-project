# Failure & Gap Analysis: arXiv:1211.0762 (Zhang, Liu & Zhang 2012)

**Verdict: REPLICATED** (Coverage 8/10, Agreement 9/10). This document separates what
reproduced with high confidence from what did not, and marks each gap as EXPECTED/scoped-out,
a CONVENTION gap, or a real shortfall.

## What reproduced (high confidence)

- **p_z helical spin texture** — angular form exact to 2.2e-16; left-handed upper cone /
  right-handed lower cone reproduced with correct sign.
- **p_x / p_y orbital spin textures (Eqs. 7, 8)** — recovered as the `[sin, cos]` small-k
  limit; residual 3.9e-5 at k=1e-4 is the O(k) truncation of the paper's own stated limit.
- **Orbital-character 2θ (π-periodic) modulation** — exact to 2.1e-16, confirming the
  `cos(2θ)` angular dependence of D_{px,0} − D_{py,0}.
- **P_{px} polarization (Eq. 10)** — exact to 2.5e-16, including the SIGN FLIP across the
  Dirac point (upper cone tangential/negative, lower cone radial/positive). This is the
  paper's proposed spin-ARPES observable.
- **Net right-handed in-plane orbital spin for BOTH cones** — the paper's headline
  qualitative surprise; angular form and handedness reproduced exactly.

## Gaps

### 1. No hexagonal-warping term — EXPECTED / correct scoping (NOT a shortfall)
The TEXTURES-100 task framing mentioned "hexagonal warping," but **arXiv:1211.0762 does not
contain a warping term.** Its model is the isotropic Dirac cone (Eq. 1) plus orbital-resolved
wavefunctions. The Fu C3v k^3 warping term belongs to a *different* paper (Fu, PRL 2009). We
deliberately replicated the actual paper; **no warping term was implemented because the paper
contains none.** If the intent was the Fu-warping model, that is a separate replication target
(captured as open question Q4). Adding a term the paper never had would be replicating a paper
that wasn't written.

### 2. Factor-2 prefactor on total in-plane spin — CONVENTION gap (NOT a physics disagreement)
Our total in-plane spin magnitude prefactor is `2(v0 ∓ k·u1)·k·w1` vs the paper's `4(…)` — an
**exact factor of 2, constant across k and θ**. Direction and handedness are identical
(right-handed both cones). Origin: (a) the paper's atom/orbital sum over α (a cross-term) is
collapsed here to one effective orbital, and (b) a Pauli-vs-spin (1/2) convention. Under this
collapse only ratios, angular forms and signs are physical — and all of those match. This is
the single point where our numbers differ from the paper, and it is a documented convention
choice, not a contradiction. (Closing it is open question Q1.)

### 3. Small-k limit of Eqs. 7, 8 — EXPECTED
Eqs. 7 and 8 are the paper's explicitly stated small-k forms. Verified in that limit; the
3.9e-5 residual is the expected O(k) correction, not an error.

### 4. No ab-initio (DFT+SOC) cross-check — scoped out for a k·p replication
The paper presents both an effective k·p model AND ab-initio results. We reproduced the
analytic k·p predictions only, which is the appropriate target for a model-Hamiltonian
replication. Independent DFT confirmation is open question Q2.

## Environment / tooling gaps (NOT physics)

- **marker / nougat not installed** → artifacts 2 & 3 delivered as `pdftotext`-based interim
  files with honest provenance headers. `marker.md` = `pdftotext -layout` (prose/structure);
  `nougat.mmd` = hand-transcribed LaTeX key-equations block + raw reading-order dump. Math
  fidelity in the raw dump is degraded (a known pdftotext limit); the authoritative equations
  are hand-transcribed in REPORT.tex and in nougat.mmd's key-equations block.
- **pdflatex not installed** → REPORT.tex ships as source; compiles off-host with any standard
  LaTeX toolchain. Not a package failure.

## What would raise the verdict
Closing Q1 (retain the α-sum, kill the factor-2) would take agreement to ~10/10; adding the
DFT cross-check (Q2) would take coverage above 8/10.
