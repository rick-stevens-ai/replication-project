#!/usr/bin/env python3
"""Replication of arXiv:1909.05074 (Yamamoto, 2019)
   "On the natural gradient for variational quantum eigensolver"

Reproduces Example 2 (H2 molecule, Fig. 5):
   H = alpha*(Z x I + I x Z) + beta*(X x X), alpha=0.4, beta=0.2
   Hardware-efficient ansatz:
     |phi(theta)> = (Ry(2t3) x Ry(2t4)) . CNOT_{control=0} . (Ry(2t1) x Ry(2t2)) |00>
   Initial params (t1,t2,t3,t4) = (-0.2, -0.2, 0, 0)
   Learning rate eta = 0.05
   Compare vanilla GD vs Quantum Natural Gradient (Fubini-Study metric).

Central claim to check: natural gradient converges faster than ordinary gradient
to ground-state energy h4 = -sqrt(4 alpha^2 + beta^2) ~ -0.8246.
"""
import json
import os
import sys
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

OUTDIR = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1909.05074-natural-gradient-vqe/report/evidence"
)
os.makedirs(OUTDIR, exist_ok=True)

alpha, beta = 0.4, 0.2

# Exact ground-state energy from paper
E_exact = -np.sqrt(4 * alpha**2 + beta**2)  # -sqrt(0.68) ~ -0.8246
print(f"Exact ground-state energy: {E_exact:.6f} (paper says h4 ~ -0.82)")

# Chemical accuracy: 1.6 mHa is standard; paper doesn't require it, but
# we use "convergence gap < 1e-3" as a strict comparable threshold.
GAP_TOL = 1e-3

# Hamiltonian as PennyLane operator
# H = alpha*(Z_0 + Z_1) + beta*(X_0 X_1)
coeffs = [alpha, alpha, beta]
obs = [qml.PauliZ(0), qml.PauliZ(1), qml.PauliX(0) @ qml.PauliX(1)]
H = qml.Hamiltonian(coeffs, obs)

# Give the device an extra wire so metric_tensor's Hadamard test has room for an aux wire.
dev = qml.device("default.qubit", wires=3)


def ansatz(theta, wires=(0, 1)):
    """|phi(theta)> = (Ry(2 t3) x Ry(2 t4)) CNOT (Ry(2 t1) x Ry(2 t2)) |00>"""
    qml.RY(2 * theta[0], wires=wires[0])
    qml.RY(2 * theta[1], wires=wires[1])
    qml.CNOT(wires=wires)
    qml.RY(2 * theta[2], wires=wires[0])
    qml.RY(2 * theta[3], wires=wires[1])


@qml.qnode(dev, interface="autograd")
def energy(theta):
    ansatz(theta)
    return qml.expval(H)


def sanity_check_analytic_metric():
    """Paper eq. after Fig. 4:
        F = [[1, 0, sin(2 t2), 0],
             [0, 1, 0, cos(2 t1)],
             [sin(2 t2), 0, 1, 0],
             [0, cos(2 t1), 0, 1]]
    Compare to PennyLane's metric_tensor at a random point.
    """
    rng = np.random.default_rng(42)
    theta = pnp.array(rng.uniform(-1, 1, size=4), requires_grad=True)

    # Full metric using Hadamard test; needs an aux wire (device has wire 2 free).
    mt = qml.metric_tensor(energy, approx=None, aux_wire=2)(theta)
    mt = np.array(mt)

    t1, t2 = float(theta[0]), float(theta[1])
    F_analytic = np.array(
        [
            [1.0, 0.0, np.sin(2 * t2), 0.0],
            [0.0, 1.0, 0.0, np.cos(2 * t1)],
            [np.sin(2 * t2), 0.0, 1.0, 0.0],
            [0.0, np.cos(2 * t1), 0.0, 1.0],
        ]
    )
    # PennyLane returns the metric with a factor convention (1/4 of Fubini-Study when
    # rotation is Ry(theta_i) with the parameter entering as theta_i itself). Because
    # our ansatz uses Ry(2*theta_i), the factor from chain rule is 2^2 = 4 per param.
    # Test: pennylane_metric * 4 should equal paper's F (approximately).
    scale_test = 4 * mt
    diff = np.max(np.abs(scale_test - F_analytic))
    print(f"Metric sanity check (max |4*ml_mt - F_paper|): {diff:.4e}")
    print("PennyLane metric_tensor (scaled x4):")
    print(scale_test)
    print("Analytic F from paper:")
    print(F_analytic)
    return {"max_abs_diff_scaled": float(diff)}


def run_vanilla(theta0, eta=0.05, n_iter=200):
    """Vanilla gradient descent: theta_{k+1} = theta_k - eta * grad f."""
    theta = pnp.array(theta0, requires_grad=True)
    opt = qml.GradientDescentOptimizer(stepsize=eta)
    energies = []
    thetas = []
    for k in range(n_iter):
        e = float(energy(theta))
        energies.append(e)
        thetas.append(np.array(theta))
        theta = opt.step(energy, theta)
    energies.append(float(energy(theta)))
    thetas.append(np.array(theta))
    return np.array(energies), np.array(thetas)


def run_qng(theta0, eta=0.05, n_iter=200):
    """Quantum Natural Gradient: theta_{k+1} = theta_k - eta * F^{-1} grad f."""
    theta = pnp.array(theta0, requires_grad=True)
    opt = qml.QNGOptimizer(stepsize=eta, approx="block-diag", lam=1e-8)  # block-diag is fine for this ansatz
    energies = []
    thetas = []
    for k in range(n_iter):
        e = float(energy(theta))
        energies.append(e)
        thetas.append(np.array(theta))
        theta = opt.step(energy, theta)
    energies.append(float(energy(theta)))
    thetas.append(np.array(theta))
    return np.array(energies), np.array(thetas)


def iters_to_gap(energies, target, tol):
    """First iteration index where |E - target| < tol; None if never."""
    for i, e in enumerate(energies):
        if abs(e - target) < tol:
            return i
    return None


def main():
    result = {
        "paper": "arXiv:1909.05074",
        "system": "H2 (2-qubit reduced Hamiltonian, alpha=0.4 beta=0.2)",
        "E_exact": float(E_exact),
        "initial_params": [-0.2, -0.2, 0.0, 0.0],
        "eta": 0.05,
        "n_iterations": 200,
    }

    print("\n=== Sanity check: analytic Fubini-Study metric vs PennyLane ===")
    result["metric_check"] = sanity_check_analytic_metric()

    theta0 = np.array([-0.2, -0.2, 0.0, 0.0])
    n_iter = 200
    eta = 0.05

    print("\n=== Running vanilla GD ===")
    e_van, th_van = run_vanilla(theta0, eta=eta, n_iter=n_iter)
    print(f"  Vanilla: E[0]={e_van[0]:.6f}, E[final]={e_van[-1]:.6f}")

    print("\n=== Running QNG ===")
    e_qng, th_qng = run_qng(theta0, eta=eta, n_iter=n_iter)
    print(f"  QNG:     E[0]={e_qng[0]:.6f}, E[final]={e_qng[-1]:.6f}")

    # Iterations to reach various gap tolerances
    tolerances = [1e-1, 1e-2, 1e-3, 1e-4]
    conv = {}
    for tol in tolerances:
        it_v = iters_to_gap(e_van, E_exact, tol)
        it_q = iters_to_gap(e_qng, E_exact, tol)
        conv[f"tol_{tol:.0e}"] = {"vanilla": it_v, "qng": it_q}
        print(f"  tol={tol:.0e}: vanilla@{it_v}  qng@{it_q}")

    result["vanilla_final_energy"] = float(e_van[-1])
    result["qng_final_energy"] = float(e_qng[-1])
    result["vanilla_gap_final"] = float(abs(e_van[-1] - E_exact))
    result["qng_gap_final"] = float(abs(e_qng[-1] - E_exact))
    result["convergence_iterations"] = conv

    # Verdict components
    natgrad_faster = False
    it_v_1em3 = conv["tol_1e-03"]["vanilla"]
    it_q_1em3 = conv["tol_1e-03"]["qng"]
    if it_q_1em3 is not None:
        if it_v_1em3 is None or it_q_1em3 < it_v_1em3:
            natgrad_faster = True
    # Also compare at 1e-2 which is closer to what the paper's plot shows visually
    it_v_1em2 = conv["tol_1e-02"]["vanilla"]
    it_q_1em2 = conv["tol_1e-02"]["qng"]
    natgrad_faster_1em2 = (
        it_q_1em2 is not None
        and (it_v_1em2 is None or it_q_1em2 < it_v_1em2)
    )
    result["natgrad_faster_at_1e-3"] = bool(natgrad_faster)
    result["natgrad_faster_at_1e-2"] = bool(natgrad_faster_1em2)

    # Save curves
    np.savetxt(
        os.path.join(OUTDIR, "energy_curves.csv"),
        np.column_stack([np.arange(len(e_van)), e_van, e_qng]),
        header="iteration,E_vanilla,E_qng",
        delimiter=",",
        comments="",
    )
    np.savetxt(
        os.path.join(OUTDIR, "params_vanilla.csv"),
        th_van,
        header="theta1,theta2,theta3,theta4",
        delimiter=",",
        comments="",
    )
    np.savetxt(
        os.path.join(OUTDIR, "params_qng.csv"),
        th_qng,
        header="theta1,theta2,theta3,theta4",
        delimiter=",",
        comments="",
    )

    with open(os.path.join(OUTDIR, "results.json"), "w") as f:
        json.dump(result, f, indent=2)

    # Plot
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7, 4.5))
        it = np.arange(len(e_van))
        ax.plot(it, e_van, "b-", label="Vanilla gradient (eta=0.05)")
        ax.plot(it, e_qng, "r-", label="Quantum Natural Gradient (eta=0.05)")
        ax.axhline(E_exact, color="k", linestyle="--", linewidth=1, label=f"Exact ground state = {E_exact:.4f}")
        ax.set_xlabel("VQE iteration step")
        ax.set_ylabel("Energy f(theta) = <H>")
        ax.set_title("H2 (alpha=0.4, beta=0.2), init=(-0.2,-0.2,0,0)\nReplication of Yamamoto arXiv:1909.05074 Fig. 5 (bottom)")
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(OUTDIR, "energy_vs_iteration.png"), dpi=140)
        print(f"\nPlot saved to {OUTDIR}/energy_vs_iteration.png")
    except Exception as ex:
        print(f"Plot skipped: {ex}")

    print("\n=== SUMMARY ===")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
