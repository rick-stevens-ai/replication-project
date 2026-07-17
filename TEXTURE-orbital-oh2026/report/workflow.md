# Workflow — oh2026 (arXiv:2605.21124) model replication

## Environment
- **Language/stack:** Python 3 + NumPy (Matplotlib for figures). No GPU, no external DFT codes.
- **Host:** CPU (single core sufficient). Model target was nuc13; ran locally in ~1 s.
- **Wall time:** `elapsed_sec = 1.082` (from results.json).
- **Determinism:** fully deterministic (analytic 3×3 Bloch Hamiltonian, fixed 401-point k-grid).

## Steps
1. **Build the model.** Construct the 3×3 Bloch Hamiltonian of a single right-handed
   `3_1` helical chain: NN hopping `-t` along the helix; inter-cell hop carries the
   axial Bloch/screw phase `e^{ikc}` (flux-threaded 3-site triangle).
2. **Diagonalize** over `k ∈ (−π/c, π/c]`, 401 points → 3 bands E_n(k), eigenvectors.
3. **Itinerant OAM.** Form position operators `Y=diag(Y_j)`, `Z=diag(Z_j)` from the
   helix geometry; velocity `v_a = i[H(k), A]`; project
   `L_Itin = ½(Y v_Z − Z v_Y)` onto each band.
4. **Locking test (C2a).** Finite-difference `∂E/∂k` per band; compute per-band
   sign-match fraction and Pearson correlation vs `L_Itin`.
5. **Chirality flip (C2b).** Rebuild the LH chain by mirroring ONLY the azimuth
   (`φ_j → −φ_j`), keeping H(k) fixed; confirm E(k) degenerate and
   `L_L = −L_R` (flip correlation, fraction of k-points flipped).
6. **Emit** `results.json` (machine-readable verdicts) and 3 figures
   (`bands.png`, `oam_texture.png`, `chirality_flip.png`).

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-orbital-oh2026/work
python3 reproduce.py     # ~1 s, writes results.json + figs/*.png
```

## Key numbers (from results.json)
- 3 bands, bandwidth `4.0 t`; split over >99% of BZ (0.995 / 0.9975).
- OAM sign-match `1.0 / 1.0 / 1.0`; `|corr(L, dE/dk)|` = 0.998 / 0.999 / 1.000 (mean 0.999).
- Chirality flip: `L_L = −L_R` exactly (flip corr 1.00, 100% of k-points flip).

## Out of scope (not in this workflow)
- DFT+Wannier bulk-Te OAM (needs SM params + VASP + Wannier90 + post_wan).
- CD-ARPES / SARPES (synchrotron beamline experiments).
