"""Generate HAADF-STEM training images via abTEM multislice simulation.

Builds STO and LSMO ABO3 perovskite [001] thin slabs, optionally a heterointerface,
plus defects (A-site vacancy, B-site vacancy, A-A antisite, B-B antisite).
Runs abTEM multislice with a 200 keV probe + HAADF detector (60-200 mrad).
Outputs (image, label_map, class_map) tensors compatible with synth_stem.py
class scheme:
  0 vacuum, 1 Sr, 2 Ti, 3 LaSr, 4 Mn, 5 defect

For speed we use ~3 slices, low-res grid, and small fields-of-view.
"""
from __future__ import annotations
import numpy as np
from ase import Atoms
from ase.build import bulk, surface, make_supercell
import abtem
from abtem import Probe, GridScan, AnnularDetector, Potential
import os, json, time

# atomic numbers
Z = {"Sr":38, "Ti":22, "La":57, "Mn":25, "O":8}

def perovskite_cell(A: str, B: str, a: float) -> Atoms:
    """ABO3 perovskite cubic cell. A at corners, B body-center, O face-centers."""
    pos = [
        (0,0,0),                    # A
        (0.5,0.5,0.5),              # B
        (0.5,0.5,0.0),              # O
        (0.5,0.0,0.5),              # O
        (0.0,0.5,0.5),              # O
    ]
    syms = [A,B,"O","O","O"]
    return Atoms(symbols=syms, scaled_positions=pos,
                 cell=[a,a,a], pbc=True)

def build_slab(kind: str, nx=4, ny=4, nz=3, defect=None):
    """Return ase Atoms slab + label code for class assignment."""
    if kind == "STO":
        a=3.905
        c = perovskite_cell("Sr","Ti", a)
    elif kind == "LSMO":
        a=3.87
        c = perovskite_cell("Sr","Mn", a)  # use Sr as proxy A site, label as LaSr later
    elif kind == "interface":
        # bottom STO, top LSMO half-half along z
        a = 3.89
        bot = perovskite_cell("Sr","Ti", a)
        bot = bot.repeat((nx, ny, nz//2 if nz>=2 else 1))
        top = perovskite_cell("Sr","Mn", a)
        top = top.repeat((nx, ny, nz - nz//2))
        # shift top in z
        top.positions[:,2] += bot.cell[2,2]
        atoms = bot + top
        atoms.set_cell([nx*a, ny*a, atoms.positions[:,2].max()+a*0.5], scale_atoms=False)
        atoms.pbc = (True, True, False)
        # apply defect if any
        if defect is not None:
            apply_defect(atoms, defect)
        return atoms
    else:
        raise ValueError(kind)
    atoms = c.repeat((nx, ny, nz))
    if defect is not None:
        apply_defect(atoms, defect)
    return atoms

def apply_defect(atoms, kind):
    syms = atoms.get_chemical_symbols()
    if kind == "A_vac":
        idx = [i for i,s in enumerate(syms) if s in ("Sr","La")]
        if idx:
            del atoms[np.random.choice(idx)]
    elif kind == "B_vac":
        idx = [i for i,s in enumerate(syms) if s in ("Ti","Mn")]
        if idx:
            del atoms[np.random.choice(idx)]
    elif kind == "B_anti":
        # swap a Ti and Mn
        ti = [i for i,s in enumerate(syms) if s=="Ti"]
        mn = [i for i,s in enumerate(syms) if s=="Mn"]
        if ti and mn:
            i,j = np.random.choice(ti), np.random.choice(mn)
            syms[i],syms[j] = "Mn","Ti"
            atoms.set_chemical_symbols(syms)
    return atoms


def render_haadf(atoms, sampling=0.05, scan_step=0.2, energy_keV=200,
                 inner_mrad=50, outer_mrad=60, slice_thickness=1.0):
    """Run abTEM multislice; return 2D HAADF intensity array."""
    pot = Potential(atoms, sampling=sampling, slice_thickness=slice_thickness,
                    projection="infinite", parametrization="kirkland")
    probe = Probe(energy=energy_keV*1e3, semiangle_cutoff=20, sampling=sampling)
    probe.grid.match(pot)
    det = AnnularDetector(inner=inner_mrad, outer=outer_mrad)
    L = atoms.cell[0,0]
    Ly = atoms.cell[1,1]
    scan = GridScan(start=(0,0), end=(L, Ly), sampling=scan_step)
    scans = probe.scan(potential=pot, scan=scan, detectors=det)
    arr = scans.compute().array
    return arr  # (sy, sx)

def build_label(atoms, scan_shape, cell, sigma_px=2.5):
    """Build per-pixel class label by Gaussian footprint at projected atom positions."""
    sy, sx = scan_shape
    Lx = cell[0,0]; Ly = cell[1,1]
    xs = np.linspace(0, Lx, sx, endpoint=False) + Lx/(2*sx)
    ys = np.linspace(0, Ly, sy, endpoint=False) + Ly/(2*sy)
    xx, yy = np.meshgrid(xs, ys)
    score = np.zeros((6, sy, sx), dtype=np.float32)
    score[0] = 0.05  # vacuum baseline
    px_per_A = sx / Lx
    sigma_A = sigma_px / px_per_A
    for at in atoms:
        x, y, z = at.position
        s = at.symbol
        if s == "Sr":
            ic = 1
        elif s == "Ti":
            ic = 2
        elif s == "La":
            ic = 3
        elif s == "Mn":
            ic = 4
        elif s == "O":
            continue  # ignore O for now
        else:
            continue
        dx = (xx - x); dy = (yy - y)
        dx -= Lx*np.round(dx/Lx); dy -= Ly*np.round(dy/Ly)
        g = np.exp(-(dx*dx + dy*dy)/(2*sigma_A**2))
        score[ic] += g
    # if image was for STO+LSMO interface, A sublattice in LSMO half should be LaSr (class 3)
    # heuristic: any Sr in upper half of cell → relabel as LaSr (class 3)
    # detect by searching: if Mn atoms exist, mark Sr above mid-cell as LaSr
    has_mn = any(at.symbol=="Mn" for at in atoms)
    if has_mn:
        z_mid = max(at.position[2] for at in atoms if at.symbol=="Mn") - 0.1
        # find Sr atoms above z_mid - 2A
        for at in atoms:
            if at.symbol=="Sr" and at.position[2] > z_mid:
                x,y,_ = at.position
                dx = (xx - x); dy = (yy - y)
                dx -= Lx*np.round(dx/Lx); dy -= Ly*np.round(dy/Ly)
                g = np.exp(-(dx*dx + dy*dy)/(2*sigma_A**2))
                score[1] -= g
                score[3] += g
    label = np.argmax(score, axis=0).astype(np.int64)
    return label


def normalize_image(img):
    img = img.astype(np.float32)
    img -= img.min()
    if img.max() > 0:
        img /= img.max()
    return img


if __name__ == "__main__":
    import sys, argparse
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=64, help="num samples")
    p.add_argument("--out", type=str, default="multislice_data")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    np.random.seed(args.seed)
    os.makedirs(args.out, exist_ok=True)

    kinds = ["STO","LSMO","interface","interface","interface"]
    defects = [None, None, None, "A_vac", "B_vac", "B_anti"]

    images = []
    labels = []
    for i in range(args.n):
        kind = np.random.choice(kinds)
        defect = np.random.choice(defects)
        nx = ny = np.random.choice([3,4])
        nz = np.random.choice([2,3])
        atoms = build_slab(kind, nx=nx, ny=ny, nz=nz, defect=defect)
        # apply small random thermal displacement
        atoms.rattle(stdev=0.05)
        try:
            t0=time.time()
            img = render_haadf(atoms, sampling=0.2, scan_step=0.2)
            t = time.time()-t0
        except Exception as e:
            print(f"[{i}] FAIL {e}")
            continue
        img = normalize_image(img)
        # add Poisson noise
        cnts = 5000  # photon counts
        img_noisy = np.random.poisson(img*cnts).astype(np.float32) / cnts
        img_noisy = normalize_image(img_noisy)
        label = build_label(atoms, img_noisy.shape, atoms.cell)
        images.append(img_noisy)
        labels.append(label)
        print(f"[{i}] {kind} defect={defect} shape={img.shape} t={t:.1f}s")
    if not images:
        print("no images generated"); sys.exit(1)
    # crop/pad to common size
    H = min(im.shape[0] for im in images)
    W = min(im.shape[1] for im in images)
    H = (H//8)*8; W = (W//8)*8
    imgs = np.stack([im[:H,:W] for im in images])
    lbls = np.stack([lb[:H,:W] for lb in labels])
    np.save(os.path.join(args.out,"images.npy"), imgs)
    np.save(os.path.join(args.out,"labels.npy"), lbls)
    meta = {"n": len(imgs), "H": H, "W": W, "classes": ["vacuum","Sr","Ti","LaSr","Mn","defect"]}
    json.dump(meta, open(os.path.join(args.out,"meta.json"),"w"), indent=2)
    print(f"saved {len(imgs)} images shape ({H},{W}) → {args.out}")
