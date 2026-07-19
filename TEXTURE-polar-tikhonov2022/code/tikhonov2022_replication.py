#!/usr/bin/env python3
"""
Minimal Ginzburg-Landau / TDGL replication of the essential mechanism
from Tikhonov et al., arXiv:2204.05000 -- "Topological polarization
networking in uniaxial ferroelectrics".

Scope (theory only; PFM experiment out of scope):
  - 2D uniaxial ferroelectric slab in the (x, z) plane, polar axis = z.
  - Order parameter: scalar P_z(x, z) (strong uniaxial anisotropy -> only Pz).
  - Free energy density:
        f = (a/2) P^2 + (b/4) P^4                 (Landau double-well, a<0,b>0)
          + (kx/2)(dP/dx)^2 + (kz/2)(dP/dz)^2    (anisotropic gradient)
          + (lambda_es/2) * phi_screen(P)         (electrostatic proxy: penalize
                                                   bound charge rho_b = -dP/dz)
  - The electrostatic term is implemented as a scalar penalty on the local
    bound-charge density squared, integrated in real space. This is the
    standard 'depolarization penalty' one gets when solving Poisson under
    short-circuit boundary conditions and expanding to leading order (see
    e.g. Bratkovsky-Levanyuk 2000; used in many phase-field studies).
    We do NOT solve the full Poisson equation -- the point is the mechanism,
    not the material constants.

  - TDGL relaxation:  dP/dt = -delta F / delta P
        = -a P - b P^3 + kx d2P/dx2 + kz d2P/dz2
          + lambda_es * (dP/dz)_z-derivative-of-charge-penalty
    Neumann (zero-flux) boundary conditions on all sides for P; this is
    equivalent to open (charged-surface) BC in this reduced electrostatic
    proxy and lets H-H / T-T terminate on the surfaces.

Claims tested:
  CLAIM 1  From noisy initial conditions the relaxed state develops a
           BRANCHING network of up-domains and down-domains, NOT parallel
           stripes. Measured by counting domain-wall junctions (skeleton
           vertices of degree >=3) and comparing to a stripe reference.
  CLAIM 2  The self-organized network has LOWER total electrostatic
           (bound-charge) energy than a naive charged H-H reference wall
           at the same anisotropy / material parameters.

Reduced-scope, CPU-only, numpy/scipy only. ~500 s target on a laptop.
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.ndimage import label, generate_binary_structure

# ---------- setup ----------
ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
FIGS = ROOT / "figs"
WORK.mkdir(exist_ok=True)
FIGS.mkdir(exist_ok=True)

RESULTS_PATH = WORK / "results.json"


def save_results(results):
    tmp = RESULTS_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    tmp.replace(RESULTS_PATH)


results = {
    "paper": "Tikhonov et al., arXiv:2204.05000",
    "scope": "GL/TDGL theory-only replication of the branching-network mechanism (2D uniaxial).",
    "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "params": {},
    "runs": {},
    "claims": {},
    "notes": [],
}
save_results(results)


# ---------- physics parameters (dimensionless units) ----------
Nx, Nz = 96, 96
dx = 1.0
dz = 1.0

a = -1.0          # double-well: -1 favors |P|=1
b = 1.0
kx = 0.3          # gradient stiffness across x (perp to polar axis) -- SOFT
kz = 1.5          # gradient stiffness along z (polar axis)     -- STIFF
                  # kz >> kx  =>  walls perpendicular to z are expensive,
                  # walls parallel to z are cheap. This is the uniaxial
                  # anisotropy of PGO: it makes SIMPLE H-H walls (which sit
                  # perpendicular to z) energetically penalized on top of
                  # the electrostatic penalty. To avoid both, the system
                  # branches.
lambda_es = 1.5   # bound-charge penalty; competes with Landau/gradient.

dt = 0.04
n_steps = 5000    # matched across all three runs for a fair comparison
n_steps_hh = 5000
report_every = 500

RNG = np.random.default_rng(20260718)

results["params"] = {
    "grid": [Nx, Nz],
    "dx": dx, "dz": dz,
    "a": a, "b": b, "kx": kx, "kz": kz, "lambda_es": lambda_es,
    "dt": dt, "n_steps": n_steps, "seed": 20260718,
}
save_results(results)


# ---------- differential operators (Neumann BC via edge replicate) ----------
def d_dz(P):
    # central difference along axis=1 (z), Neumann via edge padding
    Pp = np.pad(P, ((0, 0), (1, 1)), mode="edge")
    return (Pp[:, 2:] - Pp[:, :-2]) / (2 * dz)


def d_dx(P):
    Pp = np.pad(P, ((1, 1), (0, 0)), mode="edge")
    return (Pp[2:, :] - Pp[:-2, :]) / (2 * dx)


def laplacian_aniso(P):
    Ppx = np.pad(P, ((1, 1), (0, 0)), mode="edge")
    Ppz = np.pad(P, ((0, 0), (1, 1)), mode="edge")
    d2x = (Ppx[2:, :] - 2 * P + Ppx[:-2, :]) / (dx * dx)
    d2z = (Ppz[:, 2:] - 2 * P + Ppz[:, :-2]) / (dz * dz)
    return kx * d2x + kz * d2z


def bound_charge(P):
    # rho_b = -dPz/dz  (2D scalar polarization along z)
    return -d_dz(P)


def electrostatic_penalty_force(P):
    # E_es = (lambda_es/2) * integral (dP/dz)^2 dV
    # delta E_es / delta P = -lambda_es * d^2 P / dz^2
    Ppz = np.pad(P, ((0, 0), (1, 1)), mode="edge")
    d2z = (Ppz[:, 2:] - 2 * P + Ppz[:, :-2]) / (dz * dz)
    return -lambda_es * d2z


def free_energy(P):
    landau = 0.5 * a * P**2 + 0.25 * b * P**4
    dPx = d_dx(P)
    dPz = d_dz(P)
    grad = 0.5 * kx * dPx**2 + 0.5 * kz * dPz**2
    es = 0.5 * lambda_es * dPz**2  # == 0.5 * lambda_es * rho_b^2 (up to sign)
    return {
        "F_landau": float(np.sum(landau) * dx * dz),
        "F_grad": float(np.sum(grad) * dx * dz),
        "F_es": float(np.sum(es) * dx * dz),
        "F_total": float(np.sum(landau + grad + es) * dx * dz),
    }


def tdgl_step(P):
    # dP/dt = -a P - b P^3 + laplacian_aniso - electrostatic_force_derivative
    dF_dP = a * P + b * P**3 - laplacian_aniso(P) - (-electrostatic_penalty_force(P))
    # electrostatic force term was -lambda*d2z, its contribution to -dF/dP is +lambda*d2z
    # (already sign-consistent above)
    return P - dt * dF_dP


# ---------- run helper ----------
def relax(P0, n_steps, tag):
    P = P0.copy()
    energy_trace = []
    for step in range(n_steps):
        P = tdgl_step(P)
        # clamp to avoid rare blow-up
        np.clip(P, -3.0, 3.0, out=P)
        if step % report_every == 0 or step == n_steps - 1:
            E = free_energy(P)
            energy_trace.append({"step": step, **E})
            print(f"[{tag}] step={step:5d} F_total={E['F_total']:.3f} "
                  f"F_es={E['F_es']:.3f} F_grad={E['F_grad']:.3f}")
            # incremental save
            results["runs"].setdefault(tag, {})["energy_trace"] = energy_trace
            save_results(results)
    return P, energy_trace


# ---------- CLAIM 1: branching network from noisy IC ----------
print("=== CLAIM 1: relax from noisy initial condition ===")
t0 = time.time()
P_init_noisy = 0.05 * RNG.standard_normal((Nx, Nz))
P_network, trace_network = relax(P_init_noisy, n_steps, "network")
print(f"[network] wall clock {time.time()-t0:.1f} s")

# ---------- reference A: parallel stripes (nucleated) ----------
# Uncharged 180-degree walls: stripes run ALONG the polar axis z, so Pz
# alternates sign in x. rho_b = -dPz/dz = 0 identically (up to tiny noise
# derivatives) -> this reference has essentially ZERO electrostatic energy
# by construction. It is the RIGHT topological benchmark for branching
# ("can the noisy system nontrivially deviate from clean parallel walls?")
# but is NOT the right reference for CLAIM 2 (electrostatic comparison);
# for that we use the H-H reference below.
print("=== reference A: parallel stripes ===")
t0 = time.time()
P_init_stripes = np.zeros((Nx, Nz))
stripe_w = Nx // 4
for i in range(4):
    sign = 1.0 if (i % 2 == 0) else -1.0
    P_init_stripes[i * stripe_w:(i + 1) * stripe_w, :] = sign
P_init_stripes += 0.01 * RNG.standard_normal((Nx, Nz))
P_stripes, trace_stripes = relax(P_init_stripes, n_steps, "stripes")
print(f"[stripes] wall clock {time.time()-t0:.1f} s")

# ---------- reference B: naive charged H-H wall ----------
print("=== reference B: naive H-H charged wall (frozen) ===")
# Upper half Pz = +1, lower half Pz = -1: single flat H-H wall across the middle.
# Relax briefly so the wall picks a physical profile, but the topology (single
# H-H sheet) is preserved.
P_init_hh = np.ones((Nx, Nz))
P_init_hh[:, : Nz // 2] = -1.0
P_init_hh += 0.005 * RNG.standard_normal((Nx, Nz))
# short relaxation so wall thickness relaxes but geometry stays
P_hh, trace_hh = relax(P_init_hh, n_steps_hh, "hh_wall")
E_hh = free_energy(P_hh)

# ---------- measurements ----------
# ----- pure-numpy Zhang-Suen thinning (skeletonize) -----
def _zhang_suen(img):
    """Zhang-Suen binary thinning. img: 2D bool. Returns 2D bool skeleton."""
    img = img.astype(np.uint8).copy()
    changed = True
    H, W = img.shape
    while changed:
        changed = False
        for sub in (0, 1):
            to_del = []
            for i in range(1, H - 1):
                for j in range(1, W - 1):
                    if img[i, j] != 1:
                        continue
                    p2 = img[i-1, j];   p3 = img[i-1, j+1]
                    p4 = img[i,   j+1]; p5 = img[i+1, j+1]
                    p6 = img[i+1, j];   p7 = img[i+1, j-1]
                    p8 = img[i,   j-1]; p9 = img[i-1, j-1]
                    B = p2+p3+p4+p5+p6+p7+p8+p9
                    if B < 2 or B > 6:
                        continue
                    seq = [p2,p3,p4,p5,p6,p7,p8,p9,p2]
                    A = sum(1 for k in range(8) if seq[k] == 0 and seq[k+1] == 1)
                    if A != 1:
                        continue
                    if sub == 0:
                        if p2*p4*p6 != 0: continue
                        if p4*p6*p8 != 0: continue
                    else:
                        if p2*p4*p8 != 0: continue
                        if p2*p6*p8 != 0: continue
                    to_del.append((i, j))
            if to_del:
                changed = True
                for i, j in to_del:
                    img[i, j] = 0
    return img.astype(bool)


def domain_junctions(P):
    """
    Skeletonize the domain-wall network, then count TRUE topological
    junctions (skeleton pixels with >=3 skeleton neighbors) and endpoints.

    Reports:
      n_junctions_skel     -- skeleton branch points (network branching)
      n_endpoints_skel     -- skeleton endpoints (loose ends)
      n_skel_pixels        -- skeleton length (proxy for total wall length)
      n_wall_pixels        -- raw wall pixels
      wall_frac            -- wall_pixels / N (network density)
      n_up/down_components -- connected-component count of up/down domains
    """
    from scipy.ndimage import convolve
    S = np.sign(P).astype(np.int8)
    wall = np.zeros(S.shape, dtype=bool)
    wall[:-1, :] |= S[:-1, :] != S[1:, :]
    wall[1:, :]  |= S[1:, :]  != S[:-1, :]
    wall[:, :-1] |= S[:, :-1] != S[:, 1:]
    wall[:, 1:]  |= S[:, 1:]  != S[:, :-1]

    skel = _zhang_suen(wall)

    kernel = np.ones((3, 3), dtype=int); kernel[1, 1] = 0
    neigh_skel = convolve(skel.astype(int), kernel, mode="constant", cval=0)
    junction_mask = skel & (neigh_skel >= 3)
    endpoint_mask = skel & (neigh_skel == 1)

    struct = generate_binary_structure(2, 1)
    _, n_up = label(S > 0, structure=struct)
    _, n_dn = label(S < 0, structure=struct)
    return {
        "n_junctions_skel": int(junction_mask.sum()),
        "n_endpoints_skel": int(endpoint_mask.sum()),
        "n_wall_pixels":    int(wall.sum()),
        "n_skel_pixels":    int(skel.sum()),
        "wall_frac":        float(wall.mean()),
        "n_up_components":  int(n_up),
        "n_down_components": int(n_dn),
    }


metrics_network = domain_junctions(P_network)
metrics_stripes = domain_junctions(P_stripes)
metrics_hh = domain_junctions(P_hh)

E_network = free_energy(P_network)
E_stripes = free_energy(P_stripes)

# integrated |rho_b| and rho_b^2
def charge_stats(P):
    rb = bound_charge(P)
    return {
        "int_abs_rho": float(np.sum(np.abs(rb)) * dx * dz),
        "int_rho2":    float(np.sum(rb * rb) * dx * dz),
        "max_abs_rho": float(np.max(np.abs(rb))),
    }

cs_net = charge_stats(P_network)
cs_str = charge_stats(P_stripes)
cs_hh  = charge_stats(P_hh)

results["runs"]["network"]["metrics"] = metrics_network
results["runs"]["network"]["energy"] = E_network
results["runs"]["network"]["charge"] = cs_net
results["runs"]["stripes"]["metrics"] = metrics_stripes
results["runs"]["stripes"]["energy"] = E_stripes
results["runs"]["stripes"]["charge"] = cs_str
results["runs"]["hh_wall"]["metrics"] = metrics_hh
results["runs"]["hh_wall"]["energy"] = E_hh
results["runs"]["hh_wall"]["charge"] = cs_hh

# ---------- claim scoring ----------
# CLAIM 1: branching network -> many skeleton junctions AND many domain
# components (the ferro state fragments into many entwined patches), while
# parallel stripes have essentially 0 skeleton branch points and exactly
# 4 components (by construction). We require BOTH more junctions AND more
# components in the network. n_junctions_skel is the primary diagnostic
# for branching (topological), n_components is the secondary diagnostic
# for fragmentation.
n_comp_net = metrics_network["n_up_components"] + metrics_network["n_down_components"]
n_comp_str = metrics_stripes["n_up_components"] + metrics_stripes["n_down_components"]
c1_pass = (
    metrics_network["n_junctions_skel"] >= 10
    and metrics_network["n_junctions_skel"] > 2 * max(1, metrics_stripes["n_junctions_skel"])
    and n_comp_net > n_comp_str
)

# CLAIM 2: relaxed network E_es < naive H-H wall E_es AND relaxed network int_rho2 < H-H int_rho2
c2_pass = (E_network["F_es"] < E_hh["F_es"]) and (cs_net["int_rho2"] < cs_hh["int_rho2"])

results["claims"] = {
    "claim1_branching_vs_stripes": {
        "pass": bool(c1_pass),
        "n_junctions_skel_network": metrics_network["n_junctions_skel"],
        "n_junctions_skel_stripes": metrics_stripes["n_junctions_skel"],
        "n_endpoints_skel_network": metrics_network["n_endpoints_skel"],
        "n_endpoints_skel_stripes": metrics_stripes["n_endpoints_skel"],
        "wall_frac_network":        metrics_network["wall_frac"],
        "wall_frac_stripes":        metrics_stripes["wall_frac"],
        "n_components_network": metrics_network["n_up_components"] + metrics_network["n_down_components"],
        "n_components_stripes": metrics_stripes["n_up_components"] + metrics_stripes["n_down_components"],
    },
    "claim2_entwining_lowers_charge": {
        "pass": bool(c2_pass),
        "F_es_network": E_network["F_es"],
        "F_es_hh_wall": E_hh["F_es"],
        "int_rho2_network": cs_net["int_rho2"],
        "int_rho2_hh_wall": cs_hh["int_rho2"],
        "F_es_ratio_network_over_hh": E_network["F_es"] / max(1e-9, E_hh["F_es"]),
    },
}
save_results(results)

# ---------- figures ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def _imshow(ax, A, title, cmap="RdBu_r", vmin=None, vmax=None):
    im = ax.imshow(A.T, origin="lower", cmap=cmap, vmin=vmin, vmax=vmax,
                   interpolation="nearest", aspect="equal")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("x"); ax.set_ylabel("z")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

# Fig 1: domain network vs stripes vs H-H
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
_imshow(axes[0], P_network, "CLAIM 1: relaxed network Pz\n(from noisy IC)", vmin=-1.2, vmax=1.2)
_imshow(axes[1], P_stripes, "reference: parallel stripes Pz", vmin=-1.2, vmax=1.2)
_imshow(axes[2], P_hh,      "reference: naive H-H wall Pz",   vmin=-1.2, vmax=1.2)
plt.tight_layout()
fig.savefig(FIGS / "fig1_domain_network.png", dpi=140)
plt.close(fig)

# Fig 2: bound charge maps
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
rb_net = bound_charge(P_network)
rb_str = bound_charge(P_stripes)
rb_hh  = bound_charge(P_hh)
vmax = max(np.abs(rb_net).max(), np.abs(rb_str).max(), np.abs(rb_hh).max())
_imshow(axes[0], rb_net, "network: rho_b = -dPz/dz",    cmap="PiYG", vmin=-vmax, vmax=vmax)
_imshow(axes[1], rb_str, "stripes: rho_b",               cmap="PiYG", vmin=-vmax, vmax=vmax)
_imshow(axes[2], rb_hh,  "naive H-H wall: rho_b",        cmap="PiYG", vmin=-vmax, vmax=vmax)
plt.tight_layout()
fig.savefig(FIGS / "fig2_bound_charge.png", dpi=140)
plt.close(fig)

# Fig 3: energy comparison bar chart
fig, ax = plt.subplots(1, 1, figsize=(7, 4.5))
labels = ["relaxed\nnetwork", "parallel\nstripes", "naive\nH-H wall"]
Fes  = [E_network["F_es"],     E_stripes["F_es"],     E_hh["F_es"]]
Ftot = [E_network["F_total"],  E_stripes["F_total"],  E_hh["F_total"]]
x = np.arange(len(labels))
w = 0.35
ax.bar(x - w/2, Fes, w, label="F_electrostatic")
ax.bar(x + w/2, Ftot, w, label="F_total")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("free energy (dimensionless)")
ax.set_title("CLAIM 2: relaxed network lowers electrostatic energy vs naive H-H wall")
ax.legend()
plt.tight_layout()
fig.savefig(FIGS / "fig3_energy_comparison.png", dpi=140)
plt.close(fig)

# Fig 4: energy traces
fig, ax = plt.subplots(1, 1, figsize=(7, 4.5))
for tag, tr in [("network", trace_network), ("stripes", trace_stripes), ("hh_wall", trace_hh)]:
    steps = [d["step"] for d in tr]
    Ft    = [d["F_total"] for d in tr]
    ax.plot(steps, Ft, marker="o", label=f"{tag}: F_total")
ax.set_xlabel("TDGL step"); ax.set_ylabel("F_total")
ax.set_title("TDGL relaxation traces")
ax.legend()
plt.tight_layout()
fig.savefig(FIGS / "fig4_energy_traces.png", dpi=140)
plt.close(fig)

results["figures"] = [
    "figs/fig1_domain_network.png",
    "figs/fig2_bound_charge.png",
    "figs/fig3_energy_comparison.png",
    "figs/fig4_energy_traces.png",
]
results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# verdict
if c1_pass and c2_pass:
    verdict = "PARTIAL_STRONG"
elif c1_pass and not c2_pass:
    verdict = "PARTIAL_CLAIM1_ONLY"
elif (not c1_pass) and c2_pass:
    verdict = "PARTIAL_CLAIM2_ONLY"
else:
    verdict = "FAIL"
results["verdict"] = verdict

save_results(results)

print("\n=== SUMMARY ===")
print(json.dumps(results["claims"], indent=2))
print("verdict:", verdict)
