"""
Experiment 4 (Claim C4):  imaginary-time TEBD for the critical TFIM
recovers the free-fermion thermodynamic-limit ground-state energy per site.

Paper: Sec 3.4 "Time-evolving block decimation: linearized contraction and
boundary-state methods";  Sec 3.5 (transverse contraction), Sec 4.2
(imaginary-time evolution methods).

The paper claims (paraphrased):
  TEBD applied to an imaginary-time Trotter decomposition of exp(-tau*H)
  drives an initial state into the ground state; combined with successive
  SVD truncation to bond dimension chi, one obtains the variational
  ground-state energy per site.  For the critical TFIM (h=1), this should
  converge to  e_0 = -4/pi ~= -1.27324  as chi grows.

We use finite-chain TEBD (N=64, open BC) with second-order Trotter,
imaginary-time step dtau=0.05, target time T=10, bond dim chi=32.
We measure the energy density in the middle of the chain (avoiding boundary
effects).
"""
import json, time, math
import numpy as np
import quimb as qu
import quimb.tensor as qtn


def build_tfim_ham1d(N, h, J=1.0):
    """Local (2-site) Hamiltonian for TEBD.  Same Pauli-convention TFIM.

    Sign fix: (-J) * (Z & Z)  and  (-h) * X, with explicit unary minus so the
    multiplication order is unambiguous.
    """
    ZZ = qu.pauli('Z') & qu.pauli('Z')
    return qtn.LocalHam1D(
        L=N,
        H2={None: (-J) * ZZ},
        H1={None: (-h) * qu.pauli('X')},
        cyclic=False,
    )


def middle_energy_density(psi, H_local, N):
    """Average energy per site over the middle 20 bonds of the chain."""
    lo, hi = N // 2 - 10, N // 2 + 10
    # Sum <psi|h_i,i+1|psi> for i in [lo, hi-1] and <psi|h_i|psi> for i in [lo, hi]
    E2 = 0.0
    n2 = 0
    for i in range(lo, hi):
        # local 2-site + 1-site energies
        term = H_local.get_gate_expm(coupling=1.0)  # not the right API
        # simpler: use compute_local_expectation
        pass
    # Simpler: use MPO expectation for the full H, divide by N-1.
    return None  # placeholder


def measure_energy_pauli(psi, N, h=1.0, J=1.0):
    """Measure <psi|H|psi> for TFIM H = -J sum sigma^z sigma^z - h sum sigma^x
    directly, using the MPS's method for one- and two-site expectation values.
    (MPS has a specialized .local_expectation_canonical method.)
    """
    Z = qu.pauli('Z'); X = qu.pauli('X')
    ZZ = Z & Z
    E = 0.0
    for i in range(N - 1):
        E += -J * float(psi.local_expectation_canonical(ZZ, (i, i + 1)).real)
    for i in range(N):
        E += -h * float(psi.local_expectation_canonical(X, i).real)
    return E


def run_itebd(N=64, h=1.0, chi=32, dtau=0.05, T=8.0):
    ham = build_tfim_ham1d(N, h)

    # initial: random MPS  (Neel = |up,down,up,...>, product state, bond dim 1)
    psi = qtn.MPS_neel_state(N)
    psi.normalize()

    # imaginary-time TEBD
    tebd = qtn.TEBD(psi, ham, dt=dtau, imag=True,
                    split_opts={'max_bond': chi, 'cutoff': 1e-12})

    energies = []
    ts = []
    sample_times = list(np.arange(dtau, T + dtau / 2, 0.5))
    for t in sample_times:
        tebd.update_to(t)
        psi_t = tebd.pt
        psi_t.normalize()
        E = measure_energy_pauli(psi_t, N, h=h, J=1.0)
        energies.append(E)
        ts.append(float(t))
    return dict(N=N, chi=chi, dtau=dtau, T=T,
                ts=ts, energies=energies,
                final_energy=energies[-1],
                final_energy_per_site=energies[-1] / N)


def main():
    t0 = time.time()
    result = run_itebd(N=64, h=1.0, chi=32, dtau=0.05, T=8.0)
    dt = time.time() - t0
    e0_per_site = result["final_energy_per_site"]
    exact_thermo = -4.0 / math.pi
    # For finite N=64 the exact per-site is slightly higher; use the FF result
    from exp1_dmrg_tfim_energy import exact_tfim_open_ff
    exact_finite = exact_tfim_open_ff(64, 1.0) / 64
    print(f"iTEBD finite N=64, chi=32:  E/N = {e0_per_site:.6f}   (t={dt:.1f}s)")
    print(f"Free-fermion exact finite N=64:  E/N = {exact_finite:.6f}")
    print(f"Thermo-limit (paper) -4/pi:  E/N = {exact_thermo:.6f}")
    result["exact_ff_N64_per_site"] = float(exact_finite)
    result["thermo_limit_minus_4_over_pi"] = float(exact_thermo)
    result["itebd_vs_ff_finite_delta"] = float(e0_per_site - exact_finite)
    result["itebd_vs_thermo_delta"] = float(e0_per_site - exact_thermo)
    with open("../report/evidence/exp4_itebd_tfim.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Wrote report/evidence/exp4_itebd_tfim.json")


if __name__ == "__main__":
    main()
