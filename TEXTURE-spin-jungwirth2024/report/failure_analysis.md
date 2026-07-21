# Failure / gap analysis — Jungwirth 2024/2025 altermagnetism

## Most important caveat (lead)
**The paper is a Perspective/review with NO quantitative benchmark.** There is no fitted number
to agree with. The replication therefore targets the paper's ONE falsifiable claim — the
symmetry/mechanism content of Fig. 1b (M=0 + conserved momentum-dependent d-wave spin splitting
with a protected sign structure) — and verifies it as a set of symmetry-exact assertions. This is
why "Agreement" is scored on symmetry-exactness of forms, not on a numerical residual, and why
"Coverage" is inherently capped: the paper's breadth (d/g/i-wave + 3He/Pomeranchuk analogy +
ab-initio + relativistic effects) far exceeds a single toy model.

## What reproduced (15/15 symmetry-exact checks, d-wave + g-wave)
**d-wave (m=2 baseline):**
- Zero net magnetization: exact (Néel-compensated; BZ-avg splitting ~6e-18).
- Conserved spin channels: S_z good (no SOC), Hamiltonian block-diagonal in spin.
- Momentum-dependent spin splitting: max |Δ| = 0.561 t_nn.
- Dominant angular harmonic m=2, 2 nodal lines on the BZ diagonals (max|Δ| there = 0 to 1e-16).
- C4-ODD protection: antisymmetry residual 0 to 1e-16.
- Sign structure: numeric splitting sign matches −δ_d at 100%.

**g-wave (m=4 coverage-flip extension, MnTe/CrSb class):**
- Zero net magnetization: exact (BZ-avg splitting ~5e-20).
- Dominant angular harmonic **m=4**, **4 nodal lines** (axes k_x=0, k_y=0 AND diagonals
  k_x=±k_y), all node residuals 0 to 1e-16.
- C4-EVEN (90° residual 0) and diagonal-mirror-ODD (residual 0 to 1e-16) — the
  [C2_spin || M_110] protecting spin-group operation.
- 45°-rotation oddness of δ_g near Γ: relative residual < 0.05 (asymptotic, see note below).
- Sign structure: 100% match to −δ_g.

**Unification:** alpha knob reduces g→d exactly at alpha=0 (m2, maxsplit matches d-wave to 1e-12).

## Numerical residual
None in the usual sense — every quantity is grid-independent from n_k=24 upward (symmetry-exact
2×2 diagonalizations). The only residuals are machine epsilon (~1e-16) on node/C4/mirror tests.
The single non-exact quantity is the 45°-rotation oddness of the g-wave form factor: a continuous
45° rotation is NOT a square-lattice symmetry, so δ_g ~ r^4 sin(4θ) is 45°-odd only ASYMPTOTICALLY
near Γ (relative residual < 0.05 on a small circle). The EXACT lattice-symmetric protecting
operation is the diagonal mirror M_110, whose residual is 0 to machine precision.

## Diagnostics fixed during this retry (physics unchanged)
The prior run's g-wave PHYSICS was already correct (M=0, m=4, exact node/C4/mirror residuals) but
three DERIVED diagnostics gave false-negative checks (10/15). All three were extraction bugs, not
physics:
1. **Sign-match = 0.000**: perfect ANTI-correlation. Analytically
   split = √((d−m)²+f²) − √((d+m)²+f²) ⇒ sign(split) = −sign(δ) for m>0. The check compared
   against +sign(δ); fixed to −sign(δ) → 100% for both waves.
2. **Nodal-line count (7 for g-wave, impossible on a closed loop)**: the sign-change counter used
   `diff` without wraparound and double-counted near-zero samples. Fixed to a closed-loop
   (`roll`) sign-change count on nonzero samples → 2 (d), 4 (g), matching the harmonics.
3. **45°-oddness tested on the FULL splitting over the whole BZ**: this mixes in the C4-symmetric
   NN term f(k) and applies a rotation that isn't a lattice symmetry. Fixed to test δ_g itself on
   a small circle near Γ with a physical relative tolerance.
The tight-binding model and all raw physics observables were untouched.

## Scope NOT built (coverage-capping, expected for a Perspective)
- i-wave altermagnet (m=6, 6 nodal lines) — d- and g-wave now covered.
- Ab-initio material-specific band structure and eV-scale splitting magnitudes.
- The superfluid-3He / higher-partial-wave Pomeranchuk-instability analogy (the paper's core novelty).
- Relativistic (SOC) altermagnetic effects: weak ferromagnetism, anomalous Hall.
- Explicit spin-group operator proof (we verify C4/mirror residuals numerically, not as a symmetry algebra).

## Extraction tooling degradation (not a physics gap)
marker/nougat not installed → artifacts 2+3 are pdftotext interim fallbacks with degraded
Unicode/math rendering. Authoritative equations are hand-transcribed into REPORT.tex and
nougat.mmd. Regen commands documented in artifacts_summary.md.

## What would raise the verdict
Building the i-wave case (completing d/g/i) + a DFT band-structure comparison for MnTe/CrSb would
convert the "mechanism replicated" call into a material-anchored quantitative one. As a
Perspective, however, mechanism-level + symmetry-exact reproduction across the d- AND g-wave
classes is the correct ceiling for this paper.

## Verdict
**REPLICATED** at the mechanism / symmetry level, d-wave + g-wave (15/15 checks). Final verdict by LLM judge.
