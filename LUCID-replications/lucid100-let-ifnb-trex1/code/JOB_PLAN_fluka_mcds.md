# Heavy-compute job plan — PASS-full replication of Bragg-peak amplification claims

**Status:** plan only. **Do NOT run on CherryRd** (per LUCID100 policy).

## What we'd be reproducing

Claim from paper (abstract + Fig. 4 + last paragraph of Results):
> Monte Carlo modeling of IFNβ suggests Bragg-peak-to-entrance ratios of IFNβ production of **40, 100, and 120 for proton, alpha (⁴He), and carbon (¹²C) ion beams, respectively**, a factor of 10-20× higher than the corresponding physical dose peak-to-entrance ratios. The spatial width of the Bragg peak for IFNβ production is also a factor of two smaller.

## Inputs we'd need

| Item                                                | Where to get it                                                    |
| --------------------------------------------------- | ------------------------------------------------------------------ |
| FLUKA 4.x (Monte Carlo radiation transport)         | `https://fluka.cern/` — academic license (free, registration)      |
| MCDS (Monte Carlo Damage Simulation) binary         | Robert Stewart group, UW; available on request (no public download) |
| 6 MV phase-space file (paper uses CERR / VMC++)     | CERR (https://cerr.github.io) ships sample files                   |
| Mono-energetic proton / ⁴He / ¹²C beam configs (range 10 cm in water) | hand-construct in FLUKA input deck                  |
| Geometry: water phantom, 0.2 mm voxel, 5 mm FWHM beam spot | hand-construct                                              |
| Eq. 3 constants (RBE_DSB): a=0.9902, b=2.411, c=7.32e-4, d=1.539 | already in `lucid100_let_ifnb_trex1_model.py`        |

## Compute target priority (per AGENTS.md TOOLS.md)

1. **chiatta00** (JLSE) — 8× Intel PVC + Intel MPI; CPU FLUKA fine (FLUKA is single-thread per primary, embarrassingly parallel via MPI; no GPU needed). Use `mpiexec` to fan out per-energy or per-particle jobs. Source the chiatta-pvc env wrapper if any oneAPI tools are needed for post-processing.
2. **Aurora** (ALCF, allocation `datascience` or `AuroraGPT`) — PBS scheduler, queue is wide open for small/medium jobs. Use for the heavy 1080-energy depth scans.
3. **uicgpu** — interactive, no queue, 2 TB RAM; great for FLUKA post-processing (depth scans → RBE × dose convolution → IFNβ depth profile). HF_HOME etc. already set in `~/env.sh`.

## Step-by-step

1. Install FLUKA + flair on chiatta00 under `/home/stevens/software/fluka/` (no root needed for user install).
2. Request MCDS binary from Stewart group via Keith Stantz (corresponding author) — *or* substitute Geant4-DNA + a damage-clustering analyzer if license cannot be obtained.
3. Write 5 FLUKA decks: 220 kV SARRP x-ray (validation against paper's quoted RBE_DSB = 1.17–1.20), 6 MV x-ray (phase-space), proton 80 MeV (10 cm range), ⁴He 200 MeV/u, ¹²C 290 MeV/u.
4. For each deck, run depth scan: 10⁶ primaries per voxel, 500 voxels (0.2 mm each) → 5 hours wall-clock per beam on 64 chiatta00 ranks.
5. Score per-voxel `(z_eff/β)²` (USR routine) and physical dose (`USRBIN`).
6. Apply Eq. 3 → per-voxel RBE_DSB(depth); apply Eq. 1 → per-voxel IFNβ(depth).
7. Compute Bragg-peak-to-entrance ratios for both physical dose and IFNβ. Compare to paper's 40 / 100 / 120.
8. Compute FWHM of physical-dose Bragg peak vs FWHM of IFNβ peak; expect ratio ≈ 0.5.

## Estimated wall-clock + cost

- Setup + decks: ~2 days of operator time.
- Compute: ~30 hours of 64-rank chiatta00 (or 1 Aurora node × 6 hours).
- No paid endpoints. No GPUs strictly required.

## Submission helpers (do NOT auto-execute — these are templates)

```bash
# On chiatta00, after activating fluka env:
ssh chiatta00
cd /home/stevens/lucid100/slot14-fluka
for beam in xray220kv xray6mv proton80 he200 c290; do
  mpiexec -n 64 $FLUPRO/flutil/rfluka -e flukadpm -N0 -M5 ${beam}.inp
done
```

```bash
# On Aurora (PBS):
qsub -A datascience -l select=1:ncpus=104,walltime=06:00:00 -q prod fluka_sweep.pbs
```
