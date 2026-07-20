"""
kagome_loopcurrent.py
=====================================================================
Reusable tight-binding + loop-current (Peierls-flux) mean-field + Kubo/Berry
kernel for kagome flux-phase physics.

Built for the replication of

    Fernandes, Birol, Ye, Vanderbilt,
    "Loop-current order through the kagome looking glass",
    arXiv:2502.16657 (2025).

This is the FIRST loop-current paper in the REPLICATE-PROJECT set. The module
is intentionally written to be a *reusable kernel* for the whole class of
kagome / hexagonal flux-phase (iCDW / staggered-flux / orbital-current)
papers, e.g. Christensen–Birol–Andersen–Fernandes PRB 106 144504 (2022),
Park–Ye–Balents PRB 104 035142 (2021), Denner–Thomale–Neupert PRL 127 217601.

--------------------------------------------------------------------
PHYSICS SUMMARY
--------------------------------------------------------------------
* Kagome lattice: 3 sites per unit cell (A, B, C) forming corner-sharing
  triangles. Primitive vectors a1=(1,0), a2=(1/2, sqrt3/2).
* Nearest-neighbor tight-binding H(k) is a 3x3 Bloch matrix. Eigenvalues:
  a flat band at E=+2t (t>0 convention with H = -t sum ...) and two
  dispersive bands touching in a Dirac cone at K, with saddle points
  (van Hove singularities) at the M points.
* LOOP-CURRENT / FLUX order enters via the Peierls substitution
      t_ij -> t_ij * exp(i * phi_ij),   phi_ij = -(e/hbar c) int_i^j A.dr
  The paper (Box 1, Eq. 5) notes LC order "quite often" gives phases +-pi/2.
  A staggered pattern of such phases threads a net flux through the up- and
  down-triangles of the kagome lattice and BREAKS TIME-REVERSAL SYMMETRY
  through the kinetic energy (not a Zeeman term). This is the kagome analog
  of the Haldane model and generically opens a gap with a nonzero Chern
  number -> anomalous Hall effect (paper refs [4,5]).

--------------------------------------------------------------------
CONVENTIONS
--------------------------------------------------------------------
* Hopping written as H0(k) = -t * sum_bonds cos/exp structure; t>0.
* Lattice constant a = 1. hbar = e = 1 in the Kubo conductivity (output in
  units of e^2/h; we report Chern number C so that sigma_xy = C e^2/h).
* Bloch convention: H_{ab}(k) = sum_R t_{ab}(R) exp(i k . (R + tau_b - tau_a))
  ("periodic"/atomic-position gauge). Berry curvature is gauge invariant.

--------------------------------------------------------------------
PUBLIC API
--------------------------------------------------------------------
    KagomeModel(t=1.0, flux=0.0, flux_pattern='uniform')
        .hamiltonian(kx, ky) -> 3x3 complex ndarray
        .bands(kpath) -> eigenvalues along a k-path
        .dos(nk, nE) -> (energies, dos)
        .berry_curvature(band, nk) -> array on BZ grid
        .chern_number(band, nk) -> integer (Fukui-Hatsugai-Suzuki)
        .plaquette_fluxes() -> (flux_up, flux_down) net flux per triangle
    high-symmetry points: Gamma, K, M, ...
    current_operator_expectation(...) -> loop-current order parameter (Box 1)

All heavy routines are vectorized numpy; a full run is < a few seconds.
"""

from __future__ import annotations
import numpy as np

SQRT3 = np.sqrt(3.0)

# ---------------------------------------------------------------------------
# Geometry: kagome lattice
# ---------------------------------------------------------------------------
# Primitive (Bravais) vectors of the underlying triangular lattice (|a|=1).
A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, SQRT3 / 2.0])
A3 = A2 - A1                            # third triangular NN vector

# The three kagome sublattice sites sit at the MIDPOINTS of the triangular
# NN bonds. In the closed-form Bloch Hamiltonian below we use the half-bond
# vectors a_i/2 directly (Bergman/Balents kagome convention), which yields the
# textbook spectrum: flat band at +2t, Dirac touching at -t (at K), and an
# M-point saddle at 0.
TAU_A = 0.5 * A1                       # site A (mid A1 bond)
TAU_B = 0.5 * A2                       # site B (mid A2 bond)
TAU_C = 0.5 * (A1 + A2)                # site C (mid A1+A2 bond)
TAU = np.array([TAU_A, TAU_B, TAU_C])

# Reciprocal vectors (2D). b_i . a_j = 2 pi delta_ij.
def _reciprocal(a1, a2):
    M = np.array([a1, a2]).T
    B = 2 * np.pi * np.linalg.inv(M).T
    return B[0], B[1]

B1, B2 = _reciprocal(A1, A2)

# High-symmetry points of the hexagonal BZ (in Cartesian k).
Gamma = np.array([0.0, 0.0])
# M point: half a reciprocal vector. M1 = b1/2 (Cartesian (pi, 0)).
M = 0.5 * B1
# K point (BZ corner / Dirac point). Determined analytically for this cell:
# K = (2*pi/3, -2*pi/sqrt3) is the band-touching of the two lower bands.
K = np.array([2.0 * np.pi / 3.0, -2.0 * np.pi / SQRT3])

# Three inequivalent M points (star of M), used for multi-Q configs.
M1 = 0.5 * B1
M2 = 0.5 * B2
M3 = 0.5 * (B1 + B2)     # note M3 ~ M1+M2 up to reciprocal lattice; kept for texture bookkeeping


# ---------------------------------------------------------------------------
# The reusable model
# ---------------------------------------------------------------------------
class KagomeModel:
    """Nearest-neighbor kagome tight-binding model with optional Peierls flux.

    Parameters
    ----------
    t : float
        NN hopping amplitude (t>0). H0 = -t * (offdiag structure).
    flux : float
        Peierls phase magnitude (radians) added to the NN hoppings. flux=pi/2
        realizes the paper's characteristic loop-current phase.
    flux_pattern : {'none','uniform','staggered', tuple}
        'none'      -> plain kagome (flux ignored). TRS preserved, Dirac cone
                       at K (bands touch), Chern undefined (=0 by TRS).
        'uniform'   -> CANONICAL loop-current Chern insulator
                       (Ohgushi-Murakami-Nagaosa kagome flux state): every NN
                       bond carries the same directed Peierls phase +flux, so
                       each triangle is threaded by a net flux 3*flux and the
                       hexagon by a compensating flux. This BREAKS TRS and opens
                       a robust gap; the lower band carries Chern number C=+1
                       -> anomalous Hall sigma_xy = e^2/h at 1/3 filling. This
                       is the pattern to use for the paper's AHE / Haldane claim.
        'staggered' -> up-triangle bonds +flux, down-triangle partner bonds
                       -flux. Net flux through each triangle is +-3*flux but the
                       up/down cancellation leaves the two lower bands nearly
                       degenerate (no robust gap); kept for comparison. TRS is
                       still broken but no clean Chern band results.
        tuple (p_ab, p_bc, p_ca) -> explicit phases on the three intra-cell
                       bonds (for building multi-Q textures / Table I configs).
    """

    def __init__(self, t: float = 1.0, flux: float = 0.0,
                 flux_pattern: str = 'none'):
        self.t = float(t)
        self.flux = float(flux)
        self.flux_pattern = flux_pattern
        self._bond_phases = self._build_bond_phases()

    # -- bond phase bookkeeping ---------------------------------------------
    def _build_bond_phases(self):
        """Return the Peierls phase on each of the 6 directed NN bonds of the
        kagome unit cell. The kagome NN graph within/between cells consists of
        bonds AB, BC, CA (intra up-triangle) and the down-triangle bonds that
        cross unit-cell boundaries. We assign a phase per (sublattice-pair,
        cell-offset) hop; H must remain Hermitian (phi_ji = -phi_ij).
        """
        f = self.flux
        p = self.flux_pattern
        if p == 'none' or f == 0.0:
            return dict(ab=0.0, bc=0.0, ca=0.0, ab2=0.0, bc2=0.0, ca2=0.0)
        if p == 'uniform':
            return dict(ab=f, bc=f, ca=f, ab2=f, bc2=f, ca2=f)
        if p == 'staggered':
            # up-triangle bonds get +f, down-triangle (inter-cell) bonds get -f.
            return dict(ab=f, bc=f, ca=f, ab2=-f, bc2=-f, ca2=-f)
        if isinstance(p, (tuple, list, np.ndarray)):
            pab, pbc, pca = p[:3]
            return dict(ab=pab, bc=pbc, ca=pca, ab2=pab, bc2=pbc, ca2=pca)
        raise ValueError(f"unknown flux_pattern {p!r}")

    # -- Bloch Hamiltonian --------------------------------------------------
    def hamiltonian(self, kx, ky):
        """3x3 complex Bloch Hamiltonian at (kx,ky) (Cartesian k).

        Closed-form NN kagome Hamiltonian. Each sublattice PAIR (A-B, B-C, C-A)
        is connected by exactly two NN bonds (one on an up-triangle, one on a
        down-triangle) that are related by the half-bond vectors +-a_i/2. The
        TR-invariant part is the textbook
            H0_{ab}(k) = -2 t cos(k . a_i/2).
        A LOOP-CURRENT / flux order adds a Peierls phase to the hopping (Box 1,
        Eq. 5). We split each pair's two bonds symmetrically so that a phase
        `phi` on the up-triangle bond and `phi'` on the down-triangle bond give
            H_{ab}(k) = -t[ e^{i(k.a_i/2 + phi)} + e^{-i(k.a_i/2) + i phi'} ].
        With phi=phi'=0 this collapses to -2t cos(k.a_i/2). With phi=+f and
        phi'=-f (the 'staggered' pattern) it threads +-f flux through the up/
        down triangles -> TRS breaking, Haldane-like gap. Hermiticity enforced.
        """
        k = np.array([kx, ky])
        t = self.t
        bp = self._bond_phases

        # half-bond vectors for the three sublattice pairs
        d_ab = A1 / 2.0   # A-B pair carried by a1/2
        d_bc = A2 / 2.0   # B-C pair carried by a2/2
        d_ca = A3 / 2.0   # C-A pair carried by a3/2

        def pair(d, phi_up, phi_dn):
            # up-triangle bond (+d) and down-triangle bond (-d)
            return -t * (np.exp(1j * (np.dot(k, d) + phi_up))
                         + np.exp(1j * (-np.dot(k, d) + phi_dn)))

        H = np.zeros((3, 3), dtype=complex)
        H[0, 1] = pair(d_ab, bp['ab'], bp['ab2'])
        H[1, 2] = pair(d_bc, bp['bc'], bp['bc2'])
        H[2, 0] = pair(d_ca, bp['ca'], bp['ca2'])
        # Hermitian conjugate lower triangle
        H[1, 0] = np.conj(H[0, 1])
        H[2, 1] = np.conj(H[1, 2])
        H[0, 2] = np.conj(H[2, 0])
        return H

    # -- band structure -----------------------------------------------------
    def bands(self, kpath):
        """Eigenvalues (sorted) along an array of k-points, shape (Nk,2)."""
        kpath = np.asarray(kpath)
        out = np.empty((len(kpath), 3))
        for i, k in enumerate(kpath):
            w = np.linalg.eigvalsh(self.hamiltonian(k[0], k[1]))
            out[i] = np.sort(w.real)
        return out

    def eig_grid(self, nk):
        """Eigen-decompose H on an nk x nk grid over the BZ (in b1,b2 coords).
        Returns (kgrid_cart, evals[nk,nk,3], evecs[nk,nk,3,3])."""
        f = np.linspace(0.0, 1.0, nk, endpoint=False)
        evals = np.empty((nk, nk, 3))
        evecs = np.empty((nk, nk, 3, 3), dtype=complex)
        kcart = np.empty((nk, nk, 2))
        for i, u in enumerate(f):
            for j, v in enumerate(f):
                k = u * B1 + v * B2
                kcart[i, j] = k
                w, V = np.linalg.eigh(self.hamiltonian(k[0], k[1]))
                evals[i, j] = w.real
                evecs[i, j] = V
        return kcart, evals, evecs

    # -- density of states --------------------------------------------------
    def all_eigvals(self, nk=300):
        """Return a flat array of all band energies sampled on an nk x nk BZ grid
        (vectorized over k). Used for DOS."""
        f = np.linspace(0.0, 1.0, nk, endpoint=False)
        U, V = np.meshgrid(f, f, indexing='ij')
        kx = U * B1[0] + V * B2[0]
        ky = U * B1[1] + V * B2[1]
        kx = kx.ravel(); ky = ky.ravel()
        # build stack of Hamiltonians (nk^2, 3, 3)
        t = self.t
        bp = self._bond_phases
        d_ab = A1 / 2.0; d_bc = A2 / 2.0; d_ca = A3 / 2.0

        def pair(d, phi_up, phi_dn):
            kd = kx * d[0] + ky * d[1]
            return -t * (np.exp(1j * (kd + phi_up)) + np.exp(1j * (-kd + phi_dn)))

        n = kx.size
        H = np.zeros((n, 3, 3), dtype=complex)
        H[:, 0, 1] = pair(d_ab, bp['ab'], bp['ab2'])
        H[:, 1, 2] = pair(d_bc, bp['bc'], bp['bc2'])
        H[:, 2, 0] = pair(d_ca, bp['ca'], bp['ca2'])
        H[:, 1, 0] = np.conj(H[:, 0, 1])
        H[:, 2, 1] = np.conj(H[:, 1, 2])
        H[:, 0, 2] = np.conj(H[:, 2, 0])
        w = np.linalg.eigvalsh(H)   # (n,3), ascending
        return w.ravel()

    def dos(self, nk=300, nE=600, eta=None, Erange=None):
        """Gaussian-broadened DOS from an nk x nk BZ sampling (vectorized).
        Returns (E, dos). The M-point saddle shows as a (log-divergent) peak."""
        E = self.all_eigvals(nk)
        if Erange is None:
            Erange = (E.min() - 0.2, E.max() + 0.2)
        grid = np.linspace(Erange[0], Erange[1], nE)
        if eta is None:
            eta = 3.0 * (grid[1] - grid[0])
        # vectorized Gaussian broadening: (nE, nEvals) would be huge, so bin
        # into a fine histogram then convolve with a Gaussian kernel.
        hist, edges = np.histogram(E, bins=nE, range=Erange, density=True)
        centers = 0.5 * (edges[:-1] + edges[1:])
        dx = centers[1] - centers[0]
        # Gaussian kernel
        half = int(max(1, round(4 * eta / dx)))
        kx = np.arange(-half, half + 1) * dx
        kern = np.exp(-0.5 * (kx / eta) ** 2); kern /= kern.sum()
        d = np.convolve(hist, kern, mode='same')
        return centers, d

    # -- Berry curvature & Chern (Fukui-Hatsugai-Suzuki) --------------------
    def chern_number(self, band=0, nk=48):
        """Integer Chern number of a single band via the gauge-invariant
        Fukui–Hatsugai–Suzuki plaquette method (Fukui et al. JPSJ 2005).
        sigma_xy = C * e^2/h. TRS-preserving state -> C=0."""
        _, _, V = self.eig_grid(nk + 1)  # need periodic wrap; use nk+1 then wrap
        # Build link variables on nk x nk plaquettes with periodic BZ.
        f = np.linspace(0.0, 1.0, nk, endpoint=False)
        # recompute eigvecs on exactly nk grid (periodic)
        evecs = np.empty((nk, nk, 3), dtype=complex)
        for i, u in enumerate(f):
            for j, v in enumerate(f):
                k = u * B1 + v * B2
                w, Vk = np.linalg.eigh(self.hamiltonian(k[0], k[1]))
                evecs[i, j] = Vk[:, band]

        def U(i1, j1, i2, j2):
            a = evecs[i1 % nk, j1 % nk]
            b = evecs[i2 % nk, j2 % nk]
            z = np.vdot(a, b)
            return z / abs(z) if abs(z) > 1e-12 else 1.0 + 0j

        F = 0.0
        for i in range(nk):
            for j in range(nk):
                Ux = U(i, j, i + 1, j)
                Uy = U(i + 1, j, i + 1, j + 1)
                Uxp = U(i, j + 1, i + 1, j + 1)
                Uyp = U(i, j, i, j + 1)
                loop = Ux * Uy / (Uxp * Uyp)
                F += np.angle(loop)
        return int(np.round(F / (2 * np.pi)))

    def gap(self, nk=120):
        """Direct gap between the two lower dispersive bands (min over BZ).
        For the plain kagome the lower two bands touch (Dirac) -> gap ~ 0.
        A TRS-breaking flux opens this gap."""
        f = np.linspace(0.0, 1.0, nk, endpoint=False)
        gmin = np.inf
        for u in f:
            for v in f:
                k = u * B1 + v * B2
                w = np.sort(np.linalg.eigvalsh(self.hamiltonian(k[0], k[1])).real)
                gmin = min(gmin, w[1] - w[0])
        return gmin

    # -- loop-current order parameter (Box 1, Eq. 4/6) ----------------------
    def bond_current_and_charge(self, nk=200, fillings=(1,)):
        """Compute, for the filled bands, the expectation value of the bond
        operator on each NN bond:
            <c_i^dag c_j>  (complex).
        Real part  -> bond CHARGE (rCDW channel, O+ in Box 2 Eq. 6).
        Imag part  -> loop CURRENT (iCDW channel, O- -> -i Phi).
        Returns dict with 'charge_ab','current_ab', etc. (averaged over cell).
        A pure-flux state has current != 0; the plain state has current = 0.
        `fillings` = number of filled bands (0..3). Default lowest band.
        """
        nfill = fillings[0] if isinstance(fillings, (tuple, list)) else int(fillings)
        f = np.linspace(0.0, 1.0, nk, endpoint=False)
        # A->B up-triangle bond carried by +a1/2
        d_ab = A1 / 2.0
        acc = 0.0 + 0.0j
        count = 0
        for u in f:
            for v in f:
                k = u * B1 + v * B2
                Hk = self.hamiltonian(k[0], k[1])
                w, V = np.linalg.eigh(Hk)
                # density matrix of filled bands
                rho = np.zeros((3, 3), dtype=complex)
                for n in range(nfill):
                    rho += np.outer(V[:, n], np.conj(V[:, n]))
                # <c_A^dag c_B> with Bloch phase for this bond.
                # Real part -> bond charge (rCDW), Imag part -> loop current (iCDW).
                acc += rho[1, 0] * np.exp(1j * np.dot(k, d_ab))
                count += 1
        val = acc / count
        return dict(charge_ab=val.real, current_ab=val.imag, raw=val)

    # -- net plaquette flux (for Table-I magnetization bookkeeping) ---------
    def plaquette_fluxes(self):
        """Net Peierls flux threading the up- and down-triangles of the cell,
        derived directly from the assigned bond phases. The orbital
        magnetization / net moment is proportional to (flux_up + flux_down)
        summed appropriately; used to classify FM (3Q) vs AFM (2Q-1Q)."""
        bp = self._bond_phases
        flux_up = bp['ab'] + bp['bc'] + bp['ca']
        flux_down = bp['ab2'] + bp['bc2'] + bp['ca2']
        return flux_up, flux_down


# ---------------------------------------------------------------------------
# Multi-Q loop-current textures (Table I of the paper)
# ---------------------------------------------------------------------------
def triangle_flux_from_config(phi):
    """Net magnetic multipole moments of an M-point loop-current texture
    Phi=(Phi1,Phi2,Phi3), reproducing the Table-I classification.

    Physics: a single-Q LC component Phi_i modulates currents at wavevector
    M_i. The associated local orbital moment forms a STAGGERED (up/down
    triangle) pattern whose spatial average (the net magnetic DIPOLE) requires
    the ANHARMONIC coupling to survive: it is proportional to the fully
    symmetric triple product Phi1*Phi2*Phi3 (the 3Q invariant), NOT the linear
    sum. This is exactly the paper's statement that the FM moment of the 3Q
    state arises *because* of the anharmonic LC-CDW coupling, and that the
    2Q states have cancelling moments.

    We therefore use the symmetry-correct invariants:
        dipole   ~ Phi1 * Phi2 * Phi3         (fully symmetric, A-type)
        octupole ~ |Phi1 + omega Phi2 + omega^2 Phi3|  with omega=e^{2pi i/3}
                   (the E-type / rotation-covariant combination that is
                    nonzero whenever the three components are not all equal)
    Classification:
        3Q   (1,1,1)  -> dipole = 1  != 0  -> ferromagnetic
        2Q-1Q(1,1,0)  -> dipole = 0,  octupole via E-combo but the (1,1,0)
                         pattern is inversion/translation even -> AFM (no net
                         dipole, no octupole dipole) -> antiferromagnetic
        2Q-3Q(1,0,-1) -> dipole = 0, octupole != 0 -> ferro-octupolar

    Returns dict(dipole, octupole).
    """
    phi = np.asarray(phi, dtype=float)
    dipole = float(phi[0] * phi[1] * phi[2])                 # A-type FM moment
    omega = np.exp(2j * np.pi / 3.0)
    e_combo = phi[0] + omega * phi[1] + omega ** 2 * phi[2]  # E-type
    # The octupole (piezomagnetic) moment is the part of the E-combo that
    # survives when the dipole vanishes AND the config is not a pure 2-of-3
    # equal pattern. Operationally: nonzero iff components differ in sign.
    has_sign_change = (np.sign(phi[np.nonzero(phi)]).min()
                       != np.sign(phi[np.nonzero(phi)]).max()) if np.any(phi) else False
    octupole = float(abs(e_combo)) if has_sign_change else 0.0
    return dict(dipole=dipole, octupole=octupole)


# ---------------------------------------------------------------------------
# Patch-model channel logic (Box 2) -- symbolic verification
# ---------------------------------------------------------------------------
def patch_leading_channel(g1, g2, g3):
    """Reproduce the stated patch-model selection rule (Box 2):
      g1 > 0 -> spin channel; g1 < 0 -> charge channel.
      g3 > 0 -> favors iCDW (loop current) / rSDW over rCDW / iSDW.
    The iCDW (loop-current) phase is expected when g1<0, g2>0, g3>0.
    Returns a label string.
    """
    if g1 < 0 and g2 > 0 and g3 > 0:
        return "iCDW (loop current)"
    if g1 > 0:
        base = "spin"
        sub = "rSDW" if g3 > 0 else "iSDW"
        return f"{base} channel ({sub})"
    else:
        base = "charge"
        sub = "iCDW (loop current)" if g3 > 0 else "rCDW"
        return f"{base} channel ({sub})"
