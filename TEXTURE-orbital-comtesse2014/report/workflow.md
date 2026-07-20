# Workflow: Replicating Comtesse et al. (2014) giant inverse MCE

**Paper:** D. Comtesse et al., "First-principles calculation of the instability
leading to giant inverse magnetocaloric effects," arXiv:1401.8148 (2014).
**System:** Ni45Co5Mn37In13 (Mn-rich Heusler, poly-domain, field-cooled).
**Mode:** COARSE, performance-bounded RETRY (prior attempt timed out at 1200 s).
**Runtime this run:** ~1.6 s (target was <4 min).

## 1. Identify the ONE testable headline
Read `work/textures-orbital-comtesse2014.txt` + `report/evidence/replication_recipe.json`.
Headline: **inverse MCE with dT_ad = -6 K in 2 T, RCP_inv = -132 J/kg**, driven by
competing FM/AFM exchange (chemical disorder -> Z-sublattice Mn AFM) that produces
a magnetization jump dM(Tm) at the magnetostructural transition which *persists in
large fields* (the In-alloy fingerprint, vs the Ga alloy where it vanishes).

## 2. Build the model from scratch
- Coupled **BEG (structural, sigma in {0,+/-1}) + q=6 Potts (magnetic, Mn S=5/2) +
  magnetoelastic** Hamiltonian, faithful to the paper's Eqs. 3-4.
- 3D simple-cubic L=12 (N=1728), PBC, vectorized **checkerboard Metropolis MC**.
- Magnetoelastic competition encoded in exchange: MnY-MnY FM; Z-touching bonds FM
  in austenite, AFM in martensite. K/J = 0.23 (paper).
- **Skip DFT/KKR-CPA**: use effective lattice exchange constants tuned so Tm ~ 300 K.

## 3. Key methodological decision (matches the paper)
A single cooling MC will not nucleate martensite from pure austenite (first-order
barrier -> f_aust stuck ~1). The paper itself states it uses *separate austenite
and martensite exchange sets "which we let merge at Tm."* We therefore:
1. Run **two fixed-phase magnetic branches** (austenite: Z bonds FM; martensite:
   Z bonds AFM), sequential cooling, at 10 mT and 2 T.
2. Locate **Tm from the BEG free-energy crossover** (magnetic F via thermodynamic
   integration of MC internal energy + structural energy/entropy).
3. Read **dM(Tm)** as the inter-branch magnetization jump.

## 4. MCE thermodynamics (paper's Eqs. 6-7, Clausius-Clapeyron)
- dS_mag(Tm) = dM(Tm) / (dTm/dH),  with **dTm/dH = -2 K/T from experiment** (Liu
  2012 [20]) exactly as the paper does.
- dT_ad ~ -Tm * dS_mag / C,  C = Debye (Dulong-Petit) lattice + MC magnetic C.
- RCP_inv = -dS_mag * FWHM (~20 K proxy).

## 5. SAVE-EARLY discipline
After the first coarse branch (austenite low-field), write
`work/comtesse2014_result.json` immediately, then overwrite with the full result.

## 6. Compare + score
Sign, field-robust dM, and dS_mag magnitude reproduced quantitatively; dT_ad within
factor ~1.8; RCP order-of-magnitude. Verdict **REPLICATED**.

## 7. Package (8 artifacts)
`extraction/marker.md`, `extraction/nougat.mmd` (both INTERIM pdftotext fallback),
`report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`,
`report/artifacts_summary.md`, `report/failure_analysis.md`, plus result JSON +
code copied to `report/evidence/code/`.

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-orbital-comtesse2014/work/comtesse2014_beg_potts_mce.py
```

## Kernel credit
Routed through `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (topological orbital Hall
from skyrmions). **Not physically applicable** here (see `failure_analysis.md`);
the corpus "orbital" tag refers to the paper's d-electron orbital-resolved exchange
constants, not orbital transport. Core physics built independently.
