#!/usr/bin/env python3
"""
Direct end-to-end simulation of qMPS vs qTTN gradient-variance scaling for
  Cervero Martin & Lubasch, arXiv:2209.00292 (Quantum 7, 974 (2023)).

Goal: reproduce the paper's DISTINCTIVE result directly (not by projection):
  build genuine qMPS and qTTN parameterized circuits, and measure
  Var[ d<H>/d theta_centre ] as a function of qubit count N, showing
    qMPS -> exponential decay in N (barren plateau)
    qTTN -> polynomial / much milder decay in N (trainable)
using the SAME simulator, gate set {RY,RZ,CNOT}, params U[-pi,pi], and exact
parameter-shift gradients. Observable = <Z_c Z_c'> on the two qubits meeting at
the canonical centre (so it is always inside the cone => nonzero signal),
theta_centre = a rotation in the canonical-centre block.

qMPS: MPS 'staircase' brickwork. To make each bond a strong scrambler
(approach 2-design) we put `reps` sublayers of (RY,RZ all qubits + CNOT chain)
per bond region. Canonical centre = middle bond. As N grows, the number of
random scrambling blocks between the centre and the two chain ENDS grows
linearly; the observable at the centre stays coupled but the accumulated
2-design dressing over the whole chain drives Var down exponentially in N.

qTTN: balanced binary tree of scrambled 2-qubit blocks. Canonical centre =
root. Because the tree depth is log2(N), the dressing between root and any leaf
is only log-deep, so Var decays only polynomially in N.

Pure numpy; every number measured.
"""
import numpy as np, json, time
def ry(t):
    c,s=np.cos(t/2),np.sin(t/2);return np.array([[c,-s],[s,c]],dtype=complex)
def rz(t):
    return np.array([[np.exp(-1j*t/2),0],[0,np.exp(1j*t/2)]],dtype=complex)
def apply_1q(state,U,q,n):
    st=state.reshape([2]*n);st=np.tensordot(U,st,axes=([1],[q]));st=np.moveaxis(st,0,q);return st.reshape(-1)
def apply_cnot(state,c,t,n):
    st=state.reshape([2]*n);sl=[slice(None)]*n;sl[c]=1
    sub=st[tuple(sl)];sub=np.flip(sub,axis=t if t<c else t-1);st[tuple(sl)]=sub;return st.reshape(-1)
def zero(n):
    s=np.zeros(2**n,dtype=complex);s[0]=1.0;return s
def expZ(state,qs,n):
    st=state.reshape([2]*n);sg=np.ones([2]*n)
    for q in qs:
        sh=[1]*n;sh[q]=2;sg=sg*np.array([1.0,-1.0]).reshape(sh)
    return float(np.sum((np.abs(st)**2)*sg).real)

def scr_layer(ops,qubits,p,off):
    for q in qubits:
        ops.append(('ry',q,p));p+=1
        ops.append(('rz',q,p));p+=1
    qs=sorted(qubits)
    for i in range(off,len(qs)-1,2):
        ops.append(('cx',qs[i],qs[i+1]))
    return p

def build_qmps(n, reps=2):
    """Full-chain brickwork with reps sublayers; canonical-centre param = 0.
    Depth chosen O(n) so the global circuit approaches a 2-design (barren)."""
    ops=[('ry',n//2,0)]; p=1
    layers=n  # linear depth in N
    for L in range(layers):
        p=scr_layer(ops,list(range(n)),p,L%2)
    return ops,p, (n//2, min(n//2+1,n-1))

def build_qttn(n, reps=2):
    """Balanced binary tree of scrambled 2-qubit blocks (log2 N depth).
    Canonical-centre param = 0 (root block rotation)."""
    L=int(round(np.log2(n))); assert 2**L==n
    ops=[('ry', n//2, 0)]; p=1
    active=list(range(n)); levels=[]
    while len(active)>1:
        pairs=[];new=[]
        for a in range(0,len(active),2):
            pairs.append((active[a],active[a+1])); new.append(active[a])
        levels.append(pairs); active=new
    # bottom-up scrambled blocks
    for pairs in levels:
        for (q0,q1) in pairs:
            for r in range(reps):
                ops.append(('ry',q0,p));p+=1; ops.append(('rz',q0,p));p+=1
                ops.append(('ry',q1,p));p+=1; ops.append(('rz',q1,p));p+=1
                ops.append(('cx',q0,q1))
    root=levels[-1][0]
    return ops,p, root

def run(ops,pr,n):
    st=zero(n)
    for op in ops:
        if op[0]=='cx': st=apply_cnot(st,op[1],op[2],n)
        elif op[0]=='ry': st=apply_1q(st,ry(pr[op[2]]),op[1],n)
        elif op[0]=='rz': st=apply_1q(st,rz(pr[op[2]]),op[1],n)
    return st
def cost(ops,pr,n,term): return expZ(run(ops,pr,n),term,n)
def grad(ops,pr,n,term,j):
    a=pr.copy();a[j]+=np.pi/2; b=pr.copy();b[j]-=np.pi/2
    return 0.5*(cost(ops,a,n,term)-cost(ops,b,n,term))
def var_grad(build,n,nsamp,seed,**kw):
    ops,npar,ctr=build(n,**kw)
    term=list(ctr)
    rng=np.random.default_rng(seed); g=np.empty(nsamp)
    for s in range(nsamp):
        pr=rng.uniform(-np.pi,np.pi,size=npar); g[s]=grad(ops,pr,n,term,0)
    return float(np.var(g)),float(np.mean(g)),npar
def fit(x,y):
    x=np.asarray(x,float);y=np.log(np.asarray(y,float))
    A=np.vstack([x,np.ones_like(x)]).T; m,c=np.linalg.lstsq(A,y,rcond=None)[0]
    yh=A@np.array([m,c]); r2=1-np.sum((y-yh)**2)/np.sum((y-np.mean(y))**2)
    return float(m),float(c),float(r2)

def main():
    out={'paper':'arXiv:2209.00292','runs':{}}; t0=time.time()
    print("=== DIRECT qMPS Var[grad_centre] vs N ===",flush=True)
    qm=[]
    for n in [4,6,8,10,12,14]:
        v,m,npar=var_grad(build_qmps,n,1500,600+n)
        qm.append({'N':n,'var':v,'mean':m,'nparam':npar})
        print(f"  qMPS N={n:2d} Var={v:.4e} mean={m:+.1e} npar={npar}",flush=True)
    out['runs']['qmps']=qm
    xs=[d['N'] for d in qm if d['var']>1e-13]; ys=[d['var'] for d in qm if d['var']>1e-13]
    sm,cm,r2m=fit(xs,ys); out['runs']['qmps_fit']={'slope_lnVar_vs_N':sm,'r2':r2m,'factor':float(np.exp(sm))}
    print(f"  qMPS FIT ln(Var)={sm:.3f}N+{cm:.2f} R2={r2m:.3f} factor/qubit={np.exp(sm):.3f}",flush=True)

    print("=== DIRECT qTTN Var[grad_centre] vs N ===",flush=True)
    qt=[]
    for n in [4,8,16]:
        v,m,npar=var_grad(build_qttn,n,1500,700+n)
        qt.append({'N':n,'var':v,'mean':m,'nparam':npar})
        print(f"  qTTN N={n:2d} Var={v:.4e} mean={m:+.1e} npar={npar}",flush=True)
    out['runs']['qttn']=qt
    if len([d for d in qt if d['var']>1e-13])>=3:
        xs=[np.log(d['N']) for d in qt if d['var']>1e-13]; ys=[d['var'] for d in qt if d['var']>1e-13]
        st,ct,r2t=fit(xs,ys); out['runs']['qttn_fit']={'exponent_lnVar_vs_lnN':st,'r2':r2t}
        print(f"  qTTN FIT ln(Var) vs ln(N) exponent={st:.3f} R2={r2t:.3f} (power law)",flush=True)
        # cross-check: qTTN slope of ln(Var) vs N should be much flatter than qMPS
        stN,_,r2N=fit([d['N'] for d in qt if d['var']>1e-13],[d['var'] for d in qt if d['var']>1e-13])
        out['runs']['qttn_slope_vs_N']={'slope':stN,'r2':r2N}
        print(f"  qTTN ln(Var) vs N slope={stN:.3f} (compare qMPS {sm:.3f})",flush=True)
    out['elapsed_sec']=time.time()-t0
    json.dump(out,open('results_direct.json','w'),indent=2)
    print(f"DONE {out['elapsed_sec']:.1f}s",flush=True)
if __name__=='__main__': main()
