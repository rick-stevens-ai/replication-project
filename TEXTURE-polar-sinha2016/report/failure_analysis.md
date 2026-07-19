# Failure Analysis — Sinha 2016 replication

Everything that could have silently produced a *wrong* "replicated"/"failed"
conclusion, and how each was caught or avoided.

## 1. The symmetry-angle trap (the big one)
**Symptom risk:** The angle of deviation `δω(θ) = arccos[−ak sin3θ / √(1+a²k²−2ak cos3θ)] − π/2`
is proportional to `sin(3θ)`. It is therefore **identically zero at every
multiple of 60°** — θ = 0°, 60°, 120°, 180°, … — *for any* value of `a`,
including the broken-locking Floquet case.

**How it bites:** A naive angular grid `[0, 60, 120, …]` (the "obvious" hexagonal
sampling) returns `δω = 0` everywhere and would make the Floquet case look
*identical* to the gapless locked case → false conclusion "spin-momentum locking
NOT broken" → false FAILED verdict.

**Fix / guard:** Always sample **off-symmetry angles** (30°, 45°, 90°). The grid
used includes `[0, 30, 45, 60, 90, 120]°`, giving
`δω(a=0.55) = [0, 0.294, 0.174, 0, −0.294, 0] rad` — clearly nonzero off the
symmetry lines, zero on them, exactly as the paper describes (δω=0 only along
Γ–K and θ=π/3). The `a=0` control returns all zeros, confirming the contrast is
real and not a numerical artifact.

## 2. `a`-prefactor: fit vs. first-principles (honest gap, not a failure)
`Δω=(evA0)²/ħω` is exact. But `a = 4αβ/(ħ²ωv)` needs a bare `v`, which the paper
never gives (it only fixes the product `ħv`). Had we *pretended* to derive `a`
first-principles we would have been fabricating a number. Instead we flagged it:
empirical calibration `a ≈ 0.68·(evA0)² nm` hits the paper's 0.17/0.55 nm, and
the functional form `a ∝ (evA0)²` is correct. Documented as an honest gap, not
hidden.

## 3. `k=0` singularities in spin formulas
Eqs. 9–11 have `E_s + Δ` in denominators and `Cs²` normalization that are
`0/0`-indeterminate exactly at `k=0`. Evaluating literally at the Dirac point
throws divide-by-zero. **Guard:** evaluate at `k → 0` via small offset
(`1e-6`–`1e-9`) and use `np.errstate` to suppress spurious warnings; the limits
(`Sz→+1` gapped, `Sz→0` gapless) are stable and match the paper.

## 4. Conduction- vs. valence-band eigenvector selection
`numpy.linalg.eigh` returns eigenvalues in ascending order, so the conduction
band (`s=+1`) is column index **1**, not 0. Picking the wrong column flips the
sign of every spin component and would corrupt the analytic-vs-numeric spin
cross-check. Verified by matching `eigvalsh[1]` to the `s=+1` analytic energy;
the resulting spin max-error of `0.0` confirms the correct branch was used.

## 5. Warping cubic sign / θ convention
`Δ(k,θ) = λ k³ cos3θ = λ(kx³ − 3kx ky²)`. A sign slip or `sin↔cos` swap in the
cubic term would misplace the Sz sign domains and the δω nodes. Cross-checked by
requiring the analytic Eq.-6 energy to equal the direct diagonalization of the
Eq.-5 matrix over the whole 25×25 grid → max error `0.0 eV`, which pins down the
convention unambiguously.

## 6. Extraction-tool absence (avoided a silent quality drop)
`marker` and `nougat` are not installed. Rather than emit empty/garbled files,
`pdftotext -layout` was used and the equations hand-normalized into
`extraction/marker.md` and `extraction/nougat.mmd`, each with an explicit banner
stating the provenance. No fabricated "neural OCR" output.

## What did NOT fail
- Gap magnitudes (`2Δω`) match the paper to the quoted precision.
- Analytic ↔ numeric agreement is at machine precision for both energy and spin.
- The gapless control (`a=0`) behaves as a proper locked TI everywhere,
  isolating the light-induced effect.
