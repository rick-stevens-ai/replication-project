# JOB_PLAN — heavy Monte Carlo reproduction (NOT executed on CherryRd)

## Goal

Reproduce Hartzell et al. 2025 (DOI 10.1667/rade-24-00164.1) Figs. 2–6 and Tables 1–2
numerically: per-fragment α, β, microdosimetric spectra (z*, y*), DNA double-strand
break yields, and dose-averaged RBE for monoenergetic and SOBP carbon beams in a water
phantom, for all four RBE models (MKM, SMKM, RMF, LEM-I).

## Compute target

**uicgpu** (preferred) — 8× A100, 2 TB RAM, CUDA, interactive. Reasons:

- TOPAS is CPU-bound; uicgpu has 96+ cores.
- Geant4-DNA scoring produces large phase-space files; `/data` (14 TB NVMe) absorbs this comfortably.
- No queue → fast iteration on geometry tuning.

**Alternative:** Aurora (PBS `datascience` or `AuroraGPT` allocations). CPU-only TOPAS
queue jobs, 1–6 nodes × 104 cores Xeon Max each. Better for the final 4×4 matrix
production run.

**Forbidden:** CherryRd. M-series CPU + 16 GB RAM is wholly inadequate.

## Software stack

| Tool | Version | Purpose |
|---|---|---|
| TOPAS | ≥ 3.9 | Carbon beam transport + scoring |
| Geant4 | 11.2.x | Backend physics |
| Geant4-DNA | 11.2.x | Microdosimetric spectra (z*, y*) |
| TOPAS-nBio | latest | DSB yield scoring |
| Python | 3.11 + numpy + scipy | RBE-model post-processors |
| paramonte / emcee | optional | parameter uncertainty bands |

Install via spack on uicgpu; estimated build + validation 1 day.

## Geometry / sources

- Water phantom 40 × 40 × 40 cm³, voxel 1 × 1 × 1 mm³.
- Monoenergetic beams: 195, 290, 380, 430 MeV/u (Hartzell's likely choices; verify against article when available).
- SOBP: ridge-filter or weighted-pencil-beam modulator giving 4–6 cm modulation centered at 12 cm.
- Score in three regions: entrance plateau (3 cm), mid-SOBP, fragmentation tail.

## Scoring

Per fragment (H, He, Li, Be, B, sec C, prim C, e⁻, other):
1. Physical dose contribution (Gy per primary, Bragg curve).
2. Kinetic-energy spectrum.
3. Microdosimetric spectrum (z*, y*) in 1 µm scoring volume.
4. DSB yield (Geant4-DNA).

## RBE-model post-processing (Python)

For each model the published references give a deterministic formula taking the
scored spectra as input:

- **MKM:** Hawkins 1996; Kase 2008. Needs z*_d.
- **SMKM:** Sato & Furusawa 2012. Needs z*_d and z*_n.
- **RMF:** Carlson 2008; Frese 2012. Needs z_F and DSB yield.
- **LEM-I:** Scholz & Kraft 1996; Krämer & Scholz 2000. Needs LET spectrum and reference SF curve.

All four reduce to per-fragment (α_p, β_p); combine via dose-weighted LQ-additive
damage to get total (α_mix, β_mix) per voxel/region. RBE_{2 Gy} = D_x / D from the LQ
equivalence.

## Reference radiation

α_x and β_x for the relevant tissue/cell line. Hartzell almost certainly uses HSG
(α_x = 0.13 Gy⁻¹, β_x = 0.05 Gy⁻²) or similar; this is a controllable variable.

## Validation

- Reproduce Bragg peak depth ± 1 mm vs published carbon-SOBP data.
- Reproduce fragment dose fraction > 30 % at mid-SOBP (already shown qualitatively in our smoke).
- Reproduce per-fragment α, β at HSG reference to within 10 % of published values
  for each of the four models (cross-checked against open primary refs).

## Estimated cost

- 1 monoenergetic beam, full scoring: ~6 h × 32 cores ≈ 200 core-hours.
- 4 energies × 3 regions × ~10⁹ primaries: ~2–3 days wall clock on 64 cores.
- 4 model post-processors: minutes (Python).

## Storage

- Raw phase-space: ~200 GB. Place on `/data/stevens/scratch/hartzell-2025/` (uicgpu).
- Compressed final results + figures: ~5 GB. Sync to Dropbox/XFER/ for delivery.

## Deliverables (if requested)

- `figures/fig2_bragg_dose_decomp.png` (per-fragment Bragg curve)
- `figures/fig3_fragment_LET_spectra.png`
- `figures/fig4_per_fragment_RBE_4models.png`
- `figures/fig5_total_RBE_vs_depth.png`
- `tables/per_fragment_alpha_beta.csv` (~2 MB)
- `tables/RBE_4models_3regions.csv`
- A short markdown comparing our reproduced numbers to Hartzell's published values
  (requires obtaining the article body first).

## Status

**Not executed.** First-pass smoke replication (open-equation, qualitative) completes
the LUCID100 acceptance criteria for slot 39.
