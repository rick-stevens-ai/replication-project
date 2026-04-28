"""
linclust_py.py — Independent Python reimplementation of the core Linclust
algorithm from Steinegger & Söding (2018), "Clustering huge protein sequence
sets in linear time" (Nature Communications; OSTI 1624105).

The real Linclust (in MMseqs2) is written in heavily optimised C++ with SIMD
ungapped alignment, amino-acid reduced alphabets, vectorised hashing, and
distributed sort. This file is a pedagogical *from-scratch* reimplementation
that preserves the algorithmic essentials needed to demonstrate the paper's
central claim — linear-time clustering — and to benchmark it against a naive
O(N^2) greedy clusterer.

Algorithmic skeleton (simplified):
  1. For each sequence s_i, extract all overlapping k-mers.
  2. Select the m k-mers with the smallest hash values ("bottom-m sketch"
     a.k.a. mini-hashes).  This is the same bottom-m sampling used by
     Linclust, giving each sequence a constant-size set of k-mers
     (independent of sequence length beyond the minimum).
  3. Group sequences by selected k-mer.  For every k-mer group, the
     longest sequence in the group becomes the *center candidate*; every
     other group member proposes that center.
  4. For each sequence, consider all proposed centers.  Verify with a
     simple ungapped Hamming-identity alignment (Linclust uses SIMD
     ungapped + optional SW). Join the first (longest, lowest-id)
     center that meets the sequence-identity threshold.  Sequences with
     no valid center become their own cluster representatives.

The implementation is dependency-light (numpy only, biopython optional).
"""

from __future__ import annotations
import hashlib
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple


# ---------------------------------------------------------------------------
# k-mer utilities
# ---------------------------------------------------------------------------

def _hash_kmer(kmer: str) -> int:
    """64-bit stable hash of a k-mer string.  blake2b is fast & uniform."""
    return int.from_bytes(
        hashlib.blake2b(kmer.encode("ascii"), digest_size=8).digest(),
        "little",
        signed=False,
    )


def select_minimizers(seq: str, k: int, m: int) -> List[Tuple[int, str]]:
    """Return up to m (hash, kmer) tuples with the smallest hashes.

    This is the bottom-m sketch used by Linclust (section: "reduced k-mer
    selection").  Runtime O(L log m) per sequence of length L.
    """
    if len(seq) < k:
        return []
    items: List[Tuple[int, str]] = []
    # maintain a simple list then sort — m is small (e.g. 20), so fine.
    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        items.append((_hash_kmer(kmer), kmer))
    items.sort(key=lambda t: t[0])
    # de-duplicate on k-mer while preserving sort order
    seen = set()
    out: List[Tuple[int, str]] = []
    for h, km in items:
        if km in seen:
            continue
        seen.add(km)
        out.append((h, km))
        if len(out) >= m:
            break
    return out


# ---------------------------------------------------------------------------
# Alignment-verification: ungapped identity
# ---------------------------------------------------------------------------

def ungapped_identity(a: str, b: str) -> float:
    """Best ungapped sequence identity over all offsets.

    Linclust's verification step performs a fast SIMD ungapped alignment
    between the query and center using the shared k-mer as an anchor.  For
    our Python reimplementation we scan all offsets and compute the best
    Hamming identity over the overlap length, which is equivalent when the
    two sequences share substantial homology.
    """
    if not a or not b:
        return 0.0
    best = 0.0
    # Limit offset scan for speed; shift by -len(b)+1 .. len(a)-1
    # For short seqs that's negligible; for long seqs we cap.
    max_shift = 64
    la, lb = len(a), len(b)
    for shift in range(-min(max_shift, lb - 1), min(max_shift, la - 1) + 1):
        # overlap region
        ia0 = max(0, shift)
        ib0 = max(0, -shift)
        overlap = min(la - ia0, lb - ib0)
        if overlap < 10:
            continue
        matches = 0
        for t in range(overlap):
            if a[ia0 + t] == b[ib0 + t]:
                matches += 1
        idn = matches / overlap
        if idn > best:
            best = idn
    return best


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

@dataclass
class ClusterResult:
    representatives: List[int] = field(default_factory=list)  # seq indices
    assignments: List[int] = field(default_factory=list)      # per-seq -> rep idx
    runtime_s: float = 0.0
    n_sequences: int = 0
    algorithm: str = ""


def linclust(
    sequences: Sequence[str],
    k: int = 10,
    m: int = 20,
    min_identity: float = 0.7,
) -> ClusterResult:
    """Linear-time clustering a la Linclust.

    Complexity: O(N * (L + m log m)) extraction + O(total_kmers) grouping +
    O(sum_i C_i * L) verification, where C_i is the number of distinct
    center candidates proposed for sequence i, bounded by m.  For fixed k,m
    this is *linear* in the number of sequences.
    """
    t0 = time.time()
    N = len(sequences)
    lengths = [len(s) for s in sequences]

    # Phase 1+2: per-sequence minimizers
    sketch: List[List[Tuple[int, str]]] = [
        select_minimizers(s, k=k, m=m) for s in sequences
    ]

    # Phase 3: group by k-mer, longest seq = center candidate.
    kmer_to_center: Dict[str, int] = {}
    kmer_to_members: Dict[str, List[int]] = {}
    for i, sk in enumerate(sketch):
        for _, km in sk:
            cur = kmer_to_center.get(km, -1)
            if cur < 0 or lengths[i] > lengths[cur] or (
                lengths[i] == lengths[cur] and i < cur
            ):
                kmer_to_center[km] = i
            kmer_to_members.setdefault(km, []).append(i)

    # Phase 4: for every sequence, collect proposed centers via its k-mers
    assignments = [-1] * N
    reps: List[int] = []
    # Deterministic order: sort by descending length then index — longest
    # sequences get evaluated first and act as potential centers for others.
    order = sorted(range(N), key=lambda i: (-lengths[i], i))

    for i in order:
        if assignments[i] != -1:
            continue
        proposed = set()
        for _, km in sketch[i]:
            c = kmer_to_center.get(km, -1)
            if c != -1 and c != i:
                proposed.add(c)
        best_center = -1
        best_id = 0.0
        for c in proposed:
            # only consider already-selected representatives
            if assignments[c] == -1 or assignments[c] != c:
                continue
            idn = ungapped_identity(sequences[i], sequences[c])
            if idn >= min_identity and idn > best_id:
                best_id = idn
                best_center = c
        if best_center == -1:
            # become a representative
            reps.append(i)
            assignments[i] = i
        else:
            assignments[i] = best_center

    return ClusterResult(
        representatives=reps,
        assignments=assignments,
        runtime_s=time.time() - t0,
        n_sequences=N,
        algorithm=f"linclust(k={k},m={m},id={min_identity})",
    )


def naive_cluster(
    sequences: Sequence[str],
    min_identity: float = 0.7,
) -> ClusterResult:
    """Naive CD-HIT-like greedy clustering with O(N^2) pairwise comparisons.

    Sequences are processed in decreasing length order.  Each sequence is
    compared to every existing representative; if identity >= threshold it
    joins that cluster, else it becomes a new representative.
    """
    t0 = time.time()
    N = len(sequences)
    order = sorted(range(N), key=lambda i: (-len(sequences[i]), i))
    assignments = [-1] * N
    reps: List[int] = []
    for i in order:
        best_center = -1
        best_id = min_identity
        for c in reps:
            idn = ungapped_identity(sequences[i], sequences[c])
            if idn >= best_id:
                best_id = idn
                best_center = c
        if best_center == -1:
            reps.append(i)
            assignments[i] = i
        else:
            assignments[i] = best_center
    return ClusterResult(
        representatives=reps,
        assignments=assignments,
        runtime_s=time.time() - t0,
        n_sequences=N,
        algorithm=f"naive(id={min_identity})",
    )


# ---------------------------------------------------------------------------
# Synthetic-dataset generator with known ground-truth clusters
# ---------------------------------------------------------------------------

AA = "ACDEFGHIKLMNPQRSTVWY"


def gen_dataset(
    n_families: int,
    seqs_per_family: int,
    length: int = 120,
    mut_rate: float = 0.15,
    seed: int = 0,
) -> Tuple[List[str], List[int]]:
    """Return (sequences, ground_truth_family) lists.

    Each family has a random 'center' protein; members are produced by
    substituting each residue independently with probability ``mut_rate``.
    Family size is constant for simplicity.
    """
    rng = random.Random(seed)
    seqs: List[str] = []
    gt: List[int] = []
    for fam in range(n_families):
        center = "".join(rng.choice(AA) for _ in range(length))
        seqs.append(center)
        gt.append(fam)
        for _ in range(seqs_per_family - 1):
            mutated = []
            for r in center:
                if rng.random() < mut_rate:
                    mutated.append(rng.choice(AA))
                else:
                    mutated.append(r)
            seqs.append("".join(mutated))
            gt.append(fam)
    # shuffle so order isn't a giveaway
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    seqs = [seqs[i] for i in idx]
    gt = [gt[i] for i in idx]
    return seqs, gt


# ---------------------------------------------------------------------------
# Cluster quality metrics vs ground truth
# ---------------------------------------------------------------------------

def pairwise_prf(assignments: Sequence[int], gt: Sequence[int]) -> Dict[str, float]:
    """Pair-counting precision/recall/F1 over all O(N^2) pairs.

    A 'positive' pair is one that shares a ground-truth family;
    predicted-positive if same cluster representative.
    """
    from collections import defaultdict
    gt_groups: Dict[int, List[int]] = defaultdict(list)
    pred_groups: Dict[int, List[int]] = defaultdict(list)
    for i, g in enumerate(gt):
        gt_groups[g].append(i)
    for i, a in enumerate(assignments):
        pred_groups[a].append(i)

    def pair_count(groups: Dict[int, List[int]]) -> int:
        return sum(len(v) * (len(v) - 1) // 2 for v in groups.values())

    true_pairs = pair_count(gt_groups)
    pred_pairs = pair_count(pred_groups)

    # TP: in same predicted AND same true
    tp = 0
    # index items: map each item to predicted cluster, then count per (pred, true)
    from collections import Counter
    joint = Counter((assignments[i], gt[i]) for i in range(len(gt)))
    for _, cnt in joint.items():
        tp += cnt * (cnt - 1) // 2

    prec = tp / pred_pairs if pred_pairs else 0.0
    rec = tp / true_pairs if true_pairs else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {"precision": prec, "recall": rec, "f1": f1}


if __name__ == "__main__":
    seqs, gt = gen_dataset(n_families=50, seqs_per_family=10, length=100,
                           mut_rate=0.15, seed=1)
    r1 = linclust(seqs, k=8, m=20, min_identity=0.6)
    r2 = naive_cluster(seqs, min_identity=0.6)
    print("linclust:", len(r1.representatives), "reps in", f"{r1.runtime_s:.3f}s",
          pairwise_prf(r1.assignments, gt))
    print("naive   :", len(r2.representatives), "reps in", f"{r2.runtime_s:.3f}s",
          pairwise_prf(r2.assignments, gt))
