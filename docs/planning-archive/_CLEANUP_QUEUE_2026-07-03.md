# Unfinished-shell cleanup queue — 2026-07-03

21 incomplete replications (PDF/work present, no REPORT.md). Re-spawning to completion in rolling batches of 5 (subagent cap). Model: argo/argo:claude-opus-4.7 (free). Per Rick 2026-07-03: don't leave replications unfinished.

## Batch 1 (launched 14:1x CDT) — RUNNING
- [!] OSTI-3001618-cnn-surrogate-mc-radiation-shielding  — TIMED OUT 2x (11m, compute-heavy: OpenMC+CNN). Scripts written, evidence/ still empty, NO REPORT.md. RE-QUEUE with tiny-but-real MC scope + checkpoint. Needs its own dedicated slot.
- [ ] OSTI-2583701-mala-electronic-structure  (PDF only; MALA open-source)
- [ ] OSTI-2587616-vacancy-diffusion-hea-ml-md  (PDF + 12 files)
- [ ] OSTI-3001323-radiation-reduced-diffusion-Nd-bccFe  (PDF + 16 files)
- [ ] OSTI-3366816-...electron-deposi  (PDF + 13 files)

## Batch 2 (queued)
- [ ] OSTI-2526549-pinn-fractional-pde-highdim  (PDF + 16 files)
- [ ] OSTI-2998150-kinetic-monte-carlo-simulations-of-aging-in--pu  (PDF + 4)
- [ ] OSTI-3000748-ml-ensemble-disordered-materials  (PDF + 1520 files — lots of work already)
- [ ] OSTI-2588304-gnn-mc-lu-h-n-thermodynamics  (PDF + 2)
- [ ] OSTI-2891462-mlff-kmc-ising-magnets  (PDF + 2)

## Batch 3 (queued)
- [ ] OSTI-2336586-simulateqcd-multigpu-lattice  (PDF + 2)
- [ ] OSTI-3006635-surrogate-driven-design-optimization-...-mc  (PDF + 2)
- [ ] OSTI-3013688-e3sm-river-dycore-flooding  (PDF + 2)
- [ ] OSTI-2540232-exascale-microstructure-genlearning  (1 file — need PDF pull first)
- [ ] OSTI-2975173-ferroelectric-fractals-...-wurtzite-aln  (1 file — need PDF pull first)

## Batch 4 (queued)
- [ ] OSTI-3020811-ml-vibronic-band-structures  (1 file — need PDF pull first)
- [ ] BVBRC-64-lactobacillus-reuteri-pnw1  (empty — need genome pull)
- [ ] BVBRC-65-ecoli-blaNDM4-incFII-plasmid  (empty)
- [ ] BVBRC-67-fusobacterium-varium-fv113g1  (30 files work/, no report)
- [ ] BVBRC-68-pseudomonas-blakpc2-plasmid  (53 files work/, no report)

## Batch 5 (queued)
- [ ] BVBRC-70-mtb-hsdm-drug-resistance  (3 files)

After each batch completes: re-run census + rebuild_reconciled, update STATUS_AUDIT + report table.
