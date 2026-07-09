# HPC Job Plan — Full Rumiantcev 2023 reproduction

**Status:** plan only. Not submitted. Do not run on CherryRd.

## Compute footprint (from supplement §Computing)

The authors used the Leibniz Supercomputing Centre Compute Cloud:
- Main flavor: 1/4 of `hugemem` node = 48 vCPUs Intel Xeon Platinum 8160 @ 2.1 GHz, 1488 GiB RAM
- Lower-cost sims: 12-vCPU VMs (Xeon Silver 4210R @ 2.4 GHz, 78 GiB RAM)

Per-simulation wall and memory:

| Worst case | Init wall | Execute wall | Peak RAM |
|---|---|---|---|
| ¹⁷⁷Lu, 3D, geom 4, membrane-bound, 5000 src/cell | 34 h | 111-139 h | 46 GiB |
| ²²⁵Ac, 3D, geom 1, membrane-bound, 10 src/cell | 1 h | 35-85 h | 13 GiB |
| ¹⁷⁷Lu, typical (lower geom + smaller source counts) | <1 h | ~5-20 h | <8 GiB |
| ²²⁵Ac, typical | <1 h | ~2-10 h | <5 GiB |

## Total campaign

- 2 radionuclides × 5 cell geoms × 2 arrangements × 2 internalizations × 10 source-point counts × 10 random seeds = **4000 individual simulations**.
- Approx weighted average wall: ~20 h ¹⁷⁷Lu, ~10 h ²²⁵Ac → mean ~15 h.
- **Estimated total CPU-hours: 4000 × 15 h ≈ 60 000 single-thread CPU-h**, or about **20 000-30 000 effective CPU-h if TOPAS multi-threading scales at ~2× per simulation** (Geant4 MT does scale but you don't generally win >4× per single simulation; the bigger lever is wide parallelism across simulations).
- Plus MEDRAS-MC pass: 4000 × 10 repair-history repeats × tens of seconds per SDD ≈ **300 CPU-h** (trivial).

## Target machines (priority order, per TOOLS.md)

### Option 1: Aurora (preferred for scale)
- 6× Intel Max GPUs + Xeon Max CPUs per node, PBS scheduler.
- Allocation: `datascience` or `AuroraGPT`.
- TOPAS does NOT benefit from GPU; this is a CPU-only job. Use the CPU-side of Aurora nodes.
- Strategy: array job, ~500-1000 single-thread sims per node × ~20 nodes × ~24 h. **Budget: ~24 node-hours (Aurora is ~104 cores/node, so ~2400 CPU-h/node-day) → 10-15 node-days.** Comfortable within standard allocation.
- Submission template: see `aurora-pbs-topas.sh` (TODO if promoted).

### Option 2: uicgpu (preferred for memory-bound configs)
- 2 TB RAM, 1 node, 128+ logical CPUs.
- Best for the worst-case ¹⁷⁷Lu / 3D / geom 4 simulations (46 GiB RAM each).
- Strategy: 8-12 sims concurrent (CPU-bound, ~40 cores each), wall ~1 week to finish the worst-case slice.
- `HF_HOME=/data/stevens/.cache/...` per uicgpu storage policy (irrelevant here; topas uses local scratch).

### Option 3: ALCF/Polaris CPU partition
- Backup if Aurora allocation tight.

**Do NOT run on CherryRd, m1-mac-mini, spark-*.** TOPAS-nBio with chemistry stage is single-process CPU-heavy and would lock those hosts for weeks.

## Software stack to install
- Geant4 10.06-patch-03 (exact version paper uses; later versions change DNA physics list defaults).
- TOPAS v3.6 (compatible with Geant4 10.06.p03; registration required).
- TOPAS-nBio v1.0 (extension, needs G4 + TOPAS source).
- Python ≥ 3.8 with `numpy`, `scipy`, `matplotlib`, `pandas`. MEDRAS-MC already replicated in slot 16, BSD-2.

## Time budget (calendar)
- Geant4/TOPAS/TOPAS-nBio build: 1-2 days incl. registration.
- TOPAS input-deck reconstruction from supplement: 3-5 days.
- Sanity smoke (1 cell geom × 1 internalization × 3 source counts × 3 seeds): 1 day.
- Production campaign: ~2 weeks Aurora node time, ~1 day clock if pipelined.
- MEDRAS repair + Fig 9 regeneration: 1 day.

**Total calendar: 3-4 weeks for one engineer + allocation.**

## Cost guard rails
- Tag all jobs with `RUMIANTCEV_RBE_REPLICATION_2026` for accounting.
- Cap concurrent Aurora jobs at 20 to avoid burning allocation on a single failed input deck.
- Run `²²⁵Ac` slice first (cheaper, ~25-30% of total CPU-h) to validate end-to-end before committing to `¹⁷⁷Lu`.

## Decision
**Not run.** Promoted-replication only. The analytical + smoke layers in this folder are sufficient for first-pass LUCID coverage.
