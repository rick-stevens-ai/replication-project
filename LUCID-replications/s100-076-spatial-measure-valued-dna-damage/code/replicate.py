#!/usr/bin/env python3
"""
Replication of Cordoni 2024, "A spatial measure-valued model for radiation-induced
DNA damage kinetics and repair under protracted irradiation condition"
(J Math Biol 88:21, https://doi.org/10.1007/s00285-024-02046-3)

Replicator: Ollie subagent (Argo Opus 4.7, free endpoints), 2026-06-22
LUCID slot: s100-076

This script reproduces the spatial measure-valued process described in Section 6
"Numerical results", producing analogs of Figures 1 and 2:
  - Fig 1 top-left:  normalized dose deposition over the 5-um circular nucleus
                     using the Kase amorphous track model (D(rho) = Cc inside Rc,
                     Cp/rho^2 between Rc and Rp, 0 outside).
  - Fig 1 top-right: initial spatial distribution of sub-lethal lesions (blue) +
                     track hit positions (red).
  - Fig 1 bottom-left: same lesion field with a high-local-density cluster
                       highlighted in a 1.5 um circle.
  - Fig 1 bottom-right: discretized version (square sub-domains) showing how
                        a cluster gets diluted across discrete domains.
  - Fig 2: time evolution (Gillespie-SSA on the spatial measure-valued process)
           of sub-lethal lesions (blue) and lethal lesions (orange) at
           three time points.

Parameters (Section 6, Cordoni 2024):
  Nucleus:    2D disk, radius R_nuc = 5 um
  Beam:       40 MeV/u carbon ions, perpendicular
  Total dose: D_tot = 10 Gy
  zF:         0.04 Gy   (fluence-average specific energy per event)
  kappa:      50 Gy^-1  (sub-lethal lesions per Gy of local specific energy)
  lambda:     0.5 Gy^-1 (lethal lesions per Gy = kappa * 1e-2)
  Track model (Kase 2007, low-energy carbon proxy):
      Rc:    0.01 um   (track core; not given explicitly in paper -- standard
                        order-of-magnitude for low-E carbon)
      Rp:    1.0  um   (penumbra; chosen so visualization on 5 um disk is legible
                        and is in the documented range for ~40 MeV/u carbon)
      Cc, Cp normalized so that integral 2*pi*rho*D(rho) drho = z_i
  Reaction rates:
      r = 4.0 h^-1   (sub-lethal repair)
      a = 0.1 h^-1   (sub-lethal -> lethal conversion baseline)
      b = 0.1 h^-1   (pairwise X+X interaction baseline)
      rd = 0.5 um    (local density radius)
  Rate modulation (Eq. 73): with v_local(q) = # damages within rd of q,
      r(q) = r * (1 + 1/(v_local+1))   -- decreasing repair efficiency
                                          when site is in a damage cluster
      a(q) = a * (1 - 1/(v_local+1))   -- increasing death rate in clusters
      b(q1,q2) = b * 1{|q1-q2| < rd}

Notes:
  - The paper's repair rate formula in Eq. 73 contains a (q-qbar) indicator
    expression that is presented somewhat ambiguously in the PDF text
    extraction; we use the natural interpretation that r grows / a shrinks
    as 1/(v+1), with v being the local count of neighbors within rd.  This
    matches the paper's prose: "repair rate decreases as the number of damages
    within a radius rd = 0.5 um increases".  ** Important caveat: depending on
    sign convention this could be inverted; we follow Cordoni's prose. **
  - Diffusion (sigma_X, sigma_Y) is not specified numerically in Section 6,
    so we run with sigma=0 (purely jump-driven dynamics) as the paper's
    Figure 2 description is consistent with a quasi-static spatial distribution
    on the depicted time scale.
  - The Pairwise b reaction places the new lethal lesion at the midpoint of
    the two interacting sub-lethals (paper text).
"""

import os
import json
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# -------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------
HERE     = os.path.dirname(os.path.abspath(__file__))
BASE     = os.path.dirname(HERE)
FIG_DIR  = os.path.join(BASE, "figures")
EVID_DIR = os.path.join(BASE, "evidence")
os.makedirs(FIG_DIR,  exist_ok=True)
os.makedirs(EVID_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# Parameters (Section 6 of the paper)
# -------------------------------------------------------------------------
R_NUC    = 5.0          # um, nucleus radius
D_TOT    = 10.0         # Gy, total absorbed dose
Z_F      = 0.04         # Gy, fluence-average specific energy per event
KAPPA    = 50.0         # Gy^-1, sub-lethals per Gy
LAMBDA_X = KAPPA * 1e-2 # Gy^-1, lethals per Gy = 0.5

# Amorphous track model (Kase 2007).  Values for low-energy carbon-ion
# track structure on the order documented in Kase et al. and Bellinzona 2021.
R_C = 0.01              # um, core radius
R_P = 1.00              # um, penumbra radius (visual-friendly for 5-um disk)

# Reaction kinetics
R_BASE = 4.0            # h^-1
A_BASE = 0.1            # h^-1
B_BASE = 0.1            # h^-1   (this is the per-pair rate constant)
RD     = 0.5            # um, local-density radius

# Simulation horizon for Figure 2 analog
T_SIM_H   = 6.0         # hours
SNAPSHOTS = [0.0, 1.0, 3.0]   # snapshots used for Fig 2 panels (h)

RNG = np.random.default_rng(20260622)

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------
def sample_in_disk(n, R, rng):
    """n uniform points in disk of radius R centered at origin."""
    r = R * np.sqrt(rng.uniform(0.0, 1.0, size=n))
    th = rng.uniform(0.0, 2*np.pi, size=n)
    return np.column_stack([r*np.cos(th), r*np.sin(th)])

def amorphous_track_dose(rho, z_i, Rc=R_C, Rp=R_P):
    """Kase 2007 radial dose D(rho).  Normalized so that the area integral
    over the (Rc,Rp) cup core equals z_i, the specific energy of this event."""
    # Integral I0 of unnormalized profile:  pi Rc^2 + 2 pi ln(Rp/Rc)
    I0 = math.pi * Rc**2 + 2.0 * math.pi * math.log(Rp/Rc)
    Cc = z_i / I0
    Cp = Cc
    D = np.zeros_like(rho)
    inner = rho <= Rc
    mid   = (rho > Rc) & (rho <= Rp)
    D[inner] = Cc
    D[mid]   = Cp / (rho[mid]**2 / 1.0)   # Cp/rho^2 with rho in um
    # Note: paper writes Cp / rho^2 directly; we keep the same form.
    return D

def deposit_dose_grid(track_pos, z_events, R_nuc=R_NUC, n=400):
    """Sum the amorphous-track radial dose from all tracks onto an n x n grid
    inside [-R_nuc,R_nuc]^2.  Mask outside the nucleus disk."""
    xs = np.linspace(-R_nuc, R_nuc, n)
    ys = np.linspace(-R_nuc, R_nuc, n)
    X, Y = np.meshgrid(xs, ys)
    Dgrid = np.zeros_like(X)
    for (qx, qy), zi in zip(track_pos, z_events):
        rho = np.sqrt((X-qx)**2 + (Y-qy)**2)
        # Avoid div-by-zero in Cp/rho^2 region
        rho_safe = np.where(rho < 1e-6, 1e-6, rho)
        D = np.zeros_like(X)
        D[rho <= R_C] = zi / (math.pi * R_C**2 + 2*math.pi*math.log(R_P/R_C))
        mid_mask = (rho > R_C) & (rho <= R_P)
        Cp = zi / (math.pi * R_C**2 + 2*math.pi*math.log(R_P/R_C))
        D[mid_mask] = Cp / (rho_safe[mid_mask]**2)
        Dgrid += D
    mask = (X**2 + Y**2) <= R_nuc**2
    Dgrid = np.where(mask, Dgrid, np.nan)
    return X, Y, Dgrid

def sample_lesions_around_track(track_xy, z_i, kappa, lam, rng, Rc=R_C, Rp=R_P):
    """Sample Poisson(kappa*z_i) sub-lethals and Poisson(lam*z_i) lethals,
    distributed radially around the track with density proportional to
    rho * D(rho)  (Jacobian-corrected radial weight)."""
    nX = rng.poisson(kappa * z_i)
    nY = rng.poisson(lam   * z_i)

    def draw_radial(n):
        # PDF(rho) ~ 2*pi*rho * D(rho).  Build inverse CDF numerically.
        if n == 0:
            return np.zeros((0,2))
        rgrid = np.linspace(1e-4, Rp, 1000)
        # density profile in rho: rho*D(rho)
        prof = np.zeros_like(rgrid)
        Dunit = 1.0   # any normalization OK for CDF
        for i, rho in enumerate(rgrid):
            if rho <= Rc:
                prof[i] = rho * Dunit
            else:
                prof[i] = rho * (Dunit * Rc**2 / rho**2)   # rho * Cp/rho^2 -> Cp/rho
        cdf = np.cumsum(prof)
        cdf = cdf / cdf[-1]
        u = rng.uniform(0,1,n)
        rs = np.interp(u, cdf, rgrid)
        th = rng.uniform(0, 2*np.pi, n)
        return np.column_stack([track_xy[0]+rs*np.cos(th),
                                track_xy[1]+rs*np.sin(th)])

    Xs = draw_radial(nX)
    Ys = draw_radial(nY)
    # Trim lesions that escape the nucleus
    if len(Xs) > 0:
        Xs = Xs[ (Xs[:,0]**2 + Xs[:,1]**2) <= R_NUC**2 ]
    if len(Ys) > 0:
        Ys = Ys[ (Ys[:,0]**2 + Ys[:,1]**2) <= R_NUC**2 ]
    return Xs, Ys

# -------------------------------------------------------------------------
# Step 1.  Sample tracks + initial lesions  (Fig 1 analog)
# -------------------------------------------------------------------------
print(f"=== s100-076 Cordoni 2024 spatial measure-valued DNA damage ===")
N_tracks_mean = D_TOT / Z_F                # 250
N_tracks = RNG.poisson(N_tracks_mean)
print(f"Mean tracks per nucleus (D/zF): {N_tracks_mean:.1f}; this draw: {N_tracks}")

track_xy = sample_in_disk(N_tracks, R_NUC, RNG)
# specific energy per event: for monoenergetic narrow f_1(z) we approximate
# by the average zF (the paper says z_i ~ f_1(z) but Section 6 gives only zF).
z_events = np.full(N_tracks, Z_F)
print(f"Total deposited specific energy (sum z_i): {z_events.sum():.3f} Gy "
      f"(target 10 Gy)")

# Initial lesions
all_X = []
all_Y = []
for tpos, zi in zip(track_xy, z_events):
    Xs, Ys = sample_lesions_around_track(tpos, zi, KAPPA, LAMBDA_X, RNG)
    all_X.append(Xs); all_Y.append(Ys)
X = np.vstack(all_X) if all_X else np.zeros((0,2))
Y = np.vstack(all_Y) if all_Y else np.zeros((0,2))
print(f"Initial sub-lethal (X) count: {len(X)}   (expected ~ kappa*D*A_nuc-weighted)")
print(f"Initial lethal     (Y) count: {len(Y)}")

# Build dose-deposition grid for Fig 1 top-left
gx, gy, Dgrid = deposit_dose_grid(track_xy, z_events, R_nuc=R_NUC, n=350)
Dnorm = Dgrid / np.nanmax(Dgrid)

# Identify a dense cluster (highest local density within 1.5 um) for Fig 1 bottom-left
def local_count(pts, q, r):
    if len(pts) == 0:
        return 0
    return int(np.sum((pts[:,0]-q[0])**2 + (pts[:,1]-q[1])**2 <= r**2))

R_CLUSTER = 1.5  # um
best_q = None
best_n = -1
if len(X) > 0:
    # sample over candidate centers among lesion positions
    for q in X[RNG.choice(len(X), size=min(len(X), 200), replace=False)]:
        n = local_count(X, q, R_CLUSTER)
        if n > best_n:
            best_n = n
            best_q = q
print(f"Densest 1.5-um cluster found: center {best_q}, count {best_n}")

# -------------------------------------------------------------------------
# Step 2.  Plot Figure 1 analog (4 panels)
# -------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(11,10))

ax = axes[0,0]
pc = ax.pcolormesh(gx, gy, Dnorm, cmap='magma', shading='auto')
ax.set_aspect('equal'); ax.set_title("Fig 1 top-left: normalized dose D(q)")
ax.set_xlim(-R_NUC, R_NUC); ax.set_ylim(-R_NUC, R_NUC)
plt.colorbar(pc, ax=ax, fraction=0.046)
# overlay nucleus boundary
th = np.linspace(0, 2*np.pi, 200)
ax.plot(R_NUC*np.cos(th), R_NUC*np.sin(th), 'w-', lw=1)

ax = axes[0,1]
if len(X) > 0:
    ax.scatter(X[:,0], X[:,1], s=4, c='royalblue', label=f'sub-lethal (N={len(X)})')
ax.scatter(track_xy[:,0], track_xy[:,1], s=12, c='red', marker='x',
           label=f'track hits (N={len(track_xy)})')
ax.plot(R_NUC*np.cos(th), R_NUC*np.sin(th), 'k-', lw=1)
ax.set_aspect('equal'); ax.set_title("Fig 1 top-right: sub-lethal lesions + track hits")
ax.set_xlim(-R_NUC, R_NUC); ax.set_ylim(-R_NUC, R_NUC); ax.legend(loc='lower left', fontsize=8)

ax = axes[1,0]
if len(X) > 0:
    ax.scatter(X[:,0], X[:,1], s=4, c='royalblue', label=f'sub-lethal (N={len(X)})')
if best_q is not None:
    circ = plt.Circle(best_q, R_CLUSTER, fill=False, ec='red', ls='--', lw=2)
    ax.add_patch(circ)
    ax.set_title(f"Fig 1 bottom-left: cluster (N={best_n}) within 1.5 um")
ax.plot(R_NUC*np.cos(th), R_NUC*np.sin(th), 'k-', lw=1)
ax.set_aspect('equal'); ax.set_xlim(-R_NUC, R_NUC); ax.set_ylim(-R_NUC, R_NUC)

ax = axes[1,1]
# discretization: 5x5 sub-domains over [-R,R]^2
nbin = 5
edges = np.linspace(-R_NUC, R_NUC, nbin+1)
for e in edges:
    ax.axvline(e, color='gray', lw=0.5)
    ax.axhline(e, color='gray', lw=0.5)
if len(X) > 0:
    ax.scatter(X[:,0], X[:,1], s=4, c='royalblue')
if best_q is not None:
    circ = plt.Circle(best_q, R_CLUSTER, fill=False, ec='red', ls='--', lw=2)
    ax.add_patch(circ)
ax.plot(R_NUC*np.cos(th), R_NUC*np.sin(th), 'k-', lw=1)
ax.set_aspect('equal'); ax.set_title("Fig 1 bottom-right: discretized (5x5) view")
ax.set_xlim(-R_NUC, R_NUC); ax.set_ylim(-R_NUC, R_NUC)

plt.tight_layout()
fig1_path = os.path.join(FIG_DIR, "fig1_analog.png")
plt.savefig(fig1_path, dpi=140)
plt.close()
print(f"Wrote {fig1_path}")

# -------------------------------------------------------------------------
# Step 3.  Gillespie SSA on the measure-valued process  (Fig 2 analog)
# -------------------------------------------------------------------------
print("\n=== Gillespie SSA on spatial measure-valued process ===")

def local_density(pts, rd=RD):
    """For every lesion, count #neighbours-within-rd (excluding self)."""
    if len(pts) == 0:
        return np.zeros(0, dtype=int)
    d2 = np.sum((pts[:,None,:] - pts[None,:,:])**2, axis=-1)
    return np.sum(d2 <= rd*rd, axis=1) - 1

def step_rates(X_pts, r_base=R_BASE, a_base=A_BASE, b_base=B_BASE, rd=RD):
    """Per-lesion repair rate r_i, per-lesion conversion rate a_i,
    and total pairwise rate b_tot for X+X."""
    v = local_density(X_pts, rd=rd)
    r_i = r_base * (1.0 + 1.0/(v+1))
    a_i = a_base * (1.0 - 1.0/(v+1))   # equals 0 when v=0; baseline when crowded
    # Number of close pairs within rd
    if len(X_pts) < 2:
        n_pairs = 0
    else:
        d2 = np.sum((X_pts[:,None,:] - X_pts[None,:,:])**2, axis=-1)
        n_pairs = int(np.sum(np.triu(d2 <= rd*rd, k=1)))
    b_tot = b_base * n_pairs
    return r_i, a_i, b_tot

X_traj = X.copy()
Y_traj = Y.copy()
t = 0.0
T_END = T_SIM_H

snapshots = {0.0: (X_traj.copy(), Y_traj.copy())}
next_snap_idx = 1
last_log = 0.0
nsteps = 0

t0 = time.time()
while t < T_END and len(X_traj) > 0:
    r_i, a_i, b_tot = step_rates(X_traj)
    R_r = float(r_i.sum())
    R_a = float(a_i.sum())
    R_b = float(b_tot)
    R_tot = R_r + R_a + R_b
    if R_tot <= 0:
        break
    dt = RNG.exponential(1.0/R_tot)
    # check snapshots
    while next_snap_idx < len(SNAPSHOTS) and t + dt >= SNAPSHOTS[next_snap_idx]:
        snapshots[SNAPSHOTS[next_snap_idx]] = (X_traj.copy(), Y_traj.copy())
        next_snap_idx += 1
    t += dt
    u = RNG.uniform(0, R_tot)
    if u < R_r:
        # pick which X repairs
        idx = int(np.searchsorted(np.cumsum(r_i), u))
        idx = min(idx, len(X_traj)-1)
        X_traj = np.delete(X_traj, idx, axis=0)
    elif u < R_r + R_a:
        u2 = u - R_r
        idx = int(np.searchsorted(np.cumsum(a_i), u2))
        idx = min(idx, len(X_traj)-1)
        # X -> Y at same position
        q = X_traj[idx]
        X_traj = np.delete(X_traj, idx, axis=0)
        Y_traj = np.vstack([Y_traj, q])
    else:
        # pairwise b: pick a close pair uniformly at random
        d2 = np.sum((X_traj[:,None,:] - X_traj[None,:,:])**2, axis=-1)
        pairs_mask = np.triu(d2 <= RD*RD, k=1)
        ii, jj = np.where(pairs_mask)
        if len(ii) == 0:
            continue
        k = RNG.integers(0, len(ii))
        i1, i2 = ii[k], jj[k]
        q_mid = 0.5*(X_traj[i1] + X_traj[i2])
        # Always create lethal at midpoint (paper says p Bernoulli choice but
        # gives no explicit p; we use deterministic create as the dominant path)
        keep = np.ones(len(X_traj), dtype=bool)
        keep[i1] = False; keep[i2] = False
        X_traj = X_traj[keep]
        Y_traj = np.vstack([Y_traj, q_mid])
    nsteps += 1
    if t - last_log >= 0.5:
        last_log = t
        print(f"  t={t:5.2f} h   |X|={len(X_traj):4d}  |Y|={len(Y_traj):4d}  "
              f"steps={nsteps}")

# capture remaining snapshots
for ts in SNAPSHOTS:
    if ts not in snapshots:
        snapshots[ts] = (X_traj.copy(), Y_traj.copy())
snapshots[T_END] = (X_traj.copy(), Y_traj.copy())
elapsed = time.time() - t0
print(f"SSA finished in {elapsed:.2f}s, {nsteps} jumps, final t={t:.2f} h, "
      f"|X|={len(X_traj)}, |Y|={len(Y_traj)}")

# -------------------------------------------------------------------------
# Step 4.  Plot Figure 2 analog (time evolution)
# -------------------------------------------------------------------------
ts_show = SNAPSHOTS
fig, axes = plt.subplots(1, len(ts_show), figsize=(4.5*len(ts_show), 4.5))
for ax, ts in zip(axes, ts_show):
    Xs, Ys = snapshots[ts]
    if len(Xs):
        ax.scatter(Xs[:,0], Xs[:,1], s=4, c='royalblue', label=f'X={len(Xs)}')
    if len(Ys):
        ax.scatter(Ys[:,0], Ys[:,1], s=8, c='orange', marker='^', label=f'Y={len(Ys)}')
    ax.plot(R_NUC*np.cos(th), R_NUC*np.sin(th), 'k-', lw=1)
    ax.set_aspect('equal')
    ax.set_xlim(-R_NUC, R_NUC); ax.set_ylim(-R_NUC, R_NUC)
    ax.set_title(f"t = {ts:.1f} h")
    ax.legend(loc='lower left', fontsize=8)
plt.suptitle("Fig 2 analog: time evolution (blue=sub-lethal, orange=lethal)")
plt.tight_layout()
fig2_path = os.path.join(FIG_DIR, "fig2_analog.png")
plt.savefig(fig2_path, dpi=140)
plt.close()
print(f"Wrote {fig2_path}")

# -------------------------------------------------------------------------
# Step 5.  Evidence dump
# -------------------------------------------------------------------------
evidence = {
    "paper": "Cordoni 2024, J Math Biol 88:21, doi:10.1007/s00285-024-02046-3",
    "section_reproduced": "Section 6 (Numerical results), Fig 1 + Fig 2",
    "parameters": {
        "R_nuc_um": R_NUC, "D_tot_Gy": D_TOT, "zF_Gy": Z_F,
        "kappa_per_Gy": KAPPA, "lambda_per_Gy": LAMBDA_X,
        "Rc_um": R_C, "Rp_um": R_P,
        "r_per_h": R_BASE, "a_per_h": A_BASE, "b_per_h": B_BASE,
        "rd_um": RD, "T_sim_h": T_SIM_H,
        "snapshots_h": SNAPSHOTS,
    },
    "rng_seed": 20260622,
    "N_tracks_mean": N_tracks_mean,
    "N_tracks_drawn": int(N_tracks),
    "initial_X": int(len(X)),
    "initial_Y": int(len(Y)),
    "best_cluster_radius_um": R_CLUSTER,
    "best_cluster_count": int(best_n),
    "ssa": {
        "nsteps": int(nsteps),
        "t_end_h": float(t),
        "final_X": int(len(X_traj)),
        "final_Y": int(len(Y_traj)),
        "wallclock_s": float(elapsed),
    },
    "fig1_png": fig1_path,
    "fig2_png": fig2_path,
}
ev_path = os.path.join(EVID_DIR, "run.json")
with open(ev_path, "w") as f:
    json.dump(evidence, f, indent=2)
print(f"Wrote evidence {ev_path}")
