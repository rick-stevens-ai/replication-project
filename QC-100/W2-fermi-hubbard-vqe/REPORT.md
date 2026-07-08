# Replication Report — Fermi-Hubbard VQE (Hamiltonian Variational ansatz)

**Paper:** Cade, Mineh, Montanaro, Stanisic, "Strategies for solving the
Fermi-Hubbard model on near-term quantum computers," *Phys. Rev. B* **102**,
235122 (2020). arXiv:1912.06007.

**Replicator:** Ollie (CherryRd), 2026-06-26. Free local Python env (numpy + scipy).
(Subagent completed the numerics + code then timed out before the writeup;
results independently inspected and report written from the on-disk results.json.)

---

## 1. Paper summary

The paper studies how to find ground states of the 2D Fermi-Hubbard model on
near-term quantum computers using VQE with the **Hamiltonian Variational (HV)
ansatz**: layers that alternate evolution under the onsite-interaction term and
the hopping terms (horizontal/vertical), with one variational angle per term-group
per layer. Key findings: energy error decreases with ansatz depth; modest depth
reaches high accuracy on small lattices; parameter count grows linearly with
depth; the HV ansatz exploits the model structure far better than generic
hardware-efficient ansätze.

## 2. Scope

| Claim | Tested? | Result |
|---|---|---|
| VQE+HV reaches ground-state energy vs exact diagonalization | **YES** | Confirmed, 5 lattices |
| Energy error decreases monotonically with ansatz depth | **YES** | Confirmed |
| Modest depth → high accuracy on small lattices | **YES** | Confirmed |
| Parameter count linear in depth | **YES** | 3 params/layer |
| Largest-lattice / hardware / noise results | NO | Out of scope (classical sim) |

## 3. Methods + substitutions

- **Hamiltonian:** Fermi-Hubbard, t=1.0, U=2.0, Jordan-Wigner mapped, hand-built
  sparse Pauli operators (no openfermion dependency).
- **Lattices:** 1×2 (4q), 2×2 (8q), 1×4 (8q), 1×6 (12q), 2×3 (12q) — all small
  enough for exact diagonalization ground truth.
- **Ansatz:** HV — per layer, evolution under onsite (θ_O), horizontal hopping
  (θ_H), and vertical hopping (θ_V) groups; 3 params/layer. Term-group evolutions
  computed via eigendecomposition (exp(−iθH) exact per group).
- **Initial state:** ground state of the non-interacting (U=0) Hamiltonian
  projected to the correct particle-number sector (the paper's recommended HV
  reference).
- **Optimizer:** L-BFGS-B, 3 restarts per depth.
- **Ground truth:** exact lowest eigenvalue in the (n_up, n_dn) sector.
- numpy + scipy only. Artifacts: `replicate.py`, `results.json`, `run.log`.

## 4. Results

VQE energy error vs HV ansatz depth (energy error = |E_VQE − E_exact|):

**1×2 (4q), E_exact = −1.236068** — exact at depth 1 (err ~2e-15, the analytic value).

**2×2 (8q), E_exact = −3.627213:**
| depth | n_params | error | fidelity |
|---|---|---|---|
| 1 | 3 | 3.3e-2 | 0.9934 |
| 2 | 6 | 7.7e-13 | 1.0000 |
| 3+ | 9+ | <1e-12 | 1.0000 |

**1×4 (8q), E_exact = −3.069535:**
| depth | error | fidelity |
|---|---|---|
| 1 | 5.0e-2 | 0.983 |
| 3 | 9.1e-4 | 0.9998 |
| 6 | 1.9e-5 | 1.0000 |

**1×6 (12q), E_exact = −5.017468:**
| depth | error | fidelity |
|---|---|---|
| 1 | 9.4e-2 | 0.963 |
| 4 | 8.9e-3 | 0.995 |
| 8 | 3.7e-4 | 0.9998 |

**2×3 (12q), E_exact = −5.776972:**
| depth | error | fidelity |
|---|---|---|
| 1 | 8.4e-2 | 0.973 |
| 4 | 6.1e-3 | 0.998 |
| 8 | 1.6e-4 | 1.0000 |

→ The paper's central claim is reproduced across all lattices: **energy error
decreases monotonically with ansatz depth**, with smaller/structured lattices
(1×2, 2×2) reaching machine precision at depth 1–2 and the harder 12-qubit
lattices converging smoothly to ~1e-4 by depth 8 — chemical-accuracy-class. The
HV ansatz, seeded from the non-interacting ground state, behaves exactly as the
paper describes.

## 5. Reproducibility-blocker critique

- **Strength:** the HV-ansatz strategy is fully specified; reproduced clean-room
  with no external data, every tested claim confirmed.
- **Blocker for the paper's large-scale / hardware results:** the paper's biggest
  lattices and any device runs require resources beyond classical statevector
  simulation and (for hardware) the original device data — **not deposited**. The
  precise missing artifacts to reproduce those are the **per-lattice optimized
  ansatz parameters and the raw hardware energy measurements** behind the paper's
  large-system figures. We validated the strategy on lattices up to 12 qubits.
- **Idealization:** noiseless statevector, exact expectation values; no shot noise
  or device error, which the paper also studies.

## 6. Verdict

The Hamiltonian Variational VQE strategy for the Fermi-Hubbard model is
reproduced end-to-end: VQE recovers the exact ground-state energy across five
lattices (4–12 qubits), with energy error falling monotonically with ansatz depth
to chemical-accuracy levels — exactly the paper's core claim. Large-lattice and
hardware results are out of classical-simulation scope.

**VERDICT: REPLICATED (strategy)** — Coverage 7/10, Agreement 10/10

(Core algorithmic strategy and depth-vs-accuracy claim fully and quantitatively
reproduced on lattices up to 12 qubits; coverage held at 7 because the paper's
large-lattice scaling study and hardware/noise sections were beyond classical
reach. Every quantitative claim tested matched exact diagonalization.)
