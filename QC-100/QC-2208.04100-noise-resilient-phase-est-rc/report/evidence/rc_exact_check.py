"""
Supplementary EXACT (shot-noise-free) check for arXiv:2208.04100 replication.

Goal: the sampled Aer run showed RC error floored at the shot-noise level (~1e-4),
so the RC power-law exponent (paper: ~2.73) could not be recovered from sampled data.
Here we compute the EXACT twirled expectation value (full 4^L Pauli average is
intractable, but the single-qubit twirl of a coherent Rz(eps) noise per cycle
factorizes: the twirl of channel N over the Pauli group acting on each cycle
independently gives, in expectation, a per-cycle stochastic Pauli channel). We
compute the exact ensemble-averaged P(0|L) analytically by averaging the density
matrix over all 4^L Pauli assignments via the per-cycle twirled channel, which is
a product of L identical single-qubit twirled channels. This is exact and cheap.

We then estimate phi from the exact averaged curve and measure the residual-bias
power law vs eps -- this is the fair, shot-noise-free test of the RC scaling claim.
"""
import numpy as np

PHI = 0.37123456
L_LIST = [1,2,4,8,16,32,64,100]

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
PAULIS = [I,X,Y,Z]
H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

def rz(a):
    return np.array([[np.exp(-1j*a/2),0],[0,np.exp(1j*a/2)]], dtype=complex)

def twirled_cycle_channel(eps):
    """Return function rho -> (1/4) sum_P P (U_ideal Rz(eps)) rho (U_ideal Rz(eps))^dag ... 
    Actually twirl conjugates ONLY the noise (matches evidence construction:
    U_ideal ; P ; Rz(eps) ; P^dag). Net per-cycle map on rho:
      M(rho) = U_ideal * [ (1/4) sum_P  P Rz(eps) P^dag rho P Rz(eps)^dag P^dag ] * U_ideal^dag
    We build the 2x2 x 2x2 superoperator (on vec(rho)) and return it."""
    Uid = rz(2*PHI)
    # twirled noise superoperator
    S = np.zeros((4,4), dtype=complex)
    for P in PAULIS:
        K = P @ rz(eps) @ P            # P Rz(eps) P (P self-inverse)
        S += np.kron(K.conj(), K)      # vec: (A rho A^dag) -> kron(A.conj, A)
    S /= 4.0
    # then apply ideal U: rho -> Uid rho Uid^dag
    SU = np.kron(Uid.conj(), Uid)
    return SU @ S

def p0_exact_rc(L, eps):
    Uid = rz(2*PHI)
    M = twirled_cycle_channel(eps)          # per-cycle 4x4 superop
    # initial state |0>, then H
    rho0 = np.array([[1,0],[0,0]], dtype=complex)
    rho0 = H @ rho0 @ H.conj().T
    v = rho0.reshape(-1)                     # vec (row-major matches kron(A.conj,A) with reshape)
    ML = np.linalg.matrix_power(M, L)
    v = ML @ v
    rho = v.reshape(2,2)
    rho = H @ rho @ H.conj().T               # final H
    p0 = np.real(rho[0,0])
    return float(p0)

def p0_exact_bare(L, eps):
    U = rz(2*PHI) @ rz(eps)
    UL = np.linalg.matrix_power(U, L)
    psi = H @ np.array([1,0], dtype=complex)
    psi = UL @ psi
    psi = H @ psi
    return float(abs(psi[0])**2)

def estimate_phi(p0_list):
    p0 = np.array(p0_list); L = np.array(L_LIST, float)
    phis = np.linspace(PHI-0.5, PHI+0.5, 200001)
    best=None
    for phi in phis:
        pred=(1+np.cos(2*phi*L))/2
        e=float(np.sum((p0-pred)**2))
        if best is None or e<best[0]: best=(e,float(phi))
    return best[1]

EPS = [0.01,0.02,0.04,0.08,0.15,0.25,0.4]
print("# EXACT (shot-noise-free) residual-bias check")
print(f"# phi_true={PHI}")
eb=[]; er=[]
for eps in EPS:
    pb=[p0_exact_bare(L,eps) for L in L_LIST]
    pr=[p0_exact_rc(L,eps)   for L in L_LIST]
    fb=estimate_phi(pb); fr=estimate_phi(pr)
    e_b=abs(fb-PHI); e_r=abs(fr-PHI)
    eb.append(e_b); er.append(e_r)
    print(f"eps={eps:5.3f} | bare err={e_b:.3e} | rc err={e_r:.3e} | ratio={e_b/max(e_r,1e-15):.1f}")

eb=np.array(eb); er=np.array(er); ex=np.array(EPS)
sb=np.polyfit(np.log(ex),np.log(np.maximum(eb,1e-15)),1)[0]
sr=np.polyfit(np.log(ex),np.log(np.maximum(er,1e-15)),1)[0]
print()
print(f"EXACT power-law: bare err~eps^{sb:.3f} (paper ~1.04) ; RC err~eps^{sr:.3f} (paper ~2.73)")
print(f"slope gap = {sr-sb:.3f} (paper ~1.7)")
