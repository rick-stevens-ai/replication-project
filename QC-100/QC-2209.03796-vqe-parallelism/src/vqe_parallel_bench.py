"""VQE parallel Pauli-term evaluation benchmark for H2.

Central testable claim from Mineh & Montanaro 2022 (arXiv:2209.03796):
distributing Pauli-term measurements across parallel workers reduces the
per-iteration wall-clock time roughly linearly in the number of workers,
until network/overhead dominates.

Here we implement the *classical simulation analog*: each Pauli term's
expectation value is computed on a statevector-prepared ansatz. We compare:

    (a) sequential loop over all Pauli terms (baseline)
    (b) multiprocessing.Pool with N workers (N = 2, 4, 8, ...)

Also sanity-check that the VQE minimum matches the true ground state
(both should reach ~ -1.137 Ha for H2/STO-3G at 0.735 Å) so we know the
simulation is real, not a stub.
"""
import argparse
import json
import multiprocessing as mp
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector
from qiskit.circuit.library import TwoLocal
from qiskit.quantum_info import Pauli, SparsePauliOp, Statevector


# ------------------------------------------------------------------
# Hamiltonian loader
# ------------------------------------------------------------------

def load_hamiltonian(path: str):
    with open(path) as f:
        data = json.load(f)
    terms = [(t["pauli"], complex(t["coeff_real"], t["coeff_imag"])) for t in data["terms"]]
    return data, terms


# ------------------------------------------------------------------
# Ansatz + per-term expectation
# ------------------------------------------------------------------

def make_ansatz(num_qubits: int, reps: int = 2) -> QuantumCircuit:
    """Standard hardware-efficient RY+CZ ansatz (used widely for H2 VQE)."""
    return TwoLocal(num_qubits, "ry", "cz", reps=reps, entanglement="linear")


def prepare_state(ansatz: QuantumCircuit, params: np.ndarray) -> np.ndarray:
    bound = ansatz.assign_parameters(params)
    sv = Statevector.from_instruction(bound)
    return sv.data


def pauli_expectation(state: np.ndarray, pauli_str: str, coeff: complex) -> complex:
    """<state|P|state> * coeff computed via Pauli.to_matrix() on the state."""
    P = Pauli(pauli_str).to_matrix()
    return coeff * np.vdot(state, P @ state)


# Global state for worker processes (fork() copies it)
_WORKER_STATE = {}


def _worker_init(state_bytes: bytes, dim: int, dtype_str: str):
    """Called once per worker; unpack state into numpy view."""
    arr = np.frombuffer(state_bytes, dtype=np.dtype(dtype_str)).reshape((dim,))
    _WORKER_STATE["state"] = arr


def _worker_eval(term):
    pauli_str, cr, ci = term
    coeff = complex(cr, ci)
    state = _WORKER_STATE["state"]
    P = Pauli(pauli_str).to_matrix()
    return complex(coeff * np.vdot(state, P @ state))


# Cache for thread version: Pauli matrices are built once and reused.
_THREAD_PAULI_CACHE = {}


def _thread_prep_cache(terms):
    global _THREAD_PAULI_CACHE
    _THREAD_PAULI_CACHE = {p: Pauli(p).to_matrix() for p, _ in terms}


def _thread_eval_chunk(state, terms_chunk, per_term_latency_s: float = 0.0):
    total = 0.0 + 0.0j
    for pauli_str, coeff in terms_chunk:
        P = _THREAD_PAULI_CACHE[pauli_str]
        total += coeff * np.vdot(state, P @ state)
        if per_term_latency_s > 0.0:
            time.sleep(per_term_latency_s)
    return complex(total)


# ------------------------------------------------------------------
# Sequential energy evaluation (baseline)
# ------------------------------------------------------------------

def energy_sequential(ansatz: QuantumCircuit, params: np.ndarray, terms,
                      per_term_latency_s: float = 0.0) -> float:
    state = prepare_state(ansatz, params)
    total = 0.0 + 0.0j
    for pauli_str, coeff in terms:
        # use cache if populated (fair to parallel variants)
        if pauli_str in _THREAD_PAULI_CACHE:
            P = _THREAD_PAULI_CACHE[pauli_str]
            total += coeff * np.vdot(state, P @ state)
        else:
            total += pauli_expectation(state, pauli_str, coeff)
        if per_term_latency_s > 0.0:
            time.sleep(per_term_latency_s)
    return float(np.real(total))


# ------------------------------------------------------------------
# Multiprocessing energy evaluation
# ------------------------------------------------------------------

def energy_parallel_mp(ansatz: QuantumCircuit, params: np.ndarray, terms,
                       n_workers: int) -> float:
    """Spawn a NEW pool each call (worst case for tiny H2 problem)."""
    state = prepare_state(ansatz, params)
    state_c = np.ascontiguousarray(state)
    state_bytes = state_c.tobytes()
    dim = state_c.shape[0]
    dtype_str = str(state_c.dtype)

    packed = [(p, float(np.real(c)), float(np.imag(c))) for p, c in terms]

    ctx = mp.get_context("fork")
    with ctx.Pool(processes=n_workers,
                  initializer=_worker_init,
                  initargs=(state_bytes, dim, dtype_str)) as pool:
        vals = pool.map(_worker_eval, packed)
    return float(np.real(sum(vals)))


# --- Persistent pool: how a real VQE optimization loop would use MP ---
# Workers pre-load the Pauli-matrix cache at initialization (fork copies
# them once). Each iteration we send only the state (small: 2^n complex),
# and shard the term-index list across workers -> minimal IPC per call.

_POOL_PAULI_CACHE = {}  # {pauli_str: (P_matrix, coeff_complex)}
_POOL_TERM_INDEX = []   # ordered list of pauli_str keys


def _pool_init_terms(terms_list):
    global _POOL_PAULI_CACHE, _POOL_TERM_INDEX
    _POOL_PAULI_CACHE = {}
    _POOL_TERM_INDEX = []
    for pauli_str, coeff in terms_list:
        _POOL_PAULI_CACHE[pauli_str] = (Pauli(pauli_str).to_matrix(), complex(coeff))
        _POOL_TERM_INDEX.append(pauli_str)


def _pool_eval_chunk(args):
    """Evaluate a chunk of Pauli indices on the given state."""
    state_bytes, dim, dtype_str, idx_start, idx_stop, per_term_latency_s = args
    state = np.frombuffer(state_bytes, dtype=np.dtype(dtype_str)).reshape((dim,))
    total = 0.0 + 0.0j
    for i in range(idx_start, idx_stop):
        pauli_str = _POOL_TERM_INDEX[i]
        P, coeff = _POOL_PAULI_CACHE[pauli_str]
        total += coeff * np.vdot(state, P @ state)
        if per_term_latency_s > 0.0:
            time.sleep(per_term_latency_s)
    return complex(total)


def energy_parallel_persistent_pool(pool, ansatz, params, terms, n_workers,
                                    per_term_latency_s: float = 0.0) -> float:
    state = prepare_state(ansatz, params)
    state_c = np.ascontiguousarray(state)
    state_bytes = state_c.tobytes()
    dim = state_c.shape[0]
    dtype_str = str(state_c.dtype)
    n_terms = len(terms)

    # partition term indices across workers
    chunk = (n_terms + n_workers - 1) // n_workers
    args = []
    for w in range(n_workers):
        lo = w * chunk
        hi = min(n_terms, lo + chunk)
        if lo < hi:
            args.append((state_bytes, dim, dtype_str, lo, hi, per_term_latency_s))

    vals = pool.map(_pool_eval_chunk, args)
    return float(np.real(sum(vals)))


def energy_parallel_threads(ex: ThreadPoolExecutor, ansatz, params, terms,
                            n_workers: int,
                            per_term_latency_s: float = 0.0) -> float:
    state = prepare_state(ansatz, params)
    n_terms = len(terms)
    chunk = (n_terms + n_workers - 1) // n_workers
    chunks = [terms[i:i+chunk] for i in range(0, n_terms, chunk)]
    futs = [ex.submit(_thread_eval_chunk, state, c, per_term_latency_s) for c in chunks]
    vals = [f.result() for f in futs]
    return float(np.real(sum(vals)))


# ------------------------------------------------------------------
# Simple VQE optimization (for sanity-check that we get real physics)
# ------------------------------------------------------------------

def vqe_minimize(ansatz, terms, seed: int = 0, maxiter: int = 200):
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(-np.pi, np.pi, ansatz.num_parameters)

    calls = {"n": 0}
    def f(x):
        calls["n"] += 1
        return energy_sequential(ansatz, x, terms)

    t0 = time.perf_counter()
    res = minimize(f, x0, method="COBYLA", options={"maxiter": maxiter, "rhobeg": 0.1})
    dt = time.perf_counter() - t0
    return {
        "final_energy_electronic": float(res.fun),
        "n_iterations": int(res.nfev),
        "wall_seconds": dt,
        "x": res.x.tolist(),
    }


# ------------------------------------------------------------------
# Timing benchmark
# ------------------------------------------------------------------

def timing_benchmark(ansatz, terms, workers_list, n_repeats: int = 20,
                     n_iters: int = 100, seed: int = 42,
                     skip_spawn_per_iter: bool = False,
                     skip_mp: bool = False,
                     per_term_latency_s: float = 0.0):
    """Simulate a VQE inner loop: evaluate the energy N_ITERS times per
    trial, average across N_REPEATS trials.
    
    Each 'iteration' uses a slightly different parameter vector to mimic
    the actual VQE optimization loop's changing parameters. We time the
    total wall-clock and report seconds-per-iteration.
    """
    rng = np.random.default_rng(seed)

    param_sets = [rng.uniform(-np.pi, np.pi, ansatz.num_parameters)
                  for _ in range(n_iters)]

    results = {}

    # Pre-build Pauli-matrix cache (fair to all backends)
    _thread_prep_cache(terms)

    # (1) sequential baseline
    seq_times = []
    seq_energies_ref = []
    for _ in range(n_repeats):
        t0 = time.perf_counter()
        energies = [energy_sequential(ansatz, p, terms, per_term_latency_s)
                    for p in param_sets]
        seq_times.append(time.perf_counter() - t0)
        seq_energies_ref = energies
    results["sequential"] = {
        "workers": 1,
        "mean_total_s": float(np.mean(seq_times)),
        "std_total_s": float(np.std(seq_times)),
        "mean_per_iter_s": float(np.mean(seq_times) / n_iters),
    }

    # Force fork on macOS for the H2 case (small enough not to deadlock),
    # but note deadlocks are possible with numpy+Accelerate. For larger
    # Hamiltonians use threads.
    # (2a) mp.Pool spawned-per-iteration at each worker count
    if not skip_spawn_per_iter:
        for nw in workers_list:
            mp_times = []
            mp_energies_last = None
            for _ in range(n_repeats):
                t0 = time.perf_counter()
                energies = [energy_parallel_mp(ansatz, p, terms, nw) for p in param_sets]
                mp_times.append(time.perf_counter() - t0)
                mp_energies_last = energies
            max_abs_diff = float(np.max(np.abs(np.array(seq_energies_ref) -
                                               np.array(mp_energies_last))))
            results[f"mp_spawn_per_iter_{nw}"] = {
                "backend": "mp.Pool (spawn-per-iter)",
                "workers": nw,
                "mean_total_s": float(np.mean(mp_times)),
                "std_total_s": float(np.std(mp_times)),
                "mean_per_iter_s": float(np.mean(mp_times) / n_iters),
                "speedup_vs_sequential": float(np.mean(seq_times) / np.mean(mp_times)),
                "max_abs_energy_diff_vs_seq": max_abs_diff,
            }

    if skip_mp:
        pass
    else:
     # (2b) mp.Pool PERSISTENT with pre-cached Pauli matrices
     # NOTE: use spawn context on macOS to avoid Accelerate/numpy fork
     # deadlocks that appear with larger Hamiltonians.
     for nw in workers_list:
        mp_times = []
        mp_energies_last = None
        ctx = mp.get_context("spawn")
        for _ in range(n_repeats):
            with ctx.Pool(processes=nw,
                          initializer=_pool_init_terms,
                          initargs=(terms,)) as pool:
                t0 = time.perf_counter()
                energies = [energy_parallel_persistent_pool(
                                pool, ansatz, p, terms, nw, per_term_latency_s)
                            for p in param_sets]
                mp_times.append(time.perf_counter() - t0)
                mp_energies_last = energies
        max_abs_diff = float(np.max(np.abs(np.array(seq_energies_ref) -
                                           np.array(mp_energies_last))))
        results[f"mp_persistent_{nw}"] = {
         "backend": "mp.Pool (persistent+cache, spawn)",
         "workers": nw,
         "mean_total_s": float(np.mean(mp_times)),
         "std_total_s": float(np.std(mp_times)),
         "mean_per_iter_s": float(np.mean(mp_times) / n_iters),
         "speedup_vs_sequential": float(np.mean(seq_times) / np.mean(mp_times)),
         "max_abs_energy_diff_vs_seq": max_abs_diff,
        }

    # (3) ThreadPoolExecutor (persistent) with cached Pauli matrices
    for nw in workers_list:
        t_times = []
        t_energies_last = None
        for _ in range(n_repeats):
            with ThreadPoolExecutor(max_workers=nw) as ex:
                t0 = time.perf_counter()
                energies = [energy_parallel_threads(
                                ex, ansatz, p, terms, nw, per_term_latency_s)
                            for p in param_sets]
                t_times.append(time.perf_counter() - t0)
                t_energies_last = energies
        max_abs_diff = float(np.max(np.abs(np.array(seq_energies_ref) -
                                           np.array(t_energies_last))))
        results[f"threads_{nw}"] = {
            "backend": "ThreadPool (persistent+cache)",
            "workers": nw,
            "mean_total_s": float(np.mean(t_times)),
            "std_total_s": float(np.std(t_times)),
            "mean_per_iter_s": float(np.mean(t_times) / n_iters),
            "speedup_vs_sequential": float(np.mean(seq_times) / np.mean(t_times)),
            "max_abs_energy_diff_vs_seq": max_abs_diff,
        }

    return results


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ham", required=True, help="path to Hamiltonian JSON")
    ap.add_argument("--out", required=True, help="path to output JSON")
    ap.add_argument("--workers", default="2,3,4,6,8",
                    help="comma-separated list of worker counts")
    ap.add_argument("--n_iters", type=int, default=100,
                    help="number of 'VQE iterations' (parameter sets) per trial")
    ap.add_argument("--n_repeats", type=int, default=20,
                    help="number of timing trials to average")
    ap.add_argument("--ansatz_reps", type=int, default=2)
    ap.add_argument("--skip_vqe", action="store_true")
    ap.add_argument("--skip_spawn_per_iter", action="store_true")
    ap.add_argument("--skip_mp", action="store_true",
                    help="skip multiprocessing (use threads only)")
    ap.add_argument("--per_term_latency_ms", type=float, default=0.0,
                    help="Extra artificial latency per Pauli term in milliseconds "
                         "(simulates real hardware shot+network overhead per term)")
    args = ap.parse_args()

    data, terms = load_hamiltonian(args.ham)
    print(f"[info] H2 Hamiltonian: {data['n_qubits']} qubits, {data['n_pauli_terms']} Pauli terms")
    print(f"[info] Reference electronic ground energy: {data['electronic_ground_energy_hartree']:.6f} Ha")
    print(f"[info] Reference total ground energy: {data['total_ground_energy_hartree']:.6f} Ha")

    ansatz = make_ansatz(data["n_qubits"], reps=args.ansatz_reps)
    print(f"[info] Ansatz: TwoLocal RY+CZ reps={args.ansatz_reps} -> {ansatz.num_parameters} parameters")

    workers_list = [int(w) for w in args.workers.split(",")]

    # ---- Physics sanity check: run VQE and see if we reach the ground state ----
    vqe_out = None
    if not args.skip_vqe:
        print(f"[info] Running COBYLA VQE (physics sanity check)...")
        # take a few seeds and keep best
        best = None
        for seed in range(5):
            vqe_res = vqe_minimize(ansatz, terms, seed=seed, maxiter=400)
            if best is None or vqe_res["final_energy_electronic"] < best["final_energy_electronic"]:
                best = vqe_res
                best["seed"] = seed
        vqe_out = best
        E_electronic_vqe = vqe_out["final_energy_electronic"]
        E_total_vqe = E_electronic_vqe + data["nuclear_repulsion_energy"]
        E_total_ref = data["total_ground_energy_hartree"]
        vqe_out["final_energy_total_hartree"] = float(E_total_vqe)
        vqe_out["reference_total_hartree"] = float(E_total_ref)
        vqe_out["abs_error_hartree"] = float(abs(E_total_vqe - E_total_ref))
        print(f"[info] Best VQE total energy: {E_total_vqe:.6f} Ha  "
              f"(ref {E_total_ref:.6f}, |err|={abs(E_total_vqe - E_total_ref):.6f})")

    # ---- Timing benchmark ----
    print(f"[info] Running timing benchmark: workers={workers_list}, "
          f"n_iters={args.n_iters}, n_repeats={args.n_repeats}")
    t0 = time.perf_counter()
    per_term_latency_s = args.per_term_latency_ms / 1000.0
    bench = timing_benchmark(ansatz, terms, workers_list,
                             n_repeats=args.n_repeats, n_iters=args.n_iters,
                             skip_spawn_per_iter=args.skip_spawn_per_iter,
                             skip_mp=args.skip_mp,
                             per_term_latency_s=per_term_latency_s)
    total_bench_time = time.perf_counter() - t0

    out = {
        "hamiltonian": {
            "path": args.ham,
            "n_qubits": data["n_qubits"],
            "n_pauli_terms": data["n_pauli_terms"],
            "reference_electronic_ground_hartree": data["electronic_ground_energy_hartree"],
            "reference_total_ground_hartree": data["total_ground_energy_hartree"],
        },
        "ansatz": {
            "type": "TwoLocal(ry, cz, linear)",
            "reps": args.ansatz_reps,
            "num_parameters": int(ansatz.num_parameters),
        },
        "cpu": {
            "cpu_count": os.cpu_count(),
        },
        "benchmark_params": {
            "worker_counts": workers_list,
            "n_iters_per_trial": args.n_iters,
            "n_repeats": args.n_repeats,
            "per_term_latency_ms": args.per_term_latency_ms,
        },
        "vqe_sanity_check": vqe_out,
        "timings": bench,
        "total_benchmark_wall_seconds": total_bench_time,
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[info] wrote {args.out}")

    # Print a small summary
    seq_t = bench["sequential"]["mean_per_iter_s"]
    print(f"\n{'backend':<25s}  {'workers':>7s}  {'ms/iter':>10s}  {'speedup':>8s}")
    print(f"{'sequential':<25s}  {'1':>7s}  {seq_t*1000:>10.3f}  {'1.00x':>8s}")
    for k, v in bench.items():
        if k == "sequential":
            continue
        print(f"{v['backend']:<25s}  {v['workers']:>7d}  "
              f"{v['mean_per_iter_s']*1000:>10.3f}  "
              f"{v['speedup_vs_sequential']:>7.2f}x")


if __name__ == "__main__":
    main()
