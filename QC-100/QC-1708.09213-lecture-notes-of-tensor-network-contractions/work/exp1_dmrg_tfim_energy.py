"""
Experiment 1 (Claim C1): DMRG / MPS variational ground-state energy
of the 1D transverse-field Ising model (TFIM) at criticality.

Paper: Ran et al., "Lecture Notes of Tensor Network Contractions"
      arXiv:1708.09213 (LNP vol 964, 2020).
      Sec 2.2 (MPS), Sec 3.4 (TEBD), Sec 5.1 (canonical MPS + optimal truncation),
      Sec 6.2 (QES on 1D TFIM, Eq 6.15-6.16).

Claim tested:  Variational MPS ground state of the 1D transverse-field Ising
Hamiltonian in the Pauli-operator convention
        H = - sum_i sigma^z_i sigma^z_{i+1}  -  h * sum_i sigma^x_i
at criticality (h=1) reproduces the exact ferromagnetic thermodynamic-limit
ground-state energy per site
        e_0(h=1) = - (2 / pi) * ( integral_0^{pi/2} 2 cos(theta) dtheta )   =  -4/pi
(equivalent to the Jordan-Wigner + Bogoliubov free-fermion diagonalization,
see Pfeuty 1970, Sachdev 'Quantum Phase Transitions' eq (5.42)).

We use quimb's DMRG2 (two-site DMRG) on finite chains N=20,40,60,80 with
bond dimension chi=32 and compare E_0/N against the free-fermion exact
value on the same finite N (open boundaries).

NOTE on convention: quimb's MPO_ham_ising uses spin-S operators (S=1/2 means
s^a = (1/2) sigma^a). To match the *Pauli* convention we set  j = -4 (for the
ZZ term: -1 * sigma^z sigma^z = -1 * (2 s^z)(2 s^z) = -4 s^z s^z) and
bx = -2 (for the X term: -h sigma^x = -h * 2 s^x -> bx=-2h with h=1).
"""
import json, time, math
import numpy as np
import quimb as qu
import quimb.tensor as qtn

def exact_tfim_open_ff(N, h, J=1.0):
    """
    Exact ground-state energy of the 1D TFIM with OPEN boundary conditions
    via Jordan-Wigner + Bogoliubov (free-fermion diagonalization),
    Pauli convention  H = -J sum sigma^z sigma^z - h sum sigma^x.

    Following Pfeuty (Ann Phys 57, 79 (1970)) / Lieb-Schultz-Mattis:
        E_0 = - sum_n epsilon_n
    where epsilon_n = sqrt(eigenvalues of (A-B)(A+B)) and
        A_ii = -h,  A_{i,i+1} = A_{i+1,i} = -J/2
        B_{i,i+1} = -J/2, B_{i+1,i} = +J/2.
    Verified against exact diagonalization to 1e-14 for N=6..12 (see exp1b).
    """
    A = np.zeros((N, N))
    B = np.zeros((N, N))
    for i in range(N):
        A[i, i] = -h
    for i in range(N - 1):
        A[i, i + 1] = A[i + 1, i] = -J / 2
        B[i, i + 1] = -J / 2
        B[i + 1, i] = +J / 2
    Msq = (A - B) @ (A + B)
    w = np.linalg.eigvalsh(Msq)
    w = np.clip(w, 0.0, None)
    eps = np.sqrt(w)
    return float(-np.sum(eps))


def build_tfim_mpo(N, h, J=1.0):
    """MPO for H = -J sigma^z sigma^z - h sigma^x (Pauli operators).

    quimb's MPO_ham_ising uses spin-1/2 operators s^a = (1/2)sigma^a, so we
    convert:  -J sigma^z sigma^z  = -J (2 s^z)(2 s^z) = -4J s^z s^z, hence j=-4J.
                -h sigma^x        = -h (2 s^x)           = -2h s^x,     hence bx=-2h.
    """
    return qtn.MPO_ham_ising(N, j=-4.0 * J, bx=-2.0 * h, S=0.5, cyclic=False)


def run_dmrg(N, h, chi=32, tol=1e-10):
    H = build_tfim_mpo(N, h)
    dmrg = qtn.DMRG2(H, bond_dims=[8, 16, chi], cutoffs=1e-12)
    dmrg.solve(tol=tol, verbosity=0)
    E = dmrg.energy
    return E, dmrg.state


def main():
    h = 1.0
    J = 1.0
    results = []
    for N in [20, 40, 60, 80]:
        t0 = time.time()
        E_dmrg, psi = run_dmrg(N, h)
        t_dmrg = time.time() - t0
        E_exact = exact_tfim_open_ff(N, h, J)
        rel_err = abs(E_dmrg - E_exact) / abs(E_exact)
        per_site_dmrg = E_dmrg / N
        per_site_exact = E_exact / N
        row = dict(
            N=N,
            h=h,
            chi=32,
            E_dmrg=float(E_dmrg),
            E_exact_ff=float(E_exact),
            per_site_dmrg=float(per_site_dmrg),
            per_site_exact_ff=float(per_site_exact),
            abs_err=float(abs(E_dmrg - E_exact)),
            rel_err=float(rel_err),
            dmrg_time_s=float(t_dmrg),
        )
        results.append(row)
        print(
            f"N={N:3d}  chi=32   E_DMRG={E_dmrg:.8f}   E_FF={E_exact:.8f}   "
            f"e_DMRG={per_site_dmrg:.6f}   e_FF={per_site_exact:.6f}   "
            f"rel_err={rel_err:.2e}   t={t_dmrg:.1f}s"
        )
    thermo_limit_exact = -4.0 / math.pi
    print(f"\nThermodynamic-limit exact e_0(h=1) = -4/pi = {thermo_limit_exact:.8f}")
    # Extrapolate DMRG per-site energy to N->infinity (linear in 1/N)
    Ns = np.array([r["N"] for r in results])
    es = np.array([r["per_site_dmrg"] for r in results])
    slope, intercept = np.polyfit(1.0 / Ns, es, 1)
    print(
        f"Linear extrapolation DMRG e_0(N->inf): {intercept:.6f}  "
        f"(vs -4/pi = {thermo_limit_exact:.6f}, delta = {intercept - thermo_limit_exact:+.2e})"
    )
    out = dict(
        experiment="C1_dmrg_tfim_energy",
        hamiltonian="H = -sum Z_i Z_{i+1} - h sum X_i, open BC",
        h=h,
        J=J,
        per_N=results,
        thermo_limit_exact_minus_4_over_pi=float(thermo_limit_exact),
        dmrg_extrapolated_e0=float(intercept),
        dmrg_extrapolated_e0_minus_exact=float(intercept - thermo_limit_exact),
    )
    with open("../report/evidence/exp1_dmrg_tfim.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote report/evidence/exp1_dmrg_tfim.json")


if __name__ == "__main__":
    main()
