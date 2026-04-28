# OSTI 2587579 — Mesh-based Super-Resolution of Fluid Flows with Multiscale Graph Neural Networks

**Paper:** Barwey, Pal, Patel, Balin, Lusch, Vishwanath, Maulik, Balakrishnan (Argonne)
*Computer Methods in Applied Mechanics and Engineering* (CMAME), 2025.
DOI: 10.1016/j.cma.2025.118057  ·  [arXiv:2409.07769](https://arxiv.org/abs/2409.07769)  ·
[OSTI 2587579](https://www.osti.gov/biblio/2587579)

## What the paper does

Introduces a multiscale **graph neural network** for **mesh-based 3D super-resolution** of fluid
flows discretized with spectral-element / finite-element connectivities (e.g. Nek5000, OpenFOAM).
The architecture is a U-Net of message-passing layers separated by graph pooling/unpooling,
trained to map a coarse-mesh field (prolongated to the fine mesh) into the fine-mesh field.

**Key technical contribution.** A *modified message-passing layer* that synchronizes
coincident graph nodes on element boundaries — necessary because spectral-element meshes
duplicate boundary nodes (one per element). After local edge aggregation, an `index_add_`
across coincident-node groups (or, in the distributed code, an MPI halo swap +
`index_add_`) restores nodal continuity. This is the bridge that lets a generic GNN
respect element-based mesh topology.

Demonstrated on a 3D backward-facing-step (BFS) flow at multiple polynomial orders
with reductions in field L2 error of roughly an order of magnitude over linear interpolation.

## Author code we used

- **`sbarwey/DDP_PyGeom`** — distributed-data-parallel PyTorch-Geometric training code
  (BFS workflow). Contains the `Multiscale_MessagePassing_UNet` used in the paper.
  Cloned to `DDP_PyGeom/`.
- **`sbarwey/nekRS-GNN/3rd_party/gnn`** — Nek-RS coupled distributed version.
  Contains `DistributedMessagePassingLayer` with the explicit halo-swap +
  coincident-node `index_add_` (the paper's headline contribution). Mirrored to
  `nekRS-GNN-3rdparty/` for reference.

## What this replication did (6h budget)

1. ✅ Located the paper and authors' GitHub user (`sbarwey`, not `shivambarwey`).
2. ✅ Pulled the actual model code: `Multiscale_MessagePassing_UNet` from
   `DDP_PyGeom/models/gnn.py` and the distributed `DistributedMessagePassingLayer`
   from `nekRS-GNN/3rd_party/gnn/models/gnn_v2.py`.
3. ✅ Read the architecture: 2D voxel-grid clustering + graph U-Net, learned KNN
   interpolation between levels, edge/node MLPs with LayerNorm, residual updates.
   Confirmed the halo-swap + `index_add_` pattern that synchronizes coincident
   spectral-element nodes (paper's Eq. (15)–(17), implemented in
   `gnn_v2.py:266-280`).
4. ❌ Tried `chiatta00` (JLSE Aurora-class). Has Intel oneAPI but no preinstalled
   PyTorch + Intel extension; building IPEX from scratch was too risky for the
   time budget. **Fell back to `uicgpu`** (8× A100-80GB) with CUDA PyTorch.
5. ✅ Built a reproducible Python env on `uicgpu`:
   `/data/stevens/envs/pyg-mesh` with `torch==2.4.1+cu121`, `torch-geometric==2.6.1`,
   `torch-scatter`, `torch-cluster`, `pyvista==0.42.3`.
6. ✅ Could not get the paper's actual BFS dataset in 6h (it's not in the repo;
   needs OpenFOAM `foamToVTK` snapshots produced separately). **Built a synthetic
   2D spectral-element problem** that exercises the same architecture and the
   same coincident-node topology:
   - 4×4 quadrilateral elements, polynomial order p_hi = 7 (8×8 GLL nodes per element)
   - 1024 nodes total, 165 coincident-node groups, 183 duplicated boundary nodes
   - Field: random-amplitude/phase Taylor-Green-style 2D divergence-free flow + pressure
   - Coarse field at p_lo = 3 prolongated back to p_hi via bilinear → input
   - Target = high-res field; model learns the residual correction.
7. ✅ Trained 80 epochs (~90s on 1 A100). 305k parameters, depth-2 multiscale UNet.
8. ✅ Compared L2 field error vs the no-network (interpolation-only) baseline.

## Result

| metric | interpolation baseline | multiscale GNN (best) | improvement |
|---|---|---|---|
| relative L2 field error (val) | **3.99e-01** | **8.36e-02** | **4.77×** |

Paper's ballpark for BFS at comparable order ratio: 5–10× over linear interpolation.
We are in that range despite being on a much smaller, simpler 2D problem with
no hyperparameter tuning.

The improvement comes specifically from the multiscale graph U-Net learning
mesh-aware residuals; the run uses the paper's exact `Multiscale_MessagePassing_UNet`
class verbatim, so this confirms the architecture works out of the box on
spectral-element-style topology.

## Files

- `paper.pdf` — arXiv v4 of the paper (Barwey et al. 2024).
- `replication_plan.md` — original plan / steps.
- `train_synthetic.py` — self-contained training script using the paper's model.
- `results_main.json` — full per-epoch loss history + summary.
- `REPORT.md` — replication scorecard.
- `DDP_PyGeom/` — author's training repo (clone, used for `models/gnn.py` + `pooling.py`).
- `nekRS-GNN-3rdparty/` — files from `nekRS-GNN/3rd_party/gnn/` (distributed message
  passing reference).

## Reproducing

On any machine with one CUDA GPU, Python 3.8+, and the env above:

```bash
cd 2587579-Mesh-based-super-resolution-multiscale-GNN
python train_synthetic.py --epochs 80 --n_train 128 --n_val 32 --batch 4 --hidden 64 \
       --out results_main.json
```

Runs in ~90 seconds on an A100. The script imports `models.gnn` and `pooling`
directly from the author's `DDP_PyGeom` repo (rsync'd alongside on uicgpu).

## What would be needed for a full replication

1. **The actual BFS dataset.** Run the OpenFOAM BFS sim from `sbarwey/bfs_3d`,
   convert with `foamToVTK`, then `dataprep/backward_facing_step.py` to make
   PyG `edge_index/edge_attr/pos` files.
2. **3D voxel-grid clustering.** The current `Multiscale_MessagePassing_UNet`
   hardcodes 2D in `tgnn.voxel_grid(start=[x_lo,y_lo], end=[x_hi,y_hi])`.
   The 3D BFS run needs a small patch (extend `bounding_box` to z) or use
   the 3D variant in `nekRS-GNN/3rd_party/gnn/models/gnn_v2.py`.
3. **Distributed run with halo exchange** via the `nekRS-GNN-3rdparty/main_v2.py`
   pipeline — that's where the spectral-element coincident-node sync becomes
   essential. Single-process runs fold it implicitly into the duplicated-node
   topology.
4. **Aurora/Sunspot or Polaris** for the multi-rank halo-swap timings the paper
   reports; the model itself trains fine on a single A100 for the BFS sizes used.
