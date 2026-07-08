"""
Replication core for arXiv:1804.09796
"One-dimensional many-body entangled open quantum systems with tensor network methods"
Jaschke, Montangero, Carr (2018)

Paper's central methodological claim: three tensor-network methods
(matrix product density operators MPDO, quantum trajectories QT, locally purified
tensor networks LPTN) all reproduce the exact Lindblad master equation dynamics
of small 1D open quantum systems, with error controlled by the tensor-network
bond dimension / number of trajectories.

What we test here (small-instance faithful reproduction):

  Transverse-field Ising chain of N=6,8 spins with per-site amplitude damping
  (sigma^- Lindblad operator, rate gamma).

  Method A (reference, exact): Lindblad master equation via qutip mesolve on the
    full 2^N x 2^N density matrix. Ground truth.

  Method B (tensor-network-compatible): Quantum Trajectories (QT) -- one of the
    three methods the paper reviews (Sec. III B). QT stores a pure state (not
    rho), so it is directly compatible with MPS representations; this is
    precisely why the paper covers it as a tensor-network method for open
    systems. Implemented via qutip mcsolve.

  Comparison: expectation values <sigma^z_k>(t) and <sigma^x_1 sigma^x_N>(t)
  along the whole trajectory and at long time.

  Reproduced claim: QT converges to the exact Lindblad solution as the number
  of trajectories increases (statistical Monte-Carlo error ~ 1/sqrt(Ntraj)),
  and for small chains matches exact ED at the trajectory-noise level.

  Sanity check: at N=6 we also compute the exact steady state via
  qutip.steadystate (direct Liouvillian inversion) and confirm the long-time
  Lindblad evolution converges to it, so mesolve is itself validated.
"""
import json
import time
from pathlib import Path

import numpy as np
import qutip as qt


def build_tfim_lindblad(N: int, J: float, g: float, gamma: float):
    sx, sz, sm = qt.sigmax(), qt.sigmaz(), qt.sigmam()
    I2 = qt.qeye(2)

    def op_at(op, k):
        return qt.tensor([op if i == k else I2 for i in range(N)])

    H = 0
    for k in range(N - 1):
        H += -J * op_at(sx, k) * op_at(sx, k + 1)
    for k in range(N):
        H += -g * op_at(sz, k)

    c_ops = [np.sqrt(gamma) * op_at(sm, k) for k in range(N)]

    e_ops = [op_at(sz, k) for k in range(N)]           # <sigma^z_k>
    e_ops.append(op_at(sx, 0) * op_at(sx, N - 1))      # <sigma^x_1 sigma^x_N>
    return H, c_ops, e_ops


def initial_state(N: int):
    """|00...0> = all spins up along z (product state, MPS bond dim 1)."""
    return qt.tensor([qt.basis(2, 0) for _ in range(N)])


def run_scan(N: int, ntraj_list, tmax: float, nt: int, do_steadystate: bool):
    J, g, gamma = 1.0, 1.0, 0.1
    H, c_ops, e_ops = build_tfim_lindblad(N, J, g, gamma)
    psi0 = initial_state(N)
    tlist = np.linspace(0.0, tmax, nt)

    # ---- Method A: exact Lindblad master equation (reference)
    t0 = time.time()
    me = qt.mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops,
                    options={"progress_bar": False, "nsteps": 20000})
    dt_me = time.time() - t0
    me_expect = np.array(me.expect)  # shape (n_e_ops, nt)
    print(f"[N={N}] mesolve: {dt_me:.2f}s", flush=True)

    ss_evals = None
    dt_ss = None
    if do_steadystate:
        # Sanity check: direct steady-state via Liouvillian inversion
        t0 = time.time()
        rho_ss = qt.steadystate(H, c_ops)
        dt_ss = time.time() - t0
        ss_evals = [float(qt.expect(op, rho_ss)) for op in e_ops]
        print(f"[N={N}] steadystate: {dt_ss:.2f}s", flush=True)

    # ---- Method B: quantum trajectories at multiple ntraj
    per_ntraj = {}
    for ntraj in ntraj_list:
        t0 = time.time()
        mc = qt.mcsolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops,
                        ntraj=ntraj, seeds=1234 + ntraj,
                        options={"progress_bar": False, "nsteps": 20000,
                                 "map": "serial"})
        dt_mc = time.time() - t0
        mc_expect = np.array(mc.expect)
        diff = mc_expect - me_expect
        entry = {
            "ntraj": ntraj,
            "wall_time_mcsolve_s": dt_mc,
            "max_abs_QT_minus_Lindblad": float(np.max(np.abs(diff))),
            "rms_QT_minus_Lindblad": float(np.sqrt(np.mean(diff ** 2))),
            "final_time_mcsolve": [float(v) for v in mc_expect[:, -1]],
        }
        per_ntraj[ntraj] = entry
        print(f"[N={N}] mcsolve ntraj={ntraj}: {dt_mc:.2f}s  "
              f"maxabs={entry['max_abs_QT_minus_Lindblad']:.4e}  "
              f"rms={entry['rms_QT_minus_Lindblad']:.4e}", flush=True)

    return {
        "N": N,
        "J": J, "g": g, "gamma": gamma,
        "tmax": tmax, "nt": nt,
        "e_op_labels": [f"<sz_{k}>" for k in range(N)] + [f"<sx_0 sx_{N-1}>"],
        "wall_time_mesolve_s": dt_me,
        "wall_time_steadystate_s": dt_ss,
        "steadystate_exact": ss_evals,
        "final_time_mesolve": [float(v) for v in me_expect[:, -1]],
        "tlist": tlist.tolist(),
        "me_expect": me_expect.tolist(),
        "per_ntraj": per_ntraj,
    }


def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    results = {}

    # N=6 (Hilbert dim 64): ntraj scan + exact steady state sanity check
    print("\n===== N=6 scan (with steadystate reference) =====", flush=True)
    results["N6"] = run_scan(N=6, ntraj_list=[50, 200, 800],
                             tmax=20.0, nt=41, do_steadystate=True)

    # N=8 (Hilbert dim 256): one ntraj value, skip steadystate (too slow at 65536 vec)
    print("\n===== N=8 (mesolve reference only) =====", flush=True)
    results["N8"] = run_scan(N=8, ntraj_list=[200],
                             tmax=20.0, nt=41, do_steadystate=False)

    out_path = outdir / "tn_vs_lindblad_results.json"
    with out_path.open("w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}", flush=True)

    # Convergence CSV for N=6
    lines = ["ntraj,max_abs_QT_minus_Lindblad,rms_QT_minus_Lindblad,expected_1_over_sqrt_ntraj_scale"]
    for nt in [50, 200, 800]:
        e = results["N6"]["per_ntraj"][nt]
        lines.append(f"{nt},{e['max_abs_QT_minus_Lindblad']:.6e},"
                     f"{e['rms_QT_minus_Lindblad']:.6e},"
                     f"{1.0 / np.sqrt(nt):.4f}")
    (outdir / "qt_convergence_N6.csv").write_text("\n".join(lines) + "\n")
    print(f"Wrote {outdir / 'qt_convergence_N6.csv'}", flush=True)

    # Final-time comparison CSV (N=6): mesolve vs mcsolve@800 vs steadystate
    r6 = results["N6"]
    lines = ["operator,mesolve_final,mcsolve_800_final,steadystate_exact"]
    for i, lbl in enumerate(r6["e_op_labels"]):
        lines.append(
            f"{lbl},{r6['final_time_mesolve'][i]:.6f},"
            f"{r6['per_ntraj'][800]['final_time_mcsolve'][i]:.6f},"
            f"{r6['steadystate_exact'][i]:.6f}"
        )
    (outdir / "final_values_N6.csv").write_text("\n".join(lines) + "\n")
    print(f"Wrote {outdir / 'final_values_N6.csv'}", flush=True)

    # And an at-a-glance summary
    summary = {
        "verdict_inputs": {
            "N6_800traj_maxabs_QT_vs_Lindblad": results["N6"]["per_ntraj"][800]["max_abs_QT_minus_Lindblad"],
            "N6_800traj_rms_QT_vs_Lindblad":    results["N6"]["per_ntraj"][800]["rms_QT_minus_Lindblad"],
            "N6_mesolve_vs_steadystate_maxabs": float(np.max(np.abs(
                np.array(results["N6"]["final_time_mesolve"]) -
                np.array(results["N6"]["steadystate_exact"])))),
            "N6_mcsolve800_vs_steadystate_maxabs": float(np.max(np.abs(
                np.array(results["N6"]["per_ntraj"][800]["final_time_mcsolve"]) -
                np.array(results["N6"]["steadystate_exact"])))),
            "N8_200traj_maxabs_QT_vs_Lindblad": results["N8"]["per_ntraj"][200]["max_abs_QT_minus_Lindblad"],
            "N8_200traj_rms_QT_vs_Lindblad":    results["N8"]["per_ntraj"][200]["rms_QT_minus_Lindblad"],
        }
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"Wrote {outdir / 'summary.json'}", flush=True)


if __name__ == "__main__":
    main()
