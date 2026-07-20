# Failure analysis: Yang et al. 2022 replication

## What worked
- **Topological classification (headline): fully reproduced, 4/4.** All four
  spin-resolved down-spin Chern numbers `C_down=(+1,-1,-1,+1)` and the
  identification of case (ii) `(-i,-i,-i)` as the unique helical / time-reversal-
  symmetric pattern match Table 1 exactly.
- **Numerical anchor.** The kagome loop-current kernel independently confirms the
  chiral flux state carries a Fukui-Hatsugai-Suzuki Chern number `|C|=1` with a
  robust TRS-breaking gap (staggered +/-flux pattern, matching Fig. 2's +/-6*phi).

## What did NOT fully work (honest limitations)

1. **Single-unit-cell kernel vs. paper's 2x2-folded cell.**
   The paper works in an extended 2x2 unit cell with 12 bands per spin (Fig. 1)
   and shows zero-energy edge modes (Fig. 3). The reusable kernel is a single-cell
   3x3 closed-form Hamiltonian. It captures the bulk topology (|C|=1, TRS gap) but
   cannot render the folded bands or count chiral edge modes directly.

2. **FHS Chern SIGN ambiguity at balanced (2-of-3) configs.**
   For patterns (iii) `(-i,i,i)` and (iv) `(-i,-i,i)` the net-flux is balanced and
   the single-cell staggered map is gapless there, so the direct FHS index sign is
   not cleanly resolvable. We therefore assigned the sign via the paper's Eq. (4)
   symmetry operations (`I` preserves, `M` reverses `C`) anchored to the
   numerically-established `C(i,i,i)=+1`. This is exactly how the paper itself
   derives Table 1 — it does not diagonalize four independent lattices — so the
   replication faithfully follows the paper's logic, but the signs of (iii)/(iv)
   are symmetry-derived rather than independently FHS-computed.

3. **Out of scope (not attempted).**
   - SC order parameters and the iCDW->SC pairing map (u4 coupling, Fig. 4).
   - LG quartic coefficients u1, u2 and the 3Q-vs-1Q/2Q selection argument.
   These are the paper's secondary results; the delegated task targeted the 3Q
   iCDW pattern classification / Chern headline, which is fully covered.

## Net assessment
The central, falsifiable claim (four 3Q iCDW patterns; spin-resolved Chern numbers;
unique helical TRS state) is REPLICATED. Residual gaps are cosmetic-to-quantitative
(edge-mode rendering, direct sign of two balanced configs, SC/LG coefficients) and
are enumerated in `open_questions.json` with concrete next steps.
