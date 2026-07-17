# Workflow — wang2026 (arXiv:2607.15228)

**Paper:** Magnetic Order in bilayer Ruddlesden-Popper Nickelates (La3Ni2O7)
**Texture class:** orbital (orbital-selective correlation-driven magnetism)
**Verdict:** PARTIAL

## Environment
- **Language / stack:** Python 3, pure **NumPy** + **SciPy** (eigensolves), Matplotlib (figures).
- **No GPU, no DFT SCF, no external packages beyond numpy/scipy/matplotlib.**
- **Host:** CPU only. Recommended nuc13 (CPU); actually reproducible on any laptop.
- **Runtime:** seconds (~minutes including figure rendering). Trivial cost.

## Pipeline (as implemented in `work/reproduce.py`)
1. **Model setup** — J_perp-J1-J3(-J1') bilayer Heisenberg model with neighbor
   definitions from SM Eq.(S14):
   - J1 = intralayer R=(1,0), J2 = intralayer R=(1,1) [=0], J3 = intralayer R=(2,0),
   - J_perp = interlayer R=(0,0), J1' = interlayer R=(1,0).
   - Stated values (U=4 eV, x S): J_perpS=75, J1S=1.9, J3S=4.6, J1'S=1.38 meV.
2. **Fourier transform** of exchange → J_intra(q), J_inter(q) → 2x2 bilayer J(q) matrix.
3. **C3 — ordering vector:** Luttinger-Tisza (min of lower eigenvalue of J(q) over BZ)
   + diagonal (q,q) refinement → Q = (0.509π, 0.509π).
4. **C4 — frustration:** sweep J3/J1, record Q(J3/J1) → monotonic shift
   (fig `Q_vs_J3overJ1.png`).
5. **C5 — spin waves:** linear spin-wave theory (Holstein-Primakoff, bosonic
   Bogoliubov diagonalization) along (π/4,π/4)-(3π/4,3π/4) through Q →
   acoustic + optical branches (fig `spinwave_dispersion.png`).
6. **Luttinger-Tisza map** rendered as `luttinger_tisza_map.png`.

## Outputs
- `work/results.json` — claim-by-claim numbers (Q, J3/J1, bandwidth, branch count, softening).
- `work/dispersion.json` — full acoustic/optical branch arrays vs k along the path.
- `work/figs/{spinwave_dispersion,Q_vs_J3overJ1,luttinger_tisza_map}.png`.

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-orbital-wang2026/work
python3 reproduce.py            # writes results.json, dispersion.json, figs/
```

## Out of scope (C1/C2)
Full slave-spin Z_alpha(U) + Lindhard chi(q) + RKKY derivation of the J values
requires the DFT-derived tight-binding hoppings of Ref[49] (Liao PRB 114,045112),
which are not tabulated in this paper. Those steps would add: slave-spin mean-field
solver (Yu-Si), dense-k Lindhard susceptibility, real-space FT of RKKY — still CPU,
hours-scale, but blocked on the external hopping table.
