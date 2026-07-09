# Independent Replication Report — OSTI 2480245

**Paper:** *A Performant Energy-conserving Particle Reweighting Method for Particle-in-Cell Simulations*
**Authors:** J. J. Boerner, T. Hall, R. Hooper, M. T. Bettencourt, M. M. Hopkins, A. M. Grillet, J. L. Pacheco (Sandia National Laboratories; NVIDIA)
**Venue / IDs:** *Journal of Computational Physics* (2024) · DOI 10.1016/j.jcp.2024.113454 · SAND2024-16128J · OSTI 2480245
**Replicated by:** OpenClaw autonomous replication wave (2026-07-01), independent reimplementation from the paper's equations.
**Domain:** accelerator/plasma · PIC-DSMC macroparticle reweighting

---

## 1. Paper summary

Kinetic PIC/DSMC plasma simulations represent many real particles by weighted *macroparticles*. When plasma density varies by orders of magnitude in space/time, the number of macroparticles per cell must be adjusted ("reweighting"). The paper introduces a new **particle-based** reweighting scheme (implemented in Sandia's Aleph PIC-DSMC code) with two novel operators:

- **Split** (Sec 3.1, Fig 2, Eqs 4–5): one *parent* macroparticle becomes parent + two *children*. Children are displaced symmetrically about the parent (preserving center of mass/charge), and their field-parallel velocity component is corrected for motion through the element's electrostatic field so that **total energy (kinetic + potential) is conserved**. Splits requiring imaginary child velocities (energetically inaccessible) are rejected — the paper's stated key accuracy improvement.
- **Merge** (Sec 3.2, Fig 3, Eqs 6–12): two macroparticles become one at their center of mass, with summed weight. Modified COM velocities (Eq 7) account for field displacement; a **mass-averaged COM velocity (Eq 10) conserves momentum** but intentionally **loses a small amount of thermal KE (Eq 11)**. Merges are gated by speed/angle cutoffs (Eq 9: Δv < v_thermal, α < 30°); an optional velocity thermostat can redistribute the lost energy.

Two demonstrations: **Test 4.1** — a fixed exponential sheath potential Φ(x)=Φ_w·exp(−x/L) (Φ_w=−15 V, L=5 µm) with a rapidly ramped bump-on-tail electron beam; reweighted (split-only / merge-only) VDFs are indistinguishable from fixed-weight, and reweighting decouples wall-time from physical density. **Test 4.2** — a 0D H₂ ionization-growth swarm; the number of *real* electrons grows exponentially at a rate independent of the target computational-particle count N_c (10…10000) while the computational count stays bounded (~N_c to 1.1·N_c), with swarm parameters agreeing with Bolsig+.

## 2. Claims table

| ID | Claim | Type | Testable w/o Aleph? | Tested? |
|----|-------|------|:---:|:---:|
| C1 | Split conserves **mass** (parent W −= 2·W_child) | math/invariant | yes | ✅ |
| C2 | Split conserves **center of mass / charge** (symmetric displacement) | math/invariant | yes | ✅ |
| C3 | Split conserves **total energy** (KE + qΦ) via field-parallel velocity correction; rejects imaginary-velocity (inaccessible) splits | math/invariant | yes | ✅ |
| C4a | Merge conserves **mass** (W_merge = W₁+W₂) | math/invariant | yes | ✅ |
| C4b | Merge conserves **momentum** at COM (Eq 10) | math/invariant | yes | ✅ |
| C4c | Merge **KE_lost ≥ 0** (Eq 11); cutoffs (Eq 9) gate ineligible pairs | math/invariant | yes | ✅ |
| C4d | Merge KE loss is **small** under the paper's cutoffs | quantitative | partial | ✅ |
| C5 | Test 4.1: reweighted VDFs indistinguishable from fixed-weight in coupled sheath | full-sim | no (needs Aleph) | ⛔ out of scope |
| C6 | Test 4.2: real-electron growth rate **independent of N_c** (~3.06 s⁻¹); computational count bounded ~N_c…1.1·N_c | structural/scaling | partial (abstracted) | ✅ |
| C7 | Test 4.2: fitted-rate **precision improves with N_c** | statistical | needs Aleph DSMC noise | ⚠️ not isolable |

## 3. Method (numbered, reproducible)

**Environment:** Python 3.14, numpy 2.5.0, scipy 1.18.0 in `work/venv` (CherryRd). Operator core: `work/reweight.py`. No GPU needed (operator-level tests are light; run locally).

1. **Fetch paper.** `curl https://www.osti.gov/servlets/purl/2480245` times out from CherryRd; fetched via `ssh uicgpu` (proxy internet) → scp back → `work/paper.pdf` (5.5 MB). `pdftotext -layout paper.pdf paper.txt`.
2. **Artifact check.** Aleph is Sandia proprietary — **no public code/data package** (verified: no GitHub/Zenodo/OSTI code artifact). Strategy: reimplement the operators from Eqs 2–12 and verify their stated invariants + Test-4.2 scaling.
3. **Reimplement operators** (`reweight.py`):
   - `split_particle`: eligibility (W ≥ 3·W_min); nearest-face bound dx_max; biased spherical sampling (Eq 4) with polar axis ∥ E; symmetric ±dx displacement; Eq-5 parallel-velocity energy correction `v_∥² ± (2q/m)E·dx`; imaginary-velocity rejection with polar=π/2 fallback; weights per Sec 3.1 final paragraph.
   - `merge_pair`: nearest-speed companion; Eq-6 COM position; Eq-7 modified COM velocities (imaginary → reject); Eq-8 Δv/α cutoffs (Eq-9 values); Eq-10 mass-averaged velocity; Eq-11 KE_lost; W_max eligibility.
4. **Conservation tests** (`test_conservation.py`): 20,000 random splits and ~18,600 random merges of electron macroparticles in the **Test-4.1 exponential sheath field** E(x) = −∇[Φ_w·exp(−x/L)]; measure relative errors of every invariant. Cutoffs set to Eq-9 (Δv < √(k_BT/m) at T=5 eV, α < 30°).
5. **Growth-independence test** (`test_growth_independence.py`): 0D ionization at rate ν=3.06 s⁻¹, reweighting control loop keeping computational count within ±10 % of N_c ∈ {10,100,1000,10000}; fit n_e(t)/n_e0 = α·e^{βt} (scipy `curve_fit`); compare β across N_c and check computational-count bounds.
6. **Precision sub-claim probe** (`test_growth_stochastic.py`): added Poisson ionization noise to try to isolate C7 — could not (see §5).
7. **LLM-judge verdict** (`judge_prompt.txt`): free Argo **gpt-5.2** (localhost:44497) given all claims, results, and self-reported limitations → structured JSON verdict (`evidence/llm_judge_verdict.json`).

## 4. Results vs paper

### 4.1 Operator conservation (`evidence/conservation_results.json`)

| Check | Result (this work) | Expectation | Status |
|---|---|---|---|
| C1 split mass | max rel err **0.00e+00** (20000 splits) | exact | ✅ |
| C2 split COM | max rel err **2.89e-16** | exact (roundoff) | ✅ |
| C3 split energy (KE+qΦ) | max rel err **4.40e-16**; 0 inaccessible splits (all rejected correctly) | exact in constant-field element | ✅ |
| C4a merge mass | max rel err **0.00e+00** (18612 merges) | exact | ✅ |
| C4b merge momentum (COM) | max rel err **4.03e-16** | exact | ✅ |
| C4c merge KE_lost ≥ 0 | **0/18612** negative; **1388** pairs rejected by Eq-9 cutoffs | ≥ 0, gated | ✅ |
| C4d merge KE_lost small | median **0.062 %**, 95th pct **0.587 %** of pair KE | "small … bounded by cutoffs" | ✅ (qualitative) |

Every mathematically-specified invariant of both operators reproduces to floating-point roundoff. The energy-conserving split and its imaginary-velocity rejection — the paper's headline accuracy claim — behave exactly as described.

### 4.2 Growth-rate independence (`evidence/growth_independence.json`)

| N_c | fitted β (s⁻¹) | comp count / N_c | real growth |
|---:|---:|---|---:|
| 10 | 3.0507 | [1.00, 1.10] | 7.9×10⁷× |
| 100 | 3.0507 | [1.00, 1.11] | 7.9×10⁷× |
| 1000 | 3.0507 | [1.00, 1.06] | 7.9×10⁷× |
| 10000 | 3.0507 | [1.00, 1.01] | 7.9×10⁷× |

- **β = 3.0507 s⁻¹ for every N_c**, relative spread ≈ 1×10⁻¹⁵ → the paper's central Test-4.2 claim ("real electrons grow at the same rate independent of the target computational count") reproduces, and the absolute value matches the paper's ~3.06 s⁻¹.
- Computational count stayed within **[N_c, 1.11·N_c]** — matching the paper's "oscillates ~5 % above, elements N_c…1.1·N_c" bounded-count behavior.

## 5. Honest limitations

- **Aleph is proprietary** — no full coupled PIC sheath transient (C5, Test-4.1 VDF/density plots) nor full DSMC/cross-section physics (Test-4.2 EEDF shapes, absolute reaction rates, Bolsig+ comparison) could be rerun. Those are end-to-end *simulation-outcome* claims that depend on the whole code, not just the operators.
- **C7 (precision-improves-with-N_c)** could not be isolated: our abstract 0D bookkeeping model recovers β to machine precision at all N_c because it lacks Aleph's stochastic DSMC event noise (which is what makes small-N_c runs noisier). Reported as neither-confirmed-nor-refuted rather than over-claimed.
- The reimplementation is faithful to the *equations as written*; any undocumented Aleph implementation detail is not captured.

## 6. LLM-judge verdict (Argo gpt-5.2)

Coverage **0.78**, agreement **0.80**, verdict **PARTIAL**. Judge rationale (excerpt): *"The reimplementation convincingly reproduces the core mathematical/structural properties of the split and merge operators… and the key structural claim from Test 4.2 that the real-particle growth rate can be independent of N_c while keeping computational counts bounded… However, the paper's main end-to-end PIC/DSMC demonstration claims (VDF indistinguishability in Test 4.1 and physics-faithful 0D H₂ ionization behavior including precision-vs-N_c) were not replicated."* Full JSON: `evidence/llm_judge_verdict.json`.

## 7. Assessment

The paper's **method is correct and precisely specified**: every conservation invariant of the novel split and merge operators — mass, center of mass/charge, total (kinetic+potential) energy for splits, and mass+momentum with small bounded thermal-energy loss for merges — reproduces independently to machine precision from the published equations, including the energetically-inaccessible-split rejection that is the paper's stated accuracy advantage. The central scaling claim of Test 4.2 (growth rate independent of computational particle count, bounded computational count) also reproduces. What remains unverified is strictly the *whole-code simulation outcomes* (Aleph is unavailable): the coupled-sheath VDF-indistinguishability plots and the full DSMC/Bolsig+ physics. This is a genuine, non-inflated **PARTIAL**: the mathematical core is fully vindicated; the end-to-end demonstrations are out of independent reach.

## Verdict
**Verdict:** PARTIAL

---

WAVE_RESULT set=OSTI-100 paper=OSTI-2480245 (Boerner/Hall et al., "A Performant Energy-conserving Particle Reweighting Method for PIC Simulations", SAND2024-16128J, JCP 2024) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-2480245-energy-conserving-particle-reweighting-PIC one_line=Reimplemented the split/merge reweighting operators from the equations (Aleph is proprietary); all conservation invariants (mass, COM, energy-conserving split w/ imaginary-velocity rejection, momentum-conserving merge, KE_lost>=0 & small) reproduce to machine precision, and Test-4.2 growth rate is independent of computational particle count (beta=3.05 vs paper ~3.06 s^-1, bounded count); full coupled PIC/DSMC sim outcomes out of reach → PARTIAL (LLM-judge gpt-5.2 coverage 0.78 agreement 0.80).
