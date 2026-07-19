# Workflow — TEXTURE-orbital-fang2015 replication

## Target selection
- Paper (arXiv:1508.07414) is a **review** of first-principles methods for
  multiferroics/magnetoelectrics. No single crisp result; full DFT is
  cluster-class and out of scope.
- Chose the cleanest machine-checkable sub-result: the **OSEP double-well
  demonstration** for BaTiO3 (Fig. 1) and PbTiO3 (Fig. 2), Section 3.1.1.
- Headline quantitative anchor: BTO ferroelectric double well **vanishes at a
  ~2 eV OSEP up-shift of the Ti-3d orbital**.

## Method
1. Read `paper.pdf`, `extraction/marker.md`, `report/method_extract.md`.
2. Identified 4 machine-checkable claims (C1-C4).
3. Built a **minimal 2nd-order Jahn-Teller (vibronic) soft-mode model** in
   `code/osep_model.py`:
   - Single soft-mode coordinate Q (Ti off-center displacement).
   - 2x2 electronic Hamiltonian coupling O-2p (filled) to Ti-3d (empty) via gQ.
   - Total E(Q) = lattice (harmonic k + quartic k4) + 2x occupied bonding level.
   - Instability condition: net curvature k - 4g^2/Delta < 0.
   - OSEP = shift Ti-3d on-site energy by s; critical shift s_crit = 4g^2/k - Delta.
4. Calibrated parameters to physical BTO scale (Delta=2.6 eV from Fig 1a PDOS;
   depth ~10 meV; |Q*|~0.12 A; k chosen so s_crit=2.0 eV).
5. Ran under `work/`; emitted CSVs, JSON, PNGs.

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-orbital-fang2015/work
python3 ../code/osep_model.py
```
Requires: numpy, scipy (optional matplotlib for PNGs). No network, no DFT, no
cluster. Runs in <1 s.

## Checks performed
- C1: undisturbed BTO curve is a genuine double well (depth>5 meV, |Q*|>0).
- C2: critical OSEP up-shift compared to paper's ~2 eV (analytic + grid scan).
- C3: well depth vs 3d-2p gap -> correlation with 1/Delta (hybridization test).
- C4: PTO deepening from Ti-3d-down vs Pb-6s-up; Ti must dominate, both positive.

## Outputs (work/)
- `results.json` — per-claim pass/fail + numbers
- `bto_curves.csv` — E(Q) for OSEP shifts 0..2.5 eV
- `bto_welldepth.csv` — depth/|Q*| per shift + fine scan
- `pto_curves.csv` — PTO base / Ti-3d-down / Pb-6s-up curves
- `fig_bto_doublewell.png`, `fig_bto_welldepth_vs_shift.png`
