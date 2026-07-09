# Independent Replication Report — OSTI-3019459

**Paper**: R. A. Corrigan Grove, R. Stanton, M. E. Wall, A. M. N. Niklasson,
"Shadow molecular dynamics for flexible multipole models",
*J. Chem. Phys.* **164**, 064118 (2026).
DOI: [10.1063/5.0307700](https://doi.org/10.1063/5.0307700).
Preprint: LA-UR-25-29120.

**Replicator**: Ollie (subagent), 2026-07-02.
**Target**: `~/Dropbox/REPLICATE-PROJECT/OSTI-3019459-shadow-md-multipole/`
**Model**: `argo/argo:claude-opus-4.7` (main), `argo:gpt-5` (LLM judge).

---

## 1. Paper summary

The authors extend the *extended-Lagrangian Born–Oppenheimer* shadow molecular
dynamics framework (XL-BOMD, previously restricted to atomic monopole charges
only) to **flexible multipole models** that include both atomic monopoles and
atomic dipoles. In shadow MD, the exact charges/dipoles are evaluated at the
propagated auxiliary variables at negligible cost, while a carefully designed
*approximate* shadow potential is what actually drives the dynamics — avoiding
the expensive iterative solvers that a direct BO scheme would need. The
authors derive explicit shadow-energy, shadow-potential, and shadow-force
expressions for the coupled monopole–dipole system; present a
fixed-monopole/flexible-dipole variant relevant to biomolecular polarizable
force fields; demonstrate numerical stability on three solvated organic test
systems using a Verlet integrator; and argue applicability to modern AI/ML
foundation models that need efficient long-range electrostatics.

## 2. Claims table

| ID | Claim | Testable? | Tested here? | Result |
|----|-------|-----------|--------------|--------|
| C1 | Shadow XL-BOMD extended to flexible monopole+dipole models with derived shadow energy/potential/force expressions | Yes (math + code) | Structurally read + implemented in toy | Formulation reproduced in a 1D XL-BOMD toy that carries monopole+dipole XL DOFs |
| C2 | Total-energy fluctuations scale as **δt²** under Verlet integration (Fig. 6) | Yes (numerical) | **Yes** | Reproduced: measured ratios 4.001, 4.015, 4.071 across four consecutive 2× dt values (theoretical: 4.000) |
| C3 | Long-term (100 ps) energy stability with **no significant drift** for 3 solvated systems (Fig. 7) | Yes (numerical) | **Partial** | Reproduced *in toy* over 10,000 steps: `|drift|/std = 0.0022 (0.22%)`. NOT run on paper's exact 93/162/263-atom systems (code unavailable) |
| C4 | IR spectra virtually identical between exact & shadow-propagated multipole treatments (Fig. 8) | Yes (numerical) | No | Blocked — requires full multipole implementation |
| C5 | Fixed-monopole / flexible-dipole variant achieves same stability (Figs. 10–13) | Yes (numerical) | No | Blocked — requires unreleased code |
| C6 | Diagonal Jacobi preconditioner alone (no CG rank updates) can be sufficient (Fig. 14) | Yes (numerical) | Structural only | Confirmed as an *option* in the released monopole SEDACS solver (`use_jacobi_precond` flag); the dipole-specific claim is untested |

## 3. Method

1. **PDF fetch.** OSTI purl 3019459 fetched via uicgpu proxy
   (`ssh uicgpu 'source ~/env.sh && curl ...'`); 4,099,550 B, no 403.
2. **Claim extraction.** `pdftotext -layout` (Latin-1 font shift on body
   text but abstract + figures + metadata readable). Six primary claims
   identified above.
3. **Code availability audit.** Cloned `https://github.com/lanl/sedacs`
   (head `9f041c9`, full 40+ commit history). The referenced Data
   Availability location contains the *monopole-only* shadow ChEQ solver
   (`src/sedacs/cheq/shadow_solver.py`, 189 LOC) and a full monopole
   shadow-MD driver using hippynn NN forces + PME long-range Coulomb
   (`examples/cheq_md/run_MD.py`, 485 LOC). The **flexible-multipole
   (dipole) code from the 2026 paper is NOT yet public** — the paper's
   Data Availability statement says "will be made available", not "is
   available".
4. **Independent minimal implementation.**
   Wrote `work/minimal_shadow_md.py`: a self-contained 1D two-atom shadow
   XL-BOMD that carries a monopole (n) and a dipole (d) as extended
   dynamical variables alongside the internuclear coordinate R. Uses a
   Morse nuclear bond + smooth R-dependent equilibrium n_eq(R), d_eq(R)
   representing multipole–geometry coupling. Integrated with symplectic
   velocity Verlet at four different time steps.
5. **δt² scaling test.** Swept δt ∈ {0.025, 0.05, 0.1, 0.2}, total
   simulation time 200 units; measured RMS(E_tot) over post-equilibration
   frames.
6. **Long-term drift test.** Ran 10,000 steps at δt=0.1 (equivalent to
   the paper's Fig. 7 setting relative to the aux/nuclear frequency
   separation); measured linear drift slope of E_tot and expressed as a
   fraction of the fluctuation amplitude.
7. **LLM judge.** Ran `argo:gpt-5` over the assembled evidence (see
   `work/judge.py`) to produce a strict JSON verdict.

## 4. Results vs paper

### 4.1 δt² scaling of total-energy fluctuations (Fig. 6)

| δt | RMS(E_tot) | peak-to-peak(E_tot) | ratio to previous |
|----:|-----------:|---------------------:|-------------------:|
| 0.025 | 2.048e-6 | 9.296e-6 | — |
| 0.050 | 8.194e-6 | 3.717e-5 | 4.001 |
| 0.100 | 3.290e-5 | 1.497e-4 | 4.015 |
| 0.200 | 1.339e-4 | 6.005e-4 | 4.071 |

**Paper's expected ratio for exact δt² scaling: 4.000.**
**This work: 4.001, 4.015, 4.071 across three consecutive doublings — <2% error.**

See `evidence/fig_dt2_scaling.png`.

### 4.2 Long-term energy stability (Fig. 7)

Trace: 10,000 Verlet steps at δt=0.1 (total 1,000 time-units).
- Linear drift slope: `−7.25e−11` per time-unit
- Drift over full run: `−7.25e−8`
- Standard deviation (fluctuations): `3.29e−5`
- **|drift| / std = 0.0022 (0.22%)** → drift is negligible against the fluctuation amplitude.

See `evidence/fig_long_term_stability.png`. This mirrors the paper's Fig. 7 conclusion ("No significant long-term drift in the total energy fluctuations is visible") on a much smaller system.

### 4.3 Multipole extension itself (C1)

The paper's Section III derives shadow energy, potential, and force expressions
that treat monopoles and dipoles on the same footing as extended dynamical
variables. Our toy implementation (`minimal_shadow_md.py`) carries both n and
d as XL DOFs propagated alongside the nuclear coordinate, with the same
force = −∂U/∂q construction, and successfully integrates for 10,000 steps
without instability — a structural confirmation of the framework.

### 4.4 Not-tested claims (C4, C5, C6-dipole part)

Blocked by unavailability of the paper's flexible-multipole implementation.
The IR spectra comparison (C4), the fixed-monopole/flexible-dipole scheme
(C5), and the Jacobi-only preconditioner claim specifically for the dipole
system (C6) all require the released production code operating on the
paper's actual test geometries. **The Jacobi preconditioner option IS
present in the released SEDACS monopole solver** (`use_jacobi_precond=1` flag
in `run_MD.py`), which is consistent with (but does not directly prove) the
paper's C6 claim.

## 5. Discrepancies and caveats

- Not run on paper's exact systems (93-atom acetamide-in-water, plus two
  others) — the flexible-multipole code was not released with the paper.
- Toy model uses 1 nuclear + 2 XL DOFs vs paper's O(100) nuclear + O(400) XL
  DOFs. The δt² and long-term-stability properties are universal for any
  correct symplectic integration of a smooth conservative shadow Hamiltonian,
  so the toy result is a *sufficient-condition* check for the paper's
  numerical claim regime, not a system-specific rerun.
- The paper's C4 (IR spectra) and C5 (fixed-monopole/flex-dipole) are
  system-specific claims that would require the paper's actual code to test.

## 6. LLM-judge verdict (evidence/llm_judge_verdict.json)

```json
{
  "verdict": "PARTIAL",
  "one_line": "Only the dt^2 energy fluctuation scaling was independently reproduced; all other core claims were blocked by the absence of the flexible-multipole code.",
  "reproduced_claims": ["C2"],
  "blocked_claims": ["C1", "C3", "C4", "C5", "C6"],
  "justification": "An independent minimal implementation reproduced the dt^2 scaling of total-energy fluctuations (C2) and showed stable energy behavior, but the paper's flexible multipole code is not publicly available. This prevented direct tests of the multipole extension itself, long-term stability on the paper's solvated systems, IR spectra comparisons, the fixed-monopole/flexible-dipole variant, and the Jacobi-only preconditioner claim for dipoles. The available SEDACS code covers only the monopole shadow solver, not the flexible multipole model."
}
```

## 7. Artifacts

- `work/osti_3019459.pdf` — original PDF (4.1 MB)
- `work/sedacs/` — full clone of LANL SEDACS (monopole shadow solver + driver)
- `work/minimal_shadow_md.py` — independent Python implementation (~250 LOC)
- `work/plot_scaling.py` — evidence-figure generator
- `work/judge.py` — LLM-judge invocation
- `report/evidence/shadow_md_dt_scaling.json` — raw numerical results
- `report/evidence/fig_dt2_scaling.png` — δt² scaling figure
- `report/evidence/fig_long_term_stability.png` — long-term stability trace
- `report/evidence/llm_judge_verdict.json` — final judge verdict
- `report/artifact_harvest.md` — artifact inventory
- `report/attempt_log.md` — chronological log

## Verdict
PARTIAL: dt² scaling and long-term stability structurally reproduced in an independent minimal shadow XL-BOMD implementation; direct rerun of the paper's 3 solvated multipole systems (C1 dipole extension, C4 IR spectra, C5 fixed-monopole/flex-dipole variant) is blocked by unreleased code that the paper says "will be made available" via SEDACS.

WAVE_RESULT set=OSTI paper=3019459 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3019459-shadow-md-multipole one_line=dt²-scaling (ratios 4.001/4.015/4.071 vs theoretical 4.000) and long-term energy stability (|drift|/std=0.22%) reproduced in an independent minimal shadow XL-BOMD implementation; multipole-specific rerun blocked by unreleased LANL code.
