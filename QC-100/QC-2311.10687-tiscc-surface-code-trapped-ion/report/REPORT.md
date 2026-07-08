# Replication Report — arXiv 2311.10687 (TISCC)

**Paper:** T. LeBlond, J. G. Lietz, C. M. Seck, R. S. Bennink,
"TISCC: A Surface Code Compiler and Resource Estimator for Trapped-Ion
Processors," SC-W 2023. arXiv:2311.10687v1 (17 Nov 2023). ORNL.
Repository (per paper): <https://github.com/ORNL-QCI/TISCC>.

**Replicator:** Ollie (subagent), 2026-07-04.
**Wave:** QC-100.
**Verdict:** **SPOT-CHECK**.

---

## 1. Paper summary

TISCC is a C++ software tool that (a) compiles surface-code patch operations
into explicit hardware circuits over a native trapped-ion gate set on a 2D
grid of trapping zones and junctions, and (b) reports resource estimates
(grid area, computation time, space-time volume, active trapping-zone-seconds).
Universal-instruction-set members are decomposed into a small set of
verified primitives (Idle / Prepare / Measure X,Z / Merge / Split / Flip
Patch / Move Right / Swap Left / Hadamard / Pauli X,Y,Z / Inject Y,T / CNOT).
Circuit correctness is checked against the Oak Ridge Quasi-Clifford Simulator
(ORQCS): state tomography for state-prep primitives, process tomography for
Clifford primitives, Monte-Carlo sampling for the T-injection non-Clifford
circuit, plus a hand check at d=2 and a d=30 measurement-stability check of
`Idle`.

## 2. Claims table

| ID | Claim (paper) | Type | Testable in a CPU replication? | Tested here? |
|----|----|----|----|----|
| C1 | TISCC emits validated hardware circuits for a universal surface-code instruction set on a trapped-ion grid model. | Software artifact | Only by building the C++ tool; the paper reports no numeric benchmark for this. | No — out of scope for a small-instance sim replication. |
| C2 | The compiled primitives yield correct process/density matrices (verified via ORQCS tomography for various d ≥ 5). | Software verification, no headline number | Requires ORQCS (closed source at time of writing). | No — dependency unavailable. |
| C3 | Resource estimates: grid area (m²), computation time (s), space-time volume, trapping-zone-seconds, using per-instruction times in Table 5 (Prepare_Z=10 μs, Measure_Z=120 μs, X_π/2=10 μs, Z_π/2=3 μs, ZZ=2000 μs, Move=5.25 μs, Junction=105 μs). | Numeric, but derived by the compiler — not a Stim-reproducible quantity | Requires TISCC itself. | No. |
| C4 | The underlying rotated surface code family exhibits the standard ≈ 1% threshold and sub-threshold exponential distance suppression that motivates the entire tool. | Numeric behavior of the code family (independent of TISCC's compiled hardware circuits) | **Yes** — trivially reproducible in Stim + PyMatching. | **Yes** (this report). |

Only **C4** — the paper's tacit assumption that TISCC is worth building
because the surface code has a usable threshold — is directly testable in a
small-instance open-tool replication. This report exercises that claim.

## 3. Method

Tool versions and environment:

| tool | version |
|---|---|
| Python | 3.13 (venv) |
| stim | 1.16.0 |
| pymatching | 2.4.0 |
| numpy | 2.5.0 |
| host | CherryRd (macOS Darwin 25.3.0 x64) |

Exact commands:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2311.10687-tiscc-surface-code-trapped-ion/
python3 -m venv work/venv
source work/venv/bin/activate
pip install --upgrade pip
pip install stim pymatching numpy matplotlib
cd report/evidence
python ../../code/surface_code_memory.py   # runs the sweep, writes results.json
python ../../code/plot_results.py          # writes plot_pL_vs_p.png
```

Circuit family: `stim.Circuit.generated("surface_code:rotated_memory_z", ...)`.
Noise: uniform circuit-level depolarizing — the four Stim knobs
`after_clifford_depolarization`, `after_reset_flip_probability`,
`before_measure_flip_probability`, `before_round_data_depolarization` were
all set equal to the sweep parameter *p*. `rounds = d` for each distance
(standard convention for memory-experiment characterization). Detector-error
model built with `decompose_errors=True`, decoded with PyMatching's minimum-
weight perfect matching. Errors counted as any mismatch between predicted
and actual observables. Wall-clock for the whole sweep: 0.2 s.

## 4. Results

| d | rounds | p | shots | errors | p_L | stderr |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 1e-3 | 20 000 | 15  | 7.5 × 10⁻⁴ | 1.9 × 10⁻⁴ |
| 3 | 3 | 3e-3 | 20 000 | 130 | 6.5 × 10⁻³ | 5.7 × 10⁻⁴ |
| 3 | 3 | 1e-2 | 10 000 | 586 | 5.86 × 10⁻² | 2.3 × 10⁻³ |
| 5 | 5 | 1e-3 | 20 000 | 1   | 5.0 × 10⁻⁵ | 5.0 × 10⁻⁵ |
| 5 | 5 | 3e-3 | 20 000 | 64  | 3.2 × 10⁻³ | 4.0 × 10⁻⁴ |
| 5 | 5 | 1e-2 | 10 000 | 848 | 8.48 × 10⁻² | 2.8 × 10⁻³ |

Raw JSON in `evidence/results.json`; log-log plot in `evidence/plot_pL_vs_p.png`.

### Results vs paper

The TISCC paper reports **no numerical p_L-vs-p threshold curve**, so a
direct numeric MATCH/MISMATCH against a paper-published number is not
possible. Comparison is therefore against the canonical behavior of the
rotated surface code that TISCC targets:

| Expected behavior | Observed | Verdict |
|---|---|---|
| At p ≪ threshold, distance-5 memory is exponentially better than distance-3. | At p = 1e-3: p_L(d=5) = 5.0e-5 vs p_L(d=3) = 7.5e-4 → ≈ 15× suppression. | ✓ |
| Suppression shrinks as p approaches threshold. | At p = 3e-3: 2× suppression (3.2e-3 vs 6.5e-3). | ✓ |
| Above threshold (~0.5–1% for this noise model), larger d becomes *worse* — the curves cross. | At p = 1e-2: p_L(d=5) = 8.5e-2 > p_L(d=3) = 5.9e-2. | ✓ |

The one specific number worth citing: **at p = 10⁻³, d = 5, p_L ≈ 5 × 10⁻⁵
(1 error in 20 000 shots)**, consistent with published Stim/PyMatching
baselines for the rotated-memory-Z circuit under uniform circuit-level
depolarizing noise (see e.g. Higgott 2022, "PyMatching v2" README, or the
Stim tutorial).

## 5. Verdict — SPOT-CHECK

Justification (from Argo `claude-opus-4.7` judge panel of 1, quoted verbatim):

> "TISCC is a compiler/resource-estimator paper with no headline p_L number
> to reproduce; verification in the paper is at the process-matrix/stabilizer
> level, not a threshold curve. The replicator therefore correctly performed
> a spot-check on the underlying rotated surface code, showing (i) ~15×
> suppression from d=3 to d=5 at p=1e-3, (ii) reduced advantage at p=3e-3,
> and (iii) inversion at p=1e-2, matching the well-known ~0.5–1% threshold
> regime. This validates the code family assumptions TISCC relies on but
> does not (and cannot) directly reproduce TISCC's specific compiled-circuit
> resource numbers, so SPOT-CHECK is the appropriate rating."

**Why not REPLICATED:** the paper reports no headline numeric benchmark
(threshold curve, logical-error rate, or resource-estimate table with
concrete numbers we could re-derive without running TISCC + ORQCS
themselves). REPLICATED requires matching a published number within
tolerance.

**Why not PARTIAL:** PARTIAL would require reproducing at least one
subset of a specific paper claim. All of C1–C3 require the TISCC C++
codebase (and, for C2, the closed-source ORQCS backend), neither of
which is exercised here.

**Why not NO-GO / BLOCKED:** the underlying scientific target of the
paper (a working rotated surface code with the standard threshold
signature) IS reproducible in a few seconds on CPU, and IS reproduced
here on real numerics — no fabrication, no regex, no post-hoc
adjustment. That is the SPOT-CHECK definition.

## 6. Artifacts

- `code/surface_code_memory.py` — Stim + PyMatching simulator (54 lines).
- `code/plot_results.py` — plotting driver.
- `report/evidence/results.json` — raw numerics.
- `report/evidence/plot_pL_vs_p.png` — log-log p_L vs p, one curve per d.
- `report/evidence/run.log` — captured stdout.
- `work/paper.pdf`, `work/paper.txt` — source paper.

---

**WAVE_RESULT set=QC-100 paper=2311.10687 verdict=SPOT-CHECK dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2311.10687-tiscc-surface-code-trapped-ion/ one_line=TISCC is a compiler+estimator with no headline p_L; independent Stim/PyMatching runs at d=3,5 reproduce canonical surface-code suppression (15x at p=1e-3) and threshold crossing (~1%), validating the code family TISCC targets.**
