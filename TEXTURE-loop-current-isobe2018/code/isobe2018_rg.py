"""
isobe2018_rg.py
=====================================================================
Replication core for

    H. Isobe, N. F. Q. Yuan, L. Fu,
    "Unconventional Superconductivity and Density Waves in Twisted
     Bilayer Graphene", Phys. Rev. X 8, 041041 (2018);
     arXiv:1805.06449.

SCOPE NOTE / KERNEL PROVENANCE
------------------------------
The TEXTURES-100 shared kernel
    ~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py
is a *kagome tight-binding + Peierls-flux loop-current* kernel built for
Fernandes-Birol-Ye-Vanderbilt arXiv:2502.16657. Isobe-Yuan-Fu 2018 is a
DIFFERENT class of physics: a **hot-spot patch renormalization-group (RG)
model** for twisted bilayer graphene near the n=2 Van Hove filling. It has
NO tight-binding lattice, NO Peierls flux, NO Berry curvature/Chern number.
The kagome Bloch Hamiltonian / Chern machinery of the shared kernel is
therefore OUT OF SCOPE and is NOT reused here.

What IS shared in spirit (and cited) with the kernel is only the very high
level "density-wave / ordering-instability selection from interaction
couplings" idea. The kernel's `patch_leading_channel()` is a symbolic
patch-model channel selector (Box 2 of the Fernandes paper); Isobe uses a
quantitatively different 9-coupling one-loop RG. We re-implement the actual
in-scope core: the RG flow equations (9)-(15), the interaction-strength
formulas (17)-(23), and the RPA susceptibility divergence (16),(24).

This module runs REAL numerical RG integration; all reported numbers are
computed, none are transcribed from the paper's figures.
"""
from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Coupling-constant bookkeeping.
# State vector g = [g11,g22,g31,g32,g41,g42,g14,g24,g44]  (9 momentum-conserving)
# ---------------------------------------------------------------------------
IDX = {name: i for i, name in enumerate(
    ["g11", "g22", "g31", "g32", "g41", "g42", "g14", "g24", "g44"])}


def rg_rhs(y, g, d1m, d2m, d3m):
    """Right-hand side of RG equations (9)-(15) of Isobe et al.
    dg/dy where y = chi0- (the Cooper-pair RG scale).

    d1m,d2m,d3m are the nesting parameters d1-, d2-, d3- (assumed constant
    within the nested energy window, as the paper does). da+ neglected (=0).
    """
    g11 = g[IDX["g11"]]; g22 = g[IDX["g22"]]
    g31 = g[IDX["g31"]]; g32 = g[IDX["g32"]]
    g41 = g[IDX["g41"]]; g42 = g[IDX["g42"]]

    dg = np.zeros(9)
    # Eq. (9): intravalley gi4 do not flow
    dg[IDX["g14"]] = 0.0
    dg[IDX["g24"]] = 0.0
    dg[IDX["g44"]] = 0.0
    # Eq. (10)
    dg[IDX["g22"]] = -d3m * (g11**2 + g22**2) + d1m * (g22**2 + g32**2)
    # Eq. (11)
    dg[IDX["g32"]] = -(g31**2 + g32**2 + 2*g31*g41 + 2*g32*g42) + 2*d1m*g22*g32
    # Eq. (12)
    dg[IDX["g42"]] = -(2*g31**2 + 2*g32**2 + g41**2 + g42**2) + d2m*g42**2
    # Eq. (13)
    dg[IDX["g11"]] = (-2*d3m*g11*g22
                      + 2*d1m*(g11*g22 - g11**2 + g31*g32 - g31**2))
    # Eq. (14)
    dg[IDX["g31"]] = (-2*(g31*g32 + g31*g42 + g32*g41)
                      + 2*d1m*(g11*g32 + g22*g31 - 2*g11*g31))
    # Eq. (15)
    dg[IDX["g41"]] = -2*(2*g31*g32 + g41*g42) + 2*d2m*(g41*g42 - g41**2)
    return dg


def interaction_strengths(g):
    """Ordering-channel interaction strengths V_eta, Eqs. (17)-(23).
    A NEGATIVE V_eta (attractive) drives an instability in that channel.
    Returns dict of channel -> V.
    """
    g11 = g[IDX["g11"]]; g22 = g[IDX["g22"]]
    g31 = g[IDX["g31"]]; g32 = g[IDX["g32"]]
    g41 = g[IDX["g41"]]; g42 = g[IDX["g42"]]
    return {
        "s-SC":  2*(g42 + g41 + g32 + g31),   # Eq.17 upper
        "d-SC":  2*(g42 + g41 - g32 - g31),   # Eq.17 lower
        "p-SC":  2*(g42 - g41 - g32 + g31),   # Eq.18 upper
        "f-SC":  2*(g42 - g41 + g32 + g31),   # Eq.18 lower
        "CDW-":  4*(g11 + g31) - 2*(g22 + g32),  # Eq.19
        "CDW0":  4*g41 - 2*g42,                    # Eq.20
        "SDW-":  -2*(g22 + g32),                   # Eq.21
        "SDW0":  -2*g42,                           # Eq.22
        "PDW+":  2*(-g11 + g22),                   # Eq.23
    }


# nesting parameter d_as attached to each channel's bare susceptibility.
# d0- = 1 (BCS, all SC channels); density-wave channels use their d_as.
CHANNEL_D = {
    "s-SC": 1.0, "d-SC": 1.0, "p-SC": 1.0, "f-SC": 1.0,   # d0- = 1
    "CDW-": "d1m", "SDW-": "d1m",     # Q- particle-hole -> d1-
    "CDW0": "d2m", "SDW0": "d2m",     # Q0 particle-hole -> d2-
    "PDW+": "d3m",                    # Q+ particle-particle -> d3-
}


def integrate_rg(g0, d1m, d2m, d3m, y_max=15.0, n=4000):
    """Integrate the RG flow from y=0 to y=y_max (or until a coupling blows up).
    g0: dict or array of initial couplings. Returns (ys, gs[n,9])."""
    if isinstance(g0, dict):
        gvec = np.zeros(9)
        for k, v in g0.items():
            gvec[IDX[k]] = v
    else:
        gvec = np.asarray(g0, float)

    def rhs(y, g):
        return rg_rhs(y, g, d1m, d2m, d3m)

    # stop if any coupling exceeds a large magnitude (strong-coupling breakdown)
    def blowup(y, g):
        return 50.0 - np.max(np.abs(g))
    blowup.terminal = True
    blowup.direction = -1

    sol = solve_ivp(rhs, (0.0, y_max), gvec, t_eval=np.linspace(0, y_max, n),
                    method="RK45", rtol=1e-8, atol=1e-10, events=blowup,
                    max_step=y_max/500)
    return sol.t, sol.y.T


def leading_instability(ys, gs, d1m, d2m, d3m):
    """Given an RG trajectory, find the channel whose RPA susceptibility
    diverges first (smallest critical y_c). Eq. (16)/(24):
        chi_eta(y) = chi0_eta(y) / (1 + V_eta(y) chi0_eta(y)),
    with chi0_eta(y) ~ d_as * y. Divergence when 1 + V_eta*d_as*y -> 0,
    i.e. only possible if V_eta < 0 (attractive). We integrate the running
    of V_eta along the flow and detect the first sign of
        1 + integral-like resummation.
    Practical detector (matches the paper's g0*y_c usage): a channel becomes
    critical when the *running* combination reaches divergence. We use the
    leading-order estimate 1 + V_eta(y)*d_as*y = 0 evaluated with the running
    V_eta(y); the earliest crossing wins.
    Returns (channel, y_c, table) where table maps channel->y_c (or inf).
    """
    dmap = {"d1m": d1m, "d2m": d2m, "d3m": d3m}
    table = {}
    for ch, dtag in CHANNEL_D.items():
        das = dmap[dtag] if isinstance(dtag, str) else dtag
        if das <= 0:
            table[ch] = np.inf
            continue
        yc = np.inf
        for k in range(len(ys)):
            V = interaction_strengths(gs[k])[ch]
            denom = 1.0 + V * das * ys[k]
            if denom <= 0.0:
                yc = ys[k]
                break
        table[ch] = yc
    # winner = smallest finite y_c
    finite = {c: v for c, v in table.items() if np.isfinite(v)}
    if not finite:
        return "normal", np.inf, table
    ch = min(finite, key=finite.get)
    return ch, finite[ch], table
