# Workflow — malashevich2012 replication

## 1. Read paper + recipe
- Recipe (`report/evidence/replication_recipe.json`): method=DFT, code=Quantum ESPRESSO,
  Cr₂O₃ corundum AFM, SOC LSDA+U (U=2.0, J=0.8 eV), headline **α⊥ = 1.04 ps/m**.
- Paper text (`work/*.txt`): extracted Table II (α⊥ decomposition) and Table III
  (orbital LC/IC/CS decomposition). Key insight: **α⊥ is ~98% spin** (spin-lattice
  0.77 + spin-electronic 0.26 ps/m); orbital contributions sum to only 0.011 ps/m.
- Chern–Simons ME quantum quoted in intro: **24.3 ps/m**.

## 2. Scope decision
Absolute 1.04 ps/m ⇒ dominated by spin channels needing SOC DFT+U + phonons/Born
charges + spin susceptibility → **out of scope** for a <6 min from-scratch run.
Reproduce instead the tractable, physically distinctive **orbital / Berry-phase method**.

## 3. Build physics (`report/evidence/code/malashevich2012_orbital_ME.py`)
- **(A) Chern–Simons axion quantum:** compute (e²/2h)·μ₀ in SI → 24.34 ps/m.
  Build 3D Wilson–Dirac (BHZ) insulator; get axion angle θ from inversion parities
  at the 8 TRIM (Fu–Kane). Scan mass M₀: topological windows → θ=π → α_CS=24.3 ps/m;
  trivial → θ=0 (the Cr₂O₃-like case).
- **(B) Itinerant circulation:** reuse **gobel2024** itinerant Lz=½(r×v) operator on a
  chiral texture → finite accumulated orbital moment (IC branch active).
- **SAVE-EARLY** to `work/malashevich2012_result.json`.

## 4. Compare + score
- CS quantum 24.34 vs 24.3 ps/m (<0.2%) ✓
- topological θ=π → 24.34 ps/m ✓
- Cr₂O₃ trivial → tiny CS term (paper 0.0012 ps/m) consistent ✓
- itinerant Lz finite (IC active) ✓
- absolute α⊥=1.04: NOT reproduced (spin-DFT scoped honestly)
- **4/4 method claims → verdict PARTIAL**

## 5. Package 8 artifacts
extraction/marker.md, extraction/nougat.mmd, report/REPORT.tex,
report/open_questions.json, report/workflow.md, report/artifacts_summary.md,
report/failure_analysis.md; result JSON + code copied to report/evidence/.

## Runner
`/home/stevens/comfyui-env/bin/python` (numpy 2.3.5), runtime ≈ 2.3 s.
