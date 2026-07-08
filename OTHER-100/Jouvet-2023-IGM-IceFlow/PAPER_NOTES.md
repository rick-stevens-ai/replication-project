# Paper Notes — Jouvet 2023 IGM Ice-Flow

**Citation:** Jouvet, G. (2023). *Inversion of a Stokes glacier flow model emulated by deep learning.* Journal of Glaciology, 69(273), 13–26. DOI: 10.1017/jog.2022.41.

**Code (current):** https://github.com/instructed-glacier-model/igm (was `jouvetg/igm`, now under `instructed-glacier-model` org).

## What the paper claims (from abstract + downstream descriptions)

Data assimilation for high-order ice-flow modeling: simultaneously infer
- **ice thickness** distribution `H(x,y)`
- **ice flow parametrization** (Glen / sliding law parameters, typically `c` Arrhenius factor and `c_s` sliding coefficient)
- **ice surface** `s(x,y)`

… consistent with (a) Stokes ice-flow mechanics and (b) surface mass-balance, while best matching observations (surface velocity, surface elevation, ice thickness samples).

**Method:** replace the Stokes solver with a CNN **emulator** (trained on an ensemble of Stokes runs). The inversion is then a gradient-based optimization in TensorFlow with automatic differentiation, SGD/Adam, on GPU.

**Demonstration:** ten of the largest glaciers in **Switzerland** at **100 m** resolution.

## Headline performance claim (target metric for replication)

> "Optimizing one large-size glacier at 100 m takes **< 1 min on a laptop**" — i.e. the inversion (not the emulator training) is the < 1 min number.

This is THE numerical performance claim we can replicate quantitatively. Other paper claims (RMSE on velocity field, thickness vs. radar reference) are per-glacier specific and reported in figures/tables we'd need full-text access to.

## Target test case for replication

Use IGM's bundled example for one Swiss glacier (paper used Great Aletsch among others). The repo's `examples/` ships a ready test case. We pick whatever the official "inversion demo" is in the current IGM code.

## What we can replicate without paper PDF body

1. **Workflow:** run the inversion module on a Swiss glacier at ~100 m and produce inferred H, c, c_s, s fields.
2. **Performance claim:** time the inversion → does it complete in "minutes" on an A100? (The < 1 min on laptop claim should be ~seconds on A100; we report whichever side of that we observe.)
3. **Plausibility:** sanity check that inferred ice thickness has reasonable magnitudes (Aletsch max ≈ 800 m) and that the emulator+SMB residual is small at the inferred state (the paper's "high degree of assimilation while guaranteeing equilibrium").
4. **Reproducibility:** does the published, open-source codebase actually produce inversion output on a representative Swiss glacier with the documented tutorial? (This is itself a replication question — does the code as released match the paper's claims.)

## Things we cannot get without paper full text

- Exact numerical RMSE for velocity / thickness per glacier (paper figures/tables)
- Exact emulator architecture hyperparameters (paper §3)
- Exact loss-function weights

Strategy: use IGM defaults (which are the author's own — IGM is the paper's code), and compare order-of-magnitude.

## Verdict scheme

- **REPLICATED** — workflow runs to completion, inversion produces plausible H/c/s fields, runtime within 1 order of magnitude of paper's claim.
- **PARTIAL** — workflow runs but one key claim doesn't match (e.g. runtime way off, or no convergence).
- **FAILED** — workflow doesn't complete or produces nonsense.
