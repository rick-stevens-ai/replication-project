"""Quick smoke test: noiseless Shor for N=15, base a=7, and confirm
success rate (~ 50% is expected because a=7 has order 4 mod 15, and half
of measured phases give trivial factors)."""

import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator
from shor_noise import shor15_circuit, phase_to_factor

rng = np.random.default_rng(42)
qc = shor15_circuit(a=7, n_count=8, eps=0.0, rng=rng)
sim = AerSimulator(method="statevector")
tqc = transpile(qc, sim, optimization_level=0)
counts = sim.run(tqc, shots=4096, seed_simulator=42).result().get_counts()
succ = 0
factors = {}
for bitstr, c in counts.items():
    meas = int(bitstr, 2)  # left-to-right = MSB (Qiskit c[n-1]..c[0]) but phase reg reversed
    fac = phase_to_factor(meas, 8, 7, 15)
    if fac is not None:
        succ += c
        factors[fac] = factors.get(fac, 0) + c
print(f"Noiseless Shor N=15, a=7, n_count=8, 4096 shots:")
print(f"  success shots: {succ}/4096 = {succ/4096:.3f}")
print(f"  factors found: {factors}")
print(f"  # distinct measurement outcomes: {len(counts)}")
top = sorted(counts.items(), key=lambda kv: -kv[1])[:8]
print("  top-8 outcomes:")
for bs, c in top:
    print(f"    {bs}  int={int(bs,2):3d}  count={c}  phase={int(bs,2)/256:.4f}")
