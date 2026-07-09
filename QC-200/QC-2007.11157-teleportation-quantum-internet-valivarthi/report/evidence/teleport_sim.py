#!/usr/bin/env python3
"""
Statevector reproduction of the canonical single-qubit quantum teleportation
protocol described in Valivarthi et al. 2020, "Teleportation Systems Towards
a Quantum Internet" (arXiv:2007.11157, PRX Quantum 1, 020317).

We cannot reproduce the fiber-optic hardware, but the teleportation *protocol*
that the paper implements is exactly the Bennett-Brassard-Crepeau-Josza-
Peres-Wootters 1993 protocol adapted to time-bin qubits. We reproduce that
protocol as a 3-qubit Qiskit + qiskit-aer statevector simulation and:

  1. Show that ideal teleportation gives fidelity F = 1.0 for a bank of
     input states (|0>, |1>, |+>, |->, |+i>, |-i>, and a Haar-random state).

  2. Inject configurable dephasing (T2) noise on the entangled channel to
     represent the paper's fiber regimes (short, medium, long ~22 km) and
     reproduce the trend that experimental fidelity is bounded below unity
     by channel imperfections. Compare the ~0.90 experimental average as
     a physically-plausible anchor for the noise strength.

Every number below is the output of an actual qiskit-aer simulation.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace, state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, phase_damping_error

HERE = Path(__file__).resolve().parent
OUT = HERE
np.random.seed(20260705)


# -------------------------------------------------------------------------
# Circuit building blocks
# -------------------------------------------------------------------------

def teleportation_circuit(prep: QuantumCircuit) -> QuantumCircuit:
    """Return a 3-qubit teleportation circuit.

    Qubit 0 = Alice's data qubit (state |psi> to teleport, prepared by `prep`)
    Qubit 1 = Alice's half of the shared Bell pair
    Qubit 2 = Bob's half of the shared Bell pair (the teleportation target)

    Uses deferred classical corrections (c_if on measured bits) via the
    standard textbook protocol: Bell-pair generation on (1,2), then
    Bell-measurement on (0,1), then classical-controlled X and Z on qubit 2.
    """
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(2, "c")
    qc = QuantumCircuit(q, c)

    # (1) Prepare Alice's data qubit on q0 with the caller-supplied prep
    #     circuit (which must be a 1-qubit circuit acting on q0).
    qc.compose(prep, qubits=[q[0]], inplace=True)

    # (2) Create the Bell pair |Phi+> = (|00> + |11>)/sqrt(2) on (q1, q2).
    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.barrier()

    # (3) Bell measurement on (q0, q1): CNOT then H on the control, then
    #     measure both. This projects (q0, q1) onto the Bell basis.
    qc.cx(q[0], q[1])
    qc.h(q[0])
    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])
    qc.barrier()

    # (4) Classical corrections on Bob's qubit q2 driven by the two
    #     measurement outcomes. This is the paper's "classical bits sent
    #     to Bob" step. Qiskit 2.x uses if_test contexts.
    with qc.if_test((c[1], 1)):
        qc.x(q[2])
    with qc.if_test((c[0], 1)):
        qc.z(q[2])
    return qc


def prep_state(label: str, theta: float | None = None,
               phi: float | None = None) -> QuantumCircuit:
    """Build a 1-qubit preparation circuit for a labeled input state."""
    p = QuantumCircuit(1)
    if label == "0":
        pass
    elif label == "1":
        p.x(0)
    elif label == "+":
        p.h(0)
    elif label == "-":
        p.x(0); p.h(0)
    elif label == "+i":
        p.h(0); p.s(0)
    elif label == "-i":
        p.h(0); p.sdg(0)
    elif label == "random":
        # Uniform on the Bloch sphere: cos(theta/2)|0> + e^{i phi} sin(theta/2)|1>
        # Use U3(theta, phi, 0).
        assert theta is not None and phi is not None
        p.u(theta, phi, 0.0, 0)
    else:
        raise ValueError(f"unknown state label: {label!r}")
    return p


def target_statevector(label: str, theta: float | None = None,
                       phi: float | None = None) -> Statevector:
    """Expected 1-qubit target state |psi> that Alice teleports."""
    return Statevector.from_instruction(prep_state(label, theta=theta, phi=phi))


# -------------------------------------------------------------------------
# Ideal statevector teleportation: fidelity should be 1.0
# -------------------------------------------------------------------------

def ideal_fidelity_for(label: str, theta: float | None = None,
                       phi: float | None = None) -> float:
    """Full statevector reproduction: run the teleportation circuit on the
    density_matrix backend of AerSimulator and compare Bob's marginal to
    the intended |psi>."""
    prep = prep_state(label, theta=theta, phi=phi)
    qc = teleportation_circuit(prep)
    qc.save_density_matrix()

    sim = AerSimulator(method="density_matrix")
    result = sim.run(qc, shots=1).result()
    rho_full = DensityMatrix(np.asarray(result.data(0)["density_matrix"]))

    # Reduce over qubits 0 and 1 (Alice's qubits) to get Bob's marginal.
    # In Qiskit qubit ordering (little-endian), qubit 0 is the rightmost.
    rho_bob = partial_trace(rho_full, [0, 1])
    psi = target_statevector(label, theta=theta, phi=phi)
    return float(state_fidelity(rho_bob, psi))


# -------------------------------------------------------------------------
# Noisy channel: dephasing (phase-damping) on Bob's qubit
# -------------------------------------------------------------------------

def build_dephasing_noise(prob: float) -> NoiseModel:
    """Attach a single-qubit phase-damping error to *every* gate that touches
    Bob's qubit (q2), plus a small residual error on Alice's Bell-pair half
    (q1) to represent fiber loss/dephasing on both branches.

    `prob` is the phase-damping parameter lambda_pd ∈ [0, 1]; larger => more
    channel dephasing => lower teleportation fidelity.
    """
    noise = NoiseModel()
    err1 = phase_damping_error(prob)
    # 2-qubit gate error: tensor product with identity (no error on the other
    # qubit) - qiskit-aer's expand handles this. For CX we apply the damping
    # to whichever qubit is q2 or q1.
    err2 = err1.tensor(phase_damping_error(prob * 0.5))
    # Apply to any single-qubit gate on q1 and q2:
    noise.add_quantum_error(err1, ["id", "u", "u1", "u2", "u3", "x", "y", "z",
                                    "h", "s", "sdg", "t", "tdg", "rx", "ry",
                                    "rz"], [1])
    noise.add_quantum_error(err1, ["id", "u", "u1", "u2", "u3", "x", "y", "z",
                                    "h", "s", "sdg", "t", "tdg", "rx", "ry",
                                    "rz"], [2])
    # And to any 2-qubit gate involving q1-q2 (the Bell pair sharing step).
    noise.add_quantum_error(err2, ["cx"], [1, 2])
    return noise


def noisy_fidelity_for(label: str, prob: float,
                       theta: float | None = None,
                       phi: float | None = None) -> float:
    prep = prep_state(label, theta=theta, phi=phi)
    qc = teleportation_circuit(prep)
    qc.save_density_matrix()

    noise = build_dephasing_noise(prob)
    sim = AerSimulator(method="density_matrix", noise_model=noise)
    result = sim.run(qc, shots=1).result()
    rho_full = DensityMatrix(np.asarray(result.data(0)["density_matrix"]))
    rho_bob = partial_trace(rho_full, [0, 1])
    psi = target_statevector(label, theta=theta, phi=phi)
    return float(state_fidelity(rho_bob, psi))


# -------------------------------------------------------------------------
# Main driver
# -------------------------------------------------------------------------

def main() -> None:
    print("QC-2007.11157 teleportation replication — qiskit-aer statevector")
    print("=" * 72)

    # --- 1. Ideal case: F should be 1.0 for every input state ------------
    ideal_labels = ["0", "1", "+", "-", "+i", "-i"]
    ideal_results = {}
    for lab in ideal_labels:
        F = ideal_fidelity_for(lab)
        ideal_results[lab] = F
        print(f"  ideal  |{lab:>2s}>  F = {F:.12f}")
    # Two Haar-random states on the Bloch sphere
    rng = np.random.default_rng(20260705)
    random_states = []
    for k in range(4):
        theta = float(rng.uniform(0, math.pi))
        phi = float(rng.uniform(0, 2 * math.pi))
        F = ideal_fidelity_for("random", theta=theta, phi=phi)
        random_states.append(
            {"theta": theta, "phi": phi, "fidelity": F, "k": k}
        )
        print(f"  ideal  random(theta={theta:.4f}, phi={phi:.4f})  F = {F:.12f}")
    ideal_mean = float(np.mean(list(ideal_results.values())
                               + [r["fidelity"] for r in random_states]))
    print(f"  ideal mean F over all input states = {ideal_mean:.12f}")

    # --- 2. Noisy trend: 3 regimes (short, medium, long fiber) ----------
    # Choose lambda_pd values so the resulting fidelity brackets the
    # paper's ~0.89-0.90 experimental average.
    regimes = [
        ("short (0 km, back-to-back)",   0.02),
        ("medium (~11 km fiber)",        0.15),
        ("long (~22 km fiber)",          0.30),
    ]
    noisy_rows = []
    for name, p in regimes:
        Fs = {lab: noisy_fidelity_for(lab, p) for lab in ideal_labels}
        # random states too, same seeds for fair comparison
        rng2 = np.random.default_rng(20260705)
        r_Fs = []
        for k in range(4):
            theta = float(rng2.uniform(0, math.pi))
            phi = float(rng2.uniform(0, 2 * math.pi))
            r_Fs.append(noisy_fidelity_for("random", p, theta=theta, phi=phi))
        mean_F = float(np.mean(list(Fs.values()) + r_Fs))
        noisy_rows.append({
            "regime": name,
            "lambda_pd": p,
            "per_state_fidelity": Fs,
            "random_state_fidelities": r_Fs,
            "mean_fidelity": mean_F,
        })
        print(f"  noisy  {name:32s}  lambda_pd={p:.3f}  <F>={mean_F:.6f}")

    # --- 3. Save everything ---------------------------------------------
    payload = {
        "paper": "Valivarthi et al. 2020, arXiv:2007.11157",
        "paper_headline_number": {
            "F_avg_no_added_fiber": 0.89,
            "F_avg_with_added_fiber": 0.89,
            "abstract_claim": "F >= 0.90",
            "uncertainty": "+/- 1% (systematic) / +/- 3% (with decoys)",
        },
        "reproduction": {
            "tool": "qiskit + qiskit-aer statevector",
            "circuit": "3-qubit textbook BBCJPW teleportation protocol",
            "seed": 20260705,
        },
        "ideal": {
            "per_state_fidelity": ideal_results,
            "random_state_fidelities": random_states,
            "mean_fidelity": ideal_mean,
        },
        "noisy_regimes": noisy_rows,
    }
    with open(OUT / "results.json", "w") as f:
        json.dump(payload, f, indent=2)

    # Small CSV summary
    with open(OUT / "results.csv", "w") as f:
        f.write("regime,lambda_pd,mean_fidelity\n")
        f.write(f"ideal,0.0,{ideal_mean}\n")
        for row in noisy_rows:
            f.write(f"{row['regime']},{row['lambda_pd']},{row['mean_fidelity']}\n")

    # Save the actual textbook circuit for the |+> input so a reviewer can
    # inspect exactly what we ran.
    demo = teleportation_circuit(prep_state("+"))
    with open(OUT / "example_circuit_plus.qasm", "w") as f:
        from qiskit.qasm2 import dumps
        try:
            f.write(dumps(demo))
        except Exception as e:
            f.write(f"// qasm2 export failed: {e}\n")
            f.write(str(demo.draw(output="text")))
    with open(OUT / "example_circuit_plus.txt", "w") as f:
        f.write(str(demo.draw(output="text")))

    # Print summary line for the log
    print()
    print("SUMMARY:")
    print(f"  Ideal mean F = {ideal_mean:.6f}  (paper: 1.0 by construction)")
    for row in noisy_rows:
        print(f"  {row['regime']:32s}  <F> = {row['mean_fidelity']:.4f}")


if __name__ == "__main__":
    main()
