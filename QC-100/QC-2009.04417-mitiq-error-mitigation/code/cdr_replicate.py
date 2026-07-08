"""
Bonus replication: Mitiq CDR (Clifford Data Regression) — arXiv:2009.04417 Section 6.
Uses cirq-native circuit (Mitiq's CDR is easiest with cirq) with depolarizing noise.
Claim: CDR-mitigated expectation value should be closer to noiseless truth than raw noisy.
"""
import json
from pathlib import Path

import numpy as np
import cirq

from mitiq import cdr, Observable, PauliString

EVIDENCE = Path(__file__).resolve().parent.parent / "report" / "evidence"

# Build a 2-qubit circuit: Clifford-ish structure with a few non-Clifford Rz gates
qubits = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H.on(qubits[0]),
    cirq.CNOT.on(qubits[0], qubits[1]),
    cirq.rz(0.5).on(qubits[0]),
    cirq.rz(1.2).on(qubits[1]),
    cirq.CNOT.on(qubits[0], qubits[1]),
    cirq.rz(0.7).on(qubits[0]),
    cirq.H.on(qubits[0]),
)

# Observable Z0
obs = Observable(PauliString("ZI"))


# 2-qubit Z⊗I matrix (Z on qubit 0, identity on qubit 1)
Z_MAT = np.array([[1, 0], [0, -1]], dtype=complex)
I_MAT = np.eye(2, dtype=complex)
Z0_MAT = np.kron(I_MAT, Z_MAT)  # cirq little-endian: qubit 0 is rightmost


def _expval_from_rho(rho: np.ndarray) -> float:
    return float(np.real(np.trace(Z0_MAT @ rho)))


def noiseless_executor(circ: cirq.Circuit) -> float:
    """Simulator: exact density-matrix, return <Z0>."""
    sim = cirq.DensityMatrixSimulator()
    rho = sim.simulate(circ).final_density_matrix
    return _expval_from_rho(rho)


def make_noisy_executor(p: float = 0.02):
    def _exec(circ: cirq.Circuit) -> float:
        # add depolarizing noise after each moment
        noisy = circ.with_noise(cirq.depolarize(p=p))
        sim = cirq.DensityMatrixSimulator()
        rho = sim.simulate(noisy).final_density_matrix
        return _expval_from_rho(rho)
    return _exec


def main():
    noisy_exec = make_noisy_executor(p=0.02)

    truth = noiseless_executor(circuit)
    raw_noisy = noisy_exec(circuit)

    # CDR: build training circuits (near-Clifford), fit linear regression
    cdr_value = cdr.execute_with_cdr(
        circuit,
        executor=noisy_exec,
        simulator=noiseless_executor,  # ideal simulator for training data
        num_training_circuits=10,
        fraction_non_clifford=0.2,
    )

    err_raw = abs(raw_noisy - truth)
    err_cdr = abs(cdr_value - truth)

    summary = {
        "paper": "arXiv:2009.04417 (Mitiq)  §6 CDR",
        "claim_tested": "CDR-mitigated <Z0> is closer to noiseless truth than raw noisy <Z0>.",
        "circuit_qubits": 2,
        "circuit_ops": len(list(circuit.all_operations())),
        "noise_model": "cirq.depolarize(p=0.02) per moment",
        "observable": "Z on qubit 0",
        "truth": truth,
        "raw_noisy": raw_noisy,
        "cdr_value": cdr_value,
        "err_raw": err_raw,
        "err_cdr": err_cdr,
        "improvement_ratio": err_raw / max(err_cdr, 1e-12),
        "verdict_local": "REPLICATED" if err_cdr < err_raw else "CONTRADICTED",
    }

    outp = EVIDENCE / "cdr_results.json"
    outp.write_text(json.dumps(summary, indent=2))
    print("CDR bonus:")
    print(f"  truth    = {truth:+.4f}")
    print(f"  raw noisy= {raw_noisy:+.4f}  err={err_raw:.4f}")
    print(f"  cdr      = {cdr_value:+.4f}  err={err_cdr:.4f}")
    print(f"  verdict  = {summary['verdict_local']}   (improvement x{summary['improvement_ratio']:.2f})")
    print(f"  wrote {outp}")


if __name__ == "__main__":
    main()
