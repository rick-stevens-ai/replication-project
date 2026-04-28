"""
Replication test for Barwey et al. (CMAME 2025), OSTI 2587579,
"Mesh-based Super-Resolution of Fluid Flows with Multiscale Graph Neural Networks".

Uses the paper's actual model code (Multiscale_MessagePassing_UNet) from
https://github.com/sbarwey/DDP_PyGeom (models/gnn.py).

Goal of THIS script (limited replication):
- Build a small 2D spectral-element-style mesh (Nx*Ny elements, GLL-like grid per element)
- Generate analytic high-resolution flow snapshots (Taylor-Green vortex)
- Build a low-resolution version, prolongate back to high-res via bilinear interp
- Train the multiscale GNN to map low-res-on-high-res -> high-res
- Compare L2 field error to a no-network (identity / linear interp) baseline

This tests that:
  (a) the paper's modified message-passing UNet runs and learns,
  (b) coincident-node graph topology yields a working super-resolution operator,
  (c) we recover error reductions on the same order as paper (~5-10x over interp baseline).

NOT a full replication: paper uses 3D backward-facing-step from OpenFOAM/Nek5000;
we use a 2D synthetic flow. But it exercises the same architecture and training loop.
"""
import os, sys, time, math, argparse, json
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.gnn import Multiscale_MessagePassing_UNet


# ------------------ Mesh construction ------------------

def gll_points_1d(p):
    """Return p+1 Gauss-Lobatto-Legendre-like points on [-1,1].
    Use Chebyshev-Gauss-Lobatto for simplicity (clusters near edges, like GLL)."""
    if p == 0:
        return np.array([0.0])
    k = np.arange(p + 1)
    return -np.cos(np.pi * k / p)  # in [-1, 1]


def build_se_graph(Nx, Ny, p, Lx=2.0, Ly=2.0):
    """Build a 2D spectral-element-style mesh.
    Nx*Ny quadrilateral elements, polynomial order p (so p+1 nodes per direction per element).
    Coincident nodes on element boundaries are duplicated (one per element) — this is the
    spectral-element topology the paper's modified message-passing layer addresses.
    Edges are intra-element only (tensor-product nearest neighbors).
    """
    nloc = (p + 1) * (p + 1)
    xi = gll_points_1d(p)  # [p+1]
    eta = gll_points_1d(p)

    dx_el = Lx / Nx
    dy_el = Ly / Ny

    pos_list = []
    edges = []  # (src, dst) intra-element
    elem_id = []
    node_offset = 0
    # remember coincident pairings for evaluation/baseline
    # key: (round(x,6), round(y,6)) -> list of global node indices
    coincident = {}

    for ey in range(Ny):
        for ex in range(Nx):
            x0 = ex * dx_el
            y0 = ey * dy_el
            # element-local coordinates -> global
            ex_pos = np.empty((nloc, 2), dtype=np.float64)
            for j in range(p + 1):
                for i in range(p + 1):
                    li = j * (p + 1) + i
                    xg = x0 + 0.5 * (xi[i] + 1.0) * dx_el
                    yg = y0 + 0.5 * (eta[j] + 1.0) * dy_el
                    ex_pos[li] = (xg, yg)
                    coincident.setdefault((round(xg, 6), round(yg, 6)), []).append(node_offset + li)
            pos_list.append(ex_pos)
            elem_id.extend([ey * Nx + ex] * nloc)

            # intra-element tensor-product edges (4-neighbor)
            for j in range(p + 1):
                for i in range(p + 1):
                    li = j * (p + 1) + i
                    if i + 1 <= p:
                        ri = j * (p + 1) + (i + 1)
                        edges.append((node_offset + li, node_offset + ri))
                        edges.append((node_offset + ri, node_offset + li))
                    if j + 1 <= p:
                        ri = (j + 1) * (p + 1) + i
                        edges.append((node_offset + li, node_offset + ri))
                        edges.append((node_offset + ri, node_offset + li))
            node_offset += nloc

    pos = np.concatenate(pos_list, axis=0)
    edge_index = np.array(edges, dtype=np.int64).T  # [2, E]
    elem_id = np.array(elem_id, dtype=np.int64)
    return pos, edge_index, elem_id, coincident


def taylor_green(pos, t=0.0, k=2.0):
    """Analytic 2D divergence-free Taylor-Green flow on [0,Lx]x[0,Ly]."""
    x = pos[:, 0]
    y = pos[:, 1]
    u = np.sin(k * np.pi * x) * np.cos(k * np.pi * y) * np.exp(-0.05 * t)
    v = -np.cos(k * np.pi * x) * np.sin(k * np.pi * y) * np.exp(-0.05 * t)
    p = -0.25 * (np.cos(2 * k * np.pi * x) + np.cos(2 * k * np.pi * y)) * np.exp(-0.1 * t)
    return np.stack([u, v, p], axis=1)


def coarsen_field(pos, field, coincident, p_hi, p_lo, Nx, Ny, Lx, Ly):
    """Project the high-res field to a coarser polynomial order (p_lo) per element by
    sampling at coarse GLL nodes via bilinear interp from the high-res nodes,
    then prolongating back to high-res nodes (also bilinear).
    Returns prolongated field on the high-res mesh."""
    # Build coarse-element nodes per element
    xi_lo = gll_points_1d(p_lo)
    xi_hi = gll_points_1d(p_hi)
    nloc_hi = (p_hi + 1) ** 2
    nloc_lo = (p_lo + 1) ** 2
    out = np.zeros_like(field)

    # 1D interpolation matrix from hi to lo (Lagrange via sampled values)
    # We'll use simple linear interp through the high-res tensor grid
    # Since hi grid is denser, sampling lo points by bilinear is good enough for our test.
    dx_el = Lx / Nx
    dy_el = Ly / Ny
    # Build per-element index grids on hi
    hi_grid_idx = np.arange(nloc_hi).reshape(p_hi + 1, p_hi + 1)

    for ey in range(Ny):
        for ex in range(Nx):
            eid = ey * Nx + ex
            base = eid * nloc_hi
            local_hi = field[base: base + nloc_hi].reshape(p_hi + 1, p_hi + 1, -1)  # [py,px,F]
            # bilinear interp from xi_hi grid to xi_lo grid -> [p_lo+1, p_lo+1, F]
            lo_vals = bilinear_resample(local_hi, xi_hi, xi_hi, xi_lo, xi_lo)
            # prolongate back to xi_hi
            hi_back = bilinear_resample(lo_vals, xi_lo, xi_lo, xi_hi, xi_hi)
            out[base: base + nloc_hi] = hi_back.reshape(nloc_hi, -1)
    return out


def bilinear_resample(F_src, xi_src, eta_src, xi_dst, eta_dst):
    """Bilinear interpolate a tensor F_src[ny, nx, k] at source xi/eta coords onto
    destination xi/eta coords."""
    ny_s, nx_s, k = F_src.shape
    ny_d, nx_d = len(eta_dst), len(xi_dst)
    out = np.zeros((ny_d, nx_d, k))
    # for each dest col, find bracketing src cols
    def find_brackets(dst, src):
        idx = np.searchsorted(src, dst, side='right') - 1
        idx = np.clip(idx, 0, len(src) - 2)
        a = src[idx]
        b = src[idx + 1]
        t = (dst - a) / (b - a + 1e-12)
        return idx, t
    ix, tx = find_brackets(xi_dst, xi_src)
    iy, ty = find_brackets(eta_dst, eta_src)
    for j in range(ny_d):
        for i in range(nx_d):
            f00 = F_src[iy[j], ix[i]]
            f10 = F_src[iy[j], ix[i] + 1]
            f01 = F_src[iy[j] + 1, ix[i]]
            f11 = F_src[iy[j] + 1, ix[i] + 1]
            out[j, i] = (1 - tx[i]) * (1 - ty[j]) * f00 + tx[i] * (1 - ty[j]) * f10 \
                       + (1 - tx[i]) * ty[j] * f01 + tx[i] * ty[j] * f11
    return out


# ------------------ Dataset ------------------

def make_dataset(n_snapshots, Nx, Ny, p_hi, p_lo, Lx=2.0, Ly=2.0, k_range=(1.5, 3.5), seed=0):
    rng = np.random.default_rng(seed)
    pos_np, edge_index_np, elem_id, coincident = build_se_graph(Nx, Ny, p_hi, Lx, Ly)
    # edge_attr: relative position (paper-style)
    src = edge_index_np[0]
    dst = edge_index_np[1]
    edge_attr_np = pos_np[dst] - pos_np[src]
    # also distance ||r||
    edge_len = np.linalg.norm(edge_attr_np, axis=1, keepdims=True)
    edge_attr_full = np.concatenate([edge_attr_np, edge_len], axis=1)

    pos_t = torch.tensor(pos_np, dtype=torch.float32)
    edge_index_t = torch.tensor(edge_index_np, dtype=torch.long)
    edge_attr_t = torch.tensor(edge_attr_full, dtype=torch.float32)

    data_list = []
    for s in range(n_snapshots):
        kx = float(rng.uniform(*k_range))
        t = float(rng.uniform(0, 5))
        phase = float(rng.uniform(0, 2 * np.pi))
        # random rotation of base TG
        x = pos_np[:, 0]
        y = pos_np[:, 1]
        u = np.sin(kx * np.pi * x + phase) * np.cos(kx * np.pi * y) * np.exp(-0.05 * t)
        v = -np.cos(kx * np.pi * x + phase) * np.sin(kx * np.pi * y) * np.exp(-0.05 * t)
        p = -0.25 * (np.cos(2 * kx * np.pi * x + 2 * phase) + np.cos(2 * kx * np.pi * y)) * np.exp(-0.1 * t)
        hi = np.stack([u, v, p], axis=1).astype(np.float32)
        lo_on_hi = coarsen_field(pos_np, hi, coincident, p_hi, p_lo, Nx, Ny, Lx, Ly).astype(np.float32)
        d = Data(
            x=torch.tensor(lo_on_hi),
            y=torch.tensor(hi),
            edge_index=edge_index_t,
            edge_attr=edge_attr_t,
            pos=pos_t,
        )
        data_list.append(d)
    info = dict(N_nodes=pos_np.shape[0], N_edges=edge_index_np.shape[1],
                n_elements=Nx * Ny, p_hi=p_hi, p_lo=p_lo, Lx=Lx, Ly=Ly,
                n_coincident_groups=sum(1 for v in coincident.values() if len(v) > 1),
                n_duplicated_nodes=sum(len(v) - 1 for v in coincident.values() if len(v) > 1))
    return data_list, info


# ------------------ Training ------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Nx', type=int, default=4)
    ap.add_argument('--Ny', type=int, default=4)
    ap.add_argument('--p_hi', type=int, default=7)
    ap.add_argument('--p_lo', type=int, default=3)
    ap.add_argument('--Lx', type=float, default=2.0)
    ap.add_argument('--Ly', type=float, default=2.0)
    ap.add_argument('--n_train', type=int, default=128)
    ap.add_argument('--n_val', type=int, default=32)
    ap.add_argument('--epochs', type=int, default=60)
    ap.add_argument('--batch', type=int, default=4)
    ap.add_argument('--hidden', type=int, default=64)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    ap.add_argument('--out', default='results.json')
    args = ap.parse_args()

    print(f"[cfg] {vars(args)}")
    t0 = time.time()
    train_set, info = make_dataset(args.n_train, args.Nx, args.Ny, args.p_hi, args.p_lo,
                                   args.Lx, args.Ly, seed=1)
    val_set, _ = make_dataset(args.n_val, args.Nx, args.Ny, args.p_hi, args.p_lo,
                              args.Lx, args.Ly, seed=99)
    print(f"[data] built in {time.time()-t0:.1f}s. info={info}")

    device = torch.device(args.device)

    # baseline error: identity (= prolongated low-res = network input)
    bl_num, bl_den = 0.0, 0.0
    for d in val_set:
        e = (d.x - d.y).pow(2).sum().item()
        n = d.y.pow(2).sum().item()
        bl_num += e; bl_den += n
    baseline_l2_rel = math.sqrt(bl_num / bl_den)
    print(f"[baseline] interp-only val rel-L2 = {baseline_l2_rel:.4e}")

    # bounding box for the multiscale UNet voxel grid (2D model)
    bb = [0.0, args.Lx, 0.0, args.Ly]

    # depth=2 multiscale UNet, with two coarsening lengthscales
    el_size = args.Lx / args.Nx
    lengthscales = [0.6 * el_size, 1.2 * el_size]  # finer-than-element, then coarser
    n_mp_down = [2, 2, 2]  # depth+1 entries
    n_mp_up = [2, 2]
    model = Multiscale_MessagePassing_UNet(
        in_channels_node=3,
        in_channels_edge=3,  # dx, dy, |r|
        hidden_channels=args.hidden,
        n_mlp_encode=2,
        n_mlp_mp=2,
        n_mp_down=n_mp_down,
        n_mp_up=n_mp_up,
        n_repeat_mp_up=1,
        lengthscales=lengthscales,
        bounding_box=bb,
        interpolation_mode='knn',
        name='msr_unet',
    ).to(device)
    n_params = sum(pp.numel() for pp in model.parameters())
    print(f"[model] params={n_params:,}")

    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    train_loader = DataLoader(train_set, batch_size=args.batch, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=args.batch, shuffle=False)

    history = []
    best_val = float('inf')
    for ep in range(1, args.epochs + 1):
        model.train()
        tr = 0.0; nb = 0
        te0 = time.time()
        for batch in train_loader:
            batch = batch.to(device)
            opt.zero_grad()
            # paper's UNet outputs CORRECTION delta to be added to input
            # (model returns same node count as input)
            pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.pos, batch.batch)
            # target the residual y - x (so identity is zero correction)
            target = batch.y - batch.x
            loss = F.mse_loss(pred, target)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tr += loss.item(); nb += 1
        sched.step()
        tr /= max(nb, 1)

        # val
        model.eval()
        num = 0.0; den = 0.0
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.pos, batch.batch)
                yhat = batch.x + pred
                num += (yhat - batch.y).pow(2).sum().item()
                den += batch.y.pow(2).sum().item()
        val_rel_l2 = math.sqrt(num / den)
        if val_rel_l2 < best_val:
            best_val = val_rel_l2
        history.append((ep, tr, val_rel_l2))
        print(f"[ep {ep:3d}] train_mse={tr:.4e}  val_rel_l2={val_rel_l2:.4e}  "
              f"baseline={baseline_l2_rel:.4e}  best={best_val:.4e}  "
              f"({time.time()-te0:.1f}s)")

    result = dict(
        config=vars(args),
        info=info,
        n_params=n_params,
        baseline_rel_l2=baseline_l2_rel,
        best_val_rel_l2=best_val,
        improvement_factor=baseline_l2_rel / max(best_val, 1e-12),
        history=history,
    )
    with open(args.out, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n[done] best val rel-L2 = {best_val:.4e}, baseline = {baseline_l2_rel:.4e}, "
          f"improvement = {result['improvement_factor']:.2f}x")
    print(f"[done] saved {args.out}")


if __name__ == '__main__':
    main()
