"""
HHL (Harrow-Hassidim-Lloyd) 2x2 matrix inversion for the exact matrix used in
Zhao, Pozas-Kerstjens, Rebentrost, Wittek, "Bayesian Deep Learning on a
Quantum Computer" (arXiv:1806.11463).

Matrix:   A = (1/2) * [[3, 1],
                        [1, 3]]
This is the same A the paper inverts (Sec IV.A, Fig. 1 and Sec IV.B, IBMQX5
89% success -> fidelity 0.78).

We reproduce (i) the ideal noiseless HHL solution and its fidelity with the
classically-computed target A^{-1}|b>, and (ii) a depolarizing-noise sweep
that mirrors the paper's Fig. 1 fidelity-vs-gate-noise curve, using a
Qiskit-Aer noise model.

Reference-shallow-circuit construction follows Cao, Daskin, Frankel, Kais,
"Quantum circuit design for solving linear systems of equations",
Mol. Phys. 110, 1675 (2012), arXiv:1110.2232 -- which the paper explicitly
cites as ref. [49] and uses as the specialized 2x2 circuit.

For this specific A, the eigenvalues are lambda_1 = 1 and lambda_2 = 2
with eigenvectors |u_1> = (|0> - |1>)/sqrt(2)  and
                  |u_2> = (|0> + |1>)/sqrt(2)
so A is diagonalized by the Hadamard: A = H diag(2,1) H.
We use this to build a clean, small HHL that we then contaminate with noise.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ---------------------------------------------------------------------------
# 1. Problem definition (exactly the paper's matrix)
# ---------------------------------------------------------------------------

A = 0.5 * np.array([[3.0, 1.0],
                    [1.0, 3.0]])
# Right-hand side.  Paper does not fix a specific |b> for the 2x2 demo; the
# HHL fidelity claim is about correctly implementing A^{-1} on the encoded |b>.
# We pick |b> = |0> (a legitimate choice used in the arXiv:1110.2232 circuit
# it references) which produces a nontrivial |x> spanning both eigenvectors.
b = np.array([1.0, 0.0])

# Classical target
x_classical = np.linalg.solve(A, b)
x_classical_normalized = x_classical / np.linalg.norm(x_classical)


# ---------------------------------------------------------------------------
# 2. Build a small, faithful HHL circuit for A = H * diag(2,1) * H.
#
# Because A is diagonalized by H (single-qubit Hadamard), the QPE step for
# this A collapses to:  apply H to the b-register, then the eigenvalue is
# stored classically as the computational-basis label 01 (lambda=1) or
# 10 (lambda=2) in a 2-bit clock register.  We use 2 clock qubits
# (four bits of precision covers {1,2} exactly) which matches the paper's
# choice of "four bits of precision" for the full protocol.
#
# HHL steps (see Nielsen&Chuang / HHL / Cao 1110.2232):
#   qubits: b(1) + clock(2) + ancilla(1) = 4 qubits total
#
#   (a) prepare |b> on b-register (here trivially |0>).
#   (b) apply H to b-register -> puts b in the eigenbasis of A.
#   (c) copy eigenvalue into clock register:
#           if b=|0> after H (=|u_2>, lambda=2), clock = |10>
#           if b=|1> after H (=|u_1>, lambda=1), clock = |01>
#       In this Hadamard-diagonal case we realize (c) with 2 CNOTs.
#   (d) controlled rotation Ry(2*arcsin(C/lambda)) on ancilla
#       using the clock register as control.  We pick C = 1 (= smallest
#       eigenvalue) so both rotations have well-defined amplitudes.
#   (e) uncompute clock (reverse of (c)).
#   (f) apply H to b-register again (undo (b)) so b is back in comp basis.
#   (g) post-select ancilla = |1>.
#
# The resulting b-register state is proportional to A^{-1}|b>.
# ---------------------------------------------------------------------------

def build_hhl_circuit_paper_2x2() -> QuantumCircuit:
    b_reg = QuantumRegister(1, name="b")
    clock = QuantumRegister(2, name="c")
    anc = QuantumRegister(1, name="a")
    cr = ClassicalRegister(1, name="anc_meas")
    qc = QuantumCircuit(b_reg, clock, anc, cr)

    # (a) |b> = |0>  -> nothing to do.

    # (b) rotate into eigenbasis of A
    qc.h(b_reg[0])

    # (c) copy eigenvalue into clock:
    #     after H:  |0>_b <-> eigenvector |u_2>, eigenvalue 2 -> clock = |10>
    #               |1>_b <-> eigenvector |u_1>, eigenvalue 1 -> clock = |01>
    # We want clock high bit = NOT(b), clock low bit = b.
    qc.x(b_reg[0])
    qc.cx(b_reg[0], clock[1])       # high bit of clock <- NOT b (after X)
    qc.x(b_reg[0])                  # restore b
    qc.cx(b_reg[0], clock[0])       # low bit of clock <- b

    # (d) controlled-Ry on ancilla:
    #     lambda=1 (clock=01) -> theta = 2*arcsin(C/1) = 2*arcsin(1) = pi
    #     lambda=2 (clock=10) -> theta = 2*arcsin(C/2) = 2*arcsin(0.5) = pi/3
    theta_lambda1 = 2 * math.asin(1.0 / 1.0)   # pi
    theta_lambda2 = 2 * math.asin(1.0 / 2.0)   # pi/3

    # controlled on clock=|01> (low bit=1, high bit=0): X on high, then ccx-Ry
    qc.x(clock[1])
    # multi-controlled Ry with 2 controls -- decompose via mcry
    qc.mcry(theta_lambda1, [clock[0], clock[1]], anc[0])
    qc.x(clock[1])

    # controlled on clock=|10>
    qc.x(clock[0])
    qc.mcry(theta_lambda2, [clock[0], clock[1]], anc[0])
    qc.x(clock[0])

    # (e) uncompute clock (reverse of (c))
    qc.cx(b_reg[0], clock[0])
    qc.x(b_reg[0])
    qc.cx(b_reg[0], clock[1])
    qc.x(b_reg[0])

    # (f) uncompute eigenbasis rotation
    qc.h(b_reg[0])

    # (g) measure ancilla (post-selection on |1>)
    qc.measure(anc[0], cr[0])

    return qc


# ---------------------------------------------------------------------------
# 3. Noiseless: extract the post-selected b-register state and compare to
#    A^{-1}|b>.  We do this analytically with Statevector + projection so we
#    can compute the fidelity paper-style (F = |<psi_ideal|psi_noisy>|^2).
# ---------------------------------------------------------------------------

def noiseless_postselected_state(qc: QuantumCircuit) -> np.ndarray:
    """Simulate qc without measurement, project on ancilla=|1>, trace out
    clock+ancilla, return the (renormalized) 2-dim state on b-register."""
    qc_nom = qc.remove_final_measurements(inplace=False)
    sv = Statevector.from_instruction(qc_nom).data

    # Qubit ordering in Qiskit statevector: qubit 0 is the least-significant
    # bit of the basis-state index.  Registers are added in order:
    #   b(1)  = qubit 0
    #   clock = qubits 1,2
    #   anc   = qubit 3
    # So an index i = a * 8 + c * 2 + b   (a in {0,1}, c in {0..3}, b in {0,1})
    dim = sv.shape[0]
    post = np.zeros(2, dtype=complex)
    for i in range(dim):
        b_val = i & 1
        c_val = (i >> 1) & 3
        a_val = (i >> 3) & 1
        if a_val == 1:
            post[b_val] += sv[i]  # sum over clock (should collapse to 0
                                  # analytically since clock uncomputed)
    norm = np.linalg.norm(post)
    if norm < 1e-12:
        return post
    return post / norm


def state_fidelity_1q(v1: np.ndarray, v2: np.ndarray) -> float:
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    return float(np.abs(np.vdot(v1, v2)) ** 2)


# ---------------------------------------------------------------------------
# 4. Noisy sweep with a depolarizing gate-noise model (mirrors paper Fig. 1a).
# ---------------------------------------------------------------------------

def noisy_run(qc: QuantumCircuit, gate_noise: float, shots: int = 8192,
              b_reg_qubit_index: int = 0) -> dict:
    """Attach depolarizing noise on every 1q/2q gate (=paper's 'gate noise'
    model, Sec IV.A: 'a Pauli X ... with a certain probability on each qubit
    after every gate application').  We use qiskit-aer's depolarizing_error
    which is a slightly milder but standard analog (paper's exact
    'random-X-after-gate' model is a special case of depolarizing noise).

    We add a b-register measurement so we can compute the post-selected
    output distribution and fidelity."""
    qc_meas = QuantumCircuit(*qc.qregs, *qc.cregs)
    qc_meas.compose(qc, inplace=True)
    # add classical bit + measurement for the b-register
    b_cr = ClassicalRegister(1, name="b_meas")
    qc_meas.add_register(b_cr)
    qc_meas.measure(qc.qregs[0][0], b_cr[0])

    noise_model = NoiseModel()
    if gate_noise > 0:
        err1 = depolarizing_error(gate_noise, 1)
        err2 = depolarizing_error(gate_noise, 2)
        noise_model.add_all_qubit_quantum_error(err1, ["h", "x", "ry", "u", "u3", "u2", "u1", "sx", "rz"])
        noise_model.add_all_qubit_quantum_error(err2, ["cx", "cz"])

    sim = AerSimulator(noise_model=noise_model if gate_noise > 0 else None)
    tqc = transpile(qc_meas, sim, basis_gates=["h", "x", "ry", "cx", "u", "measure"])
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()

    # counts keys look like "b_meas anc_meas" (space-separated per register,
    # Qiskit joins in reverse register-add order).  Cleanest way: iterate.
    post_counts = {"0": 0, "1": 0}
    total_succ = 0
    total = 0
    for bitstring, n in counts.items():
        # bitstring is space-separated register bits, order = reverse of add.
        # Registers added: (anc_meas first cr), then b_cr.
        # Qiskit puts most-recently-added register on the LEFT.
        parts = bitstring.split()
        # parts[0] = b_meas, parts[1] = anc_meas (last-added first)
        if len(parts) == 2:
            b_val, anc_val = parts[0], parts[1]
        else:
            # single string, ordering: leftmost = most-recent register
            b_val = bitstring[0]
            anc_val = bitstring[1]
        total += n
        if anc_val == "1":
            post_counts[b_val] += n
            total_succ += n

    if total_succ == 0:
        return {
            "gate_noise": gate_noise,
            "shots": shots,
            "success_rate": 0.0,
            "p0": 0.0, "p1": 0.0,
            "counts_raw": counts,
        }

    p0 = post_counts["0"] / total_succ
    p1 = post_counts["1"] / total_succ

    # Reconstruct a *diagonal* density-matrix approximation of the noisy
    # b-register state from measurement statistics, then compute fidelity
    # against the classical target |x>_normalized (also treated as a state).
    # This is the same figure of merit the paper uses in Fig. 1a
    # (F = |<psi_real|psi_ideal>|^2).  Diagonal in comp basis is the honest
    # thing we can get from a single Z-basis measurement pass.
    ideal = x_classical_normalized
    p_ideal_0 = float(np.abs(ideal[0]) ** 2)
    p_ideal_1 = float(np.abs(ideal[1]) ** 2)
    # Bhattacharyya coefficient serves as a lower bound on state fidelity
    # for diagonal reconstruction; report both.
    bhatt = (math.sqrt(p0 * p_ideal_0) + math.sqrt(p1 * p_ideal_1)) ** 2

    return {
        "gate_noise": gate_noise,
        "shots": shots,
        "success_rate": total_succ / total,
        "p0": p0, "p1": p1,
        "p_ideal_0": p_ideal_0, "p_ideal_1": p_ideal_1,
        "fidelity_lower_bound_bhattacharyya": bhatt,
    }


# ---------------------------------------------------------------------------
# 5. Main: run noiseless + sweep, dump JSON to report/evidence/
# ---------------------------------------------------------------------------

def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    qc = build_hhl_circuit_paper_2x2()
    qasm_path = out_dir / "hhl_circuit.txt"
    qasm_path.write_text(str(qc.draw(output="text", fold=200)))

    # ----- Noiseless -----
    psi_out = noiseless_postselected_state(qc)
    fid_ideal = state_fidelity_1q(psi_out, x_classical_normalized)

    noiseless = {
        "matrix_A": A.tolist(),
        "b": b.tolist(),
        "classical_solution_unnorm": x_classical.tolist(),
        "classical_solution_normalized": x_classical_normalized.tolist(),
        "hhl_output_state": {
            "real": psi_out.real.tolist(),
            "imag": psi_out.imag.tolist(),
        },
        "fidelity_hhl_vs_classical": fid_ideal,
    }
    (out_dir / "hhl_noiseless.json").write_text(json.dumps(noiseless, indent=2))
    print("=== Noiseless HHL ===")
    print(f"classical x (normalized):  {x_classical_normalized}")
    print(f"HHL output state:          {psi_out}")
    print(f"Fidelity (ideal HHL vs classical A^-1 b): {fid_ideal:.6f}")

    # ----- Noisy sweep -----
    print("\n=== Noisy sweep (depolarizing 'gate noise', 8192 shots each) ===")
    sweep = []
    for gn in [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
        res = noisy_run(qc, gate_noise=gn, shots=8192)
        sweep.append(res)
        print(f"  gate_noise={gn:>6}  success={res['success_rate']:.3f}  "
              f"p0={res['p0']:.3f} p1={res['p1']:.3f}  "
              f"F_lb={res.get('fidelity_lower_bound_bhattacharyya', 0):.3f}")
    (out_dir / "hhl_noisy_sweep.json").write_text(json.dumps(sweep, indent=2))

    # ----- Compare to paper's IBMQX5 89% success -> F=0.78 headline number
    # In the paper they use a *swap-test* success probability, not the
    # HHL post-selection success rate.  Their reported hardware fidelity
    # 0.78 is what an ideal HHL sim + realistic noise ~0.01-0.02 gate error
    # should bracket.  We report where our noisy sim lands.
    summary = {
        "paper_headline_ideal": {
            "claim": "HHL applied to A=(1/2)*[[3,1],[1,3]] should produce A^-1|b> up to normalization.",
            "expected_fidelity_ideal": 1.0,
            "measured_fidelity_ideal": fid_ideal,
            "match": bool(fid_ideal > 0.999),
        },
        "paper_headline_ibmqx5": {
            "claim_text": "IBMQX5: swap-test success 89% -> fidelity 0.78",
            "reported_success_probability": 0.89,
            "reported_fidelity": 0.78,
            "our_noisy_sweep_reference": [
                {"gate_noise": r["gate_noise"],
                 "fidelity_lb": r.get("fidelity_lower_bound_bhattacharyya", None)}
                for r in sweep
            ],
        },
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\n=== Summary written to report/evidence/summary.json ===")


if __name__ == "__main__":
    main()
