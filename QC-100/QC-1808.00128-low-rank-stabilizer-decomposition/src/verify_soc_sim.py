"""
Faithful sum-over-Cliffords check on a REAL Clifford+T circuit.

Tests the paper's core algorithmic claim (Sec 2.3.2 / Eq.17-20): a Clifford+T
circuit U can be written U = sum_j c_j K_j with each K_j Clifford, using the
EXACT rank-2 single-T decomposition T = a*I + b*S (paper Eq.27 with theta=pi/4,
lifting lemma). Summing all 2^t Clifford branches must equal the exact statevector
to machine precision; this validates the decomposition that underlies the whole
low-rank simulator. We then keep only k random branches (importance sampling,
Bravyi/Gosset Sec.4 of Ref[11]) and show the estimate converges.

The earlier exp2 used WRONG coefficients (a=(1+e^{i pi/4})/2). The correct exact
solution of T = a I + b S is a = 1-b, b = (e^{i pi/4}-1)/(i-1).
"""
from __future__ import annotations
import itertools, json, math, os
import numpy as np

I2=np.eye(2,dtype=complex)
H=(1/math.sqrt(2))*np.array([[1,1],[1,-1]],dtype=complex)
S=np.array([[1,0],[0,1j]],dtype=complex)
T=np.array([[1,0],[0,np.exp(1j*math.pi/4)]],dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)

# EXACT rank-2 decomposition of T
_e=np.exp(1j*math.pi/4); B=(_e-1)/(1j-1); A=1-B
assert np.allclose(A*I2+B*S, T), "T=aI+bS failed"

def apply1(state,g,q,n):
    st=state.reshape([2]*n); st=np.tensordot(g,st,axes=([1],[q])); st=np.moveaxis(st,0,q); return st.reshape(2**n)
def applycx(state,c,t,n):
    st=state.reshape([2]*n); g=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex).reshape(2,2,2,2)
    st=np.tensordot(g,st,axes=([2,3],[c,t])); st=np.moveaxis(st,[0,1],[c,t]); return st.reshape(2**n)

def run(n,circ):
    st=np.zeros(2**n,dtype=complex); st[0]=1
    for name,qs in circ:
        if name=="H": st=apply1(st,H,qs[0],n)
        elif name=="S": st=apply1(st,S,qs[0],n)
        elif name=="T": st=apply1(st,T,qs[0],n)
        elif name=="X": st=apply1(st,X,qs[0],n)
        elif name=="CX": st=applycx(st,qs[0],qs[1],n)
    return st

def expZ(st,q,n):
    p=np.abs(st)**2; v=0
    for i,pp in enumerate(p):
        v+=(1-2*((i>>(n-1-q))&1))*pp
    return float(np.real(v))

def branch(n,circ,bits):
    coeff=1+0j; mod=[]; it=iter(bits)
    for name,qs in circ:
        if name=="T":
            b=next(it)
            if b==0: coeff*=A
            else: coeff*=B; mod.append(("S",qs))
        else: mod.append((name,qs))
    return coeff, run(n,mod)

def soc_all(n,circ):
    t=sum(1 for nm,_ in circ if nm=="T"); acc=np.zeros(2**n,dtype=complex)
    for bits in itertools.product([0,1],repeat=t):
        c,psi=branch(n,circ,bits); acc+=c*psi
    return acc,2**t

def soc_sampled(n,circ,k,seed):
    t=sum(1 for nm,_ in circ if nm=="T"); rng=np.random.default_rng(seed)
    # importance sampling: |A|,|B| equal? no. sample branch b_i with prob |c_i|/||c||_1 per T.
    pa=abs(A)/(abs(A)+abs(B)); acc=np.zeros(2**n,dtype=complex); norm1=(abs(A)+abs(B))**t
    for _ in range(k):
        bits=tuple(0 if rng.random()<pa else 1 for _ in range(t))
        c,psi=branch(n,circ,bits)
        # unbiased: divide by prob, times 1/k, but keep phase; weight = c/|c| * ||c||_1
        phase=c/abs(c); acc+=phase*norm1*psi
    return acc/k

def mk(n,t,seed=42):
    rng=np.random.default_rng(seed); circ=[("H",(q,)) for q in range(n)]; placed=0; layer=0
    while placed<t:
        for q in range(n-1): circ.append(("CX",(q,q+1)))
        for q in range(n):
            if placed<t and rng.random()<0.7: circ.append(("T",(q,))); placed+=1
        for q in range(n-1): circ.append(("CX",(q,q+1)))
        layer+=1
        if layer>200: break
    circ.append(("H",(0,))); return circ

def main():
    outdir=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","report","evidence"))
    res=[]
    print(f"exact rank-2 T: a={A:.4f}, b={B:.4f}, |a|+|b|={abs(A)+abs(B):.6f}, xi(T)={(abs(A)+abs(B))**2:.6f}")
    for t in [2,4,6,8,10]:
        circ=mk(5,t); n=5
        psi=run(n,circ); z_sv=expZ(psi,0,n)
        acc,br=soc_all(n,circ); z_soc=expZ(acc,0,n)
        # sampled with k = ceil( xi^t / 0.5^2 )-ish, cap small
        k=min(br, max(50, int(math.ceil((abs(A)+abs(B))**(2*t)/0.04))))
        z_samp=expZ(soc_sampled(n,circ,k,7),0,n)
        rec=dict(n=n,t=t,z_statevector=z_sv,z_soc_all_branches=z_soc,
                 err_soc_vs_sv=abs(z_soc-z_sv),branches=br,
                 z_soc_sampled=z_samp,k_samples=k,err_sampled_vs_sv=abs(z_samp-z_sv))
        res.append(rec)
        print(f"  t={t:2d} branches={br:5d}: <Z0>_sv={z_sv:+.6f} <Z0>_soc_all={z_soc:+.6f} "
              f"err={rec['err_soc_vs_sv']:.2e} | sampled(k={k}) <Z0>={z_samp:+.4f} err={rec['err_sampled_vs_sv']:.3f}")
    with open(os.path.join(outdir,"exp2_soc_corrected.json"),"w") as f:
        json.dump(res,f,indent=2,default=float)
    print("wrote exp2_soc_corrected.json ;  max err_soc_vs_sv =",max(r['err_soc_vs_sv'] for r in res))

if __name__=="__main__": main()
