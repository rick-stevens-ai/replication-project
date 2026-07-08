"""
Replication of Brown & Eastin (arXiv:1801.04042) "Randomized Benchmarking with
Restricted Gate Sets."

Core claims being tested:
  1. Full Clifford RB gives single-exponential decay f_l = c0 + c1 * lambda^l with
     lambda = 1 - p * 4^n / (4^n - 1). This is the baseline.
  2. Real Clifford subgroup (gen by H, CNOT, Pauli) is NOT a 2-design. Twirling
     yields 2 non-trivial blocks:
       * B1 (even # of Y, non-identity) - "real Pauli"
       * B2 (odd  # of Y)                - "imaginary Pauli"
     With an initial state that is an eigenstate of only real Pauli operators (e.g.
     |0...0>), only lambda1 is measured. Bounds:
       (2^n - 1)/(4^n + 2^n - 2) * (1-lambda1)  <=  p  <=  (1-lambda1)/2^n * 2^n ...
     Actually the paper's bound:
       (2^n-1)/(4^n+2^n-2) * (1-lambda1) <= p <= (1-lambda1)                (rewritten below)
     The paper's neat form (Eq. after "recalling that p = p1+p2"):
       (2^n - 1)/(4^n + 2^n - 2) * (1-lambda1) <= p <= (1-lambda1)  [approximately]
     What we actually verify:
       lambda1 = 1 - p1 * 4^n/(4^n + 2^n - 2) - p2 * 4^n/(4^n - 2^n)      (Eq. 25 in paper -- rewritten)
     For a symmetric depolarizing channel (all Pauli errors equally likely) this
     reduces to a well-defined lambda1 that we can compute and compare to a fit.
  3. CNOT+Pauli subgroup: 4 blocks (Z-only, X-only, mixed-XZ-only-even-Y, odd-Y).
     Two independent decays lambda1 (from |0..0>) and lambda2 (from |+..+>) with
     the paper's block eigenvalue formulas.

Approach:
  - Full Clifford: use stim.Tableau.random(n) (Bravyi/Maslov uniform Clifford).
  - Real-Clifford subgroup: random walk over generators {H_i, CNOT_ij, X_i, Z_i, Y_i}.
    Since (H, CNOT, Pauli) generate the real Clifford group [Aaronson-Gottesman
    normal form; the paper's Sec III.A]. The random walk mixes; we take a long
    burn-in per gate.
  - CNOT+Pauli: same idea, generators {CNOT_ij, X_i, Y_i, Z_i}.

Noise: after each sampled group element U, apply a per-qubit depolarizing channel
of strength p_dep (i.e. w.p. p_dep, apply a uniformly-random non-identity Pauli).
This produces a well-defined stochastic Pauli channel that we can analyze.

Entanglement infidelity vs depolarizing-strength conversion (n qubits, per-qubit
independent depolarizing with error prob p_dep per gate):
  After n independent single-qubit depolarizing errors of strength p_dep each,
  probability of identity = (1 - p_dep)^n, so
  p = 1 - (1 - p_dep)^n   (this is the total non-identity Pauli probability).
  Under uniform mixing this matches the paper's `p` (sum_{mu != I} x_{mu mu}).

Author: Ollie (arXiv 1801.04042 replication for QC-100 wave)
"""

from __future__ import annotations
import json
import math
import random
import time
from pathlib import Path
from dataclasses import dataclass, asdict

import numpy as np
import stim
from scipy.optimize import curve_fit

# ------------------ Utilities ------------------

def count_y_in_pauli_string(ps: stim.PauliString) -> int:
    """Count Y factors in a Pauli string."""
    return sum(1 for i in range(len(ps)) if ps[i] == 2)  # 0=I,1=X,2=Y,3=Z

def is_identity_pauli(ps: stim.PauliString) -> bool:
    return all(ps[i] == 0 for i in range(len(ps)))

def classify_block_real_clifford(ps: stim.PauliString) -> int:
    """Return 0 (identity), 1 (real, even #Y, non-I), 2 (imaginary, odd #Y)."""
    if is_identity_pauli(ps):
        return 0
    return 1 if count_y_in_pauli_string(ps) % 2 == 0 else 2

def classify_block_cnot_pauli(ps: stim.PauliString) -> int:
    """Return block index 0..4 per paper Sec III.B.
    0: identity
    1: non-identity Pauli with only Z and I
    2: non-identity Pauli with only X and I
    3: even #Y, not in B1 or B2 (mixed X/Z, no Y beyond even count of Y)
    4: odd #Y
    """
    if is_identity_pauli(ps):
        return 0
    n_y = count_y_in_pauli_string(ps)
    if n_y % 2 == 1:
        return 4
    # even number of Y (could be 0). Check if only Z/I or only X/I.
    if n_y == 0:
        has_x = any(ps[i] == 1 for i in range(len(ps)))
        has_z = any(ps[i] == 3 for i in range(len(ps)))
        if has_x and not has_z:
            return 2
        if has_z and not has_x:
            return 1
    return 3  # mixed even-Y (or has X and Z, no Y, on the same string)

# ------------------ Group sampling ------------------

def random_full_clifford_tableau(n: int, rng: random.Random) -> stim.Tableau:
    """Uniform random n-qubit Clifford (Bravyi-Maslov)."""
    seed = rng.getrandbits(63)
    return stim.Tableau.random(n)  # stim uses its own RNG; that's fine for our purposes

def apply_generator_real_clifford(circ: stim.Circuit, n: int, rng: random.Random) -> None:
    """Apply one random generator of the real Clifford group."""
    # Generators: H_i, CNOT_ij (i!=j), X_i, Y_i, Z_i.
    # We weight them roughly proportional to their count so the walk mixes well.
    kind_choices = ["H", "CNOT", "PAULI"]
    kind = rng.choice(kind_choices)
    if kind == "H":
        q = rng.randrange(n)
        circ.append("H", [q])
    elif kind == "CNOT" and n >= 2:
        i = rng.randrange(n); j = rng.randrange(n)
        while j == i:
            j = rng.randrange(n)
        circ.append("CX", [i, j])
    else:
        q = rng.randrange(n)
        p = rng.choice(["X", "Y", "Z"])
        circ.append(p, [q])

def apply_generator_cnot_pauli(circ: stim.Circuit, n: int, rng: random.Random) -> None:
    """Apply one random generator of the CNOT+Pauli group."""
    kind_choices = ["CNOT", "PAULI"] if n >= 2 else ["PAULI"]
    kind = rng.choice(kind_choices)
    if kind == "CNOT":
        i = rng.randrange(n); j = rng.randrange(n)
        while j == i:
            j = rng.randrange(n)
        circ.append("CX", [i, j])
    else:
        q = rng.randrange(n)
        p = rng.choice(["X", "Y", "Z"])
        circ.append(p, [q])

def random_group_element_tableau(n: int, group: str, walk_len: int,
                                  rng: random.Random) -> stim.Tableau:
    """Sample a Clifford tableau from the specified group.

    group = 'full' | 'real' | 'cnot_pauli'
    For 'real' / 'cnot_pauli' we perform a random walk of `walk_len` generators.
    """
    if group == "full":
        return stim.Tableau.random(n)
    apply_fn = {
        "real": apply_generator_real_clifford,
        "cnot_pauli": apply_generator_cnot_pauli,
    }[group]
    circ = stim.Circuit()
    for _ in range(walk_len):
        apply_fn(circ, n, rng)
    # convert to Tableau via simulator
    sim = stim.TableauSimulator()
    sim.do_circuit(circ)
    return sim.current_inverse_tableau().inverse()  # tableau of the applied circuit

# ------------------ RB experiment ------------------

@dataclass
class RBConfig:
    n_qubits: int
    group: str                     # 'full' | 'real' | 'cnot_pauli'
    lengths: tuple                 # gate sequence lengths m
    n_sequences_per_length: int
    p_dep: float                   # per-qubit depolarizing prob per group element
    initial_state: str = "0"       # '0' -> |0..0>, '+' -> |+..+>
    walk_len: int = 40             # for restricted-group sampling
    shots_per_sequence: int = 1    # 1 shot per sequence is enough because we average over many sequences

def prepare_initial_state_circuit(n: int, kind: str) -> stim.Circuit:
    c = stim.Circuit()
    if kind == "0":
        pass  # stim starts in |0..0>
    elif kind == "+":
        for q in range(n):
            c.append("H", [q])
    else:
        raise ValueError(kind)
    return c

def measurement_ops(n: int, kind: str) -> stim.Circuit:
    """Return a circuit that measures the survival probability of the initial state.
    For |0..0>: measure Z on each qubit; survival = all outcomes are 0.
    For |+..+>: apply H then measure Z; survival = all outcomes are 0.
    """
    c = stim.Circuit()
    if kind == "+":
        for q in range(n):
            c.append("H", [q])
    for q in range(n):
        c.append("M", [q])
    return c

def apply_depolarizing_noise(circ: stim.Circuit, n: int, p_dep: float) -> None:
    """Independent per-qubit depolarizing channel of strength p_dep."""
    if p_dep <= 0:
        return
    for q in range(n):
        circ.append("DEPOLARIZE1", [q], p_dep)

def build_rb_sequence(n: int, tableaus: list, cfg: RBConfig) -> stim.Circuit:
    """Build a sequence of group elements + inverse + noise + measurement."""
    circ = prepare_initial_state_circuit(n, cfg.initial_state)
    product = stim.Tableau(n)  # identity
    for T in tableaus:
        # append the circuit for T
        subc = T.to_circuit(method="elimination")
        circ += subc
        apply_depolarizing_noise(circ, n, cfg.p_dep)
        product = product.then(T)  # accumulate: (previous product) then T
    # inverse of full product to bring back to |initial>
    inv = product.inverse()
    circ += inv.to_circuit(method="elimination")
    apply_depolarizing_noise(circ, n, cfg.p_dep)
    circ += measurement_ops(n, cfg.initial_state)
    return circ

def run_rb(cfg: RBConfig, seed: int = 0, verbose: bool = True) -> dict:
    """Run RB experiment. Returns dict of length -> mean survival."""
    rng = random.Random(seed)
    results = {}
    t0 = time.time()
    for m in cfg.lengths:
        successes = 0
        total_shots = 0
        for s in range(cfg.n_sequences_per_length):
            tableaus = [
                random_group_element_tableau(cfg.n_qubits, cfg.group, cfg.walk_len, rng)
                for _ in range(m)
            ]
            circ = build_rb_sequence(cfg.n_qubits, tableaus, cfg)
            sampler = circ.compile_sampler()
            samples = sampler.sample(shots=cfg.shots_per_sequence)  # shape (shots, n_qubits)
            # survival = all zeros in measurement outcomes
            surv = np.all(samples == 0, axis=1).sum()
            successes += int(surv)
            total_shots += cfg.shots_per_sequence
        f_m = successes / total_shots
        results[m] = f_m
        if verbose:
            print(f"  m={m:3d}  f={f_m:.4f}  [seq={cfg.n_sequences_per_length}, elapsed={time.time()-t0:.1f}s]",
                  flush=True)
    return results

# ------------------ Fitting ------------------

def single_exp(m, a, b, lam):
    return a + b * lam**m

def double_exp(m, a, b1, lam1, b2, lam2):
    return a + b1 * lam1**m + b2 * lam2**m

def fit_single(lengths, fs):
    lengths = np.asarray(lengths, dtype=float)
    fs = np.asarray(fs, dtype=float)
    try:
        popt, _ = curve_fit(single_exp, lengths, fs, p0=[0.5, 0.5, 0.99],
                            bounds=([0, -1, 0.5], [1, 1, 1.0]),
                            maxfev=20000)
    except Exception as e:
        return None
    return dict(a=popt[0], b=popt[1], lam=popt[2])

def fit_double(lengths, fs):
    lengths = np.asarray(lengths, dtype=float)
    fs = np.asarray(fs, dtype=float)
    best = None
    for lam1_init, lam2_init in [(0.99, 0.9), (0.98, 0.85), (0.95, 0.7)]:
        try:
            popt, _ = curve_fit(double_exp, lengths, fs,
                                p0=[0.5, 0.25, lam1_init, 0.25, lam2_init],
                                bounds=([0, -1, 0.0, -1, 0.0], [1, 1, 1.0, 1, 1.0]),
                                maxfev=50000)
            resid = np.sum((double_exp(lengths, *popt) - fs) ** 2)
            if best is None or resid < best[1]:
                best = (popt, resid)
        except Exception:
            continue
    if best is None:
        return None
    popt = best[0]
    return dict(a=popt[0], b1=popt[1], lam1=popt[2], b2=popt[3], lam2=popt[4],
                resid=best[1])

# ------------------ Theory ------------------

def theory_lambda_full_clifford(n: int, p: float) -> float:
    """Full-Clifford single decay: lambda = 1 - p * 4^n/(4^n - 1)."""
    return 1 - p * 4**n / (4**n - 1)

def theory_lambda1_real_clifford_symmetric(n: int, p: float) -> float:
    """Real-Clifford: lambda1 for the symmetric depolarizing channel where every
    non-identity Pauli is equally likely.
    Under uniform Pauli mixing, p1/N1 = p2/N2 = (p/(4^n - 1))/(1) block-mass:
      Actually p1 = (N1(n)) * (p/(4^n - 1))    [mass in B1]
              p2 = (N2(n)) * (p/(4^n - 1))
    Then:
      lambda1 = 1 - p1 * 4^n/(4^n + 2^n - 2) - p2 * 4^n/(4^n - 2^n)
    """
    N1 = (4**n + 2**n) // 2 - 1
    N2 = (4**n - 2**n) // 2
    p_per = p / (4**n - 1)
    p1 = N1 * p_per
    p2 = N2 * p_per
    lam1 = 1 - p1 * (4**n) / (4**n + 2**n - 2) - p2 * (4**n) / (4**n - 2**n)
    return lam1, dict(N1=N1, N2=N2, p1=p1, p2=p2)

def theory_lambda_cnot_pauli_symmetric(n: int, p: float) -> dict:
    """CNOT+Pauli: four blocks, four decay rates for symmetric depolarizing."""
    N1 = 2**n - 1                        # Z-only
    N2 = 2**n - 1                        # X-only
    N3 = (4**n - 3 * 2**n) // 2 + 1      # even #Y, not B1/B2
    N4 = (4**n - 2**n) // 2              # odd #Y
    p_per = p / (4**n - 1)
    p1 = N1 * p_per; p2 = N2 * p_per; p3 = N3 * p_per; p4 = N4 * p_per
    lam1 = 1 - (p2 + p3 + p4) * (2**n) / (2**n - 1)
    lam2 = 1 - (p1 + p3 + p4) * (2**n) / (2**n - 1)
    lam3 = 1 - (p1 + p2 + p4) * (2**n) / (2**n - 1) - p3 * (4**n - 2**(n+2)) / (4**n - 3 * 2**n + 2)
    lam4 = 1 - (p1 + p2 + p3) * (2**n) / (2**n - 1) - p4 * (2**n - 2) / (2**n - 1)
    return dict(N1=N1, N2=N2, N3=N3, N4=N4,
                p1=p1, p2=p2, p3=p3, p4=p4,
                lam1=lam1, lam2=lam2, lam3=lam3, lam4=lam4)

def dep_prob_to_total_p(n: int, p_dep: float) -> float:
    """Total entanglement infidelity p = 1 - (1 - p_dep)^n for independent single-qubit
    depolarizing on each of n qubits. Under stim's DEPOLARIZE1(p), the channel is
    (1-p)*I + p/3 * (X rho X + Y rho Y + Z rho Z), so identity probability is 1-p.
    For n qubits independent: identity prob = (1 - p_dep)^n."""
    return 1 - (1 - p_dep) ** n


# ------------------ Main harness ------------------

def main():
    outdir = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/"
                  "QC-1801.04042-randomized-benchmarking-with-restricted-gate-sets/report/evidence")
    outdir.mkdir(parents=True, exist_ok=True)

    all_results = {}

    # ---- Experiment 1: baseline (full Clifford, n=2) ----
    print("=" * 70)
    print("Experiment 1: FULL CLIFFORD baseline, n=2, p_dep=0.01")
    print("=" * 70)
    n = 2; p_dep = 0.01
    cfg = RBConfig(n_qubits=n, group="full",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=60, p_dep=p_dep,
                   initial_state="0")
    res = run_rb(cfg, seed=1)
    lengths = sorted(res.keys()); fs = [res[m] for m in lengths]
    fit = fit_single(lengths, fs)
    p_total = dep_prob_to_total_p(n, p_dep)
    lam_theory = theory_lambda_full_clifford(n, p_total)
    print(f"\n  Fit: lambda = {fit['lam']:.4f}")
    print(f"  Theory: lambda = {lam_theory:.4f} (p_total = {p_total:.4f})")
    print(f"  |diff| = {abs(fit['lam'] - lam_theory):.4f}")
    all_results["exp1_full_clifford_n2"] = dict(
        config=asdict(cfg), lengths=lengths, fs=fs,
        fit=fit, theory_lambda=lam_theory, p_total=p_total,
    )

    # ---- Experiment 2: real Clifford, n=2 ----
    print()
    print("=" * 70)
    print("Experiment 2: REAL CLIFFORD subgroup, n=2, p_dep=0.01, init=|00>")
    print("=" * 70)
    n = 2; p_dep = 0.01
    cfg = RBConfig(n_qubits=n, group="real",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=80, p_dep=p_dep,
                   initial_state="0", walk_len=60)
    res = run_rb(cfg, seed=2)
    lengths = sorted(res.keys()); fs = [res[m] for m in lengths]
    p_total = dep_prob_to_total_p(n, p_dep)
    # symmetric depolarizing => lambda1 = lambda2 (single decay looks single-exp anyway,
    # because uniformly-random Pauli errors put equal weight on B1 and B2 blocks).
    lam1_theory, meta = theory_lambda1_real_clifford_symmetric(n, p_total)
    fit_s = fit_single(lengths, fs)
    fit_d = fit_double(lengths, fs)
    print(f"\n  Single-exp fit: lambda = {fit_s['lam']:.4f}")
    print(f"  Theory lambda1 (symmetric depolarizing): {lam1_theory:.4f}")
    print(f"  Block sizes: N1={meta['N1']}, N2={meta['N2']}, p1={meta['p1']:.4f}, p2={meta['p2']:.4f}")
    all_results["exp2_real_clifford_n2"] = dict(
        config=asdict(cfg), lengths=lengths, fs=fs,
        fit_single=fit_s, fit_double=fit_d,
        theory_lambda1=lam1_theory, meta=meta, p_total=p_total,
    )

    # ---- Experiment 3: CNOT+Pauli, n=2, |00> ----
    print()
    print("=" * 70)
    print("Experiment 3a: CNOT+PAULI subgroup, n=2, p_dep=0.01, init=|00>")
    print("=" * 70)
    n = 2; p_dep = 0.01
    cfg = RBConfig(n_qubits=n, group="cnot_pauli",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=80, p_dep=p_dep,
                   initial_state="0", walk_len=60)
    res = run_rb(cfg, seed=3)
    lengths = sorted(res.keys()); fs = [res[m] for m in lengths]
    p_total = dep_prob_to_total_p(n, p_dep)
    th = theory_lambda_cnot_pauli_symmetric(n, p_total)
    fit_s = fit_single(lengths, fs)
    print(f"\n  Single-exp fit: lambda = {fit_s['lam']:.4f}")
    print(f"  Theory: lam1(Z-only,|00>)={th['lam1']:.4f}  lam2(X-only,|++>)={th['lam2']:.4f}")
    print(f"          lam3={th['lam3']:.4f}  lam4={th['lam4']:.4f}")
    print(f"  Block sizes: N1={th['N1']}, N2={th['N2']}, N3={th['N3']}, N4={th['N4']}")
    all_results["exp3a_cnot_pauli_n2_00"] = dict(
        config=asdict(cfg), lengths=lengths, fs=fs,
        fit_single=fit_s, theory=th, p_total=p_total,
    )

    # ---- Experiment 3b: CNOT+Pauli, n=2, |++> ----
    print()
    print("=" * 70)
    print("Experiment 3b: CNOT+PAULI subgroup, n=2, p_dep=0.01, init=|++>")
    print("=" * 70)
    n = 2; p_dep = 0.01
    cfg = RBConfig(n_qubits=n, group="cnot_pauli",
                   lengths=(1, 2, 4, 8, 16, 32, 64, 128),
                   n_sequences_per_length=80, p_dep=p_dep,
                   initial_state="+", walk_len=60)
    res = run_rb(cfg, seed=4)
    lengths = sorted(res.keys()); fs = [res[m] for m in lengths]
    p_total = dep_prob_to_total_p(n, p_dep)
    th = theory_lambda_cnot_pauli_symmetric(n, p_total)
    fit_s = fit_single(lengths, fs)
    print(f"\n  Single-exp fit: lambda = {fit_s['lam']:.4f}")
    print(f"  Theory lam2 (X-only block, |++>): {th['lam2']:.4f}")
    all_results["exp3b_cnot_pauli_n2_plusplus"] = dict(
        config=asdict(cfg), lengths=lengths, fs=fs,
        fit_single=fit_s, theory=th, p_total=p_total,
    )

    # save
    outfile = outdir / "results.json"
    with open(outfile, "w") as fh:
        json.dump(all_results, fh, indent=2, default=str)
    print(f"\n\nSaved results to: {outfile}")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY (all p_dep=0.01, n=2, p_total = {:.4f})".format(
        dep_prob_to_total_p(2, 0.01)))
    print("=" * 70)
    print(f"{'Experiment':40s} {'lam_fit':>10s} {'lam_theory':>12s} {'|diff|':>10s}")
    print("-" * 74)
    e1 = all_results["exp1_full_clifford_n2"]
    print(f"{'1  full Clifford, |00>':40s} {e1['fit']['lam']:10.4f} {e1['theory_lambda']:12.4f} "
          f"{abs(e1['fit']['lam']-e1['theory_lambda']):10.4f}")
    e2 = all_results["exp2_real_clifford_n2"]
    print(f"{'2  real Clifford, |00>':40s} {e2['fit_single']['lam']:10.4f} {e2['theory_lambda1']:12.4f} "
          f"{abs(e2['fit_single']['lam']-e2['theory_lambda1']):10.4f}")
    e3a = all_results["exp3a_cnot_pauli_n2_00"]
    print(f"{'3a CNOT+Pauli, |00> -> lam1':40s} {e3a['fit_single']['lam']:10.4f} {e3a['theory']['lam1']:12.4f} "
          f"{abs(e3a['fit_single']['lam']-e3a['theory']['lam1']):10.4f}")
    e3b = all_results["exp3b_cnot_pauli_n2_plusplus"]
    print(f"{'3b CNOT+Pauli, |++> -> lam2':40s} {e3b['fit_single']['lam']:10.4f} {e3b['theory']['lam2']:12.4f} "
          f"{abs(e3b['fit_single']['lam']-e3b['theory']['lam2']):10.4f}")


if __name__ == "__main__":
    main()
