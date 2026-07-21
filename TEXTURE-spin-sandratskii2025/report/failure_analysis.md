# Failure / Gap Analysis — sandratskii2025 (arXiv:2501.11327)

## What was reproduced (qualitatively, 6/6 checks)
- **P1** Exact moment compensation (zero net moment) — trivially exact by construction.
- **P2** Spin-degenerate nodal line along (0,0,kz) — emerges from C6z symmetry.
- **P3** Nonzero spin splitting at general k=(0.1,0.2,kz).
- **P4** Sign-changing form factor, BZ-average/max ratio = 0.020 (~0), 50/50 +/- area.
- **P5** Well-defined kz parity (even).
- **Null** Isotropic (ferromagnet-like) model gives zero splitting (3e-15).

## Honest gaps

### GAP 1 — Form factor is d-wave-like (4 nodes), not MnTe's g-wave (8 nodes)
Measured angular sign-changes at |k|=0.3 = **4**, i.e. a d-wave-like pattern.
Real alpha-MnTe is a **g-wave** altermagnet (8 nodes) because the two Mn sublattices
are related by a 6-fold screw, not a simple 60-deg rotation of a single anisotropic
lobe. The minimal single-anisotropic-hopping surrogate captures the *existence* and
*sign-changing/BZ-null* character of the splitting but underrepresents the angular
harmonic order. This is a **form-factor mismatch, not a qualitative failure**.
Fix: full two-pair hexagonal model with the C6z^n screw stacking (see open_questions Q1).

### GAP 2 — The paper's actual method is not reproduced
The paper's headline *contribution* is the **direct-DFT two-constraint magnon method**
and the claim that the electronic k-space spin-splitting pattern equals the magnon
q-space chirality-splitting pattern. We reproduced only the **electronic** side, and
via a tight-binding surrogate rather than DFT. The magnon method and the k/q pattern
equivalence are untested here (see open_questions Q2, Q5).

### GAP 3 — No physical energy scale
Splitting is in arbitrary model (hopping) units; no meV calibration to DFT/ARPES.
No quantitative comparison to any number in the paper is possible (see Q3).

### GAP 4 — Te-induced moments omitted
The paper emphasizes Te-induced moments in magnon states; our Mn-only model cannot
address them (see Q4).

## Bottom line
The electronic altermagnetism headline is reproduced at the qualitative/symmetry level
with a from-scratch model and a passing null test. Because the defining altermagnet
class (g-wave) is only approximated (d-wave-like), the DFT magnon method is not
reproduced, and no meV-scale comparison exists, the honest verdict is **PARTIAL**.
