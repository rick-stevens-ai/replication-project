"""Standalone Shor N=15 depolarizing noise sweep. Uses n_count=5 phase
qubits (still gives 3/4 QPE success in the noiseless case since the four
phase peaks 0, 8, 16, 24 in the 32-bin grid are still exactly at 0, 1/4,
1/2, 3/4). Density matrix simulator size: 2^(5+4)=512 complex --> tiny."""

import json, time
from pathlib import Path
import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from shor_noise import shor15_circuit, phase_to_factor


def run(n_count=5, shots=4096, p_list=None, seed=20260703,
        outdir=Path("../report/evidence")):
    if p_list is None:
        p_list = [0.0, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2, 5e-2, 1e-1]
    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    qc = shor15_circuit(a=7, n_count=n_count, eps=0.0, rng=rng)
    results = []
    for p in p_list:
        t0 = time.time()
        if p == 0.0:
            sim = AerSimulator(method="statevector")
        else:
            nm = NoiseModel()
            one_q = ["u","u1","u2","u3","h","x","y","z","s","sdg","t","tdg",
                     "p","rz","rx","ry","id"]
            two_q = ["cx","cz","cp","swap"]
            nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), one_q)
            nm.add_all_qubit_quantum_error(depolarizing_error(min(1.0, p*10), 2), two_q)
            sim = AerSimulator(method="density_matrix", noise_model=nm)
        tqc = transpile(qc, sim, optimization_level=0)
        counts = sim.run(tqc, shots=shots, seed_simulator=seed).result().get_counts()
        succ = 0
        for bs, c in counts.items():
            meas = int(bs, 2)
            if phase_to_factor(meas, n_count, 7, 15) is not None:
                succ += c
        rate = succ / shots
        dt = time.time() - t0
        results.append({"p_1q": p, "p_2q": min(1.0, p*10),
                        "success_count": succ, "shots": shots,
                        "success_rate": rate, "time_s": round(dt, 2)})
        print(f"p_1q={p:>8.4g} p_2q={min(1.0,p*10):>7.4g} rate={rate:.4f} "
              f"({succ}/{shots}) t={dt:.1f}s")
    payload = {
        "experiment": "Shor N=15 (a=7) depolarizing noise sweep",
        "N": 15, "a": 7, "n_count": n_count, "shots": shots,
        "seed": seed,
        "noise_model": "depolarizing_error(p,1) on 1q gates, "
                       "depolarizing_error(10p,2) on 2q gates (clamped 1.0)",
        "results": results,
    }
    (outdir / "shor15_depolarizing.json").write_text(json.dumps(payload, indent=2))
    print(f"Wrote shor15_depolarizing.json")


if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"total {time.time()-t0:.1f}s")
