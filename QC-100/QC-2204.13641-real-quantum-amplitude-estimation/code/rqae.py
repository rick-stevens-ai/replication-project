"""
Real Quantum Amplitude Estimation (RQAE) — reimplementation of Algorithm 1 from
Manzano, Musso, Leitao "Real Quantum Amplitude Estimation" arXiv:2204.13641.

Real, shot-based Qiskit Aer simulation. The oracle A_b prepares a state whose
amplitude on |phi>=|0> is (a+b), so that measuring |0> yields probability
(a+b)^2. We use a single working qubit throughout: this is the minimal
"toy problem" of estimating a known amplitude a in [-1,1].

The Grover operator G = -A_b R_|0> A_b^dag R_|phi>  with R_|0> = I-2|0><0|
and R_|phi> = I - 2|phi><phi|. With |phi>=|0> in our toy encoding the second
reflection is identical to the first: R_|phi> = R_|0>. This is convenient
and does not affect the RQAE logic which is what we are validating here.

Because b is chosen so that (a+b) can exceed 1, we cannot just do R_y(2 arcsin(a+b)).
We instead build the sub-normalized target amplitude by encoding on an ancilla:
we prepare a 2-qubit state
    |Psi> = (a+b)|0>|0> + sqrt(1-(a+b)^2)|0>|1>_ancilla + junk on |1>|*>
Then measuring the ancilla in |0> and the primary in |0> yields probability
(a+b)^2 exactly — matching the RQAE construction from the paper (eq 2, 4).

To keep the code compact and provably correct, we implement A_b as an
R_y rotation on a single qubit with angle 2*arcsin(a+b) (valid as long as
|a+b| <= 1). RQAE's shift rule guarantees b in [-1,1] and we cap so that
|a+b| <= 1 by construction of the algorithm (the paper's Algorithm 1 keeps
b = -a^min_i in [-1,1]).

Verdict target: reproduce the quadratic-speedup scaling
  N_oracle ~ 1/eps   (RQAE)  vs   N_oracle ~ 1/eps^2   (classical sampling).
Exactly the headline of Figure 6 in the paper.
"""
from __future__ import annotations
import json, math, os, sys, time
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

RNG = np.random.default_rng(20260704)


def _ry(angle: float) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.ry(angle, 0)
    return qc


# Two-qubit "shifted oracle" encoding.
# We use 2 qubits: q0 = ancilla (state indicator), q1 = shift indicator.
# The "good" state |phi> is |00>. We build A_b so that
#   A_b|00> = (a+b)/S |00> + something orthogonal * sqrt(1 - ((a+b)/S)^2)
# where S is an *encoding scale* chosen large enough that |(a+b)/S| <= 1 always.
# We take S = 2 so any a in [-1,1] and any b in [-1,1] give |a+b|/S <= 1.
# The RQAE algorithm's math still works: measuring |00> gives probability
# ((a+b)/S)^2. We rescale by S in the a_hat formulas.
# Amplitude to be estimated is a' = a/S; b' = b/S; RQAE outputs a'; we return a.
#
# But wait: the paper's algorithm assumes measurement probability = (a+b)^2
# directly and a is in [-1,1]. Introducing a scale S changes the effective
# precision domain by factor S. To keep the math clean we ABSORB the scale
# by re-defining the problem: estimate a_scaled = a/S on the fly. The RQAE
# loop already lives in [-1,1] for a_scaled. On output we return a = S * a_hat.
#
# This is the standard "pad the amplitude" trick used when embedding an
# arbitrary real number into a normalized quantum state; it preserves the
# quadratic-scaling property being replicated.

ENCODING_SCALE = 2.0  # so both a and b in [-1,1] give |(a+b)/S|<=1


def build_A_b(a_plus_b_scaled: float) -> QuantumCircuit:
    """Oracle A_b acting on 1 qubit. We define the 'good' state as |1>, so
    that R_y(2 arcsin(c))|0> = cos(arcsin(c))|0> + sin(arcsin(c))|1> = sqrt(1-c^2)|0> + c|1>.
    Then P(|1>) = c^2 = ((a+b)/S)^2 exactly as RQAE requires.
    Valid for c in [-1,1]; guaranteed by RQAE + S=2.
    """
    c = max(-1.0, min(1.0, a_plus_b_scaled))
    theta = 2.0 * math.asin(c)
    qc = QuantumCircuit(1, name=f"A_b(c={c:.6f})")
    qc.ry(theta, 0)
    return qc


def grover_operator(a_plus_b_scaled: float) -> QuantumCircuit:
    """G = -A_b R_|0> A_b^dag R_|phi>, |phi> = |1> (the 'good' state).
    R_|0> = I - 2|0><0| = diag(-1, +1) = -Z
    R_|phi> = R_|1> = I - 2|1><1| = diag(+1, -1) = +Z
    So G = -A_b (-Z) A_b^dag (Z) = A_b Z A_b^dag Z (up to global phase).
    """
    A = build_A_b(a_plus_b_scaled)
    A_dag = A.inverse()
    qc = QuantumCircuit(1, name=f"G(c={a_plus_b_scaled:.6f})")
    qc.z(0)                       # R_|phi> = Z (|phi>=|1>)
    qc.compose(A_dag, inplace=True)
    qc.z(0)                       # R_|0> = -Z, global sign ignored
    qc.compose(A, inplace=True)
    return qc


def make_circuit_for_k(a_true: float, b: float, k: int) -> QuantumCircuit:
    """Build circuit preparing (A_b|0>) then G^k. Uses scaled amplitude."""
    c = (a_true + b) / ENCODING_SCALE
    qc = QuantumCircuit(1, 1)
    A = build_A_b(c)
    qc.compose(A, inplace=True)
    G = grover_operator(c)
    for _ in range(k):
        qc.compose(G, inplace=True)
    qc.measure(0, 0)
    return qc


SIM = AerSimulator()


def measure_prob(a_true: float, b: float, k: int, shots: int, seed: int) -> Tuple[float, int]:
    """Return (empirical probability of |0> AFTER SCALE-INVERSION, oracle calls).
    Measurement prob is c^2 where c = (a+b)/S. RQAE math wants (a+b)^2. So we
    RETURN c^2 and downstream code operates on the scaled amplitude a_scaled=a/S.
    Oracle calls per shot = 2k+1.
    """
    qc = make_circuit_for_k(a_true, b, k)
    tqc = transpile(qc, SIM)
    job = SIM.run(tqc, shots=shots, seed_simulator=seed)
    result = job.result()
    counts = result.get_counts()
    n1 = counts.get("1", 0)  # |1> is the 'good' state in our encoding
    p_hat = n1 / shots  # empirical estimate of ((a+b)/S)^2
    calls = (2 * k + 1) * shots
    return p_hat, calls


# --- RQAE (Algorithm 1) --------------------------------------------------

@dataclass
class RQAEResult:
    a_true: float
    a_hat: float
    epsilon_final: float
    n_oracle: int
    n_iters: int
    k_max_used: int
    epsilon_target: float
    gamma: float
    q: float
    trace: List[Dict]


def rqae(a_true: float, eps_target: float, gamma: float = 0.05, q: float = 2.0,
         seed: int = 0) -> RQAEResult:
    """Implementation of Algorithm 1 (RQAE) from arXiv:2204.13641.
    Runs a real Qiskit-Aer simulation with `a_true` embedded in the oracle A_b.
    """
    # Parameters (paper Section 3, Eq. 18-19)
    p = 0.5 * math.sin(math.pi / (2.0 * (q + 2.0)))**2
    # T(q, eps) = log_q( q^2 * arcsin(sqrt(2 p(q))) / arcsin(2 eps) )
    try:
        T = max(1, int(math.ceil(
            math.log(q * q * math.asin(math.sqrt(2.0 * p)) /
                     math.asin(2.0 * eps_target)) / math.log(q))))
    except ValueError:
        T = 30
    gamma_i = gamma / T
    # Ni per Eq. (19): Ni = ceil( (1/(2*p^2)) * log(2T/gamma) ). Note p is SQUARED.
    Ni = int(math.ceil((1.0 / (2.0 * p * p)) * math.log(2.0 * T / gamma)))
    p_i = math.sqrt((1.0 / (2.0 * Ni)) * math.log(2.0 / gamma_i))
    # Eq. (14) k_max: pi/(4*arcsin(2*eps_target)) - 1/2
    k_max = int(math.ceil(math.pi / (4.0 * math.asin(2.0 * eps_target)) - 0.5))

    trace: List[Dict] = []
    total_calls = 0
    max_k_used = 0

    # We estimate a_scaled = a/S internally, then multiply by S on output.
    S = ENCODING_SCALE
    a_true_scaled = a_true / S
    # First iteration: b1 (scaled) = sin(pi/(2(q+2))) / 2
    b1_scaled = 0.5 * math.sin(math.pi / (2.0 * (q + 2.0)))
    # We pass the unscaled b to measure_prob which will scale internally
    b1_unscaled = b1_scaled * S
    p_sum, calls_sum = measure_prob(a_true, +b1_unscaled, 0, Ni, seed=seed + 1)
    p_diff, calls_diff = measure_prob(a_true, -b1_unscaled, 0, Ni, seed=seed + 2)
    total_calls += calls_sum + calls_diff
    # p_sum ~= ((a+b1)/S)^2 = (a_scaled + b1_scaled)^2
    # RQAE formula (7): a_scaled_hat = (p_sum - p_diff) / (4*b1_scaled)
    a_hat_scaled = (p_sum - p_diff) / (4.0 * b1_scaled)
    a_max = min(a_hat_scaled + p_i / (2.0 * abs(b1_scaled)), 1.0)
    a_min = max(a_hat_scaled - p_i / (2.0 * abs(b1_scaled)), -1.0)
    a_center = 0.5 * (a_max + a_min)
    eps_cur = 0.5 * (a_max - a_min)

    trace.append({"iter": 0, "k": 0, "b_scaled": b1_scaled, "shots": Ni,
                  "p_sum": p_sum, "p_diff": p_diff,
                  "a_hat_scaled": a_hat_scaled, "a_min_scaled": a_min,
                  "a_max_scaled": a_max, "a_center_scaled": a_center,
                  "eps_cur_scaled": eps_cur, "cum_calls": total_calls})

    # eps_target/eps_cur are on the SCALED amplitude (a_scaled in [-1,1]).
    # If user specified eps_target on unscaled a, they should divide by S first.
    # We treat eps_target as SCALED.
    it = 0
    while eps_cur > eps_target and it < 200:
        it += 1
        b_scaled = -a_min                          # RQAE's shift rule
        b_scaled = max(-1.0, min(1.0, b_scaled))
        # k choice on the SCALED interval width. Per Eq. (14),
        #   k_{i+1} = ceil(pi/(4 arcsin(2 eps_i)) - 1/2)
        # This is only meaningful when 2*eps_i <= 1 (i.e. eps_i <= 0.5).
        # If eps_cur > 0.5 (very wide interval), amplification would push the
        # confidence fan past pi/2 into the second quadrant, causing branch
        # ambiguity in asin. In that regime we stay at k=0 and let the shots
        # tighten the interval before amplifying.
        if 2.0 * eps_cur >= 1.0:
            k = 0
        else:
            # Eq. (14): k = ceil( pi / (4 * arcsin(2*eps_i)) - 1/2 )
            k = int(math.ceil(math.pi / (4.0 * math.asin(2.0 * eps_cur)) - 0.5))
        if k > k_max:
            k = k_max
        if k < 0:
            k = 0
        b_unscaled = b_scaled * S
        p_hat, calls = measure_prob(a_true, b_unscaled, k, Ni, seed=seed + 100 + it)
        total_calls += calls
        max_k_used = max(max_k_used, k)

        p_max = min(p_hat + p_i, 1.0)
        p_min_v = max(p_hat - p_i, 0.0)

        theta_max = math.asin(math.sqrt(p_max)) / (2 * k + 1)
        theta_min = math.asin(math.sqrt(p_min_v)) / (2 * k + 1)
        # These theta values map back to scaled amplitude: sin(theta) = a_scaled + b_scaled
        a_max_new = math.sin(theta_max) - b_scaled
        a_min_new = math.sin(theta_min) - b_scaled
        lo, hi = sorted([a_min_new, a_max_new])
        a_min, a_max = max(-1.0, lo), min(1.0, hi)
        a_center = 0.5 * (a_max + a_min)
        eps_cur = 0.5 * (a_max - a_min)

        trace.append({"iter": it, "k": k, "b_scaled": b_scaled, "shots": Ni,
                      "p_hat": p_hat, "a_min_scaled": a_min, "a_max_scaled": a_max,
                      "a_center_scaled": a_center, "eps_cur_scaled": eps_cur,
                      "cum_calls": total_calls})

    # Un-scale back to true amplitude units
    a_hat_true = a_center * S
    eps_true = eps_cur * S
    return RQAEResult(a_true=a_true, a_hat=a_hat_true, epsilon_final=eps_true,
                      n_oracle=total_calls, n_iters=it, k_max_used=max_k_used,
                      epsilon_target=eps_target * S, gamma=gamma, q=q, trace=trace)


# --- Classical (unamplified) reference -----------------------------------

def classical_amplitude_estimate(a_true: float, eps_target: float, gamma: float = 0.05,
                                 seed: int = 0) -> Dict:
    """Estimate a by direct sampling of A_b (k=0). Needs N ~ 1/eps^2 shots.
    Uses same scaled-oracle encoding as RQAE for a fair oracle-call comparison.
    eps_target here is on the TRUE (unscaled) a.
    Method: compute p_sum-p_diff with a fixed b=1 (scaled b'=0.5).
    a_hat = (p_sum - p_diff) / (4 * b_scaled) * S
    Hoeffding-ish shot bound: N = log(2/gamma) / (2 * (eps_target/S * 2*b_scaled)^2)
    """
    S = ENCODING_SCALE
    b_scaled = 0.5
    b_unscaled = b_scaled * S    # = 1.0
    eps_scaled = eps_target / S
    N = int(math.ceil(math.log(2.0 / gamma) /
                      (2.0 * (eps_scaled * 2.0 * b_scaled)**2)))
    p_sum, calls_sum = measure_prob(a_true, +b_unscaled, 0, N, seed=seed + 11)
    p_diff, calls_diff = measure_prob(a_true, -b_unscaled, 0, N, seed=seed + 22)
    a_hat_scaled = (p_sum - p_diff) / (4.0 * b_scaled)
    a_hat = a_hat_scaled * S
    return {"a_true": a_true, "a_hat": a_hat, "eps_target": eps_target,
            "n_oracle": calls_sum + calls_diff, "shots_per_side": N,
            "b_scaled": b_scaled}


if __name__ == "__main__":
    # Quick smoke test: eps_target is on SCALED amplitude (i.e. divide desired
    # unscaled epsilon by S).
    S = ENCODING_SCALE
    for a_true in (0.3, 0.7, -0.4):
        r = rqae(a_true=a_true, eps_target=0.05 / S, gamma=0.05, q=2.0, seed=1)
        print(json.dumps({"a_true": a_true, "a_hat": r.a_hat,
                          "|err|": abs(r.a_hat - a_true),
                          "eps_final": r.epsilon_final,
                          "n_oracle": r.n_oracle,
                          "iters": r.n_iters, "k_max": r.k_max_used}, indent=2))
