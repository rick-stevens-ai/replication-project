#!/usr/bin/env python3
"""
Independent replication of arXiv:2308.02536 (qgym).

The paper's central verifiable claim (proof-of-concept):
"even basic non-optimized RL agents can offer improvements over a standard
[ALAP / heuristic] method."

We reproduce this claim on the ROUTING task (mentioned as one of qgym's
provided environments) by:
  1. Training a small PPO agent on qgym.envs.Routing for a modest number of steps.
  2. Evaluating SWAP count vs Qiskit's default routing (BasicSwap /
     SabreSwap heuristic) on the same random interaction circuits over the
     same coupling graph.
  3. Reporting mean SWAP count per random circuit.

If RL final SWAP count is <= Qiskit's mean SWAP count on the same
instances, the qualitative claim ("RL can match or beat heuristic") is
supported at this small scale.

We use a small ring/grid coupling graph so training completes in minutes on CPU.
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path

import networkx as nx
import numpy as np

# --- qgym / RL ---
from qgym.envs.routing import Routing
from qgym.generators.interaction import BasicInteractionGenerator
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# --- Qiskit routing baseline ---
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, PassManager
from qiskit.transpiler.passes import SabreSwap, BasicSwap, TrivialLayout

OUT_DIR = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 20260703
random.seed(SEED)
np.random.seed(SEED)

# ---------- Coupling graph: 5-qubit path (linear line topology) ----------
N_QUBITS = 5
edges = [(i, i + 1) for i in range(N_QUBITS - 1)]  # 0-1-2-3-4
coupling_graph = nx.Graph()
coupling_graph.add_nodes_from(range(N_QUBITS))
coupling_graph.add_edges_from(edges)

# ---------- Training ----------
def make_env():
    env = Routing(
        connection_graph=coupling_graph,
        interaction_generator=BasicInteractionGenerator(max_length=5, seed=SEED),
        max_observation_reach=5,
    )
    return env

print("[train] building env...")
env = DummyVecEnv([make_env])

TRAIN_STEPS = 100_000  # matches paper's 10^5 steps for the scheduling POC
print(f"[train] training PPO for {TRAIN_STEPS} steps...")
t0 = time.time()
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=0,
    seed=SEED,
    n_steps=256,
    batch_size=64,
    n_epochs=4,
    learning_rate=3e-4,
)
model.learn(total_timesteps=TRAIN_STEPS)
train_time = time.time() - t0
print(f"[train] done in {train_time:.1f}s")

# ---------- Test set: generate N random interaction circuits ----------
N_TEST = 30
MAX_INTERACTION_LEN = 5  # match training regime (paper uses <=5 gates)

def sample_interactions(rng, n_gates):
    """Return list[(q,q')] of two-qubit interactions on logical qubits."""
    inters = []
    for _ in range(n_gates):
        a, b = rng.sample(range(N_QUBITS), 2)
        inters.append((a, b))
    return inters

rng = random.Random(SEED + 1)
test_circuits = [sample_interactions(rng, MAX_INTERACTION_LEN) for _ in range(N_TEST)]

# ---------- Qiskit baseline: SabreSwap ----------
cmap = CouplingMap(couplinglist=[list(e) for e in edges]
                                + [list(reversed(e)) for e in edges])

def qiskit_swap_count(interactions, method="sabre"):
    qc = QuantumCircuit(N_QUBITS)
    for (a, b) in interactions:
        qc.cx(a, b)
    if method == "sabre":
        pm = PassManager([TrivialLayout(cmap), SabreSwap(cmap, heuristic="basic", seed=SEED)])
    else:
        pm = PassManager([TrivialLayout(cmap), BasicSwap(cmap)])
    routed = pm.run(qc)
    return sum(1 for inst in routed.data if inst.operation.name == "swap")

qiskit_sabre_swaps = [qiskit_swap_count(c, "sabre") for c in test_circuits]
qiskit_basic_swaps = [qiskit_swap_count(c, "basic") for c in test_circuits]

# ---------- RL agent evaluation ----------
def rl_swap_count(interactions):
    """Roll out trained PPO agent, count swap actions.

    qgym Routing action space is Discrete(n_edges + 1):
      action == 0  -> surpass current gate
      action >= 1  -> insert SWAP on edge (action-1)
    Uses env's authoritative swap_gates_inserted deque for the count.
    """
    eval_env = Routing(
        connection_graph=coupling_graph,
        interaction_generator=BasicInteractionGenerator(max_length=len(interactions), seed=SEED),
        max_observation_reach=5,
    )
    ic = np.array(interactions, dtype=np.int_)
    obs, _info = eval_env.reset(seed=SEED, options={"interaction_circuit": ic})
    steps = 0
    done = False
    max_steps = 200
    while not done and steps < max_steps:
        action, _ = model.predict(obs, deterministic=True)
        a = int(action)
        obs, reward, terminated, truncated, info = eval_env.step(a)
        steps += 1
        done = terminated or truncated
    swaps = len(eval_env._state.swap_gates_inserted)
    return swaps, steps, terminated

rl_swaps, rl_steps, rl_done = [], [], []
for c in test_circuits:
    s, st, d = rl_swap_count(c)
    rl_swaps.append(s)
    rl_steps.append(st)
    rl_done.append(d)

# ---------- Summary ----------
def stats(xs):
    return {"mean": float(np.mean(xs)), "median": float(np.median(xs)),
            "min": int(min(xs)), "max": int(max(xs))}

results = {
    "seed": SEED,
    "n_qubits": N_QUBITS,
    "topology": "path5",
    "n_test_circuits": N_TEST,
    "max_interaction_len": MAX_INTERACTION_LEN,
    "train_steps": TRAIN_STEPS,
    "train_time_sec": train_time,
    "qiskit_sabre_swaps": {"per_circuit": qiskit_sabre_swaps, **stats(qiskit_sabre_swaps)},
    "qiskit_basic_swaps": {"per_circuit": qiskit_basic_swaps, **stats(qiskit_basic_swaps)},
    "qgym_ppo_swaps": {"per_circuit": rl_swaps, **stats(rl_swaps)},
    "qgym_ppo_completed_fraction": float(sum(rl_done) / len(rl_done)),
    "qgym_ppo_mean_episode_len": float(np.mean(rl_steps)),
    "versions": {
        "qgym": __import__("qgym").__version__,
        "stable_baselines3": __import__("stable_baselines3").__version__,
        "qiskit": __import__("qiskit").__version__,
    },
}

# Verdict decision (numeric):
ppo_mean = results["qgym_ppo_swaps"]["mean"]
sabre_mean = results["qiskit_sabre_swaps"]["mean"]
basic_mean = results["qiskit_basic_swaps"]["mean"]
if ppo_mean <= sabre_mean:
    replication_claim = "RL <= Qiskit SabreSwap (headline claim SUPPORTED at N=%d qubits)" % N_QUBITS
elif ppo_mean <= basic_mean:
    replication_claim = "RL <= Qiskit BasicSwap but > SabreSwap (partial support)"
else:
    replication_claim = "RL > both Qiskit heuristics (claim NOT supported at this scale)"
results["numeric_verdict"] = replication_claim

out_path = OUT_DIR / "results.json"
out_path.write_text(json.dumps(results, indent=2))
print(f"\n[done] wrote {out_path}")
print(json.dumps(
    {k: v for k, v in results.items() if not isinstance(v, dict) or "mean" in v},
    indent=2, default=str))
