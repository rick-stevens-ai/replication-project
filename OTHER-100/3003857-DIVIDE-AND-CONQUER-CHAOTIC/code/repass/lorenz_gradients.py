"""Lorenz-63 — Section 4.1 of the paper (re-pass, fast diagnostic version).

Reproduces the *qualitative* claims of Fig. 2:
  (a) Vanilla autodiff of J = mean(|z|) over a long Lorenz rollout produces a
      gradient w.r.t. the control parameter rho whose magnitude grows
      exponentially with horizon length T (the classic chaotic-system exploding
      gradient -- Eckmann-Ruelle / horseshoe-mapping argument).
  (b) Multi-step penalty splitting (K segments) keeps the per-segment
      gradients bounded, so the *total* gradient stays O(1) even at large T.

We don't need a multi-hour optimization to demonstrate this.  We demonstrate it
analytically by:
  - integrating Lorenz-63 with rho as a leaf parameter
  - computing |dJ/drho| for horizons T = {2, 5, 10, 20, 40} time units
    (i.e. ~0.1, 0.25, 0.5, 1, 2 Lyapunov times for L63)
  - comparing the vanilla single-shot gradient to the MP gradient
    (sum of K independent segment gradients, each of length T/K)

This is computationally tractable (<= 1 minute on CPU) and produces a
controlled, reproducible diagnostic for the paper's central claim.

Outputs (under results/repass/lorenz/):
  - gradient_vs_horizon.json
  - lorenz_gradient_explosion.png
  - summary.json

Reference: arXiv:2407.00568v5, Section 4.1.1 (Exploding Gradients).
"""
import json, os, time
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

torch.set_default_dtype(torch.float64)
torch.manual_seed(0)
np.random.seed(0)

SIGMA = 10.0
BETA = 8.0 / 3.0
DT = 0.01  # matches paper (T=20, 2000 steps)


def rk4_step(state, rho, dt):
    sigma, beta = SIGMA, BETA
    def f(s):
        x, y, z = s[..., 0], s[..., 1], s[..., 2]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return torch.stack([dx, dy, dz], dim=-1)
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def vanilla_gradient(rho_value, T, x0, dt=DT):
    """Vanilla single-shot: integrate from x0 for time T, compute |dJ/drho|.
    Returns the L1 magnitude of the gradient and the objective value."""
    rho = torch.tensor(rho_value, requires_grad=True)
    n_steps = int(round(T / dt))
    state = x0
    z_accum = state[2].abs()
    for _ in range(n_steps):
        state = rk4_step(state, rho, dt)
        z_accum = z_accum + state[2].abs()
    J = z_accum / (n_steps + 1)
    rho.grad = None
    J.backward()
    return float(abs(rho.grad.detach())), float(J.detach())


def mp_gradient(rho_value, T, K, x0, dt=DT):
    """MP version: split horizon T into K equal windows. Each window k starts
    from a *detached* state (we don't differentiate across windows). The
    gradient is the sum of within-window gradients."""
    rho = torch.tensor(rho_value, requires_grad=True)
    n_steps = int(round(T / dt))
    per_seg = n_steps // K
    total_grad = 0.0
    total_J = 0.0
    n_terms = 0

    # First propagate (no_grad) to build the q_k stitching points
    state = x0.clone()
    starts = [state.clone()]
    with torch.no_grad():
        for k in range(K):
            for _ in range(per_seg):
                state = rk4_step(state, torch.tensor(rho_value), dt)
            starts.append(state.clone())

    # Now compute the gradient *within* each segment separately
    for k in range(K):
        rho.grad = None
        s = starts[k].clone()  # detached, fresh leaf for this segment
        z_acc = s[2].abs()
        for _ in range(per_seg):
            s = rk4_step(s, rho, dt)
            z_acc = z_acc + s[2].abs()
        J_seg = z_acc / (per_seg + 1)
        J_seg.backward()
        total_grad += float(rho.grad.detach())
        total_J += float(J_seg.detach())
        n_terms += 1
    return abs(total_grad), total_J / n_terms


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "results", "repass", "lorenz")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    rho_value = 28.0
    x0 = torch.tensor([1.0, 1.0, 1.0])
    # Burn in for 10 time units to reach the attractor
    with torch.no_grad():
        s = x0.clone()
        for _ in range(int(10.0 / DT)):
            s = rk4_step(s, torch.tensor(rho_value), DT)
        x0 = s.clone()

    horizons = [2.0, 5.0, 10.0, 20.0, 40.0]  # last is ~2 Lyapunov times
    K_split = 10  # MP into 10 segments

    print(f"Lorenz-63 gradient explosion diagnostic")
    print(f"  rho={rho_value}, dt={DT}, K_segments={K_split}")
    print(f"  IC after burn-in: x0={x0.numpy()}")
    print("-" * 60)

    results = {"horizons": horizons, "K_split": K_split,
               "rho": rho_value, "dt": DT,
               "vanilla_grad": [], "vanilla_J": [],
               "mp_grad": [],      "mp_J": []}

    t0 = time.time()
    for T in horizons:
        vg, vJ = vanilla_gradient(rho_value, T, x0)
        mg, mJ = mp_gradient(rho_value, T, K_split, x0)
        results["vanilla_grad"].append(vg)
        results["vanilla_J"].append(vJ)
        results["mp_grad"].append(mg)
        results["mp_J"].append(mJ)
        print(f"  T={T:>5.1f}   vanilla |dJ/drho|={vg:.3e}  J={vJ:.4f}  |  MP |dJ/drho|={mg:.3e}  J={mJ:.4f}", flush=True)
    print(f"Total time: {time.time()-t0:.1f}s")

    # Save
    with open(os.path.join(out_dir, "gradient_vs_horizon.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.semilogy(horizons, results["vanilla_grad"], "o-", color='C3', lw=2, label="vanilla single-shot autodiff")
    ax.semilogy(horizons, results["mp_grad"], "s-", color='C0', lw=2, label=f"MP (K={K_split} segments)")
    ax.set_xlabel("Integration horizon T (time units; Lyapunov time tau_L ≈ 22)")
    ax.set_ylabel("|d J / d rho|   (log scale)")
    ax.set_title("Lorenz-63: gradient magnitude vs horizon length\n"
                 "(reproduces qualitative claim of Fig. 2 / Section 4.1.1)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "lorenz_gradient_explosion.png"), dpi=140)
    plt.close(fig)

    # Quantitative summary
    ratio_at_longest = results["vanilla_grad"][-1] / max(results["mp_grad"][-1], 1e-30)
    growth_factor_vanilla = results["vanilla_grad"][-1] / results["vanilla_grad"][0]
    growth_factor_mp = results["mp_grad"][-1] / max(results["mp_grad"][0], 1e-30)
    summary = {
        "rho": rho_value,
        "horizons": horizons,
        "K_split": K_split,
        "vanilla_grad_at_T2":  results["vanilla_grad"][0],
        "vanilla_grad_at_T40": results["vanilla_grad"][-1],
        "mp_grad_at_T2":  results["mp_grad"][0],
        "mp_grad_at_T40": results["mp_grad"][-1],
        "vanilla_to_mp_ratio_at_T40":  ratio_at_longest,
        "vanilla_growth_factor_T2_to_T40":  growth_factor_vanilla,
        "mp_growth_factor_T2_to_T40":  growth_factor_mp,
        "paper_qualitative_claim": "vanilla grad O(1e8) early, MP grad bounded",
        "our_qualitative_finding": (
            f"vanilla grows {growth_factor_vanilla:.2e}x from T=2 to T=40; "
            f"MP grows {growth_factor_mp:.2e}x; "
            f"vanilla/MP ratio at T=40 = {ratio_at_longest:.2e}"
        ),
    }
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
