"""
Generate a synthetic Lu(H, N, Va)_3 dataset mimicking the paper's
1179 idealized 2x2x2 FCC supercell configurations.

Structure:
  - 2x2x2 FCC Lu supercell (8 Lu atoms) with a=5.03 Angstrom (LuH3 lattice)
  - Octahedral interstitial sites: 8 (Wyckoff 4b + supercell scaling => 8 per 2x2x2)
  - Tetrahedral interstitial sites: 16 (Wyckoff 8c ... => 16 per 2x2x2)
  - Paper mentions "3^{12} in 1x1x1 unit cell" => 12 interstitial sites/unit cell
  - Simplification here: use 24 total interstitial sites per supercell, each randomly
    occupied by H, N, or Va (vacancy = no atom placed)

Ground-truth "formation energy" per atom (pseudo-DFT):
  We use a physically-motivated bond-counting model that reproduces the paper's
  qualitative finding "low Ef,0 is correlated with high N content" (Figure 3, caption).

  Ef,0 [eV/atom] = ( sum of pair bond energies for interstitial-interstitial
                     and Lu-interstitial pairs within cutoff r_c=4.5 A )
                   / n_atoms
  Pair energies (eV):  Lu-H = -0.35,  Lu-N = -1.10,  H-H = +0.15,
                       H-N = -0.05, N-N = -0.60
  (These are chosen so Ef ranges roughly [-1.5, 0] eV/atom, matching Figure 2a
   colorbar in the paper. They are NOT DFT numbers; this is a synthetic pseudo-DFT
   target so CGCNN's fitting behavior can be checked.)

Output: work-alike CGCNN input dir with
   id_prop.csv  (id, Ef in eV/atom)
   <id>.cif     (idealized FCC structure)
   atom_init.json (copied from cgcnn/data/sample-regression)
"""
import os, json, random, shutil, sys, hashlib
import numpy as np
from pymatgen.core import Structure, Lattice
from ase import Atoms
from ase.io import write as ase_write, read as ase_read

random.seed(20260703)
np.random.seed(20260703)

OUT = "dataset_lu_h_n"
N_CONFIGS = 1000     # comparable order-of-magnitude to paper's 1179
A_LU = 5.03          # Angstrom, LuH3 fcc lattice
R_CUT = 4.5          # matches paper's r_c
PAIR = {
    ("H","H"): 0.15,  ("H","N"): -0.05, ("N","N"): -0.60,
    ("Lu","H"): -0.35, ("Lu","N"): -1.10, ("Lu","Lu"): 0.0,
}
def pair_e(a, b):
    key = tuple(sorted([a, b]))
    if key in PAIR: return PAIR[key]
    key = (a, b) if (a, b) in PAIR else (b, a)
    return PAIR.get(key, 0.0)

def build_fcc_lu_supercell(a):
    # Conventional FCC cubic cell (4 Lu) tiled 2x2x2 => 32 Lu?
    # Paper says 2x2x2 supercell. To keep runtimes small, use primitive fcc x (2,2,2).
    # Primitive fcc has 1 Lu; 2x2x2 => 8 Lu, plus 8 octahedral + 16 tetrahedral.
    lat = Lattice.from_parameters(a=a*2, b=a*2, c=a*2, alpha=90, beta=90, gamma=90)
    # 8 Lu at fcc conventional positions of the 2x2x2 primitive
    lu_sites = []
    for i in (0, 0.5):
        for j in (0, 0.5):
            for k in (0, 0.5):
                lu_sites.append((i, j, k))
    # octahedral: (1/2,1/2,1/2)-shifted from Lu => 8 sites in this conv 2x cell
    oct_sites = [(i+0.25, j+0.25, k+0.25) for i,j,k in lu_sites]
    # tetrahedral: (1/4,1/4,1/4) & (3/4,3/4,3/4) per fcc primitive => 16 in 2x2x2
    tet_sites = []
    for i,j,k in lu_sites:
        tet_sites.append((i+0.125, j+0.125, k+0.125))
        tet_sites.append((i+0.375, j+0.375, k+0.375))
    return lat, lu_sites, oct_sites, tet_sites

def random_config():
    """Return list of (species, frac_coord) for one supercell."""
    lat, lu, octs, tets = build_fcc_lu_supercell(A_LU)
    species, coords = [], []
    for s in lu:
        species.append("Lu"); coords.append(s)
    for s in octs + tets:
        occ = random.choices(["H","N","Va"], weights=[0.45, 0.35, 0.20])[0]
        if occ != "Va":
            species.append(occ); coords.append(s)
    return lat, species, coords

def formation_energy(structure):
    # sum pair energies for atoms within r_cut using pymatgen distances
    all_sites = structure.sites
    n = len(all_sites)
    dm = structure.distance_matrix  # NxN
    e = 0.0
    for i in range(n):
        for j in range(i+1, n):
            d = dm[i, j]
            if d < R_CUT:
                # simple cosine cutoff weight
                w = 0.5 * (np.cos(np.pi * d / R_CUT) + 1.0)
                e += w * pair_e(str(all_sites[i].specie), str(all_sites[j].specie))
    return e / n  # per atom

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # atom_init.json: use CGCNN's shipped one (elemental one-hot init)
    shutil.copy("cgcnn/data/sample-regression/atom_init.json",
                os.path.join(OUT, "atom_init.json"))

    rows = []
    for cid in range(N_CONFIGS):
        lat, sp, cc = random_config()
        s = Structure(lat, sp, cc, coords_are_cartesian=False)
        e = formation_energy(s)
        # write CIF via ASE (pymatgen 2024.10.3 requires explicit t/b mode in zopen)
        atoms = Atoms(symbols=sp,
                      scaled_positions=cc,
                      cell=lat.matrix,
                      pbc=True)
        ase_write(os.path.join(OUT, f"{cid}.cif"), atoms, format="cif")
        rows.append((cid, e))

    with open(os.path.join(OUT, "id_prop.csv"), "w") as f:
        for cid, e in rows:
            f.write(f"{cid},{e:.6f}\n")

    es = np.array([e for _, e in rows])
    print(f"[dataset] N={len(rows)}  Ef range [{es.min():.3f}, {es.max():.3f}] eV/atom")
    print(f"[dataset] mean={es.mean():.3f}  std={es.std():.3f}")
    # sanity: bin by N-content
    n_frac = []
    for cid in range(N_CONFIGS):
        a = ase_read(os.path.join(OUT, f"{cid}.cif"))
        syms = a.get_chemical_symbols()
        nl = sum(1 for x in syms if x=="Lu")
        nn = sum(1 for x in syms if x=="N")
        n_frac.append(nn/nl)
    n_frac = np.array(n_frac)
    print(f"[dataset] xN/xLu range [{n_frac.min():.2f}, {n_frac.max():.2f}]  mean={n_frac.mean():.2f}")
    # correlation Ef vs xN
    corr = np.corrcoef(n_frac, es)[0,1]
    print(f"[dataset] corr(xN/xLu, Ef) = {corr:.3f}   (paper: low Ef correlates with high N)")

if __name__ == "__main__":
    main()
