# Workflow — Reduced-model replication of Agarwal et al. (arXiv:2408.04017)

## Goal
Reproduce the *essential mechanism* (not the full material): shift-photoconductivity
vector σ(r) forms real-space vortices tracing a polar meron/antimeron network and is
(anti)parallel to the in-plane polarization P(r).

## Discipline applied
Previous attempt timed out reasoning too long before coding. This run: <3 min reading
method_extract.md + marker grep, then wrote code to disk immediately, streamed results
to `work/results.json` after every claim, ran early (22s first pass), refined once.

## Steps
1. **Read** `report/method_extract.md` + grepped `extraction/marker.md` for the key
   equations (meron winding Q=±1/2, shift vector Eq.2-3, antiparallel-to-P claim, ω_M~6eV).
2. **Design the reduced model** (deliberately minimal):
   - 2-band `H(k;r) = d(k,r)·σ` with in-plane offset `(b·n_x, b·n_y)` from a
     configuration-space meron field `n(r)` over the moiré cell.
   - This collapses the paper's four-band SU(4) reconstruction to the smallest model
     that still carries the topology + shift-current geometry.
3. **Claim 1 — meron quantization:** built `n(r)` as a meron/antimeron; computed the
   skyrmion charge via signed spherical-triangle solid angle (Oosterom–Strackee) and the
   integer in-plane director winding via a discrete loop integral of arg(P).
4. **Claim 2 — shift vortex:** computed σ(r) per real-space point as a BZ-summed,
   resonance-weighted shift vector; measured the winding of σ around the meron core and
   its vorticity (curl_z).
5. **Claim 3 — σ ∥ P:** masked out the vanishing-|P| core, computed cos∠(σ,P) map,
   mean|cos|, and aligned fraction.
6. **Claim 3b — antiparallel window:** re-evaluated σ at the *upper* resonance branch to
   show the parallel/antiparallel SIGN is a frequency-window property (paper's ω_M
   antiparallel fingerprint), giving cos → −1.
7. **Figures** (matplotlib, Agg): P texture + σ vortex; P-vs-σ overlay + cos-angle map.
8. **Report artifacts:** REPORT.tex→pdf, open_questions.json, this workflow, artifacts
   summary, failure analysis; updated META.json.

## Numerical methods
- Eigensystem: `numpy.linalg.eigh` on 2×2 d·σ per (k,r).
- Meron charge: signed spherical-triangle areas summed / 4π.
- σ(r): closed-form two-band shift vector direction (∝ ±d/|d|) × transverse dipole
  weight × Lorentzian band-edge resonance, BZ-summed. Gauge-invariant (no noisy phase
  unwrapping — the v1 finite-difference version was noisy and was replaced).
- Grids: P texture 121×121; σ(r) on 41×41 real-space, 20×20 k-grid per point.

## Runtime
CPU-only, numpy/scipy/matplotlib. Full pipeline ≈1.5 s after the analytic σ refactor
(the initial finite-difference σ took ~22 s). No paid APIs, no network.

## Reproduce
```
cd TEXTURE-polar-agarwal2024
python3 code/agarwal2024_replication.py     # writes work/results.json + figs/
cd report && pdflatex REPORT.tex            # -> REPORT.pdf
```
