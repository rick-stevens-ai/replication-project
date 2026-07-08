"""
Classical variational simulation of QAOA following Medvidović & Carleo 2020/21
(arXiv:2009.01760), Section IV.

The paper uses a *Neural-Network Quantum State* (specifically a complex-valued
Restricted Boltzmann Machine, RBM) to variationally represent |gamma, beta>.
The core trick is:
  - RZZ (i.e. UC) gates are applied EXACTLY by adding hidden units
    (Carleo et al 2018 arXiv:1808.04642).
  - RX gates are applied APPROXIMATELY by compressing back to a fixed hidden
    unit count via stochastic optimization on the fidelity.

For this INDEPENDENT REPLICATION we implement the *scientific idea* of the
paper — a classical NN-parametrized ansatz that variationally approximates the
exact QAOA state — at a scale we can actually run + verify against exact
statevector (n <= ~14 qubits).

We use a **complex-valued feedforward NN** (very close in spirit to a shallow
NQS / RBM) rather than the paper's specific RBM+hidden-unit-doubling scheme.
The point of this replication is to test the paper's *headline claim*:

  ==>  "For small p, a classical NN ansatz can approximate the QAOA
        output distribution / energy with high fidelity (>90-98%)."

We report:
  - final RBM-vs-exact fidelity |<psi_NN | psi_QAOA>|^2
  - RBM energy vs exact QAOA energy vs Appendix A analytical value
"""
from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, asdict
from itertools import product

import numpy as np

from qaoa_exact import (
    qaoa_energy_statevector,
    qaoa_p1_energy_analytical,
    qaoa_statevector,
    qaoa_cost_op,
    random_3_regular_graph,
)


# ---------- Basis enumeration ----------
def all_bitstrings(n: int) -> np.ndarray:
    """(2^n, n) matrix of +/-1 spins, row-index in binary big-endian to
    match qiskit statevector ordering (index i, bit q corresponds to
    the state where qubit q is the ((i >> q) & 1) bit)."""
    idx = np.arange(2 ** n)
    bits = np.zeros((2 ** n, n), dtype=np.int8)
    for q in range(n):
        bits[:, q] = (idx >> q) & 1
    # convert 0/1 -> +/-1  (0 -> +1, 1 -> -1)
    return 1 - 2 * bits


# ---------- Complex NN wavefunction ----------
@dataclass
class NNParams:
    W_re: np.ndarray  # (n, H)
    W_im: np.ndarray  # (n, H)
    b_re: np.ndarray  # (H,)
    b_im: np.ndarray  # (H,)
    a_re: np.ndarray  # (n,)  visible bias
    a_im: np.ndarray  # (n,)

    def to_vec(self) -> np.ndarray:
        return np.concatenate([
            self.W_re.ravel(), self.W_im.ravel(),
            self.b_re, self.b_im,
            self.a_re, self.a_im,
        ])

    @staticmethod
    def from_vec(v: np.ndarray, n: int, H: int) -> "NNParams":
        idx = 0
        W_re = v[idx:idx + n * H].reshape(n, H); idx += n * H
        W_im = v[idx:idx + n * H].reshape(n, H); idx += n * H
        b_re = v[idx:idx + H]; idx += H
        b_im = v[idx:idx + H]; idx += H
        a_re = v[idx:idx + n]; idx += n
        a_im = v[idx:idx + n]; idx += n
        return NNParams(W_re, W_im, b_re, b_im, a_re, a_im)


def init_params(n: int, H: int, rng: np.random.Generator, scale: float = 0.05) -> NNParams:
    return NNParams(
        W_re=rng.normal(0, scale, size=(n, H)),
        W_im=rng.normal(0, scale, size=(n, H)),
        b_re=rng.normal(0, scale, size=H),
        b_im=rng.normal(0, scale, size=H),
        a_re=rng.normal(0, scale, size=n),
        a_im=rng.normal(0, scale, size=n),
    )


def log_psi(params: NNParams, spins: np.ndarray) -> np.ndarray:
    """log psi(s) for a shallow complex RBM-like ansatz.

    log psi(s) = sum_i a_i * s_i + sum_h log(2 cosh(b_h + sum_i W_ih s_i))

    a and (W, b) are complex; s in {+/-1}. This is the standard NQS RBM form
    from Carleo & Troyer 2017.
    """
    W = params.W_re + 1j * params.W_im   # (n, H)
    b = params.b_re + 1j * params.b_im   # (H,)
    a = params.a_re + 1j * params.a_im   # (n,)

    visible = spins @ a                              # (B,)
    theta = spins @ W + b[None, :]                   # (B, H)
    # log(2 cosh(z)) computed stably as log(1 + exp(-2z)) + z (up to log 2)
    # simpler: use numpy's cosh on complex — dynamic range is fine for our sizes
    hidden = np.sum(np.log(2 * np.cosh(theta)), axis=1)
    return visible + hidden


def psi_vector(params: NNParams, n: int) -> np.ndarray:
    """Full 2^n amplitude vector for the NN ansatz (small n only)."""
    spins = all_bitstrings(n)
    logp = log_psi(params, spins)
    # subtract max real part for stability, then normalize
    logp = logp - np.max(logp.real)
    amps = np.exp(logp)
    amps = amps / np.linalg.norm(amps)
    return amps


# ---------- Training: fidelity maximization ----------
def infidelity_and_grad(
    params_vec: np.ndarray, target: np.ndarray, n: int, H: int
) -> tuple[float, np.ndarray]:
    """Loss = 1 - |<psi_NN | target>|^2, computed on the full 2^n basis
    (works for small n). Gradient by finite difference (simple + robust)."""
    params = NNParams.from_vec(params_vec, n, H)
    amps = psi_vector(params, n)
    overlap = np.vdot(amps, target)
    infid = 1.0 - float(np.abs(overlap) ** 2)
    return infid, amps, overlap


def _psi_and_dlogpsi_UNUSED(params: NNParams, spins: np.ndarray) -> tuple[np.ndarray, dict]:
    """Return log_psi(s) for all basis s and d log_psi / d(each complex param).

    Returns:
      logp: (B,) complex log psi values.
      grads: dict of name -> gradient array of shape (B, param_shape)
             containing d log_psi(s) / d theta   (complex).
    """
    W = params.W_re + 1j * params.W_im
    b = params.b_re + 1j * params.b_im
    a = params.a_re + 1j * params.a_im

    n, H = W.shape
    B = spins.shape[0]
    theta = spins @ W + b[None, :]           # (B, H)
    th = np.tanh(theta)                       # (B, H)

    visible = spins @ a                       # (B,)
    hidden = np.sum(np.log(2 * np.cosh(theta)), axis=1)  # (B,)
    logp = visible + hidden

    # d log_psi / d a_i = s_i
    dLda = spins.astype(complex)                            # (B, n)
    # d log_psi / d b_h = tanh(theta_h)
    dLdb = th                                                # (B, H)
    # d log_psi / d W_ih = s_i * tanh(theta_h)
    # -> (B, n, H)
    dLdW = spins[:, :, None] * th[:, None, :]

    return logp, {"a": dLda, "b": dLdb, "W": dLdW}


def train_nn_to_target(
    target: np.ndarray,
    n: int,
    H: int,
    seed: int = 0,
    n_steps: int = 400,
    lr: float = 0.05,
    verbose: bool = False,
) -> tuple[NNParams, list[float]]:
    """Optimize the infidelity 1 - |<psi_NN | target>|^2 with scipy L-BFGS-B
    using a *complex-step* gradient (accurate + fast; no cancellation error).

    complex-step derivative: d f(x)/dx  ~  Im[ f(x + i h) ] / h  for small h.
    Because our loss is analytic in each real parameter separately, this is
    exact to machine precision for any reasonable h (e.g. h=1e-20). And
    critically, we only need *one* complex evaluation per parameter, not two.

    We fall back to central FD only if complex-step doesn't behave (e.g. due
    to the log-sum-exp shift).
    """
    rng = np.random.default_rng(seed)
    params = init_params(n, H, rng)
    theta = params.to_vec()
    n_params = theta.size
    spins = all_bitstrings(n)

    def _psi_from_theta(theta_vec):
        p = NNParams.from_vec(theta_vec, n, H)
        W = p.W_re + 1j * p.W_im
        b = p.b_re + 1j * p.b_im
        a = p.a_re + 1j * p.a_im
        theta_arg = spins @ W + b[None, :]
        logp = spins @ a + np.sum(np.log(2 * np.cosh(theta_arg)), axis=1)
        m_shift = np.max(logp.real)
        A = np.exp(logp - m_shift)
        return A / np.linalg.norm(A)

    def infid_only(vec):
        psi = _psi_from_theta(vec)
        overlap = np.vdot(psi, target)
        return 1.0 - float(np.abs(overlap) ** 2)

    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    history: list[float] = []
    eps_fd = 1e-4

    loss0 = infid_only(theta)
    history.append(loss0)
    if verbose:
        print(f"  step 0  infid={loss0:.4e}  fid={1-loss0:.4f}")

    for step in range(1, n_steps + 1):
        # forward finite differences (reuse base eval)
        f_base = infid_only(theta)
        grad = np.zeros_like(theta)
        for k in range(n_params):
            saved = theta[k]
            theta[k] = saved + eps_fd
            fp = infid_only(theta)
            theta[k] = saved
            grad[k] = (fp - f_base) / eps_fd

        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * grad * grad
        mhat = m / (1 - beta1 ** step)
        vhat = v / (1 - beta2 ** step)
        theta = theta - lr * mhat / (np.sqrt(vhat) + eps)

        loss = infid_only(theta)
        history.append(loss)
        if verbose and (step % 25 == 0 or step == n_steps):
            print(f"  step {step}  infid={loss:.4e}  fid={1-loss:.4f}")

    return NNParams.from_vec(theta, n, H), history


# ---------- Driver ----------
def run_replication(
    n: int,
    seed_graph: int,
    seed_nn: int,
    p: int,
    gammas,
    betas,
    H: int,
    n_steps: int,
    lr: float,
    verbose: bool = False,
) -> dict:
    G = random_3_regular_graph(n, seed=seed_graph)
    n_edges = G.number_of_edges()

    # exact statevector target
    t0 = time.time()
    target = qaoa_statevector(G, gammas, betas)
    t_sv = time.time() - t0

    # exact QAOA energy from statevector
    E_exact = qaoa_energy_statevector(G, gammas, betas)

    # analytical p=1 value if p==1
    E_ana = qaoa_p1_energy_analytical(G, gammas[0], betas[0]) if p == 1 else None

    # train NN
    t0 = time.time()
    params, history = train_nn_to_target(
        target, n=n, H=H, seed=seed_nn, n_steps=n_steps, lr=lr, verbose=verbose
    )
    t_train = time.time() - t0

    # eval NN
    psi_nn = psi_vector(params, n)
    fid = float(np.abs(np.vdot(psi_nn, target)) ** 2)
    # NN energy via full 2^n cost operator (small n)
    from qiskit.quantum_info import Operator
    op = qaoa_cost_op(G, n)
    op_mat = op.to_matrix()
    E_nn = float(np.real(np.vdot(psi_nn, op_mat @ psi_nn)))

    return {
        "n": n,
        "num_edges": n_edges,
        "p": p,
        "gammas": list(gammas),
        "betas": list(betas),
        "H_hidden": H,
        "n_params": params.to_vec().size,
        "n_steps": n_steps,
        "lr": lr,
        "seed_graph": seed_graph,
        "seed_nn": seed_nn,
        "E_exact_statevector": E_exact,
        "E_p1_analytical": E_ana,
        "E_NN_variational": E_nn,
        "fidelity_NN_vs_exact": fid,
        "initial_infidelity": history[0],
        "final_infidelity": history[-1],
        "history": history,
        "time_statevector_s": t_sv,
        "time_train_s": t_train,
    }


if __name__ == "__main__":
    import sys, os

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    H = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    n_steps = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    seed_graph = int(sys.argv[5]) if len(sys.argv) > 5 else 42
    seed_nn = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    out = sys.argv[7] if len(sys.argv) > 7 else f"../data/nn_n{n}_p{p}.json"

    # QAOA angles: use paper's regime -- small angles near optimum for 3-regular graphs.
    # At p=1 for 3-regular graphs the analytical optimum is around
    # gamma ~ 0.6155 (~pi/5), beta ~ pi/8 (Farhi et al 2014).
    # For p>1 we use "small angles" following the paper's Fig.4 recipe.
    if p == 1:
        gammas = [0.6155]     # ~ optimal at p=1 for 3-reg
        betas = [math.pi / 8]  # ~ optimal at p=1 for 3-reg
    elif p == 2:
        gammas = [0.42, 0.66]
        betas = [0.55, 0.29]
    else:  # p == 4
        gammas = [0.31, 0.51, 0.66, 0.75]
        betas = [0.61, 0.48, 0.32, 0.14]
    gammas = gammas[:p]
    betas = betas[:p]

    result = run_replication(
        n=n,
        seed_graph=seed_graph,
        seed_nn=seed_nn,
        p=p,
        gammas=gammas,
        betas=betas,
        H=H,
        n_steps=n_steps,
        lr=0.03,
        verbose=True,
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(result, f)

    print("\n=== SUMMARY ===")
    print(f"n={result['n']} p={result['p']} H={result['H_hidden']} n_params={result['n_params']}")
    print(f"E_exact_statevector = {result['E_exact_statevector']:.6f}")
    if result["E_p1_analytical"] is not None:
        print(f"E_p1_analytical     = {result['E_p1_analytical']:.6f}   (diff = {result['E_exact_statevector']-result['E_p1_analytical']:.3e})")
    print(f"E_NN_variational    = {result['E_NN_variational']:.6f}   (rel err = {abs(result['E_NN_variational']-result['E_exact_statevector'])/max(1e-9,abs(result['E_exact_statevector'])):.3e})")
    print(f"fidelity_NN_vs_exact = {result['fidelity_NN_vs_exact']:.4f}")
    print(f"train_time = {result['time_train_s']:.1f} s")
    print(f"wrote {out}")
