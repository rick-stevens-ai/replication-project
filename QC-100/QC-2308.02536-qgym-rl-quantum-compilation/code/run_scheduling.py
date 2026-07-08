#!/usr/bin/env python3
"""
Independent replication of arXiv:2308.02536 (qgym) - SCHEDULING task.

This mirrors the paper's demonstrated proof-of-concept (Sec III.B "Experiments
and Results"):

  "During training, a quantum circuit with at most 5 gates was randomly
   generated at the start of each episode. Fig. 4 shows the mean episode
   length and mean episode reward for the 10^5 total steps that were taken
   during training. Fig. 4(A) shows that the mean episode length decreases,
   while Fig. 4(B) shows an increase in reward. ... we show that even basic
   non-optimized RL agents can offer improvements over a standard ALAP
   method."

We reproduce this by:
  1. Building qgym.envs.Scheduling with a 3-qubit MachineProperties.
  2. Training vanilla PPO from stable-baselines3 for 10^5 steps on <=5 gate
     circuits (matching the paper).
  3. Recording mean episode length + mean reward over training (buckets).
  4. Comparing final trained-agent mean episode length vs an ALAP baseline
     scheduler run on the SAME distribution of test circuits.
  5. Verdict: the paper's claim (Fig. 4 monotone trends + RL <= ALAP) is
     supported if training curves show decrease in length + increase in
     reward AND RL episode length <= ALAP episode length on test circuits.
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path
from collections import deque

import numpy as np

from qgym.envs.scheduling import Scheduling
from qgym.envs.scheduling.machine_properties import MachineProperties
from qgym.generators.circuit import BasicCircuitGenerator
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 20260703
random.seed(SEED); np.random.seed(SEED)

N_QUBITS = 3
MAX_GATES = 5  # paper: "at most 5 gates"
TRAIN_STEPS = 100_000  # paper: 10^5 steps

GATES = {"x": 2, "y": 2, "z": 1, "h": 2, "cnot": 4, "measure": 10, "prep": 1}


def make_machine():
    mp = MachineProperties(n_qubits=N_QUBITS)
    mp.add_gates(GATES)
    return mp


def make_env():
    return Scheduling(
        make_machine(),
        max_gates=MAX_GATES,
        circuit_generator=BasicCircuitGenerator(seed=SEED),
    )


# -------- Training callback to record per-episode length + reward --------
class EpisodeLogger(BaseCallback):
    def __init__(self):
        super().__init__()
        self.episode_lengths = []
        self.episode_rewards = []
        self._cur_len = 0
        self._cur_rew = 0.0

    def _on_step(self) -> bool:
        # SB3 gives locals["rewards"], locals["dones"] as arrays (VecEnv)
        r = float(self.locals["rewards"][0])
        d = bool(self.locals["dones"][0])
        self._cur_len += 1
        self._cur_rew += r
        if d:
            self.episode_lengths.append(self._cur_len)
            self.episode_rewards.append(self._cur_rew)
            self._cur_len = 0
            self._cur_rew = 0.0
        return True


print(f"[train] PPO for {TRAIN_STEPS} steps on qgym.Scheduling, {N_QUBITS} qubits, up to {MAX_GATES} gates...")
venv = DummyVecEnv([make_env])
# PPO with SB3 defaults; larger n_steps improves stability on this env.
model = PPO(
    "MultiInputPolicy",
    venv,
    verbose=0,
    seed=SEED,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    learning_rate=3e-4,
    gamma=0.99,
    ent_coef=0.01,
)
cb = EpisodeLogger()
t0 = time.time()
model.learn(total_timesteps=TRAIN_STEPS, callback=cb)
train_time = time.time() - t0
n_eps = len(cb.episode_lengths)
print(f"[train] done in {train_time:.1f}s, {n_eps} episodes")

# Bucket into deciles for a paper-Fig4-style curve
def buckets(xs, k=10):
    xs = np.asarray(xs, dtype=float)
    if len(xs) < k:
        return xs.tolist()
    idx = np.linspace(0, len(xs), k + 1, dtype=int)
    return [float(xs[idx[i]:idx[i+1]].mean()) for i in range(k)]

ep_len_curve = buckets(cb.episode_lengths, 10)
ep_rew_curve = buckets(cb.episode_rewards, 10)


# -------- Test evaluation: PPO vs ALAP --------
def sample_circuit(rng):
    """Sample a random circuit up to MAX_GATES gates from a common distribution."""
    n = rng.randint(1, MAX_GATES)
    single_qubit = ["x", "y", "z", "h", "measure"]
    circ = []
    for _ in range(n):
        if rng.random() < 0.3:  # cnot
            a, b = rng.sample(range(N_QUBITS), 2)
            circ.append(("cnot", (a, b)))
        else:
            g = rng.choice(single_qubit)
            q = rng.randrange(N_QUBITS)
            circ.append((g, (q,)))
    return circ


def alap_schedule_length(circ, gate_durations):
    """
    Standard ALAP scheduling with per-qubit ready times, respecting per-gate
    durations. Two-qubit gates block both qubits. This is the "priority-based
    ALAP" baseline referenced by the paper.
    Returns schedule length in cycles.
    """
    qubit_free = [0] * N_QUBITS
    for gname, qs in circ:
        dur = gate_durations[gname]
        start = max(qubit_free[q] for q in qs)
        end = start + dur
        for q in qs:
            qubit_free[q] = end
    return max(qubit_free) if qubit_free else 0


def run_env_with_policy(policy_fn, seed):
    """Sample a circuit using the same BasicCircuitGenerator as training and run
    the given policy_fn(obs, env) -> action to completion. Returns
    (final_cycle, steps, terminated, encoded_circuit_names).
    """
    env = Scheduling(
        make_machine(),
        max_gates=MAX_GATES,
        circuit_generator=BasicCircuitGenerator(seed=seed),
    )
    obs, _ = env.reset(seed=seed)
    steps = 0
    done = False
    while not done and steps < 500:
        a = policy_fn(obs, env)
        obs, r, term, trunc, _ = env.step(a)
        steps += 1
        done = term or trunc
    return env._state.cycle, steps, term, [int(g.name) for g in env._state.circuit_info.encoded]


def ppo_policy(obs, env):
    a, _ = model.predict(obs, deterministic=True)
    return a


def alap_policy(obs, env):
    """Greedy legal-gate-first ALAP-ish policy inside the qgym env: schedule any
    legal gate this cycle; only advance cycle when none are legal."""
    legal = obs["legal_actions"]
    legal_gates = [i for i, x in enumerate(legal) if x]
    if legal_gates:
        return np.array([legal_gates[0], 0], dtype=np.int64)
    return np.array([0, 1], dtype=np.int64)


N_TEST = 50
test_seeds = list(range(SEED + 1000, SEED + 1000 + N_TEST))

alap_cycles, alap_steps, alap_completed = [], [], []
ppo_cycles, ppo_steps_taken, ppo_completed = [], [], []
circuits_seen = []
for s in test_seeds:
    ac, ast, ad, gates_alap = run_env_with_policy(alap_policy, s)
    pc, pst, pd, gates_ppo = run_env_with_policy(ppo_policy, s)
    assert gates_alap == gates_ppo, "circuits diverged for same seed"
    circuits_seen.append(gates_alap)
    alap_cycles.append(ac); alap_steps.append(ast); alap_completed.append(ad)
    ppo_cycles.append(pc); ppo_steps_taken.append(pst); ppo_completed.append(pd)

alap_lens = alap_cycles


def stats(xs):
    xs = list(xs)
    return {"mean": float(np.mean(xs)), "median": float(np.median(xs)),
            "min": float(min(xs)), "max": float(max(xs))}


results = {
    "paper": "arXiv:2308.02536",
    "seed": SEED,
    "n_qubits": N_QUBITS,
    "max_gates": MAX_GATES,
    "train_steps": TRAIN_STEPS,
    "train_time_sec": train_time,
    "n_train_episodes": n_eps,
    "training_curve_episode_length_deciles": ep_len_curve,
    "training_curve_episode_reward_deciles": ep_rew_curve,
    "training_first_decile_mean_len": ep_len_curve[0] if ep_len_curve else None,
    "training_last_decile_mean_len": ep_len_curve[-1] if ep_len_curve else None,
    "training_first_decile_mean_rew": ep_rew_curve[0] if ep_rew_curve else None,
    "training_last_decile_mean_rew": ep_rew_curve[-1] if ep_rew_curve else None,
    "n_test_circuits": N_TEST,
    "alap_schedule_length": {"per_circuit": alap_lens, **stats(alap_lens)},
    "alap_completion_fraction": float(sum(alap_completed) / N_TEST),
    "ppo_schedule_cycles": {"per_circuit": ppo_cycles, **stats(ppo_cycles)},
    "ppo_completion_fraction": float(sum(ppo_completed) / N_TEST),
    "ppo_mean_env_steps": float(np.mean(ppo_steps_taken)),
    "versions": {
        "qgym": __import__("qgym").__version__,
        "stable_baselines3": __import__("stable_baselines3").__version__,
    },
}

# ---- Paper-claim decisions ----
c1_len_decreased = (ep_len_curve[-1] < ep_len_curve[0]) if ep_len_curve else None
c1_rew_increased = (ep_rew_curve[-1] > ep_rew_curve[0]) if ep_rew_curve else None
c2_ppo_le_alap = results["ppo_schedule_cycles"]["mean"] <= results["alap_schedule_length"]["mean"]

results["claims"] = {
    "C1_episode_length_decreased_over_training": bool(c1_len_decreased),
    "C1_episode_reward_increased_over_training": bool(c1_rew_increased),
    "C2_PPO_mean_schedule_cycles_le_ALAP": bool(c2_ppo_le_alap),
    "PPO_completion_fraction_ge_0.9": bool(results["ppo_completion_fraction"] >= 0.9),
}

# Verdict logic
if c1_len_decreased and c1_rew_increased and results["ppo_completion_fraction"] >= 0.9 and c2_ppo_le_alap:
    verdict = "REPLICATED"
elif c1_len_decreased and c1_rew_increased and results["ppo_completion_fraction"] >= 0.9:
    verdict = "PARTIAL"
elif c1_len_decreased or c1_rew_increased:
    verdict = "SPOT-CHECK"
else:
    verdict = "SPOT-CHECK"
results["verdict"] = verdict

out = OUT / "scheduling_results.json"
out.write_text(json.dumps(results, indent=2))
print(f"\n[done] wrote {out}")
for k in ("training_first_decile_mean_len", "training_last_decile_mean_len",
          "training_first_decile_mean_rew", "training_last_decile_mean_rew",
          "ppo_completion_fraction", "claims", "verdict"):
    print(f"  {k}: {results[k]}")
print("  alap_mean:", results["alap_schedule_length"]["mean"])
print("  ppo_mean:", results["ppo_schedule_cycles"]["mean"])
