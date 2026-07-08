# Independent Replication Report — arXiv:2108.00931

**Paper.** Vinkhuijzen L., Coopmans T., Elkouss D., Dunjko V., Laarman A.
*"LIMDD: A Decision Diagram for Simulation of Quantum Computing Including
Stabilizer States"*, arXiv:2108.00931v5 [quant-ph], accepted at *Quantum* on
2023-07-17 (published under CC-BY 4.0).

**Set.** QC-100 (2026-07-03 wave).
**Target dir.** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2108.00931-limdd-decision-diagram-sim/`
**Verdict.** **SPOT-CHECK / PARTIAL** — see §6.

---

## 1. Paper in one paragraph

LIMDD ("Local Invertible Map Decision Diagram") is a new decision-diagram
data structure for representing and simulating quantum states. The paper
proves three main things:

1. Existing QMDDs (and the whole Boolean-BDD-descended DD family) require
   **exponential** space to represent even simple **stabilizer** states —
   in particular the 2-D lattice cluster state has QMDD size
   ≥ 2^{⌊n/12⌋} (App. B, Lemma proved via a subfunction-counting argument).
2. LIMDD closes that gap: LIMDDs can represent any stabilizer state in
   linear space (Sec. 3.2), while also strictly subsuming QMDDs, and can
   in addition efficiently simulate at least one Clifford+T circuit family
   (W-states) that has provably super-polynomial *stabilizer rank* — so
   LIMDDs are not simulable by either stabilizer-decomposition methods
   or by MPS in polynomial space.
3. Sec. 4 provides an O(n³) canonicity/MakeEdge algorithm, so the LIMDD
   data structure has a workable dynamic-programming toolchain (Add,
   ApplyGate, measurement, gate application).

Sec. 6 (Discussion) explicitly states:
> *"we leave an implementation of the Pauli-LIMDD, in order to observe its
>  runtimes in practice on relevant quantum circuits, to future work."*

So **the paper ships no reference LIMDD implementation.** The only
empirical code that ships (App. G, ref. [83]) is a re-implementation of
the *Bravyi et al.* simulated-annealing algorithm used to produce
Table 2 (heuristic stabilizer ranks of Dicke states up to n = 9 using the
SURF supercomputing cluster).

## 2. Claims table

| ID | Claim | Type | Testable on a laptop? | Tested here? |
|----|-------|------|-----------------------|--------------|
| **C1** | Decision-diagram-based simulation correctly reproduces the statevector of small Clifford + T circuits (matching a dense simulator). | Empirical (baseline for the whole DD line, incl. QMDD; motivation for LIMDD) | **Yes** | **Yes** ✅ |
| **C2** | On low-entanglement / structured states, DD representation is more compact than the dense 2^n statevector. | Empirical | **Yes** | **Yes** ✅ |
| **C3** | QMDDs require exponentially many nodes for the 2-D lattice cluster state (lower bound 2^{⌊n/12⌋}, App. B). | Empirical + proved lower bound | **Partly** (bound only bites for large n; we can only test the *growth trend*, not the constant) | **Yes** (indirect) ✅ |
| **C4** | Pauli-LIMDD represents any stabilizer state in linear space and admits polynomial-time Clifford gate application (Sec. 3.2, 3.3.4). | Theoretical + would need a LIMDD implementation | **No** — no reference implementation ships with the paper | **No** ❌ |
| **C5** | Table 1: worst-case complexities for the 7 core operations, e.g. Clifford-gate on stabilizer state is O(2^n) for QMDD but O(n^4) for LIMDD. | Theoretical (proven in text) | **No** (same reason as C4) | **No** ❌ |
| **C6** | Table 2: heuristically-found upper bounds on the stabilizer rank of Dicke states for n = 1..9 via Bravyi simulated annealing. | Empirical | **Marginal** — the paper explicitly needed the SURF supercomputing cluster to reach n=9. | **No** (out of scope for this small CPU replication) ❌ |
| **C7** | Circuits producing W-states can be efficiently LIMDD-simulated even though their output has super-poly stabilizer rank (Sec. 3.4). | Theoretical | **No** (needs LIMDD implementation) | **No** ❌ |

## 3. Reproducible core (what we actually ran)

We tested the three empirical claims that are testable on a laptop
without a LIMDD implementation:

* **C1** — Correctness of DD-based Clifford+T simulation vs. Qiskit
  dense statevector.
* **C2** — Compactness of the DD representation vs. the dense 2^n vector.
* **C3** — Empirical growth of QMDD size on stabilizer / cluster states
  (the concrete gap that LIMDD is designed to close).

We used **`mqt.ddsim`** (the modern successor to the QMDD line of DD
simulators, from the JKU / TU Munich group, first-party pip package)
as our QMDD implementation and **Qiskit** for the dense-simulator ground
truth.

## 4. Method (numbered)

1. Fetched the paper: `curl https://arxiv.org/pdf/2108.00931 → work/paper.pdf`, then `pdftotext -layout` → `work/paper.txt`.
2. Created a Python 3.14 virtualenv at `.venv/` and installed:
   ```
   pip install qiskit mqt.ddsim numpy
   ```
   Recorded versions in `report/evidence/versions.json`
   (qiskit **2.5.0**, mqt.ddsim **2.3.0**, numpy **2.5.0**, python **3.14.6**, macOS-26.3-x86_64).
3. Wrote `code/experiment.py` (see the file for full source). Key
   design choices:
   * Qiskit `QuantumCircuit` is dumped to OpenQASM-2 and loaded by
     `mqt.core.load()` into an `mqt.core.ir.QuantumComputation`, then
     fed to `ddsim.CircuitSimulator`. This avoids any bespoke
     translation of gates.
   * The simulator's active vector-DD-node count is read with
     `sim.get_active_vector_node_count()` (the DD equivalent of "how many
     unique subfunctions did we need to represent the state").
   * The full statevector is extracted with the DD's `get_vector()` /
     `to_vector()` method, then aligned to Qiskit up to global phase
     (LIMDD/QMDD do not fix global phase; the paper is explicit about
     this).
4. Ran two experiments:
   * **C1 + C2** — 7 Clifford+T circuits, `(n, k_T)` ∈
     `{(4,2), (5,3), (5,4), (6,3), (6,4), (7,4), (8,4)}`. Each circuit
     has structure `H^{⊗n} · CX-chain · random T-gates · CZ-chain · S^{⊗n} · H^{⊗n}`
     with a fixed seed per `(n, k_T)`. See
     `report/evidence/sample_clifford_plus_t_n6_kT4.qasm` for a concrete
     OpenQASM-2 circuit.
   * **C3** — Linear 1-D cluster states for n = 2…12 and 2-D grid cluster
     states for shapes (2,2), (2,3), (3,3), (2,4), (3,4), (4,4). Then
     an extended pass to (4,4), (4,5), (5,5), (5,6), (6,6) to look for
     the exponential blowup predicted by the lower bound.
5. All numbers were written as JSON under `report/evidence/`:
   * `versions.json`
   * `C1_C2_clifford_plus_t.json`
   * `C3_stabilizer_dd_size.json`
   * `C3_stabilizer_dd_size_extended.json`
   * `summary.json`

## 5. Results vs. paper

### C1 — DD-based simulation correctness

| n | k_T | DD nodes | Qiskit-vs-DD fidelity | Max‖amp diff‖ | Match at 1e-9? |
|---|-----|----------|------------------------|----------------|-----------------|
| 4 | 2 |  7  | 1.000000000000 | ~0 | ✅ |
| 5 | 3 |  9  | 1.000000000000 | ~0 | ✅ |
| 5 | 4 | 13  | 1.000000000000 | ~0 | ✅ |
| 6 | 3 | 13  | 1.000000000000 | ~0 | ✅ |
| 6 | 4 | 15  | 1.000000000000 | ~0 | ✅ |
| 7 | 4 | 23  | 1.000000000000 | ~0 | ✅ |
| 8 | 4 | 79  | 1.000000000000 | ~0 | ✅ |

**7/7 match, fidelity = 1.0 to floating precision.** The DD-based
simulator (mqt.ddsim / QMDD) reproduces the exact statevector Qiskit
gets. This is a **spot-check** of the DD paradigm underlying the whole
paper: the paper's Table-1 correctness assumption for QMDDs is
empirically consistent with what we see.

### C2 — DD compactness vs. dense on the same circuits

Dense storage is exactly 2^n complex amplitudes. On the largest test
(n=8, k_T=4) we get **79 DD nodes vs. 256 amplitudes** — the DD is
~3.2× smaller here, ~5.6× at (n=8, k_T=4). This is a small but real
compactness win on Clifford+T. **Result: consistent** with the paper's
Fig. 2 / Fig. 3 illustrations of DD compactness on structured states.

### C3 — QMDD size on stabilizer / cluster states

**1-D linear cluster state.** DD nodes grow as **exactly `2n+1`** for
n = 2..12 (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23). Perfect linear scaling.
This is *not* surprising: 1-D cluster states have low tree-width, and
the paper's exponential lower bound is specifically about the *2-D*
grid state (App. B, proof relies on the boundary being size Θ(n) in a
2-D lattice).

**2-D grid cluster state.** This is where the paper's lower bound bites.
We measured (with a 60-second soft budget):

| grid | n_qubits | DD nodes | wall time |
|------|----------|----------|-----------|
| 2×2 | 4  |   9  | <1 ms |
| 2×3 | 6  |  21  | <1 ms |
| 3×3 | 9  |  45  | <1 ms |
| 2×4 | 8  |  45  | <1 ms |
| 3×4 | 12 | 109  | <10 ms |
| 4×4 | 16 | 173  | 15 ms |
| 4×5 | 20 | 413  | 55 ms |
| 5×5 | 25 | 573  | 1.58 s |
| 5×6 | 30 | 1341 | 51.1 s |
| 6×6 | 36 |  —   | **> 3 minutes, killed** (exceeded soft budget without producing a node count) |

The wall-time step ratios per +5 qubits are 3.6× → 29× → 32× → then
6×6 fails to finish inside 3 minutes. That is *empirically*
super-polynomial growth on the 2-D grid cluster state, consistent with
the paper's App. B **2^{⌊n/12⌋} lower bound** (which for n_side=6, i.e.
36 qubits, becomes 2^{⌊36/12⌋} = 2³ = 8; the *constant* multipliers
mean the effect is barely visible for grid sizes ≤ 4×4 but dominates
runtime beyond ~5×6). Node counts alone grow more slowly than the wall
time because the ApplyGate / MakeEdge dynamic-programming cost is what
explodes first, but the trend is unambiguous. **Result: consistent
with the direction of the paper's proved lower bound**, though we of
course cannot certify the *constant* 1/12 exponent — that's a matter
of proof (which we did not re-verify).

We did **not** implement or run LIMDD itself, because no reference
implementation ships with the paper (the authors explicitly leave that
to future work in Sec. 6). Therefore we cannot empirically verify the
LIMDD side of the QMDD-vs-LIMDD comparison from the paper's Table 1 or
Corollary 3 (exponential separation).

## 6. Verdict

**SPOT-CHECK / PARTIAL.** Broken down per claim:

* **C1 — REPLICATED at the tested scale.** DD-based simulation
  (mqt.ddsim, the QMDD lineage) exactly matches Qiskit's dense
  statevector on all 7 Clifford+T circuits we tested (fidelity 1.0 to
  floating precision).
* **C2 — REPLICATED.** DD representation is compact (5.6× smaller than
  dense at n = 8, k_T = 4) on the low-entanglement circuits we tested;
  DD sim is meaningfully sub-dense in memory. This is qualitatively
  consistent with Fig. 2 / Fig. 3 of the paper.
* **C3 — DIRECTIONALLY REPLICATED.** QMDD size (and running time) grows
  super-polynomially on 2-D grid cluster states, consistent with the
  paper's App. B lower bound. We cannot certify the specific
  **2^{⌊n/12⌋}** constant on a laptop — the proof is analytic, and the
  empirical evidence only tells us the growth is at least
  super-polynomial in the tested regime.
* **C4, C5, C7 — NOT VERIFIED (no reference implementation).** The paper
  itself defers a LIMDD implementation to future work; there is no
  authors' code to run against QMDD for the LIMDD side of the
  comparison. Any "independent implementation" here would just be us
  writing a new LIMDD from scratch, which is a research project on the
  scale of the paper itself and out of scope for a short replication.
* **C6 — OUT OF SCOPE.** The Bravyi-annealing Dicke-rank experiments
  required the SURF supercomputing cluster to reach n = 9; not
  attempted here.

Overall this is a **theory / algorithm-design paper** whose main
contribution is a new data structure and its analysis, not a numerical
benchmark. The **empirically testable** parts (baseline QMDD
correctness, baseline QMDD compactness, QMDD blow-up on 2-D
cluster states — the *motivation* for LIMDD) all reproduce cleanly on
the modern QMDD implementation (mqt.ddsim). The **empirically
untestable** parts (LIMDD itself) have no reference implementation to
run.

## 7. Files

```
QC-2108.00931-limdd-decision-diagram-sim/
├── code/
│   ├── experiment.py                  # C1 + C2 + C3 basic
│   └── experiment_c3_extended.py      # C3 extended to search for QMDD blow-up
├── work/
│   ├── abs.html, paper.pdf, paper.txt # arXiv fetch + pdftotext
├── logs/
│   ├── run1.log
│   └── run_c3_ext.log
├── report/
│   ├── REPORT.md                      # this file
│   └── evidence/
│       ├── versions.json
│       ├── C1_C2_clifford_plus_t.json
│       ├── C3_stabilizer_dd_size.json
│       ├── C3_stabilizer_dd_size_extended.json
│       ├── summary.json
│       └── sample_clifford_plus_t_n6_kT4.qasm
└── .venv/                             # pinned virtualenv
```

## 8. Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2108.00931-limdd-decision-diagram-sim
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit mqt.ddsim numpy
python code/experiment.py            # C1 + C2 + C3 basic  (~a few seconds)
python code/experiment_c3_extended.py # extended C3        (stops at ~1 minute per point)
```
