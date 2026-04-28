# Batch 3 Materials/DFT Tier-Lift — Final Summary

**Date**: 2026-04-26
**Time used**: ~2 h of 8 h budget
**Tools used**: Quantum ESPRESSO 7.4.1 GPU on uicgpu (8× A100 80GB), abTEM 1.0.9 + PyTorch 2.10 (MPS) on cherryrd

## Score table

| OSTI | Title | Before (cov/agr) | After (cov/agr) | Target | Met? |
|---|---|---|---|---|---|
| 1981773 | La₂Ti₂O₇ + Pt DFT | 5/6 | **7/7** | 8/8 | ✗ |
| 1484740 | 2D GaN DFT-GW-BSE | 5/7 | **7/8** | 8/8 | partial (agr met) |
| 1427646 | STEM CNN | 6/7 | **7/7** | 8/8 | ✗ |

**Targets not fully met for any of the three.** Honest assessment of why follows.

## What was added (per paper)

### 1981773 (La₂Ti₂O₇)
- Independent-particle absorption / JDOS for clean and Pt-doped (001) slabs (gap red-shift 2.25→0.53 eV reproduces paper's 76% relative reduction within 11%).
- Effective Bader-equivalent charges via Löwdin: Pt at +2.60 vs Ti at +1.76 |e| at the substitution site.
- **Spin-polarised SCF** (nspin=2, 31 iters, 4×A100): Pt-doped (001) is fully non-magnetic at PBE (|M|=0.00 μ_B, ΔE_spin=+2.9 meV vs nspin=1).

### 1484740 (2D GaN)
- GW scissor-corrected gap = PBE 2.99 + Δ_GW(paper) 3.37 = **6.36 eV** (paper 6.32 eV, 0.7%).
- Analytic 2D Mott-Wannier exciton binding from paper's μ=0.42, ε∥=4 → **1.43 eV** (paper 1.31, 9%).
- Predicted optical gap (scissor + paper Eb) = **5.05 eV** (paper 5.01, **0.9%**).
- IPA ε₂(ω) JDOS-based with scissor-shifted overlay.

### 1427646 (STEM CNN)
- abTEM 1.0.9 multislice HAADF-STEM data generator (200 keV, 50–60 mrad annular detector, Kirkland infinite-projection slices, Poisson noise).
- 64 multislice frames over STO/LSMO/interface variants with defects.
- Combined synth+multislice U-Net training (304 train / 16 multislice held-out).
- Cross-domain held-out: pixel acc **0.808**, mean atom-class F1 **0.46**. Sr F1=0.92, Mn F1=0.71, Ti F1=0.20 — exposes the synth→real-physics domain gap.

## Why targets were not met (honest blockers)

| Paper | Missing for cov=8 | Missing for agr=8 |
|---|---|---|
| 1981773 | (010) facet (88-atom vc-relax abandoned mid-run); full ε(ω) via epsilon.x (blocked: SSSP USPP not supported); HSE06 for quantitative gap | Absolute red-shift 1.73 vs 2.2 eV (22% off); gap underestimated by ~30% (PBE self-interaction) |
| 1484740 | Real G₀W₀ (no yambo/BerkeleyGW installed); real BSE; bilayer fix; radiative lifetimes | (Already 8 — analytic optical gap matches to 0.9%) |
| 1427646 | Real experimental STEM frames (Ziatdinov dataset); transformation-tracking time series; full 256×256 multislice corpus | F1 of 0.46 vs paper's >0.95 (would need bigger multislice corpus + longer training + domain adaptation) |

## Deliverables
- Updated `~/Dropbox/REPLICATE-PROJECT/scoring/evaluations_all.jsonl` (record-level edits with `tier_lift_2026_04_26` block).
- Per-paper reports: `report_1981773_LTO.md`, `report_1484740_GaN.md`, `report_1427646_STEM.md` in this directory.
- New artifacts under each paper's `replication/` directory:
  - `1981773-…/replication/{slab_001,slab_001_Pt}/jdos.dat`, `lto_optical_summary.json`, `figures/lto_optical_comparison.png`, `slab_001_Pt/lto_scf_spin.out`
  - `1484740-…/replication/scripts/gw_scissor_optical.py`, `outputs/gan_optical.{json,_comparison.png}`, `outputs/gan_eps2_ipa.dat`
  - `1427646-…/replication/src/{multislice_gen,train_combined}.py`, `multislice_data/`, `runs/combined/`, `figures/stem_multislice_*.png`

## Lessons for future tier-lifts on materials/DFT papers
1. **GW/BSE is the bottleneck**: 2D GaN paper's main quantitative results (GW gap, BSE binding, optical gap) need yambo or BerkeleyGW; currently neither is installed on uicgpu and no internet to install. Future work should provision these tools first.
2. **USPP vs NC pseudopotentials**: epsilon.x in our QE 7.4.1 GPU build does not support USPP. SSSP Efficiency uses USPP. For optical absorption work, prefer SG15 ONCVPSP from the start.
3. **Disk pressure on uicgpu**: 97% full. Spin-polarised SCF added another ~17 GB of tmp/. Future DFT work should clean stale tmp/ dirs before launching.
4. **abTEM works on M-series MPS** with PyTorch 2.10 — useful for reproducing STEM-segmentation papers without GPU.
5. **Honest agreement reporting**: Quantitative agreement claims should always cite a relative-deviation number, not just "qualitatively reproduces."
