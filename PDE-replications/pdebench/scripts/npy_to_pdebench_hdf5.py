"""Convert PDEBench data_gen_NLE .npy advection outputs into the HDF5 format
expected by PDEBench training code (FNODatasetSingle / UNetDatasetSingle).

The HDF5 needs:
  - dataset 'tensor': shape (b, t, x) float32  -- the solution snapshots
  - dataset 'x-coordinate': shape (x,)
  - dataset 't-coordinate': shape (t,)

This matches the public PDEBench file '1D_Advection_Sols_beta1.0.hdf5'.
"""
from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import h5py


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", required=True, help="dir with 1D_Advection_Sols_beta*.npy and x_coordinate.npy/t_coordinate.npy")
    ap.add_argument("--beta", default="1.0")
    ap.add_argument("--out", required=True, help="destination .hdf5 path")
    args = ap.parse_args()

    src = Path(args.src_dir)
    u = np.load(src / f"1D_Advection_Sols_beta{args.beta}.npy").astype(np.float32)
    x = np.load(src / "x_coordinate.npy").astype(np.float32)
    t = np.load(src / "t_coordinate.npy").astype(np.float32)

    # u shape from generator: (b, it_tot, nx). It_tot includes both the initial slot
    # and the final overwrite at index it_tot-1 (uu[-1]). t has it_tot+1 entries (off by one).
    # Match official dataset convention by using t[:u.shape[1]].
    t_match = t[: u.shape[1]]

    print(f"u  shape={u.shape}  dtype={u.dtype}")
    print(f"x  shape={x.shape}  dtype={x.dtype}")
    print(f"t  shape={t_match.shape}  dtype={t_match.dtype}  (truncated from {t.shape})")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(out_path, "w") as f:
        f.create_dataset("tensor", data=u, compression="gzip")
        f.create_dataset("x-coordinate", data=x)
        f.create_dataset("t-coordinate", data=t_match)
    print(f"wrote {out_path}  size={out_path.stat().st_size/1e6:.2f} MB")


if __name__ == "__main__":
    main()
