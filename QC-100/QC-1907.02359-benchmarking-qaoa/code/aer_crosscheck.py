#!/usr/bin/env python3
"""Cross-check: rerun p=1 QAOA on 3reg_n8 using Aer shot-based QASM simulator
with the optimized parameters from the statevector run and confirm the
approximation ratio matches within shot noise."""
import json, math
from pathlib import Path
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

here = Path(__file__).resolve().parent
res = json.load(open(here.parent / "report" / "evidence" / "qaoa_results.json"))

# Rebuild the exact same 3reg_n8_s23 graph and its p=1 optimal params
G = nx.random_regular_graph(3, 8, seed=23)
rec = next(r for r in res["results"] if r["graph"] == "3reg_n8_s23" and r["p"] == 1)
params = rec["opt_params"]
gamma, beta = params[0], params[1]
Ep_sv = rec["Ep"]; alpha_sv = rec["alpha"]; Cmax = rec["Cmax"]

n = G.number_of_nodes()
qc = QuantumCircuit(n, n)
for q in range(n): qc.h(q)
for (u, v) in G.edges(): qc.rzz(gamma, u, v)
for q in range(n): qc.rx(2 * beta, q)
qc.measure(range(n), range(n))

sim = AerSimulator()
tqc = transpile(qc, sim)
shots = 20000
job = sim.run(tqc, shots=shots, seed_simulator=42)
counts = job.result().get_counts()

def cut(bitstr):
    bits = [int(b) for b in bitstr[::-1]]  # qiskit little-endian
    return sum(1 for u, v in G.edges() if bits[u] != bits[v])

mean_cut = 0.0
ground_shots = 0
for bs, c in counts.items():
    cv = cut(bs)
    mean_cut += cv * c
    if cv == Cmax:
        ground_shots += c
mean_cut /= shots
alpha_shots = mean_cut / Cmax
P_ground_shots = ground_shots / shots

out = {
    "graph": "3reg_n8_s23", "p": 1, "gamma": gamma, "beta": beta,
    "Cmax": Cmax, "shots": shots,
    "statevector": {"Ep": Ep_sv, "alpha": alpha_sv, "P_ground": rec["P_ground"]},
    "shot_based":  {"mean_cut": mean_cut, "alpha": alpha_shots, "P_ground": P_ground_shots},
    "alpha_delta": abs(alpha_sv - alpha_shots),
    "match_within_shot_noise_0p02": abs(alpha_sv - alpha_shots) < 0.02,
}
print(json.dumps(out, indent=2))
json.dump(out, open(here.parent / "report" / "evidence" / "aer_shot_crosscheck.json", "w"), indent=2)
