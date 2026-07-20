# Workflow — You et al. 2021 replication

## Goal
Reproduce the central theory claim of You et al. 2021: an out-of-plane spin
polarization σz (from the cluster magnetic octupole of Mn3SnN) drives field-free
deterministic SOT switching of a perpendicular ferromagnet, with polarity set by
current sign, and this vanishes when σz is absent (J⊥T).

## Steps
1. **Read** `report/evidence/replication_recipe.json` and `work/textures-multipolar-you2021.txt`
   (678-line plaintext). Identified method = experiment (ST-FMR/SOT), but with a
   symmetry-defined theory core (Eq.1, torque decomposition τ_B, τ_C).
2. **Classify**: not pure experiment-only — the σz antidamping-torque → field-free
   switching mechanism is reproducible via macrospin LLG. Proceed to PARTIAL replication.
3. **Build** `work/you2021_llg.py`: single-macrospin LLG (RK4), uniaxial PMA along z,
   Gilbert α=0.1, zero external field. SOT enters as τ_DL·m×(m×p) + τ_FL·m×p with
   amplitudes scaled from paper ratios θ_AD,z=0.003, θ_FL,z=0.053.
4. **Two configurations**:
   - Case A (J‖T): p ≈ ẑ (σz present).
   - Case B (J⊥T): p = ŷ (σz absent, only σy).
   Determinism test: init both up and down; final must depend only on current sign.
5. **Run** with `/home/stevens/comfyui-env/bin/python`, <10 s. SAVE-EARLY to
   `work/you2021_result.json`.
6. **Compare**: Case A deterministic (up/down both → down for +I, up for −I);
   Case B non-deterministic (state tracks init). Matches Fig.4c vs 4f control.
7. **Package** 8 artifacts (extraction ×2, report ×5, evidence copies).

## Tools
- Physics runner: `/home/stevens/comfyui-env/bin/python` (numpy).
- No source PDF present; plaintext used directly as extraction of record.

## Reproduce
```
cd /home/stevens/textures-100/corpus/textures-multipolar-you2021/work
/home/stevens/comfyui-env/bin/python you2021_llg.py
```
Output: `you2021_result.json` (also copied to `report/evidence/`).
