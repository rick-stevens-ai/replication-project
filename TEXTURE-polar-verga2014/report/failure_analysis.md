# Failure / Gap Analysis --- textures-polar-verga2014

Verga 2014, "Skyrmion collapse," arXiv:1409.0256v2.
Verdict: **PARTIAL** --- Coverage 6/10, Agreement 8/10.

This is a **dynamics/mechanism** paper. Per the `computational-replication-execution`
skill (Verga2014 guidance), the correct scoping under a wall-clock budget is to
replicate the **static energetics + topological invariant + scaling exponents**
(all cheap and where the checkable physics lives) and to **explicitly scope out**
the full coupled time integrator. That is what was done. The gaps below are
deliberate scope, not silent failures.

## What reproduced (agreement high)

1. **BP exchange energy -> 4piJ.** Discrete Heisenberg energy of the BP field
   converges to the exact continuum `E_xc = 4piJ = 5.0265`: `E/(4piJ) = 0.9966`
   at lambda=8 on L=512 (<0.5%). This is a real replication of the paper's central
   energetics, not a fit.
2. **Topological charge Q = +/-1.** Berg-Luscher lattice charge gives Q = -0.980
   (core -z) / +0.980 (reversed), correct magnitude AND sign convention (paper's
   collapsing initial state is Q = -1 / core -z).
3. **Lattice scale-invariance breaking -> barrier-free collapse.** E(lambda) peaks
   near lambda~6 and decreases toward the ferromagnet (E=0) with NO barrier, so a
   single-spin flip is downhill --- the paper's "collapse by change of a single spin,"
   regularized by the lattice cutoff a.
4. **Self-similar exponents alpha=1, beta=1/2.** Recovered exactly by dimensional
   balance of the paper's ansatz w=(t*-t)^{-alpha} f(r/(t*-t)^beta) (Eq. 17), with
   no dynamics simulated.

## Honest gaps (NOT built)

1. **Coupled Schrodinger + Landau-Lifshitz time integrator.** The core dynamical
   engine --- quantum electron propagation on the lattice feeding the STT into the
   LL equation each step --- was NOT built. All time-dependent claims (Figs. 2-3)
   depend on it. This is the single unlock for open questions Q1-Q5.
2. **Collapse time t* ~ lambda/(s0 a).** Not measured; requires the solver above.
   The paper's snapshots are around t ~ 5900 t0.
3. **Electron b-field topological-vortex nucleation.** The claim that the
   Q-collapse correlates with an intense electron b-field vortex (Sec. III) needs
   the self-consistent electron spin field s(r,t); not built.
4. **Exchange-dissipation smoothing (Fig. 3 d-scan).** The dissipation-dependent
   smoothing of the Q(t) transition was not reproduced; needs the solver + a d-scan.
5. **Full self-similar PROFILE f(X) (Eqs. 24-25).** Only the exponents were
   verified, not the master profile / data collapse.

## Non-gaps (things that look like failures but are not)

- **E/(4piJ) drop at lambda=64 (0.951).** This is the skyrmion tail reaching the
  open boundary at lambda -> L/8 on L=512, a finite-box edge effect --- NOT a
  disagreement with the 4piJ result. The clean comparison window is lambda=8-16.
- **Q = 0.980 rather than exactly 1.000.** Discretization of a lambda=20 field on
  L=256; converges to 1 with larger lambda/L. The sign and quantization are the
  physics; the ~2% is lattice resolution.
- **No DMI term.** Correct: the paper has none. The task brief's "DMI" phrasing is
  generic; the model is pure exchange + STT + polarization field. Adding DMI would
  replicate a different paper.

## Extraction-tooling limitation
Marker and Nougat are not installed on this host; `extraction/marker.md` and
`extraction/nougat.mmd` are pdftotext-based interim artifacts (the skill's
sanctioned fallback). Equation fidelity in nougat.mmd is hand-transcribed, not
Nougat-OCR'd. Re-run with the real tools when available.
