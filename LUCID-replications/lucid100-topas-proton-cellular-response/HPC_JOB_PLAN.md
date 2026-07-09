# HPC Job Plan — Full reproduction of Zhu et al. 2020 TOPAS-nBio Table A2

This is the plan we would execute on **uicgpu** or **Aurora** if/when we want
to reproduce the damage-induction stage of Zhu et al. 2020 from scratch. It
is **not** to be run on CherryRd.

## Target

Reproduce Appendix Table A2 of Zhu et al. 2020:
12 proton energies (0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 5.0, 10, 20, 50, 200, 500
MeV) → DSB/SSB/SB yields per Gy per Gbp, total + direct + indirect + hybrid.

## Software stack

1. **TOPAS** v3.9+ (registered, free-for-academic; binary install).
2. **TOPAS-nBio** extension from <https://github.com/topas-nbio/TOPAS-nBio>.
3. **Geant4** 11.x with `-DGEANT4_USE_GDML=ON` and the Geant4-DNA data files
   `G4EMLOW`, `G4PII`, etc.
4. Output: SDDv1.0 files per (energy, run); one file per primary or per run
   depending on TOPAS-nBio settings.
5. Post-processing: MEDRAS-MC `repairanalysis/medrasrepair.py` (already
   vendored in `artifacts/Medras-MC/`).

## Geometry / parameter file

Build the Zhu nucleus from the published recipe (Methods §"DNA Model"):

| Element          | Setting                                              |
|------------------|------------------------------------------------------|
| Nucleus shape    | Sphere, diameter 9.3 μm                              |
| Material         | G4_WATER, density 1 g/cm³ (backbone 1.407 g/cm³)     |
| Voxel size       | 0.3 μm side                                          |
| Voxels per nucleus | 14,328                                             |
| DNA per voxel    | 0.42 Mbp                                             |
| Nucleotides per nucleosome | 200 bp wrapped + 99 bp linker              |
| Nucleosomes per fiber | 51 (= 15,150 bp per chromatin fiber)            |
| Chromatin fiber radius / length | 37.1 nm / 120 nm                      |
| Folding          | Continuous 3D Hilbert space-filling curve per fiber loop; 7 fibers per loop, 4 loops per voxel |
| Chromosomes      | 46 (sizes per Table 1; X+Y included)                 |
| Direct SB threshold | ≥17.5 eV in backbone + hydration shell per history |
| Indirect SB      | OH only, reaction probability 0.4                    |
| DSB definition   | 2 SBs on opposite strands within ≤10 bp              |
| Physics          | `TsEmDNAPhysics` (extended ionization to 500 MeV)    |
| Chemistry        | `TsEmDNAChemistry`, chemical stage cutoff 1 ns       |

Source geometry: protons launched at random points on the nucleus surface,
random inward direction. Each run delivers 1 Gy nucleus dose. Number of
primaries per run = 1,000–250,000 depending on energy (Table A1).

## Compute cost estimate

From the paper (Table A1): ~10 h wall-clock per 1 Gy run, 10-thread mode on
Xeon L5640/X5660/E5450 @ 2.27–3.00 GHz (so ~100 thread-hours per run).

For Table A2 reproduction:
- 12 energies × 100 runs each = 1,200 runs.
- 100 thread-hours/run × 1,200 = **120,000 thread-hours** for full Table A2.

Targets:

| Cluster       | Per-node thread-hours/day | Days for 120k tH (1 node) | Reasonable allocation |
|---------------|---------------------------|---------------------------|-----------------------|
| uicgpu (96 CPU cores nominal) | ~2,300       | ~52 days                  | Use 8 nodes × 7 days  |
| Aurora (Xeon Max 9470, 52 cores × 2 sockets/node) | ~2,500 | ~48 days | Use 32 nodes × 2 days, datascience allocation |

A reduced reproduction (12 energies × 10 runs each + statistical uncertainty
~6%) is **~12,000 thread-hours** → ~5 days on 1 uicgpu node or ~6 hours on
32 Aurora nodes. **This is the recommended first job submission.**

## Output volume

Each SDDv1.0 file with 1 Gy worth of damage on this nucleus ≈ 50 KB – 1 MB.
1,200 runs × ~500 KB ≈ **600 MB**; trivial storage. Park in `/data/stevens/`
on uicgpu (HOT NVMe per workspace AGENTS storage policy).

## Repair stage (lightweight, runs anywhere)

After SDD files are produced, run on CherryRd:

```bash
cd lucid100-topas-proton-cellular-response/artifacts/Medras-MC
python3 -c "
import sys; sys.path.insert(0,'.')
from repairanalysis.medrasrepair import repairSimulation
repairSimulation('/path/to/sdds', 'Fidelity', repeats=50,
                 repairFailure=True, addFociDelay=True)
"
```

Reproduces Zhu Figs 6–8 (residual DSB, misrepair fractions, dicentric/
acentric yields, MN-percent BN). Per the prior `lucid-medras-mc` replication,
this finishes in minutes on 1 CPU.

## Stretch goal

Compare to Friedland et al. 2017 (Sci Rep 7:45161) PARTRAC numbers and
Meylan et al. 2017 (Sci Rep 7:11923) Geant4-DNA numbers, both already cited
by Zhu in Fig 5. Both have published numerical yield tables; no rerun needed
on their side.

## Decision

**Hold.** This first-pass scoping shows the full TOPAS-nBio rerun is HPC-grade
work and the per-claim agreement of Zhu vs literature is already
well-established. The MEDRAS-MC repair-stage portion is already replicated in
LUCID `lucid-medras-mc`. If campaign upgrades this paper from "first-pass" to
"deep replication", queue the reduced (10-runs-per-energy) job on uicgpu first.
