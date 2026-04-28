# Replication plan — OSTI 2587579

**Target paper:** Barwey et al., "Mesh-based Super-Resolution of Fluid Flows with
Multiscale Graph Neural Networks", CMAME 2025.

## Goal
Reproduce the multiscale GNN super-resolution pipeline end-to-end, including the
coincident-node synchronization layer that is the paper's headline contribution.

## Hardware path
1. **Primary:** chiatta00 (JLSE Aurora-class, 8× Intel Max GPUs, oneAPI).
   - Risk: requires building Intel Extension for PyTorch (IPEX) + PyG from source.
2. **Fallback:** uicgpu (8× A100 80GB, CUDA). Selected after assessing chiatta00.

## Steps
1. Pull paper PDF from arXiv (v4, May 2025).
2. Find author code: `github.com/sbarwey` → `DDP_PyGeom` (training) and
   `nekRS-GNN/3rd_party/gnn` (distributed, halo-swap version).
3. Clone, inspect `models/gnn.py::Multiscale_MessagePassing_UNet` and
   `models/gnn_v2.py::DistributedMessagePassingLayer`. Confirm halo-swap +
   `index_add_` is the spectral-element-aware coincident-node sync.
4. Set up Python env on selected GPU host:
   - PyTorch 2.4.1, PyG 2.6.1, torch-scatter, torch-cluster, pyvista < 0.43,
     hydra, numpy < 2.
5. Construct a small spectral-element-style mesh problem:
   - 4×4 quadrilateral elements, p_hi=7 (8×8 GLL-like nodes/element)
   - intra-element edges only, coincident boundary nodes duplicated
   - target field = analytic Taylor-Green-style flow at random parameters
   - input = bilinearly coarsened-then-prolongated field at p_lo=3
6. Train the paper's `Multiscale_MessagePassing_UNet` (depth-2, hidden=64,
   ~300k params) for 80 epochs with Adam(1e-3) + cosine schedule.
7. Compare best validation rel-L2 vs the interpolation-only baseline.
8. Document gap to the full paper (BFS 3D dataset not reproduced — see README).

## Acceptance
- Model runs end-to-end with author's code unmodified ✓
- Coincident-node topology present in mesh (165 groups, 183 dups) ✓
- GNN achieves ≥3× error reduction over interpolation baseline ✓ (4.77×)
- Honest report of what was and was not reproduced ✓
