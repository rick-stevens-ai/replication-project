"""Smoke test: verify sim probability P(1) after A Q^m equals sin^2((2m+1)theta_a)."""
import math, sys
sys.path.insert(0, '.')
from mlae_replicate import build_measure_circuit
from qiskit import transpile
from qiskit_aer import AerSimulator

a = 1/3
theta_a = math.asin(math.sqrt(a))
sim = AerSimulator()
print(f"a={a}, theta_a={theta_a:.6f}")
print(f"{'m':>3s} {'expected p1':>14s} {'measured (N=20000)':>20s}")
for m in [0, 1, 2, 3, 5, 8]:
    qc = build_measure_circuit(theta_a, m)
    tqc = transpile(qc, sim)
    res = sim.run(tqc, shots=20000, seed_simulator=42+m).result()
    c1 = res.get_counts().get('1', 0)
    p_meas = c1 / 20000
    p_exp = math.sin((2*m+1)*theta_a)**2
    print(f"{m:3d} {p_exp:14.6f} {p_meas:20.6f}  diff={p_meas-p_exp:+.4f}")
