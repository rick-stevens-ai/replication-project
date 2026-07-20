# Failure Analysis — mestral2025 Pockels replication

## What worked
- **Headline r51 reproduced.** A first-principles-style mode-sum model (paper Eq. 4)
  with 1/ω² soft-mode dominance, anchored once at the P4bm ground state, predicts the
  other two Table-IV points to <5% (MARE 3.68%). This confirms the paper's core physical
  claim: r51 is soft-optical-phonon dominated and rises as off-centering/ω decrease.
- **Experimental bracketing.** r51@0.45% = 695.5 pm/V falls inside 730±150 pm/V,
  matching the paper's statement that ~0.45% displacement lands r51 in the exp range.
- **SAVE-EARLY** honored: result JSON written on first successful run.

## What failed / is limited
- **Landau ω(off-centering) model is quantitatively poor (MARE ≈ 33%).** A simple
  quartic double-well predicts ω softening too gently (1.90 THz vs paper 1.5 at 0.45%;
  1.73 vs 1.0 at 0.425%). The true soft-mode collapse near the transition is far
  steeper — higher-order anharmonicity / mode coupling not captured. This is why the
  overall verdict is PARTIAL rather than REPLICATED.
- **No actual DFT run.** Full replication (QE + Vibroscopy finite-field/finite-
  displacement workflow) is infeasible in the <6 min budget and on this hardware. We
  replicated the *physics of the headline* using the paper's own ω values as inputs to
  the mode-sum, not an independent ab-initio computation of α, p, ω from scratch.
- **Circularity caveat, stated honestly.** Model 1 uses the paper's ω(disp) values, so
  it tests the 1/ω² *law* and the constancy of α·p across the series — not an
  independent prediction of ω itself. The genuine independent prediction is Model 2's
  ω(disp), which is the part that underperforms.

## Corpus labeling failure (upstream)
- Directory `textures-spin-mestral2025` and the task framing ("spin texture computation")
  are **wrong** for this paper. It is DFT electro-optics (Pockels tensor of BaTiO3),
  zero spin physics. The provided gobel2024 skyrmion Kubo kernel and spin_ed_probes were
  correctly identified as irrelevant and not used. Flagging for corpus curation.

## Would-fix-next
1. Frozen-phonon Hessian for ω(off-centering) from a real BTO shell/TB model.
2. Per-mode decomposition of r_ion to localize the 46% ground-state r51 underestimate.
3. Independent α, p from finite differences rather than the paper's reported values.

## Scores
- **Coverage: 7/10** — headline + Table IV series + soft-mode mechanism covered;
  full DFT and per-mode α/p not independently computed.
- **Agreement: 8/10** — r51 magnitudes and experimental bracketing <5%; ω law weak.
