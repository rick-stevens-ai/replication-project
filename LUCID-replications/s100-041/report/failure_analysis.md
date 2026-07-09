# Failure analysis — s100-041

## Queue vs substance mismatch (VERDICT DOWNGRADE)

- **Queue verdict:** REPLICATED
- **Honest substance verdict:** **SPOT-CHECK** (analytical-only; MD pipeline was NOT independently regenerated)
- **Downgrade justified:** YES — falls squarely in the "analytical only" and "self-consistency, not independent regeneration of the mechanistic pipeline" categories that Rick's 2026-07-05 backfill brief flags as note-tag optimism.

## What was actually done vs what the paper claims

| Paper contribution | Reproduced here? | Kind of check |
|---|---|---|
| Multiscale MD pipeline (Geant4-DNA → CPMD → LAMMPS-ReaxFF) — §II.A, Figs 1–5 | **NO** | Citation + logic audit only. No trajectory rerun. |
| Coarse-grained rate equations Eqs 1–2 numerical solution — §II.B, Figs 6–7 | **YES** | Independent ODE integration in scipy. N2(FLASH)/N2(CDR)=1.70 vs paper's ≈2. |
| Analytical scaling limits Eqs 7–9 | **YES** | Log-log slope fits: 1.000, 3.000, 0.342 vs analytic 1, 3, 1/3. |
| Physoxic-optimum claim (§III text) | **NO** | Not evaluated; μ_1 is symbolic-only in the paper. |
| Mechanistic story (NROS chains cause FLASH sparing) | **NO** | Untestable without the ReaxFF trajectories. |

## Why the queue label is misleading

The rate-equation panel (Figs 6–7) is a 2-ODE toy model that a first-year grad student could re-integrate in an afternoon from the printed equations. Reproducing it is a **reproducibility floor** — the minimum consistency check that the paper's own math is internally coherent — not evidence for the paper's scientific claim.

The scientific claim of the paper is: **"UHDR/FLASH dose rates favour NROS-chain formation over free ROS, and this shifts the O2-depletion balance in a way that spares normal tissue but not tumour."**

To independently support that claim, one would have to:
1. Rerun Geant4-DNA to get the ionisation-event map at FLASH vs CDR rates → not done.
2. Rerun CPMD/DFT on the ionised H2O + O2 fragments → not done.
3. Rerun LAMMPS-ReaxFF on the DNA + water + O2 + radical box out to 1 ns and count NROS species vs ROS species → not done.
4. Sweep O2 concentration and reproduce the physoxic-optimum curve → not done.
5. Cross-check the ReaxFF output against a second FF or ab initio benchmark → not done.

None of that was done here. What was done is: "assuming the rate equations describe the true chemistry, they behave as the paper says they behave."

## Category tags (Rick's 2026-07-05 list)

- ✅ **"analytical only"** — YES, the reproduction is confined to §II.B, which is 2 ODEs.
- ✅ **"self-consistency not independent regeneration"** — YES, we reproduced the paper's own equations from its own equations. We did not regenerate the underlying mechanism.
- ⚠️ **"blocked by unreleased artifact"** — PARTIAL. The MD input decks, ReaxFF parameter files, Geant4-DNA macro, and CPMD configuration are not released (only a Facebook link to movies). This blocks independent MD reruns even if compute were available.
- ⚠️ **"unfalsifiable"** — PARTIAL. The paper acknowledges that G and D_f are phenomenological, so the numerical N2/N1 ≈ 2× claim cannot be tied to any Gy/s and cannot be experimentally falsified. It is a model-consistency statement.

## Why "MC never re-run" doesn't quite apply
This paper is not a Monte Carlo dose-simulation paper (it's MD-plus-rate-equations), so the exact phrasing "MC never re-run" is imperfect. But the analogous statement is exact: **the MD pipeline never re-run.** The 2-ODE toy model that WAS run is analogous to running just the analytical post-processing of a MC paper without touching the MC engine — a weak spot-check.

## What would elevate this to genuine REPLICATED
1. A LAMMPS-ReaxFF rerun of the DNA + water + O2 box at two pulse rates, showing NROS-chain counts.
2. An independent measurement of D_f from that rerun, plugged back into Eqs 1–2 to give the pulse-shape figure in **physical** units of Gy/s and µM.
3. A comparison of the resulting [H2O2](t) to the Montay-Gruel PNAS 2019 measurements.
4. Sensitivity of the physoxic-optimum claim to force-field choice.

Any one of those four would be worth another 1–3 Agreement points. All four would push this to REPLICATED honestly.

## Honest one-line takeaway
The paper's math is self-consistent (we verified). The paper's mechanism is not verified (we did not touch the MD). Calling this REPLICATED conflates the two.
