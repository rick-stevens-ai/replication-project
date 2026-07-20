# Extraction — You et al. 2021 (Mn3SnN cluster octupole σz)

**Title:** Cluster magnetic octupole induced out-of-plane spin polarization in antiperovskite antiferromagnet
**Authors:** Yunfeng You, Hua Bai, Xiaoyu Feng, Xiaolong Fan, Lei Han, Xiaofeng Zhou, Yongjian Zhou, Ruiqi Zhang, Tongjin Chen, Feng Pan, Cheng Song (Tsinghua Univ. / Lanzhou Univ.)
**Corresponding:** songcheng@mail.tsinghua.edu.cn

## Extraction method
- Source: `work/textures-multipolar-you2021.txt` (pre-existing `pdftotext`-style plaintext, 678 lines). No source PDF present in the corpus dir, so the plaintext is the extraction of record.
- `marker.md` = this file (structured Markdown extraction + header). `nougat.mmd` = math-flavored interim capture of key equations/claims.

## Headline claim
Field-free deterministic SOT switching of an adjacent perpendicular ferromagnet (Co/Pd)3 is realized using out-of-plane spin polarization **σz** generated in noncollinear AFM Mn3SnN. σz appears when charge current **J // cluster magnetic octupole moment T**, and vanishes when **J ⊥ T**.

## Key physics (theory-reproducible part)
- σz ∝ **H_so × T**   (Eq. 1). Carrier spins (along T) precess about spin–orbit field H_so ⟂ J. When T‖J, spins ⟂ H_so → robust σz; when T⟂J, spins ‖ H_so → no precession → σz = 0.
- SOT torque decomposition on FM (m):
  - σy conventional antidamping: τ_S ∝ m×(m×σy)
  - σz field-like: **τ_B ∝ m×σz**
  - σz antidamping (out-of-plane): **τ_C ∝ m×(m×σz)**  ← this term enables field-free deterministic switching of a PMA magnet.
- Measured spin-torque ratios (ST-FMR, Mn3SnN/Py): θ_AD,z = 0.003 ± 0.001; θ_FL,z = 0.053 ± 0.005.

## Key experimental parameters
- (110)-oriented Mn3SnN on MgO(110); epitaxy MgO(110)[100]//Mn3SnN(110)[100]; a_out = 3.98 Å.
- Mn:Sn:N = 3:0.94:1.03; Ra = 0.199 nm; T_N = 475 K (highest in Mn3AN family).
- Γ4g noncollinear AFM order (confirmed via AHE at 300 K & 100 K).
- ST-FMR: 2–17 GHz, rep. 5 GHz, 20 dBm, φ=45°(Kittel)/100°(spectrum), J along [001].
- Switching stack: MgO/Mn3SnN(12 nm)/(Co0.4/Pd0.8)×3; pulse 1 ms; J_crit ≈ 9×10^6 A/cm².
- Control: J along [110] (⟂T) → no field-free switching hysteresis.

## Reproducibility assessment
Primarily an experimental thin-film/ST-FMR/SOT-device paper. **However** the central mechanistic claim (σz antidamping torque → field-free deterministic switching; polarity set by current sign; absent when σz=0) is a symmetry-defined *theory* result reproducible with a macrospin LLG model. That is what this replication builds.
