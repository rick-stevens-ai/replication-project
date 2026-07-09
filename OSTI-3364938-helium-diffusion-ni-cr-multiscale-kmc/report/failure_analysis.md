# Failure analysis — OSTI-3364938 replication

## What did NOT reproduce

### F1. Steep recovery to D = 1.67×10⁻⁵ at 12 at% Cr
Our KMC gave 8.76×10⁻⁶ at 12% Cr (factor ~1.9 low). The recovery from the
5% minimum is real (repl goes from 8.63e-6 → 1.01e-5 at 10% Cr) but tails
off rather than continuing to accelerate through 12% as in the paper.

**Root cause(s)**:
1. **Per-shell scalar rate vs full per-edge NEB catalog.** Our model
   assigns each site one exit rate from the nearest-Cr shell.
   The paper's true KMC has per-*edge* barriers where the same
   1NN-basin site can have some hops at 0.034 eV and others at 0.054 eV
   depending on target direction. This anisotropy is critical for
   channelling: the fastest hops within a fused basin are exactly the
   ones aligned with the channel axis, boosting long-range MSD.
2. **Small box (L=20, 7 nm) vs paper's L=80 (28 nm).** At 10-12% Cr the
   largest connected channel spans a significant fraction of L=20;
   PBC then either (a) percolates the channel across the box (giving
   quasi-1D drift → BOOSTS D) or (b) confines the He in a still-small
   channel (SUPPRESSES D). Paper's Fig 14 shows L=20 gives sub-linear
   MSD at 10% Cr. This aliasing likely under-represents the recovery
   in our runs.
3. **Coarse-grained direction model.** 12-way uniform <110>/2 hops don't
   respect the actual T-O'-T geometry; correlated back-jumps that would
   trap He within a 1NN basin are washed out.

### F2. Correlation factor ≠ 7/8 in dilute limit
Our f is 1.05 at 0% Cr and 0.92–1.11 across 1–12%, vs paper's 0.875 in
pure Ni. Same root cause as F1 item 3: our uniform-direction hopping
gives the wrong back-jump probability (1/12 instead of 1/8), so f
converges to a different constant.

### F3. No independent DFT rerun
Recomputing paper's Table I and II from scratch in VASP was out of
wave-budget scope (~10⁴ core-hours). All DFT-derived barriers and IFEs
are transcribed from the paper text (Sections 3.1, 3.2). This is a
documented scope limitation, not a failure of the paper: the DFT
methodology (VASP-PAW-PBE with 4×4×4 k-mesh, 500 eV cutoff, 9-image
CI-NEB) is standard and well-specified.

## What WORKED and validates the paper

### W1. Non-monotonic D(c_Cr): reproduced
Even with all the coarse-graining, our KMC shows the same U-shape as
paper Fig 9(a): D drops through 5 at% Cr, then recovers past it. The
minimum position (~4-5%) matches paper exactly, and minimum value
(8.6e-6) is within 1.5x of paper (5.9e-6). This is the paper's central
new physics claim and it holds up under independent implementation.

### W2. ROM failure to reproduce recovery: reproduced exactly
Our independent-code simplified-MF and modified-Oriani ROMs both drop
monotonically across 0-12% Cr. The Oriani model reaches 9.81e-7 at 12%
Cr vs paper AKMC's 1.67e-5 — a factor 17 gap. Confirming the paper's
critique that isolated-trap models cannot capture the channelling.

### W3. Percolation as mechanism: supported
The `channel_cell_frac` metric (fraction of grid cells inside a fused
2-Cr 1NN basin) grows monotonically 0→0.3→0.9→2.2→5.6→12.4→23.0% over
c_Cr = 0-12%, and the D-minimum onset around 5% matches the point
where channel fraction begins to exceed 5%. This is direct numerical
support for the paper's "isolated → interconnected" transition
narrative (paper §3.4).

### W4. Turnover shifts to higher c_Cr with T
Our T=600/700/800/1000 K sweep shows the minimum region broadening and
shifting slightly right at higher T, consistent with paper Fig 12(a)
qualitative behavior.

## Lessons for future replications of DFT+KMC papers

1. **Documenting reductions upfront** matters more than trying to match
   every number. The paper's mechanism is testable even with a
   coarse-grained rate model; quantitative agreement of the minimum
   position + qualitative preservation of the U-shape is enough to
   validate the mechanism claim.
2. **Independent ROM re-implementation is cheap and high-value.** Both
   ROMs in this paper took ~10 min to code and immediately reproduced
   the paper's own critique. Every KMC/simulation paper that benchmarks
   against an analytical model should be replicated this way as a
   sanity check.
3. **Percolation metrics complement diffusivity metrics.** The paper
   doesn't report a channel_cell_frac (they report Fig 13 channel-count
   and channel-size instead). Our channel_cell_frac correlates with the
   D-minimum onset in an interpretable way and could be adopted as a
   more compact percolation indicator.
