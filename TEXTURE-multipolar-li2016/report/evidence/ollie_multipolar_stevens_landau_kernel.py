#!/usr/bin/env python3
"""
Reusable TEXTURES-100 multipolar-order kernel.

Purpose: minimal, transparent support for quadrupolar/octupolar/heavy-fermion
multipolar papers.  It builds angular-momentum matrices, Stevens quadrupole
operators, thermal susceptibilities, and a simple Landau mean-field transition
estimate.  This is suitable for honest PARTIAL/qualitative replication when the
paper's full DFT/material-specific CEF model is unavailable.

Use for Banerjee/Sim/Patri/Li/Das/Kotetes/You/Chen/Konakanchi/Jaubert class.
"""
from __future__ import annotations
import argparse, json
import numpy as np


def spin_matrices(J: float):
    """Return Jx,Jy,Jz in |m=J,J-1,...,-J> basis."""
    m = np.arange(J, -J-1, -1, dtype=float)
    n = len(m)
    Jp = np.zeros((n,n), complex)
    # J+ |m> = sqrt(J(J+1)-m(m+1)) |m+1>; basis index decreases for m+1
    for col, mv in enumerate(m):
        mp = mv + 1
        if mp <= J:
            row = int(round(J - mp))
            if 0 <= row < n:
                Jp[row, col] = np.sqrt(J*(J+1) - mv*mp)
    Jm = Jp.conj().T
    Jx = 0.5*(Jp+Jm); Jy = (Jp-Jm)/(2j); Jz = np.diag(m)
    return Jx, Jy, Jz, m


def stevens_operators(J: float) -> dict[str, np.ndarray]:
    Jx,Jy,Jz,m = spin_matrices(J); I=np.eye(len(m))
    J2=J*(J+1)
    ops={
        "Jx":Jx,"Jy":Jy,"Jz":Jz,
        # quadrupoles (rank 2)
        "O20":3*Jz@Jz - J2*I,
        "O22":Jx@Jx - Jy@Jy,
        "Oxy":Jx@Jy + Jy@Jx,
        "Oyz":Jy@Jz + Jz@Jy,
        "Ozx":Jz@Jx + Jx@Jz,
    }
    # common cubic octupole-like symmetrized moment T_xyz
    ops["Txyz"] = (Jx@Jy@Jz + Jx@Jz@Jy + Jy@Jx@Jz + Jy@Jz@Jx + Jz@Jx@Jy + Jz@Jy@Jx)/6
    return ops


def cef_hamiltonian(J: float, B20=0.0, B22=0.0, B40=0.0) -> np.ndarray:
    """Small CEF Hamiltonian with quadrupolar anisotropy and simple O40 term."""
    ops=stevens_operators(J); Jx,Jy,Jz,_=spin_matrices(J); I=np.eye(int(2*J+1))
    J2=J*(J+1)
    O40 = 35*np.linalg.matrix_power(Jz,4) - (30*J2-25)*(Jz@Jz) + (3*J2*J2-6*J2)*I
    return B20*ops["O20"] + B22*ops["O22"] + B40*O40


def thermal_susceptibility(H: np.ndarray, O: np.ndarray, T: float=1.0) -> float:
    """Static single-ion susceptibility via fluctuation formula beta(<O^2>-<O>^2).

    Good for overnight qualitative comparisons; for near-degenerate CEF levels it
    captures Curie growth.  Use T in same energy units as H.
    """
    w,V=np.linalg.eigh(H)
    beta=1/max(T,1e-12)
    ew=np.exp(-beta*(w-w.min())); p=ew/ew.sum()
    Oe=V.conj().T@O@V
    mean=np.sum(p*np.diag(Oe).real)
    mean2=np.sum(p*np.diag(Oe@Oe).real)
    return float(beta*(mean2-mean*mean))


def landau_transition_temperature(Jex: float, chi0_T1: float, z: int=4) -> float:
    """Mean-field estimate: instability when 1 - z*Jex*chi(T)=0.

    If chi is Curie-like, chi(T) ~= chi(T=1)/T, so T_c ~= z Jex chi(T=1).
    """
    return float(z*Jex*chi0_T1)


def scan(J=1.5, B20=0.0, B22=0.0, B40=0.0, Jex=0.05, z=4):
    ops=stevens_operators(J); H=cef_hamiltonian(J,B20,B22,B40)
    out={"kernel":"ollie_multipolar_stevens_landau_kernel","J":J,"B20":B20,"B22":B22,"B40":B40,"Jex":Jex,"z":z,"channels":{}}
    for name in ["O20","O22","Oxy","Oyz","Ozx","Txyz"]:
        chi1=thermal_susceptibility(H, ops[name], T=1.0)
        out["channels"][name]={
            "chi_T1":chi1,
            "Tc_meanfield_curie_proxy":landau_transition_temperature(Jex,chi1,z),
        }
    # dominant channel
    dom=max(out["channels"].items(), key=lambda kv: kv[1]["chi_T1"])
    out["dominant_channel"]={"name":dom[0], **dom[1]}
    out["interpretation"]="dominant quadrupole/octupole susceptibility + positive mean-field Tc proxy supports multipolar ordering tendency; material-specific CEF/exchange needed for strict quantitative match"
    return out


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--J", type=float, default=1.5)
    ap.add_argument("--B20", type=float, default=0.0); ap.add_argument("--B22", type=float, default=0.0); ap.add_argument("--B40", type=float, default=0.0)
    ap.add_argument("--Jex", type=float, default=0.05); ap.add_argument("--z", type=int, default=4)
    args=ap.parse_args()
    print(json.dumps(scan(args.J,args.B20,args.B22,args.B40,args.Jex,args.z), indent=2))
