# Failure & Limitation Analysis — Patri et al. (2018) Replication

**Verdict: REPLICATED** (all four headline sub-claims reproduced). This document records what the replication does *not* establish and the honest caveats behind the perfect-looking agreement.

## 1. Why agreement is "exact" — and what that does/doesn't prove
The headline is a **symmetry-dictated identity**, not a fitted number. Once the T_d-allowed octupole–strain coupling `ΔF=-g_O m(ε_yz h_x+ε_xz h_y+ε_xy h_z)` is written down, minimizing the quadratic elastic energy gives `ε_xy=(g_O/c44)m h_z` algebraically, so:
- linear-in-h (exponent exactly 1),
- coefficient exactly ∝ m and ∝ g_O/c44,
- the [111] projection factor 1/√3

all follow **analytically and parameter-free**. Our numerics confirm we implemented the algebra correctly (exponent 1.0000, R²=1.000), which validates the paper's *internal logic* very strongly — but it does **not** independently confirm any material-specific magnitude.

## 2. What is NOT replicated (coverage gaps → Coverage 8/10)
1. **Microscopic g_O and γ₀.** These come from 2nd/3rd-order perturbation theory in h·J with the real CEF gaps Δ(Γ4), Δ(Γ5). We did not diagonalize the full PrV₂Al₂₀ CEF Hamiltonian, so the absolute size of the effect is not tested.
2. **The T_O ≈ 0.65 K transition and Fig.1 phase diagram.** Part C uses an *isolated* FO double-well; the paper's T_O is renormalized by the u_φm, u_φ̃m couplings to the quadrupolar sector, which we did not include.
3. **Hysteresis loop shape/coercive field.** Our loop width (=1 in units of spontaneous m) is a qualitative demonstrator of the cubic-in-h mechanism, not a fit to a competing quadrupolar landscape or to data.
4. **Other field directions (Table 2, [100]/[110]).** Not attempted here; these are the quadrupolar-probe cross-checks.

## 3. Bugs encountered and fixed
- **KeyError in ket() construction.** `spin_matrices` returns the |m=J,...,-J> ordering; the |Jz=mz>→row map was initially `int(round(J-mm))` (an index, not m_z), which failed on `ket(-4)`. Fixed to `int(round(mm))`. The SAVE-EARLY write of part-B had already succeeded before this crash, so no data was lost — validating the save-early discipline.
- **Claim-3 false negative.** The computed ratio A/[(g_O/c44)m] = 0.57735 first registered as a mismatch against a naive expectation of 1. This is exactly 1/√3 = the [111] geometric projection (h_i=h/√3); the paper only claims proportionality (∝), which holds. The comparison test was corrected to compare against 1/√3.

## 4. Susceptibility caveat
The octupole susceptibility (part A) uses the kernel's flat-CEF near-degenerate limit, giving a clean Curie 1/T growth (χ=220 @0.3 K, 22 @3.0 K). This supports an FO instability tendency but is a single-ion proxy, not the interacting mean-field T_O.

## 5. Honesty statement
No numbers were fabricated. Every reported value is emitted by `work/patri2018_replicate.py` into `patri2018_result.json`. The "REPLICATED" verdict reflects reproduction of the paper's central scaling relations and their symmetry origin; it is explicitly *not* a claim to have reproduced the material-specific magnitudes or the full phase diagram (see §2).
