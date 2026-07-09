#!/usr/bin/env python3
"""
mash_tree.py — Pure-Python re-implementation of the Mash MinHash genome-distance
method (Ondov et al. 2016), which Bazinet (2017) uses (Mash + FastME) to decide
which species belong to Bacillus cereus sensu lato and to build a rapid
distance-based phylogeny.

We compute, for each genome:
  - the bottom-sketch MinHash of its canonical k-mers (k=21, sketch size s=1000),
then estimate pairwise Mash distance
  D = -1/k * ln( 2j / (1+j) ),   j = Jaccard estimate from shared hashes,
and build a distance tree (neighbor-joining) with Biopython.

This is the method-level core of the paper's species-delineation / rapid
phylogeny step, run on a small public surrogate set of complete B. cereus s.l.
genomes (+ outgroups) downloaded from NCBI RefSeq.
"""
import sys, glob, os
import numpy as np

K = 21
SKETCH = 1000

# 2-bit encoding, vectorized rolling k-mer hashing (fast, NumPy).
_MAP = np.full(256, -1, dtype=np.int64)
for c, v in zip(b"ACGT", (0, 1, 2, 3)):
    _MAP[c] = v
_MASK64 = np.uint64(0xFFFFFFFFFFFFFFFF)
# 64-bit mixing constant (splitmix64-style) to spread 2k-bit codes uniformly.
_MIX = np.uint64(0x9E3779B97F4A7C15)

def _mix64(x):
    x = np.asarray(x, dtype=np.uint64)
    x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    x = x ^ (x >> np.uint64(31))
    return x

def canonical_kmer_hashes_np(seq_bytes, k=K):
    codes = _MAP[np.frombuffer(seq_bytes, dtype=np.uint8)]
    n = codes.size
    if n < k:
        return np.empty(0, dtype=np.uint64)
    # forward 2-bit rolling value per position (only where all k bases valid)
    valid = (codes >= 0).astype(np.int8)
    codes_u = np.where(codes >= 0, codes, 0).astype(np.uint64)
    # build k-mer integer via sliding window using powers of 4
    # fwd[i] = sum_{j} codes[i+j] * 4^(k-1-j)
    pows = (np.uint64(4) ** np.arange(k-1, -1, -1, dtype=np.uint64))
    # windowed dot: use stride trick
    from numpy.lib.stride_tricks import sliding_window_view
    win = sliding_window_view(codes_u, k)               # (n-k+1, k)
    fwd = (win * pows).sum(axis=1).astype(np.uint64)
    # reverse complement code: comp = 3 - base, reversed order
    rcwin = (np.uint64(3) - win)[:, ::-1]
    rev = (rcwin * pows).sum(axis=1).astype(np.uint64)
    canon = np.minimum(fwd, rev)
    # mask windows containing any invalid base
    vwin = sliding_window_view(valid, k)
    ok = vwin.all(axis=1)
    canon = canon[ok]
    return _mix64(canon)

def sketch_of_fasta(path, k=K, s=SKETCH):
    from Bio import SeqIO
    seqs = [str(r.seq).upper() for r in SeqIO.parse(path, "fasta")]
    full = ("N".join(seqs)).encode()
    h = canonical_kmer_hashes_np(full, k)
    u = np.unique(h)
    return u[:s]  # bottom-sketch: s smallest hashes

def jaccard_from_sketches(a, b, s=SKETCH):
    # merge bottom sketches, count shared among the s smallest of the union
    sa, sb = set(a.tolist()), set(b.tolist())
    union_sorted = sorted(sa | sb)[:s]
    us = set(union_sorted)
    shared = len(us & sa & sb)
    return shared / len(union_sorted)

def mash_distance(j, k=K):
    if j <= 0:
        return 1.0
    if j >= 1:
        return 0.0
    return -1.0/k * np.log(2*j/(1+j))

def main(gdir, out_json, out_nwk):
    import json
    fnas = sorted(glob.glob(os.path.join(gdir, "**", "*.fna"), recursive=True))
    names = {}
    # map accession -> organism
    rep = glob.glob(os.path.join(gdir, "**", "assembly_data_report.jsonl"), recursive=True)
    if rep:
        for line in open(rep[0]):
            d = json.loads(line)
            names[d["accession"]] = d.get("organism", {}).get("organismName", d["accession"])
    labels, sketches = [], []
    for f in fnas:
        acc = os.path.basename(os.path.dirname(f))
        org = names.get(acc, acc)
        short = org.replace("[","").replace("]","")
        # short label
        parts = short.split()
        lab = "_".join(parts[:3]) + f"__{acc}"
        labels.append(lab)
        sketches.append(sketch_of_fasta(f))
        print(f"sketched {lab}  ({len(sketches[-1])} hashes)")
    N = len(labels)
    D = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            jac = jaccard_from_sketches(sketches[i], sketches[j])
            d = mash_distance(jac)
            D[i, j] = D[j, i] = d
    # print matrix
    print("\nMash distance matrix:")
    print("        " + " ".join(f"{l.split('__')[0][:10]:>10}" for l in labels))
    for i in range(N):
        print(f"{labels[i].split('__')[0][:10]:>10} " + " ".join(f"{D[i,j]:10.4f}" for j in range(N)))
    # NJ tree via Biopython
    from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
    lower = [[float(D[i][j]) for j in range(i+1)] for i in range(N)]
    dm = DistanceMatrix(names=labels, matrix=lower)
    tree = DistanceTreeConstructor().nj(dm)
    from Bio import Phylo
    Phylo.write(tree, out_nwk, "newick")
    print(f"\nwrote NJ tree -> {out_nwk}")
    Phylo.draw_ascii(tree)
    json.dump({"labels": labels, "k": K, "sketch": SKETCH,
               "distance_matrix": D.tolist()}, open(out_json, "w"), indent=2)
    print(f"wrote distances -> {out_json}")

if __name__ == "__main__":
    gdir = sys.argv[1] if len(sys.argv) > 1 else "genomes"
    main(gdir, sys.argv[2] if len(sys.argv) > 2 else "mash_distances.json",
         sys.argv[3] if len(sys.argv) > 3 else "mash_tree.nwk")
