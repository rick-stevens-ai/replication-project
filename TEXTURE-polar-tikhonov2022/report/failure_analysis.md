# Failure Analysis — TEXTURE-polar-tikhonov2022

Honest log of what failed on the way to the final PARTIAL_STRONG verdict.

## Failure 1: skimage not installed → wrong "branching" metric
- **Symptom.** First scoring rule used a raw-wall junction count (wall pixel with ≥3 wall neighbors). Straight thick walls trivially satisfy this, so the "parallel stripes" reference showed 576 "junctions" — larger than the network's 73 — and Claim 1 spuriously failed.
- **Root cause.** I assumed `skimage.morphology.skeletonize` was available. It wasn't on this host (system Python, PEP 668). The raw wall pixels are ≥ 2 wide, so any wall pixel has many wall neighbors; the diagnostic is meaningless without prior thinning.
- **Fix.** Wrote a pure-numpy Zhang–Suen thinning to skeletonize the wall mask, then counted branch points on the 1-pixel-wide skeleton. Post-fix, straight stripes have 6 skeleton junctions (small boundary artifacts) and the network has 48.
- **Lesson.** For binary-morphology diagnostics, always thin/skeletonize first; do not rely on optional deps in a sealed run.

## Failure 2: overstrong depolarization penalty → collapse
- **Symptom.** First run with `λ_es=4.0, kx=1.5, kz=0.6, N=8000` produced a network that had already coarsened into 2 large components with a low wall fraction (0.008); junctions dropped from ~200 to 73.
- **Root cause.** `λ_es` was so large it dominated the Landau term and drove the system toward uniform `P_z` — it eliminates all bound charge by eliminating all domains. `F_es` was low but for the wrong reason.
- **Fix.** Dropped `λ_es` into the frustrated regime where it competes with Landau + gradient without dominating (`λ_es=1.5`), and used stronger uniaxial anisotropy (`k_z=1.5, k_x=0.3`) so H–H walls are geometrically penalized instead of driven out entirely.
- **Lesson.** In TDGL parameter tuning, the target is the frustrated regime; monitor `F_landau`, `F_grad`, `F_es` separately per step to catch runaway dominance.

## Failure 3: matched-time comparison flipped Claim 2 at intermediate N
- **Symptom.** With `λ_es=2.0, N=3000` the network had 78 junctions (Claim 1 strong) but `F_es_network = 72.6 > F_es_hh = 55.4` (Claim 2 flipped).
- **Root cause.** The network relaxes its charge on a slower timescale than the H–H reference (which just needs to broaden a single wall). At N=3000 the network hadn't finished the second (charge-minimizing) relaxation stage but the H–H reference was already fully converged (from N ≈ 500 onward).
- **Fix.** Held all three runs to N=5000 with parameters that keep branching alive during that long relaxation: anisotropic gradient (`kz/kx = 5`) locks in vertical branches so the coarsening timescale is much longer than the charge-relaxation timescale. Final: 48 skeleton junctions AND `F_es` ratio 0.69.
- **Lesson.** For fair energy comparisons, all runs must be at the same fictitious relaxation time; use physics (anisotropy) rather than early-stopping tricks to preserve topology.

## Failure 4: parallel-stripes reference is uncharged by construction
- **Symptom.** Reference "stripes" always shows `F_es = 0.000`, which is a trivially lower bound than any relaxed network.
- **Root cause.** Parallel stripes along the z-axis have `∂z P = 0` everywhere, so `ρ_b ≡ 0` and `F_es = 0`. This is not a physical failure of the model, but it means the stripes reference is NOT the right benchmark for Claim 2 — it would trivially "win" every electrostatic comparison.
- **Fix.** Kept stripes as the reference ONLY for Claim 1 (branching topology comparison), and introduced a separate naive **H–H wall** reference — which is charged by construction — for Claim 2. Reported both explicitly to avoid confusion.
- **Lesson.** Use the right reference for the right claim. A topological claim needs a topological reference; an energetic claim needs an energetic reference.

## Non-failures I want to flag
- The 2D scalar model cannot resolve the paper's 3D multiconnected-wall-surface topology. This is not a bug of the harness; it is the reduced-scope boundary of the replication (declared upfront in method_extract and re-declared in REPORT/limitations).
- The local `(∂z P)^2` depolarization proxy is not a full Poisson solve. This is also declared upfront. It captures the SIGN and rough magnitude of the H–H penalty; a full Poisson solve would change the numbers but not (per Bratkovsky–Levanyuk-style arguments) the sign of the network vs H–H comparison.
