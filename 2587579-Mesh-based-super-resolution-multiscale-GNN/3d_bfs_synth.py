"""
3D BFS-style synthetic super-resolution test for Barwey et al. (CMAME 2025).

Builds a small 3D backward-facing-step inspired spectral-element mesh
(Nx x Ny x Nz hex elements at order p), an analytic flow field with shear-
layer-like structure, coarsens it (low polynomial order), prolongates back
via trilinear interp, and trains the paper's Multiscale_MessagePassing_UNet
to recover the high-res field. Reports rel-L2 vs interpolation baseline.

The author's gnn.py voxel_grid pooling has a 2D-hardcoded bounding-box
(`start=[x_lo,y_lo]`, `end=[x_hi,y_hi]`). We monkey-patch the bounding-box
attributes onto the model so we can pass 3D bounds; the underlying
`tgnn.voxel_grid` (PyTorch Geometric) accepts arbitrary-dim bounds.

Run:
  python 3d_bfs_synth.py --device cuda  --epochs 60
"""
import os, sys, time, json, argparse, math
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DDP_PyGeom'))
from models.gnn import Multiscale_MessagePassing_UNet
import torch_geometric.nn as tgnn


# ----------------- 3D mesh build ----------------------

def gll_points_1d(p):
    if p == 0:
        return np.array([0.0])
    k = np.arange(p + 1)
    return -np.cos(np.pi * k / p)


def build_3d_se_mesh(Nx, Ny, Nz, p, Lx=4.0, Ly=1.0, Lz=1.0, step_h=0.5, step_x=1.0):
    """Build a 3D backward-facing-step-style hex SE mesh.
    Domain [0,Lx] x [0,Ly] x [0,Lz]. The 'step' is at x=step_x, y<step_h: cells
    in that region are excluded (mimicking the BFS geometry where the floor
    drops). For simplicity we keep every element but tag those in the step
    region for the analytic field shaping (no actual element removal).
    Returns: pos (Nnodes,3), edge_index (2,E), elem_id, coincident dict.
    """
    pp1 = p + 1
    xi = gll_points_1d(p)
    nloc = pp1 ** 3
    dx_el = Lx / Nx
    dy_el = Ly / Ny
    dz_el = Lz / Nz

    pos_list = []
    edges = []
    coincident = {}
    elem_id = []
    elem_in_step = []
    node_offset = 0

    for ez in range(Nz):
        for ey in range(Ny):
            for ex in range(Nx):
                x0 = ex * dx_el
                y0 = ey * dy_el
                z0 = ez * dz_el
                in_step = (x0 < step_x) and ((y0 + dy_el) <= step_h)
                eid_local = ((ez * Ny) + ey) * Nx + ex
                elem_in_step.append(in_step)
                ex_pos = np.empty((nloc, 3), dtype=np.float64)
                for k in range(pp1):
                    for j in range(pp1):
                        for i in range(pp1):
                            li = (k * pp1 + j) * pp1 + i
                            xg = x0 + 0.5 * (xi[i] + 1.0) * dx_el
                            yg = y0 + 0.5 * (xi[j] + 1.0) * dy_el
                            zg = z0 + 0.5 * (xi[k] + 1.0) * dz_el
                            ex_pos[li] = (xg, yg, zg)
                            coincident.setdefault(
                                (round(xg, 6), round(yg, 6), round(zg, 6)),
                                []).append(node_offset + li)
                pos_list.append(ex_pos)
                elem_id.extend([eid_local] * nloc)
                # intra-element 6-neighbor edges (i-1/+1, j-1/+1, k-1/+1)
                for k in range(pp1):
                    for j in range(pp1):
                        for i in range(pp1):
                            li = (k * pp1 + j) * pp1 + i
                            base_id = node_offset + li
                            if i + 1 < pp1:
                                ri = (k * pp1 + j) * pp1 + (i + 1)
                                edges.append((base_id, node_offset + ri))
                                edges.append((node_offset + ri, base_id))
                            if j + 1 < pp1:
                                ri = (k * pp1 + (j + 1)) * pp1 + i
                                edges.append((base_id, node_offset + ri))
                                edges.append((node_offset + ri, base_id))
                            if k + 1 < pp1:
                                ri = ((k + 1) * pp1 + j) * pp1 + i
                                edges.append((base_id, node_offset + ri))
                                edges.append((node_offset + ri, base_id))
                node_offset += nloc

    pos = np.concatenate(pos_list, axis=0)
    edge_index = np.array(edges, dtype=np.int64).T
    elem_id = np.array(elem_id, dtype=np.int64)
    elem_in_step = np.array(elem_in_step, dtype=bool)
    return pos, edge_index, elem_id, coincident, elem_in_step


# ----------------- analytic BFS-like field ----------------------

def bfs_like_field(pos, t=0.0, kx=1.5, kz=1.5, step_h=0.5, step_x=1.0, phase=0.0,
                   Re=1.0):
    """Synthetic divergence-free-ish 3D flow with BFS-like shear:
       upstream of step (x<step_x): channel flow above y=step_h, near-zero below
       downstream: separated shear layer that decays then reattaches.
       u, v, w, p as 4 channels.
    """
    x = pos[:, 0]; y = pos[:, 1]; z = pos[:, 2]
    Lx = x.max() - x.min(); Ly = y.max() - y.min(); Lz = z.max() - z.min()
    # base streamwise
    h_eff = np.where(x < step_x, np.maximum(y - step_h, 0.0), y)
    Ly_eff = np.where(x < step_x, Ly - step_h, Ly)
    u_base = np.where(x < step_x,
                      np.where(y < step_h, 0.0,
                               6.0 * h_eff / np.maximum(Ly_eff, 1e-9) *
                               (1 - h_eff / np.maximum(Ly_eff, 1e-9))),
                      6.0 * y / Ly * (1 - y / Ly))
    # shear-layer mixing past step
    sep = np.exp(-((x - step_x - 0.5) ** 2) / 0.5) * np.tanh((y - step_h) * 5.0)
    # spanwise modulation
    span = np.cos(kz * np.pi * z / Lz + phase)
    # streamwise oscillation
    osc = np.sin(kx * np.pi * x / Lx + phase) * np.exp(-0.05 * t)
    u = u_base + 0.3 * sep * span + 0.1 * osc
    v = -0.2 * np.gradient_like(x) if False else 0.05 * np.cos(2*np.pi*x/Lx + phase) * span
    # construct an approximate divergence-correction-free pair (not exact)
    v = 0.15 * sep * np.sin(np.pi * z / Lz) - 0.08 * osc * np.cos(np.pi * y / Ly)
    w = 0.10 * np.sin(np.pi * x / Lx + phase) * np.cos(np.pi * y / Ly)
    p = -0.2 * (np.cos(2 * kx * np.pi * x / Lx + phase) +
                np.cos(2 * kz * np.pi * z / Lz)) * np.exp(-0.1 * t)
    return np.stack([u, v, w, p], axis=1).astype(np.float32)


# ----------------- 3D coarsen / prolongate ----------------------

def trilinear_resample(F_src, xi_src_x, dst_xi, dst_eta, dst_zeta, xi_src_y=None, xi_src_z=None):
    """Vectorized trilinear resample. F_src shape (nz_s, ny_s, nx_s, k).
    Sources can have different src grids per axis (default same as xi_src_x).
    """
    if xi_src_y is None: xi_src_y = xi_src_x
    if xi_src_z is None: xi_src_z = xi_src_x
    def find_brackets(dst, src):
        idx = np.searchsorted(src, dst, side='right') - 1
        idx = np.clip(idx, 0, len(src) - 2)
        a = src[idx]; b = src[idx + 1]
        t = (dst - a) / (b - a + 1e-12)
        return idx, t
    ix, tx = find_brackets(dst_xi, xi_src_x)
    iy, ty = find_brackets(dst_eta, xi_src_y)
    iz, tz = find_brackets(dst_zeta, xi_src_z)
    # vectorized 8-corner gather
    II = ix[None, None, :]   # (1,1,nx_d)
    JJ = iy[None, :, None]   # (1,ny_d,1)
    KK = iz[:, None, None]   # (nz_d,1,1)
    A = tx[None, None, :]
    B = ty[None, :, None]
    C = tz[:, None, None]
    out = 0.0
    for dk in (0, 1):
        for dj in (0, 1):
            for di in (0, 1):
                w = ((A if di else 1 - A) *
                     (B if dj else 1 - B) *
                     (C if dk else 1 - C))[..., None]
                out = out + w * F_src[KK + dk, JJ + dj, II + di]
    return out


def coarsen_3d(field, p_hi, p_lo, Nx, Ny, Nz):
    xi_hi = gll_points_1d(p_hi)
    xi_lo = gll_points_1d(p_lo)
    nloc_hi = (p_hi + 1) ** 3
    out = np.zeros_like(field)
    for ez in range(Nz):
        for ey in range(Ny):
            for ex in range(Nx):
                eid = ((ez * Ny) + ey) * Nx + ex
                base = eid * nloc_hi
                local_hi = field[base:base + nloc_hi].reshape(p_hi + 1, p_hi + 1, p_hi + 1, -1)
                lo_vals = trilinear_resample(local_hi, xi_hi, xi_lo, xi_lo, xi_lo)
                hi_back = trilinear_resample(lo_vals, xi_lo, xi_hi, xi_hi, xi_hi)
                out[base:base + nloc_hi] = hi_back.reshape(nloc_hi, -1)
    return out


# ----------------- patched model for 3D voxel-grid bounds ----------------------

def make_3d_model(in_channels_node, in_channels_edge, hidden, lengthscales, bbox3d,
                   n_mp_down=(2, 2), n_mp_up=(2, 2), n_repeat_mp_up=1):
    """Build the paper's UNet then patch its bounding-box attributes for 3D
    voxel-grid clustering."""
    model = Multiscale_MessagePassing_UNet(
        in_channels_node=in_channels_node,
        in_channels_edge=in_channels_edge,
        hidden_channels=hidden,
        n_mlp_encode=2,
        n_mlp_mp=2,
        n_mp_down=list(n_mp_down),
        n_mp_up=list(n_mp_up),
        n_repeat_mp_up=n_repeat_mp_up,
        lengthscales=list(lengthscales),
        bounding_box=[bbox3d[0], bbox3d[1], bbox3d[2], bbox3d[3]],  # placeholder 2D
        interpolation_mode='knn',
        name='msm_3d',
    )
    # Override the voxel_grid call by monkey-patching x_lo/x_hi/y_lo/y_hi to
    # carry only 2 dims; we will REPLACE the forward's voxel_grid call via a
    # method patch below.
    model._bbox3d = bbox3d  # (xlo,xhi,ylo,yhi,zlo,zhi)
    return model


def patch_voxel_grid_3d(model):
    """Replace tgnn.voxel_grid call inside model.forward with a 3D-aware one
    by monkeypatching the model's `forward`. We just re-route by patching
    tgnn.voxel_grid in the call site? Simplest: subclass and override forward.
    Since gnn.py's forward is long, we instead monkeypatch `tgnn.voxel_grid`
    used inside it via attribute on the module."""
    bbox3d = model._bbox3d
    x_lo, x_hi, y_lo, y_hi, z_lo, z_hi = bbox3d
    # gnn.py references `tgnn.voxel_grid` directly, so we cannot just override
    # on the model. We monkey-patch the module's binding for the duration of
    # the forward via a context: replace start/end at call time by making
    # x_lo/x_hi/y_lo/y_hi accept 3D lists.
    # Trick: set x_lo and x_hi to 3-tuples; the `start=[self.x_lo, self.y_lo]`
    # will become `start=[(xlo,ylo,zlo), (?,)]` -- no, that's broken.
    # Cleanest: write a custom subclass below.
    raise NotImplementedError("use Multiscale3D")


class Multiscale3D(Multiscale_MessagePassing_UNet):
    """Tiny override: replace the 2D-hardcoded voxel_grid bounds with 3D."""
    def __init__(self, *args, bbox3d=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert bbox3d is not None
        # bbox3d = (xlo, xhi, ylo, yhi, zlo, zhi)
        self.bbox3d = bbox3d

    def forward(self, x, edge_index, edge_attr, pos, batch=None):
        # mirror of parent forward but with 3D voxel_grid bounds. We re-implement
        # the minimum needed by calling parent.forward through monkeypatch on
        # tgnn.voxel_grid. Cleanest approach: monkey-patch x_lo/y_lo/x_hi/y_hi
        # to a sentinel and monkey-patch `tgnn.voxel_grid` for this call.
        from models import gnn as _gnn
        orig = _gnn.tgnn.voxel_grid
        bxlo, bxhi, bylo, byhi, bzlo, bzhi = self.bbox3d
        def vg_3d(pos, size, batch=None, start=None, end=None):
            return orig(pos=pos, size=size, batch=batch,
                         start=[bxlo, bylo, bzlo], end=[bxhi, byhi, bzhi])
        _gnn.tgnn.voxel_grid = vg_3d
        try:
            return super().forward(x, edge_index, edge_attr, pos, batch)
        finally:
            _gnn.tgnn.voxel_grid = orig


# ----------------- dataset ----------------------

def build_dataset(n, Nx, Ny, Nz, p_hi, p_lo, seed=0):
    rng = np.random.default_rng(seed)
    pos, edge_index, elem_id, coincident, elem_step = build_3d_se_mesh(Nx, Ny, Nz, p_hi)
    src = edge_index[0]; dst = edge_index[1]
    rel = pos[dst] - pos[src]
    rlen = np.linalg.norm(rel, axis=1, keepdims=True)
    edge_attr = np.concatenate([rel, rlen], axis=1).astype(np.float32)  # 4 channels
    pos_t = torch.tensor(pos, dtype=torch.float32)
    ei_t = torch.tensor(edge_index, dtype=torch.long)
    ea_t = torch.tensor(edge_attr, dtype=torch.float32)

    data = []
    for s in range(n):
        kx = float(rng.uniform(1.0, 3.0))
        kz = float(rng.uniform(1.0, 3.0))
        phase = float(rng.uniform(0, 2 * np.pi))
        t = float(rng.uniform(0, 5))
        hi = bfs_like_field(pos, t=t, kx=kx, kz=kz, phase=phase)
        lo_on_hi = coarsen_3d(hi, p_hi, p_lo, Nx, Ny, Nz)
        d = Data(
            x=torch.tensor(lo_on_hi, dtype=torch.float32),
            y=torch.tensor(hi, dtype=torch.float32),
            edge_index=ei_t,
            edge_attr=ea_t,
            pos=pos_t,
        )
        data.append(d)
    info = dict(N_nodes=pos.shape[0], N_edges=edge_index.shape[1],
                n_elements=Nx * Ny * Nz, p_hi=p_hi, p_lo=p_lo,
                Nx=Nx, Ny=Ny, Nz=Nz,
                n_coincident_groups=sum(1 for v in coincident.values() if len(v) > 1),
                n_duplicated_nodes=sum(len(v) - 1 for v in coincident.values() if len(v) > 1))
    return data, info, (pos, edge_index)


# ----------------- main ----------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Nx', type=int, default=8)
    ap.add_argument('--Ny', type=int, default=4)
    ap.add_argument('--Nz', type=int, default=4)
    ap.add_argument('--p_hi', type=int, default=5)
    ap.add_argument('--p_lo', type=int, default=2)
    ap.add_argument('--n_train', type=int, default=64)
    ap.add_argument('--n_val', type=int, default=16)
    ap.add_argument('--epochs', type=int, default=60)
    ap.add_argument('--batch', type=int, default=2)
    ap.add_argument('--hidden', type=int, default=48)
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    ap.add_argument('--out', default='results_3d.json')
    args = ap.parse_args()
    print(f"[cfg] {vars(args)}")
    device = torch.device(args.device)

    t0 = time.time()
    train_set, info, (pos_np, ei_np) = build_dataset(args.n_train, args.Nx, args.Ny, args.Nz,
                                                       args.p_hi, args.p_lo, seed=1)
    val_set, _, _ = build_dataset(args.n_val, args.Nx, args.Ny, args.Nz, args.p_hi, args.p_lo, seed=99)
    print(f"[data] built in {time.time()-t0:.1f}s. info={info}")

    # baseline (interpolation only)
    bl_num = bl_den = 0.0
    for d in val_set:
        diff = (d.x - d.y).numpy()
        bl_num += float(np.linalg.norm(diff))
        bl_den += float(np.linalg.norm(d.y.numpy()))
    rel_baseline = bl_num / max(bl_den, 1e-12)

    # build model: 3D
    Lx, Ly, Lz = 4.0, 1.0, 1.0
    hi_per_el_x = Lx / args.Nx
    hi_per_el_y = Ly / args.Ny
    hi_per_el_z = Lz / args.Nz
    # one level of coarsening (depth=2 in U-Net = 2 pool ratios)
    lengthscales = [
        max(hi_per_el_x, hi_per_el_y, hi_per_el_z) * 0.6,
        max(hi_per_el_x, hi_per_el_y, hi_per_el_z) * 1.2,
    ]
    bbox3d = (0.0, Lx, 0.0, Ly, 0.0, Lz)
    model = Multiscale3D(
        in_channels_node=4, in_channels_edge=4, hidden_channels=args.hidden,
        n_mlp_encode=2, n_mlp_mp=2,
        n_mp_down=[2, 2, 2], n_mp_up=[2, 2], n_repeat_mp_up=1,
        lengthscales=lengthscales,
        bounding_box=[0.0, Lx, 0.0, Ly],
        interpolation_mode='knn', name='msm_3d',
        bbox3d=bbox3d,
    ).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] params={n_params/1e3:.1f}k lengthscales={lengthscales}")

    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    train_loader = DataLoader(train_set, batch_size=args.batch, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=args.batch, shuffle=False)

    history = []
    best_val = float('inf')
    best_rel = float('inf')
    t_train_start = time.time()
    for epoch in range(args.epochs):
        model.train()
        tr_loss = 0.0; ntr = 0
        for batch in train_loader:
            batch = batch.to(device)
            opt.zero_grad()
            pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.pos, batch.batch)
            loss = F.mse_loss(pred, batch.y)
            loss.backward()
            opt.step()
            tr_loss += loss.item() * batch.num_graphs
            ntr += batch.num_graphs
        tr_loss /= max(ntr, 1)

        model.eval()
        v_num = v_den = 0.0; v_loss = 0.0; nv = 0
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.pos, batch.batch)
                diff = (pred - batch.y).cpu().numpy()
                y = batch.y.cpu().numpy()
                v_num += float(np.linalg.norm(diff))
                v_den += float(np.linalg.norm(y))
                v_loss += F.mse_loss(pred, batch.y).item() * batch.num_graphs
                nv += batch.num_graphs
        v_loss /= max(nv, 1)
        rel_l2 = v_num / max(v_den, 1e-12)
        history.append(dict(epoch=epoch, train_mse=tr_loss, val_mse=v_loss, val_rel_l2=rel_l2))
        if rel_l2 < best_rel:
            best_rel = rel_l2
        if epoch % 5 == 0 or epoch == args.epochs - 1:
            print(f"[ep {epoch:3d}] train_mse={tr_loss:.4e} val_mse={v_loss:.4e} "
                  f"val_rel_l2={rel_l2:.4f}  baseline={rel_baseline:.4f}")

    t_train = time.time() - t_train_start
    print(f"[done] best val rel L2 = {best_rel:.4f} | baseline = {rel_baseline:.4f} | "
          f"improvement = {rel_baseline / max(best_rel,1e-12):.2f}x | train time = {t_train:.1f}s")
    result = dict(
        cfg=vars(args), info=info, n_params=int(n_params),
        rel_baseline=rel_baseline, best_val_rel_l2=best_rel,
        improvement_factor=rel_baseline / max(best_rel, 1e-12),
        train_time_s=t_train, history=history,
    )
    with open(args.out, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"[saved] {args.out}")


if __name__ == '__main__':
    main()
