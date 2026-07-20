#!/usr/bin/env python3
"""
Reusable TEXTURES-100 loop-current/orbital-current kernel.

Purpose: fast minimal replication support for kagome / multi-orbital papers where
headline physics is spontaneous current-loop order, orbital magnetization, or
current susceptibility.  This is NOT a DFT replacement; it is a reproducible
mean-field/tight-binding probe that can generate honest PARTIAL/qualitative
artifacts overnight.

Core idea
---------
Represent current-loop order as an oriented Peierls flux phi through each
triangle/plaquette.  Diagonalize H(phi), form occupied one-body density matrix,
and evaluate bond currents

    J_ij = -2 Im[ H_ij rho_ji ]

Then use an oriented plaquette average as the loop-current order parameter and a
finite-field derivative d(loop_order)/dphi as the loop-current susceptibility.

Use for: Tazai/Xie/Nakazawa/Li/Christensen/Yang/Feng/Kumar/Chung/Gerguri class.
"""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from typing import Iterable
import numpy as np


SQ3 = np.sqrt(3.0)


@dataclass(frozen=True)
class KagomeCluster:
    Lx: int
    Ly: int
    positions: np.ndarray      # (N,2)
    sublattice: np.ndarray     # (N,)
    triangles: list[tuple[int, int, int]]  # oriented CCW site triples
    bonds: list[tuple[int, int, int]]      # i,j,orientation sign (+ follows triangle orientation)


def kagome_cluster(Lx: int = 4, Ly: int = 4) -> KagomeCluster:
    """Periodic kagome cluster with three sites/cell and up-triangle plaquettes.

    Geometry is deliberately simple/stable for small overnight probes.  It uses
    nearest-neighbor bonds: intra-cell up triangle plus inter-cell links that form
    down triangles.  Up triangles are oriented (A,B,C); down triangles are
    included as (A(cell+1,0), C(cell), B(cell+0,1)).
    """
    basis = np.array([[0.0, 0.0], [0.5, 0.0], [0.25, SQ3/4]], float)
    a1 = np.array([1.0, 0.0]); a2 = np.array([0.5, SQ3/2])
    def idx(x, y, s): return ((y % Ly) * Lx + (x % Lx)) * 3 + s
    pos=[]; sub=[]
    for y in range(Ly):
        for x in range(Lx):
            R = x*a1 + y*a2
            for s in range(3):
                pos.append(R + basis[s]); sub.append(s)
    triangles=[]
    for y in range(Ly):
        for x in range(Lx):
            A=idx(x,y,0); B=idx(x,y,1); C=idx(x,y,2)
            triangles.append((A,B,C))  # up
            # neighboring down triangle, orientation chosen consistently
            triangles.append((idx(x+1,y,0), C, idx(x,y+1,1)))
    # Unique oriented bonds from triangles; sign records first encountered orientation.
    orient={}
    for tri in triangles:
        for i,j in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:
            key=tuple(sorted((i,j)))
            if key not in orient:
                orient[key] = (i,j)
    bonds=[]
    for (a,b),(i,j) in orient.items():
        bonds.append((i,j,+1))
    return KagomeCluster(Lx,Ly,np.array(pos),np.array(sub),triangles,bonds)


def build_hamiltonian(cluster: KagomeCluster, t: float = 1.0, phi: float = 0.0,
                      mass: float = 0.0, onsite: Iterable[float] | None = None) -> np.ndarray:
    """Nearest-neighbor kagome Hamiltonian with loop-current Peierls phase.

    phi is the phase on each oriented bond; reversing the bond conjugates it.
    mass adds a simple sublattice potential [mass, -mass/2, -mass/2] to allow
    symmetry-breaking/control sweeps.  onsite can override per-sublattice onsite.
    """
    N=len(cluster.sublattice)
    H=np.zeros((N,N), complex)
    if onsite is None:
        eps=np.array([mass, -0.5*mass, -0.5*mass], float)
    else:
        eps=np.array(list(onsite), float)
    H[np.arange(N), np.arange(N)] = eps[cluster.sublattice]
    amp = -t * np.exp(1j*phi)
    for i,j,_ in cluster.bonds:
        H[i,j] += amp
        H[j,i] += np.conj(amp)
    return H


def occupied_density(H: np.ndarray, filling: float = 0.5, temperature: float = 0.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return one-body density matrix rho_ij=<c_j^dag c_i>, eigenvalues, occupations."""
    evals, vecs = np.linalg.eigh(H)
    n = H.shape[0]
    if temperature <= 0:
        nocc = int(round(filling*n))
        occ = np.zeros(n); occ[:nocc] = 1.0
    else:
        # choose chemical potential by bisection for target filling
        target=filling*n; lo=evals.min()-50*temperature-10; hi=evals.max()+50*temperature+10
        for _ in range(120):
            mu=(lo+hi)/2
            occ=1/(1+np.exp((evals-mu)/temperature))
            if occ.sum() > target: hi=mu
            else: lo=mu
    rho = (vecs * occ) @ vecs.conj().T
    return rho, evals, occ


def bond_currents(H: np.ndarray, rho: np.ndarray, bonds: Iterable[tuple[int,int,int]]) -> dict[str, float]:
    out={}
    for i,j,_ in bonds:
        Jij = -2.0*np.imag(H[i,j] * rho[j,i])
        out[f"{i}->{j}"] = float(Jij)
    return out


def loop_order(cluster: KagomeCluster, H: np.ndarray, rho: np.ndarray) -> float:
    """Average oriented current around triangles; nonzero indicates loop-current order."""
    vals=[]
    for a,b,c in cluster.triangles:
        vals.append((-2*np.imag(H[a,b]*rho[b,a]) -2*np.imag(H[b,c]*rho[c,b]) -2*np.imag(H[c,a]*rho[a,c]))/3.0)
    return float(np.mean(vals))


def probe(Lx=4, Ly=4, t=1.0, filling=0.5, phi=1e-3, mass=0.0) -> dict:
    c=kagome_cluster(Lx,Ly)
    H0=build_hamiltonian(c,t=t,phi=0.0,mass=mass); rho0,e0,occ0=occupied_density(H0,filling)
    Hp=build_hamiltonian(c,t=t,phi=+phi,mass=mass); rhop,ep,occp=occupied_density(Hp,filling)
    Hm=build_hamiltonian(c,t=t,phi=-phi,mass=mass); rhom,em,occm=occupied_density(Hm,filling)
    op=loop_order(c,Hp,rhop); om=loop_order(c,Hm,rhom); o0=loop_order(c,H0,rho0)
    return {
        "kernel":"ollie_loop_current_meanfield_kernel",
        "Lx":Lx,"Ly":Ly,"N":3*Lx*Ly,"filling":filling,"t":t,"mass":mass,
        "loop_order_phi0":o0,
        "loop_order_plus_phi":op,
        "loop_current_susceptibility":(op-om)/(2*phi),
        "bandwidth":float(e0.max()-e0.min()),
        "fermi_gap_proxy":float(e0[int(round(filling*len(e0)))]-e0[int(round(filling*len(e0)))-1]) if 0<int(round(filling*len(e0)))<len(e0) else None,
        "interpretation":"finite susceptibility supports loop-current/orbital-current response; spontaneous order needs self-consistent interaction or Landau negative quadratic fit"
    }


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--L", type=int, default=4); ap.add_argument("--phi", type=float, default=1e-3)
    ap.add_argument("--filling", type=float, default=0.5); ap.add_argument("--mass", type=float, default=0.0)
    args=ap.parse_args()
    print(json.dumps(probe(args.L,args.L,phi=args.phi,filling=args.filling,mass=args.mass), indent=2))
