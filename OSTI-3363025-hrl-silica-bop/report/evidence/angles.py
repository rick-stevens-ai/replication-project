import sys, math
import numpy as np
def parse_lammps_data(fn):
    lines = open(fn).readlines()
    atoms = []
    bounds = {}
    tilt = None
    in_atoms = False
    hdr = True
    for i,l in enumerate(lines):
        s = l.strip()
        if not s: continue
        if "xlo xhi" in l:
            p=s.split(); bounds["x"]=(float(p[0]),float(p[1]))
        elif "ylo yhi" in l:
            p=s.split(); bounds["y"]=(float(p[0]),float(p[1]))
        elif "zlo zhi" in l:
            p=s.split(); bounds["z"]=(float(p[0]),float(p[1]))
        elif "xy xz yz" in l:
            p=s.split(); tilt=(float(p[0]),float(p[1]),float(p[2]))
        elif s.startswith("Atoms"):
            in_atoms = True; continue
        elif s.startswith("Velocities") or s.startswith("Bonds"):
            in_atoms = False
        elif in_atoms and len(s.split())>=7 and s[0].isdigit():
            p=s.split()
            atoms.append((int(p[0]), int(p[2]), float(p[4]), float(p[5]), float(p[6])))
    return bounds, tilt, atoms
def build_positions(atoms, bounds, tilt):
    xlo,xhi=bounds["x"]; ylo,yhi=bounds["y"]; zlo,zhi=bounds["z"]
    xy,xz,yz = tilt if tilt else (0,0,0)
    lx=xhi-xlo; ly=yhi-ylo; lz=zhi-zlo
    return atoms, np.array([[lx,0,0],[xy,ly,0],[xz,yz,lz]])
def compute_angles(atoms, box, r_si_o_cut=2.2):
    ids = [a[0] for a in atoms]
    types = np.array([a[1] for a in atoms])
    coords = np.array([[a[2],a[3],a[4]] for a in atoms])
    # find Si (type 1) and O (type 2)
    invbox = np.linalg.inv(box)
    def min_image(dr):
        s = dr @ invbox
        s = s - np.round(s)
        return s @ box
    # For each Si, list its O neighbors within cutoff
    si_idx = np.where(types==1)[0]
    o_idx  = np.where(types==2)[0]
    si_neigh = {i:[] for i in si_idx}
    o_neigh  = {i:[] for i in o_idx}
    for i in si_idx:
        for j in o_idx:
            dr = coords[j] - coords[i]
            dr = min_image(dr)
            d = np.linalg.norm(dr)
            if d < r_si_o_cut:
                si_neigh[i].append((j,d))
                o_neigh[j].append((i,d))
    # O-Si-O angles: for each Si with >=2 O neighbors
    osioangles=[]
    for i,nbrs in si_neigh.items():
        for a in range(len(nbrs)):
            for b in range(a+1,len(nbrs)):
                ja,_ = nbrs[a]; jb,_ = nbrs[b]
                v1 = min_image(coords[ja]-coords[i])
                v2 = min_image(coords[jb]-coords[i])
                cos = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
                cos = max(-1,min(1,cos))
                osioangles.append(math.degrees(math.acos(cos)))
    # Si-O-Si angles: for each O with 2 Si neighbors
    sioSiangles=[]
    for i,nbrs in o_neigh.items():
        if len(nbrs)>=2:
            for a in range(len(nbrs)):
                for b in range(a+1,len(nbrs)):
                    ja,_ = nbrs[a]; jb,_ = nbrs[b]
                    v1 = min_image(coords[ja]-coords[i])
                    v2 = min_image(coords[jb]-coords[i])
                    cos = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
                    cos = max(-1,min(1,cos))
                    sioSiangles.append(math.degrees(math.acos(cos)))
    return osioangles, sioSiangles, si_neigh, o_neigh
if __name__=="__main__":
    fn = sys.argv[1]
    b,t,a = parse_lammps_data(fn)
    coords, box = build_positions(a,b,t)
    osi, sios, si_n, o_n = compute_angles(coords, box)
    print(f"FILE={fn}")
    print(f"N_atoms={len(a)}, N_Si={sum(1 for x in a if x[1]==1)}, N_O={sum(1 for x in a if x[1]==2)}")
    # coordination distribution
    from collections import Counter
    si_cn = Counter(len(v) for v in si_n.values())
    o_cn = Counter(len(v) for v in o_n.values())
    print(f"Si coordination: {dict(si_cn)}")
    print(f"O coordination: {dict(o_cn)}")
    print(f"O-Si-O: n={len(osi)}, mean={np.mean(osi):.2f}, std={np.std(osi):.2f}")
    print(f"Si-O-Si: n={len(sios)}, mean={np.mean(sios):.2f}, std={np.std(sios):.2f}")
