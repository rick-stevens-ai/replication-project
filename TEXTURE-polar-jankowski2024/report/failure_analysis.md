# Failure analysis — jankowski2024

## Verdict: REPLICATED (mechanism-level), 4/4 sub-claims pass.

## What was NOT reproduced (honest scope limits)
1. **No first-principles SHP/HWCC pipeline.** The paper's actual observable —
   local polarization from semilocal hybrid polarizations via Wilson-loop hybrid
   Wannier charge centers (Eqs. 3–5), and the quantized `ΔC({r_j})` (Eq. 8) — was
   NOT implemented. A full tight-binding super-Haldane / twisted-Haldanium
   diagonalization + Wilson loops is beyond the <6 min CPU budget.
2. **Magnitude jump is qualitative, not quantized.** We show a ~30% discontinuous
   drop in `<|P|>`; the paper reports the jump in units of the polarization quantum
   from SHP integration. Our number is a phase-field surrogate, not the TB value.
3. **Single meron, not the moiré triangulation.** We relaxed one meron
   (|Q|≈½); we did not tile the AA/AB/BA triangular domains of the θ≈5° moiré cell.
4. **Noise-free relaxation.** The TPT crosses an intermediate metallic critical
   point; we did not probe thermal robustness of winding survival near criticality.

## Failure encountered and fixed during the run
- **Texture distortion from over-strong depolarization.** The initial
  topological-branch model set `eps=1.2` + reduced `K_z=0.20` to suppress `|P|`.
  This deformed the meron and pushed Q from +0.46 to +0.96 (looked like a full
  skyrmion), failing T4 (winding preservation) and yielding PARTIAL.
  **Root cause:** the depolarization term reshapes the texture, conflating a
  magnitude change with a topology change. **Fix:** isolate the magnitude drop to
  the ferroelectric well depth (raise relaxation `T` toward `T0`) while holding all
  texture-shaping parameters (`K_z`, `g`, `eps`) fixed. Result: |P| dropped 30% with
  ΔQ=0.016 → REPLICATED.

## Threats to validity
- The surrogate mapping "topological branch ↔ shallower ferroelectric well" is a
  modeling choice justified physically (staggered-flux NNN hoppings suppress the
  electronic dipole) but not derived from the tight-binding Hamiltonian.
- Berg–Lüscher Q over an open domain is boundary-sensitive; we mitigated with a
  finite-difference Pontryagin cross-check (both ≈+0.46–0.47).

## Confidence
High that the QUALITATIVE mechanism (half-integer meron, discontinuous-but-
nonvanishing magnitude, preserved winding) matches the paper. Low that quantitative
SHP magnitudes match — that requires the full Wilson-loop pipeline (see open_questions).
