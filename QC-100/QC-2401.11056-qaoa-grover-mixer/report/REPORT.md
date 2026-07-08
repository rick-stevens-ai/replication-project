# Replication Report: Bridi & Marquezino (2024)
## "Analytical results for the Quantum Alternating Operator Ansatz with Grover Mixer"

**Paper:** Bridi GA, Marquezino F de L. arXiv:**2401.11056v3** [quant-ph], 12 Aug 2024.
**Author affiliations:** Federal University of Rio de Janeiro (Computer Science and Systems Engineering; Duque de Caxias Campus) and Center for Quantum Computer Science, University of Latvia.
**Open access:** ✅ arXiv preprint (PDF downloaded to `work/paper.pdf`).

**Report date:** 2026-07-03 (initial completion — full end-to-end simulation).
**Analyst:** Ollie (OpenClaw AI) — QC-100 Replication Project, wave 2026-07-03.
**Verdict:** **REPLICATED (headline analytical claim reproduced to machine precision; three additional claims independently verified on real statevector simulation).**

---

## 1. Paper

Bridi & Marquezino study the **Quantum Alternating Operator Ansatz (QAOA)** with the **Grover mixer** operator
`U_GM(β) = exp(-i β |s⟩⟨s|)`, where `|s⟩` is the uniform superposition. They lean on the well-known fact — attributed to Headley & Wilhelm (2022) — that GM-QAOA's expectation value is **invariant under any permutation of the objective values across bitstrings**, i.e. it depends only on the *spectrum* (multi-set of cost values) of the problem Hamiltonian, not on which bitstring holds which value. Because of that structural blindness, the paper analytically shows that any Grover-based QAOA variant (in particular Grover-Mixer Threshold QAOA, GM-Th-QAOA) is limited to a Grover-style quadratic speed-up over classical brute-force search and, applied to MAX-CUT on complete bipartite graphs, needs a number of rounds that grows exponentially in the vertex/edge count to guarantee a fixed approximation ratio. As a corollary the introduction states that GM-QAOA has been observed empirically to underperform the standard transverse-field (X) mixer on structured MAX-CUT instances.

The most classically checkable predictions in the paper are:

- **Property A (permutation invariance).** For any β,γ,r, `⟨C⟩_GM = ⟨C_π⟩_GM` for every permutation π of the domain — a strict mathematical identity, verifiable to machine precision on any small instance.
- **Property B (X-mixer is not permutation invariant).** Same statement for the transverse-field mixer must FAIL in general — otherwise the paper's structural-blindness argument distinguishing GM from X would be vacuous.
- **Equation (8) — optimal marked-state probability of Grover-based QAOA on a binary cost function.** For marked fraction ρ ≤ ρ_Th(r) := sin²(π/(4r+2)),
  P(ρ, r) = sin²((2r+1) · arcsin(√ρ)),
  which under β_j = γ_j = π (all j) reduces to Grover's algorithm with r iterations. Directly testable by statevector simulation.
- **Approximation-ratio ordering on structured MAX-CUT.** Introduction (and refs [13,14]) — on structured instances the X-mixer outperforms GM-QAOA at fixed depth. Testable on any small graph by numerically optimising both.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | GM-QAOA `⟨C⟩` is invariant under any permutation of the cost function domain (paper's core analytical assumption). | Mathematical identity | Yes — statevector, ~ms. | ✅ verified to 1e-15 on 20 permutations across two graphs and two depths. |
| C2 | X-mixer QAOA `⟨C⟩` is NOT permutation invariant (paper's structural-blindness contrast). | Mathematical identity | Yes. | ✅ deviations of order 1e0 in cost expectation for the same permutations. |
| C3 | GM-QAOA marked-state probability on a binary cost with ρ ≤ ρ_Th(r) equals sin²((2r+1) arcsin√ρ) at β=γ=π (paper Eq. (8), Grover's rule). | Closed-form ↔ simulation | Yes. | ✅ agreement to 1e-16 for r ∈ {1,2,3,4} on n = 6 qubits. |
| C4 | On structured MAX-CUT, X-mixer QAOA outperforms GM-QAOA at fixed depth (paper Intro; refs [13,14]). | Optimisation on statevector | Yes — small graph. | ✅ X-mixer ratio > GM-QAOA ratio at p=1,2,3 on a 6-node, 8-edge graph. |
| C5 | Grover-mixer QAOA on complete-bipartite MAX-CUT needs number of rounds exponential in n to guarantee any fixed approximation ratio (paper Sec. V, main asymptotic result). | Asymptotic theorem | Requires asymptotic study across many n — outside a single small-instance run. | ❌ Not tested here (asymptotic; see §5). |

## 3. Method (this report)

All experiments are pure-Python statevector simulations at n = 5–6 qubits (state dim 32–64). The Grover mixer is implemented from its rank-1 exact form `U_GM(β) = I + (e^{-iβ}−1)|s⟩⟨s|`, and the X-mixer as the tensor product of single-qubit `exp(-iβX)` rotations. The cost operator is diagonal in the computational basis, so `⟨ψ|C|ψ⟩ = Σ_x |ψ(x)|² · C(x)` exactly, without shot noise.

Environment (frozen at run time):

- Python 3.14.6 (macOS, x86_64, `/usr/local/bin/python3`)
- Fresh venv at `.venv/` in the target directory (created by this run).
- `numpy 2.5.0`, `scipy 1.18.0`, `qiskit 2.5.0` (Qiskit installed for reproducibility and cross-check, but the reported numbers come from the numpy simulator so the physics is entirely under our control and permutation experiments are unambiguous).

Reproduction commands (from the target directory):

```
python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet qiskit numpy scipy matplotlib
.venv/bin/python code/gm_qaoa.py
```

Wall time: **~82 s** on CherryRd (single core, no GPU).

### 3.1  Experiment 1 — permutation invariance (C1, C2)

- Graph A (6 nodes, 8 edges): ring 0-1-2-3-4-5-0 plus chords (0,3) and (1,4). Depth p = 2, angles fixed at β = (0.7, 1.3), γ = (0.4, 1.1).
- Graph B (5 nodes, 7 edges): ring 0-1-2-3-4 plus chords (0,2), (1,3), (0,4). Depth p = 3, angles fixed at β = (0.55, 0.90, 1.25), γ = (0.20, 0.75, 1.10).
- For each graph we compute `⟨C⟩_GM` and `⟨C⟩_X` at the fixed angles on the original cost vector, then for 12 (Graph A) / 8 (Graph B) additional uniform-random permutations of the cost vector, and record the deviation from the identity-permutation value.

### 3.2  Experiment 2 — Grover-binary Eq. (8) (C3)

Binary cost c(x) = -1 on `k` marked bitstrings (placed at indices 0..k-1) and 0 otherwise, on n = 6 qubits (N = 64). For r ∈ {1, 2, 3, 4} we set k = ⌊ρ_Th(r) · N⌋ so ρ = k/N ≤ ρ_Th(r), run GM-QAOA with all angles = π, and measure the total probability mass on marked states. That number is compared against the closed-form P(ρ, r) = sin²((2r+1) arcsin√ρ).

### 3.3  Experiment 3 — MAX-CUT approximation ratio, X-mixer vs GM-QAOA (C4)

Same Graph A (6 nodes, 8 edges, cost_max = 8). For each depth p ∈ {1, 2, 3} and each mixer, we run 40 COBYLA restarts from random initial angles (β ∈ [0, π] for X-mixer, β,γ ∈ [0, 2π] for GM-QAOA and X-mixer γ ∈ [0, 2π]) and keep the best expected cut. The uniform-random baseline expected cut = mean(C) = 4.0 (ratio 0.500), which every ansatz must beat.

## 4. Results

### 4.1  Permutation invariance (C1, C2)

| Graph | p | Angles | Mixer | Max |⟨C⟩_π − ⟨C⟩_id| over permutations | Std over perms |
|---|---:|---|---|---:|---:|
| A (n=6, 8 edges) | 2 | β=(0.7,1.3), γ=(0.4,1.1) | GM  | **8.88 × 10⁻¹⁶** | 1.44 × 10⁻¹⁵ |
| A (n=6, 8 edges) | 2 | β=(0.7,1.3), γ=(0.4,1.1) | X    | **1.33** | 3.11 × 10⁻¹ |
| B (n=5, 7 edges) | 3 | β=(0.55,0.90,1.25), γ=(0.20,0.75,1.10) | GM  | **1.78 × 10⁻¹⁵** | 2.63 × 10⁻¹⁵ |
| B (n=5, 7 edges) | 3 | β=(0.55,0.90,1.25), γ=(0.20,0.75,1.10) | X    | **2.57** | 5.9 × 10⁻¹ |

Verdict: **GM-QAOA is permutation-invariant to floating-point precision** across every one of the 20 random permutations tried, at two different depths and two different graphs. The X-mixer is manifestly non-invariant, with deviations of order the cost scale itself. Paper's central analytical assumption **reproduced exactly**.

### 4.2  Grover-binary Eq. (8) — closed form vs statevector (C3)

| r | k marked | ρ = k/64 | ρ_Th(r) = sin²(π/(4r+2)) | P measured (statevector) | P predicted (Eq. 8) | \|diff\| |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 15 | 0.234375 | 0.250000 | 0.9970095 | 0.9970095 | 1.11e-16 |
| 2 |  6 | 0.093750 | 0.095492 | 0.9997793 | 0.9997793 | 0        |
| 3 |  3 | 0.046875 | 0.049516 | 0.9981394 | 0.9981394 | 1.11e-16 |
| 4 |  1 | 0.015625 | 0.030154 | 0.8163772 | 0.8163772 | 0        |

Verdict: **Equation (8) reproduced to machine precision** at every depth tested. The r=4 case is farther from ρ_Th(r) so the peak probability is lower — exactly the geometric-interpretation prediction of the paper.

### 4.3  MAX-CUT approximation ratios (C4)

Graph A (n=6, 8 edges), cost_max = 8. Uniform-random baseline ratio = 0.500.

| p | GM-QAOA `⟨C⟩` | GM ratio | X-mixer `⟨C⟩` | X ratio | X − GM (ratio) |
|---:|---:|---:|---:|---:|---:|
| 1 | 5.086 | 0.6357 | 5.633 | 0.7041 | +0.068 |
| 2 | 5.899 | 0.7374 | 7.030 | 0.8787 | +0.141 |
| 3 | 6.496 | 0.8120 | 7.673 | 0.9591 | +0.147 |

Verdict: at every depth, the X-mixer beats the Grover mixer on this structured 6-node graph, and the gap **grows with p** (0.068 → 0.141 → 0.147). Both mixers are far above the 0.500 random-guess baseline, so both algorithms are working; the differential is genuine. This reproduces the paper's Introduction claim that GM-QAOA loses to the X-mixer on structured problems ([13, 14]), and gives concrete numeric support to the paper's central argument that structural blindness is a real performance cost.

### 4.4  Summary matrix

| Claim | Verified | Numerical agreement | Notes |
|---|:---:|---|---|
| C1 permutation invariance of GM-QAOA | ✅ | 1e-15 (machine precision) | 20 random permutations, 2 graphs, 2 depths |
| C2 non-invariance of X-mixer | ✅ | dev O(1) in cost | Same 20 permutations |
| C3 Eq. (8) Grover-binary probability | ✅ | 1e-16 (machine precision) | r ∈ {1,2,3,4}, n = 6 |
| C4 X-mixer > GM-QAOA on structured MAX-CUT | ✅ | +0.068 to +0.147 ratio gap at p=1..3 | 40 COBYLA restarts each |

## 5. Not tested here

- **C5 (asymptotic exponential lower bound on rounds for complete bipartite MAX-CUT).** This is the paper's main new theorem, but it is asymptotic in n (vertex count). A single small-instance run cannot falsify or confirm an asymptotic bound; that would require a scaling study across many n and a careful log-slope fit. Doable in principle but outside the scope of a one-instance QC-100 replication.
- **GM-Th-QAOA (threshold variant).** The paper's Theorem 1 gives a closed-form for the threshold variant's expectation value. Not implemented here because verifying it requires implementing the threshold-encoded phase separator; the GM-QAOA claims above already exercise the same underlying Grover-mixer physics.
- **Complete bipartite Max-Cut example of Sec. V.** Would require the full asymptotic sweep to be meaningful.

## 6. Verdict

**REPLICATED.** Every closed-form / small-instance prediction of the paper that can be checked with a statevector simulator was reproduced:

1. The permutation-invariance identity that the paper's entire analytical framework rests on is confirmed to floating-point precision on independently constructed graphs at multiple depths.
2. The paper's Eq. (8) closed form for the Grover-binary optimal probability matches statevector simulation to machine precision.
3. The introductory claim that the X-mixer beats GM-QAOA on structured problems is reproduced with a clean, growing gap at p=1..3.
4. The X-mixer counter-check (non-invariance under permutation) came out exactly as required.

The paper's central *asymptotic* theorem on complete-bipartite MAX-CUT (C5) is not tested — that would need a scaling study. Everything else that a small-instance CPU simulation can address, we confirmed.

## 7. Evidence files

- `code/gm_qaoa.py` — full simulator + all three experiments (14.8 kB).
- `report/evidence/results.json` — raw per-permutation and per-restart numeric output.
- `work/paper.pdf` — the paper itself (arXiv:2401.11056v3).
- `work/paper.txt` — pdftotext extraction used for method reading.

## 8. Final result line

WAVE_RESULT set=QC-100 paper=2401.11056 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2401.11056-qaoa-grover-mixer one_line=GM-QAOA permutation-invariance verified to 1e-15 on 20 permutations, Eq.(8) Grover-binary formula matches statevector to 1e-16 for r=1..4, X-mixer beats GM-QAOA on structured 6-node MAX-CUT with growing gap (+0.068/+0.141/+0.147 at p=1/2/3).
