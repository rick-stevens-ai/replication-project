"""
Multi-rank halo-swap validation for Barwey et al. (CMAME 2025).

Validates the paper's headline distributed-sync contribution:
    edge update -> edge aggregate -> halo-swap (across MPI ranks)
    -> local index_add over coincident-node pairs

The author's reference is nekRS-GNN-3rdparty/models/gnn_v2.py:266-313, which
operates on the *reduced* graph (one node per unique gid per rank) plus a
halo region holding partner-rank twins of boundary gids. Here we use
torch.distributed.all_to_all_single directly on a partitioned 2D
spectral-element graph.

Test:
  * Nx x Ny quadrilateral elements, polynomial order p (p+1 nodes per dir
    per element, with within-element duplicates collapsed by gid -> reduced
    SE graph).
  * Element-block partition along x (rank r owns ix in [r*Nx/W, (r+1)*Nx/W)).
  * Each rank has: owned_gids (unique reduced nodes from its elements that
    are *not* shared with a higher-rank partition's interior), and halo_gids
    (twins of its boundary gids that other ranks own).
  * Single-rank reference: full reduced graph, edge_aggregate with random
    edge features.
  * Multi-rank: each rank does local edge_aggregate on its (owned+halo) set,
    halo-swaps its halo-position partial sums to the owning rank, the owning
    rank index_add's them into its owned positions. Result on owned gids
    must equal the single-rank reference exactly (modulo FP nondeterminism).
  * Time halo cost vs compute.

Run:
  torchrun --standalone --nproc_per_node=2 multi_rank_halo_swap.py [--backend nccl|gloo]
"""
import os
import sys
import json
import time
import argparse
import numpy as np
import torch
import torch.distributed as dist
from torch_geometric.utils import coalesce, to_undirected, remove_self_loops


# ----------------------------- mesh build ---------------------------------

def gll_points_1d(p):
    if p == 0:
        return np.array([0.0])
    k = np.arange(p + 1)
    return -np.cos(np.pi * k / p)


def build_global_se_reduced(Nx, Ny, p, Lx=2.0, Ly=2.0):
    """Build the reduced SE graph: one node per unique gid (i.e., per
    physical mesh point). Returns:
      pos_red (Ngid,2), edge_index_red (2,E), elem2gids (Nx*Ny,(p+1)^2),
      elem_ix (Nx*Ny,) ix index for partitioning.
    """
    pp1 = p + 1
    xi = gll_points_1d(p)
    eta = gll_points_1d(p)
    hx = Lx / Nx
    hy = Ly / Ny

    pos_dup = []
    elem_dup_ids = []
    elem_ix = []
    nid = 0
    for iy in range(Ny):
        for ix in range(Nx):
            cx = ix * hx + 0.5 * hx
            cy = iy * hy + 0.5 * hy
            local = []
            for j in range(pp1):
                for i in range(pp1):
                    x = cx + 0.5 * hx * xi[i]
                    y = cy + 0.5 * hy * eta[j]
                    pos_dup.append([x, y])
                    local.append(nid)
                    nid += 1
            elem_dup_ids.append(local)
            elem_ix.append(ix)
    pos_dup = np.asarray(pos_dup)

    # global gid via rounded position
    key = np.round(pos_dup * 1e7).astype(np.int64)
    gid_map = {}
    gid = np.zeros(pos_dup.shape[0], dtype=np.int64)
    for i, k in enumerate(key):
        t = (int(k[0]), int(k[1]))
        if t not in gid_map:
            gid_map[t] = len(gid_map)
        gid[i] = gid_map[t]
    Ngid = int(gid.max()) + 1

    # reduced positions: average duplicates (they're at identical points anyway)
    pos_red = np.zeros((Ngid, 2))
    cnt = np.zeros(Ngid)
    for i, g in enumerate(gid):
        pos_red[g] += pos_dup[i]
        cnt[g] += 1
    pos_red /= cnt[:, None]

    # build elem2gids
    elem2gids = []
    for el in elem_dup_ids:
        elem2gids.append([int(gid[d]) for d in el])
    elem2gids = np.asarray(elem2gids)

    # reduced edges: within each element, tensor-product 4-neighbor edges,
    # mapped through gid. Each (a,b) pair is also tagged with the element id
    # that produced it, so we can deterministically assign edge ownership to
    # the rank that owns the element. After coalesce we resolve duplicate
    # (a,b) pairs (which can occur when two elements share a boundary edge
    # entirely) by keeping the lowest element id (and thus lowest rank).
    edge_pairs = []  # list of (min_a, max_a, elem_id, a_orig, b_orig)
    for el_id, el in enumerate(elem2gids):
        arr = np.asarray(el).reshape(pp1, pp1)
        for j in range(pp1):
            for i in range(pp1):
                a = int(arr[j, i])
                if i + 1 < pp1:
                    b = int(arr[j, i + 1])
                    if a != b:
                        edge_pairs.append((a, b, el_id))
                if j + 1 < pp1:
                    b = int(arr[j + 1, i])
                    if a != b:
                        edge_pairs.append((a, b, el_id))
    # symmetrize then dedupe (lowest-elem wins)
    sym = []
    for a, b, e_ in edge_pairs:
        sym.append((a, b, e_))
        sym.append((b, a, e_))
    sym.sort(key=lambda t: (t[0], t[1], t[2]))
    src_l, dst_l, eid_l = [], [], []
    last = (-1, -1)
    for a, b, e_ in sym:
        if (a, b) != last:
            src_l.append(a); dst_l.append(b); eid_l.append(e_)
            last = (a, b)
    ei = torch.tensor([src_l, dst_l], dtype=torch.long)
    eid = torch.tensor(eid_l, dtype=torch.long)

    return (
        torch.tensor(pos_red, dtype=torch.float32),
        ei,
        torch.tensor(elem2gids, dtype=torch.long),
        torch.tensor(elem_ix, dtype=torch.long),
        eid,
    )


# ------------------------- partition & halo build -------------------------

def partition_reduced(elem2gids, edge_index_red, edge_owner_rank, elem_ix, world_size, rank, Nx, Ngid):
    """Element-block partition.
    Returns local index space:
        local id 0..n_own-1: owned gids (those that 'belong' to this rank)
        local id n_own..n_own+n_halo-1: halo gids (twins owned by another rank)

    Ownership rule for boundary gids: lowest rank that touches the gid wins.
    This guarantees each gid is owned exactly once globally.
    """
    chunk = Nx // world_size

    # per-rank gid-touched set
    rank_gids = []
    for r in range(world_size):
        r_lo = r * chunk
        r_hi = r_lo + chunk
        r_elems = ((elem_ix >= r_lo) & (elem_ix < r_hi)).nonzero(as_tuple=False).flatten()
        s = set()
        for e in r_elems:
            for g in elem2gids[e].tolist():
                s.add(int(g))
        rank_gids.append(s)

    # gid -> owner = lowest rank that touches it
    owner = -np.ones(Ngid, dtype=np.int64)
    for r in range(world_size):
        for g in rank_gids[r]:
            if owner[g] < 0:
                owner[g] = r

    # owned_gids on this rank: gids in rank_gids[rank] AND owner==rank
    my_touch = rank_gids[rank]
    owned_gids = sorted([g for g in my_touch if owner[g] == rank])
    # halo_gids on this rank: gids in my_touch but owned by another rank
    halo_gids_per_other = {r: [] for r in range(world_size) if r != rank}
    for g in sorted(my_touch):
        o = int(owner[g])
        if o != rank:
            halo_gids_per_other[o].append(g)

    # local indexing: owned first, then halo concatenated by other-rank order
    n_own = len(owned_gids)
    halo_concat = []
    halo_offsets = {}
    cursor = n_own
    for r in sorted(halo_gids_per_other.keys()):
        h = halo_gids_per_other[r]
        halo_offsets[r] = (cursor, cursor + len(h))
        cursor += len(h)
        halo_concat.extend(h)
    n_halo = len(halo_concat)
    local_gids_arr = np.array(owned_gids + halo_concat, dtype=np.int64)
    g2l = -np.ones(Ngid, dtype=np.int64)
    g2l[local_gids_arr] = np.arange(local_gids_arr.size)

    # local edges: edges of reduced graph with both endpoints in local_gids
    src = edge_index_red[0].numpy()
    dst = edge_index_red[1].numpy()
    # An edge is local on this rank iff its producing element belongs to
    # this rank. Boundary-boundary edges (which appear in multiple elements,
    # potentially across ranks) are deterministically assigned to one rank by
    # build_global_se_reduced (lowest elem id during dedup).
    edge_keep = edge_owner_rank == rank
    src_loc = src[edge_keep]
    dst_loc = dst[edge_keep]
    # both endpoints MUST be local (owned ∪ halo) since the edge lives in our
    # element. Sanity check + map to local ids.
    assert (g2l[src_loc] >= 0).all() and (g2l[dst_loc] >= 0).all(), "edge endpoints not local"
    ei_local = np.stack([g2l[src_loc], g2l[dst_loc]], axis=0)
    ei_local_t = torch.from_numpy(ei_local).long()

    # mask_send / mask_recv: for each pair (rank, other_rank), exchange the
    # gids both ranks touch where one rank owns, the other has halo.
    mask_send_per_other = {}  # other_rank -> local indices (in owned region) we send
    mask_recv_per_other = {}  # other_rank -> local indices (in halo region) we recv into
    for r_other in range(world_size):
        if r_other == rank:
            continue
        # we send to r_other: all gids we own AND r_other touches
        send_gids = sorted([g for g in owned_gids if g in rank_gids[r_other]])
        send_locals = [int(g2l[g]) for g in send_gids]
        # we recv from r_other: halo_gids_per_other[r_other] in canonical sorted order
        recv_gids = sorted(halo_gids_per_other.get(r_other, []))
        recv_locals = [int(g2l[g]) for g in recv_gids]
        # canonical order: sort by global gid (already done)
        if send_locals:
            mask_send_per_other[r_other] = torch.tensor(send_locals, dtype=torch.long)
        if recv_locals:
            mask_recv_per_other[r_other] = torch.tensor(recv_locals, dtype=torch.long)

    # halo_info: pairs (own_recv_local, halo_send_local) -- 1:1 mapping
    # owner-rank receives halo-position partial sums, indexes them back into
    # owned positions. Built per-other-rank: each gid we send is paired with
    # the partner-rank's halo gid that has SAME global gid -- but on OUR rank,
    # halo_info matters when we are the OWNER receiving halo data from our own
    # halo region (after the all_to_all already deposited it there).
    # In this code, we run halo_swap to fetch *partner's local edge_agg of
    # boundary gids* into our halo block. That partner edge_agg is the
    # contribution of the partner's edges to that gid. We then index_add it
    # into our owned slot for that gid (those are the gids r_other touches and
    # we own).
    # So: idx_recv = local id of owned slot for gid g; idx_send = local id of
    # halo slot we just filled with partner's contribution to gid g.
    # halo block holds gids OTHER ranks own; so it does NOT carry partner
    # contributions to OUR owned gids. We need a *different* exchange.
    #
    # Re-think: the protocol that makes sense is:
    #   1) every rank computes ea_local on owned+halo positions.
    #   2) each rank sends, for every halo gid g (owned by rank_o, touched by
    #      us), our local ea_local at the halo slot to rank_o.
    #   3) rank_o places it into a recv buffer and index_add's into its owned
    #      slot for g.
    # i.e., we need send=halo slots, recv=owned slots, on DIFFERENT ranks.
    #
    # Reorganize masks for this protocol:
    #   send-from-halo: per other_rank r_o, for each halo gid g owned by r_o,
    #     local index in halo block.
    #   recv-into-owned: per other_rank r_o, for each owned gid g touched by
    #     r_o, local index in owned block. After recv, we index_add the recv
    #     buffer into ea[recv_locals].

    # rebuild with this correct protocol:
    send_mask = {}  # r_o -> halo-block local indices to send to r_o
    recv_mask = {}  # r_o -> owned-block local indices where we add r_o's data
    for r_o in range(world_size):
        if r_o == rank:
            continue
        # Halo gids owned by r_o:
        h_gids = sorted(halo_gids_per_other.get(r_o, []))
        if h_gids:
            send_mask[r_o] = torch.tensor([int(g2l[g]) for g in h_gids], dtype=torch.long)
        # Owned gids that r_o touches:
        recv_gids = sorted([g for g in owned_gids if g in rank_gids[r_o]])
        if recv_gids:
            recv_mask[r_o] = torch.tensor([int(g2l[g]) for g in recv_gids], dtype=torch.long)

    return dict(
        n_own=n_own,
        n_halo=n_halo,
        local_gids=torch.from_numpy(local_gids_arr).long(),
        edge_index_local=ei_local_t,
        send_mask=send_mask,
        recv_mask=recv_mask,
        owned_gids=owned_gids,
    )


# ----------------------------- ops --------------------------------------

def edge_aggregate(x, ei, e):
    """Sum-aggregate e[k] into node ei[1,k] (target). Mirrors the paper's
    edge_aggregator with reduce='sum'."""
    n = x.size(0)
    out = torch.zeros((n, e.size(1)), device=x.device, dtype=e.dtype)
    out.index_add_(0, ei[1], e)
    return out


def halo_send_add(buf, send_mask, recv_mask, world_size, device):
    """Send halo-position partial sums to owners; owners index_add into
    their owned positions.
    """
    F = buf.size(1)
    # build send tensor: concat over peers in rank order
    send_chunks = []
    send_split = []
    for r in range(world_size):
        if r in send_mask:
            send_chunks.append(buf[send_mask[r]].contiguous())
            send_split.append(int(send_mask[r].numel()))
        else:
            send_chunks.append(torch.empty((0, F), device=device, dtype=buf.dtype))
            send_split.append(0)
    recv_split = []
    for r in range(world_size):
        if r in recv_mask:
            recv_split.append(int(recv_mask[r].numel()))
        else:
            recv_split.append(0)
    send_cat = torch.cat(send_chunks, dim=0) if send_chunks else torch.empty((0, F), device=device, dtype=buf.dtype)
    recv_cat = torch.empty((sum(recv_split), F), device=device, dtype=buf.dtype)
    dist.all_to_all_single(recv_cat, send_cat, recv_split, send_split)
    # index_add into owned slots
    cursor = 0
    for r in range(world_size):
        n = recv_split[r]
        if n > 0:
            buf.index_add_(0, recv_mask[r].to(device), recv_cat[cursor:cursor + n])
            cursor += n
    return buf


# --------------------------- main rank routine --------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Nx', type=int, default=4)
    ap.add_argument('--Ny', type=int, default=4)
    ap.add_argument('--p', type=int, default=5)
    ap.add_argument('--feat', type=int, default=16)
    ap.add_argument('--iters', type=int, default=200)
    ap.add_argument('--backend', type=str, default='nccl')
    ap.add_argument('--out', type=str, default='results_multirank.json')
    args = ap.parse_args()

    rank = int(os.environ.get('RANK', '0'))
    world_size = int(os.environ.get('WORLD_SIZE', '1'))
    local_rank = int(os.environ.get('LOCAL_RANK', '0'))

    if args.backend == 'nccl':
        device = torch.device(f'cuda:{local_rank}')
        torch.cuda.set_device(device)
    else:
        device = torch.device('cpu')

    dist.init_process_group(backend=args.backend, init_method='env://')

    # global reduced mesh on every rank (deterministic)
    pos_red, edge_index_red, elem2gids, elem_ix, edge_elem_id = build_global_se_reduced(args.Nx, args.Ny, args.p)
    # edge owner rank = rank of the producing element
    chunk_g = args.Nx // world_size
    edge_owner_rank = (elem_ix[edge_elem_id] // chunk_g).numpy()
    Ngid = pos_red.size(0)
    if rank == 0:
        print(f"[global] Ngid={Ngid} Nedges={edge_index_red.size(1)} Nelems={elem2gids.size(0)}")

    F = args.feat
    torch.manual_seed(42)
    x_full = torch.randn(Ngid, F, device=device)
    e_full = torch.randn(edge_index_red.size(1), F, device=device)

    # ---- single-rank reference ----
    ei_full = edge_index_red.to(device)
    ea_ref = edge_aggregate(x_full, ei_full, e_full)

    # ---- partition ----
    part = partition_reduced(elem2gids, edge_index_red, edge_owner_rank, elem_ix, world_size, rank, args.Nx, Ngid)
    n_own = part['n_own']
    n_halo = part['n_halo']
    n_total = n_own + n_halo
    local_gids = part['local_gids'].to(device)
    ei_local = part['edge_index_local'].to(device)
    send_mask = {r: m.to(device) for r, m in part['send_mask'].items()}
    recv_mask = {r: m.to(device) for r, m in part['recv_mask'].items()}

    x_local = x_full[local_gids].clone()

    # local edges + the corresponding e_local: we need e values whose source
    # edge in the reduced graph survived our edge_keep filter.
    # Easiest correct path: rebuild edge ownership in same order as global ei,
    # then take the slice.
    edge_local_global_idx = np.where(edge_owner_rank == rank)[0]
    e_local = e_full[edge_local_global_idx]

    if rank == 0:
        print(f"[rank 0] n_own={n_own} n_halo={n_halo} n_local_edges={ei_local.size(1)} "
              f"n_send={sum(m.numel() for m in send_mask.values())} "
              f"n_recv={sum(m.numel() for m in recv_mask.values())}")

    # warmup
    for _ in range(5):
        ea = edge_aggregate(x_local, ei_local, e_local)
        if world_size > 1:
            ea = halo_send_add(ea, send_mask, recv_mask, world_size, device)

    # timed run
    if device.type == 'cuda':
        torch.cuda.synchronize()
    dist.barrier()
    t_compute = 0.0
    t_halo = 0.0
    for it in range(args.iters):
        if device.type == 'cuda':
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        ea = edge_aggregate(x_local, ei_local, e_local)
        if device.type == 'cuda':
            torch.cuda.synchronize()
        t1 = time.perf_counter()
        if world_size > 1:
            ea = halo_send_add(ea, send_mask, recv_mask, world_size, device)
        if device.type == 'cuda':
            torch.cuda.synchronize()
        t2 = time.perf_counter()
        t_compute += (t1 - t0)
        t_halo += (t2 - t1)

    # verification: ea[:n_own] should equal ea_ref at owned_gids
    owned_gids_t = torch.tensor(part['owned_gids'], dtype=torch.long, device=device)
    expected = ea_ref[owned_gids_t]
    actual = ea[:n_own]
    diff = (actual - expected).abs()
    max_abs = float(diff.max().item())
    rel = float((diff.norm() / expected.norm().clamp_min(1e-12)).item())

    max_t = torch.tensor([max_abs], device=device)
    rel_t = torch.tensor([rel], device=device)
    dist.all_reduce(max_t, op=dist.ReduceOp.MAX)
    dist.all_reduce(rel_t, op=dist.ReduceOp.MAX)

    if rank == 0:
        print(f"[verify] max|actual-expected| = {max_t.item():.3e}")
        print(f"[verify] rel L2 error        = {rel_t.item():.3e}")
        print(f"[timing] iters={args.iters} compute={t_compute*1000:.2f}ms "
              f"halo={t_halo*1000:.2f}ms (per-iter halo {t_halo/args.iters*1e6:.1f}us, "
              f"compute {t_compute/args.iters*1e6:.1f}us)")
        result = dict(
            world_size=world_size,
            backend=args.backend,
            Nx=args.Nx, Ny=args.Ny, p=args.p, feat=F,
            Ngid=Ngid,
            n_own_rank0=n_own,
            n_halo_rank0=n_halo,
            n_local_edges_rank0=int(ei_local.size(1)),
            n_send_rank0=sum(int(m.numel()) for m in send_mask.values()),
            n_recv_rank0=sum(int(m.numel()) for m in recv_mask.values()),
            iters=args.iters,
            t_compute_ms_total=t_compute * 1000,
            t_halo_ms_total=t_halo * 1000,
            t_compute_per_iter_us=t_compute / args.iters * 1e6,
            t_halo_per_iter_us=t_halo / args.iters * 1e6,
            halo_compute_ratio=t_halo / max(t_compute, 1e-9),
            verify_max_abs_err=max_t.item(),
            verify_rel_l2_err=rel_t.item(),
            verify_pass=bool(rel_t.item() < 1e-5),
        )
        with open(args.out, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"[saved] {args.out}")

    dist.barrier()
    dist.destroy_process_group()


if __name__ == '__main__':
    main()
