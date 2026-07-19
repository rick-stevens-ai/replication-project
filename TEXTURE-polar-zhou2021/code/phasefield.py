"""
Reduced 2D phase-field (TDGL) model of polar skyrmion manipulation in a
PbTiO3/SrTiO3 superlattice, following the physics of:

  Zhou, Wu, Das, ... Ramesh, Hong,
  "Local Manipulation and Topological Phase Transitions of Polar Skyrmions"
  arXiv:2104.12990 (2021).

SCOPE / PHILOSOPHY
------------------
The paper solves a full 3D coupled electrostatic + elastic + Landau phase-field
problem on a 320x320x350 mesh with a sixth-order PbTiO3 Landau potential
(Haun 1987 coefficients), an iterative-perturbation elastic solver, and a
superposition electrostatic solver over film + substrate + air. That is a
workstation-scale multiphysics job and is explicitly OUT OF SCOPE for an
independent-replication smoke model.

Instead we build the *tractable core* that reproduces the paper's TOPOLOGICAL
and QUALITATIVE claims:

  * A 3-component polarization field P = (Px, Py, Pz) on a 2D (x,y) grid
    representing the top PTO layer (the plane the paper analyzes for the
    Pontryagin density).
  * A Landau double-well in |P| that favors a fixed spontaneous magnitude Ps,
    plus a gradient (domain-wall / exchange-like) stiffness.
  * A weak easy-axis / anisotropy term and a Dzyaloshinskii-Moriya-like (DMI)
    winding term that stabilizes Neel-type polar skyrmion bubbles -- the
    effective interfacial-inversion-broken analogue of the depolarization +
    gradient competition that makes Neel bubbles in the real superlattice.
  * A local electric field E(x,y) from a top electrode: a downward (-z) Ez
    under the electrode plus a fringing in-plane Ex at the electrode edges
    (the sharp phi: V -> 0 transition the paper stresses).
  * TDGL relaxation dP/dt = -L dF/dP.

Topological charge (Pontryagin / skyrmion number):

    q = (1/4pi) n . (dn/dx x dn/dy),   Q = integral q dx dy

computed on the unit-vector field n = P/|P| by the lattice (Berg-Luscher)
solid-angle method so Q is an exact integer for smooth textures.

This model is deliberately dimensionless (reduced units). It is NOT meant to
reproduce absolute voltages (V), lattice constants, or the exact 650 dielectric
constant -- those require the full multiphysics solve. It IS meant to test the
machine-checkable TOPOLOGICAL claims of the paper.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Topological charge (Berg-Luscher lattice solid angle) -- exact integer for
# smooth fields, robust for skyrmion counting.
# ---------------------------------------------------------------------------
def _solid_angle(n1, n2, n3):
    """Signed solid angle of the spherical triangle (n1,n2,n3), each (...,3)."""
    num = np.einsum('...i,...i->...', n1, np.cross(n2, n3))
    den = (1.0
           + np.einsum('...i,...i->...', n1, n2)
           + np.einsum('...i,...i->...', n2, n3)
           + np.einsum('...i,...i->...', n3, n1))
    return 2.0 * np.arctan2(num, den)


def topological_charge_density(P):
    """
    Berg-Luscher Pontryagin density per plaquette on the unit field n=P/|P|.
    P: (Ny, Nx, 3). Returns q of shape (Ny-1, Nx-1); Q = sum(q)/(4pi).
    """
    mag = np.linalg.norm(P, axis=-1, keepdims=True)
    mag = np.where(mag < 1e-12, 1.0, mag)
    n = P / mag
    n00 = n[:-1, :-1]
    n10 = n[:-1, 1:]
    n11 = n[1:, 1:]
    n01 = n[1:, :-1]
    # two triangles per plaquette
    a = _solid_angle(n00, n10, n11)
    b = _solid_angle(n00, n11, n01)
    return a + b


def topological_charge(P):
    """Integer-valued skyrmion number Q = (1/4pi) sum solid angles."""
    return float(topological_charge_density(P).sum() / (4.0 * np.pi))


def pontryagin_density_continuous(P, dx=1.0, dy=1.0):
    """
    Continuous q = (1/4pi) n . (dn/dx x dn/dy) for plotting line profiles
    (the paper's 'Pontryagin density' maps). Returns (Ny, Nx).
    """
    mag = np.linalg.norm(P, axis=-1, keepdims=True)
    mag = np.where(mag < 1e-12, 1.0, mag)
    n = P / mag
    dnx = np.gradient(n, dx, axis=1)
    dny = np.gradient(n, dy, axis=0)
    cross = np.cross(dnx, dny)
    q = np.einsum('...i,...i->...', n, cross)
    return q / (4.0 * np.pi)


# ---------------------------------------------------------------------------
# Free-energy functional derivative (delta F / delta P) for TDGL.
# ---------------------------------------------------------------------------
def laplacian(f):
    """5-point periodic Laplacian on last-two spatial axes of (Ny,Nx,3)."""
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0)
            + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4.0 * f)


def dmi_field(P):
    """
    Neel-type DMI effective field. Energy density:
      f_DMI = D [ Pz (dPx/dx + dPy/dy) - (Px dPz/dx + Py dPz/dy) ]
    Its functional derivative gives the winding that stabilizes Neel bubbles,
    the reduced analogue of the depolarization+gradient competition in the
    real polar superlattice (paper stresses Neel-component Pontryagin rings).
    """
    Px, Py, Pz = P[..., 0], P[..., 1], P[..., 2]
    dPz_dx = 0.5 * (np.roll(Pz, -1, 1) - np.roll(Pz, 1, 1))
    dPz_dy = 0.5 * (np.roll(Pz, -1, 0) - np.roll(Pz, 1, 0))
    dPx_dx = 0.5 * (np.roll(Px, -1, 1) - np.roll(Px, 1, 1))
    dPy_dy = 0.5 * (np.roll(Py, -1, 0) - np.roll(Py, 1, 0))
    H = np.zeros_like(P)
    # delta f / delta Px, Py, Pz  (from integration by parts)
    H[..., 0] = 2.0 * dPz_dx
    H[..., 1] = 2.0 * dPz_dy
    H[..., 2] = -2.0 * (dPx_dx + dPy_dy)
    return H


def dF_dP(P, params, Efield):
    """
    delta F / delta P for:
      f_land = (a2/2)|P|^2 + (a4/4)|P|^4 + (a6/6)|P|^6   (double/triple-well)
      f_aniso= (Kz/2) (|Pxy|^2 - ... )  easy-plane-ish tuning via Ku on Pz
      f_grad = (G/2) |grad P|^2
      f_DMI  = D (Neel)
      f_elec = -E . P
    """
    a2 = params['a2']; a4 = params['a4']; a6 = params['a6']
    G = params['G']; D = params['D']; Ku = params['Ku']
    mag2 = np.sum(P * P, axis=-1, keepdims=True)
    dland = (a2 + a4 * mag2 + a6 * mag2 * mag2) * P
    dgrad = -G * laplacian(P)
    ddmi = D * dmi_field(P)
    daniso = np.zeros_like(P)
    daniso[..., 2] = Ku * P[..., 2]          # uniaxial along z (out of plane)
    delec = -Efield
    return dland + dgrad + ddmi + daniso + delec


# ---------------------------------------------------------------------------
# Electrode electric field model.
# ---------------------------------------------------------------------------
def electrode_field(Nx, Ny, params, V, d0):
    """
    Build E(x,y) from a top electrode of half-width d0 (in grid units), centred
    in x, running along y. Under the electrode: strong downward Ez (~ -V).
    At the electrode edges: fringing in-plane Ex pointing AWAY from electrode
    (the sharp phi transition), whose sign flips across centre.

    Returns E of shape (Ny, Nx, 3).
    """
    E = np.zeros((Ny, Nx, 3))
    xc = Nx / 2.0
    x = np.arange(Nx)[None, :] - xc          # (1,Nx) centred
    xg = np.broadcast_to(x, (Ny, Nx))
    inside = np.abs(xg) <= d0
    # out-of-plane field under electrode (downward => -z)
    E[..., 2] = np.where(inside, -params['Ez_gain'] * V, 0.0)
    # fringing in-plane field near the two edges, decaying over 'edge_w'
    edge_w = params.get('edge_w', 6.0)
    dist_from_edge = np.abs(xg) - d0         # >0 outside electrode
    fringe = np.exp(-np.clip(dist_from_edge, 0, None)**2 / (2 * edge_w**2))
    fringe = np.where(inside, 0.0, fringe)
    # points away from electrode: +x on right side, -x on left side
    sign = np.sign(xg)
    E[..., 0] = params['Ex_gain'] * V * fringe * sign
    return E


# ---------------------------------------------------------------------------
# Initial condition: lattice of Neel skyrmion bubbles.
# ---------------------------------------------------------------------------
def neel_skyrmion(Nx, Ny, cx, cy, R, Ps, pol=+1, chir=+1):
    """One Neel-type polar skyrmion centred at (cx,cy), radius R, added to grid."""
    y, x = np.mgrid[0:Ny, 0:Nx]
    dx = x - cx; dy = y - cy
    r = np.sqrt(dx * dx + dy * dy)
    r_safe = np.where(r < 1e-9, 1e-9, r)
    # 360-degree profile: core up(pol), rim down, Neel radial in-plane
    theta = np.pi * np.clip(r / R, 0, 1)     # 0 at core -> pi at r=R
    pz = pol * np.cos(theta)
    pin = np.sin(theta)
    px = chir * pin * dx / r_safe
    py = chir * pin * dy / r_safe
    P = np.zeros((Ny, Nx, 3))
    P[..., 0] = px; P[..., 1] = py; P[..., 2] = pz
    # only apply inside r<R (leave background elsewhere)
    mask = r <= R
    return P, mask


def init_skyrmion_lattice(Nx, Ny, spacing, R, Ps, bg_pol=-1):
    """
    Uniform out-of-plane background (c- domain) with a hexagonal-ish lattice of
    up-core Neel skyrmions. Returns P scaled to magnitude ~Ps.
    """
    P = np.zeros((Ny, Nx, 3))
    P[..., 2] = bg_pol                        # background c-domain
    row = 0
    y = spacing // 2
    while y < Ny - spacing // 4:
        offset = (spacing // 2) if (row % 2) else 0
        x = spacing // 2 + offset
        while x < Nx - spacing // 4:
            sky, mask = neel_skyrmion(Nx, Ny, x, y, R, Ps, pol=+1, chir=+1)
            P[mask] = sky[mask]
            x += spacing
        y += int(spacing * 0.87)
        row += 1
    # normalize to spontaneous magnitude
    mag = np.linalg.norm(P, axis=-1, keepdims=True)
    mag = np.where(mag < 1e-9, 1.0, mag)
    P = P / mag * Ps
    return P


# ---------------------------------------------------------------------------
# TDGL integrator.
# ---------------------------------------------------------------------------
def relax(P, params, Efield, nsteps, dt, L, record_every=0, callback=None):
    """
    Semi-implicit-free explicit Euler TDGL: dP/dt = -L dF/dP.
    Returns final P; optional callback(step, P) for logging.
    """
    for step in range(nsteps):
        F = dF_dP(P, params, Efield)
        P = P - L * dt * F
        if record_every and (step % record_every == 0) and callback:
            callback(step, P)
    return P


def default_params():
    return dict(
        a2=-1.0,     # Landau double-well: negative => spontaneous P
        a4=-0.6,     # first-order-ish triple well support
        a6=0.6,      # sixth-order stabilizer (paper: 6th-order Landau)
        G=1.0,       # gradient (domain-wall) stiffness
        D=1.35,      # Neel DMI winding (stabilizes bubbles)
        Ku=0.15,     # uniaxial out-of-plane anisotropy
        Ez_gain=1.0, # electrode out-of-plane field gain per unit V
        Ex_gain=0.9, # fringing in-plane field gain per unit V
        edge_w=6.0,  # fringe decay width (grid units)
    )
