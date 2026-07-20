# Workflow — replication of arXiv:1506.07172

## Steps executed

1. **Fetch/extract.** `paper.pdf` was pre-fetched. Extracted text with
   `pdftotext -layout paper.pdf paper.txt` (1245 lines). Read abstract, model
   section (II), mean-field derivation (Eqs. 1–33), results (III), conclusions
   (IV), and Appendix A (Γ-matrix definitions, Eqs. A1–A10).

2. **Classification check.** Compared against the routed class
   (loop-current *kagome tight-binding*) and the shared kernel
   `loop_current_kagome_kernel.py`. Determined this paper is a **square-lattice
   8-hot-spot spin-fermion model** of the cuprate CuO2 plane, NOT kagome. Logged
   the misclassification in `extraction/marker.md` and used the kernel only for
   *conceptual* provenance (real/imag = charge/current split; TRS breaking via
   the kinetic sector; free-energy minimization), cited in code.

3. **Claim selection.** Picked 5 machine-checkable claims (see marker.md):
   coupled MF solution exists; R_II↑ & b↓ with V_pd; b↑ & R_II↓ with λ;
   ratio R_II^c/V_pd^c ≈ 0.2; M_LC ≈ 0.19 μB.

4. **Model implementation.**
   - `code/hotspot_mft.py` — first attempt: full 24×24 linearized-hot-spot
     G⁻¹ from Appendix A with R_II via (γ₁,γ₂,φ,θ) and b via the QDW Σ₃ field.
     Vectorized batched `eigvalsh` over the BZ. This captures the Γ-matrix
     structure exactly but the two orders gapped *independent* sectors → no
     competition. Kept as documentation of the exact Appendix-A structure.
   - `code/hotspot_competition.py` — faithful **minimal competition model**:
     both orders open **anticommuting gaps on the same hot-spot fermion**, so
     `E_k = ±√(ξ² + gap_R² + gap_b²)` with the R_II form factor taken from the
     exact Appendix-A γ₁,γ₂ (Eqs. A9–A10) and a d-wave QDW form factor
     (cos kx − cos ky). Free energy uses the **verbatim Eq. 32 coefficients**:
     LC penalty R_II²/V_pd, QDW stiffness (8/3λ²)·⟨D_eff⁻¹⟩·b², constant
     −n_p²U_p/8. Electronic term = condensation energy (gapped − normal) with a
     hot-spot bandwidth cutoff Λ (the effective theory's UV cutoff).

5. **Solve & sweep.** `code/run_sweeps.py` minimizes F(R_II,b) coupled on a
   grid + Nelder–Mead refine, over two sweeps matching Fig. 4:
   (a) V_pd ∈ [4,24] at λ=20; (b) λ ∈ [8,32] at V_pd=14. Outputs
   `work/results.json`, `work/sweep_{Vpd,lam}.csv`, `work/fig4_replication.png`.

6. **Quantitative comparison.** Computed Pearson correlations of each order
   parameter vs the swept coupling (sign = trend direction), the critical
   ratio, and the M_LC estimate through the paper's own linear map.

7. **Robustness.** Re-ran the V_pd sweep at cutoffs Λ = 0.6, 1.0, 1.5 to confirm
   the competition signs are calibration-independent.

## Reproduce

```bash
cd code
python3 run_sweeps.py        # ~13 s; writes work/*.json,*.csv,*.png
python3 hotspot_competition.py   # single default-point solution
```

## Environment
- Python 3.13, numpy 2.4.3, scipy 1.18.0, matplotlib (Agg).
- No network, no paid endpoints. All computation local on CherryRd.
