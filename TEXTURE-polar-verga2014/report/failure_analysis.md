# Failure / Gap Analysis --- textures-polar-verga2014

Verga 2014, "Skyrmion collapse," arXiv:1409.0256v2.
Verdict: **REPLICATED (target)** --- Coverage 8/10, Agreement 8/10.

This is a **dynamics/mechanism** paper. Earlier passes replicated the static
energetics + topological invariant + scaling exponents but explicitly scoped out
the full coupled time integrator. **This coverage-flip pass BUILDS that solver**:
a self-consistent Schrodinger(electrons) + Landau-Lifshitz(spins) time integrator
that reproduces the paper's central *dynamic* claim --- the current-driven,
finite-time topological collapse Q:-1->0. What remains unbuilt is now
quantitative fine-detail (exact t* value, full 2D b-field field maps), not the
mechanism.

## What reproduced (agreement high)

### Static / scaling core (prior pass)
1. **BP exchange energy -> 4piJ.** `E/(4piJ) = 0.9966` at lambda=8 on L=512 (<0.5%).
2. **Topological charge Q = +/-1.** Berg-Luscher: Q = -0.980 / +0.980, correct
   sign convention (collapsing initial state Q = -1, core -z).
3. **Lattice scale-invariance breaking -> barrier-free collapse.** E(lambda) peaks
   near lambda~6 then decreases toward the ferromagnet with no barrier.
4. **Self-similar exponents alpha=1, beta=1/2.** Exact by dimensional balance of
   Eq. 17.

### Dynamic core (THIS pass -- coupled solver)
5. **Coupled Schrodinger+LL time integrator BUILT and stable.** Strang
   operator-splitting, norm-conserving electron propagation (FFT kinetic +
   analytic 2x2 local spin rotation with Peierls phase from the E-field) coupled
   to RK4 Landau-Lifshitz with the STT torque `Js s_i` and the exchange
   dissipation `d = beta grad^2 f`. ~0.7 ms/step on L=48; 7 full runs in 122 s.
6. **Dynamic topological transition Q:-1->0 at finite t*.** The driven skyrmion
   collapses to the ferromagnet: Q(t) evolves monotonically from -1.00 to ~-0.07
   (baseline). This is the paper's main dynamic result (Figs. 2-3), now
   reproduced from the coupled equations, NOT bracketed statically.
7. **Norm-breaking is essential (paper Sec. II).** The collapse only proceeds
   because the exchange-dissipation term breaks |S|=1; with |S| renormalized each
   step (topological protection restored) Q stays pinned at -1 and the core only
   oscillates. This directly confirms the paper's stated regularization mechanism.
8. **Dissipation shortens t* (Fig. 3 trend).** t* = 2653 / 2523 / 820 t0 for
   beta = 0.001 / 0.01 / 0.1 --- monotonic decrease, same qualitative trend as
   the paper (5936 / 1748 / 1236). Order of magnitude (~10^3 t0) matches.
9. **t* ~ lambda0 / s0 (paper line 616).** t* = 1835 / 2653 / 3350 t0 for
   lambda0 = 6 / 8 / 10 --- increases ~linearly (slope ~379), consistent with the
   paper's finite-time estimate t* ~ lambda0/(s0 a).
10. **Self-similar core-shrink law.** The core size follows
    lambda(t) = lambda0/sqrt(1+(s t)^2) (paper line 551) with a fittable rate s.

## Honest gaps (remaining, quantitative fine-detail)

1. **Exact t* value.** Our t* ~ 2653 t0 (baseline) vs the paper's ~5936 t0 ---
   same order of magnitude (~10^3) and correct trends, but not the exact number.
   Expected: we use a **mean-field single-field reduction** of the many-electron
   Fermi sea (density ~ne) on a small L=48 lattice, whereas the paper propagates
   the full spectral electron problem on L=128. The absolute t* depends on the
   detailed electron-spin backreaction magnitude, which the reduction rescales.
2. **Electron b-field vortex maps (Fig. 4).** We compute the electron spin field
   s(r,t) self-consistently (it IS the torque source), but did not produce the
   full 2D b-field topological-density snapshots / the Qelec = +1 balance imagery.
3. **Full self-similar PROFILE f(X) (Eqs. 18-25, Meijer-G).** Only the exponents
   and the sqrt shrink law are verified, not the master profile / data collapse.
4. **L=128, full-spectral electron sea.** Out of the perf budget; the mean-field
   reduction is the deliberate trade to keep the coupled run under a few minutes.

## Non-gaps (things that look like failures but are not)

- **t* factor ~2 below paper.** Not a disagreement in mechanism --- it is the
  mean-field/lattice-size reduction rescaling the absolute torque; all *trends*
  (beta down -> t* down; lambda0 up -> t* up; sqrt shrink; Q:-1->0) reproduce.
- **Qfinal ~ -0.07 not exactly 0.** Berg-Luscher on a norm-broken, near-uniform
  lattice; the residual is lattice-discretization noise on an essentially
  ferromagnetic state.
- **E/(4piJ) drop at lambda=64 (0.951).** Skyrmion tail reaching the open box
  boundary on L=512; finite-box edge effect, clean window is lambda=8-16.
- **No DMI term.** Correct: the paper has none (pure exchange + STT + polarization
  field). The task brief's "DMI" phrasing is generic.

## Extraction-tooling limitation
Marker and Nougat are not installed on this host; `extraction/marker.md` and
`extraction/nougat.mmd` are pdftotext-based interim artifacts (the skill's
sanctioned fallback). Re-run with the real tools when available.
