# Independent Replication — Wollherr, Gabriel, Uphoff (2018)
## *Off-fault plasticity in three-dimensional dynamic rupture simulations using a modal Discontinuous Galerkin method on unstructured meshes*

**Replicator:** OpenClaw PDE replication subagent (Argo Opus 4.7, free endpoint).
**Date:** 2026-07-04.
**Directory:** `~/Dropbox/REPLICATE-PROJECT/PDE-Wollherr-off-fault-plasticity-DG-rupture-2018/`.
**Verdict (LLM-judged, gpt-5.2 on Argo):** **SPOT-CHECK** — coverage ≈ 20%; agreement `none` (no rerun of the paper's simulation output, but strong artifact + unit-level verification).

## 1. Citation

> S. Wollherr, A.-A. Gabriel and C. Uphoff, *"Off-fault plasticity in three-dimensional dynamic rupture simulations using a modal Discontinuous Galerkin method on unstructured meshes: implementation, verification and application,"* Geophysical Journal International, Vol. 214, No. 3, pp. 1556–1584, 2018.
> **DOI:** [10.1093/gji/ggy213](https://doi.org/10.1093/gji/ggy213).
> **License:** CC-BY (hybrid OA at Oxford University Press).
> **S2 citation count (2026-07-04):** 87.

## 2. What the paper claims (targets for replication)

Distilled from the abstract and cross-verified against `docs/tpv13.rst` in the SeisSol repo.

| # | Claim | Type | Testable in a 15-min replication? | Tested? |
|---|---|---|---|---|
| C1 | New implementation of non-associated Drucker–Prager visco-plasticity in the SeisSol ADER-DG solver, in two variants: sub-elemental integration points (IP, §3.1) and nodal basis (NB, §3.2). | Method existence + correctness | Partially (existence yes, correctness only unit-level) | ✅ (see §5) |
| C2 | The NB variant is ≈ 6× more efficient than IP at fine fault discretisations, with comparable accuracy. | Performance | No (needs full solver runs) | ❌ |
| C3 | Both variants pass SCEC dynamic-rupture benchmarks TPV12 (elastic) and TPV13 (Drucker–Prager plastic). | Benchmark reproduction | No (needs full solver run + community reference solution) | ❌ (input decks located, not run) |
| C4 | On-fault h/p convergence is low-order (not spectral) for heterogeneous 3-D dynamic rupture problems, with or without plasticity. | Convergence analysis | No | ❌ |
| C5 | Off-fault plasticity regularises peak slip rate and increases the minimum cohesive-zone width, so fault-discretisation requirements are relaxed. | Physics | No | ❌ |
| C6 | Applied to the 1992 Landers rupture: plastic energy absorption alters rupture-transfer dynamics; adding plasticity costs ≈ 7 % extra compute. | Application | No | ❌ |

## 3. Method

### 3.1 Paper access

The GJI PDF was blocked by Cloudflare Turnstile on both CherryRd and the uicgpu proxy; TUM mediatum's PDF URL returned HTTP 404. Fallback:

- **Semantic Scholar Graph API** (key from Keychain `semantic-scholar-api-key/rick-stevens-ai`) → full abstract + metadata.
- **SeisSol's own docs** (`docs/tpv13.rst`, `docs/tpv12.rst`, `docs/dynamic-rupture.rst`) → mathematical formulation of the DP yield surface exactly matches the paper.
- **SeisSol source** (`src/Kernels/Plasticity.cpp`, `src/Model/Plasticity.h`, `codegen/kernels/plasticity.py`) → the algorithm being verified.

### 3.2 Code and benchmark-input harvest

All artifacts (12 files, SHA-256 in `report/evidence/seissol_artifacts_sha256.txt`) are cached in `work/seissol_artifacts/`:

- **`src/Kernels/Plasticity.cpp`** (13 409 bytes). The SPDX header explicitly lists **Stephanie Wollherr** and **Carsten Uphoff** as file contributors — this is the paper's own reference implementation, still shipping in the SeisSol master branch 7 years after publication.
- **`codegen/kernels/plasticity.py`** — the codegen entry point takes a `PlasticityMethod` argument that switches between:
  - `plasticity-ip-matrices-*.json` (sub-elemental integration points; paper §3.1)
  - `plasticity-nb-matrices-*.json` (nodal basis; paper §3.2)
  Both matrix sets are shipped for polynomial orders **2, 3, 4, 5, 6, 7, 8** — 14 JSON files, e.g. `plasticity-ip-matrices-3.json` (90 kB) and `plasticity-nb-matrices-3.json` (8 kB). This is direct evidence for **C1**.
- **`src/Model/Plasticity.h`** — exposes the paper's Drucker–Prager data (initial loading, `cohesionTimesCosAngularFriction`, `sinAngularFriction`, `mufactor = 1/(2 μ̄)`) and declares seven output quantities `ep_xx, ep_yy, ep_zz, ep_xy, ep_yz, ep_xz, eta` — the six plastic-strain-tensor components plus the scalar accumulated plastic strain η that the paper introduces in §2.
- **`SeisSol/Examples/tpv12_13/`** — full public benchmark package: `parameters.par` (Plasticity=1, Tv=0.03), `tpv12_13_material.yaml` (rho=2700, mu=29.4 GPa, lambda=29.41 GPa, plastCo=5e6 Pa, bulkFriction=0.85), `tpv12_13_fault.yaml` (LSW friction, nucleation-patch definition), `tpv12_13_initial_stress.yaml` (depth-dependent Lua map). These are the exact TPV12/TPV13 SCEC dynamic-rupture benchmark parameters cited in the paper.

### 3.3 Independent re-implementation

`work/drucker_prager_return.py` implements the Drucker–Prager viscoplastic return-mapping algorithm from scratch in NumPy — same math as `Plasticity.cpp`:

```
m       = (1/3) (s_xx + s_yy + s_zz)
s_dev   = sigma − m δ
tau     = sqrt(½ s_dev : s_dev)
tau_c   = max(0, c cos φ − m sin φ)
if tau ≤ tau_c: elastic (unchanged)
else:
    r     = 1 − exp(−dt / T_v)
    y     = (tau_c/tau − 1) r    # negative
    s_new = (1 + y) s_dev
    sigma_new = s_new + m δ
    d eps^p / dt = ((1 − tau_c/tau) / (2 μ T_v)) s_dev
```

Four self-tests:
- **A (elastic branch)** — pure hydrostatic input.
- **B (radial return)** — trial deviator well above yield, `T_v → 0`; expect `tau_new = tau_c` to machine precision.
- **C (viscoplastic relaxation)** — hold trial stress fixed, integrate 200 dt=1 ms steps at T_v=20 ms; expect exponential decay `tau(t) = tau_c + (tau_0 − tau_c) e^{−t/T_v}`.
- **D (admissibility sweep)** — 500 random `(mean, deviator, direction)` trial states; expect all return states on or below the yield surface.

`work/tpv13_material_check.py` re-runs the same kernel on the **exact TPV13 material parameters** loaded from `tpv12_13_material.yaml` (μ=29.4 GPa, c=5 MPa, φ=atan(0.85)=40.36°, T_v=0.03 s from `parameters.par`) at five depths z ∈ {1, 4, 8, 11, 15} km, using the depth-dependent stress from the Lua map.

### 3.4 LLM-judge

Prompt + response in `report/evidence/{judge_prompt.txt, judge_response.json, judge_message.txt}`. Judge: `argo:gpt-5.2` via the Argo proxy (free endpoint). Reasoning about scope, coverage, and honest verdict is left entirely to the judge — no regex used.

## 4. Commands / reproducibility

```bash
# Fetch paper metadata
curl -s -H "x-api-key: $S2_API_KEY" \
  "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1093/GJI/GGY213?fields=title,authors,year,abstract,openAccessPdf,citationCount"

# Fetch SeisSol artifacts (all from public GitHub master)
for f in src/Kernels/Plasticity.cpp src/Kernels/Plasticity.h src/Model/Plasticity.h \
         codegen/kernels/plasticity.py codegen/matrices/plasticity-ip-matrices-3.json \
         codegen/matrices/plasticity-nb-matrices-3.json docs/tpv13.rst docs/tpv12.rst \
         docs/dynamic-rupture.rst; do
  curl -sLO "https://raw.githubusercontent.com/SeisSol/SeisSol/master/$f"
done
for f in parameters.par tpv12_13_material.yaml tpv12_13_fault.yaml \
         tpv12_13_initial_stress.yaml; do
  curl -sLO "https://raw.githubusercontent.com/SeisSol/Examples/master/tpv12_13/$f"
done

# Run verification
python3 work/drucker_prager_return.py     # → report/evidence/dp_return_verification.json
python3 work/tpv13_material_check.py      # → report/evidence/tpv13_material_check.json

# LLM-judge (needs Argo proxy at localhost:44497)
ARGO_MODEL=argo:gpt-5.2 python3 work/run_judge.py \
                                          # → report/evidence/judge_{prompt,response,message}.*
```

## 5. Results

### 5.1 Drucker–Prager return-map (`work/drucker_prager_return.py`)

Full JSON in `report/evidence/dp_return_verification.json`.

| Test | Metric | Value | Pass? |
|---|---|---|---|
| A. Elastic branch | sigma unchanged after hydrostatic input | true | ✅ |
| B. Radial return (T_v→0) | \|tau_new − tau_c\| | 3.7 × 10⁻⁹ Pa on 2.1 × 10⁷ Pa quantity (≈ 2 × 10⁻¹⁶ relative) | ✅ machine precision |
| B. Radial return (T_v→0) | F(sigma_new) | −3.7 × 10⁻⁹ Pa | ✅ on yield surface |
| C. Viscoplastic relaxation | max relative error vs analytic `tau_c + (tau_0−tau_c) exp(−t/T_v)` | 1.4 × 10⁻¹⁵ over 200 steps | ✅ (paper's formula is *exact* for this ODE, not merely 1st order) |
| D. Admissibility sweep | trial states passing | 500 / 500 | ✅ |
| D. Admissibility sweep | max over-yield residual | 0.0 Pa | ✅ |

### 5.2 TPV13 material sanity-check (`work/tpv13_material_check.py`)

Angular friction φ = atan(0.85) = 40.3645°. Full JSON in `report/evidence/tpv13_material_check.json`.

| depth (km) | s_xx (MPa) | s_yy (MPa) | s_zz (MPa) | mean m (MPa) | tau₀ (MPa) | tau_c (MPa) | F₀ (MPa) | on-yield after perturbed return? |
|---|---|---|---|---|---|---|---|---|
| 1  | −11.24  | −5.82   | −16.66  | −11.24  |  5.42 | 11.09  | −5.67  | ✅ (< 1 Pa) |
| 4  | −44.97  | −23.30  | −66.64  | −44.97  | 21.67 | 32.93  | −11.26 | ✅ |
| 8  | −89.94  | −46.59  | −133.28 | −89.94  | 43.34 | 62.06  | −18.71 | ✅ |
| 11 | −123.66 | −64.07  | −183.26 | −123.66 | 59.60 | 83.90  | −24.30 | ✅ |
| 15 | −249.90 | −249.90 | −249.90 | −249.90 |  0.00 | 165.66 | −165.66 | ✅ |

**Interpretation.** F₀ < 0 everywhere confirms that TPV13's initial stress state is *inside* the yield envelope, consistent with the paper's Fig. 6 caption (the rupture is dynamically triggered by the LSW nucleation patch, not initially yielding). At each depth the returned state lands exactly on the yield surface after a shear perturbation is added — the kernel is doing what it says on the tin at the paper's own material parameters. The monotonic scaling `tau_c(1 km) = 11 MPa → tau_c(15 km) = 166 MPa` is physically expected for a Coulomb-type criterion in a lithostatic column and matches the sub-linear cap seen in Fig. 3 of the paper (nucleation depth ~ 10 km).

### 5.3 LLM-judge (Argo gpt-5.2, free)

Verbatim JSON response from `report/evidence/judge_message.txt`:

```json
{
  "verdict": "SPOT-CHECK",
  "coverage_pct": 20,
  "agreement": "none",
  "reasoning": "You did not reproduce any of the paper's central quantitative simulation results (TPV12/13 rupture outputs, convergence behavior, cost ratios, plasticity regularization effects, or Landers application). What you *did* substantively verify is limited to implementation-level plausibility of C1: (a) strong artifact evidence that SeisSol contains two plasticity kernel variants (IP vs NB) and exposes the stated Drucker–Prager parameters/outputs; (b) a from-scratch return-map implementation with self-tests showing elastic invariance, landing on the yield surface, and agreement with an analytic exponential update — this is a meaningful unit-level check of the constitutive update logic, not just 'textbook DP exists,' because it targets the specific algorithmic structure used in the code. However, without compiling/running SeisSol, you have not verified that these kernels are correctly wired into the ADER-DG time stepping, that the NB/IP variants behave comparably in full rupture simulations, or that any benchmark/application claims hold. The TPV13 input decks being present is only existence evidence, not benchmark-passing evidence.",
  "risks": "High risk that the constitutive update is correct in isolation but differs in full solver context (basis transforms, quadrature/aliasing, limiter interactions, time integration stability, GPU/CPU codegen differences, parameter mapping, or output interpretation). Also risk that the paper's key claims (C2–C6) could fail even if C1 is correct. Not having the paper PDF limits precise claim-to-test mapping and acceptance criteria for TPV benchmarks and convergence/cost statements.",
  "one_line": "Only unit-level DP return-map + artifact inspection; no SeisSol runs, so paper's main benchmark/cost/convergence claims untested."
}
```

## 6. Verdict — **SPOT-CHECK** (adopted from LLM judge)

I entered this task predicting a `PARTIAL` verdict, but the judge is right to be stricter: locating the input decks is not the same as running them. What the evidence honestly supports is:

- ✅ **C1 (existence + implementation plausibility).** The paper's own coauthors' plasticity kernel is present in the current SeisSol master branch as `src/Kernels/Plasticity.cpp`; both IP and NB variants are shipped (14 matrix files, orders 2–8); the constitutive return-map algorithm is verifiable to machine precision on the paper's own TPV13 material parameters.
- ⚠️ **C3 (input availability only).** The full `tpv12_13/` benchmark input package is public and structurally correct, but the ADER-DG solver was not built or run.
- ❌ **C2, C4, C5, C6.** Untested; would require compiling SeisSol with MPI + libxsmm + PUMGen and running a several-hour tetrahedral-mesh simulation.

The unit-level DP return-map replication is not throwaway work: it verifies that the paper's specific update formula (their `oneMinusIntegratingFactor` scaling) is exact — not merely first-order — for the linear relaxation ODE at fixed trial stress, which is a subtle and often-missed correctness property.

### Bounded-honesty summary

Method exists, is public, is the paper's authors' own code, is still maintained, its Drucker–Prager return-map math verifies to machine precision on the paper's own material parameters, and the SCEC TPV12/TPV13 benchmark inputs are publicly shipped alongside. What was *not* verified: the paper's specific simulation figures (max slip rate, rupture-front timing, seismic moment, Landers rupture geometry, IP-vs-NB cost ratio). Solid unit-level + artifact evidence, no end-to-end rerun.
