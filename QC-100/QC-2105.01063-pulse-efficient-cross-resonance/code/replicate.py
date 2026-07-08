"""
Independent replication of arXiv:2105.01063
"Pulse-efficient circuit transpilation for quantum applications on
cross-resonance-based hardware" (Earnest, Tornow, Egger; 2021).

Reproducible core, laptop-CPU only, real Qiskit simulations:

  C1  RZZ(theta) gate: paper (Fig 1/2) claims that decomposing RZZ(theta)
      into 2x scaled RZX(theta/2) with echo is more coherence-efficient
      than the standard double-CNOT decomposition.
      Testable: (i) 2Q-op count and total |theta| of RZX gates (proxy
      for cross-resonance pulse time); (ii) simulated process fidelity
      under a depolarising noise model where each RZX(phi) has error
      proportional to |phi|/(pi/2) — this is the "coherence-limited"
      model the paper itself uses in Fig 1(d) / App C.

  C2  Small QAOA (MAX-CUT) on a non-hardware-native graph.  Paper
      (Sec V, Fig 6) applies the template-substitution pulse-efficient
      pass to depth-1 QAOA on an 11-node graph on ibmq_mumbai and
      reports 42-52% CR-time reduction and 38% reduction in the max
      absolute deviation of the average cut value.
      We use n=4 (K4 complete graph on a linear coupling 0-1-2-3, which
      forces SWAPs).  We measure the same three things (op count,
      total pulse-theta, max |dev| vs noiseless).
"""

import json, os, sys, time, math
from pathlib import Path
import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.circuit.library import RZXGate, RZZGate, HGate
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import TemplateOptimization
from qiskit.transpiler.passes.calibration.rzx_templates import (
    rzx_templates, RZXTemplateMap
)
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def circuit_stats(qc: QuantumCircuit):
    """Return (n_2q_ops, total_abs_theta_of_2q_ops, list_of_(name,theta))."""
    n2q, total_theta = 0, 0.0
    details = []
    for inst, qargs, _ in qc.data:
        if len(qargs) == 2:
            n2q += 1
            if inst.name == "cx":
                th = math.pi / 2  # CX = one RZX(pi/2) pulse
            elif inst.name in ("rzx", "rzz"):
                th = abs(float(inst.params[0]))
            else:
                th = math.pi / 2
            total_theta += th
            details.append((inst.name, th))
    return n2q, total_theta, details


def build_noise_model(qc, per_pi_2_error):
    """Same coherent-noise model for any circuit.  Each 2Q gate gets
    depolarising error proportional to its cross-resonance time
    (|theta|/(pi/2)); each 1Q gate gets a small fixed error."""
    noise = NoiseModel()
    seen_2q = set()
    for inst, qargs, _ in qc.data:
        if len(qargs) != 2:
            continue
        if inst.name == "cx":
            frac = 1.0
        elif inst.name in ("rzx", "rzz"):
            frac = abs(float(inst.params[0])) / (math.pi / 2)
        else:
            frac = 1.0
        p = min(per_pi_2_error * frac, 0.75)
        qidx = tuple(qc.find_bit(q).index for q in qargs)
        # For rzx/rzz where angle varies, we need one error per angle;
        # here we simply add a per-qubit-pair error keyed by gate name.
        # Since qiskit-aer chooses the LAST-added error for a given
        # (name, qubits), we instead attach errors via `add_quantum_error`
        # per gate-instance by giving each rzx a unique dummy name isn't
        # possible — so we approximate by using an *average* rate over
        # the circuit, computed below.
        seen_2q.add((inst.name, qidx, round(p, 6)))

    # Group by (name, qubits) and use max p (worst-case) — this is
    # conservative but keeps the model tractable.  Alternative: use
    # instruction-level `save_expectation_value` — but average p suffices
    # since our claim is "relative" fidelity comparison.
    per_pair = {}
    for name, qidx, p in seen_2q:
        key = (name, qidx)
        per_pair[key] = max(per_pair.get(key, 0.0), p)
    for (name, qidx), p in per_pair.items():
        noise.add_quantum_error(
            depolarizing_error(p, 2), name, list(qidx), warnings=False)

    # 1Q errors (small)
    for inst_name in ("rz", "sx", "x", "rx", "ry", "u", "u3", "h", "p", "id"):
        noise.add_all_qubit_quantum_error(
            depolarizing_error(per_pi_2_error / 20, 1), inst_name,
            warnings=False,
        )
    return noise


def build_noise_model_avg(qc, per_pi_2_error):
    """Cleaner variant: assign each 2Q gate the AVERAGE error rate over
    all its instances (Aer registers one error per (name, qubits) so we
    average per instance-count-weighted).  Used for C1 where every 2Q
    op is on the same pair (0,1)."""
    noise = NoiseModel()
    accum = {}
    for inst, qargs, _ in qc.data:
        if len(qargs) != 2:
            continue
        if inst.name == "cx":
            frac = 1.0
        elif inst.name in ("rzx", "rzz"):
            frac = abs(float(inst.params[0])) / (math.pi / 2)
        else:
            frac = 1.0
        p = min(per_pi_2_error * frac, 0.75)
        qidx = tuple(qc.find_bit(q).index for q in qargs)
        key = (inst.name, qidx)
        accum.setdefault(key, []).append(p)
    for key, ps in accum.items():
        p_avg = float(np.mean(ps))
        noise.add_quantum_error(
            depolarizing_error(p_avg, 2), key[0], list(key[1]),
            warnings=False)

    for inst_name in ("rz", "sx", "x", "rx", "ry", "u", "u3", "h", "p", "id"):
        noise.add_all_qubit_quantum_error(
            depolarizing_error(per_pi_2_error / 20, 1), inst_name,
            warnings=False,
        )
    return noise


def state_fidelity_from_dm(qc, target_op, noise):
    """Fidelity of |psi_noisy> = channel|0..0> against |psi_ideal> =
    target|0..0>."""
    sim = AerSimulator(method="density_matrix", noise_model=noise)
    qc_meas = qc.copy()
    qc_meas.save_density_matrix()
    result = sim.run(qc_meas, shots=1).result()
    dm = result.data(0)["density_matrix"].data

    ideal_state = Statevector.from_label("0" * qc.num_qubits).evolve(target_op)
    ideal_dm = np.outer(ideal_state.data, ideal_state.data.conj())
    return float(np.real(np.trace(dm @ ideal_dm)))


# ------------------------------------------------------------------
# C1: RZZ(theta) — hand-built decompositions (no slow template pass)
# ------------------------------------------------------------------
def rzz_double_cnot(theta):
    """Standard: CX · Rz(theta) on target · CX  ==  RZZ(theta)."""
    qc = QuantumCircuit(2, name=f"rzz_cnot({theta:.3f})")
    qc.cx(0, 1)
    qc.rz(theta, 1)
    qc.cx(0, 1)
    return qc


def rzz_pulse_efficient(theta):
    """Pulse-efficient RZZ built from an ECHOED pair of scaled RZX(theta/2),
    matching Fig 1(a) and the ZZ2 template in Qiskit's rzx_templates.

      RZZ(theta) = (I x H) · RZX_echoed(theta) · (I x H)
                 = (I x H) · [X(qc)·RZX(-theta/2)·X(qc)·RZX(theta/2)] · (I x H)

    This is exactly what `RZXCalibrationBuilder` would attach a scaled CR
    pulse to on real hardware.  The 2-qubit cross-resonance time is
    |theta|/2 + |theta|/2 = |theta| (vs pi for the double-CNOT which
    always executes 2 RZX(pi/2) pulses).
    """
    qc = QuantumCircuit(2, name=f"rzz_pe({theta:.3f})")
    qc.h(1)
    # Echoed RZX(theta): X on control, RZX(-theta/2), X on control, RZX(theta/2)
    qc.rzx(theta / 2, 0, 1)
    qc.x(0)
    qc.rzx(-theta / 2, 0, 1)
    qc.x(0)
    qc.h(1)
    return qc


def experiment_C1(per_pi_2_error=0.02):
    thetas = np.linspace(0.1, np.pi, 12)
    rows = []
    for th in thetas:
        qc_c = rzz_double_cnot(float(th))
        qc_p = rzz_pulse_efficient(float(th))
        target = Operator(RZZGate(float(th)))

        # sanity: pulse-efficient should still equal RZZ(theta)
        u_p = Operator(qc_p)
        u_t = target
        # allow global phase difference
        overlap = abs((u_p.data.conj().T @ u_t.data).trace() / 4)
        assert overlap > 0.999, f"pulse-eff circuit != RZZ (overlap {overlap})"

        n2c, tc, _ = circuit_stats(qc_c)
        n2p, tp, _ = circuit_stats(qc_p)

        noise_c = build_noise_model_avg(qc_c, per_pi_2_error)
        noise_p = build_noise_model_avg(qc_p, per_pi_2_error)

        f_c = state_fidelity_from_dm(qc_c, target, noise_c)
        f_p = state_fidelity_from_dm(qc_p, target, noise_p)
        e_c, e_p = 1 - f_c, 1 - f_p
        rel = 100 * (e_c - e_p) / e_c if e_c > 0 else 0.0

        rows.append(dict(
            theta=float(th),
            cnot_2q_ops=n2c, cnot_total_pulse_theta=tc,
            pe_2q_ops=n2p, pe_total_pulse_theta=tp,
            pulse_theta_ratio_pe_over_cnot=tp / tc if tc > 0 else 0.0,
            fid_cnot=f_c, fid_pulse_efficient=f_p,
            rel_error_reduction_pct=rel,
        ))
        print(f"th={th:.3f}  cnot n2q={n2c} T={tc:.3f}  pe n2q={n2p} T={tp:.3f}  "
              f"fid {f_c:.4f} vs {f_p:.4f}  err_red={rel:+.1f}%")
    return rows


# ------------------------------------------------------------------
# C2: QAOA MAX-CUT n=4 (K4 on linear coupling 0-1-2-3)
# ------------------------------------------------------------------
def build_qaoa_k4(gamma, beta):
    n = 4
    edges = [(i, j, 1.0) for i in range(n) for j in range(i+1, n)]
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for i, j, w in edges:
        qc.rzz(2 * gamma * w, i, j)
    for q in range(n):
        qc.rx(2 * beta, q)
    return qc, edges


def cut_expectation(counts, edges, total_shots):
    total = 0.0
    for bs, c in counts.items():
        b = bs[::-1]  # qiskit endian
        v = 0.0
        for i, j, w in edges:
            zi = 1 - 2 * int(b[i]); zj = 1 - 2 * int(b[j])
            v += w * (1 - zi * zj) / 2
        total += v * c
    return total / total_shots


def transpile_cnot(qc):
    cm = [[0,1],[1,0],[1,2],[2,1],[2,3],[3,2]]
    return transpile(qc, basis_gates=["cx", "u3"],
                     coupling_map=cm, optimization_level=3, seed_transpiler=42)


def transpile_pulse_eff(qc):
    """Hand-built pulse-efficient variant: transpile to CX basis first,
    then walk the DAG and replace every  CX-Rz(θ)-CX  block (which is
    exactly RZZ(θ)) with the echoed 2×RZX(θ/2) decomposition.  This
    reproduces what the paper's template-substitution pass does for the
    RZZ template — but bypasses the O(|C|^7) TemplateOptimization pass
    which was unusably slow for even 15 thetas on our machine."""
    qc_cx = transpile_cnot(qc)
    return replace_cxrzcx_with_pulse_eff(qc_cx)


def _rz_angle(inst):
    """If instruction is effectively Rz(theta), return theta."""
    if inst.name == "rz":
        try: return float(inst.params[0])
        except Exception: return None
    if inst.name == "u3" and len(inst.params) == 3:
        try: th, ph, lam = [float(p) for p in inst.params]
        except Exception: return None
        if abs(th) < 1e-9 and abs(ph) < 1e-9:
            return lam
    if inst.name == "u1":
        try: return float(inst.params[0])
        except Exception: return None
    return None


def replace_cxrzcx_with_pulse_eff(qc):
    """Swap every CX-Rz(theta)-CX-on-same-pair triple with the
    pulse-efficient echoed 2xRZX(theta/2) equivalent (paper's zz2)."""
    ops = list(qc.data)
    out = QuantumCircuit(*qc.qregs, *qc.cregs)
    i = 0
    n_repl = 0
    while i < len(ops):
        if i + 2 < len(ops):
            a, qa, _ = ops[i]
            b, qb, _ = ops[i+1]
            c, qc_, _ = ops[i+2]
            theta = _rz_angle(b)
            if (a.name == "cx" and c.name == "cx"
                and tuple(qa) == tuple(qc_)
                and len(qb) == 1 and qb[0] == qa[1]
                and theta is not None):
                q0, q1 = qa[0], qa[1]
                out.h(q1)
                out.rzx(theta / 2, q0, q1)
                out.x(q0)
                out.rzx(-theta / 2, q0, q1)
                out.x(q0)
                out.h(q1)
                i += 3
                n_repl += 1
                continue
        out.append(ops[i][0], ops[i][1], ops[i][2])
        i += 1
    out._n_pulse_eff_replacements = n_repl
    return out


def experiment_C2(per_pi_2_error=0.02, shots=8192):
    n_grid = 5
    gammas = np.linspace(0.1, 1.0, n_grid)
    betas  = np.linspace(0.1, 0.8, n_grid)

    rows = []
    max_dev_c, max_dev_p = 0.0, 0.0

    for g in gammas:
        for b in betas:
            qc, edges = build_qaoa_k4(float(g), float(b))

            # ideal
            sim_i = AerSimulator()
            qc_m = qc.copy(); qc_m.measure_all()
            cnts_i = sim_i.run(transpile(qc_m, sim_i, seed_transpiler=1),
                               shots=shots).result().get_counts()
            ideal_cut = cut_expectation(cnts_i, edges, shots)

            # CNOT-basis noisy
            qc_c = transpile_cnot(qc)
            n2c, tc, _ = circuit_stats(qc_c)
            noise_c = build_noise_model(qc_c, per_pi_2_error)
            sim_c = AerSimulator(noise_model=noise_c)
            qc_cm = qc_c.copy(); qc_cm.measure_all()
            cnts_c = sim_c.run(qc_cm, shots=shots).result().get_counts()
            cnot_cut = cut_expectation(cnts_c, edges, shots)

            # Pulse-efficient noisy
            qc_p = transpile_pulse_eff(qc)
            n2p, tp, _ = circuit_stats(qc_p)
            noise_p = build_noise_model(qc_p, per_pi_2_error)
            sim_p = AerSimulator(noise_model=noise_p)
            qc_pm = qc_p.copy(); qc_pm.measure_all()
            cnts_p = sim_p.run(qc_pm, shots=shots).result().get_counts()
            pe_cut = cut_expectation(cnts_p, edges, shots)

            dev_c = abs(cnot_cut - ideal_cut)
            dev_p = abs(pe_cut - ideal_cut)
            max_dev_c = max(max_dev_c, dev_c)
            max_dev_p = max(max_dev_p, dev_p)

            rows.append(dict(
                gamma=float(g), beta=float(b),
                ideal_cut=ideal_cut,
                cnot_cut=cnot_cut, pe_cut=pe_cut,
                dev_cnot=dev_c, dev_pe=dev_p,
                cnot_2q_ops=n2c, cnot_pulse_theta=tc,
                pe_2q_ops=n2p, pe_pulse_theta=tp,
                pulse_theta_reduction_pct=(100*(tc-tp)/tc) if tc>0 else 0,
            ))
            print(f"g={g:.2f} b={b:.2f}  ideal={ideal_cut:.3f}  "
                  f"cnot={cnot_cut:.3f}(Δ{dev_c:+.3f})  "
                  f"pe={pe_cut:.3f}(Δ{dev_p:+.3f})  "
                  f"n2q {n2c}->{n2p}  T {tc:.2f}->{tp:.2f} ({100*(tc-tp)/tc:.1f}%)")

    return rows, dict(
        max_dev_cnot=max_dev_c,
        max_dev_pe=max_dev_p,
        max_dev_reduction_pct=100*(max_dev_c - max_dev_p)/max_dev_c if max_dev_c>0 else 0,
    )


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":
    t0 = time.time()

    print("=" * 68)
    print("C1: RZZ(theta) — pulse-efficient (echoed 2xRZX(theta/2)) vs double-CNOT")
    print("=" * 68)
    c1 = experiment_C1(per_pi_2_error=0.02)
    with open(OUT / "C1_rzz_sweep.json", "w") as f:
        json.dump(c1, f, indent=2)

    med_ratio = float(np.median([r["pulse_theta_ratio_pe_over_cnot"] for r in c1]))
    med_err  = float(np.median([r["rel_error_reduction_pct"] for r in c1]))
    max_err  = float(max(r["rel_error_reduction_pct"] for r in c1)) 

    print(f"\nC1 SUMMARY")
    print(f"  median pulse-theta ratio (PE/CNOT): {med_ratio:.3f}")
    print(f"  median rel error reduction: {med_err:+.1f}%")
    print(f"  max rel error reduction:    {max_err:+.1f}%")
    print(f"  paper (Fig 1/4): 'up to 50%' error reduction  <-- claim")

    print("\n" + "=" * 68)
    print("C2: Depth-1 QAOA MAX-CUT on K4 (n=4)")
    print("=" * 68)
    c2_rows, c2_sum = experiment_C2(per_pi_2_error=0.02, shots=8192)
    with open(OUT / "C2_qaoa_sweep.json", "w") as f:
        json.dump({"rows": c2_rows, "summary": c2_sum}, f, indent=2)

    med_pt_red = float(np.median([r["pulse_theta_reduction_pct"] for r in c2_rows]))
    print(f"\nC2 SUMMARY")
    print(f"  max |dev CNOT vs ideal| = {c2_sum['max_dev_cnot']:.3f}")
    print(f"  max |dev PE   vs ideal| = {c2_sum['max_dev_pe']:.3f}")
    print(f"  max-dev reduction       = {c2_sum['max_dev_reduction_pct']:+.1f}%")
    print(f"  median pulse-theta reduction across grid = {med_pt_red:+.1f}%")
    print(f"  paper (Sec V, Fig 6/7): 42-52% schedule-time reduction, "
          f"38% max-avg-cut error reduction  <-- claim")

    summary = dict(
        c1_median_pulse_ratio=med_ratio,
        c1_median_error_reduction_pct=med_err,
        c1_max_error_reduction_pct=max_err,
        c2_max_dev_cnot=c2_sum["max_dev_cnot"],
        c2_max_dev_pe=c2_sum["max_dev_pe"],
        c2_max_dev_reduction_pct=c2_sum["max_dev_reduction_pct"],
        c2_median_pulse_theta_reduction_pct=med_pt_red,
        wall_seconds=time.time() - t0,
        qiskit_version=__import__("qiskit").__version__,
        aer_version=__import__("qiskit_aer").__version__,
        numpy_version=np.__version__,
        per_pi_2_error=0.02,
    )
    with open(OUT / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nDONE in {time.time()-t0:.1f}s")
    print(json.dumps(summary, indent=2))
