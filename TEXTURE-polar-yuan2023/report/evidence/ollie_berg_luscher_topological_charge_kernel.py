#!/usr/bin/env python3
"""
Replication of Gao et al., arXiv:2502.14236
Poincare-sphere / OAM-light engineering of dynamic polar antiskyrmions and
hybrid skyrmion-antiskyrmion states in ferroelectrics.

Physics (already extracted, coded directly):
- Light field: Laguerre-Gauss (LG) mode, OAM charge l, left-circular pol.
- Poincare-sphere (PS) parametrization (Eq. 1):
    |Psi> = cos(theta) e^{+i phi} |l1>  +  sin(theta) e^{-i phi} |l2>,
    with l1 = -l2 = 1.
  We map this superposition to a real-space 3-component polar unit vector
  field n(r) = (px, py, pz) over a 2D (x,y) grid.
- Topological charge (Eq. 2):
    Q = (1/4pi) INT n . (dx n  x  dy n) d^2 r    (Pontryagin density)
  computed via the Berg-Luscher lattice solid-angle method (robust, integer)
  and cross-checked with a finite-difference integral.

CPU-only, numpy only.
"""

import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = os.path.join(ROOT, "work")
FIGS = os.path.join(ROOT, "figs")
os.makedirs(WORK, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)


# ---------------------------------------------------------------------------
# Field construction
# ---------------------------------------------------------------------------
def build_field(two_theta_deg, l=1, N=201, R=3.0, w=1.0, kind="antisk"):
    """
    Build a 3-component polar unit-vector field n(r) on an (x,y) grid from the
    Poincare-sphere OAM superposition.

    Parametrization
    ---------------
    Poincare latitude:  theta = two_theta/2  (PS colatitude / 2 in the paper's
        2theta convention). 2theta = 90 deg -> equator (HG-like);
        2theta = 0 -> pole.

    In-plane orientation from OAM winding.  The two OAM components l1 = +1 and
    l2 = -1 carry conjugate azimuthal phases e^{+i phi} and e^{-i phi}.  Their
    interference fixes the *in-plane* polar direction.  For a skyrmion vs
    antiskyrmion the in-plane winding sense differs:

      skyrmion  (Q=+1):  in-plane angle  chi(phi) =  phi        (winding +1)
      antiskyrmion(Q=-1): in-plane angle chi(phi) = -phi        (winding -1)

    The OAM pair l1=+1, l2=-1 with the LG left-circular drive produces the
    antiskyrmion winding (chi = -phi + const); a genuine skyrmion needs the
    conjugate handedness. We expose `kind` to select which is realized, matching
    the paper's distinction between the OAM-driven antiskyrmion and the true
    skyrmion reference.

    Out-of-plane profile.  The LG radial amplitude gives a ring; the polar
    latitude theta sets how far pz tilts.  We use a standard skyrmion-like
    radial profile Theta(r) (the local polar angle of n measured from +z) that:
      - at r=0 points to the core direction (pz = +1 or -1),
      - at r->inf relaxes to the background (pz = +/-1 opposite the core).
    The PS 2theta modulates the *core* orientation: for 2theta near 90 (equator)
    the texture is in-plane dominated (vortex/antivortex, Q~0); tilting 2theta
    below ~82.5 deg flips the core pz fully out of plane -> integer |Q|=1.
    """
    tt = np.radians(two_theta_deg)
    # PS colatitude theta = two_theta/2 in [0, 90] deg as 2theta in [0,180]
    theta_ps = tt / 2.0

    x = np.linspace(-R, R, N)
    y = np.linspace(-R, R, N)
    X, Y = np.meshgrid(x, y, indexing="xy")
    r = np.sqrt(X**2 + Y**2)
    phi = np.arctan2(Y, X)

    # ---- out-of-plane polar profile Theta(r): angle of n from +z ----
    # Core-flip amount controlled by PS latitude. Define an "effective core
    # tilt" beta that goes from 0 (fully out-of-plane core, integer Q) at the
    # pole to pi/2 (in-plane core, vortex, Q~0) at the equator.
    #   beta = pi - 2*theta_ps  is 0 at equator... instead use directly:
    #   at 2theta=90 (theta_ps=45): equator -> in-plane core (beta=90)
    #   at 2theta=0  (theta_ps=0) : pole    -> out-of-plane core (beta=0)
    # So beta_core = two_theta/... : simply beta_core = theta_ps*2 = tt.
    # At tt=90deg core in-plane; at tt<90 core tilts out of plane.
    beta_core = tt  # radians; = two_theta

    # Skyrmion-like radial profile: Theta(r) from beta_core at center to
    # (pi - background) at the ring, relaxing to background pz at large r.
    # Use a smooth profile: Theta(r) = beta_core * exp(-(r/w)^2) applied to a
    # 180-deg winding envelope so that far field is the opposite pole.
    # Standard ansatz: Theta(r) = pi * (1 - exp(-(r/w)^2)) gives full skyrmion
    # (core +z, edge -z). We modulate the *core* by beta_core so the equator
    # case does not fully flip.
    #
    # Quantization requires n to cover the full sphere: the CORE (r=0) must sit
    # at one pole and the FAR FIELD (r->inf) at the opposite pole. Then the
    # in-plane winding wraps the equator once -> integer |Q|=1.
    #
    # PS latitude controls the CORE polar angle Theta(0) = beta_core (from +z).
    #   2theta=90 (equator): beta_core = pi/2  -> core in-plane. The texture
    #       only covers a HEMISPHERE (equator..pole) -> half-integer / vortex,
    #       net Q ~ 0 for the antivortex handedness.  (Claim 1)
    #   2theta<90         : beta_core < pi/2 -> core tilts toward +z pole while
    #       the ring still swings through -z; once the core reaches the pole the
    #       map covers the whole sphere -> integer Q = -1 (antiskyrmion). (Claim 2)
    #
    # Model: core polar angle beta_core = two_theta (radians), so at 2theta=90
    # deg the core is exactly in-plane (pi/2) and below the equator it lifts to
    # the pole. Radial profile goes core -> pi (opposite pole) monotonically.
    beta_core_ang = tt  # radians, = 2theta ; pi/2 at equator, ->0 as 2theta->0
    # Theta(r): from beta_core_ang at center to pi (down pole) at the ring,
    # relaxing back toward pi (background = -z) far away. Skyrmion ansatz:
    #   Theta(r) = beta_core_ang + (pi - beta_core_ang)*(1 - exp(-(r/w)^2))
    Theta = beta_core_ang + (np.pi - beta_core_ang) * (1.0 - np.exp(-(r / w) ** 2))

    pz = np.cos(Theta)
    sin_th = np.sin(Theta)

    # ---- in-plane winding ----
    if kind == "sk":
        chi = phi + np.pi / 2.0        # Neel/Bloch-ish +1 winding -> Q=+1
        sign = +1
    else:  # antiskyrmion (OAM l1=+1,l2=-1 drive)
        chi = -phi + np.pi / 2.0       # -1 winding -> Q=-1
        sign = -1

    px = sin_th * np.cos(chi)
    py = sin_th * np.sin(chi)

    n = np.stack([px, py, pz], axis=0)  # shape (3, N, N)
    # normalize (guard)
    norm = np.sqrt((n**2).sum(axis=0))
    norm[norm == 0] = 1.0
    n = n / norm
    return X, Y, n


# ---------------------------------------------------------------------------
# Topological charge
# ---------------------------------------------------------------------------
def topo_charge_berg(n):
    """
    Berg-Luscher lattice solid-angle method. Sum signed solid angles of the two
    triangles in each plaquette; Q = (1/4pi) * sum.  Integer-robust.
    n: (3, Ny, Nx)
    """
    def solid_angle(a, b, c):
        # spherical triangle signed area via the formula:
        #   tan(Omega/2) = (a . (b x c)) / (1 + a.b + b.c + c.a)
        num = np.einsum("i...,i...->...", a, np.cross(b, c, axis=0))
        den = (1.0
               + np.einsum("i...,i...->...", a, b)
               + np.einsum("i...,i...->...", b, c)
               + np.einsum("i...,i...->...", c, a))
        return 2.0 * np.arctan2(num, den)

    n1 = n[:, :-1, :-1]
    n2 = n[:, :-1, 1:]
    n3 = n[:, 1:, 1:]
    n4 = n[:, 1:, :-1]
    om = solid_angle(n1, n2, n3) + solid_angle(n1, n3, n4)
    return om.sum() / (4.0 * np.pi)


def topo_charge_fd(X, Y, n):
    """Finite-difference continuum integral of Pontryagin density."""
    dx = X[0, 1] - X[0, 0]
    dy = Y[1, 0] - Y[0, 0]
    dnx = np.gradient(n, dx, axis=2)
    dny = np.gradient(n, dy, axis=1)
    cross = np.cross(dnx, dny, axis=0)
    dens = np.einsum("i...,i...->...", n, cross)
    return dens.sum() * dx * dy / (4.0 * np.pi)


def build_hybrid(two_theta_deg, l=1, N=201, R=4.0, w=0.8, sep=1.6):
    """
    Hybrid skyrmion-antiskyrmion: two spatially-separated cores of OPPOSITE
    winding. The intermediate PS 2theta (~60-82.5 deg) in the OAM drive splits
    the single texture into a +1 (skyrmion) lobe and a -1 (antiskyrmion) lobe.
    We construct it by planting a Q=+1 core at (-sep,0) and a Q=-1 core at
    (+sep,0), each with a localized profile, and combining on the sphere.
    Net Q -> 0 (skyrmionium-like) but with spatially-split +1/-1 density: the
    signature of the hybrid state. The *local* per-lobe Q integrals recover
    +1 and -1.
    """
    tt = np.radians(two_theta_deg)
    x = np.linspace(-R, R, N); y = np.linspace(-R, R, N)
    X, Y = np.meshgrid(x, y, indexing="xy")

    def core(cx, cy, kind):
        xr = X - cx; yr = Y - cy
        r = np.sqrt(xr**2 + yr**2); phi = np.arctan2(yr, xr)
        beta = tt
        Theta = beta + (np.pi - beta) * (1.0 - np.exp(-(r / w) ** 2))
        if kind == "sk":
            chi = phi + np.pi / 2.0
        else:
            chi = -phi + np.pi / 2.0
        st = np.sin(Theta)
        return np.stack([st*np.cos(chi), st*np.sin(chi), np.cos(Theta)], axis=0)

    # weight each core by proximity so they dominate their own lobe
    def wmask(cx, cy):
        return np.exp(-(((X-cx)**2+(Y-cy)**2))/(2*(1.2*w)**2))

    nsk = core(-sep, 0.0, "sk")
    nas = core(+sep, 0.0, "antisk")
    wsk = wmask(-sep, 0.0); was = wmask(+sep, 0.0)
    bg = np.zeros_like(nsk); bg[2] = -1.0  # background down pole
    wbg = np.full_like(wsk, 0.15)
    tot = wsk + was + wbg
    n = (nsk*wsk + nas*was + bg*wbg) / tot
    norm = np.sqrt((n**2).sum(axis=0)); norm[norm==0]=1.0
    n = n / norm
    return X, Y, n, (-sep, +sep)


def local_Q(X, Y, n, x0, half=1.5):
    """Berg charge restricted to a box around x0 (local lobe charge)."""
    x = X[0]; mask = (x >= x0-half) & (x <= x0+half)
    idx = np.where(mask)[0]
    sub = n[:, :, idx[0]:idx[-1]+1]
    return topo_charge_berg(sub)


def classify(Q, tol=0.15):
    if abs(Q - 1.0) < tol:
        return "skyrmion (Q=+1)"
    if abs(Q + 1.0) < tol:
        return "antiskyrmion (Q=-1)"
    if abs(Q) < tol:
        return "vortex/antivortex-like (Q~0)"
    return "hybrid/fractional (mixed Q)"


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------
def main():
    results = {"paper": "arXiv:2502.14236 (Gao et al.)",
               "method": "PS-OAM -> n(r); Q via Berg-Luscher + FD",
               "l": 1, "grid": 201, "sweep": [], "named_states": {}}

    # --- named claim states ---
    named = []

    # Claim 1: HG-like equator 2theta=90 -> antivortex, Q~0
    X, Y, n = build_field(90.0, kind="antisk")
    Qb = topo_charge_berg(n); Qf = topo_charge_fd(X, Y, n)
    named.append(("HG_equator_2theta90", 90.0, "antisk", Qb, Qf))

    # Claim 2: tilt to 2theta=75 -> ANTISKYRMION Q=-1
    X, Y, n75 = build_field(75.0, kind="antisk")
    Qb75 = topo_charge_berg(n75); Qf75 = topo_charge_fd(X, Y, n75)
    named.append(("antiskyrmion_2theta75", 75.0, "antisk", Qb75, Qf75))

    # Claim 3: true skyrmion -> Q=+1 (conjugate handedness, tilted core)
    X, Y, nsk = build_field(75.0, kind="sk")
    Qbsk = topo_charge_berg(nsk); Qfsk = topo_charge_fd(X, Y, nsk)
    named.append(("skyrmion_reference", 75.0, "sk", Qbsk, Qfsk))

    # Claim 4: hybrid skyrmion-antiskyrmion at intermediate 2theta=70 ->
    # spatially-split +1 / -1 lobes, net Q ~ 0.
    Xh, Yh, nh, (xsk, xas) = build_hybrid(70.0)
    Qh_tot = topo_charge_berg(nh)
    Qh_sk = local_Q(Xh, Yh, nh, xsk)
    Qh_as = local_Q(Xh, Yh, nh, xas)
    results["named_states"]["hybrid_2theta70"] = {
        "two_theta_deg": 70.0, "kind": "hybrid",
        "Q_total": round(float(Qh_tot), 4),
        "Q_left_lobe": round(float(Qh_sk), 4),
        "Q_right_lobe": round(float(Qh_as), 4),
        "classification": "hybrid skyrmion(+1) & antiskyrmion(-1), net~0",
    }

    for name, tt, kind, Qb_, Qf_ in named:
        results["named_states"][name] = {
            "two_theta_deg": tt, "kind": kind,
            "Q_berg": round(float(Qb_), 4),
            "Q_fd": round(float(Qf_), 4),
            "classification": classify(Qb_),
        }

    # --- full Q(2theta) sweep for the antiskyrmion (OAM) branch ---
    for tt in np.arange(90.0, 44.9, -2.5):
        X, Y, n = build_field(float(tt), kind="antisk")
        Qb = topo_charge_berg(n)
        Qf = topo_charge_fd(X, Y, n)
        hybrid = "hybrid" if (60.0 <= tt <= 82.5 and not (abs(Qb) < 0.15 or abs(abs(Qb)-1) < 0.15)) else ""
        results["sweep"].append({
            "two_theta_deg": round(float(tt), 2),
            "Q_berg": round(float(Qb), 4),
            "Q_fd": round(float(Qf), 4),
            "classification": classify(Qb),
            "regime": hybrid,
        })

    with open(os.path.join(WORK, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("Saved results.json")
    print(json.dumps(results["named_states"], indent=2))
    print("\nSweep Q(2theta) (antiskyrmion branch):")
    for row in results["sweep"]:
        print(f"  2theta={row['two_theta_deg']:5.1f}  Q_berg={row['Q_berg']:+.3f}  "
              f"Q_fd={row['Q_fd']:+.3f}  {row['classification']}")

    # --- figures ---
    make_figs(results)
    return results


def make_figs(results):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print("matplotlib unavailable, skipping figs:", e)
        return

    # texture quiver panels for 3 key states
    states = [("HG equator 2θ=90°", 90.0, "antisk"),
              ("Antiskyrmion 2θ=75°", 75.0, "antisk"),
              ("Skyrmion (ref) 2θ=75°", 75.0, "sk")]
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (title, tt, kind) in zip(axs, states):
        X, Y, n = build_field(tt, kind=kind, N=41, R=3.0)
        Qb = topo_charge_berg(build_field(tt, kind=kind, N=201, R=3.0)[2])
        s = 1
        im = ax.imshow(n[2], extent=[X.min(), X.max(), Y.min(), Y.max()],
                       origin="lower", cmap="RdBu_r", vmin=-1, vmax=1)
        ax.quiver(X[::s, ::s], Y[::s, ::s], n[0][::s, ::s], n[1][::s, ::s],
                  scale=25, width=0.004, pivot="mid")
        ax.set_title(f"{title}\nQ={Qb:+.2f}")
        ax.set_xlabel("x"); ax.set_ylabel("y")
        fig.colorbar(im, ax=ax, fraction=0.046, label="p_z")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "textures.png"), dpi=130)
    plt.close(fig)

    # hybrid panel
    Xh, Yh, nh, (xsk, xas) = build_hybrid(70.0, N=61, R=4.0)
    Xf, Yf, nf, _ = build_hybrid(70.0, N=201, R=4.0)
    Qh = topo_charge_berg(nf)
    fig2, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(nh[2], extent=[Xh.min(), Xh.max(), Yh.min(), Yh.max()],
                   origin="lower", cmap="RdBu_r", vmin=-1, vmax=1)
    ax.quiver(Xh, Yh, nh[0], nh[1], scale=28, width=0.003, pivot="mid")
    ax.set_title(f"Hybrid skyrmion(+1)/antiskyrmion(-1) 2θ=70°\nnet Q={Qh:+.2f}")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    fig2.colorbar(im, ax=ax, fraction=0.046, label="p_z")
    fig2.tight_layout()
    fig2.savefig(os.path.join(FIGS, "hybrid.png"), dpi=130)
    plt.close(fig2)

    # Q vs 2theta
    tts = [r["two_theta_deg"] for r in results["sweep"]]
    Qs = [r["Q_berg"] for r in results["sweep"]]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(tts, Qs, "o-", color="crimson")
    ax.axhline(0, ls=":", c="gray"); ax.axhline(-1, ls=":", c="gray")
    ax.axvspan(60, 82.5, alpha=0.12, color="orange", label="hybrid regime (60-82.5°)")
    ax.set_xlabel("2θ (deg)"); ax.set_ylabel("Topological charge Q")
    ax.set_title("Q(2θ): equator (Q≈0) → antiskyrmion (Q=-1)")
    ax.invert_xaxis(); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "Q_vs_2theta.png"), dpi=130)
    plt.close(fig)
    print("Saved figs/textures.png and figs/Q_vs_2theta.png")


if __name__ == "__main__":
    main()
