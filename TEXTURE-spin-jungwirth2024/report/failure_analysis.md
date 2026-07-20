# Failure / gap analysis — Jungwirth 2024/2025 altermagnetism

## Most important caveat (lead)
**The paper is a Perspective/review with NO quantitative benchmark.** There is no fitted number
to agree with. The replication therefore targets the paper's ONE falsifiable claim — the
symmetry/mechanism content of Fig. 1b (M=0 + conserved momentum-dependent d-wave spin splitting
with a protected sign structure) — and verifies it as a set of symmetry-exact assertions. This is
why "Agreement" is scored on symmetry-exactness of forms, not on a numerical residual, and why
"Coverage" is inherently capped: the paper's breadth (d/g/i-wave + 3He/Pomeranchuk analogy +
ab-initio + relativistic effects) far exceeds a single toy model.

## What reproduced (6/6 symmetry-exact checks)
- Zero net magnetization: exact (Néel-compensated by construction, BZ-avg splitting ~1e-18).
- Conserved spin channels: S_z good (no SOC), Hamiltonian block-diagonal in spin.
- Momentum-dependent spin splitting: max |Δ| = 0.561 t_nn, finite and k-dependent.
- d-wave nodes on BZ diagonals: max|Δ| on k_x=±k_y is 0 to 1e-16.
- Sign flip under C4: ΓX (−0.2246) vs ΓY (+0.2246), antisymmetry residual 0 to 1e-16.
- d-wave sign structure: numeric splitting sign matches analytic (t1−t2)(cos kx − cos ky) at 100%.

## Numerical residual
None to report in the usual sense — every quantity is grid-independent from n_k=24 upward
(these are symmetry-exact 2×2 diagonalizations). The only "residual" is machine epsilon on the
node and C4-antisymmetry tests (~1e-16).

## Convention note fixed during the run
The first coarse run reported a d-wave sign-match of 0.000 — a **perfect anti-correlation**, i.e.
a pure sign-convention artifact in how the analytic form factor δ(k) was written. The physics was
correct (splitting exactly tracked −δ); flipping δ to (t1−t2)(cos kx − cos ky) to match the
diagonalized lower-band splitting gave 100% match. No physics changed; documented for honesty.

## Scope NOT built (coverage-capping, expected for a Perspective)
- g-wave / i-wave altermagnets — the paper's actual materials MnTe, CrSb are g-wave.
- Ab-initio material-specific band structure and eV-scale splitting magnitudes.
- The superfluid-3He / higher-partial-wave Pomeranchuk-instability analogy (the paper's core novelty).
- Relativistic (SOC) altermagnetic effects: weak ferromagnetism, anomalous Hall.
- Explicit spin-group operator proof (we verify C4 antisymmetry numerically, not as a symmetry algebra).

## Extraction tooling degradation (not a physics gap)
marker/nougat not installed → artifacts 2+3 are pdftotext interim fallbacks with degraded
Unicode/math rendering. Authoritative equations are hand-transcribed into REPORT.tex and
nougat.mmd. Regen commands documented in artifacts_summary.md.

## What would raise the verdict
Building the g-wave case + a DFT band-structure comparison for MnTe/CrSb would convert the
"mechanism replicated" call into a material-anchored quantitative one. As a Perspective, however,
mechanism-level + symmetry-exact reproduction is the correct ceiling for this paper.

## Verdict
**REPLICATED** at the mechanism / symmetry level (6/6 checks). Final verdict by LLM judge.
