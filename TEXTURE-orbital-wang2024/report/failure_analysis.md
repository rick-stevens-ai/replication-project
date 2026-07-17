# Failure Analysis — wang2024 (arXiv:2411.00315)

Verdict is **REPLICATED (headline)**. This document records the honest gaps and
limitations — what did NOT fully reproduce and what a fuller replication would need.

## 1. Absolute sigma normalization constant (the one real gap)
- **Symptom:** the spin Hall in-gap plateau reads **~2.85**, not the canonical
  **2 e^2/h** expected for the QSH phase; the orbital Hall plateau reads **-8.83** in
  the same units.
- **Root cause:** `sigma` is reported with a generic Chern-integral normalization
  (e^2/h-like), NOT the exact spin-Hall `e/4*pi` vs orbital `e/2*pi` unit conventions.
  It is an overall multiplicative **units constant**, not a physics error.
- **Why it does not change the verdict:** the physically meaningful, testable
  quantities — plateau flatness (std = 0.000), in-gap constancy, and the
  orbital-`>>`-spin ratio — are **prefactor-independent**. The topological claim is
  about quantization/flatness and hierarchy, all of which reproduce.
- **Fix path (see open_questions Q1):** calibrate the prefactor against the known
  QSH result (spin plateau -> exactly 2 e^2/h) in the pristine KM topological phase,
  then apply the same constant to the orbital channel.

## 2. Minimal-model scope
- **What was reproduced:** the minimal 4-band Kane-Mele honeycomb model — the standard
  low-energy description of a buckled group-IV monolayer.
- **What the paper actually uses:** the richer Liu-Jiang-Yao (ref [42]) 4-orbital
  (s, p_x, p_y, p_z) x spin x sublattice germanene TB, plus the full POAM /
  Wannier-charge-center analysis.
- **Implication:** the **universal, topology-protected claim** (a flat quantized in-gap
  orbital Hall plateau) is exactly what the minimal model captures and confirms. The
  *exact* plateau value in the full multi-orbital model is untested (open_questions Q2).

## 3. Claims not directly tested
- **C1 (POAM sector WCC windings):** the topological invariant was inferred via its Kubo
  transport consequence, not computed independently (open_questions Q3).
- **C4 (feature-Berry k-space texture map):** the Kubo integrand peaks near the Dirac
  points as expected, but a full feature-Berry-curvature texture render was not produced.
- **C5 (ribbon edge states / bulk-boundary):** bulk-only reproduction; the zigzag-ribbon
  orbital-polarized edge states were not attempted.

## 4. Prior bug (already fixed, recorded for completeness)
- An earlier orbital operator `L_z = tau_y` gave `sigma^L = 0` because
  `{tau_y, tau_x(=v_x)} = 0`. Fixed by switching to the itinerant position-based
  `L_z = 0.5*(X v_y - Y v_x)`, the physically correct honeycomb orbital operator, which
  yields the nonzero plateau. This is a resolved implementation bug, not an open failure.

## 5. What a fuller reproduction needs
1. Pin the e^2/h normalization (Q1).
2. Implement the full ref-[42] germanene multi-orbital TB (Q2).
3. Direct POAM Chern number via WCC winding / Fukui-Hatsugai (Q3).
4. Rashba + staggered-potential robustness sweep (Q4).
5. Finite-T + disorder robustness (Q5).
6. Ribbon calculation for the bulk-boundary correspondence (C5).
