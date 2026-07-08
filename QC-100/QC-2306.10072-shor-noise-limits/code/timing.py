"""Quick timing test: 1 eps, 4 trials, 512 shots."""
import time, numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator
from shor_noise import shor15_circuit, phase_to_factor

sim = AerSimulator(method="statevector")
for eps in (0.0, 0.03, 0.3, 1.0, 3.0, 10.0):
    t0 = time.time()
    rates = []
    for t in range(4):
        rng = np.random.default_rng(1000 + t)
        qc = shor15_circuit(a=7, n_count=8, eps=eps, rng=rng)
        tqc = transpile(qc, sim, optimization_level=0)
        counts = sim.run(tqc, shots=512, seed_simulator=1000+t).result().get_counts()
        succ = 0
        for bs, c in counts.items():
            meas = int(bs, 2)
            if phase_to_factor(meas, 8, 7, 15) is not None:
                succ += c
        rates.append(succ/512)
    dt = time.time() - t0
    print(f"eps={eps}: mean={np.mean(rates):.3f} std={np.std(rates):.3f}  time={dt:.1f}s (4 trials x 512 shots)")
