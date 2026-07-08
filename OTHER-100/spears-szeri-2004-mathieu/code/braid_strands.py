"""
braid_strands.py
=================

Spears & Szeri (2004), Sec. 3.2-3.3 (Figs. 16, 17, 18): TTB topology
characterised by the number of strands ("braid strands") of the attractor
in a Poincare section of the suspended R^2 x T^2 flow.

Setup.  The QP-forced Mathieu equation (2) is non-autonomous in t̂ via
two trigonometric forcings:
    primary    cos(2 t̂)         with period pi
    secondary  cos(2 wf t̂)      with period pi/wf
Suspending in R^2 x T^2 introduces two phase variables theta_1, theta_2
(see paper Eq. 22-ish; the OCR is fuzzy on the equation numbers but the
structure is standard: theta_1(t̂) = 2 t̂ mod 2 pi, theta_2(t̂) = 2 wf t̂
mod 2 pi).

For each choice of Poincare section we strobe the suspended flow at
*one* of the two phases (we use theta_1 = 0, i.e. t̂ = k pi for k in Z):
    Sigma_theta_1 = { (z, zdot, theta_2) : theta_1 = 0 }.

In Sigma_theta_1 the attractor is a closed curve.  Its strand count =
number of disconnected components when we further project to the (z, zdot)
plane (i.e. we forget theta_2).  Paper's claim:
    non-resonant  -> 1 strand   (Fig. 16)
    resonant      -> 2 strands  (Fig. 17)

Why 2 strands at resonance:  the slow Poincare map (built by strobing at
the SLOW forcing period) has a stable period-2 orbit in (A,B), as we
confirmed in detuned_poincare.py.   This period-2 implies the attractor
in the fast suspended flow consists of TWO topologically distinct closed
curves (one passing through each fixed point of the slow Poincare).
When we strobe at theta_1 = 0 we see two disjoint loops.

Anchoring (paper Sec. 3.3).   We reconstruct an initial condition (z, zdot)
from a slow-amplitude fixed point (A0, B0) via the 5-term truncation
    z0(t̂=0)    = A0 sum_n D_2n
    z0'(t̂=0)   = B0 sum_n (2n+beta) D_2n
and then integrate the fast (z, zdot) system long enough to densely cover
the attractor.

Cases.
  (a) NON-RESONANT.  Detune outside the resonance window, wf < 0.6375 or
      wf > 0.6405.  The numerics show z -> 0 (paper Fig. 10/16):
      attractor is the origin -> trivially 1 strand (a point in the section).
      We use a small initial condition to land on the trivial attractor.
  (b) RESONANT.  wf in [0.6375, 0.6405] inside the response peak; integrate
      a large-amplitude initial condition to land on the period-2 orbit.

For each case we:
  - integrate (z, zdot) from t=0 to t=T_long,
  - extract the Poincare section by linearly interpolating z, zdot at the
    times when t̂ = k pi  (theta_1 wraps),
  - drop the early ~30% as transient,
  - cluster the section points and count the number of well-separated
    connected components -> "braid strand count".

Run:  python3 braid_strands.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from mathieu_beta import solve_beta, compute_D_coeffs
from simulate import simulate


# ----------------------------------------------------------------------
# Strand counting
# ----------------------------------------------------------------------

def count_strands(zsamp: np.ndarray, dsamp: np.ndarray,
                  n_clusters_max: int = 6) -> tuple[int, dict]:
    """Count discrete connected components in the Poincare-section point
    cloud (z, dz/dt).  We use a simple k-means scan and detect the
    elbow in SSE: the strand count is the smallest k for which the
    per-point cluster scatter is significantly smaller than the inter-
    cluster distance.
    """
    from scipy.cluster.vq import kmeans2
    pts = np.column_stack([zsamp, dsamp])
    # Normalise scale so z and dz/dt are comparable in the L2 metric
    span = np.std(pts, axis=0)
    span[span < 1e-9] = 1.0
    pts_n = pts / span
    info = {}
    sse_list = []
    sigma_list = []
    sep_list = []
    for k in range(1, n_clusters_max + 1):
        if len(pts_n) < k:
            sse_list.append(float('nan'))
            sigma_list.append(float('nan'))
            sep_list.append(0.0)
            continue
        c, l = kmeans2(pts_n, k, seed=0, minit='++')
        ss = float(np.sum(np.linalg.norm(pts_n - c[l], axis=1) ** 2))
        sse_list.append(ss)
        sigma_list.append((ss / max(len(pts_n), 1)) ** 0.5)
        if k >= 2:
            # min center-center distance
            dmin = float('inf')
            for i in range(k):
                for j in range(i + 1, k):
                    d = float(np.linalg.norm(c[i] - c[j]))
                    if d < dmin:
                        dmin = d
            sep_list.append(dmin)
        else:
            sep_list.append(0.0)

    # If the data is one big cloud (continuous loop), k=1 gives a large
    # sigma that is comparable to the data span itself (sigma ~ 1
    # after normalisation).  If it is N disconnected clusters, after
    # k=N the per-point sigma drops to ~ point-thickness << separation.
    # Heuristic: strand count = smallest k for which sigma_k < 0.10 *
    # min_separation_k.
    strand_count = 1
    for k in range(1, len(sse_list)):
        if sep_list[k] > 0 and sigma_list[k] < 0.10 * sep_list[k]:
            strand_count = k + 1   # k index 0 = k=1, so k=1 is index 1
            break
    # SPECIAL CASE: if even k=1 gives sigma ~ 0 (trivial point attractor)
    if sigma_list[0] < 1e-3:
        strand_count = 1

    info['sse_per_k'] = sse_list
    info['sigma_per_k'] = sigma_list
    info['min_separation_per_k'] = sep_list
    info['detected_strand_count'] = int(strand_count)
    info['span_used_for_normalisation'] = span.tolist()
    return strand_count, info


# ----------------------------------------------------------------------
# Poincare section extraction by linear interpolation across t = k pi
# ----------------------------------------------------------------------

def poincare_section_theta(t, z, zdot, period, drop_first_frac=0.4):
    """Strobe at t̂ = k * `period` (theta = 0 for the forcing of that period).
    For Sigma_{theta_1}=0 use period=pi (primary forcing).
    For Sigma_{theta_2}=0 use period=pi/wf (secondary forcing).
    """
    t0 = t[0]; tend = t[-1]
    k_start = int(np.ceil(t0 / period))
    k_end = int(np.floor(tend / period))
    drop_until = t0 + drop_first_frac * (tend - t0)
    z_pts = []
    d_pts = []
    t_pts = []
    for k in range(k_start, k_end + 1):
        t_strobe = k * period
        if t_strobe < drop_until:
            continue
        i = np.searchsorted(t, t_strobe)
        if i <= 0 or i >= len(t):
            continue
        t1, t2 = t[i - 1], t[i]
        if t2 == t1:
            continue
        f = (t_strobe - t1) / (t2 - t1)
        z_pts.append(z[i - 1] + f * (z[i] - z[i - 1]))
        d_pts.append(zdot[i - 1] + f * (zdot[i] - zdot[i - 1]))
        t_pts.append(t_strobe)
    return np.array(t_pts), np.array(z_pts), np.array(d_pts)


def count_components_dbscan(pts, eps_frac=0.05,
                            trivial_radius_threshold=1e-2):
    """Topological component count via DBSCAN with eps tied to the
    point-cloud span.  Returns (n_components, labels).  Points labeled
    -1 (noise) are ignored.

    Special case: if the entire point cloud lies within a small ball
    around the origin (max radius < `trivial_radius_threshold`), report
    1 component (trivial attractor at the origin).
    """
    from sklearn.cluster import DBSCAN
    N = len(pts)
    if N < 4:
        return 1, np.zeros(N, dtype=int)
    # Trivial attractor detector: amplitude << 1
    max_r = float(np.max(np.linalg.norm(pts, axis=1)))
    if max_r < trivial_radius_threshold:
        return 1, np.zeros(N, dtype=int)
    span = np.std(pts, axis=0)
    span[span < 1e-9] = 1.0
    pts_n = pts / span
    # For ~ N points on a connected loop in a normalised plane,
    # nearest-neighbour spacing ~ 6/N (loop circumference ~ 2 pi after
    # std-normalising).  Two disjoint loops separated by ~ 1 unit have
    # inter-loop distance ~ 1, intra-loop spacing ~ 6/N -> ratio ~ N/6.
    # Set eps to a small multiple of intra-loop spacing.
    eps_val = max(24.0 / N, eps_frac)
    db = DBSCAN(eps=eps_val, min_samples=3).fit(pts_n)
    labels = db.labels_
    # Count clusters that contain >= 5% of the points (suppress micro-noise)
    raw_labels = set(labels)
    if -1 in raw_labels:
        raw_labels.remove(-1)
    big_components = 0
    min_size = max(5, int(0.05 * N))
    for c in raw_labels:
        if int(np.sum(labels == c)) >= min_size:
            big_components += 1
    n_components = big_components if big_components > 0 else 1
    return int(n_components), labels


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def run_case(label, wf, y0, t_end, alpha, gamma, mu, chi, delta, eps,
             figdir: Path, evdir: Path):
    print(f"\n=== {label}  (wf={wf:.5f}, y0={y0}, t_end={t_end:.0f}) ===")
    dt = 0.025  # ~120 samples per primary period pi for clean interp
    t_eval = np.arange(0.0, t_end, dt)
    t, z, zdot = simulate(alpha, gamma, mu, chi, delta, eps, wf,
                          t_end=t_end, y0=y0, t_eval=t_eval,
                          rtol=1e-9, atol=1e-11)
    print(f"  integrated {len(t)} samples to t={t[-1]:.0f}; "
          f"final |z|={abs(z[-1]):.3f}")

    # Build both Poincare sections per paper Sec 3.2.
    # Sigma_{theta_1=0}: strobe at primary period pi  (paper says count remains 1)
    # Sigma_{theta_2=0}: strobe at secondary period pi/wf  (paper: 1 -> 2 at resonance)
    tps1, zps1, dps1 = poincare_section_theta(t, z, zdot, period=np.pi,
                                              drop_first_frac=0.5)
    tps2, zps2, dps2 = poincare_section_theta(t, z, zdot, period=np.pi/wf,
                                              drop_first_frac=0.5)
    print(f"  Sigma_theta1 (period pi):       {len(zps1)} samples; "
          f"z [{zps1.min():.3f},{zps1.max():.3f}]  zdot [{dps1.min():.3f},{dps1.max():.3f}]")
    print(f"  Sigma_theta2 (period pi/wf):    {len(zps2)} samples; "
          f"z [{zps2.min():.3f},{zps2.max():.3f}]  zdot [{dps2.min():.3f},{dps2.max():.3f}]")

    # Component count via DBSCAN, separately on each section.
    pts1 = np.column_stack([zps1, dps1])
    pts2 = np.column_stack([zps2, dps2])
    n_comp_1, labels1 = count_components_dbscan(pts1)
    n_comp_2, labels2 = count_components_dbscan(pts2)
    print(f"  Sigma_theta1 connected components (DBSCAN): {n_comp_1}")
    print(f"  Sigma_theta2 connected components (DBSCAN): {n_comp_2}")

    # Per paper, the braid strand count is the Sigma_theta_2 component count.
    strand_count = n_comp_2
    info = dict(n_components_theta1=n_comp_1,
                n_components_theta2=n_comp_2,
                n_samples_theta1=int(len(zps1)),
                n_samples_theta2=int(len(zps2)))

    # Plot: phase plane + two Poincare sections
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    ax = axes[0]
    ax.plot(z[::80], zdot[::80], '-', lw=0.2, color='grey', alpha=0.5)
    ax.set_xlabel('z'); ax.set_ylabel("dz/dt")
    ax.set_title(f"Fast phase plane (z, dz/dt)\n{label}, wf={wf:.5f}")
    ax.grid(True, alpha=0.3)

    cmap = plt.get_cmap('tab10')
    ax1 = axes[1]
    for c in sorted(set(labels1)):
        m = labels1 == c
        color = 'k' if c < 0 else cmap(c % 10)
        ax1.scatter(zps1[m], dps1[m], color=color, s=10, alpha=0.7,
                    label=f'cluster {c}' if c >= 0 else 'noise')
    ax1.set_xlabel('z'); ax1.set_ylabel('dz/dt')
    ax1.set_title(f"Sigma_theta1=0 (strobe t=k pi)\n"
                  f"components = {n_comp_1}  (paper: 1)")
    ax1.grid(True, alpha=0.3)
    if n_comp_1 <= 6:
        ax1.legend(loc='best', fontsize=7)

    ax2 = axes[2]
    for c in sorted(set(labels2)):
        m = labels2 == c
        color = 'k' if c < 0 else cmap(c % 10)
        ax2.scatter(zps2[m], dps2[m], color=color, s=10, alpha=0.7,
                    label=f'cluster {c}' if c >= 0 else 'noise')
    ax2.set_xlabel('z'); ax2.set_ylabel('dz/dt')
    ax2.set_title(f"Sigma_theta2=0 (strobe t=k pi/wf)\n"
                  f"components = {n_comp_2}  (paper: 1 nonres / 2 res)")
    ax2.grid(True, alpha=0.3)
    if n_comp_2 <= 6:
        ax2.legend(loc='best', fontsize=7)
    fig.tight_layout()
    return dict(label=label, wf=float(wf),
                t_end=float(t_end),
                n_samples_theta1=int(len(zps1)),
                n_samples_theta2=int(len(zps2)),
                z_range=[float(zps2.min()), float(zps2.max())],
                zdot_range=[float(dps2.min()), float(dps2.max())],
                strand_count=int(strand_count),
                n_components_theta1=int(n_comp_1),
                n_components_theta2=int(n_comp_2),
                ), fig, (tps2, zps2, dps2)


def main():
    here = Path(__file__).resolve().parent
    figdir = here.parent / "figures"; figdir.mkdir(exist_ok=True)
    evdir  = here.parent / "evidence"; evdir.mkdir(exist_ok=True)

    alpha = 0.05
    gamma = -0.10
    mu = chi = delta = 1.0
    eps = 1e-3
    beta = solve_beta(alpha, gamma)
    D_dict = compute_D_coeffs(alpha, gamma, beta, n_max=2)
    D_numeric = {n: float(D_dict[n]) for n in range(-2, 3)}
    print(f"beta = {beta:.6f}")

    # ------------------------------------------------------------------
    # CASE (a): non-resonant.  wf well outside the resonance window
    # ([0.6375, 0.6405]).  Choose wf = 0.55 (paper's Fig. 16 region).
    # Small initial seed so we land on the trivial attractor (origin).
    # ------------------------------------------------------------------
    res_nonres, fig_nonres, ps_nonres = run_case(
        "non-resonant",
        wf=0.55,
        y0=(0.05, 0.0),
        t_end=12000.0,
        alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta, eps=eps,
        figdir=figdir, evdir=evdir,
    )
    fig_nonres.savefig(figdir / "fig16_braid_nonres.png", dpi=160)
    plt.close(fig_nonres)
    print(f"  wrote figures/fig16_braid_nonres.png")

    # ------------------------------------------------------------------
    # CASE (b): resonant.  wf inside the resonance window.  We use the
    # same parameters as the detuned Poincare run -> wf = 0.638503.
    # Large initial seed to land on the period-2 attractor.
    # ------------------------------------------------------------------
    wf_res = 0.638503
    res_res, fig_res, ps_res = run_case(
        "resonant (in window)",
        wf=wf_res,
        y0=(1.0, 0.0),
        t_end=20000.0,
        alpha=alpha, gamma=gamma, mu=mu, chi=chi, delta=delta, eps=eps,
        figdir=figdir, evdir=evdir,
    )
    fig_res.savefig(figdir / "fig17_braid_res.png", dpi=160)
    plt.close(fig_res)
    print(f"  wrote figures/fig17_braid_res.png")

    # Save data and summary
    np.savez(evdir / "braid_sections.npz",
             nonres_t=ps_nonres[0], nonres_z=ps_nonres[1], nonres_d=ps_nonres[2],
             res_t=ps_res[0], res_z=ps_res[1], res_d=ps_res[2],
             beta=beta, alpha=alpha, gamma=gamma,
             eps=eps, mu=mu, chi=chi, delta=delta,
             wf_nonres=0.55, wf_res=wf_res)
    print(f"  saved evidence/braid_sections.npz (theta_2 sections only)")

    summary = {
        "alpha": alpha, "gamma": gamma, "mu": mu, "chi": chi, "delta": delta,
        "eps": eps, "beta": beta,
        "non_resonant": res_nonres,
        "resonant": res_res,
        "claim": ("paper Sec. 3.2: non-resonant attractor is a 1-strand braid "
                  "(Fig. 16); resonant attractor is a 2-strand braid (Fig. 17)."),
        "verdict": (
            f"non-resonant strands = {res_nonres['strand_count']}, "
            f"resonant strands = {res_res['strand_count']} "
            "-> paper claim {} confirmed".format(
                "is" if (res_nonres['strand_count'] == 1
                         and res_res['strand_count'] == 2)
                else "needs review")
        ),
    }
    (evdir / "braid_strands.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"\nWrote evidence/braid_strands.json")
    print(f"\nSUMMARY:")
    print(f"  non-resonant  (wf={summary['non_resonant']['wf']:.4f}): "
          f"{summary['non_resonant']['strand_count']} strand(s)")
    print(f"  resonant      (wf={summary['resonant']['wf']:.4f}): "
          f"{summary['resonant']['strand_count']} strand(s)")
    print(f"  -> {summary['verdict']}")


if __name__ == "__main__":
    main()
