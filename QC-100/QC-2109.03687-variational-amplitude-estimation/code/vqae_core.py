"""
Variational Quantum Amplitude Estimation (VQAE) — independent replication
of Plekhanov, Rosenkranz, Fiorentini, Lubasch, arXiv:2109.03687v2.

Implements the three algorithms compared in Fig. 4:
  1) Classical Monte-Carlo sampling of the ancilla qubit    → expect δθ ~ Nq^(-1/2)
  2) MLAE (linear schedule)                                  → expect δθ ~ Nq^(-3/4)
  3) Naïve VQAE with k=1, gradient-based variational step    → expect an intermediate
     behavior — ideal scaling Nq^(-3/2) at small M, MC-limited Nq^(-1/2) at large M.

All algorithms operate on statevectors (Qiskit Aer statevector simulator). The
"query oracle" A prepares |chi_0>, the Grover-like operator Q = -R_chi R_good
is built from reflections.

We keep the instance size faithful but small (n = 4 qubits + 1 ancilla) so the
whole comparison finishes in a few minutes on CPU.
"""

import json
import math
import os
import time
from dataclasses import dataclass, asdict
from typing import Callable, List, Tuple

import numpy as np
from scipy.stats import cauchy

# ---------------------------------------------------------------------------
# 1. Problem definition: MC integration of a shifted Cauchy-Lorentz PDF
#    (one of the three distributions used in the paper).
#
#    We encode probabilities p(x) on n qubits and the function value
#    sqrt(f(x)) on an ancilla via a rotation R_y(2 * arcsin(sqrt(f(x)))).
#    The amplitude to be estimated is a = sum_x p(x) f(x).
# ---------------------------------------------------------------------------


def cauchy_lorentz_probs(n: int, x0: float = 0.5, gamma: float = 0.1) -> np.ndarray:
    """Discrete Cauchy-Lorentz probabilities on the grid x_i = i/2^n, normalised."""
    N = 2 ** n
    xs = np.arange(N) / N
    w = cauchy.pdf(xs, loc=x0, scale=gamma)
    w = w / w.sum()
    return w


def linear_f(x: np.ndarray) -> np.ndarray:
    """f(x) = x, a standard choice used in the amplitude-estimation literature."""
    return x


def build_state_chi0(n: int, p: np.ndarray, f_values: np.ndarray) -> np.ndarray:
    """Return |chi_0>_{n+1} = sum_x sqrt(p(x)) |x>_n (sqrt(1-f(x))|0>+sqrt(f(x))|1>).

    Layout: ancilla is the highest-order (leftmost) qubit.  Full state has 2^(n+1) amps.
    """
    N = 2 ** n
    assert p.shape == (N,) and f_values.shape == (N,)
    amps = np.zeros(2 ** (n + 1), dtype=complex)
    sqrt_p = np.sqrt(p)
    sqrt_1mf = np.sqrt(np.clip(1.0 - f_values, 0.0, 1.0))
    sqrt_f = np.sqrt(np.clip(f_values, 0.0, 1.0))
    # index of |anc=0, x>_{n+1} is x; index of |anc=1, x>_{n+1} is x + N
    amps[:N] = sqrt_p * sqrt_1mf
    amps[N:] = sqrt_p * sqrt_f
    return amps


def true_a(p: np.ndarray, f_values: np.ndarray) -> float:
    return float(np.sum(p * f_values))


def prob_ancilla_one(state: np.ndarray, n: int) -> float:
    """Probability of measuring the ancilla in |1> for a full (n+1)-qubit statevector."""
    N = 2 ** n
    return float(np.sum(np.abs(state[N:]) ** 2))


# ---------------------------------------------------------------------------
# 2. Grover-like query operator Q = -R_chi R_good  (implemented on the statevector)
# ---------------------------------------------------------------------------


def apply_R_good(state: np.ndarray, n: int) -> np.ndarray:
    """Reflection about the 'good' subspace where ancilla = 1: flips sign of |anc=1> amps."""
    N = 2 ** n
    out = state.copy()
    out[N:] *= -1.0
    return out


def apply_R_chi(state: np.ndarray, chi0: np.ndarray) -> np.ndarray:
    """Reflection about |chi_0>:  R_chi = 2|chi_0><chi_0| - I."""
    proj = np.vdot(chi0, state)
    return 2.0 * proj * chi0 - state


def apply_Q(state: np.ndarray, chi0: np.ndarray, n: int) -> np.ndarray:
    """Q = -R_chi R_good ."""
    s1 = apply_R_good(state, n)
    s2 = apply_R_chi(s1, chi0)
    return -s2


def apply_Qk(state: np.ndarray, chi0: np.ndarray, n: int, k: int) -> np.ndarray:
    out = state
    for _ in range(k):
        out = apply_Q(out, chi0, n)
    return out


# ---------------------------------------------------------------------------
# 3. Classical MC sampling estimator
# ---------------------------------------------------------------------------


def classical_mc(chi0: np.ndarray, n: int, N_shots: int, rng: np.random.Generator) -> float:
    """Estimate a by measuring ancilla of |chi_0> N_shots times."""
    p1 = prob_ancilla_one(chi0, n)
    hits = rng.binomial(N_shots, p1)
    return hits / N_shots


# ---------------------------------------------------------------------------
# 4. MLAE (Suzuki et al. 2020) with linear schedule m = 1..M
# ---------------------------------------------------------------------------


def mlae_shots(chi0: np.ndarray, n: int, M: int, h: int, rng: np.random.Generator
               ) -> Tuple[List[int], List[int]]:
    """Return (m_list, hits_list) with h shots each and m = 0..M (m=0 == chi_0)."""
    m_list = list(range(M + 1))  # include m=0 == the |chi_0> measurement
    hits = []
    state = chi0.copy()
    for m in m_list:
        p1 = prob_ancilla_one(state, n)
        hits.append(int(rng.binomial(h, p1)))
        # advance to next m
        state = apply_Q(state, chi0, n)
    return m_list, hits


def mlae_log_likelihood(theta: np.ndarray, m_list: List[int], hits: List[int], h: int) -> np.ndarray:
    """Vectorised log-likelihood over theta grid. Suzuki likelihood (Eq. 12)."""
    ll = np.zeros_like(theta)
    for m, hm in zip(m_list, hits):
        angle = (2 * m + 1) * theta
        s2 = np.sin(angle) ** 2
        c2 = np.cos(angle) ** 2
        # guard log(0)
        s2 = np.clip(s2, 1e-300, 1.0)
        c2 = np.clip(c2, 1e-300, 1.0)
        ll += hm * np.log(s2) + (h - hm) * np.log(c2)
    return ll


def mlae_estimate_theta(m_list: List[int], hits: List[int], h: int, n_grid: int = 5000) -> float:
    """Brute-force max of the log-likelihood on theta in (0, pi/2), matching the paper."""
    theta_grid = np.linspace(1e-6, math.pi / 2 - 1e-6, n_grid)
    ll = mlae_log_likelihood(theta_grid, m_list, hits, h)
    return float(theta_grid[int(np.argmax(ll))])


def mlae_run(chi0: np.ndarray, n: int, M: int, h: int, rng: np.random.Generator
             ) -> Tuple[float, int]:
    """Run one MLAE trial, return (theta_hat, Nq_total)."""
    m_list, hits = mlae_shots(chi0, n, M, h, rng)
    theta_hat = mlae_estimate_theta(m_list, hits, h)
    # Nq counted as in Eq. (19): h * sum_{m=0..M} (2m+1) A-queries
    # (paper uses m=1..M; m=0 adds cost h*1 which is negligible for the scaling)
    Nq = h * sum(2 * m + 1 for m in m_list)
    return theta_hat, Nq


# ---------------------------------------------------------------------------
# 5. Naïve VQAE with k=1 and a hardware-efficient PQC of depth d
#
#    ansatz: layers of R_y(theta_j) on every (n+1) qubit followed by a ladder
#    of CNOTs (0-1, 1-2, ..., n-1-n).  Initial state |0>_{n+1}.
# ---------------------------------------------------------------------------


def apply_ry(state: np.ndarray, n_total: int, qubit: int, angle: float) -> np.ndarray:
    """Apply R_y(angle) on the given qubit (0 = LSB) of an n_total-qubit statevector."""
    c = math.cos(angle / 2.0)
    s = math.sin(angle / 2.0)
    # reshape state to have the target qubit as a separate axis
    dim = 2 ** n_total
    st = state.reshape([2] * n_total)  # axes are qubit indices from MSB..LSB in numpy?
    # We stored amps with index = sum(bit_i * 2^i), so axis order after reshape
    # (with default C order and shape [2]*n_total) is [q_{n-1}, ..., q_1, q_0] (MSB first).
    axis = n_total - 1 - qubit
    st = np.moveaxis(st, axis, 0)
    a0 = st[0].copy()
    a1 = st[1].copy()
    st[0] = c * a0 - s * a1
    st[1] = s * a0 + c * a1
    st = np.moveaxis(st, 0, axis)
    return st.reshape(dim)


def apply_cnot(state: np.ndarray, n_total: int, ctrl: int, tgt: int) -> np.ndarray:
    dim = 2 ** n_total
    out = state.copy()
    # index encoding: bit i is (idx >> i) & 1
    for idx in range(dim):
        if (idx >> ctrl) & 1:
            partner = idx ^ (1 << tgt)
            if partner > idx:
                out[idx], out[partner] = state[partner], state[idx]
    return out


def build_ansatz_indices(n_total: int, d: int):
    """Return a list describing the ansatz: list of ('ry', qubit, param_idx) and
    ('cx', ctrl, tgt).  d layers of Ry on every qubit + CNOT ladder + one final Ry layer."""
    ops = []
    p = 0
    for _layer in range(d):
        for q in range(n_total):
            ops.append(("ry", q, p)); p += 1
        for q in range(n_total - 1):
            ops.append(("cx", q, q + 1))
    for q in range(n_total):
        ops.append(("ry", q, p)); p += 1
    n_params = p
    return ops, n_params


def apply_ansatz(params: np.ndarray, ops, n_total: int, init: np.ndarray = None) -> np.ndarray:
    if init is None:
        state = np.zeros(2 ** n_total, dtype=complex)
        state[0] = 1.0
    else:
        state = init.copy()
    for op in ops:
        if op[0] == "ry":
            state = apply_ry(state, n_total, op[1], params[op[2]])
        else:
            state = apply_cnot(state, n_total, op[1], op[2])
    return state


def variational_approximate(target: np.ndarray, n_total: int, d: int,
                             init_params: np.ndarray = None,
                             init_state: np.ndarray = None,
                             n_sweeps: int = 60, lr: float = 0.1
                             ) -> Tuple[np.ndarray, float]:
    """Fit ansatz(params) ≈ target via Adam-optimised objective F = Re<phi_var|target>.

    Returns (params, final_fidelity_squared).
    We use analytic gradients (parameter-shift rule with pi/2 shift for Ry).
    """
    ops, n_params = build_ansatz_indices(n_total, d)
    if init_params is None:
        rng = np.random.default_rng(0)
        params = 0.1 * rng.standard_normal(n_params)
    else:
        params = init_params.copy()

    # Adam
    m = np.zeros_like(params)
    v = np.zeros_like(params)
    b1, b2, eps = 0.9, 0.999, 1e-8

    def objective(p):
        state = apply_ansatz(p, ops, n_total, init=init_state)
        return float(np.real(np.vdot(state, target)))

    best_F = -np.inf
    best_params = params.copy()
    for t in range(1, n_sweeps + 1):
        # gradient via parameter shift
        grad = np.zeros_like(params)
        for j in range(n_params):
            p_plus = params.copy(); p_plus[j] += math.pi / 2
            p_minus = params.copy(); p_minus[j] -= math.pi / 2
            grad[j] = 0.5 * (objective(p_plus) - objective(p_minus))
        # Adam step (maximise F → gradient ascent)
        m = b1 * m + (1 - b1) * grad
        v = b2 * v + (1 - b2) * grad * grad
        m_hat = m / (1 - b1 ** t)
        v_hat = v / (1 - b2 ** t)
        params = params + lr * m_hat / (np.sqrt(v_hat) + eps)
        F_now = objective(params)
        if F_now > best_F:
            best_F = F_now; best_params = params.copy()

    final_state = apply_ansatz(best_params, ops, n_total, init=init_state)
    fidelity2 = float(np.abs(np.vdot(final_state, target)) ** 2)
    return best_params, fidelity2, final_state


def naive_vqae(chi0: np.ndarray, n: int, M: int, h: int, d: int,
               rng: np.random.Generator, n_sweeps: int = 40, verbose: bool = False
               ) -> Tuple[float, int, List[float]]:
    """Naïve VQAE with k=1: after each Q application, re-approximate the state
    with a fresh PQC starting from |0>_{n+1}.

    Returns (theta_hat, Nq_samp, infidelities).
    (We don't count variational query cost here — the paper treats N_var/1 as a free
    parameter; we report the sampling cost that MLAE would have paid.)"""
    n_total = n + 1
    ops, n_params = build_ansatz_indices(n_total, d)
    hits = []
    m_list = list(range(M + 1))
    infidelities = []

    # start from |chi_0>, sample it once
    state = chi0.copy()
    p1 = prob_ancilla_one(state, n)
    hits.append(int(rng.binomial(h, p1)))

    # initial variational fit of |chi_0> so later fits start from a warm state
    # (paper starts from |0>; we do that too, and re-initialize small each round)
    prev_params = None
    for m in range(1, M + 1):
        # advance the *variational approximation* by one Q
        target = apply_Q(state, chi0, n)
        # re-fit
        init_params = None if prev_params is None else prev_params
        prev_params, fid2, state = variational_approximate(
            target, n_total, d, init_params=init_params,
            init_state=None, n_sweeps=n_sweeps)
        infidelities.append(1.0 - fid2)
        # sample this variationally-approximated state
        p1 = prob_ancilla_one(state, n)
        hits.append(int(rng.binomial(h, p1)))
        if verbose:
            print(f"  m={m:2d}  1-F^2={1-fid2:.2e}  p1={p1:.4f}")

    theta_hat = mlae_estimate_theta(m_list, hits, h)
    Nq_samp = h * sum(2 * m + 1 for m in m_list)
    return theta_hat, Nq_samp, infidelities


# ---------------------------------------------------------------------------
# 6. Utility
# ---------------------------------------------------------------------------


def theta_from_a(a: float) -> float:
    return math.asin(math.sqrt(a))


def a_from_theta(theta: float) -> float:
    return math.sin(theta) ** 2


def delta_theta(theta_hat: float, theta_true: float) -> float:
    return abs(theta_hat - theta_true)


if __name__ == "__main__":
    # quick self-test
    n = 4
    p = cauchy_lorentz_probs(n, x0=0.5, gamma=0.1)
    N = 2 ** n
    x = np.arange(N) / N
    f = linear_f(x)
    chi0 = build_state_chi0(n, p, f)
    a = true_a(p, f)
    theta_star = theta_from_a(a)
    print(f"n={n}  a_true={a:.6f}  theta_true={theta_star:.6f}")
    # Grover rotation check: <chi_0|Q^m|chi_0> should oscillate as cos((2m+1)theta)
    rng = np.random.default_rng(0)
    state = chi0.copy()
    for m in range(5):
        p1 = prob_ancilla_one(state, n)
        pred = math.sin((2 * m + 1) * theta_star) ** 2
        print(f"  m={m}  measured p1={p1:.6f}  predicted sin^2((2m+1)θ)={pred:.6f}")
        state = apply_Q(state, chi0, n)
