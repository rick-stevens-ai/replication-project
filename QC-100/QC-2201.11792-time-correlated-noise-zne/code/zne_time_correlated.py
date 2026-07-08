"""
Replication of headline claim from arXiv:2201.11792
"Analyzing the impact of time-correlated noise on zero-noise extrapolation"
Schultz et al. (2022).

HEADLINE CLAIM (paper): Standard ZNE assumes uncorrelated (white) noise.
Under time-correlated (colored) noise, ZNE with local noise scaling produces
substantially larger residual bias than under white noise. Global folding is
more robust, but the general point is:

    ZNE reduces bias under uncorrelated noise;
    ZNE leaves substantial residual bias / added variance under time-correlated
    (non-Markovian) noise.

REPRODUCTION STRATEGY (small, real, CPU):
* Build a fixed 4-qubit hardware-efficient ansatz circuit (2 layers).
* Observable: O = |0000><0000| (probability of ground state) -- same family
  as the paper's RB observables.
* Two noise models, matched to have roughly equal single-shot fidelity impact:
    (i)  UNCORRELATED depolarizing noise (Qiskit Aer NoiseModel with per-gate
         depolarizing errors -- resamples independently every gate).
    (ii) TIME-CORRELATED coherent noise: a slowly-drifting global Z
         over-rotation whose angle for each single-qubit or two-qubit gate is
         sampled as a random walk in "time" (gate index). Within a single
         shot, the rotation drifts smoothly -> highly correlated across
         gates. Across shots it re-seeds. This is a coherent, non-Markovian
         (correlated-in-time) noise consistent with the SchWARMA-style
         dephasing model in the paper (colored dephasing).
* For each noise model, apply Mitiq ZNE (Richardson extrapolation with
  scale factors [1, 3, 5], local unitary folding at gate level).
* Report:
    - Noiseless expectation value (exact, no noise).
    - Noisy raw expectation value (scale factor 1).
    - ZNE-mitigated expectation value.
    - Bias (mitigated - noiseless).

If the paper's headline is right we should see:
    |bias_zne_uncorrelated|  <  |bias_raw_uncorrelated|   (ZNE helps)
    |bias_zne_correlated|   >~ |bias_raw_correlated|      (ZNE fails)
       OR at minimum
    |bias_zne_correlated|   > |bias_zne_uncorrelated|     (ZNE worse under
                                                           correlation).
"""

import json
import os
import time
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from mitiq import zne
from mitiq.zne.scaling import fold_gates_at_random
from mitiq.zne.inference import RichardsonFactory


RNG_SEED = 20260704
NUM_SHOTS = 8000            # per (noise-model, scale) evaluation
NUM_TRIALS_CORRELATED = 100 # correlated-noise trajectories per shot batch
SCALE_FACTORS = [1.0, 3.0, 5.0]
DEPOL_P = 0.02              # per-gate depolarizing (uncorrelated) probability
CORR_SIGMA_STEP = 0.05      # rad per gate random-walk step for coherent noise


def build_ansatz(num_qubits: int = 4, num_layers: int = 2, seed: int = 7) -> QuantumCircuit:
    """Small hardware-efficient ansatz with fixed parameters."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(num_qubits)
    for _ in range(num_layers):
        for q in range(num_qubits):
            qc.ry(float(rng.uniform(0, 2 * np.pi)), q)
            qc.rz(float(rng.uniform(0, 2 * np.pi)), q)
        for q in range(num_qubits - 1):
            qc.cx(q, q + 1)
    qc.measure_all()
    return qc


def observable_prob_all_zero(counts: dict, num_qubits: int) -> float:
    """Return P(|0...0>) from Qiskit counts dict."""
    target = "0" * num_qubits
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return counts.get(target, 0) / total


# ------------- Executor: noiseless -------------

def executor_noiseless(circuit: QuantumCircuit) -> float:
    sim = AerSimulator()
    tqc = transpile(circuit, sim, optimization_level=0)
    result = sim.run(tqc, shots=NUM_SHOTS).result()
    counts = result.get_counts()
    return observable_prob_all_zero(counts, circuit.num_qubits - _n_ancilla(circuit))


def _n_ancilla(circuit: QuantumCircuit) -> int:
    # measure_all adds a classical register but doesn't add qubits.
    return 0


# ------------- Executor: uncorrelated depolarizing -------------

def make_depolarizing_noise_model(p: float) -> NoiseModel:
    nm = NoiseModel()
    err1 = depolarizing_error(p, 1)
    err2 = depolarizing_error(min(1.0, 2 * p), 2)
    for g in ["ry", "rz", "u", "u1", "u2", "u3", "sx", "x", "h"]:
        nm.add_all_qubit_quantum_error(err1, g)
    nm.add_all_qubit_quantum_error(err2, ["cx", "cz"])
    return nm


def executor_uncorrelated(circuit: QuantumCircuit) -> float:
    nm = make_depolarizing_noise_model(DEPOL_P)
    sim = AerSimulator(noise_model=nm)
    tqc = transpile(circuit, sim, optimization_level=0)
    result = sim.run(tqc, shots=NUM_SHOTS, seed_simulator=int(np.random.randint(1 << 30))).result()
    counts = result.get_counts()
    return observable_prob_all_zero(counts, tqc.num_qubits)


# ------------- Executor: time-correlated coherent noise -------------
#
# Model: for each shot, we simulate the circuit with a coherent Z over-rotation
# after every gate, where the rotation angle theta_t follows a random walk in
# "time index" t across gates within that shot:
#     theta_0 ~ N(0, sigma_init)
#     theta_{t+1} = theta_t + eta_t,  eta_t ~ N(0, sigma_step^2)
# The SAME slowly drifting theta_t is applied on ALL qubits (a common-mode
# dephasing drift). This produces strong temporal correlation of the noise
# within each shot (non-Markovian), while resampling across shots. This is a
# faithful qualitative stand-in for the SchWARMA colored dephasing used in the
# paper: the noise spectrum is low-frequency dominated (a random walk has
# 1/f^2 power spectrum).
#
# Because Aer executes shot batches internally without an easy per-gate
# stochastic hook, we implement this by building N_TRIALS distinct
# noise-instantiated circuits (each with baked-in per-gate Rz(theta_t) after
# every op), running each with a small shots count, and averaging.

def _inject_coherent_drift(circuit: QuantumCircuit, rng: np.random.Generator) -> QuantumCircuit:
    """Return a copy of circuit with a small Rz(theta_t) inserted after every
    gate on every qubit that gate touches, where theta_t follows a random walk
    across gate indices in this single circuit instance (= one 'shot')."""
    new = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    theta = float(rng.normal(0.0, CORR_SIGMA_STEP))
    for instr in circuit.data:
        op = instr.operation
        qargs = instr.qubits
        cargs = instr.clbits
        new.append(op, qargs, cargs)
        if op.name in ("measure", "barrier", "reset"):
            continue
        # random walk step
        theta += float(rng.normal(0.0, CORR_SIGMA_STEP))
        for q in qargs:
            new.rz(theta, q)
    return new


def executor_time_correlated(circuit: QuantumCircuit) -> float:
    """Estimate <O> under time-correlated coherent noise. We build many
    noise-realized copies of the circuit, run each with a small shot budget,
    and pool results."""
    sim = AerSimulator()
    trials = NUM_TRIALS_CORRELATED
    shots_per_trial = max(1, NUM_SHOTS // trials)
    rng = np.random.default_rng()  # fresh per call so ZNE-folded circuits get independent noise draws
    all_counts = {}
    circuits = [_inject_coherent_drift(circuit, rng) for _ in range(trials)]
    tqcs = transpile(circuits, sim, optimization_level=0)
    result = sim.run(tqcs, shots=shots_per_trial).result()
    for i in range(trials):
        c = result.get_counts(i)
        for k, v in c.items():
            all_counts[k] = all_counts.get(k, 0) + v
    return observable_prob_all_zero(all_counts, circuit.num_qubits)


# ------------- Run the experiment -------------

def evaluate(circuit, executor, name, log):
    t0 = time.time()
    # 1) raw noisy expectation value (scale = 1)
    raw = executor(circuit)
    log(f"[{name}] raw noisy <O> at scale=1: {raw:.6f}   ({time.time()-t0:.1f}s)")

    # 2) ZNE
    t1 = time.time()
    factory = RichardsonFactory(scale_factors=SCALE_FACTORS)
    zne_value = zne.execute_with_zne(
        circuit=circuit,
        executor=executor,
        factory=factory,
        scale_noise=fold_gates_at_random,
    )
    scale_expvals = [(x, y) for x, y in zip(factory.get_scale_factors(), factory.get_expectation_values())]
    log(f"[{name}] scale/expval pairs from ZNE: {scale_expvals}")
    log(f"[{name}] Richardson-extrapolated <O>: {zne_value:.6f}   ({time.time()-t1:.1f}s)")
    return raw, zne_value, scale_expvals


def main():
    np.random.seed(RNG_SEED)
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "report", "evidence")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "run.log")
    logf = open(log_path, "w")

    def log(msg):
        print(msg)
        logf.write(msg + "\n")
        logf.flush()

    log(f"# Replication run: arXiv 2201.11792")
    log(f"# num_shots={NUM_SHOTS}, scale_factors={SCALE_FACTORS}, depol_p={DEPOL_P}, corr_sigma_step={CORR_SIGMA_STEP}")
    log(f"# num_trials_correlated={NUM_TRIALS_CORRELATED}")

    circ = build_ansatz(num_qubits=4, num_layers=2, seed=7)
    log(f"# Ansatz: {circ.num_qubits} qubits, depth={circ.depth()}, size={circ.size()}")

    # noiseless
    t0 = time.time()
    noiseless = executor_noiseless(circ)
    log(f"[noiseless] <O> = {noiseless:.6f}   ({time.time()-t0:.1f}s)")

    # (i) uncorrelated depolarizing
    raw_u, zne_u, pairs_u = evaluate(circ, executor_uncorrelated, "uncorrelated", log)

    # (ii) time-correlated coherent
    raw_c, zne_c, pairs_c = evaluate(circ, executor_time_correlated, "time_correlated", log)

    bias_raw_u = raw_u - noiseless
    bias_zne_u = zne_u - noiseless
    bias_raw_c = raw_c - noiseless
    bias_zne_c = zne_c - noiseless

    zne_helps_uncorrelated = abs(bias_zne_u) < abs(bias_raw_u)
    zne_worse_under_correlation = abs(bias_zne_c) > abs(bias_zne_u)

    summary = {
        "arxiv_id": "2201.11792",
        "num_shots": NUM_SHOTS,
        "num_trials_correlated": NUM_TRIALS_CORRELATED,
        "scale_factors": SCALE_FACTORS,
        "depol_p": DEPOL_P,
        "corr_sigma_step": CORR_SIGMA_STEP,
        "circuit": {
            "num_qubits": circ.num_qubits,
            "depth": circ.depth(),
            "size": circ.size(),
        },
        "noiseless": noiseless,
        "uncorrelated": {
            "raw": raw_u,
            "zne": zne_u,
            "bias_raw": bias_raw_u,
            "bias_zne": bias_zne_u,
            "scale_expvals": pairs_u,
        },
        "time_correlated": {
            "raw": raw_c,
            "zne": zne_c,
            "bias_raw": bias_raw_c,
            "bias_zne": bias_zne_c,
            "scale_expvals": pairs_c,
        },
        "checks": {
            "zne_helps_uncorrelated": bool(zne_helps_uncorrelated),
            "zne_worse_under_correlation_vs_uncorrelated": bool(zne_worse_under_correlation),
        },
    }
    out_json = os.path.join(out_dir, "results.json")
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2, default=float)
    log(f"# wrote {out_json}")
    log(f"# noiseless           = {noiseless:.4f}")
    log(f"# raw (uncorr)        = {raw_u:.4f}   bias = {bias_raw_u:+.4f}")
    log(f"# ZNE (uncorr)        = {zne_u:.4f}   bias = {bias_zne_u:+.4f}   ZNE-helps={zne_helps_uncorrelated}")
    log(f"# raw (corr)          = {raw_c:.4f}   bias = {bias_raw_c:+.4f}")
    log(f"# ZNE (corr)          = {zne_c:.4f}   bias = {bias_zne_c:+.4f}")
    log(f"# ZNE-worse-under-correlation = {zne_worse_under_correlation}")
    logf.close()


if __name__ == "__main__":
    main()
