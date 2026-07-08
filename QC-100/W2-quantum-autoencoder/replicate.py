#!/usr/bin/env python3
"""
Replication of the core method of:
  Romero, Olson, Aspuru-Guzik, "Quantum autoencoders for efficient compression
  of quantum data," Quantum Sci. Technol. 2, 045001 (2017). arXiv:1612.02806.

CORE CLAIM tested (classical statevector replication):
  A parameterized "encoder" circuit U(theta) on n qubits can compress an input
  state into k < n "latent" qubits by training U so that the remaining (n-k)
  "trash" qubits are disentangled and driven to a fixed reference |0...0>.
  The training cost is the trash-qubit fidelity with |0>. After training, the
  decoder U^dagger reconstructs the input with high fidelity. Reconstruction
  fidelity is high when the latent size is large enough to hold the data's
  effective support, and DEGRADES when compressed too aggressively.

We:
  1. Build a small family of correlated input states living (approximately) in a
     low-dimensional subspace of an n=4 qubit register.
  2. Train a hardware-efficient encoder by MAXIMIZING average trash-qubit |0>
     fidelity (equivalently minimizing 1 - F_trash), the paper's cost function.
  3. Decode (apply U^dagger after resetting trash to |0>) and measure
     reconstruction fidelity with the original input.
  4. Sweep the number of trash qubits (n-k) to show fidelity-vs-compression.

numpy + scipy.optimize only. Statevector sim. n=4.
"""
import numpy as np
from scipy.optimize import minimize
import json

rng = np.random.default_rng(20260626)

# ---- gates ----
I2=np.eye(2,dtype=complex)
def Ry(t): c,s=np.cos(t/2),np.sin(t/2); return np.array([[c,-s],[s,c]],dtype=complex)
def Rz(t): return np.array([[np.exp(-1j*t/2),0],[0,np.exp(1j*t/2)]],dtype=complex)

def op_on(g,q,n):
    out=np.array([[1]],dtype=complex)
    for i in range(n):
        out=np.kron(out, g if i==q else I2)
    return out

def cnot(ctrl,tgt,n):
    dim=2**n; M=np.zeros((dim,dim),dtype=complex)
    for b in range(dim):
        bits=[(b>>(n-1-i))&1 for i in range(n)]
        if bits[ctrl]==1: bits[tgt]^=1
        nb=0
        for i in range(n): nb=(nb<<1)|bits[i]
        M[nb,b]=1
    return M

def encoder_unitary(theta, n, depth=3):
    """Hardware-efficient ansatz: layers of Ry,Rz on each qubit + linear CNOT chain."""
    U=np.eye(2**n,dtype=complex)
    idx=0
    for d in range(depth):
        for q in range(n):
            U = op_on(Ry(theta[idx]),q,n) @ U; idx+=1
            U = op_on(Rz(theta[idx]),q,n) @ U; idx+=1
        for q in range(n-1):
            U = cnot(q,q+1,n) @ U
    return U

def n_params(n,depth=3): return depth*n*2

def make_input_family(n, n_states=6, eff_dim=2, seed=0):
    """
    Inputs living near an eff_dim-dimensional subspace of the n-qubit space:
    pick eff_dim fixed random basis vectors, each input = random combo + small
    noise. Compressible to ceil(log2(eff_dim)) latent qubits in principle.
    """
    r=np.random.default_rng(seed)
    dim=2**n
    basis=[r.normal(size=dim)+1j*r.normal(size=dim) for _ in range(eff_dim)]
    # orthonormalize
    B=np.array(basis).T
    Q,_=np.linalg.qr(B)
    states=[]
    for _ in range(n_states):
        coef=r.normal(size=eff_dim)+1j*r.normal(size=eff_dim)
        v=Q@coef
        v=v/np.linalg.norm(v)
        states.append(v)
    return states

def trash_zero_fidelity(psi, n, n_trash):
    """
    Fidelity that the last n_trash qubits are in |0>: sum of |amp|^2 over
    computational basis states whose trash bits are all 0.
    """
    dim=2**n
    f=0.0
    for b in range(dim):
        trash_bits=b & ((1<<n_trash)-1)   # last n_trash bits
        if trash_bits==0:
            f+=abs(psi[b])**2
    return f

def reconstruct(psi_in, U, n, n_trash):
    """Encode, project/reset trash to |0>, decode."""
    enc = U @ psi_in
    # reset trash qubits to |0>: keep only amplitudes with trash=0, renormalize,
    # then place latent content with trash=|0>
    dim=2**n
    reset=np.zeros(dim,dtype=complex)
    for b in range(dim):
        if (b & ((1<<n_trash)-1))==0:
            reset[b]=enc[b]
    nrm=np.linalg.norm(reset)
    if nrm<1e-12: return np.zeros(dim,dtype=complex)
    reset/=nrm
    dec = U.conj().T @ reset
    return dec

def train_and_eval(n, n_trash, inputs, depth=3, restarts=4):
    npar=n_params(n,depth)
    def cost(theta):
        U=encoder_unitary(theta,n,depth)
        # maximize avg trash fidelity -> minimize (1 - avg)
        fs=[trash_zero_fidelity(U@psi,n,n_trash) for psi in inputs]
        return 1.0-np.mean(fs)
    best=None
    for _ in range(restarts):
        x0=rng.uniform(-np.pi,np.pi,npar)
        res=minimize(cost,x0,method='COBYLA',options={'maxiter':800,'rhobeg':0.4})
        if best is None or res.fun<best.fun: best=res
    U=encoder_unitary(best.x,n,depth)
    train_trash_fid=np.mean([trash_zero_fidelity(U@psi,n,n_trash) for psi in inputs])
    recon_fids=[abs(np.vdot(psi, reconstruct(psi,U,n,n_trash)))**2 for psi in inputs]
    return train_trash_fid, float(np.mean(recon_fids)), [float(x) for x in recon_fids]

def main():
    n=4
    eff_dim=2  # data ~ 2D subspace -> needs ~1 latent qubit, compressible
    inputs=make_input_family(n,n_states=6,eff_dim=eff_dim,seed=1)
    print(f"n={n} qubits, data effective dim={eff_dim} (compressible to ~{int(np.ceil(np.log2(eff_dim)))} latent qubit)")
    results={'n':n,'eff_dim':eff_dim,'sweep':[]}
    print(f"\n{'n_trash':>8} {'latent_k':>8} {'train_Ftrash':>13} {'recon_fid':>10}")
    for n_trash in [1,2,3]:
        k=n-n_trash
        tt,rf,rfs=train_and_eval(n,n_trash,inputs)
        results['sweep'].append({'n_trash':n_trash,'latent_k':k,'train_trash_fid':tt,
                                 'recon_fid_mean':rf,'recon_fids':rfs})
        print(f"{n_trash:>8} {k:>8} {tt:>13.4f} {rf:>10.4f}")
    json.dump(results,open('results.json','w'),indent=2)
    print("\nWrote results.json")
    # headline interpretation
    sw=results['sweep']
    print("\nInterpretation:")
    print(f"  - Data lives in a {eff_dim}-dim subspace -> compressible.")
    for s in sw:
        verdict="HIGH" if s['recon_fid_mean']>0.95 else ("OK" if s['recon_fid_mean']>0.8 else "DEGRADED")
        print(f"  - compress to k={s['latent_k']} (discard {s['n_trash']}): recon F={s['recon_fid_mean']:.3f} [{verdict}]")

if __name__=="__main__":
    main()
