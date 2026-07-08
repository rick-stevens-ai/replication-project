#!/usr/bin/env python
"""3-judge Argo panel for the qgym (arXiv:2308.02536) replication verdict."""
import json, urllib.request, sys

ARGO = "http://localhost:44497/v1/chat/completions"
KEY = "stevens"

EVIDENCE = """
PAPER: arXiv:2308.02536 "qgym: A Gym for Training and Benchmarking RL-Based Quantum Compilation".
It is a SOFTWARE-FRAMEWORK paper. Its ONLY empirical claim is a proof-of-concept (PoC), Sec III.B / Figs 3-4:
  Claim H1 (mechanism): Because the (Pauli-)X gate and CNOT COMMUTE, a commutation-aware schedule of the
     Fig.3(A) circuit (X, CNOT, measure) is STRICTLY SHORTER than the standard ALAP schedule that ignores
     commutation. (Fig 3B ALAP vs Fig 3C optimal.)
  Claim H2 (training dynamics): A VANILLA PPO agent (stable-baselines3, MultiInputPolicy) trained in qgym's
     Scheduling env for 1e5 steps on <=5-gate random circuits shows (Fig 4A) mean EPISODE LENGTH DECREASING
     and (Fig 4B) mean REWARD INCREASING over training; reward = -5 illegal, -1 per cycle advance, else 0.
  Claim H3 (headline): "even basic non-optimized RL agents can offer improvements over a standard ALAP method"
     (agent recovers the optimal Fig 3C schedule).

INDEPENDENT REPLICATION RESULTS (real runs, qgym 0.3.1, stable-baselines3 2.4.1, qiskit 2.4.2, CPU):

RESULT for H1 (mechanism) -- REPRODUCED, deterministic:
  Built Fig.3(A) circuit as qgym Gates; computed ALAP schedule length from the commutation blocking-matrix.
  * ALAP without any commutation rule: 23 cycles.
  * Commutation-aware (X<->CNOT commute, plus qgym default disjoint/same-gate rules): 13 cycles.
  * => commutation gives a STRICTLY SHORTER schedule (13 < 23). Exactly the Fig 3B-vs-3C effect. MATCH.

RESULT for H2 (training dynamics) -- DID NOT REPRODUCE (two independent runs agree):
  Run A (n_steps=1024): 88 episodes, mean episode length first-20%=63.3 -> last-20%=503.9 (INCREASED, not decreased).
  Run B (n_steps=256, run_scheduling.py): 178 episodes, episode-length deciles
     [39,36,39,37,46,53,60,83,117,1885]  -> length EXPLODES late (INCREASED);
     reward deciles [-93,-72,-73,-63,-81,-84,-82,-104,-157,-1944] -> reward DECREASED.
  Both runs: the vanilla PPO agent collapses into a degenerate "keep advancing cycles" policy and does NOT
  reproduce the paper's decreasing-length / increasing-reward Fig.4 trend with default hyperparameters at 1e5 steps.

RESULT for H3 (headline / recover optimal schedule) -- NOT ACHIEVED:
  Trained agents did not complete the Fig.3(A) scheduling within a 2000-step cap (completion fraction ~0),
  so they did not recover the optimal Fig 3C schedule. PPO mean test schedule = 200 (step-capped) vs ALAP mean = 9.5.

SUMMARY: The paper's underlying quantum-compilation MECHANISM (commutation shortens the schedule) reproduces
exactly and deterministically. The paper's RL proof-of-concept training-dynamics claim (Fig.4 trends, agent
beats ALAP) did NOT reproduce with a vanilla PPO agent at the paper's stated 1e5 steps and default settings.
"""

RUBRIC = """
You are grading an INDEPENDENT REPLICATION. Choose ONE verdict from:
  REPLICATED  - headline number/claim reproduced within tolerance on a real simulation
  PARTIAL     - some claims reproduced, others not
  SPOT-CHECK  - code/method verified & a real demo run, but the full headline claim not established
  CONTRADICTED- replication actively contradicts the paper's claim
  NO-GO / BLOCKED / FAILED - could not run
Weigh that this is a framework paper whose sole empirical content is the PoC. The mechanism (H1) reproduced
deterministically; the RL training-dynamics PoC (H2/H3) did not reproduce at the paper's stated settings.
Answer in the form:
VERDICT: <one label>
REASON: <2-4 sentences>
"""

def ask(model):
    body = {
        "model": model,
        "messages": [
            {"role":"system","content":"You are a rigorous scientific replication judge."},
            {"role":"user","content": EVIDENCE + "\n" + RUBRIC},
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(ARGO, data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]

if __name__ == "__main__":
    models = ["argo:gpt-4o", "argo:claude-opus-4.8", "argo:gpt-o3-mini"]
    out = {}
    for m in models:
        try:
            out[m] = ask(m)
            print(f"===== {m} =====\n{out[m]}\n")
        except Exception as e:
            out[m] = f"ERROR: {e}"
            print(f"===== {m} ERROR: {e}")
    with open("../report/evidence/judge_panel.json","w") as f:
        json.dump(out, f, indent=2)
    print("WROTE judge_panel.json")
