# HPC job plan — full TOPAS-nBio replication of Masilela et al 2026

Run this **only** when (a) the chemistry parameter files promised in the
paper land in `topas-nbio/TOPAS-nBio-v2.0` (or OpenTOPAS), and (b) someone has
explicitly approved the compute spend.  Do not run any of this on CherryRd.

## Target machine choice

| Target | Pros | Cons | Recommended? |
|---|---|---|---|
| **Aurora** (`ssh aurora`, ALCF) | PBS, large allocation, fits TOPAS-nBio easily; allocation `datascience` or `AuroraGPT` | Intel Max GPUs; TOPAS-nBio is CPU-only — wastes GPUs but plenty of Xeon CPU cores | ★★★ batch sweeps |
| **uicgpu** (`ssh uicgpu`) | 2 TB RAM, fast NVMe, no queue, interactive — perfect for iterating on chemistry decks | Single node only | ★★★★ dev/debug + medium runs |
| **chiatta00** (JLSE, PVC GPUs) | Same caveat re: GPU waste; available CPU cores | Smaller CPU pool than uicgpu | ★★ fallback |
| **CELS rbdgx2 / rbdgx3** | GPU-dominant, lots of CPU cores too | Shared with vLLM serving | ★★ fallback |
| **Sophia** (ALCF, via studio-ts proxy) | GPU; vLLM-shared | Same GPU caveat | ★ |

**Primary plan:** uicgpu for dev + small sweeps; Aurora for the full UHDR-vs-CONV × 4-σ × 2-models × statistical-uncertainty sweep.

## Software stack

```text
OpenTOPAS v4.0.0          (https://opentopas.github.io)
TOPAS-nBio v4.0 dev       (whatever tag the authors push; for now monitor
                           https://github.com/topas-nbio/TOPAS-nBio-v2.0/releases)
Geant4 11.1.3             (lib/include must match the TOPAS build)
Python 3.11 + numpy, scipy, matplotlib   (for the DSB post-processor)
```

Container suggestion (uicgpu): build a Singularity/Apptainer image from
`continuumio/miniconda3` + apt deps for Geant4 11.1.3, layered with
OpenTOPAS-v4.0.0 from source.  Cache the image under
`/data/stevens/containers/opentopas-v4.0.0.sif` per the
[uicgpu hot/cold storage policy](../../../../TOOLS.md).

## Run topology

The paper's run that *must* be reproduced:

| Phase | What | # particles | Walltime estimate |
|---|---|---|---|
| 1. Condensed history | 225 kVp x-rays in concentric water spheres (5 + 10 cm); score vertex spectrum at 5 cm sphere | 5 × 10⁸ photons | ~6 h on 64 Xeon cores (Aurora node) |
| 2. Track-structure chemistry × 2 models × 4 σ × 2 dose rates | 100 Gy delivered as a single pulse of 5 µs (UHDR) or 1000 s (CONV) into a ~1 µm sphere with 10 pUC19 plasmids | as many primary electrons as needed to deposit 100 Gy in the µm sphere; IRT chemistry; runs needed until SSB stat unc < 2% | TS chemistry dominates: rough estimate **~20-50 k CPU-h** per single condition, scaling linearly with # primaries; full 16-cell matrix → **~0.5-1 M CPU-h** if reproduced at full statistics |
| 3. DSB post-processing | 10⁶ acceptance-resampling draws per condition over per-strand IDs | trivial | < 1 CPU-h per condition |

A *minimum-viable* HPC run that would be defensible as "replication-grade":
1 condition (DMSO 1e-5 M, 21% O₂, 100 Gy, Model 1, UHDR + CONV pair), stat unc ≤ 5%.
Estimate: **5 k CPU-h** on Aurora = ~80 wall hours on a 64-core node.  Allocation
`datascience` can absorb this without difficulty.

## PBS skeleton (Aurora)

```bash
#!/bin/bash -l
#PBS -A datascience
#PBS -q prod
#PBS -l select=8:ncpus=64
#PBS -l walltime=24:00:00
#PBS -N topas_uhdr_plasmid
#PBS -o $HOME/projects/lucid100-uhdr-plasmid/logs/${PBS_JOBID}.out
#PBS -j oe

module load oneapi
source $HOME/projects/lucid100-uhdr-plasmid/env/topas-nbio-env.sh
cd $PBS_O_WORKDIR

mpiexec -n $(($PBS_NUM_NODES * $PBS_NUM_PPN)) \
    $TOPAS_DIR/bin/topas \
    decks/model1_dmso_1e-5_o2_21pc_100Gy_UHDR.topas \
    > logs/run_${PBS_JOBID}.log 2>&1
```

The `.topas` decks themselves are not in this folder — they have to be
constructed from the chemistry table in `scripts/chemistry_table1.csv` plus
the TOPAS-nBio examples in `topas-nbio/TOPAS-nBio-v2.0/examples/` (see e.g.
`examples/processes/scavengers/`).

## Acceptance criteria for "replication succeeded"

A full replication is accepted when, at all four DMSO concentrations,

1. SSB G-values (Gy⁻¹ Da⁻¹) at CONV agree with the paper's reported values
   within 2 × the quoted statistical uncertainty (Table-like list in §3.1):
   `3.63e-7, 9.31e-8, 1.63e-8, 6.59e-10` ± ≤2%.
2. UHDR vs CONV reduction reproduces 54.7% / 14.6% / 1.1% / 0.1% within
   ±5% absolute.
3. DSB G-values (Gy⁻¹ Da⁻¹) reproduce
   CONV: `2.88e-8, 2.76e-9, 1.68e-10, 1.76e-11`;
   UHDR: `7.64e-9, 2.16e-9, 1.62e-9, 1.79e-11` within stated uncertainties.
4. Model 2 (WR-1065 at 1 mM, 21% O₂) reproduces the 3.5% reduction in SSB
   at the biologically-relevant scavenging point.

## Estimated cost if executed today (full matrix)

- Aurora `datascience` allocation: 1 M CPU-h easily fits within quarterly budget.
- uicgpu: interactive, no allocation needed; can sustain ~500 k CPU-h/month
  on a single 256-core box.  Realistic to reproduce 1–2 conditions per week
  while iterating on the decks.

**Bottom line:** the bottleneck is the chemistry-deck release, not compute.
