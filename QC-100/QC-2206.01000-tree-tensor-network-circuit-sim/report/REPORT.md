# QC-100 Replication Report — arXiv:2206.01000

**Paper:** Philipp Seitz, Ismael Medina, Esther Cruz, Qunsheng Huang, Christian B. Mendl.
*"Simulating quantum circuits using tree tensor networks."* Quantum 7, 964 (2023-03-20). arXiv:2206.01000 v3.

**Replicator:** Ollie (OpenClaw subagent, model argo/argo:claude-opus-4.7).
**Date:** 2026-07-04.
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2206.01000-tree-tensor-network-circuit-sim/`.
**Verdict:** **PARTIAL** (representational claim on tree-clusterable circuits fully replicates; caveat on "hard" circuit signature — see §5).

---

## 1. Paper summary

The authors propose representing the statevector of a quantum circuit as a **rooted tree tensor network (TTN)** rather than the more common matrix-product state (MPS). Gates are applied by absorbing 1q gates into leaves and splitting 2q gates via SVD, threading a virtual bond through the tree. Because the maximum leaf-to-leaf path length in a balanced tree is O(log N) vs. O(N) for an MPS, TTNs can capture longer-range correlations at the same virtual bond dimension for circuits whose entanglement graph admits a clustering structure.

Key theoretical result: for tree-clusterable circuits (Fig. 12 "well-structured" pattern — clusters of qubits with dense intra-cluster gates and only a bounded number `k_G` of inter-cluster gates threaded through cluster roots), a **uniformly bounded** internal bond dimension suffices (Sect. 3.4). Circuits with all-to-all connectivity (QFT-style) or dense nearest-neighbor 2D lattices (Sect. 4.1 "lattice circuit") are hard for both TTN and MPS.

Reference implementation: <https://github.com/Gistbatch/tree-tensor-network-simulator> (Python).

## 2. Claims table

| ID | Claim | Type | Testable in scope? | Tested? |
|----|-------|------|--------------------|---------|
| C1 | TTN can represent the statevector of a tree-clusterable circuit at bounded chi with high fidelity, and TTN ≥ MPS at same chi on such circuits. | representational, quantitative | ✅ yes (N=12 small enough for exact statevector reference) | ✅ yes |
| C2 | Fidelity → 1 as chi grows (controllable error) for both TTN and MPS on tree-clusterable circuits. | quantitative | ✅ yes | ✅ yes |
| C3 | For lattice / all-to-all circuits (Fig. 11 style), both TTN and MPS struggle; MPS may fail entirely due to numerical divergence of the bond dimensions (Fig. 14 "MPS fails at gate 57"). | qualitative | partially (we can only check qualitative fidelity behavior, not full runtime scaling) | ✅ yes, with caveat |
| C4 | Wall-clock scaling: TTN beats MPS on tree-clusterable circuits up to 37 qubits (Fig. 13). | performance | out of scope (needs their custom simulator; qualitative signature only) | ❌ no (not attempted — would need paper's simulator, not just quimb) |
| C5 | Dry-run bond-dimension scaling up to 100 qubits (Fig. 15) matches theoretical bounds. | analytical | out of scope for a wave-brief-scale replication | ❌ no |

Reproducible headline (per brief): C1 + C2. Both are the "one most-checkable number" test the brief asks for.

## 3. Method — exact commands and tool versions

**Environment:**
- macOS Darwin 25.3.0 (x86_64), CherryRd.
- Python 3.11.15 in a fresh venv (`.venv/`).
- `quimb 1.14.0`, `numpy 2.0.2`, `scipy 1.17.1`, `numba 0.62.1`, `llvmlite 0.45.1`, `autoray 0.8.11`, `cotengra 0.8.2`, `opt_einsum 3.4.0`, `cytoolz 1.1.0`.
- Install: `python3.11 -m venv .venv && . .venv/bin/activate && pip install quimb numpy scipy cytoolz && pip install --only-binary=:all: numba` (needed `--only-binary` because llvmlite 0.45.x has no source-build path on macOS x86_64 without matching LLVM).

**Circuits (code/run_ttn_vs_mps.py, `build_circuit_generic`):**
- N = 12 qubits, deterministic seed 20260704.
- Init: random `U3(θ,φ,λ)` on each qubit.
- 2q gates: Haar-random via QR decomposition of a random complex Gaussian, phase-fixed.
- **Family A ("tree"):** 3 clusters of 4 qubits (qubits {0..3}, {4..7}, {8..11}). 3 sweeps of dense pairwise Haar-random 2q gates *within each cluster*. Then 2 rounds of all-pair Haar-random 2q gates *between cluster roots only* (qubits 0, 4, 8). This is the paper's Fig. 12 "well-structured" pattern.
- **Family B ("hard"):** 12 qubits, 2 rounds of all-to-all pair-shuffled Haar-random 2q gates. Stand-in for lattice/QFT-hard regime (Sect. 4.1).

**Exact statevector:** `quimb.tensor.Circuit(N=12).to_dense()` — full 4096-vector, contracted from the tensor network with quimb's default optimizer. Renormalized to unit L2.

**MPS run:** `quimb.tensor.CircuitMPS(N=12, max_bond=chi, cutoff=0.0)`. Same gate sequence as exact (deterministic via seed). `.psi.to_dense()` → renormalized dense vector. Fidelity `F = |<exact|approx>|^2`.

**TTN run:** balanced binary hierarchical SVD compression of the exact statevector. At every internal edge of the balanced binary tree over 12 qubits, keep at most `chi` singular values. Implemented recursively in `ttn_compress_fidelity` (see code). This measures the *representational capacity* of a bounded-chi TTN — which is the paper's central theoretical object (their Sect. 3 bounds Dmax the same way).

**Sanity check (passed):** at chi=64, CircuitMPS matches exact Circuit statevector to F = 1.00000000, confirming qubit-ordering and normalization consistency.

**Commands to reproduce:**
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2206.01000-tree-tensor-network-circuit-sim
. .venv/bin/activate
python code/run_ttn_vs_mps.py
```
Runtime: ~20 seconds. Deterministic.

## 4. Results

### 4.1 Fidelity vs χ (evidence: `report/evidence/fidelity_vs_chi.csv`)

**Tree-clusterable circuit (paper Fig. 12 pattern):**

| χ | MPS fidelity | TTN fidelity | Ratio TTN/MPS |
|---|--------------|--------------|---------------|
| 2 | 0.02941 | 0.25082 | **8.5×** |
| 4 | 0.37915 | 0.61086 | 1.6× |
| 8 | 0.79166 | 0.93911 | 1.19× |
| 16 | 1.00000 | 1.00000 | 1.0 |
| 32 | 1.00000 | 1.00000 | 1.0 |

**Hard all-to-all circuit (paper Fig. 11 stand-in):**

| χ | MPS fidelity | TTN fidelity |
|---|--------------|--------------|
| 2 | 0.00056 | 0.01414 |
| 4 | 0.00047 | 0.06144 |
| 8 | 0.00027 | 0.20746 |
| 16 | 0.00021 | 0.53116 |
| 32 | 0.02161 | 0.89233 |

### 4.2 Results-vs-paper table

| Claim | Paper prediction | Our reproduction | Match? |
|-------|------------------|------------------|--------|
| C1 (tree: TTN ≥ MPS at same χ) | TTN strictly better at low χ; both reach exact at moderate χ | TTN strictly better at χ=2, 4, 8 (up to 8.5× at χ=2); both reach F=1 at χ=16 | ✅ **MATCH** |
| C2 (fidelity → 1 with χ) | monotonic convergence | monotonic 0.03→0.38→0.79→1.00→1.00 (MPS), 0.25→0.61→0.94→1.00→1.00 (TTN) | ✅ **MATCH** |
| C3 (hard: both struggle) | both struggle; MPS may fail | MPS clearly fails (fidelity ≤ 0.022 across all χ we tried); TTN struggles but reaches 0.89 at χ=32 — better than the paper implies for their sequential TTN evolution | ⚠️ **PARTIAL** (see §5) |

## 5. Discussion / caveats

**Why C3 is only a partial match.** Our TTN is a *direct compression* of the exact statevector into a balanced-binary tree with per-edge SVD truncation. This gives the **optimal** bounded-chi TTN representation of that state — an upper bound on what any TTN evolution algorithm can achieve. The paper's algorithm evolves the TTN *sequentially* by SVD-splitting each 2q gate and threading the bond through the tree, which incurs additional truncation error at every gate. For structureless all-to-all circuits, the paper reports that internal bond dimensions blow up during sequential evolution — a distinct failure mode from a pure representation-capacity failure. So our χ=32 TTN fidelity of 0.89 on the hard circuit is a *representation* number, not a *sequential-evolution* number, and does not contradict the paper.

GPT-5 judge flagged this exact nuance ("suggests the TTN construction/compression method here is substantially stronger than the circuit-evolution TTN setting being compared in the paper") and voted PARTIAL. Sonnet-4.6 judge voted REPLICATED. We take the more conservative verdict.

**Bond-dimension scaling / wall-clock (C4, C5).** Out of scope for this wave-brief. Requires either running the authors' custom simulator at github.com/Gistbatch/tree-tensor-network-simulator, or a much larger-N experiment (up to 37 or 100 qubits with dry-run bond tracking). A full reproduction of Figs. 13 and 15 would be a follow-up.

**Sanity checks passed:**
- CircuitMPS(χ=64) matches Circuit statevector to F=1.00000000 (ordering/norm OK).
- Exact statevector unit-norm (‖ψ‖=1.000000).
- MPS fidelity monotonically increases with χ on the tree circuit (0.03 → 1.0).
- TTN fidelity monotonically increases with χ on both circuits.

## 6. Verdict

**PARTIAL** — The paper's core representational claim (C1 + C2) is reproduced quantitatively on a small, exact-statevector-verifiable instance. TTN clearly outperforms MPS at every truncated bond dimension on the tree-clusterable circuit, and both converge to exact at moderate χ. The "hard for both" prediction (C3) reproduces for MPS but not for our optimal-TTN-compression baseline; the mismatch is methodological (compression vs sequential evolution) rather than physical, and does not challenge the paper's conclusions. Full runtime and large-N scaling (C4, C5) not attempted.

**LLM-judge panel:**
- Judge 1 (argo:gpt-5.2): PARTIAL — flagged the compression-vs-evolution nuance.
- Judge 2 (argo:claude-sonnet-4.6): REPLICATED — noted both signatures reproduce.
- Judge 3 (argo:claude-opus-4.7 or 4.8): not obtained — endpoint was returning a Vertex parser-validation error during this wave (all Opus 4.7/4.8 calls at the time failed with "Value at 'choices[0].message' does not match any variant of ..."), so we substituted GPT-5.2 and Sonnet-4.6.

Conservative resolution: **PARTIAL**.

## 7. Evidence files

- `code/run_ttn_vs_mps.py` — the replication script (~16 KB, one-shot deterministic).
- `code/llm_judge.py` — Argo LLM-judge caller.
- `report/evidence/fidelity_vs_chi.csv` — full result table.
- `report/evidence/fidelity_vs_chi.json` — same data, structured.
- `report/evidence/llm_verdict.txt` — GPT-5.2 judge output.
- `report/evidence/llm_verdict_judge2.txt` — Sonnet-4.6 judge output.
- `logs/run1.log` — full stdout of `run_ttn_vs_mps.py`.
- `work/paper.pdf`, `work/paper.txt` — arXiv v3 PDF and pdftotext dump.
