#!/usr/bin/env python3
"""
Replication of:
  Griffiths & Niu, "Semiclassical Fourier Transform for Quantum Computation,"
  Phys. Rev. Lett. 76, 3228 (1996). arXiv:quant-ph/9511007.

CORE CLAIM (algorithm equivalence):
  In phase estimation, the inverse Quantum Fourier Transform on the k counting
  qubits can be replaced by a SEMICLASSICAL procedure: measure the qubits one at
  a time (most-significant first in the standard QPE convention; here we follow
  the standard "measure LSB-of-the-iQFT first" Kitaev/Griffiths-Niu ordering),
  and apply single-qubit Z-rotations to the not-yet-measured qubits CONDITIONED
  on the classical measurement outcomes. This uses only single-qubit gates +
  feed-forward and produces EXACTLY the same output bit distribution as the full
  coherent inverse QFT.

We verify exact equivalence by computing, for each method, the full probability
distribution over k-bit outcomes (no sampling needed for the distribution — we
propagate amplitudes/probabilities exactly), for many eigenphases phi and bit
counts k, and confirm total-variation distance = 0 (machine precision).

numpy only. The key correctness subtlety (which a naive implementation gets
wrong) is BIT ORDERING: standard QPE produces the estimate with the QFT's
natural bit reversal. We make the convention explicit and identical for both
methods, so any agreement/disagreement is about the ALGORITHM, not endianness.

Setup: single-qubit phase gate U|1> = e^{2 pi i phi}|1>, eigenstate |1> in the
target register. After the Hadamard-controlled-U^{2^j} ladder, counting qubit j
(j=0..k-1, j=0 the LSB) holds phase e^{2 pi i (2^j phi)}. The exact pre-iQFT
counting-register state is the product state
   |psi> = prod_j (|0> + e^{2 pi i 2^j phi} |1>)/sqrt2 .
Both methods act on this same |psi>.
"""
import numpy as np
import json

def counting_state(phi, k):
    """Product state after the controlled-U ladder; qubit j has phase 2^j phi.
       Return as a length-2^k statevector with qubit 0 = LSB (rightmost bit)."""
    # Build per-qubit single-qubit states then kron in order qubit (k-1)...0
    # We index basis by integer y = sum_j b_j 2^j  (b_j is bit of qubit j).
    psi = np.ones(1, dtype=complex)
    # kron from most significant (qubit k-1) down to least (qubit 0) so that
    # the resulting vector index has qubit0 as the LSB.
    for j in range(k-1, -1, -1):
        ph = np.exp(2j*np.pi*(2**j)*phi)
        qubit = np.array([1.0, ph], dtype=complex)/np.sqrt(2)
        psi = np.kron(psi, qubit)
    return psi

def inverse_qft_matrix(k):
    n = 2**k
    F = np.zeros((n, n), dtype=complex)
    w = np.exp(-2j*np.pi/n)   # inverse QFT
    for a in range(n):
        for b in range(n):
            F[a, b] = w**(a*b)
    return F/np.sqrt(n)

def qft_method_distribution(phi, k):
    """Apply the full inverse QFT, return probability over outcomes y (with the
       standard QPE bit-reversal applied so y/2^k estimates phi)."""
    psi = counting_state(phi, k)
    F = inverse_qft_matrix(k)
    out = F @ psi
    probs = np.abs(out)**2
    # With this state-build convention the raw iQFT index y already satisfies
    # y/2^k = phi (verified on exactly-representable phases). No bit reversal.
    return probs

def semiclassical_distribution(phi, k):
    """
    Semiclassical (measured) inverse QFT via exact probability propagation.
    Griffiths-Niu: measure qubit 0 (LSB) first; based on its outcome, apply a
    classically-conditioned Z-phase to the remaining qubits before measuring the
    next, etc. We enumerate ALL measurement-outcome branches and accumulate exact
    probabilities -> gives the full distribution with no sampling.

    Equivalent formulation: the probability of outcome bits (m_0,...,m_{k-1}) is
       prod over qubits of single-qubit measurement probs, where each qubit's
       effective phase is corrected by the already-measured lower bits.
    We implement it directly as the branch-product, which is mathematically the
    measured-QFT, and check it equals the coherent iQFT distribution.
    """
    # Iterative phase estimation (Griffiths-Niu / Kitaev). Measure the qubit
    # carrying phase 2^{k-1} phi FIRST -> that yields the LEAST significant bit
    # of the estimate; feed it forward to correct subsequent (higher-significance)
    # measurements. Bit b_i (i=0 is the LSB of the estimate y) is obtained when
    # processing the qubit with phase 2^{k-1-i} phi, after subtracting the phase
    # implied by the already-measured lower bits.
    #
    # Estimate y = sum_i b_i 2^i, with phi ~ y/2^k. We enumerate all branches and
    # accumulate exact probabilities.
    probs = np.zeros(2**k)
    for outcome in range(2**k):
        b = [(outcome>>i)&1 for i in range(k)]   # b[i] = i-th estimate bit (LSB i=0)
        p = 1.0
        for i in range(k):
            # step i measures the qubit with phase 2^{k-1-i} phi
            theta = (2**(k-1-i))*phi
            # feedback: subtract 0.0...0 b_{i-1} ... b_0 (the lower bits already known)
            # already-measured bits are b_0..b_{i-1}; their contribution to this
            # qubit's phase is sum_{l<i} b_l * 2^{-(i-l+1)}
            corr = 0.0
            for l in range(i):
                corr += b[l] / (2**(i-l+1))
            angle = theta - corr
            frac = angle - np.floor(angle)
            p0 = np.cos(np.pi*frac)**2
            p1 = np.sin(np.pi*frac)**2
            p *= (p0 if b[i]==0 else p1)
        y = sum(b[i]<<i for i in range(k))
        probs[y] += p
    return probs

def run():
    experiments=[]
    phis=[0.375, 0.0625, 0.8125, 0.46875, 0.5, 0.1, 0.7, 0.333333]
    ks=[3,4,4,5,3,4,4,5]
    max_tv=0.0
    for phi,k in zip(phis,ks):
        pq=qft_method_distribution(phi,k)
        ps=semiclassical_distribution(phi,k)
        tv=0.5*np.sum(np.abs(pq-ps))
        max_tv=max(max_tv,tv)
        yq=int(np.argmax(pq)); ys=int(np.argmax(ps))
        experiments.append({
            'phi_true':phi,'k':k,
            'qft_mode_y':yq,'qft_phi_est':yq/2**k,
            'sc_mode_y':ys,'sc_phi_est':ys/2**k,
            'tv_distance':tv,
            'mode_match':yq==ys,
        })
        print(f"phi={phi:.5f} k={k}: QFT->{yq/2**k:.5f}  SC->{ys/2**k:.5f}  TV={tv:.2e}  match={yq==ys}")
    summary={
        'paper':'Griffiths & Niu, Semiclassical Fourier Transform (PRL 1996)',
        'n_experiments':len(experiments),
        'max_tv_distance':max_tv,
        'all_modes_match':all(e['mode_match'] for e in experiments),
        'equivalence':'EXACT' if max_tv<1e-9 else 'APPROX' if max_tv<1e-3 else 'DISAGREEMENT',
        'experiments':experiments,
    }
    json.dump(summary,open('results.json','w'),indent=2)
    print(f"\nmax TV distance over all experiments: {max_tv:.3e}")
    print(f"equivalence verdict: {summary['equivalence']}")
    print("Wrote results.json")

if __name__=="__main__":
    run()
