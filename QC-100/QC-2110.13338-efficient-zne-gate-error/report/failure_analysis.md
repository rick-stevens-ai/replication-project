# Failure analysis — honest critique

Independent replication of arXiv:2110.13338 (Pascuzzi, He, Bauer, de Jong,
Nachman, 2022) — *Computationally Efficient Zero Noise Extrapolation for
Quantum Gate Error Mitigation*.

Verdict on record: **REPLICATED** (headline C1–C4 on the Fig 2/3 example).
This document lists, plainly, what that verdict does and does not cover.

## What was actually demonstrated
1. Raw `Pr(|11>)` under two-qubit depolarising (ε=1%) + amplitude damping
   (T₁=50 µs, T_CNOT=200 ns) on the paper's Fig 3 CNOT-ladder circuit
   decays from 0.97 (n_c=2) to 0.68 (n_c=30) — qualitatively matching the
   paper's Fig 2 raw curve. (C1 ✓)
2. A full-ZNE recipe (Richardson, 3 scale factors {1,2,3}, global folding)
   pulls the extrapolated observable back near 1: mean 1.005, MAE 0.056
   across 11 CNOT points. (C2 ✓)
3. An efficient-ZNE recipe (linear, 2 scale factors {1,3}, random-gate
   folding) achieves MAE 0.048 at 66.7 % of the shot cost of the full
   recipe. (C3 ✓)
4. Across three shot budgets {4096, 8192, 16384}, 30 trials each at
   n_c=10, the efficient recipe has ~3× smaller empirical standard
   deviation than the full recipe at equal shots. That reproduces the
   qualitative message of the paper's Eqs. 10–11. (C4 ✓ qualitatively)

## What was NOT demonstrated
### (a) Independent reimplementation of "efficient ZNE"
The "efficient" arm here is `mitiq.zne.LinearFactory` +
`fold_gates_at_random`, which is spiritually SIIM/LIIM (fewer scales,
gate-local folding), but is **not** a line-by-line implementation of the
LIIM/SIIM formulae in Section III of the paper. The paper's efficiency
claim is reproduced at the *recipe level* — a lighter recipe wins at
reduced cost — not by re-deriving the paper's estimator from scratch and
matching it against the Mitiq implementation on a common noise model.

### (b) Variance-vs-shots was reproduced qualitatively, not quantitatively
The 30-trial precision study confirms that the lighter recipe has lower
per-shot variance than the heavier one at n_c=10. It does **not** compare
the empirical variance against the closed-form prediction of Eq. 10 or
Eq. 11 in the paper. So "Eqs. 10–11 hold on our simulator" is a claim
this replication does not make; only "the ordering they predict holds"
is verified.

### (c) No generic-ZNE (no-folding) baseline
Both arms use folding-based scale-factor synthesis. A stronger test would
be a Richardson or linear extrapolation implemented against a true
identity-insertion RIIM or a pulse-stretch-style noise scaling. That was
not performed. The comparison here is between two folding recipes of
different weights, not between "the paper's method" and "generic ZNE".

### (d) Single noise model, single ε
Only one noise recipe (ε=1 % two-qubit depolarising + T₁=50 µs amp
damping) at one ε was tested. The paper motivates the efficient variants
across families of gate-error models. No ε sweep, no coherent
over-rotation channel, no biased Pauli noise, no biased T₂/T₁ ratio.
Robustness of the efficiency claim under those perturbations is unknown
from this replication.

### (e) Small instance only
n_c ≤ 30 CNOTs on 2 qubits. The paper motivates efficient variants for
near-term devices where sample cost matters at much larger n_c and qubit
count. The claimed scaling advantage at that regime was not demonstrated
here.

### (f) No hardware
All results are simulator-only. Real device runs would introduce
readout error, spectator/idle noise, and time-varying calibration —
none of which appear in this replication.

### (g) C5 and C6 not tested
- **C5 (LIIM per-CNOT list):** requires per-CNOT noise assignment; the
  paper's own Section III.A construction would need to be built out.
  Not done.
- **C6 (parallel RIIM across devices):** requires a multi-backend
  simulation harness or actual hardware. Not done.

### (h) Nougat/OCR extraction stub
The `extraction/nougat.mmd` file is a stub. Nougat was not run against
this paper in the original attempt — `work/paper.txt` was extracted
via `pdftotext -layout`, and that plain-text extraction was sufficient
to locate the noise recipe and circuit family. A proper Nougat pass
would be needed if we wanted machine-readable versions of Eqs. 10–11
for the quantitative variance check flagged in (b).

## Net honest assessment
The paper's headline efficiency claim (a lighter ZNE recipe can match a
heavier one at reduced sampling cost on the Fig 2/3 target under the
paper's own noise recipe) is reproduced on an independent software stack.
That is a genuine result and justifies the REPLICATED verdict — the
headline exercise passes.

The tighter claims — the LIIM/SIIM formulaic derivation, quantitative
match to Eqs. 10–11 coefficients, robustness across noise families,
multi-device parallel RIIM, scaling behaviour at practically relevant
depth and width — are **not** exercised by this replication, and any of
them could in principle fail without contradicting the number we
reproduced. The five open questions in `open_questions.json` map
directly onto (a)–(h) above and are the concrete next steps to close
each remaining gap.
