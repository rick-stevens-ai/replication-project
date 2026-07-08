"""
Experiment 2 (Claim C2):  CFT entanglement-entropy scaling of the
critical TFIM ground state.

The paper (Sec 2.4.3 'Tensor network and quantum entanglement', Sec 5.1
'canonicalization of matrix product state', and general TN pedagogy)
emphasizes that for critical 1D systems the half-chain / block entropy
grows LOGARITHMICALLY with block size, controlled by the CFT central
charge c per Calabrese-Cardy:
    S(l) = (c/6) log( (2N/pi) sin(pi l / N) ) + const     (open BC)
For TFIM at criticality, c = 1/2 (Ising CFT).

We diagonalize the DMRG ground state of TFIM at h=1 for N=32, 64, 128
and extract S(l) for l = 1..N-1, then fit  S = (c/6) * log(chord(l)) + a.
"""
import json, math, time
import numpy as np
import quimb as qu, quimb.tensor as qtn


def build_tfim_mpo(N, h, J=1.0):
    return qtn.MPO_ham_ising(N, j=-4.0 * J, bx=-2.0 * h, S=0.5, cyclic=False)


LN2 = math.log(2)

def block_entropy(psi_mps, l):
    """
    von-Neumann entropy IN NATS of the left block of size l on an MPS.
    quimb's .entropy() returns entropy in log-2 units (bits); convert.
    psi_mps is a quimb MatrixProductState (finite, open BC).
    """
    psi = psi_mps.copy()
    psi.canonize(l)
    return float(psi.entropy(l)) * LN2


def chord(l, N):
    return (2 * N / math.pi) * math.sin(math.pi * l / N)


def run_case(N, chi=64, h=1.0):
    t0 = time.time()
    H = build_tfim_mpo(N, h)
    dmrg = qtn.DMRG2(H, bond_dims=[8, 16, 32, chi], cutoffs=1e-12)
    dmrg.solve(tol=1e-10, verbosity=0)
    psi = dmrg.state
    t_dmrg = time.time() - t0
    # Compute S(l) for all bonds
    ls, Ss, chords = [], [], []
    for l in range(1, N):
        S = block_entropy(psi, l)
        ls.append(l)
        Ss.append(S)
        chords.append(chord(l, N))
    return dict(
        N=N, chi=chi, dmrg_energy=float(dmrg.energy), dmrg_time_s=t_dmrg,
        ls=ls, S=Ss, chord=chords,
    )


def fit_c(chords, Ss, N, l_edge_cut=None):
    """
    Fit S = (c/6) log(chord) + a  restricted to the middle of the chain
    (avoid l too small / too large where lattice corrections dominate).
    """
    if l_edge_cut is None:
        l_edge_cut = max(4, N // 8)
    ls = np.arange(1, len(Ss) + 1)
    mask = (ls >= l_edge_cut) & (ls <= (N - l_edge_cut))
    x = np.log(np.array(chords)[mask])
    y = np.array(Ss)[mask]
    slope, intercept = np.polyfit(x, y, 1)
    c_fit = 6 * slope
    return float(c_fit), float(slope), float(intercept), int(mask.sum())


def main():
    all_out = []
    for N in [32, 64, 128]:
        case = run_case(N, chi=64, h=1.0)
        c_fit, slope, intercept, npts = fit_c(case["chord"], case["S"], N)
        case["fit_center_c"] = c_fit
        case["fit_slope"] = slope
        case["fit_intercept"] = intercept
        case["fit_npoints"] = npts
        case["c_reference"] = 0.5
        case["c_fit_minus_ref"] = c_fit - 0.5
        all_out.append(case)
        print(f"N={N:3d}  chi={case['chi']}   E={case['dmrg_energy']:.6f}   "
              f"fit c = {c_fit:.4f} (ref 0.500, delta={c_fit-0.5:+.4f}, n={npts})   "
              f"t={case['dmrg_time_s']:.1f}s")
    out = dict(
        experiment="C2_entanglement_scaling_central_charge",
        model="TFIM critical (h=1)",
        formula="S(l) = (c/6) log( (2N/pi) sin(pi l / N) ) + const",
        c_reference=0.5,
        cases=all_out,
    )
    with open("../report/evidence/exp2_entanglement_scaling.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote report/evidence/exp2_entanglement_scaling.json")


if __name__ == "__main__":
    main()
