"""
Render figures for replication report:
  fig_3d_loss.png : training loss + val rel-L2 vs epoch (3D BFS)
  fig_multirank.png : halo-swap timing breakdown across configs
"""
import json, glob, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))


def fig_3d_loss():
    p = os.path.join(here, 'results_3d.json')
    if not os.path.exists(p):
        print("no results_3d.json"); return
    R = json.load(open(p))
    h = R['history']
    eps = [e['epoch'] for e in h]
    tr = [e['train_mse'] for e in h]
    vl = [e['val_mse'] for e in h]
    rel = [e['val_rel_l2'] for e in h]
    base = R['rel_baseline']
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].semilogy(eps, tr, label='train MSE')
    ax[0].semilogy(eps, vl, label='val MSE')
    ax[0].set_xlabel('epoch'); ax[0].set_ylabel('MSE'); ax[0].legend(); ax[0].grid(True, alpha=0.3)
    ax[0].set_title('3D BFS-style: training curves')
    ax[1].plot(eps, rel, label='multiscale GNN val rel-L2', color='C2')
    ax[1].axhline(base, color='C3', linestyle='--', label=f'interp baseline={base:.3f}')
    ax[1].set_xlabel('epoch'); ax[1].set_ylabel('rel L2'); ax[1].legend(); ax[1].grid(True, alpha=0.3)
    ax[1].set_title('3D BFS-style: validation rel-L2 vs interp baseline')
    plt.tight_layout()
    out = os.path.join(here, 'fig_3d_loss.png')
    plt.savefig(out, dpi=140)
    print(f"[fig] {out}")


def fig_multirank():
    files = sorted(glob.glob(os.path.join(here, 'results_multirank*.json')))
    if not files:
        print("no multirank results"); return
    rows = []
    for f in files:
        R = json.load(open(f))
        rows.append((os.path.basename(f), R['world_size'], R['Ngid'],
                     R['p'], R['t_compute_per_iter_us'], R['t_halo_per_iter_us'],
                     R['halo_compute_ratio'], R['verify_rel_l2_err']))
    rows.sort(key=lambda r: (r[1], r[2]))
    labels = [f"{r[0].replace('results_multirank','')} W={r[1]} Ngid={r[2]}" for r in rows]
    comp = [r[4] for r in rows]
    halo = [r[5] for r in rows]
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(rows))
    ax.bar(x - 0.2, comp, 0.4, label='compute (us/iter)')
    ax.bar(x + 0.2, halo, 0.4, label='halo (us/iter)')
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20, ha='right', fontsize=8)
    ax.set_ylabel('per-iter time [us]'); ax.set_yscale('log'); ax.grid(True, axis='y', alpha=0.3)
    ax.legend(); ax.set_title('Multi-rank halo-swap: compute vs halo cost (gloo, CPU)')
    plt.tight_layout()
    out = os.path.join(here, 'fig_multirank.png')
    plt.savefig(out, dpi=140)
    print(f"[fig] {out}")


if __name__ == '__main__':
    fig_3d_loss()
    fig_multirank()
