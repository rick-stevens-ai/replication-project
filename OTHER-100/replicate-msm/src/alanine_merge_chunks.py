"""
Merge chunk results into single dihedrals_short.npz.
Usage: python alanine_merge_chunks.py <n_chunks>
"""
import numpy as np
import sys
from pathlib import Path

if __name__ == "__main__":
    n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    data_dir = Path(__file__).parent.parent / "data" / "alanine_short"

    chunks = []
    for i in range(n_chunks):
        p = data_dir / f"dihedrals_chunk{i}.npz"
        if not p.exists():
            print(f"Missing chunk {i}: {p}")
            sys.exit(1)
        d = np.load(p)
        chunks.append(d['dihedrals'])
        print(f"  chunk {i}: {d['dihedrals'].shape[0]} sims, idx [{int(d['start_idx'])}, {int(d['end_idx'])})")

    merged = np.concatenate(chunks, axis=0)
    start_probs = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
    n_per_struct = np.round(start_probs * 11388).astype(int)
    n_per_struct[-1] = 11388 - n_per_struct[:-1].sum()

    out = data_dir / "dihedrals_short.npz"
    np.savez(out, dihedrals=merged, start_probs=start_probs, n_per_struct=n_per_struct)
    print(f"\nMerged {merged.shape[0]} sims → {out} — shape {merged.shape}")
