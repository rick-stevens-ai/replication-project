# Failure analysis — textures-polar-dahl2002

## What could have gone wrong, and what did
- **Old-style arXiv id**: `cond-mat/0211693` needs the bare-id PDF URL
  (`/pdf/cond-mat/0211693`). Worked first try (327 KB, %PDF-1.2). The `v1`
  fallback was not needed.
- **Paper has no simulation**: it is a polemical review of Lagerwall's book.
  Risk = nothing quantitative to replicate. Mitigated by extracting Dahl's own
  operational, falsifiable diagnostic (loop width vs. drive frequency) rather
  than inventing a numeric result.

## Genuine physics subtlety encountered (not a failure — a feature)
At high drive frequency (ω ≥ 0.5) the double-well model **stopped switching**
(coercive field → 0, loop collapses to a thin minor loop). Naively fitting the
loop-area-vs-ω slope over ALL frequencies gave slope = −0.73 for the double
well, which looked like a partial contradiction. This is not lossy behaviour: it
is the barrier-limited regime — the field reverses before the polarization can
climb over the barrier, so the loop never reaches ±P0. This is itself a
signature of TRUE bistability (a lossy monostable material has no barrier and
keeps a loop at all ω). Dahl's claim is explicitly about the low-frequency limit
("width ... independent of the frequency" for the switching loop). Restricting
the slope fit to the switching window (ω ≤ 0.2, where both potentials form a
P=0-crossing loop) gives the clean result: DW slope −0.02, SW slope +1.06.

## Limitations of the replication
- **0D reduction**: uniform monodomain, scalar P. Does not test Dahl's central
  thesis that SSFLC bistability is SURFACE-stabilized (needs spatial P(z) +
  anchoring). We proved the diagnostic distinguishes double-well vs. lossy; we
  did not prove which one real SSFLC cells are.
- **Idealized loss model**: TDGL overdamped relaxation is the only dissipation;
  the exact lossy exponent (+1.06 vs. Dahl's "approx. proportional") depends on
  the loss mechanism.
- **No experimental data**: comparison is model-internal (double-well vs.
  single-well), matching Dahl's qualitative prediction, not measured FLC loops.

## Nothing fabricated
All numbers come from the actual run in `work/dahl2002_result.json`
(runtime 1.7 s). Marker/Nougat outputs are honestly labeled pdftotext interims.
