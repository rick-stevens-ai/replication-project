#!/usr/bin/env python3
"""
dg_stokes.py — Interior-penalty DG solver for 2D steady incompressible Stokes,
built on the SIPG machinery validated in dg_poisson.py (which reproduces the
optimal order k+1 that the Cockburn-Kanschat-Schotzau LDG framework proves).

  -nu Lap(u) + grad p = f,   div u = 0   on (0,1)^2,   u = g on boundary.

Equal-order Pk velocity + Pk pressure, DG, SIPG viscous term, consistent
pressure-velocity coupling, with a grad-grad pressure stabilization
(Brezzi-Pitkaranta style, eps*h^2) to control the equal-order inf-sup.

We use a divergence-free manufactured solution and measure L2 orders of u,p
and the discrete divergence (mass conservation). This tests the paper's
quantitatively-verifiable core: C3 optimal order, C2 small divergence.

Pure NumPy/SciPy.
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla

# ---- reference element (reuse validated helpers) ----
def ref_nodes(k):
    pts=[(i/k if k else 0.,j/k if k else 0.) for i in range(k+1) for j in range(k+1-i)]
    return np.array(pts)
def mono_powers(k): return [(a,b) for a in range(k+1) for b in range(k+1-a)]
def vander(pts,k):
    pw=mono_powers(k);r,s=pts[:,0],pts[:,1];V=np.zeros((len(pts),len(pw)))
    for c,(a,b) in enumerate(pw): V[:,c]=(r**a)*(s**b)
    return V
def vander_grad(pts,k):
    pw=mono_powers(k);r,s=pts[:,0],pts[:,1]
    Vr=np.zeros((len(pts),len(pw)));Vs=np.zeros((len(pts),len(pw)))
    for c,(a,b) in enumerate(pw):
        Vr[:,c]=(a*r**(a-1) if a>=1 else 0.)*(s**b)
        Vs[:,c]=(r**a)*(b*s**(b-1) if b>=1 else 0.)
    return Vr,Vs
def tri_quad(o):
    x,w=np.polynomial.legendre.leggauss(o);x=0.5*(x+1);w=0.5*w
    R,S,W=[],[],[]
    for i in range(o):
        for j in range(o):
            a,b=x[i],x[j];R.append(a);S.append(b*(1-a));W.append(w[i]*w[j]*(1-a))
    return np.column_stack([R,S]),np.array(W)
def edge_quad(o):
    x,w=np.polynomial.legendre.leggauss(o);return 0.5*(x+1),0.5*w
def unit_square_tris(n):
    idx={};verts=[]
    for j in range(n+1):
        for i in range(n+1):
            idx[(i,j)]=len(verts);verts.append((i/n,j/n))
    verts=np.array(verts);tris=[]
    for j in range(n):
        for i in range(n):
            v00=idx[(i,j)];v10=idx[(i+1,j)];v01=idx[(i,j+1)];v11=idx[(i+1,j+1)]
            tris.append((v00,v10,v11));tris.append((v00,v11,v01))
    return verts,np.array(tris)
def affine(tv):
    p0,p1,p2=tv;B=np.column_stack([p1-p0,p2-p0])
    return p0,B,np.linalg.det(B),np.linalg.inv(B).T

# ---- divergence-free manufactured solution ----
NU=1.0
def exact_u(x,y):
    return (np.sin(np.pi*x)*np.cos(np.pi*y), -np.cos(np.pi*x)*np.sin(np.pi*y))
def exact_p(x,y):
    return np.sin(np.pi*x)*np.sin(np.pi*y)-4.0/(np.pi*np.pi)  # mean ~0
def rhs_f(x,y):
    pi=np.pi
    lap1=-2*pi*pi*np.sin(pi*x)*np.cos(pi*y)
    lap2= 2*pi*pi*np.cos(pi*x)*np.sin(pi*y)
    dpx= pi*np.cos(pi*x)*np.sin(pi*y)
    dpy= pi*np.sin(pi*x)*np.cos(pi*y)
    return (-NU*lap1+dpx, -NU*lap2+dpy)

def solve(n,k,quad_order=None,pstab=1e-2,penalty_scale=None):
    if quad_order is None: quad_order=k+2
    if penalty_scale is None: penalty_scale=6.0*(k+1)   # tuned; ~12 for k=1
    verts,tris=unit_square_tris(n)
    rn=ref_nodes(k);Np=len(rn);Vinv=np.linalg.inv(vander(rn,k))
    qp,qw=tri_quad(quad_order);Vq=vander(qp,k)@Vinv
    Vqr,Vqs=vander_grad(qp,k);Vqr=Vqr@Vinv;Vqs=Vqs@Vinv
    eq_t,eq_w=edge_quad(quad_order)
    nT=len(tris);dpe=3*Np;N=nT*dpe
    rows,cols,vals=[],[],[];F=np.zeros(N)
    geom=[affine(verts[t]) for t in tris]
    ref_edges=[(0,1),(1,2),(2,0)]
    emap={}
    for el,t in enumerate(tris):
        for le,(a,b) in enumerate(ref_edges):
            emap.setdefault(tuple(sorted((t[a],t[b]))),[]).append((el,le,(t[a],t[b])))
    def gd(el,f,i): return el*dpe+f*Np+i
    def add(gi,gj,v): rows.append(gi);cols.append(gj);vals.append(v)

    # ---- volume ----
    for el,t in enumerate(tris):
        p0,B,detJ,invJT=geom[el];aJ=abs(detJ);w=qw*aJ
        gx=Vqr*invJT[0,0]+Vqs*invJT[0,1];gy=Vqr*invJT[1,0]+Vqs*invJT[1,1]
        K=NU*((gx.T*w)@gx+(gy.T*w)@gy)         # vector Laplacian (per comp)
        # pressure gradient in momentum, weak: -(p, div v) => (grad? ) use -(dv/dx, p)
        Gx=-(gx.T*w)@Vq  # (u1 test i, p trial j)
        Gy=-(gy.T*w)@Vq
        # continuity -(q, div u): (q i, u1 j)=-(phi_i, du1/dx)
        Dx=-(Vq.T*w)@gx
        Dy=-(Vq.T*w)@gy
        # pressure stab (grad q, grad p)*eps*h^2
        h=np.sqrt(aJ)
        Sp=(pstab*h*h)*((gx.T*w)@gx+(gy.T*w)@gy)
        xq=p0[0]+B[0,0]*qp[:,0]+B[0,1]*qp[:,1];yq=p0[1]+B[1,0]*qp[:,0]+B[1,1]*qp[:,1]
        f1,f2=rhs_f(xq,yq)
        for i in range(Np):
            F[gd(el,0,i)]+=np.sum(Vq[:,i]*f1*w)
            F[gd(el,1,i)]+=np.sum(Vq[:,i]*f2*w)
            for j in range(Np):
                add(gd(el,0,i),gd(el,0,j),K[i,j])
                add(gd(el,1,i),gd(el,1,j),K[i,j])
                add(gd(el,0,i),gd(el,2,j),Gx[i,j])
                add(gd(el,1,i),gd(el,2,j),Gy[i,j])
                add(gd(el,2,i),gd(el,0,j),Dx[i,j])
                add(gd(el,2,i),gd(el,1,j),Dy[i,j])
                add(gd(el,2,i),gd(el,2,j),Sp[i,j])

    # ---- faces ----
    for key,ents in emap.items():
        if len(ents)==2:
            (elA,leA,ev),(elB,leB,_)=ents
            p0A,BA,detA,invA=geom[elA];p0B,BB,detB,invB=geom[elB]
            va,vb=ev;xa,xb=verts[va],verts[vb];elen=np.linalg.norm(xb-xa)
            tang=(xb-xa)/elen;nA=np.array([tang[1],-tang[0]])
            if np.dot(0.5*(xa+xb)-verts[list(tris[elA])].mean(0),nA)<0: nA=-nA
            hf=min(np.sqrt(abs(detA)),np.sqrt(abs(detB)));pen=penalty_scale/hf*NU
            for tq,wq in zip(eq_t,eq_w):
                wl=wq*elen;xp=xa+(xb-xa)*tq
                rA=np.linalg.solve(BA,xp-p0A);rB=np.linalg.solve(BB,xp-p0B)
                pA=(vander(rA[None],k)@Vinv)[0];pB=(vander(rB[None],k)@Vinv)[0]
                gAr,gAs=vander_grad(rA[None],k);gAr=(gAr@Vinv)[0];gAs=(gAs@Vinv)[0]
                gBr,gBs=vander_grad(rB[None],k);gBr=(gBr@Vinv)[0];gBs=(gBs@Vinv)[0]
                gnA=(gAr*invA[0,0]+gAs*invA[0,1])*nA[0]+(gAr*invA[1,0]+gAs*invA[1,1])*nA[1]
                gnB=(gBr*invB[0,0]+gBs*invB[0,1])*nA[0]+(gBr*invB[1,0]+gBs*invB[1,1])*nA[1]
                sd=[(elA,pA,gnA,+1.0),(elB,pB,gnB,-1.0)]
                # SIPG viscous per velocity component
                for a in range(2):
                    ea,pav,gna,sa=sd[a]
                    for b in range(2):
                        eb,pbv,gnb,sb=sd[b]
                        Mv=(-0.5*np.outer(sa*pav,gnb)-0.5*np.outer(gna,sb*pbv)
                            +pen*np.outer(sa*pav,sb*pbv))*wl
                        for i in range(Np):
                            for j in range(Np):
                                add(gd(ea,0,i),gd(eb,0,j),Mv[i,j])
                                add(gd(ea,1,i),gd(eb,1,j),Mv[i,j])
                # pressure/continuity face coupling: restore IBP boundary terms
                #   momentum: +{p}[v].n   ; continuity: -{u.n}[q] ... use consistent central
                for a in range(2):
                    ea,pav,_,sa=sd[a]
                    for b in range(2):
                        eb,pbv,_,sb=sd[b]
                        # momentum row(v side a) <- p (side b): +0.5*pbv * (sa*pav)*n
                        cpv=0.5*np.outer(sa*pav,pbv)*wl
                        for i in range(Np):
                            for j in range(Np):
                                add(gd(ea,0,i),gd(eb,2,j),cpv[i,j]*nA[0])
                                add(gd(ea,1,i),gd(eb,2,j),cpv[i,j]*nA[1])
                        # continuity row(q side a) <- u (side b): -0.5*(sa*pav)*pbv*n
                        cqv=0.5*np.outer(sa*pav,sb*pbv)*wl  # jump form for stability
                        for i in range(Np):
                            for j in range(Np):
                                add(gd(ea,2,i),gd(eb,0,j),-cqv[i,j]*nA[0])
                                add(gd(ea,2,i),gd(eb,1,j),-cqv[i,j]*nA[1])
        else:
            (elA,leA,ev),=ents
            p0A,BA,detA,invA=geom[elA]
            va,vb=ev;xa,xb=verts[va],verts[vb];elen=np.linalg.norm(xb-xa)
            tang=(xb-xa)/elen;nA=np.array([tang[1],-tang[0]])
            if np.dot(0.5*(xa+xb)-verts[list(tris[elA])].mean(0),nA)<0: nA=-nA
            hf=np.sqrt(abs(detA));pen=penalty_scale/hf*NU
            for tq,wq in zip(eq_t,eq_w):
                wl=wq*elen;xp=xa+(xb-xa)*tq
                rA=np.linalg.solve(BA,xp-p0A);pA=(vander(rA[None],k)@Vinv)[0]
                gAr,gAs=vander_grad(rA[None],k);gAr=(gAr@Vinv)[0];gAs=(gAs@Vinv)[0]
                gn=(gAr*invA[0,0]+gAs*invA[0,1])*nA[0]+(gAr*invA[1,0]+gAs*invA[1,1])*nA[1]
                ue1,ue2=exact_u(xp[0],xp[1])
                Mv=(-np.outer(pA,gn)-np.outer(gn,pA)+pen*np.outer(pA,pA))*wl
                for fld,ub in ((0,ue1),(1,ue2)):
                    for i in range(Np):
                        gi=gd(elA,fld,i)
                        F[gi]+=(-gn[i]*ub+pen*pA[i]*ub)*wl
                        for j in range(Np):
                            add(gi,gd(elA,fld,j),Mv[i,j])
                    # boundary pressure coupling into momentum: +p n
                    for i in range(Np):
                        for j in range(Np):
                            add(gd(elA,fld,i),gd(elA,2,j),pA[i]*pA[j]*wl*nA[fld])
                # continuity boundary: exact u.n known -> to RHS
                for i in range(Np):
                    F[gd(elA,2,i)]+=-pA[i]*(ue1*nA[0]+ue2*nA[1])*wl

    A=sp.csr_matrix((vals,(rows,cols)),shape=(N,N)).tocsc()
    A=A+sp.identity(N)*1e-12
    sol=spla.spsolve(A,F)

    # pressure mean shift
    numP=0.;area=0.
    for el,t in enumerate(tris):
        p0,B,detJ,invJT=geom[el];w=qw*abs(detJ)
        ph=Vq@sol[el*dpe+2*Np:el*dpe+3*Np]
        numP+=np.sum(ph*w);area+=np.sum(w)
    pmean=numP/area
    eU=0.;nU=0.;eP=0.;nP=0.;dv=0.
    for el,t in enumerate(tris):
        p0,B,detJ,invJT=geom[el];aJ=abs(detJ);w=qw*aJ
        xq=p0[0]+B[0,0]*qp[:,0]+B[0,1]*qp[:,1];yq=p0[1]+B[1,0]*qp[:,0]+B[1,1]*qp[:,1]
        u1=Vq@sol[el*dpe+0*Np:el*dpe+1*Np];u2=Vq@sol[el*dpe+1*Np:el*dpe+2*Np]
        ph=Vq@sol[el*dpe+2*Np:el*dpe+3*Np]-pmean
        ue1,ue2=exact_u(xq,yq);pe=exact_p(xq,yq)
        eU+=np.sum(((u1-ue1)**2+(u2-ue2)**2)*w);nU+=np.sum((ue1**2+ue2**2)*w)
        eP+=np.sum((ph-pe)**2*w);nP+=np.sum(pe**2*w)
        gx=Vqr*invJT[0,0]+Vqs*invJT[0,1];gy=Vqr*invJT[1,0]+Vqs*invJT[1,1]
        d=gx@sol[el*dpe+0*Np:el*dpe+1*Np]+gy@sol[el*dpe+1*Np:el*dpe+2*Np]
        dv+=np.sum(d*d*w)
    return dict(h=1./n,k=k,ndof=N,errU=np.sqrt(eU),errP=np.sqrt(eP),
                relU=np.sqrt(eU/nU),relP=np.sqrt(eP/max(nP,1e-30)),divL2=np.sqrt(dv))

def order(e,h): return [np.log(e[i-1]/e[i])/np.log(h[i-1]/h[i]) for i in range(1,len(e))]

if __name__=="__main__":
    import json,sys
    out={}
    for k in (1,2):
        ns=[2,4,8,16] if k==1 else [2,4,8]
        R=[solve(n,k) for n in ns]
        h=[r["h"] for r in R];eu=[r["errU"] for r in R];ep=[r["errP"] for r in R]
        dv=[r["divL2"] for r in R]
        ou=order(eu,h);op=order(ep,h)
        out[f"k={k}"]=dict(h=h,errU=eu,errP=ep,divL2=dv,orderU=ou,orderP=op,
                           ndof=[r["ndof"] for r in R])
        print(f"\n=== DG Stokes k={k} (expect optimal order {k+1}) ===")
        print(f"{'h':>8}{'ndof':>8}{'errU':>13}{'ordU':>7}{'errP':>13}{'ordP':>7}{'divL2':>11}")
        for i,r in enumerate(R):
            os1=f"{ou[i-1]:.2f}" if i>0 else "  -"
            os2=f"{op[i-1]:.2f}" if i>0 else "  -"
            print(f"{r['h']:8.4f}{r['ndof']:8d}{r['errU']:13.4e}{os1:>7}{r['errP']:13.4e}{os2:>7}{r['divL2']:11.2e}")
    json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else "stokes_results.json","w"),indent=2)
    print("\nwrote json")
