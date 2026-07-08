# Workflow — Fermi-Hubbard VQE (Hamiltonian Variational)

**Paper:** Cade, Mineh, Montanaro, Stanisic, Phys. Rev. B **102**, 235122 (2020). arXiv:1912.06007.
**Replicator:** Ollie (CherryRd), 2026-06-26. Writeup 2026-07-06.
**Set:** QC-100.

## Environment
- Host: CherryRd (macOS, m1 mesh peer).
- Python: system + numpy + scipy only (no `openfermion`, no `qiskit`, no `pennylane`).
- No hardware, no cloud, no shot sampling — pure classical statevector.

## Pipeline
1. **Hamiltonian construction (clean-room).**
   - Fermi-Hubbard on a rectangular lattice, `t=1.0`, `U=2.0`.
   - Jordan-Wigner mapping hand-implemented; sparse Pauli operators built term-by-term for onsite (`U * n↑ n↓`) and hopping (`-t * (c†c + h.c.)`) contributions.
   - Two sanity checks: (a) hermiticity of the sparse matrix; (b) trace against a small brute-force construction on the 4-qubit lattice.
2. **Ground-truth exact diagonalization.**
   - Projected to the target `(n_up, n_dn)` particle-number sector (half-filling).
   - Lowest eigenpair via `scipy.sparse.linalg.eigsh(..., k=1, which='SA')`.
3. **Reference state (depth-0).**
   - Non-interacting (U=0) ground state in the target particle-number sector — the paper's recommended HV starting point.
4. **HV ansatz.**
   - Per layer, apply `exp(-i θ_O H_onsite) · exp(-i θ_H H_hop_horiz) · exp(-i θ_V H_hop_vert)`.
   - Each `exp(-i θ H_group)` computed by dense eigendecomposition of `H_group` restricted to the sector (small enough to be exact).
   - Parameter count per layer: 3 (or 2 if the lattice has no vertical bonds, e.g. 1×N).
5. **Optimization.**
   - `scipy.optimize.minimize(..., method='L-BFGS-B')`.
   - 3 random restarts per depth; best final energy kept.
   - Depth sweep: 1, 2, 3, 4, 6, 8 depending on lattice size.
6. **Recording.**
   - Per (lattice, depth): `n_params`, best `E_VQE`, `|E_VQE − E_exact|`, `|⟨ψ_VQE|ψ_exact⟩|²`.
   - All written to `results.json`. Human-readable log in `run.log`.

## Lattice set
| Lattice | Qubits | (n_up, n_dn) | Notes |
|---|---|---|---|
| 1×2 | 4 | (1,1) | analytic sanity |
| 2×2 | 8 | (2,2) | first 2D test |
| 1×4 | 8 | (2,2) | 1D scaling |
| 1×6 | 12 | (3,3) | 1D at 12q |
| 2×3 | 12 | (3,3) | 2D at 12q |

## What was NOT done (and why)
- No shot-based sampler → the paper's noise/shot analysis is not exercised.
- No hardware backend → paper's device runs unreproducible without deposited hardware data.
- No comparison against a hardware-efficient-ansatz baseline → we validated HV against exact, not against a rival ansatz.
- No DMRG cross-check → exact diagonalization was ground truth at ≤12 qubits, adequate for the tested sizes.
- No lattice > 12 qubits → statevector wall-time / memory ceiling on this box.

## Reproduction command (for the record)
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/W2-fermi-hubbard-vqe
python3 code/replicate.py --lattices 1x2 2x2 1x4 1x6 2x3 --depths 1 2 3 4 6 8
```

Full results in `results.json`; per-run trace in `run.log`.
