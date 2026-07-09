"""Parse the 1ZBB tetranucleosome PDB.

Extracts per-nucleotide backbone target positions for both DNA chains (I and J)
and returns:
  - nt_centers: (N, 3) array of per-nucleotide backbone phosphate positions (Å)
  - nt_chain:   (N,) array of chain id ('I' or 'J')
  - nt_resseq:  (N,) array of resseq within the chain
  - serial_index: (N,) 1..N serial index across chains in chain-order (matches
    paper's nucleotide-pair serial index referenced in Figure 1).

The paper says N=694 bp; in the original 1ZBB PDB, DNA chains I and J each have
347 nucleotides (346 with P atoms; the 5'-end residue has no P). We use the
P-atom location as the per-nucleotide backbone target; for the 5'-end residue
without P, we substitute the C5' atom position.
"""

from __future__ import annotations

import numpy as np


def parse_1zbb(path: str = "1zbb.pdb"):
    chain_atoms: dict[str, dict[int, dict[str, np.ndarray]]] = {"I": {}, "J": {}}

    # Atoms in the ribose-phosphate backbone of a DNA nucleotide (PDB4DNA
    # ribose-phosphate moiety, the strand-break target):
    BACKBONE_ATOMS = {"P", "OP1", "OP2", "O5'", "C5'", "C4'", "O4'", "C3'",
                      "O3'", "C2'", "C1'"}

    with open(path) as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            chain = line[21]
            if chain not in ("I", "J"):
                continue
            res = line[17:20].strip()
            if res not in ("DA", "DC", "DG", "DT"):
                continue
            atom = line[12:16].strip()
            resseq = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            chain_atoms[chain].setdefault(resseq, {})[atom] = np.array([x, y, z])

    centers = []
    chains = []
    resseqs = []
    bb_atoms = []  # list of (n_atoms, 3) backbone-atom coordinates per nt
    for chain in ("I", "J"):
        for resseq in sorted(chain_atoms[chain].keys()):
            atoms = chain_atoms[chain][resseq]
            # Primary backbone position (P preferred, C5' fallback) for centroid
            if "P" in atoms:
                pos = atoms["P"]
            elif "C5'" in atoms:
                pos = atoms["C5'"]
            else:
                pos = np.mean(list(atoms.values()), axis=0)
            centers.append(pos)
            chains.append(chain)
            resseqs.append(resseq)
            # All backbone atoms of the nucleotide for sub-target detection
            bb_list = [atoms[a] for a in BACKBONE_ATOMS if a in atoms]
            if len(bb_list) == 0:
                bb_list = [pos]
            bb_atoms.append(np.array(bb_list))

    centers = np.array(centers)
    chains = np.array(chains)
    resseqs = np.array(resseqs)
    serial = np.arange(1, len(centers) + 1)
    return centers, chains, resseqs, serial, bb_atoms


if __name__ == "__main__":
    centers, chains, resseqs, serial, bb_atoms = parse_1zbb()
    print(f"Total nucleotide backbone targets: {len(centers)}")
    print(f"Per chain: I={np.sum(chains == 'I')}, J={np.sum(chains == 'J')}")
    bb_min = centers.min(axis=0) / 10.0
    bb_max = centers.max(axis=0) / 10.0
    bb_size = bb_max - bb_min
    print(f"DNA backbone bounding box (nm): "
          f"x={bb_size[0]:.1f}, y={bb_size[1]:.1f}, z={bb_size[2]:.1f}")
    centroid = centers.mean(axis=0) / 10.0
    print(f"DNA centroid (nm): {centroid}")

    # Flatten backbone sub-target atoms into a single (M, 3) array with a
    # parallel (M,) array mapping each sub-target to its parent nucleotide.
    total_atoms = sum(b.shape[0] for b in bb_atoms)
    flat = np.zeros((total_atoms, 3))
    parent = np.zeros(total_atoms, dtype=np.int64)
    off = 0
    for i, b in enumerate(bb_atoms):
        n = b.shape[0]
        flat[off:off + n] = b
        parent[off:off + n] = i
        off += n
    print(f"Backbone sub-target atoms: {total_atoms} (mean {total_atoms/len(centers):.1f} per nt)")

    np.savez(
        "nt_targets.npz",
        centers_A=centers,
        chains=chains,
        resseqs=resseqs,
        serial=serial,
        bb_flat_A=flat,
        bb_parent=parent,
    )
    print("Saved nt_targets.npz")
