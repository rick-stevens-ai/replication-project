# Failure Analysis — zhao2025

## What went wrong / limits
1. **Subagent timed out during cleanup (5m19s).** The physics + code + results.json + figures completed and all 4 claims passed; only the 5 report artifacts were unwritten. Parent recovered them from the confirmed results (Yeil's "recover-from-disk" pattern) — no re-run of the science needed (code re-executed clean, exit 0).
2. **Symmetry-only edges, not DFT coefficients.** The eta mixing ratios matched the paper's reported values, but we did not independently compute the coupling coefficients from DFT; the graph edges encode symmetry-allowed couplings, and quantitative eta used the paper's coefficient inputs. A fully independent quantitative check needs DFT frozen-phonon coupling fits (see open questions).
3. **Parent-phase choice for HfO2.** Used Fm-3m as parent; a tetragonal parent could shift the compatibility verdict (open question 4).

## Verdict impact
Framework + all worked-example verdicts reproduced; the one honest gap is the DFT-coefficient independence of the quantitative eta, which keeps this a strong REPLICATED of the methodology rather than a from-first-principles quantitative reproduction.
