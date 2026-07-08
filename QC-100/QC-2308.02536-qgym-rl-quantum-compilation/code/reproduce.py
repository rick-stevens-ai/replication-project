#!/usr/bin/env python
"""
Independent replication of the qgym proof-of-concept (arXiv:2308.02536).

Paper: "qgym: A Gym for Training and Benchmarking RL-Based Quantum Compilation"
       van der Linde, de Kok, Bontekoe, Feld (2023).

Headline PoC claim (Sec. III.B, Figs. 3-4):
  A vanilla PPO agent trained in the qgym Scheduling environment on a 2-qubit
  system with commutation rules learns a schedule shorter than the standard
  ALAP schedule, by exploiting that the (Pauli-)X gate and the CNOT commute.
  Fig.3(B) = ALAP schedule (no commutation).  Fig.3(C) = optimal schedule
  (commutation-aware, strictly shorter).  Fig.4 = mean episode length decreases
  and mean reward increases over 1e5 training steps.  Reward: -5 illegal action,
  -1 per timestep increment, 0 otherwise.

This script reproduces the CHECKABLE mechanism + the training-dynamics trend:
  C1: commutation-aware scheduling of the Fig.3(A) circuit yields a strictly
      shorter schedule than ALAP-without-commutation (the whole point of Fig 3B vs 3C).
  C2: a vanilla PPO agent's mean episode length decreases over training (Fig 4A trend).
"""
import json, time, sys
import numpy as np

from qgym.envs import Scheduling
from qgym.envs.scheduling import MachineProperties, CommutationRulebook
from qgym.envs.scheduling.rulebook import CommutationRulebook as CRB
from qgym.custom_types import Gate
from qgym.generators.circuit import BasicCircuitGenerator, NullCircuitGenerator

OUT = {}

# ---------------------------------------------------------------------------
# Machine properties: 2-qubit system. Gate durations (cycles): match paper spirit.
#   x: 1 cycle single-qubit; cnot: 2 cycles two-qubit (typical qgym example);
#   measure: 10 cycles. Durations only affect absolute length, not the
#   ALAP-vs-commutation comparison direction.
# ---------------------------------------------------------------------------
def make_mp():
    mp = MachineProperties(n_qubits=2)
    # include the full gate set emitted by BasicCircuitGenerator (prep,x,y,z,cnot,measure)
    mp.add_gates({"prep": 1, "x": 1, "y": 1, "z": 1, "cnot": 2, "measure": 10})
    return mp

# Fig.3(A) circuit: X on q0, then CNOT(control=q0,target=q1), then measure both.
# qgym Gate = (name, q1, q2).  For single-qubit gates q1==q2.
def fig3_circuit():
    return [
        Gate("x", 0, 0),
        Gate("cnot", 0, 1),
        Gate("measure", 0, 0),
        Gate("measure", 1, 1),
    ]

# X (on the CONTROL qubit of a CNOT) commutes with that CNOT.  The paper's Fig.3
# relies exactly on X<->CNOT commuting so the X can slide past the CNOT.
def x_cnot_commute(g1, g2):
    a, b = g1, g2
    def is_x(g): return g.name == "x"
    def is_cnot(g): return g.name == "cnot"
    # X on control qubit commutes with CNOT
    if is_x(a) and is_cnot(b) and a.q1 == b.q1:
        return True
    if is_x(b) and is_cnot(a) and b.q1 == a.q1:
        return True
    return False

# ---------------------------------------------------------------------------
# C1: greedy ALAP schedule length using the dependency (blocking) matrix built
#     from a rulebook, WITHOUT vs WITH the X<->CNOT commutation rule.
#     We schedule as-late-as-possible respecting the blocking matrix and qubit
#     occupancy, and report the total number of cycles used.
# ---------------------------------------------------------------------------
def alap_length(circuit, mp, rulebook):
    """Compute an ALAP schedule length (in cycles) given a commutation rulebook.

    Blocking matrix B[i,j] (i<j) True means gate i must be scheduled before
    gate j is *encountered* going right-to-left cannot pass it. We do a simple
    list-scheduling: process gates from the end; a gate can be placed at the
    latest free cycle on its qubits, but cannot start later than any gate that
    it blocks (non-commuting successor). Returns total cycles.
    """
    n = len(circuit)
    B = rulebook.make_blocking_matrix(circuit)  # B[i,j], i<j, True = i blocks j (no commute)
    durations = {"prep":1, "x":1, "y":1, "z":1, "cnot":2, "measure":10}
    def qubits(g):
        return {g.q1} if g.q1 == g.q2 else {g.q1, g.q2}

    # ALAP: schedule from the back. finish[i] = cycle index (0=last cycle block).
    # We measure schedule length as max over gates of (start_from_end + duration).
    # Represent time as "cycles from the end". Larger = earlier in real time.
    start_from_end = [None]*n
    # process in reverse circuit order (back to front, as paper's agent does)
    # qubit_busy_until[q] = furthest-from-end extent already occupied on qubit q
    qbusy = {0:0, 1:0}
    for i in reversed(range(n)):
        g = circuit[i]
        d = durations[g.name]
        # earliest slot (from end) allowed by qubit occupancy
        slot = max(qbusy[q] for q in qubits(g))
        # must respect non-commuting predecessors already placed (j>i with B[i,j])
        for j in range(i+1, n):
            if B[i, j] and start_from_end[j] is not None:
                # gate i is before gate j in circuit and they don't commute:
                # i must occupy a LATER-in-real-time (smaller from_end) ... actually
                # i precedes j, so i must finish before j starts in real time,
                # i.e. i is further from end => start_from_end[i] >= end_of_j
                slot = max(slot, start_from_end[j] + durations[circuit[j].name])
        start_from_end[i] = slot
        for q in qubits(g):
            qbusy[q] = slot + d
    total = max(start_from_end[i] + durations[circuit[i].name] for i in range(n))
    return int(total)

def run_c1():
    mp = make_mp()
    circ = fig3_circuit()

    rb_nocomm = CRB(default_rules=False)          # NO commutation at all -> pure order
    rb_default = CRB(default_rules=True)           # disjoint-qubit + same-gate only
    rb_paper = CRB(default_rules=True)
    rb_paper.add_rule(x_cnot_commute)              # + X<->CNOT (the paper's rule)

    len_alap_nocomm = alap_length(circ, mp, rb_nocomm)
    len_default     = alap_length(circ, mp, rb_default)
    len_paper       = alap_length(circ, mp, rb_paper)

    # sanity: the blocking matrices
    Bn = rb_nocomm.make_blocking_matrix(circ).astype(int).tolist()
    Bp = rb_paper.make_blocking_matrix(circ).astype(int).tolist()

    OUT["C1_schedule_lengths_cycles"] = {
        "ALAP_no_commutation": len_alap_nocomm,
        "default_rules_only": len_default,
        "paper_rules_X_CNOT_commute": len_paper,
    }
    OUT["C1_blocking_matrix_no_commute"] = Bn
    OUT["C1_blocking_matrix_paper"] = Bp
    OUT["C1_shorter_with_commutation"] = bool(len_paper < len_alap_nocomm)
    print(f"[C1] ALAP (no commutation) length = {len_alap_nocomm} cycles")
    print(f"[C1] commutation-aware (X<->CNOT) length = {len_paper} cycles")
    print(f"[C1] commutation gives strictly shorter schedule: {len_paper < len_alap_nocomm}")
    return len_alap_nocomm, len_paper

# ---------------------------------------------------------------------------
# C2: Train a vanilla PPO agent in the qgym Scheduling env with the paper's
#     reward (-5 illegal, -1 per cycle-advance) and check mean episode length
#     decreases over training (Fig 4A trend).
# ---------------------------------------------------------------------------
def run_c2(total_steps=30000):
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import BaseCallback
    from qgym.envs.scheduling.scheduling_rewarders import BasicRewarder

    mp = make_mp()
    rb = CRB(default_rules=True)
    rb.add_rule(x_cnot_commute)

    # paper reward: illegal action -5, advancing cycle -1, else 0
    rewarder = BasicRewarder(
        illegal_action_penalty=-5.0,
        update_cycle_penalty=-1.0,
        schedule_gate_bonus=0.0,
    )
    # random circuits up to 5 gates (as in paper: "at most 5 gates")
    gen = BasicCircuitGenerator(seed=42)
    env = Scheduling(
        mp,
        max_gates=8,
        circuit_generator=gen,
        rulebook=rb,
        rewarder=rewarder,
    )

    class EpLenCB(BaseCallback):
        def __init__(self):
            super().__init__()
            self.ep_lengths = []
            self.cur = 0
        def _on_step(self):
            self.cur += 1
            done = self.locals["dones"][0]
            if done:
                self.ep_lengths.append(self.cur)
                self.cur = 0
            return True

    cb = EpLenCB()
    model = PPO("MultiInputPolicy", env, verbose=0, seed=0, n_steps=1024, batch_size=256)
    t0 = time.time()
    model.learn(int(total_steps), callback=cb)
    train_secs = time.time() - t0

    ep = np.array(cb.ep_lengths, dtype=float)
    n = len(ep)
    if n >= 20:
        k = max(5, n//5)
        first = float(ep[:k].mean())
        last = float(ep[-k:].mean())
    else:
        first = float(ep[:max(1,n//2)].mean()); last = float(ep[max(1,n//2):].mean())
    OUT["C2_total_steps"] = int(total_steps)
    OUT["C2_num_episodes"] = int(n)
    OUT["C2_mean_ep_len_first_20pct"] = round(first,3)
    OUT["C2_mean_ep_len_last_20pct"] = round(last,3)
    OUT["C2_ep_len_decreased"] = bool(last < first)
    OUT["C2_train_seconds"] = round(train_secs,1)
    print(f"[C2] episodes={n}  mean_ep_len first20%={first:.2f}  last20%={last:.2f}  decreased={last<first}")

    # Evaluate trained agent on the fixed Fig.3(A) circuit: schedule length achieved
    circ = fig3_circuit()
    obs, info = env.reset(options={"circuit": circ})
    steps=0; done=False; illegal=0
    while not done and steps < 2000:
        action, _ = model.predict(obs, deterministic=True)
        obs, r, done, trunc, info = env.step(action)
        steps += 1
        if r <= -5: illegal += 1
        if trunc: break
    # final cycle count from state
    try:
        final_cycles = int(env._state.cycle)
    except Exception:
        final_cycles = None
    OUT["C2_eval_fig3_steps"] = steps
    OUT["C2_eval_fig3_final_cycle"] = final_cycles
    OUT["C2_eval_fig3_illegal_actions"] = illegal
    OUT["C2_eval_fig3_done"] = bool(done)
    print(f"[C2] eval on Fig3(A): steps={steps} final_cycle={final_cycles} done={done} illegal={illegal}")
    return ep.tolist()

if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    run_c1()
    if steps > 0:
        ep_lengths = run_c2(total_steps=steps)
        OUT["ep_length_trace_len"] = len(ep_lengths)
    OUT["qgym_version"] = __import__("qgym").__version__
    import stable_baselines3, qiskit, torch
    OUT["stable_baselines3_version"] = stable_baselines3.__version__
    OUT["torch_version"] = torch.__version__
    with open("../report/evidence/commutation_mechanism.json","w") as f:
        json.dump(OUT, f, indent=2)
    print("\nWROTE report/evidence/commutation_mechanism.json")
