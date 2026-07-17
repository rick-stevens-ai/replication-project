# Workflow — göbel2024 (arXiv:2410.00820) replication

**Paper:** Topological orbital Hall effect caused by skyrmions and antiferromagnetic skyrmions (Göbel, Schimpf, Mertig, 2024).

## Environment
- **Language / stack:** Python 3, pure `numpy` (linear algebra) + `matplotlib` (figure only). No scipy, no GPU, no external solvers.
- **Host:** CPU (single machine). No cluster, no MPI.
- **Runtime:** ~229 s (~4 min) total for the full λ∈{2,3,4,5} sweep including FM-background baselines.
- **Deps present:** numpy, matplotlib (both already installed).

## Steps
1. **Method extraction** — `extraction/marker.md` (clean pdftotext; full Methods with Eqs. 1–11) → `report/method_extract.md`. The marker pass was unusually complete (all transport equations present); nougat unnecessary.
2. **Model build** (`work/reproduce.py`):
   - Spinful s-electron square lattice, dim = 2·L² = 1568 for L=28.
   - Hamiltonian `H = -t Σ⟨ij⟩ c†c + m Σ c†(n·σ)c`, **no SOC**.
   - Néel skyrmion texture `θ(r)=π·exp(-r/λ)` at radius λ.
3. **Exact diagonalization** (T=0, clean) of the dense 1568×1568 Hermitian H.
4. **Kubo / Berry-curvature Hall sums** for charge (TKNN), spin (O=Sz), orbital (L_z=½(X v_y − Y v_x), v=i[H,R]).
5. **FM-background subtraction** — recompute each response for the uniform ferromagnet (n=+ẑ) at equal occupied count and subtract, isolating the texture-induced (topological) part. Essential: raw orbital background ~1e5 swamps the signal.
6. **Scaling sweep** — repeat for λ∈{2,3,4,5} at the SAME low-filling minigap (nocc=69, μ≈−7.95t, filling≈0.044) for apples-to-apples size comparison.
7. **Outputs** — `work/results.json` (per-λ numbers + per-claim verdicts), `work/figs/scaling.png` (σ vs λ), console summary.
8. **Report** — this write-up phase: `report/REPORT.{tex,pdf}` + JSON/MD artifacts. No recompute.

## Reproduce
```
cd work && python3 reproduce.py    # writes results.json, figs/scaling.png; prints summary
```

## Notes
- Single skyrmion in a fixed finite cell (not a skyrmion-crystal supercell) — chosen for speed; consequence: no global charge gap → charge Hall ≈0 (see failure_analysis.md).
- All numbers are FM-subtracted texture-induced values; a.u. as in the paper.
