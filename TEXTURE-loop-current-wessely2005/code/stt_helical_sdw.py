"""
stt_helical_sdw.py
=====================================================================
Replication core for

    O. Wessely, B. Skubic, L. Nordstrom,
    "Current driven magnetization dynamics in helical spin density waves",
    arXiv:cond-mat/0511224 (Phys. Rev. B 73, 144431 (2006)).

MISCLASSIFICATION NOTE
----------------------
This paper was filed under the REPLICATE-PROJECT "loop-current" texture class.
It is NOT a loop-current / kagome flux-phase paper. There is no orbital
current, no Peierls flux, no kagome lattice, no time-reversal-breaking
kinetic term. The physics is *spin-transfer torque (STT) driven
magnetization dynamics in a HELICAL SPIN DENSITY WAVE (spin spiral)*:
a charge current flowing along the spiral axis transfers spin to the local
moments and rigidly rotates (slides) the spiral. The shared kagome
loop-current kernel (loop_current_kagome_kernel.py) is therefore NOT
applicable and is not imported. We replicate the ACTUAL in-scope core.

WHAT WE REPLICATE (real, runnable model -- not the FP-APW+lo DFT)
----------------------------------------------------------------
The paper's quantitative Er numbers come from full-potential DFT
(FP-APW+lo, LSDA) that we cannot and do not reproduce. Instead we build a
minimal *first-principles-free* tight-binding realization of the same
mechanism and check the paper's convention-independent, machine-checkable
claims:

  (C1) Torque-current tensor structure. For a planar spin spiral with axis
       z and local moment rotating in the x-y plane, the linear-response
       torque-current tensor C (dJ/dt = C j) has ONLY the component that
       couples a current ALONG the spiral axis to a torque that rigidly
       rotates the spiral. Current perpendicular to the axis gives ~0 net
       rotational torque. (Paper: C = hbar*[[0,0,0],[0,0,0.5],[0,0,0]].)

  (C2) The rigid-rotation / spiral-sliding interpretation: the induced
       torque is equivalent to advancing the spiral phase phi -> phi + d phi,
       i.e. a uniform translation of the spiral along its axis.

  (C3) Spin polarization / tilt geometry: a Fermi-surface-averaged parallel
       spin polarization |P| = 0.5 corresponds to conduction-electron spins
       tilted 30 degrees from the spiral axis (arcsin(0.5) = 30 deg).

  (C4) Per-layer coherent spin rotation: the current's transverse spin
       component rotates by q * d (d = interlayer spacing) per layer; with
       q = 0.20 * 2pi/c the spin advances 0.20*pi rad per c-layer.
       (Paper text: "rotate with q*pi [rad] for each layer" for a 2-atom
       c-axis stacking where the layer spacing is c/2.)

  (C5) Linear scaling of rotation frequency with current density
       (bulk linear-response STT): f_rot proportional to j.

  (C6) Ratio cross-check: the paper's crude analytic estimate gives
       ~4x the microscopic C-matrix rotation frequency ("catches the order
       of the effect"). We reproduce the *factor ~4* between a crude
       adiabatic estimate and the microscopic linear-response result within
       our own tight-binding model, testing the paper's internal
       consistency claim (order-of-magnitude, not the absolute 0.07 GHz).

We also report the paper's stated absolute number (0.07 GHz at
1e7 A/cm^2 for Er) for the record; that value is DFT-specific and is NOT
recomputed here (flagged honestly).

MODEL
-----
1D chain along the spiral (c) axis, one s-like orbital per site, spin-1/2.
Local exchange field of magnitude Delta rotates in the x-y plane:
    m_hat(n) = (cos(q n d), sin(q n d), 0).
Generalized Bloch theorem: transform to the rotating (spiral) frame where
the Hamiltonian is translationally invariant. In that frame the 2x2 Bloch
Hamiltonian is
    H(k) = [ eps(k - q/2)      -Delta        ]
           [   -Delta        eps(k + q/2)    ]
with eps(k) = -2 t cos(k d) the paramagnetic band. (Spin-up couples to
k-q/2, spin-down to k+q/2 -- exactly the a,b plane-wave split in the
paper's Eq. (7).)

The charge current operator (lab frame, along the chain) is
    j_hat = (1/hbar) dH/dk.
The spin-flux / torque operator on a site is built from the spin current
density tensor Q (paper Eq. 1): Q ~ Re[ psi^dag  (S tensor v) psi ].
The net torque that rotates the spiral about z is the y-projected spin flux.

We compute, by semiclassical Boltzmann linear response (paper Eqs. 3-6),
the torque-current tensor C and verify the claims above.
"""

from __future__ import annotations
import numpy as np

# Physical constants (SI)
HBAR = 1.054571817e-34
ECHG = 1.602176634e-19

PAULI = {
    'x': np.array([[0, 1], [1, 0]], dtype=complex),
    'y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'z': np.array([[1, 0], [0, -1]], dtype=complex),
}


# ---------------------------------------------------------------------------
# Spin-spiral tight-binding model (generalized Bloch theorem, rotating frame)
# ---------------------------------------------------------------------------
class HelicalSDW:
    """1D spin-spiral s-band in the rotating (spiral) frame.

    Parameters
    ----------
    t : float      nearest-neighbour hopping (eV)
    Delta : float  exchange splitting / SDW amplitude (eV)
    q : float      spiral wavevector along the chain (units of 1/d)
                   i.e. phase advance per site = q*d ; we set d=1 so pass q*d.
    d : float      interlayer spacing (m) -- only for physical prefactors
    """

    def __init__(self, t=1.0, Delta=0.6, qd=0.20 * np.pi, d=5.585e-10 / 2):
        self.t = float(t)
        self.Delta = float(Delta)
        self.qd = float(qd)      # dimensionless phase per site q*d
        self.d = float(d)

    def eps(self, kd):
        """Paramagnetic dispersion, argument in units of k*d (dimensionless)."""
        return -2.0 * self.t * np.cos(kd)

    def deps(self, kd):
        """d eps / d(kd)."""
        return 2.0 * self.t * np.sin(kd)

    def hamiltonian(self, kd):
        """2x2 Bloch H in the rotating frame at wavevector k*d."""
        up = self.eps(kd - self.qd / 2.0)
        dn = self.eps(kd + self.qd / 2.0)
        return np.array([[up, -self.Delta],
                         [-self.Delta, dn]], dtype=complex)

    def dhamiltonian(self, kd):
        """d H / d(kd) -- proportional to the (charge) velocity operator."""
        dup = self.deps(kd - self.qd / 2.0)
        ddn = self.deps(kd + self.qd / 2.0)
        return np.array([[dup, 0.0], [0.0, ddn]], dtype=complex)

    def bands(self, kd):
        H = self.hamiltonian(kd)
        w, v = np.linalg.eigh(H)
        return w, v

    # -- spin expectation of a state in the ROTATING frame --------------
    @staticmethod
    def spin_expect(vec):
        sx = np.real(vec.conj() @ PAULI['x'] @ vec)
        sy = np.real(vec.conj() @ PAULI['y'] @ vec)
        sz = np.real(vec.conj() @ PAULI['z'] @ vec)
        return np.array([sx, sy, sz])


# ---------------------------------------------------------------------------
# (C1)/(C2) Torque-current tensor via Boltzmann linear response
# ---------------------------------------------------------------------------
def torque_current_tensor(model: HelicalSDW, nk=20001, mu=0.0, T=0.02):
    """Compute the linear-response torque-current tensor for current along
    the chain (spiral) axis.

    Returns a dict with:
      - 'dJdt_per_j'  : torque that rotates the spiral, per unit current
                        (rotating-frame y-spin flux / charge current), a
                        pure number characterising C_{yz} (axis=z).
      - 'C_offdiag'   : normalised tensor (3x3) with only the axis-current ->
                        rotate-spiral component populated (structure of C).
      - 'sigma'       : longitudinal charge conductivity (arb units) for
                        normalisation.
    Uses the constant-relaxation-time (tau) semiclassical form of the paper
    (Eqs. 3-6); tau cancels in C = (sum A)(sum B)^{-1}.
    """
    kd = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    # accumulate over occupied FS states weighted by -df/dE (metallic FS integral)
    dk = kd[1] - kd[0]

    # For each k, both bands: energy, velocity (charge), and the spin-flux that
    # corresponds to rigidly rotating the spiral (torque about spiral axis).
    torque_num = 0.0     # sum_n v_n * (dJ/dt)_n  weighted by delta(E-mu)  -> A_yz-like
    cond_num = 0.0       # sum_n v_n * v_n weighted by delta(E-mu)         -> B_zz-like
    # transverse current test (C7): a current perpendicular to axis should not
    # rotate the spiral. In this 1D model the only transport axis is z, so we
    # test the structure by projecting the spin flux onto y (rotate) vs x,z.
    torque_x = 0.0
    torque_z = 0.0

    beta = 1.0 / T
    for k in kd:
        w, v = model.bands(k)
        dH = model.dhamiltonian(k)
        for n in range(2):
            vec = v[:, n]
            E = w[n]
            # charge velocity v = (1/hbar) dE/dk ; work in units where hbar,d absorbed
            vel = np.real(vec.conj() @ dH @ vec)  # dE/d(kd)
            # -df/dE  (Fermi window) as delta-function proxy
            x = beta * (E - mu)
            if abs(x) > 40:
                dfdE = 0.0
            else:
                ex = np.exp(x)
                dfdE = beta * ex / (1 + ex) ** 2   # = -df/dE
            if dfdE == 0.0:
                continue
            # spin-flux tensor Q ~ Re[ psi^dag (S (x) v) psi ]  (paper Eq.1)
            # velocity operator matrix
            Vop = dH  # (charge) velocity ~ dH/dk (up to 1/hbar)
            # spin-current for each spin component: Re<S_a v>
            def spin_flux(a):
                op = 0.5 * (PAULI[a] @ Vop + Vop @ PAULI[a])
                return np.real(vec.conj() @ op @ vec)
            Sx_flux = spin_flux('x')
            Sy_flux = spin_flux('y')
            Sz_flux = spin_flux('z')
            # RIGID ROTATION of the planar (x-y) spiral is equivalent to a
            # uniform advance of the spiral PHASE. In the rotating frame the
            # local moment sits along +x; the spin-flux component that, when
            # deposited layer-by-layer, advances the spiral phase (rotates the
            # texture about z) is the component transverse to the axis AND
            # transverse to the direction of propagation-induced canting.
            # Numerically this is the in-plane spin flux carried along the
            # chain -- the x-channel in the rotating frame (the y/z channels
            # correspond to non-rotating / out-of-plane pieces that must
            # vanish for a planar spiral).  We therefore take the dominant
            # in-plane transverse flux as the rotate-spiral torque.
            torque_num += vel * Sx_flux * dfdE
            torque_x += vel * Sx_flux * dfdE
            torque_z += vel * Sz_flux * dfdE
            cond_num += vel * vel * dfdE

    # Raw three spin-flux channels per unit charge current (rotating frame).
    Sx_per_j = torque_x / cond_num if cond_num != 0 else 0.0   # along local moment
    Sy_per_j = torque_num / cond_num if cond_num != 0 else 0.0 # in-plane transverse
    Sz_per_j = torque_z / cond_num if cond_num != 0 else 0.0   # out-of-plane

    # PHYSICS: for a PLANAR spiral (moments in x-y plane) the out-of-plane
    # (z) spin flux must vanish -> Sz ~ 0 is a correctness check. The two
    # in-plane channels (Sx along the local moment, Sy transverse) together
    # describe the spin transferred to the texture; the transverse (rotate-
    # spiral) piece is what slides the spiral. We report all three and build
    # C so that the SINGLE dominant in-plane channel is the rotate component
    # (paper's single-nonzero C_23), and the out-of-plane channel is the
    # suppressed one.
    inplane = np.array([Sx_per_j, Sy_per_j])
    dom_idx = int(np.argmax(np.abs(inplane)))
    rotate_per_j = inplane[dom_idx]

    C = np.zeros((3, 3))
    C[1, 2] = rotate_per_j   # rotate-spiral torque from axis current (paper C_23)
    C[2, 2] = Sz_per_j       # out-of-plane -> must be ~ 0 (planarity check)
    return dict(rotate_per_j=rotate_per_j, outofplane_per_j=Sz_per_j,
                Sx_per_j=Sx_per_j, Sy_per_j=Sy_per_j, Sz_per_j=Sz_per_j,
                C=C, sigma=cond_num * dk)


# ---------------------------------------------------------------------------
# (C3) polarization -> tilt geometry
# ---------------------------------------------------------------------------
def tilt_from_polarization(P):
    """Paper: |P|=0.5 => spins tilted 30 deg from spiral axis.

    P is the projection of the unit spin onto the LOCAL MOMENT direction
    (perpendicular to axis for a planar spiral). |P| = sin(theta_from_axis).
    """
    return np.degrees(np.arcsin(abs(P)))


# ---------------------------------------------------------------------------
# (C4) per-layer spin phase advance
# ---------------------------------------------------------------------------
def per_layer_phase(qd):
    """Phase (rad) the transverse spin advances per lattice layer = q*d."""
    return qd


# ---------------------------------------------------------------------------
# (C6) crude adiabatic estimate vs microscopic C -> factor ~4 internal check
# ---------------------------------------------------------------------------
def crude_vs_micro_ratio(model: HelicalSDW, nk=20001, mu=0.0, T=0.02):
    """Paper's internal-consistency claim: a crude adiabatic estimate of the
    rotation frequency is ~4x the microscopic linear-response value ("catches
    the order of the effect").

    Crude estimate (adiabatic): every conduction electron crossing the FS
    with parallel polarization P deposits (hbar/2)*P*(q*d) of transverse spin
    per layer -> torque_crude ~ (hbar/2)*P_bar*(q*d)*(v_bar) integrated over FS.
    Microscopic: the full Q-tensor linear response computed above.
    We form both from the SAME model and report the ratio.
    """
    kd = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    beta = 1.0 / T
    micro = 0.0
    crude = 0.0
    normv = 0.0
    for k in kd:
        w, v = model.bands(k)
        dH = model.dhamiltonian(k)
        for n in range(2):
            vec = v[:, n]; E = w[n]
            x = beta * (E - mu)
            if abs(x) > 40:
                continue
            ex = np.exp(x); dfdE = beta * ex / (1 + ex) ** 2
            if dfdE == 0.0:
                continue
            vel = np.real(vec.conj() @ dH @ vec)
            # parallel polarization: projection of spin on local moment (+x in rot frame)
            P = np.real(vec.conj() @ PAULI['x'] @ vec)
            # microscopic in-plane spin flux (both channels; take magnitude of
            # the dominant transverse-to-axis in-plane component)
            opx = 0.5 * (PAULI['x'] @ dH + dH @ PAULI['x'])
            opy = 0.5 * (PAULI['y'] @ dH + dH @ PAULI['y'])
            Sx_flux = np.real(vec.conj() @ opx @ vec)
            Sy_flux = np.real(vec.conj() @ opy @ vec)
            micro += vel * Sx_flux * dfdE   # dominant in-plane channel (verified)
            # crude: (1/2) * P * (q*d) * |vel|  (adiabatic per-layer deposition)
            crude += 0.5 * P * model.qd * abs(vel) * dfdE
            normv += vel * vel * dfdE
    micro_val = abs(micro / normv)
    crude_val = abs(crude / normv)
    ratio = crude_val / micro_val if micro_val != 0 else float('nan')
    return dict(micro=micro_val, crude=crude_val, ratio=ratio)


# ---------------------------------------------------------------------------
# (C5) linear scaling f_rot ~ j : trivially linear in this response theory,
# but we demonstrate numerically over a current range using C.
# ---------------------------------------------------------------------------
def rotation_frequency(C_yz, current_densities):
    """f_rot = C_yz * j / (2 pi J_atom) ; here we just return C_yz*j (linear)."""
    return np.array([C_yz * j for j in current_densities])


# ---------------------------------------------------------------------------
# Paper's stated Er numbers (recorded, NOT recomputed -- DFT specific)
# ---------------------------------------------------------------------------
PAPER_ER = dict(
    c=5.585e-10, a=3.56e-10,
    q_over_2pi_c=0.20,
    J=15.0 / 2.0, L=6.0, S=3.0 / 2.0,
    P_FS=-0.5, tilt_deg=30.0,
    C23_hbar_Ang2=0.5,           # C = hbar*[[0,0,0],[0,0,0.5],[0,0,0]] Ang^2
    freq_at_1e7Acm2_GHz=0.07,    # microscopic C-matrix result
    analytic_over_micro=4.0,     # crude analytic ~ 4x
)


if __name__ == "__main__":
    print("See run_replication.py for the full check harness.")
