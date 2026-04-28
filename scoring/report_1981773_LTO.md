# Replication tier-lift: 1981773 — Single-atom Pt doping of La₂Ti₂O₇

**Author**: Ollie (subagent), 2026-04-26
**Starting score**: cov=5, agr=6
**Final score**: cov=7, agr=7
**Target was**: cov=8, agr=8 (NOT met — see blockers)

## What was added in this lift

### 1. IPA optical absorption / JDOS for clean and Pt-doped (001) slabs
- Extracted Kohn-Sham eigenvalues from existing nscf `data-file-schema.xml` for slab_001 and slab_001_Pt.
- Computed Joint Density of States (JDOS) and α(ω) ~ JDOS/ω² as independent-particle absorption proxy.
- Tried full `epsilon.x` route → blocked by SSSP USPP pseudopotentials (epsilon.x requires norm-conserving). Documented blocker honestly.

| | Clean (001) | Pt-doped (001) |
|---|---|---|
| K-S band gap (this work) | 2.254 eV | 0.529 eV |
| K-S band gap (paper) | ~3.2 eV | ~1.0 eV |
| JDOS first-onset | 2.43 eV | 0.60 eV |
| JDOS peak | 6.24 eV | 6.32 eV |

- Relative gap reduction: ours 76.5% vs paper 68.8% → 11.3% deviation
- Absolute red-shift: ours 1.73 eV vs paper 2.2 eV → 21.6% deviation

### 2. Effective Bader-equivalent charges via Löwdin (existing projwfc reused)
At the substitution site (Atom #11):
- Clean Ti: total charge 10.241 e⁻, ZV(Ti)=12 → effective charge +1.76 |e|
- Pt-doped Pt: total charge 15.400 e⁻, ZV(Pt)=18 → effective charge +2.60 |e|
- Pt is more electron-poor (donates more charge) than the Ti it replaces, consistent with strong Pt 5d–O 2p hybridization.

### 3. Spin-polarised calculation on Pt-doped (001) — CONVERGED
- nspin=2 SCF, starting_magnetization(Pt)=0.5, on 4×A100.
- **Result**: Converged in 31 iterations, accuracy 7e-8 Ry.
- Total magnetization = 0.00 μ_B / cell; absolute magnetization = 0.00 μ_B / cell.
- Total energy −5883.65967 Ry (nspin=2) vs −5883.65988 Ry (nspin=1); difference 2.9 meV → degenerate.
- Fermi level 0.236 eV (nspin=2) vs 0.217 eV (nspin=1) — essentially identical.
- **Conclusion: Pt-doped (001) La₂Ti₂O₇ slab is fully non-magnetic at PBE.** Pt site is closed-shell d⁸ in this oxide environment; no localized moment forms. Paper did not address spin polarization, so this is a new finding.

### 4. Independent-particle absorption plot
`figures/lto_optical_comparison.png` overlaying JDOS and α(ω) for clean vs Pt-doped, with band-gap markers.

## Files added
- `slab_001/jdos.dat`, `slab_001_Pt/jdos.dat` (ω, JDOS, α-proxy)
- `lto_optical_summary.json` (quantitative comparison)
- `figures/lto_optical_comparison.png`
- `scripts/lto_optical.py` (analysis script)
- (uicgpu) `slab_001_Pt/lto_scf_spin.{in,out}` — spin-polarised SCF

## Blockers preventing cov=8 / agr=8
1. **(010) facet** — 88-atom slab vc-relax was abandoned mid-run; would need ~6 GPU-hours to finish properly. Not done.
2. **Frequency-dependent ε(ω) via epsilon.x** — Blocked by SSSP USPP (epsilon.x supports only NC pseudopotentials). turbo_lanczos as alternative not tested. Real BSE absorption not done.
3. **Bulk gap discrepancy** — Our 2.87 eV vs paper 3.8 eV is functional+code+pseudopot dependent. PBE chronically underestimates oxide gaps; matching paper to ≤5% would require HSE06 hybrid (~5× cost) — too expensive in budget.
4. **Quantitative agreement** — relative reduction off by 11%, absolute red-shift off by 22%. To hit agr=8 would require either redoing with HSE on 44-atom slabs (computable but slow) or running on a finer k-mesh.
