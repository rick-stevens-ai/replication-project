#!/usr/bin/env python3
"""
dg_poisson.py — Symmetric Interior Penalty (SIPG) DG solver for the 2D Poisson
problem -Lap(u)=f on (0,1)^2, Dirichlet BC.  This VALIDATES the DG machinery
(nodal basis, quadrature, SIPG face terms) used for the Stokes replication and
independently confirms the OPTIMAL convergence order k+1 in L2 that the
Cockburn-Kanschat-Schotzau LDG framework proves for the elliptic/viscous
operator (the heart of their optimal-order result).

Pure NumPy/SciPy.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def ref_nodes(k):
    pts=[]
    for i in range(k+1):
        for j in range(k+1-i):
            pts.append((i/k if k else 0.0, j/k if k else 0.0))
    return np.array(pts)
def mono_powers(k): return [(a,b) for a in range(k+1) for b in range(k+1-a)]
def vander(pts,k):
    pw=mono_powers(k); r,s=pts[:,0],pts[:,1]
    V=np.zeros((len(pts),len(pw)))
    for c,(a,b) in enumerate(pw): V[:,c]=(r**a)*(s**b)
    return V
def vander_grad(pts,k):
    pw=mono_powers(k); r,s=pts[:,0],pts[:,1]
    Vr=np.zeros((len(pts),len(pw))); Vs=np.zeros((len(pts),len(pw)))
    for c,(a,b) in enumerate(pw):
        Vr[:,c]=(a*r**(a-1) if a>=1 else 0.0)*(s**b)
        Vs[:,c]=(r**a)*(b*s**(b-1) if b>=1 else 0.0)
    return Vr,Vs
def tri_quad(order):
    x,w=np.polynomial.legendre.leggauss(order); x=0.5*(x+1);w=0.5*w
    R,S,W=[],[],[]
    for i in range(order):
        for j in range(order):
            a,b=x[i],x[j]; R.append(a);S.append(b*(1-a));W.append(w[i]*w[j]*(1-a))
    return np.column_stack([R,S]),np.array(W)
def edge_quad(order):
    x,w=np.polynomial.legendre.leggauss(order); return 0.5*(x+1),0.5*w
def unit_square_tris(n):
    idx={};verts=[]
    for j in range(n+1):
        for i in range(n+1):
            idx[(i,j)]=len(verts); verts.append((i/n,j/n))
    verts=np.array(verts); tris=[]
    for j in range(n):
        for i in range(n):
            v00=idx[(i,j)];v10=idx[(i+1,j)];v01=idx[(i,j+1)];v11=idx[(i+1,j+1)]
            tris.append((v00,v10,v11)); tris.append((v00,v11,v01))
    return verts,np.array(tris)
def affine(tv):
    p0,p1,p2=tv; B=np.column_stack([p1-p0,p2-p0])
    return p0,B,np.linalg.det(B),np.linalg.inv(B).T

def uex(x,y): return np.sin(np.pi*x)*np.sin(np.pi*y)
def fex(x,y): return 2*np.pi*np.pi*np.sin(np.pi*x)*np.sin(np.pi*y)

def solve(n,k,quad_order=None,penalty_scale=None):
    if quad_order is None: quad_order=k+2
    if penalty_scale is None: penalty_scale=3.0*(k+1)*(k+2)
    verts,tris=unit_square_tris(n)
    rn=ref_nodes(k); Np=len(rn); Vinv=np.linalg.inv(vander(rn,k))
    qp,qw=tri_quad(quad_order); Vq=vander(qp,k)@Vinv
    Vqr,Vqs=vander_grad(qp,k); Vqr=Vqr@Vinv; Vqs=Vqs@Vinv
    eq_t,eq_w=edge_quad(quad_order)
    nT=len(tris); N=nT*Np
    rows,cols,vals=[],[],[]; F=np.zeros(N)
    geom=[affine(verts[t]) for t in tris]
    ref_edges=[(0,1),(1,2),(2,0)]
    corners=np.array([[0.,0.],[1.,0.],[0.,1.]])
    emap={}
    for el,t in enumerate(tris):
        for le,(a,b) in enumerate(ref_edges):
            emap.setdefault(tuple(sorted((t[a],t[b]))),[]).append((el,le,(t[a],t[b])))
    def gd(el,i): return el*Np+i
    # volume
    for el,t in enumerate(tris):
        p0,B,detJ,invJT=geom[el]; w=qw*abs(detJ)
        gx=Vqr*invJT[0,0]+Vqs*invJT[0,1]; gy=Vqr*invJT[1,0]+Vqs*invJT[1,1]
        K=(gx.T*w)@gx+(gy.T*w)@gy
        xq=p0[0]+B[0,0]*qp[:,0]+B[0,1]*qp[:,1]; yq=p0[1]+B[1,0]*qp[:,0]+B[1,1]*qp[:,1]
        ff=fex(xq,yq)
        for i in range(Np):
            F[gd(el,i)]+=np.sum(Vq[:,i]*ff*w)
            for j in range(Np):
                rows.append(gd(el,i));cols.append(gd(el,j));vals.append(K[i,j])
    # faces
    for key,ents in emap.items():
        if len(ents)==2:
            (elA,leA,ev),(elB,leB,_)=ents
            p0A,BA,detA,invA=geom[elA]; p0B,BB,detB,invB=geom[elB]
            va,vb=ev; xa,xb=verts[va],verts[vb]; elen=np.linalg.norm(xb-xa)
            tang=(xb-xa)/elen; nA=np.array([tang[1],-tang[0]])
            if np.dot(0.5*(xa+xb)-verts[list(tris[elA])].mean(0),nA)<0: nA=-nA
            hf=min(np.sqrt(abs(detA)),np.sqrt(abs(detB))); pen=penalty_scale/hf
            for tq,wq in zip(eq_t,eq_w):
                wl=wq*elen; xp=xa+(xb-xa)*tq
                rA=np.linalg.solve(BA,xp-p0A); rB=np.linalg.solve(BB,xp-p0B)
                phiA=(vander(rA[None],k)@Vinv)[0]; phiB=(vander(rB[None],k)@Vinv)[0]
                gAr,gAs=vander_grad(rA[None],k); gAr=(gAr@Vinv)[0];gAs=(gAs@Vinv)[0]
                gBr,gBs=vander_grad(rB[None],k); gBr=(gBr@Vinv)[0];gBs=(gBs@Vinv)[0]
                gnA=(gAr*invA[0,0]+gAs*invA[0,1])*nA[0]+(gAr*invA[1,0]+gAs*invA[1,1])*nA[1]
                gnB=(gBr*invB[0,0]+gBs*invB[0,1])*nA[0]+(gBr*invB[1,0]+gBs*invB[1,1])*nA[1]
                # sides: 0=A(sign +1 wrt nA), 1=B(sign -1)
                # Scalar SIPG, fixed edge normal n_e = nA (A->B).
                #  jump [w] = wA - wB ; average {q} = 0.5(qA + qB).
                # side sign s: A-> +1, B-> -1  (so [w] = sA*wA + sB*wB).
                sd=[(elA,phiA,gnA,+1.0),(elB,phiB,gnB,-1.0)]
                for a in range(2):
                    ea,pa,gna,sa=sd[a]   # v (test) side a
                    for b in range(2):
                        eb,pb,gnb,sb=sd[b]   # u (trial) side b
                        # -{grad u . n_e} [v] = -(0.5*gnb) * (sa*pa)
                        #   contributes only from the trial side b's gradient, averaged (0.5)
                        t1 = -0.5*np.outer(sa*pa, gnb)          # rows=v(a,i), cols=u(b,j)
                        # -{grad v . n_e} [u] = -(0.5*gna)*(sb*pb)
                        t2 = -0.5*np.outer(gna, sb*pb)
                        # + pen [u][v] = pen*(sa*pa)(sb*pb)
                        t3 = pen*np.outer(sa*pa, sb*pb)
                        M=(t1+t2+t3)*wl
                        for i in range(Np):
                            gi=gd(ea,i)
                            for j in range(Np):
                                rows.append(gi);cols.append(gd(eb,j));vals.append(M[i,j])
        else:
            (elA,leA,ev),=ents
            p0A,BA,detA,invA=geom[elA]
            va,vb=ev; xa,xb=verts[va],verts[vb]; elen=np.linalg.norm(xb-xa)
            tang=(xb-xa)/elen; nA=np.array([tang[1],-tang[0]])
            if np.dot(0.5*(xa+xb)-verts[list(tris[elA])].mean(0),nA)<0: nA=-nA
            hf=np.sqrt(abs(detA)); pen=penalty_scale/hf
            for tq,wq in zip(eq_t,eq_w):
                wl=wq*elen; xp=xa+(xb-xa)*tq
                rA=np.linalg.solve(BA,xp-p0A); phiA=(vander(rA[None],k)@Vinv)[0]
                gAr,gAs=vander_grad(rA[None],k);gAr=(gAr@Vinv)[0];gAs=(gAs@Vinv)[0]
                gn=(gAr*invA[0,0]+gAs*invA[0,1])*nA[0]+(gAr*invA[1,0]+gAs*invA[1,1])*nA[1]
                ub=uex(xp[0],xp[1])
                M=(-gn[:,None]*phiA[None,:]-gn[None,:]*phiA[:,None]+pen*np.outer(phiA,phiA))*wl
                for i in range(Np):
                    gi=gd(elA,i)
                    F[gi]+=(-gn[i]*ub+pen*phiA[i]*ub)*wl
                    for j in range(Np):
                        rows.append(gi);cols.append(gd(elA,j));vals.append(M[i,j])
    A=sp.csr_matrix((vals,(rows,cols)),shape=(N,N))
    sol=spla.spsolve(A.tocsc(),F)
    e2=0;nrm=0
    for el,t in enumerate(tris):
        p0,B,detJ,invJT=geom[el]; w=qw*abs(detJ)
        xq=p0[0]+B[0,0]*qp[:,0]+B[0,1]*qp[:,1]; yq=p0[1]+B[1,0]*qp[:,0]+B[1,1]*qp[:,1]
        uh=Vq@sol[el*Np:(el+1)*Np]; ue=uex(xq,yq)
        e2+=np.sum((uh-ue)**2*w); nrm+=np.sum(ue**2*w)
    return 1.0/n,N,np.sqrt(e2)

if __name__=="__main__":
    import json,sys
    out={}
    for k in (1,2,3):
        ns=[2,4,8,16] if k<=2 else [2,4,8]
        hs=[];es=[];nd=[]
        for n in ns:
            h,N,e=solve(n,k); hs.append(h);es.append(e);nd.append(N)
        ords=[np.log(es[i-1]/es[i])/np.log(hs[i-1]/hs[i]) for i in range(1,len(es))]
        out[f"k={k}"]=dict(h=hs,err=es,ndof=nd,order=ords)
        print(f"\n=== Poisson SIPG k={k} (expect order {k+1}) ===")
        for i,(h,e) in enumerate(zip(hs,es)):
            os=f"{ords[i-1]:.3f}" if i>0 else "  -"
            print(f"  h={h:.4f}  err={e:.4e}  order={os}")
    json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else "poisson_results.json","w"),indent=2)
    print("wrote json")
