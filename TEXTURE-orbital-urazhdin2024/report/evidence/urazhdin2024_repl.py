#!/usr/bin/env python3
"""
Independent replication of Urazhdin 2024 (arXiv:2408.08683v3):
"Atomic and inter-atomic orbital magnetization induced in SrTiO3 by chiral phonons"

Minimal molecular-orbital (MO) tight-binding model for STO valence states:
 basis = 4 oxygen p_z orbitals (ring) + Ti d_sigma orbitals (d+, d-).

We independently:
  1. Build & diagonalize the 6-state static MO Hamiltonian; verify the MO level
     structure (Eqs. 1-4): nonbonding +/-2 t_OO, bonding/antibonding E_a,b, gap Delta.
  2. Reconstruct the Koster-Slater parameter chain a_t, a_l, a_+, a_- (Eqs. 10-11).
  3. Numerically integrate time-dependent perturbation theory (TDPT) for the
     chiral phonon coupling (Eqs. 5-7) to independently recover the excitation
     probabilities p_sigma and the ATOMIC orbital moment Eq. (8).
  4. Compute the INTER-ATOMIC orbital moment Eq. (18) via mu_1 = e a^2 |t_OO|/2hbar.
  5. Compare to the paper's numeric claims and emit a verdict.

Units: energies in eV, lengths in nm, moments in Bohr magnetons (mu_B).
Independent re-derivation from the paper's equations -- NOT author code.
"""
import json, os
import numpy as np

# ---------------- physical constants ----------------
e_C     = 1.602176634e-19        # C
hbar_Js = 1.054571817e-34        # J s
hbar_eVs= 6.582119569e-16        # eV s
muB_JT  = 9.2740100783e-24       # J/T
eV_J    = 1.602176634e-19

# ---------------- paper parameters ----------------
t_TiO = -1.14        # eV   Vpd_pi, Ti-O sigma-bond hopping (paper: t_TiO=-Vpd_pi=-1.14)
t_OO  = -0.8         # eV   O-O nearest-neighbour p-p hopping (Koster-Slater estimate)
r_TiO = 0.20         # nm   Ti-O distance
a_lat = 0.39         # nm   STO lattice constant
Delta_paper = 3.2    # eV   bandgap target
f_THz = 3.0          # THz  phonon frequency
hbar_omega = 0.0124  # eV   phonon energy (=h f, paper states 12.4 meV)
omega = hbar_omega/hbar_eVs        # rad/s
c_chir = +1                        # chirality
tau = 1.0e-12        # s    pulse width (tau >> hbar/Delta ~2e-16 s; 1/tau << Delta/hbar)

results = {"paper": "Urazhdin 2024 arXiv:2408.08683v3",
           "params": dict(t_TiO=t_TiO, t_OO=t_OO, r_TiO=r_TiO, a_lat=a_lat,
                          Delta_paper=Delta_paper, hbar_omega=hbar_omega, tau_s=tau)}

# =====================================================================
# 1. STATIC 6-STATE MO HAMILTONIAN  (choose E_d to reproduce gap 3.2 eV)
# =====================================================================
# Two-level (d_sigma <-> coupling O-combo) eigenvalues (Eq.3):
#   E_{a,b} = E_d/2 +/- sqrt(E_d^2/4 + 2 t_TiO^2)
# Nonbonding O states at +/- 2 t_OO (Eq.1). Gap (Eq.4): Delta = E_a - E_{n2}.
# E_{n2} = -2 t_OO. Solve for E_d so that E_a - (-2 t_OO) = 3.2.
E_n2 = -2*t_OO
E_a_target = Delta_paper + E_n2
# E_a = E_d/2 + sqrt(E_d^2/4 + 2 t_TiO^2)  ->  solve
# sqrt(E_d^2/4 + 2t^2) = E_a - E_d/2 ; square:
# 2 t^2 = E_a^2 - E_a E_d  ->  E_d = (E_a^2 - 2 t_TiO^2)/E_a
E_d = (E_a_target**2 - 2*t_TiO**2)/E_a_target
results["E_d_eV"] = E_d

def build_H(Ed):
    """6x6 MO Hamiltonian. Basis: p1,p2,p3,p4, d+, d-.
    O ring: uniform NN hopping t_OO (1-2-3-4-1).
    Ti-O: <d_sigma|H|p_n> = (t_TiO/sqrt2) exp(i sigma n pi/2), sigma=+/-1.
    (amplitude 1/sqrt2 because complex d_sigma spreads over both bond axes -> gives
     coupling |V|^2 = 2 t_TiO^2, reproducing Eq.3)."""
    H = np.zeros((6,6), dtype=complex)
    # oxygen onsite = 0 (energy relative to atomic O p-level); Ti onsite = Ed
    H[4,4] = Ed; H[5,5] = Ed
    # O-O ring hopping
    ring = [(0,1),(1,2),(2,3),(3,0)]
    for i,j in ring:
        H[i,j] += t_OO; H[j,i] += t_OO
    # Ti-O hybridization
    for si,sigma in enumerate([+1,-1]):
        d = 4+si
        for n in range(1,5):          # oxygen labels n=1..4
            v = (t_TiO/np.sqrt(2))*np.exp(1j*sigma*n*np.pi/2)
            H[d, n-1] += v
            H[n-1, d] += np.conj(v)
    return H

H = build_H(E_d)
evals, evecs = np.linalg.eigh(H)
evals_sorted = np.sort(evals.real)
results["mo_eigenvalues_eV"] = [float(x) for x in evals_sorted]

# analytic MO levels
E_ab = np.array([E_d/2 + s*np.sqrt(E_d**2/4 + 2*t_TiO**2) for s in (+1,-1)])  # E_a,E_b
E_nb = np.array([2*t_OO, -2*t_OO])  # n1, n2
analytic_levels = np.sort(np.concatenate([E_ab, E_ab, E_nb]))  # a,b are doubly deg (d+,d-)
results["mo_analytic_levels_eV"] = [float(x) for x in analytic_levels]
gap_diag = evals_sorted[-1] - sorted(evals_sorted)[3]  # antibonding(top 2) - highest nonbonding
# gap = E_a - E_n2
gap_analytic = E_ab[0] - E_nb[1]
results["gap_analytic_eV"] = float(gap_analytic)
# gap from diagonalization: E_a is the (doubly-deg) top level; E_n2 is nonbonding just below bonding manifold
# identify: sorted levels = [E_b(x2), E_n2 or E_n1..]; robustly: antibonding = max
E_a_diag = evals_sorted[-1]
# nonbonding levels are +/-2t_OO = +/-1.6
gap_diag = E_a_diag - E_n2
results["gap_from_diag_eV"] = float(gap_diag)

Delta = gap_analytic   # use consistent gap for mechanism

# sin^2 theta_a : d-weight of antibonding state. theta_a = atan( sqrt2 t_TiO/(E_d - E_a) )
theta_a = np.arctan2(np.sqrt(2)*t_TiO, (E_d - E_ab[0]))
sin2_theta_a = np.sin(theta_a)**2
results["sin2_theta_a"] = float(sin2_theta_a)

# =====================================================================
# 2. KOSTER-SLATER PARAMETER CHAIN (Eqs. 10-11)
# =====================================================================
a_t = -t_TiO / r_TiO          # eV/nm  (Eq.10)  = 1.14/0.2 = 5.7
a_l = 3.5 * a_t               # eV/nm  (Eq.11)  = 7 a_t/2 = 20.0
a_plus  = (a_l + a_t)/2
a_minus = (a_l - a_t)/2
diff2   = a_plus**2 - a_minus**2   # = a_l a_t
results["koster_slater"] = dict(a_t=a_t, a_l=a_l, a_plus=a_plus, a_minus=a_minus,
                                a2_diff=diff2, al_at=a_l*a_t)

# =====================================================================
# 3. NUMERIC TDPT -> ATOMIC ORBITAL MOMENT (Eqs. 5-8)
# =====================================================================
# Coupling (interaction picture), gap Delta between filled nonbonding and empty
# antibonding psi_{a,sigma}. Q(t)=Q0 exp(-|t|/tau).
#   V_{sigma,n1}(t) = 2 sin(theta_a) Q(t) a_+ exp(-i c sigma omega t)   [couples n1]
#   V_{sigma,n2}(t) = 2 sin(theta_a) Q(t) a_- exp(+i c sigma omega t)   [couples n2]
# First-order amplitude into psi_{a,sigma}:
#   b(0) = -(i/hbar) INT_{-inf}^{0} V(t) exp(i Delta t/hbar) dt
# p_sigma = |b_n1|^2 + |b_n2|^2  (distinct initial states -> incoherent sum)
# m_z = -2 mu_B (p_+ - p_-)   (factor 2 = spin doubling)

sin_th = np.sqrt(sin2_theta_a)

def p_sigma_numeric(Q0_nm, sigma):
    """Numerically integrate TDPT amplitudes; Q0 in nm, a_+/a_- in eV/nm -> V in eV."""
    Q0 = Q0_nm
    # integrate t in [-Ntau*tau, 0]
    N = 400000
    Tspan = 30*tau
    t = np.linspace(-Tspan, 0.0, N)
    Qt = Q0*np.exp(t/tau)                      # t<=0 -> exp(t/tau)
    phaseD = np.exp(1j*(Delta/hbar_eVs)*t)     # exp(i Delta t/hbar), Delta in eV
    # n1 (a_+, e^{-i c sigma omega t})
    V1 = 2*sin_th*Qt*a_plus*np.exp(-1j*c_chir*sigma*omega*t)
    integ1 = V1*phaseD
    b1 = -1j/hbar_eVs * np.trapezoid(integ1, t)
    # n2 (a_-, e^{+i c sigma omega t})
    V2 = 2*sin_th*Qt*a_minus*np.exp(+1j*c_chir*sigma*omega*t)
    integ2 = V2*phaseD
    b2 = -1j/hbar_eVs * np.trapezoid(integ2, t)
    return abs(b1)**2 + abs(b2)**2

def p_sigma_closed(Q0_nm, sigma):
    """Closed-form: |b|^2 = (2 sin Q0 a)^2 / [(Delta -/+ c sigma hw)^2 + hbar^2/tau^2]."""
    Q0 = Q0_nm
    hbar_tau = hbar_eVs/tau
    pref = (2*sin_th*Q0)**2
    d1 = (Delta - c_chir*sigma*hbar_omega)**2 + hbar_tau**2   # n1 term (a_+)
    d2 = (Delta + c_chir*sigma*hbar_omega)**2 + hbar_tau**2   # n2 term (a_-)
    return pref*(a_plus**2/d1 + a_minus**2/d2)

def mz_atomic_numeric(Q0_nm):
    pp = p_sigma_numeric(Q0_nm, +1)
    pm = p_sigma_numeric(Q0_nm, -1)
    return -2.0*(pp - pm), pp, pm      # in units of mu_B

def mz_atomic_eq8(Q0_nm):
    """Paper Eq.8 (leading order)."""
    return 32*c_chir*hbar_omega*sin2_theta_a*Q0_nm**2*diff2/Delta**3   # in mu_B

# Verify at a reference amplitude
Q0_ref = 0.08   # nm  (paper's stated amplitude)
mz_num, pp, pm = mz_atomic_numeric(Q0_ref)
mz_num = abs(mz_num)
mz_e8  = abs(mz_atomic_eq8(Q0_ref))
# closed-form cross-check of p_sigma
pp_c = p_sigma_closed(Q0_ref,+1); pm_c = p_sigma_closed(Q0_ref,-1)

results["atomic"] = dict(
    Q0_nm=Q0_ref,
    p_plus_numeric=float(pp), p_minus_numeric=float(pm),
    p_plus_closed=float(pp_c), p_minus_closed=float(pm_c),
    mz_atomic_numeric_muB=float(mz_num),
    mz_atomic_eq8_muB=float(mz_e8),
    ratio_num_over_eq8=float(mz_num/mz_e8),
)

# Back out Q0 required for mz = 1e-2 muB  (paper claims ~0.08 nm)
# mz_eq8 = K * Q0^2  ->  Q0 = sqrt(1e-2/K)
K = 32*hbar_omega*sin2_theta_a*diff2/Delta**3
Q0_for_1e2 = np.sqrt(1e-2/K)
results["atomic"]["Q0_nm_for_1e-2_muB"] = float(Q0_for_1e2)
results["atomic"]["paper_claim_Q0_nm"]  = 0.08

# =====================================================================
# 4. INTER-ATOMIC ORBITAL MOMENT (Eq. 18)
# =====================================================================
# mu_1 = e a^2 |t_OO| / (2 hbar)   [SI], then express in mu_B
a_m   = a_lat*1e-9                 # m
tOO_J = abs(t_OO)*eV_J            # J
mu_1_JT = e_C * a_m**2 * tOO_J / (2*hbar_Js)
mu_1_muB = mu_1_JT/muB_JT
results["mu_1_muB"] = float(mu_1_muB)
results["mu_1_paper_muB"] = 1.6

# interatomic moment = (mu_1/mu_B) * atomic-moment-formula
mz_ia_eq18 = abs(32*c_chir*hbar_omega*sin2_theta_a*Q0_ref**2*diff2/Delta**3) * mu_1_muB  # in mu_B
results["interatomic"] = dict(
    Q0_nm=Q0_ref,
    mz_interatomic_eq18_muB=float(mz_ia_eq18),
    ratio_interatomic_to_atomic=float(mu_1_muB),   # since same formula scaled by mu_1/muB
)

# =====================================================================
# 5. VERDICT CHECKS
# =====================================================================
checks = {}
checks["a_t_eV_nm"]     = (a_t, 5.7)
checks["a_l_eV_nm"]     = (a_l, 20.0)
checks["a_plus_eV_nm"]  = (a_plus, 13.0)
checks["a_minus_eV_nm"] = (a_minus, 7.0)
checks["mu_1_muB"]      = (mu_1_muB, 1.6)
checks["Q0_for_1e-2muB_nm"] = (Q0_for_1e2, 0.08)
checks["gap_eV"]        = (gap_analytic, 3.2)
checks["num_vs_eq8_ratio"] = (mz_num/mz_e8, 1.0)

def relerr(a,b): return abs(a-b)/abs(b)
results["checks"] = {k: dict(computed=float(v[0]), paper=float(v[1]),
                             rel_err=float(relerr(*v))) for k,v in checks.items()}

all_ok = all(relerr(*v) < 0.10 for v in checks.values())
results["all_checks_within_10pct"] = bool(all_ok)

# ---------------- print summary ----------------
print("="*70)
print("STATIC MO HAMILTONIAN (6-state)")
print(f"  E_d chosen = {E_d:.4f} eV to hit gap {Delta_paper} eV")
print(f"  eigenvalues (eV): {np.round(evals_sorted,4)}")
print(f"  analytic levels : {np.round(analytic_levels,4)}")
print(f"  gap (diag)={gap_diag:.4f}  gap(analytic)={gap_analytic:.4f}  (paper 3.2)")
print(f"  sin^2(theta_a) = {sin2_theta_a:.4f}")
print("-"*70)
print("KOSTER-SLATER:")
print(f"  a_t={a_t:.3f} (p5.7)  a_l={a_l:.3f} (p20)  a_+={a_plus:.3f} (p13)  a_-={a_minus:.3f} (p7)")
print(f"  a_+^2-a_-^2 = a_l a_t = {diff2:.3f} (eV/nm)^2")
print("-"*70)
print("ATOMIC ORBITAL MOMENT (Eq.8) @ Q0=0.08 nm:")
print(f"  numeric TDPT : |m_z| = {mz_num:.4e} muB")
print(f"  Eq.8 formula : |m_z| = {mz_e8:.4e} muB   (ratio {mz_num/mz_e8:.4f})")
print(f"  p_+={pp:.3e}  p_-={pm:.3e}  (closed {pp_c:.3e}/{pm_c:.3e})")
print(f"  Q0 for 1e-2 muB = {Q0_for_1e2:.4f} nm  (paper ~0.08 nm)")
print("-"*70)
print("INTER-ATOMIC ORBITAL MOMENT (Eq.18):")
print(f"  mu_1 = {mu_1_muB:.4f} muB   (paper 1.6)")
print(f"  interatomic/atomic ratio = {mu_1_muB:.3f}  -> 'very close', comparable")
print("-"*70)
print(f"ALL CHECKS < 10% : {all_ok}")
for k,v in results["checks"].items():
    print(f"  {k:24s} comp={v['computed']:.4g}  paper={v['paper']:.4g}  relerr={v['rel_err']*100:.2f}%")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "urazhdin2024_result.json")
with open(out,"w") as fh:
    json.dump(results, fh, indent=2)
print("="*70)
print("wrote", out)
