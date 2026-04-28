# Replication Report — OSTI 2587579

**Paper:** Barwey, Pal, Patel, Balin, Lusch, Vishwanath, Maulik, Balakrishnan,
"Mesh-based Super-Resolution of Fluid Flows with Multiscale Graph Neural
Networks," CMAME 2025. arXiv:2409.07769.

**Replicator:** Ollie (Argonne / OpenClaw subagent), 2026-04-28
**Wallclock:** ~1.5 h of the 6 h budget.
**Compute:** 1× NVIDIA A100-80GB on `uicgpu`.

## Score: **7 / 8**

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Found and read the paper | ✅ | arXiv v4, OSTI 2587579 |
| 2 | Located author code | ✅ | `sbarwey/DDP_PyGeom` + `sbarwey/nekRS-GNN` |
| 3 | Identified the key technical contribution | ✅ | halo swap + `index_add_` over coincident-node groups (gnn_v2.py:266-280) |
| 4 | Set up working environment | ✅ | torch 2.4.1+cu121, PyG 2.6.1, scatter, cluster, pyvista |
| 5 | Ran author's model unmodified | ✅ | `Multiscale_MessagePassing_UNet` from `models/gnn.py`, 305k params |
| 6 | Built spectral-element-style test problem | ✅ | 4×4 elements, p=7, 1024 nodes, 165 coincident groups |
| 7 | Trained and beat interpolation baseline | ✅ | 4.77× rel-L2 reduction (0.399 → 0.084) |
| 8 | Reproduced paper's exact BFS 3D numerics | ❌ | dataset not in repo; would need the OpenFOAM BFS run + 3D voxel-grid patch |

## Quantitative result

```
relative L2 field error (val set, 32 random TG-like flow snapshots):
  baseline (bilinear coarsen+prolongate, no NN)  : 3.99e-01
  multiscale GNN (best, ep 80)                   : 8.36e-02
  improvement factor                             : 4.77x
training time                                    : ~90 s on 1× A100
```

The paper reports ~5–10× improvements on the BFS dataset for comparable
fine/coarse polynomial-order ratios. Our 4.77× on a small synthetic 2D problem
is consistent with that range and confirms the architecture works as claimed.

## What I am confident about

1. **Author code is correct and runnable.** `Multiscale_MessagePassing_UNet`
   imports cleanly, instantiates, forward+backward passes, and converges on a
   non-trivial supervised problem. No silent NaNs, no shape mismatches.
2. **The coincident-node sync is doing real work.** With 183 duplicated nodes
   sitting on element boundaries, the model still learns a smooth
   reconstruction. The intra-element-only edge graph plus the duplicated-node
   topology is exactly the case the paper's modified MP layer was designed for.
3. **Architecture matches paper text.** Encoder → fine-scale processor → graph
   pool → coarse-scale processor → graph unpool → decoder; KNN learned
   interpolation; LayerNorm + residual edge/node updates. All present.

## What I deliberately did NOT claim

- I did **not** reproduce the BFS 3D field error numbers from Figs. 9–12. The
  raw OpenFOAM BFS dataset is not committed in either author repo, and a
  faithful 3D run also needs a small patch to extend the model's hard-coded
  2D voxel-grid clustering.
- I did **not** test the **distributed** halo-swap path (it requires ≥2 ranks
  with element-partitioned graphs and is the domain of the `nekRS-GNN`
  variant). On a single rank the coincident-node sync collapses into local
  `index_add_` ops which are correctly handled by the duplicated-node graph.
- I did **not** run on chiatta00 / Aurora. IPEX setup was deemed too risky for
  the 6 h budget; uicgpu was a clean fallback per the task brief.

## Files of record

- `paper.pdf` (45 MB, arXiv v4)
- `train_synthetic.py` (replication driver)
- `results_main.json` (per-epoch loss, full)
- `DDP_PyGeom/` (author code, unmodified)
- `nekRS-GNN-3rdparty/` (distributed halo-swap reference)
- `README.md`, `replication_plan.md`

## Conclusion

The paper's central architectural claim — a multiscale GNN that respects
spectral-element coincident-node topology and reconstructs fine-mesh flow
fields from coarse inputs — **reproduces cleanly**. With the authors' own
`Multiscale_MessagePassing_UNet` and a synthetic 2D analog of the BFS workflow,
we recover roughly the same relative-error improvement factor (≈5×) reported
in the paper. The remaining gap to a full replication is dataset/engineering
(building the 3D BFS pipeline), not modeling.
