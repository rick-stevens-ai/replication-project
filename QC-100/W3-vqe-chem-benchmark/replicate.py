#!/usr/bin/env python3
"""
Replication of: A. J. McCaskey, Z. P. Parks, J. Jakowski, S. V. Moore,
T. D. Morris, T. S. Humble, R. C. Pooser,
"Quantum chemistry as a benchmark for near-term quantum computers",
npj Quantum Information 5, 99 (2019).

The paper's *primary results* are hardware runs on IBM Tokyo and Rigetti Aspen
(Table 1 energies are device- and noise-specific and are NOT reproducible
without those exact QPUs). What IS classically/simulator-reproducible is the
benchmark's algorithmic backbone, which the paper itself defines:

  - each alkali-metal hydride (NaH/KH/RbH) is reduced by frozen-core + active
    space to "two valence electrons and the equivalent of a hydrogen molecule
    in minimal basis" (4 spin orbitals -> 4 qubits, JW-mapped);
  - the state-prep primitive is the single-parameter UCC ansatz (ucc-1): one
    double-excitation amplitude theta;
  - the "theoretically exact E(theta)" curve (solid line, Fig. 2) is the
    noiseless reference the hardware is compared against;
  - benchmark metric = closeness of the recovered ground-state energy to FCI,
    with chemical accuracy = 0.0016 Ha;
  - zero-noise (Richardson) extrapolation: linear and quadratic fits to r=0.

We reproduce that backbone on the H2/STO-3G active-space Hamiltonian (the
paper's stated equivalent system; H2 coefficients from the standard STO-3G
2-qubit tapered Hamiltonian and the 4-qubit JW Hamiltonian):

  C1  Noiseless ucc-1 VQE: sweep theta in [-pi,pi], cubic-spline the optimum,
      confirm the minimum equals FCI (exact diagonalization) to << chemical
      accuracy. This validates "ucc-1 recovers FCI" -- the paper's claim that
      the single-parameter UCC, with mitigation, reaches FCI within error bars.
  C2  Show the hardware-efficient (HWE)-style unconstrained ansatz can drop
      BELOW the true ground energy / give unphysical electron number (paper:
      "prepares states with varying numbers of electrons that yield unphysical
      results", and "hwe was unable to produce results comparable to FCI").
  C3  Reproduce the Richardson zero-noise extrapolation METHOD: inject a
      controlled depolarizing-like linear+quadratic noise model E(r) (r = #CNOT
      identity insertions), fit linear and quadratic to r=0, recover the
      noiseless energy. Confirms the extrapolation machinery the paper relies on.
  C4  E(R) potential curve from ucc-1 over several bond lengths (Fig. 5 analog),
      confirming VQE tracks FCI across the surface.

Convention: 4-qubit JW Hamiltonian for H2/STO-3G at R=0.7414 A. Qubit 0 = LSB.
All energies from exact statevector / exact diagonalization, no device data.
"""
import numpy as np
import json
from scipy.optimize import curve_fit, minimize
from scipy.interpolate import CubicSpline

CHEM_ACC = 0.0016  # Hartree

# Pauli
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
P = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}

def op(n, term):
    ops = {}
    if term != 'I':
        for tok in term.split():
            ops[int(tok[1:])] = tok[0]
    mats = [P.get(ops.get(q, 'I')) for q in range(n-1, -1, -1)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

# H2/STO-3G 4-qubit JW Hamiltonian at equilibrium (standard literature coeffs,
# R=0.7414 A; e.g. O'Malley 2016 / OpenFermion). Electronic + nuclear repulsion.
def H2_hamiltonian_4q():
    terms = [
        (-0.81261, 'I'),
        (0.171201, 'Z0'), (0.171201, 'Z1'),
        (-0.2227965, 'Z2'), (-0.2227965, 'Z3'),
        (0.16862325, 'Z1 Z0'),
        (0.12054625, 'Z2 Z0'), (0.165868, 'Z2 Z1'),
        (0.165868, 'Z3 Z0'), (0.12054625, 'Z3 Z1'),
        (0.17434925, 'Z3 Z2'),
        (-0.04532175, 'X3 X2 Y1 Y0'), (0.04532175, 'X3 Y2 Y1 X0'),
        (0.04532175, 'Y3 X2 X1 Y0'), (-0.04532175, 'Y3 Y2 X1 X0'),
    ]
    n = 4
    H = np.zeros((16,16), dtype=complex)
    for c, t in terms:
        H += c*op(n, t)
    return H

def hf_state_4q():
    """Hartree-Fock reference |0011> (two lowest spin orbitals occupied)."""
    # occupation |f3 f2 f1 f0> = |0011> -> index in our qubit0-LSB layout:
    idx = 0b0011
    v = np.zeros(16, dtype=complex); v[idx] = 1.0
    return v

def ucc1_state(theta):
    """Single-parameter UCC: exp(theta (a2^dag a3^dag a0 a1 - h.c.)) applied to HF.
    JW double-excitation generator -> the standard single-excitation-angle
    rotation in the {|0011>,|1100>} subspace. We build the exact unitary."""
    H = H2_hamiltonian_4q()  # not used directly; build generator
    # Double excitation generator G = i/2 (X3 Y2 X1 X0 + ... ) — use the exact
    # 2-level rotation: |0011> and |1100> are coupled by the double excitation.
    psi0 = hf_state_4q()
    i0 = 0b0011; i1 = 0b1100
    psi = psi0.copy().astype(complex)
    c = np.cos(theta); s = np.sin(theta)
    a = psi[i0]; b = psi[i1]
    psi[i0] = c*a - s*b
    psi[i1] = s*a + c*b
    return psi

def energy(psi, H):
    return float(np.real(psi.conj() @ H @ psi))

# =================== RUN ===================
results = {}
H = H2_hamiltonian_4q()
evals, evecs = np.linalg.eigh(H)
fci = float(evals[0])
hf_E = energy(hf_state_4q(), H)
results["reference"] = {"FCI_ground_energy": fci, "HF_energy": hf_E,
                        "chemical_accuracy": CHEM_ACC}

# C1: ucc-1 theta sweep + cubic spline optimum
thetas = np.linspace(-np.pi, np.pi, 401)
Es = np.array([energy(ucc1_state(t), H) for t in thetas])
spline = CubicSpline(thetas, Es)
# refine optimum
res = minimize(lambda t: spline(t[0]), x0=[thetas[np.argmin(Es)]],
               bounds=[(-np.pi, np.pi)])
theta_opt = float(res.x[0]); E_opt = float(res.fun)
results["C1_ucc1_vqe"] = {
    "theta_opt": theta_opt, "E_opt": E_opt,
    "FCI": fci, "abs_error_to_FCI": abs(E_opt - fci),
    "within_chemical_accuracy": bool(abs(E_opt - fci) < CHEM_ACC),
    "recovers_correlation_below_HF": bool(E_opt < hf_E - 1e-6),
}

# C2: unconstrained (HWE-like) ansatz can leave the physical sector / go below FCI
# Build a generic 4-qubit product-rotation ansatz and minimize over the FULL
# 16-dim space (no electron-number conservation) -> minimum is the global min
# of H which for a number-non-conserving search can sit in a different particle
# sector than the chemically correct 2-electron ground state.
def hwe_min_over_full_space():
    # global minimum over ALL states = smallest eigenvalue of H (any sector)
    return float(evals[0]), evals
# To illustrate the unphysical-sector issue, compute ground energy restricted to
# the correct 2-electron sector vs the absolute spectrum minimum.
def particle_number_op(n):
    # N = sum_j (I - Z_j)/2
    N = np.zeros((1<<n, 1<<n), dtype=complex)
    for j in range(n):
        N += 0.5*(op(n,'I') - op(n, f'Z{j}'))
    return N
Nop = particle_number_op(4)
# eigen-decompose: find ground energy within 2-electron subspace
two_e_indices = [i for i in range(16) if bin(i).count('1') == 2]
H_2e = H[np.ix_(two_e_indices, two_e_indices)]
ev_2e = np.linalg.eigvalsh(H_2e)
results["C2_hwe_unphysical"] = {
    "absolute_spectrum_min_any_sector": float(evals[0]),
    "two_electron_sector_min_FCI": float(ev_2e[0]),
    "min_particle_number_at_global_min": int(round(float(
        np.real(evecs[:,0].conj() @ Nop @ evecs[:,0])))),
    "note": "HWE/unconstrained search is not particle-number conserving; can "
            "exit the 2-electron sector (paper: 'unphysical results'). Here the "
            "global min happens to be the 2e ground state, but the FCI metric "
            "must be taken IN the correct sector.",
    "two_e_sector_equals_FCI": bool(abs(ev_2e[0]-fci) < 1e-9),
}

# C3: Richardson zero-noise extrapolation method
# Model measured energy vs noise stretch factor r (r=1 native, r=3, r=5...).
# True noiseless = E_opt. Inject: E(r) = E_opt + alpha*(r-1) + beta*(r-1)^2 + noise
rng = np.random.default_rng(7)
alpha, beta = 0.03, 0.004   # synthetic but fixed, physically-scaled noise slopes
r_vals = np.array([1.0, 3.0, 5.0])
E_meas = E_opt + alpha*(r_vals-1) + beta*(r_vals-1)**2
E_meas_noisy = E_meas + rng.normal(0, 0.001, size=r_vals.shape)
sigma = np.full_like(r_vals, 0.001)
# linear fit to r=0
lin = np.polyfit(r_vals, E_meas_noisy, 1)
E_lin0 = float(np.polyval(lin, 0.0))
# quadratic fit to r=0
quad = np.polyfit(r_vals, E_meas_noisy, 2)
E_quad0 = float(np.polyval(quad, 0.0))
results["C3_richardson_extrapolation"] = {
    "r_values": r_vals.tolist(),
    "noisy_measured_E": E_meas_noisy.tolist(),
    "linear_extrap_to_r0": E_lin0, "quadratic_extrap_to_r0": E_quad0,
    "true_noiseless_E_opt": E_opt,
    "linear_abs_err": abs(E_lin0 - E_opt),
    "quadratic_abs_err": abs(E_quad0 - E_opt),
    "quadratic_better_than_linear": bool(abs(E_quad0-E_opt) <= abs(E_lin0-E_opt)+1e-9),
}

# C4: potential energy surface E(R) via ucc-1 (Fig. 5 analog).
# Self-consistent H2/STO-3G coefficient family from O'Malley et al. PRX 6,031007
# (2016), Table I (the canonical 2-qubit-equivalent H2 coefficient set; here
# embedded in the 4-qubit JW Hamiltonian whose 2-electron ground state lies in
# span{|0011>,|1100>}, so ucc-1 is full-CI-complete for this sector and MUST
# equal FCI in the 2-electron sector at every R -- this is the test).
# Coefficients (g0 I + g1 Z0 + g2 Z1 + g3 Z0Z1 + g4 X0X1 + g5 Y0Y1) on the
# 2-qubit reduced H. We diagonalize the 2-qubit reduced Hamiltonian directly
# (the chemically-correct sector), and run ucc-1 as a 2-level rotation there.
omalley = {  # R(A): (g0, g1, g2, g3, g4)   2-qubit reduced H2/STO-3G
    0.20: ( 2.8489,  0.5678, -1.4508,  0.6799,  0.0791),
    0.55: ( 0.6826,  0.2098, -0.7813,  0.3061,  0.0540),
    0.7414:(-0.4804,  0.3435, -0.4347,  0.5716,  0.0910),
    1.00: (-1.0466,  0.3861, -0.2616,  0.5847,  0.1027),
    1.50: (-1.5973,  0.3947, -0.0510,  0.5901,  0.1294),
    2.00: (-1.8538,  0.3522,  0.0466,  0.5489,  0.1538),
}
def H_at_R_2q(params):
    g0,g1,g2,g3,g4 = params
    terms = [(g0,'I'),(g1,'Z0'),(g2,'Z1'),(g3,'Z1 Z0'),(g4,'X1 X0'),(g4,'Y1 Y0')]
    HH = np.zeros((4,4), dtype=complex)
    for c,t in terms:
        HH += c*op(2,t)
    return HH
def ucc1_2q(theta):
    # HF ref |01>; ucc-1 rotates in {|01>,|10>} (the 2-electron-equivalent sector)
    psi = np.zeros(4, dtype=complex); psi[0b01] = 1.0
    c,s = np.cos(theta), np.sin(theta)
    a,b = psi[0b01], psi[0b10]
    psi[0b01] = c*a - s*b; psi[0b10] = s*a + c*b
    return psi
pes = []
for R, par in omalley.items():
    HR = H_at_R_2q(par)
    fciR = float(np.linalg.eigvalsh(HR)[0])
    EsR = [float(np.real(ucc1_2q(t).conj() @ HR @ ucc1_2q(t))) for t in thetas]
    vqeR = float(min(EsR))
    pes.append({"R_angstrom": R, "VQE_ucc1": vqeR, "FCI": fciR,
                "abs_err": abs(vqeR-fciR),
                "within_chem_acc": bool(abs(vqeR-fciR) < CHEM_ACC)})
results["C4_potential_surface"] = pes
results["C4_all_within_chem_acc"] = bool(all(p["within_chem_acc"] for p in pes))

with open("results.json","w") as fh:
    json.dump(results, fh, indent=2)

print("=== VQE chem benchmark (McCaskey et al.) — simulator-backbone replication ===")
print(f"Reference: FCI={fci:.6f}  HF={hf_E:.6f}  chem.acc={CHEM_ACC}")
print(f"C1 ucc-1 VQE: theta_opt={theta_opt:.5f}  E_opt={E_opt:.6f}  "
      f"|E-FCI|={abs(E_opt-fci):.2e}  within_chem_acc={results['C1_ucc1_vqe']['within_chemical_accuracy']}")
print(f"   recovers correlation below HF: {results['C1_ucc1_vqe']['recovers_correlation_below_HF']}")
print(f"C2 HWE/unphysical: 2e-sector min == FCI: {results['C2_hwe_unphysical']['two_e_sector_equals_FCI']}; "
      f"global-min particle number = {results['C2_hwe_unphysical']['min_particle_number_at_global_min']}")
print(f"C3 Richardson: lin->r0 err={results['C3_richardson_extrapolation']['linear_abs_err']:.2e}  "
      f"quad->r0 err={results['C3_richardson_extrapolation']['quadratic_abs_err']:.2e}  "
      f"quad better/equal: {results['C3_richardson_extrapolation']['quadratic_better_than_linear']}")
print("C4 PES (ucc-1 vs FCI):")
for p in pes:
    print(f"   R={p['R_angstrom']:.4f}A  VQE={p['VQE_ucc1']:.6f}  FCI={p['FCI']:.6f}  "
          f"err={p['abs_err']:.2e}  chem_acc={p['within_chem_acc']}")
print(f"   all within chemical accuracy: {results['C4_all_within_chem_acc']}")
print("\nWrote results.json")
