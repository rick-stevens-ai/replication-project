# Failure analysis — CS-VQE replication (arXiv:2011.10027)

**Verdict: REPLICATED, but read the limitations. The headline claim is
exercised only on the paper's smallest molecule; the practical case
(large molecules, real hardware, noise) is *not* independently
established here.**

## What we actually did vs what CS-VQE actually promises

The paper's practical claim is that CS-VQE lets near-term quantum
hardware handle molecules that full VQE cannot, by shrinking the
number of qubits needed on the QPU. We verified the *algorithmic
mechanism* on H2/STO-3G by exhaustively enumerating noncontextual
Pauli-term partitions and diagonalizing the resulting projected
Hamiltonians. That confirms the math but does not confirm the
practical case. Below is the honest gap between what we tested and
what a fair evaluator would demand.

## Limitation 1 — No VQE optimization loop was actually run

We take the paper's own explicit shortcut: "quantum corrections were
simulated classically by directly evaluating the lowest eigenvalues of
the Hamiltonians restricted to the noncontextual ground states." That
means no parameterized ansatz, no classical optimizer, no measurement
sampling, no shot-noise, no barren-plateau behavior. All results are
noise-free classical linear algebra on a matrix small enough
(4-qubit -> 16x16) to eigendecompose exactly.

**Impact:** we cannot say whether a *real* VQE on the reduced-qubit
CS-VQE circuit would converge to the projected ground state, or how
fast, or how many shots are needed. The paper's Fig. 3 also mostly
avoids this (measurement-count claim is about term counts, not shot
budgets).

## Limitation 2 — Only H2/STO-3G was tested end-to-end

The paper's real punchline is Fig. 2 (LiH, H2O, N2, ..., all at
STO-3G+JW) showing qubit-reduction ratios of 2--3x across molecules
too large for full-state simulation. We did not reproduce Fig. 2. Our
H2 result (q=1 vs 4, ratio 4x) is better than the paper's overall
claim of ">2x", but H2 is trivially small: even the full Hamiltonian
is a 16x16 eigenvalue problem, so "qubit reduction" for H2 is a
theoretical curiosity, not a practical enabler.

**Impact:** the *interesting* claim -- that the qubit-reduction ratio
survives at LiH/H2O scale where full VQE is already hard -- is
untested here. Reproducing it requires either much bigger
classical eigensolves (LiH is 12 qubits = 4096-dim, still feasible;
H2O is 14 qubits = 16384-dim, feasible but slower) or an actual
CS-VQE run with an ansatz, which was out of scope.

## Limitation 3 — Only closed-shell singlet in minimal basis

H2 at 0.7414 A with STO-3G and Jordan-Wigner is the easiest possible
test case: single closed-shell determinant, weakly-correlated,
minimal basis. The noncontextual model's accuracy on radicals,
transition-metal complexes, larger active spaces, or stretched-bond
strongly-correlated geometries was not tested. Rick's candidate-probe
list explicitly flags open-shell extensions as an open question --- see
`open_questions.json` #1 and #3.

**Impact:** we have no independent evidence about whether CS-VQE
degrades gracefully or catastrophically for the systems where quantum
advantage would actually matter (multireference, strong correlation).

## Limitation 4 — Exhaustive partition search, not the paper's heuristic

Our H2 headline uses the best partition found by exhaustive
enumeration of all 2^15 = 32,768 term subsets (6,015 turned out to be
noncontextual). This is intractable beyond ~20 terms. The paper puts
significant weight on their Section 3 greedy heuristic; we did not
implement or test that heuristic, so we cannot say whether it finds
our optimal H2 partition or how it scales.

**Impact:** our q=1 headline is an upper bound on what CS-VQE can
achieve; whether the *deployable* CS-VQE (with a heuristic partition
search) hits the same q is not verified.

## Limitation 5 — No noise model

Real quantum hardware has T1/T2 decoherence, readout error, gate
error, crosstalk, and calibration drift. All our simulations are
noiseless. The whole near-term-hardware case for CS-VQE rests on the
smaller circuit being *more noise-robust* than the full-qubit VQE,
but we have zero evidence on that -- see `open_questions.json` #5.

**Impact:** if CS-VQE's smaller circuit has *lower* fidelity per gate
(because the reduced-qubit Hamiltonian has more non-local Pauli
strings from the projection?), the whole reduction could be
noise-negative. This is directly untested.

## Limitation 6 — No comparison against modern qubit-reduction alternatives

Z2 tapering (Bravyi et al. 2017), Fermion-to-qubit mapping choice
(BK, parity, ternary tree), and active-space reduction (frozen-core,
CASSCF) all reduce qubit count too. We did not compare CS-VQE to any
of them, nor test composition (see open question #2). Without that
comparison, the practical value proposition of CS-VQE vs a modern
combined pipeline is unclear.

## Limitation 7 — Only one JW mapping

Bravyi-Kitaev and parity mappings produce different Pauli
Hamiltonians with different anticommutation structure. Whether CS-VQE
reductions are consistent across mappings, or whether one mapping is
strictly better for CS-VQE, is not tested here.

## Limitation 8 — Seed sensitivity of Section 2.4 not scanned

The Sec. 2.4 mean errors are stable at n=500 (0.2537 / 0.0261) and
n=10,000 (0.2558 / 0.0267), so the seed does not dominate. But we
only ran one seed (20260703). A proper replication would report
multiple seeds and their spread to show the mean is a property of the
family geometry, not of any one draw. (We argue this in the report but
did not measure it.)

## Honest overall assessment

CS-VQE's *mathematical* framework is correctly stated and reproducible
from the paper. Both quantitative claims we could test on a laptop
CPU landed within 0.5% of paper values. The paper is honest, its
math is right, and its shortcut (classical simulation of the "quantum"
correction) is documented up front.

But the practical near-term-hardware case -- (i) the reduction
survives at deployment-relevant molecule size, (ii) it composes with
modern tapering/mapping tricks rather than being redundant to them,
(iii) the reduced circuit is actually more noise-robust when run on
real hardware, (iv) the heuristic partition search finds near-optimal
partitions at scale -- rests on downstream work that this replication
does not touch. Read the verdict as "the paper reproduces on the
paper's smallest example on an independent stack", not as "CS-VQE has
been re-validated as a near-term-hardware method".

## Where this leaves us

* Verdict preserved: **REPLICATED**. The headline reduced-qubit VQE
  energy for H2/STO-3G was independently reproduced to numerical
  precision at q=1.
* Confidence in *practical near-term deployment case*: not
  independently established here.
* Five concrete follow-ups in `open_questions.json` (open-shell,
  taper composition, strongly-correlated, ML partition, noise
  robustness) would close the biggest gaps.
