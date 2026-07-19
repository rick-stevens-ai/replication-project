# Workflow — TEXTURE-orbital-ederer2005

## Target
Ederer & Spaldin, *Recent progress in first-principles studies of magnetoelectric
multiferroics*, arXiv:cond-mat/0512330 (2005). **Review article**, texture class:
orbital, method class: first-principles DFT (review).

## Challenge
A review has no single novel result and everything cited is DFT-heavy (LSDA+U,
Berry-phase, DFPT) — a poor stand-alone replication target as flagged in
`method_extract.md`. Strategy adopted: extract the review's **machine-checkable
physics claims** and reproduce each with the **minimal model carrying the physics of
the cited work** (the same model classes the review's own references used), running
real tractable code rather than faking DFT.

## Steps executed
1. Read `paper.pdf` (via prior pdftotext extraction in `extraction/marker.md`) +
   `report/method_extract.md` + `META.json`. Identified 5 concrete claims.
2. Implemented one Python script per claim under `code/`, run under `work/`:
   - `claim1_polarization_quantum.py` → BiFeO3 quantum eR/V vs 185.6 uC/cm^2 (Fig.1)
   - `claim2_berry_phase_polarization.py` → Rice-Mele KSV Berry phase (Sec.2 modern
     theory of polarization; quantization + odd switching path = Fig.1)
   - `claim3_d0_rule.py` → 2-level vibronic (pseudo-JT) d0 double-well vs d1/d2
   - `claim4_ymno3_improper.py` → Landau K3+Gamma2- improper-FE model (Sec.3.1)
   - `claim5_bifeo3_canting.py` → J+DM two-sublattice canting → 0.1 uB/cell (Sec.3.2.3)
3. Captured stdout to `work/claim*_out.txt`; aggregated `work/results_summary.json`.
4. Wrote 8-artifact bar in `report/`.

## Environment
- python3 3.x, numpy 2.4.3, scipy 1.18.0 (host CherryRd). No network, no DFT, no
  external endpoints used. All deterministic; re-running reproduces identical numbers.

## Reproduce
```
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-orbital-ederer2005
for i in 1 2 3 4 5; do python3 code/claim${i}_*.py; done
```
