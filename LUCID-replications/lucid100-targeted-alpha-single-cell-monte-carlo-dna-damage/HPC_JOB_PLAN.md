# HPC_JOB_PLAN — Slot 41 full TOPAS-nBio reproduction

**Goal:** reproduce the full Jolly & Fielding 2025 targeted-alpha single-cell dosimetry and DNA-damage simulations.

## Why not CherryRd

The full paper uses OpenTOPAS 3.9 + TOPAS-nBio on Geant4 v11.1 / Geant4-DNA with track-structure scoring in a microscopic nucleus. The campaign is approximately:

- 4 radionuclides: Ac-225, Ra-223, Pb-212, At-211
- 4 source localizations: cell wall, cytoplasm, nucleus wall, nucleus volume
- 2 physics configurations: condensed-history opt0 and Geant4-DNA in nucleus
- 20 independent repeats
- 100 radionuclides per repeat

That is roughly 640 high-cost configuration/repeat jobs before parameter sweeps or debugging, and track-structure scoring is expensive.

## Preferred target

Use `uicgpu` or Aurora only after a small install/test job. For uicgpu, keep heavy work under `/data/stevens/projects-active/` and source `~/env.sh` for network access.

## Steps

1. Build or load Geant4 v11.1 with data libraries.
2. Build OpenTOPAS 3.9 and TOPAS-nBio extensions.
3. Create the two-sphere geometry: cell radius 10 µm, nucleus radius 5 µm, 30 µm water box.
4. Implement four source distributions and radionuclide decay chains.
5. Configure scorers:
   - `DoseToMedium` in nucleus, total and alpha-filtered;
   - `SurfaceTrackCount` at nucleus surface;
   - TOPAS-nBio DBSCAN clustered DNA damage scorer.
6. Run a smoke subset first: At-211, nucleus source, g4em-dna, 2 repeats.
7. Scale to all radionuclides/source localizations/physics lists/repeats.
8. Compare Table 2 cGy/decay and DSB summaries; save raw scorer dumps for reproducibility.

## Expected outputs

- per-repeat scorer CSVs
- aggregate Table 2 reproduction CSV
- DSB/sDSB/cDSB summaries
- run environment manifest with Geant4/OpenTOPAS/TOPAS-nBio commits or versions

## Notes

No author contact. No paid endpoints. Full rerun is compute/setup-gated, not scientifically blocked.
