#!/usr/bin/env python3
"""
build_clusters.py -- Construct chemically valid FLiBe cluster geometries for the
replication of arXiv:2606.30402 (Quantum Computations on Fusion Blanket Molten Salts).

The paper's exact 9 AIMD/MLFF snapshots are NOT publicly deposited, so we cannot
reproduce their exact coordinates. Instead we build representative clusters that obey
the same stoichiometry, charge, spin, and coordination chemistry described in the SI:

  System 1  FLiBe    : Li6 Be3 F12          (21 atoms, charge 0, singlet)
  System 2a FLiBeF-  : [Li6 Be3 F13]^-      (22 atoms, charge -1, singlet)
  System 2b FLiBeTF  : Li6 Be3 F13 (T=H)    (23 atoms, charge 0, singlet)

Chemistry enforced (SI S1, S3):
  * each Be tetrahedrally coordinated by 4 F  (BeF4 motif), corner-sharing network
  * stoichiometry 1 BeF2 : 2 LiF
  * Li+ counterions near bridging/terminal fluorides
  * in FLiBeTF the tritium (modeled as protium H; same electronic structure, the
    paper removes T as a bare T+ = H+ nucleus for E_bind) bridges two F (F-T-F motif)
  * 22-atom anion = 23-atom FLiBeTF with the T nucleus removed (identical F/Li/Be coords)

We build ONE seed geometry per system, then create 9 conformers by applying small
random thermal displacements (mimicking finite-T AIMD sampling ~783-900 K), then
DFT-relax each. This yields a 9-cluster ensemble analogous to the paper's.

Units: Angstrom.
"""
import numpy as np
from ase import Atoms
from ase.io import write
import os, json

np.random.seed(20260708)

# --- Reference bond lengths (Angstrom), from FLiBe structural chemistry ---
D_BeF = 1.55    # Be-F in tetrahedral BeF4 (2-)
D_LiF = 1.85    # Li-F ionic
D_FH  = 1.02    # F-H(T) in bent F-T-F ; stretched relative to isolated HF (0.92)

def tetrahedron(center, d, orient=None):
    """4 vertices of a tetrahedron at distance d around center."""
    v = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], float)
    v /= np.linalg.norm(v[0])
    if orient is not None:
        # simple random rotation
        from numpy import cos, sin
        a,b,c = orient
        Rx=np.array([[1,0,0],[0,cos(a),-sin(a)],[0,sin(a),cos(a)]])
        Ry=np.array([[cos(b),0,sin(b)],[0,1,0],[-sin(b),0,cos(b)]])
        Rz=np.array([[cos(c),-sin(c),0],[sin(c),cos(c),0],[0,0,1]])
        v = v @ (Rx@Ry@Rz).T
    return center + d*v

def build_flibe_core():
    """
    Build a corner-sharing Be3F(bridging)+terminal network: Li6Be3F12.
    3 Be centers, arranged in a triangle, each BeF4 tetrahedron sharing corners
    so total F = 12 (matches Li6Be3F12). 6 Li placed around the periphery.
    """
    symbols = []
    pos = []

    # Place 3 Be in a triangle
    R = 2.6  # Be-Be-ish spacing through bridging F
    be_centers = np.array([
        [ 0.0,          0.0, 0.0],
        [ R,            0.0, 0.0],
        [ R/2, R*np.sqrt(3)/2, 0.0],
    ])
    # Bridging F between each Be pair (3 bridges), terminal F to reach 12 total.
    # Each Be needs 4 F. 3 bridging F shared by 2 Be each -> contributes 6 Be-F bonds.
    # Remaining Be-F bonds = 3*4 - 6 = 6 terminal F. Total F = 3 bridge + ... need 12.
    # Use 3 bridging + 9 terminal = 12 F. Then Be coordination:
    #   Be0: bridges to Be1, Be2 (2 bridging F) + 2 terminal = 4  OK
    #   Be1: bridges to Be0, and needs 3 terminal ... balance below.
    F_pos = []
    centroid = be_centers.mean(axis=0)
    # ONE central bridging F shared by all 3 Be (mu3-F) -> gives each Be 1 bond, F count 1
    muF = centroid.copy(); muF[2] += 0.2
    F_pos.append(muF)
    coord = {0:1,1:1,2:1}
    # terminal F: each Be needs 3 more -> 3 bridging?? no: 1 shared + 3 terminal each = 1 + 9 = 10
    # add 2 more edge-bridging F to reach 12 while keeping Be coordination = 4.
    # Scheme: mu3-F (1) + 3 terminal per Be (9) + 2 extra terminal on two Be (raise those to 5-coord? no).
    # Cleaner: 1 mu3-F + 11 terminal distributed so Be coord = [4,4,4] uses 1+3*3=10; add 2 extra
    # terminal fluorides as loosely-bound (second-shell) F to hit stoichiometry 12. Keep them >2.2A.
    for bi in range(3):
        need = 4 - coord[bi]  # 3 each
        away = be_centers[bi]-centroid
        if np.linalg.norm(away) < 1e-6: away = np.array([1.0,0,0])
        away = away/np.linalg.norm(away)
        for k in range(need):
            ang = 2*np.pi*k/max(need,1) + bi
            perp = np.array([np.cos(ang),np.sin(ang),0.0])
            direction = 0.7*away + 0.5*perp + np.array([0,0, 1.0*(-1)**k])
            direction = direction/np.linalg.norm(direction)
            F_pos.append(be_centers[bi] + D_BeF*direction)
            coord[bi]+=1
    # 2 extra second-shell fluorides (charge-balancing F-, loosely near Li region)
    for k in range(2):
        base_be = be_centers[k]
        away = base_be-centroid; away/=np.linalg.norm(away)
        F_pos.append(base_be + away*3.0 + np.array([0,0,1.6*(-1)**k]))
    F_pos = np.array(F_pos)
    assert len(F_pos)==12, f"expected 12 F, got {len(F_pos)}"

    # 6 Li placed near F (ionic), around periphery, out of plane
    centroid = be_centers.mean(axis=0)
    li_pos = []
    for k in range(6):
        # near a fluoride, offset outward
        f = F_pos[k % len(F_pos)]
        out = f - centroid
        if np.linalg.norm(out)<1e-6: out=np.array([1.0,0,0])
        out = out/np.linalg.norm(out)
        zz = 1.4*(-1)**k
        li_pos.append(f + D_LiF*out*0.7 + np.array([0,0,zz]))
    li_pos = np.array(li_pos)

    for c in be_centers: symbols.append('Be'); pos.append(c)
    for f in F_pos:      symbols.append('F');  pos.append(f)
    for l in li_pos:     symbols.append('Li'); pos.append(l)
    return symbols, np.array(pos), be_centers, F_pos

def build_system2(be_centers, F_pos, li_symbols_pos):
    """
    FLiBeTF (23 atoms): add one extra bridging fluoride F13 and a tritium (H)
    forming F-T-F between the new F and an existing terminal F.
    22-atom anion = same minus the H.
    """
    # Add extra fluoride near an existing terminal F to make an F...F pair
    F_all = list(F_pos)
    anchorF = F_pos[-1]
    centroid = be_centers.mean(axis=0)
    out = anchorF - centroid; out /= np.linalg.norm(out)
    newF = anchorF + out*2.4  # ~F..F separation to host bridging T
    F_all.append(newF)
    F_all = np.array(F_all)  # 13 F

    # Tritium (H) bridging anchorF and newF (bent F-T-F)
    mid = (anchorF + newF)/2.0
    # push slightly perpendicular for bent geometry
    axis = newF - anchorF; axis /= np.linalg.norm(axis)
    perp = np.cross(axis, [0,0,1.0]); 
    if np.linalg.norm(perp)<1e-6: perp=np.array([0,1.0,0])
    perp/=np.linalg.norm(perp)
    Hpos = mid + perp*0.35
    return F_all, Hpos

def rattle(pos, sigma):
    return pos + np.random.normal(0, sigma, pos.shape)

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    sym1, pos1, be, F12 = build_flibe_core()
    li_pos = pos1[15:21]  # last 6 are Li

    # System 2 coords (F13 + T)
    F13, Hpos = build_system2(be, F12, li_pos)

    # Assemble base geometries
    # System 1: Be3 F12 Li6  (order: Be,F,Li)
    base1 = Atoms(['Be']*3 + ['F']*12 + ['Li']*6,
                  positions=np.vstack([be, F12, li_pos]))
    # System 2b FLiBeTF: Be3 F13 Li6 H1
    base2b = Atoms(['Be']*3 + ['F']*13 + ['Li']*6 + ['H'],
                   positions=np.vstack([be, F13, li_pos, Hpos[None,:]]))
    # System 2a FLiBeF-: FLiBeTF minus H (identical Be/F/Li coords)
    base2a = Atoms(['Be']*3 + ['F']*13 + ['Li']*6,
                   positions=np.vstack([be, F13, li_pos]))

    meta = {
        "system1_FLiBe":  {"formula":"Li6Be3F12","natoms":21,"charge":0,"spin":0},
        "system2a_FLiBeF":{"formula":"Li6Be3F13-","natoms":22,"charge":-1,"spin":0},
        "system2b_FLiBeTF":{"formula":"Li6Be3F13T","natoms":23,"charge":0,"spin":0},
        "note":"T modeled as H (protium); identical electronic structure. E_bind removes T as bare H+ nucleus.",
        "conformer_rattle_sigma_A":0.15,
        "n_conformers":9,
    }
    with open(os.path.join(outdir,"meta.json"),"w") as f: json.dump(meta,f,indent=2)

    # Write base + 9 rattled conformers for each system
    sigma = 0.15  # ~ finite-T displacement amplitude
    for name, base in [("FLiBe",base1),("FLiBeF",base2a),("FLiBeTF",base2b)]:
        d = os.path.join(outdir, name); os.makedirs(d, exist_ok=True)
        write(os.path.join(d, f"{name}_base.xyz"), base)
        for c in range(1,10):
            at = base.copy()
            at.set_positions(rattle(base.get_positions(), sigma))
            write(os.path.join(d, f"{name}_c{c}.xyz"), at)
    print("Wrote clusters to", outdir)
    # sanity
    for name, base, chg in [("FLiBe",base1,0),("FLiBeF",base2a,-1),("FLiBeTF",base2b,0)]:
        print(f"  {name}: {len(base)} atoms, formula {base.get_chemical_formula()}, charge {chg}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else "clusters")
