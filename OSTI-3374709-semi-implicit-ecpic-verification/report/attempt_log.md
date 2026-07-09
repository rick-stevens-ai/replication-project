# Attempt Log

1. Read WAVE_BRIEF_2026-07-01.md + OSTI100_TOPUP50 TSV; listed existing OSTI-* dirs to skip.
2. Ranked undone candidates. Fetched three OA PDFs (rank 4 3374709, rank 7 2448207, rank 3 3020556)
   via `ssh uicgpu` proxy (CherryRd times out on osti.gov). pdftotext each; scanned abstracts + keyword
   grep (dispersion/convergence/analytic/exact).
3. **Picked OSTI 3374709** (rank 4, "Verification of an energy-conserving semi-implicit ES-PIC"):
   it is a *verification* paper with a clean, self-contained ANALYTIC target — the SIPIC plasma-frequency
   down-shift `ωpe/√(1+C_SI·ωpe²·Δt²/4)` (Eqs. 12/16) — reproducible with a small from-scratch PIC, no
   proprietary data, no heavy compute. Non-colliding target dir confirmed via `ls`.
4. Extracted Eqs. 5–18 + Table I parameters (C_SI=4, a∈{0.5,1,2,4,8}).
5. Wrote `sipic_dispersion.py`: 1D ES-PIC (leapfrog, CIC deposit/gather, spectral Poisson), SIPIC
   effective dielectric in the field solve; seed cold Langmuir mode; FFT the mode's E-field to get ω.
6. **Bug 1 (diagnostic):** first runs measured ω/ωpe ≈ 2.0 for classical validation. Cause: I recorded
   `|E_k|` (magnitude), which folds the sinusoid and doubles the apparent frequency. Fix: record the
   SIGNED real part of the complex Fourier coefficient. Validation then → ≈1.0. (Logged to failure-log.)
7. **Bug 2 (sign of the dielectric):** SIPIC runs *up-shifted* ω instead of down-shifting. Cause: I set
   `eps_eff = eps0·κ` with κ=1/(1+…) < 1, which strengthens E. The physical field operator (Eqs. 9-10)
   multiplies the Laplacian by `(1+C_SI·ωpe²·Δt²/4)` = an ENLARGED permittivity → weaker E → down-shift
   (Eq. 16). The paper's Eq.12/13 bookkeeping (κ=1/F, ω²=ωp²/κ) is internally inverted vs the stated
   Eq.16 result; I implemented the physical operator directly. Fix: `eps_eff = eps0·(1+C_SI·ωpe²·Δt²/4)`.
   All cases then tracked the down-shift.
8. **Bug 3 (FFT peak):** a=1.0 case picked a spurious near-DC drift peak (slow particle-noise heating).
   Fix: restrict `measure_freq` to a physical band [0.3×pred, min(3×pred, 0.98×Nyquist)]. a=1.0 → 0.9% err.
9. Final sweep (C_SI=4): measured ω/ωpe = 0.731/0.451/0.252/0.126/0.069 vs Eq.16 pred
   0.707/0.447/0.243/0.124/0.062 → errors 3.3/0.9/3.9/1.9/10.2 %. Classical validation → 1.03/1.01/1.02.
10. LLM-judge (free Argo `argo:gpt-5.2`, temp 0): verdict **REPLICATED**.
11. Wrote plot (matplotlib) + all report files. Light compute — ran locally (≈30 s total).

## Compute used
- OA PDF fetch + pdftotext: `ssh uicgpu` (proxy). Everything else: local NumPy/matplotlib on CherryRd.
- LLM: Argo proxy localhost:44497, model argo:gpt-5.2 (free). No paid endpoints.
