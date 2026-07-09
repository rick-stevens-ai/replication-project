"""
Spot-check: load a G-NOME .vert.txt output and compute interchromosomal
bead clustering at the cluster radii used in Fig 1C/2C of Ingram et al. 2020
(PLoS Comput Biol 16(12): e1008476).

Definitions (from paper):
  clustering(CR) = average over all beads i of (#beads j != i within CR of i).
  interchromosomal clustering = average over all beads i of
       (#beads j on a DIFFERENT chromosome within CR of i).
  Homologous chromosomes are counted as the same chromosome (per paper).

Output: prints clustering vs. cluster radius. Should grow with CR and
should match the qualitative shape in Fig 2C (HMEC line).
"""
import sys
import pathlib
import re
import numpy as np
from scipy.spatial import cKDTree


def load_vert(path):
    """G-NOME .vert.txt: header lines start with '#', then 1 line per bead:
       seqid<TAB>x y z radius  (units = micrometres in the paper's defaults).
       Bead seqid contains the chromosome label (e.g. chr1_A, chr1_B, ...).
    """
    coords = []
    chroms = []
    radii = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = re.split(r"\s+", line.strip())
            # Actual G-NOME .vert.txt body format observed:
            #   chrom  homologue_id  x  y  z  radius  bp_length
            # e.g. 'chr10 A 65.69 -125.91 64.44 1.0 2950000'
            if len(parts) < 6:
                continue
            chrom = parts[0]          # e.g. 'chr10'
            # parts[1] is homologue label 'A' or 'B' — paper says homologues
            # are treated as same chromosome, so collapse to bare chrom name.
            base = chrom
            try:
                x, y, z, r = (float(parts[2]), float(parts[3]),
                              float(parts[4]), float(parts[5]))
            except ValueError:
                continue
            coords.append((x, y, z))
            chroms.append(base)
            radii.append(r)
    return np.asarray(coords, dtype=float), np.asarray(chroms), np.asarray(radii)


def clustering_curves(coords, chroms, radii_nm):
    """For each cluster radius CR (nm), compute mean total / inter / intra
    clustering per bead. Assumes coords already in nm; we will convert
    from µm → nm at the call site if needed.
    """
    tree = cKDTree(coords)
    n = len(coords)
    out = []
    for CR in radii_nm:
        idx_lists = tree.query_ball_point(coords, r=CR)
        total = 0
        inter = 0
        intra = 0
        for i, neigh in enumerate(idx_lists):
            # exclude self
            others = [j for j in neigh if j != i]
            total += len(others)
            same = sum(1 for j in others if chroms[j] == chroms[i])
            intra += same
            inter += len(others) - same
        out.append((CR, total / n, inter / n, intra / n))
    return out


def main():
    vert = pathlib.Path(sys.argv[1])
    coords_um, chroms, radii = load_vert(vert)
    print(f"Loaded {len(coords_um)} beads, {len(set(chroms))} unique chromosomes "
          f"(after collapsing homologues).", file=sys.stderr)
    # Convert µm → nm so cluster radii are in nm (paper uses nm everywhere
    # for cluster radius axes).
    coords_nm = coords_um * 1000.0
    CRs = [100, 200, 300, 400, 500, 700, 1000, 1500, 2000]
    rows = clustering_curves(coords_nm, chroms, CRs)
    print("cluster_radius_nm\ttotal_mean\tinter_mean\tintra_mean")
    for CR, tot, inter, intra in rows:
        print(f"{CR}\t{tot:.3f}\t{inter:.3f}\t{intra:.3f}")


if __name__ == "__main__":
    main()
