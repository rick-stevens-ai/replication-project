# Failure analysis — Fermi-Hubbard VQE (Hamiltonian Variational)

**Paper:** Cade, Mineh, Montanaro, Stanisic. Phys. Rev. B **102**, 235122 (2020). arXiv:1912.06007.
**Replication verdict:** REPLICATED (strategy). Coverage 7/10, Agreement 10/10.
**Author of this critique:** Ollie, 2026-07-06.

This document is the *honest* self-critique. Nothing here contradicts the REPLICATED verdict — the paper's core strategy claim IS reproduced — but it names precisely what is and is not on the ledger.

---

## 1. What was actually re-derived from scratch

- Fermi-Hubbard Hamiltonian construction on 1D and small-2D lattices, Jordan-Wigner mapped **without** `openfermion`. Verified against a brute-force 4-qubit build.
- Ground-truth exact diagonalization in the (n_up, n_dn) sector via `scipy.sparse.linalg.eigsh`.
- The HV ansatz itself: onsite / horizontal-hop / vertical-hop group evolutions, one angle per group per layer, exact term-group `exp(-iθH)` via dense eigendecomposition.
- The non-interacting (U=0) reference state, projected into the correct particle-number sector — the paper's recommended HV starting point.
- L-BFGS-B optimization with 3 random restarts per depth.

This is a genuine clean-room reimplementation. There is no borrowed VQE library sitting under the hood.

## 2. What was quantitatively verified against the paper's claims

- **Depth-monotone energy-error convergence.** Confirmed on all 5 lattices. This is the paper's headline scaling claim, and it is exercised.
- **High accuracy at modest depth on small lattices.** Confirmed: 1×2 exact at depth 1; 2×2 to machine precision at depth 2; 12-qubit lattices to ~1e-4 by depth 8.
- **Parameter count linear in depth.** Confirmed: exactly 3 params/layer (or 2 for 1×N without vertical bonds).
- **Comparison against exact diagonalization ground truth.** Yes, per lattice, per depth.

## 3. What was NOT verified (and why the verdict is still REPLICATED for the strategy)

- **HV vs. hardware-efficient ansatz (HEA) head-to-head.** The paper's claim that HV *beats* generic HEA at matched depth was **not** exercised here. Only HV-vs-exact was tested. So the "HV is better structured" side of the claim is unverified by this replication.
- **DMRG / MPS cross-check.** Not done. Exact diagonalization was ground truth at ≤12 qubits, which is defensible for the sizes tested but leaves the tensor-network comparison as an open item.
- **Large-lattice scaling.** The paper considers lattices well beyond 12 qubits. Classical statevector simulation caps out here; those lattices are simply outside the scope of this replication.
- **Shot noise.** All expectation values were computed as exact inner products. Real hardware runs at shots ~1e3-1e5 per Pauli term.
- **Device / gate noise.** No depolarizing channel, no readout error, no crosstalk. At the depths (~8 layers) needed for 12-qubit chemical-accuracy convergence, real-device error would materially degrade the reproduced numbers.
- **Hardware runs.** The paper's raw device measurements are **not deposited** with the paper. Reproducing them from scratch would require ~10^4 CNOT-count circuits on a Sycamore-class device — not achievable here.
- **Strong-coupling / doped regimes.** Only U/t=2 at half-filling was tested. The physically interesting Fermi-Hubbard regime (U/t≳8, finite doping) is untouched. The non-interacting reference state is expected to be worse there, and HV depth requirements may explode — this is speculation, not measurement.
- **Alternative structured ansätze.** No comparison against k-UpCCGSD, ADAPT-VQE, qubit-ADAPT, or number-preserving UCC. Any of these might beat HV at matched circuit-depth-or-CNOT-count on the same lattices; we don't know.

## 4. Known idealizations (call them what they are)

- **Exact `exp(-iθH_group)` per term-group.** On hardware, term-group evolutions are Trotterized, and the Trotter error interacts with the variational optimization. This replication skips that entirely.
- **Deterministic optimizer landscape.** No shot-noise-induced landscape roughness. Real VQE optimizers see much noisier gradients / values.
- **Small optimizer restart budget.** 3 restarts per depth is fine for the small lattices tested; at larger depths the barren-plateau risk rises and 3 restarts may not sample enough of the landscape.

## 5. Provenance / process risk

- The numerics and code were produced by a subagent that timed out before writing prose. The final markdown report was hand-written from `results.json` by a downstream inspector. This means the report is inspection-quality, not reviewed-by-original-author quality. The `results.json` and `run.log` are the ground truth; the prose is a faithful summary of them.
- No independent second-run cross-check on a different machine. A fresh reproducer running `python3 code/replicate.py` on m1 would be a useful sanity check but was not performed.

## 6. Bottom line

The paper's *strategy* is reproduced: the HV ansatz, seeded from the U=0 ground state, converges monotonically with depth to chemical-accuracy energies on Fermi-Hubbard lattices up to 12 qubits, exactly as claimed. The paper's *large-lattice* and *hardware/noise* sections are untouched — they were out of scope. Anyone using this replication as evidence for or against Fermi-Hubbard VQE on real hardware should be aware that the hardware side of the paper is **not** exercised here.
