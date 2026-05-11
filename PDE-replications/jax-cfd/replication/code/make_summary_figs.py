#!/usr/bin/env python
"""Build summary figures: re_scaling.png, decaying_turb_spectrum.png.

Combines existing Re=1000 results (results.npz) with new Re=4000 results
(results_high_re/arrays_re4000.npz) and decaying-turb results.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_RE1K = os.path.join(ROOT, 'results', 'results.npz')
RES_RE4K = os.path.join(ROOT, 'results', 'high_re', 'arrays_re4000.npz')
RES_DEC  = os.path.join(ROOT, 'results', 'decaying', 'arrays_decaying.npz')
JSON_RE4K = os.path.join(ROOT, 'results', 'high_re', 'results_re4000.json')
JSON_DEC  = os.path.join(ROOT, 'results', 'decaying', 'results_decaying.json')


def thr(corr, times, threshold=0.95):
    below = np.where(corr < threshold)[0]
    return float(times[below[0]]) if len(below) else float(times[-1])


def main():
    out_dir = os.path.join(ROOT, 'results')
    re1k = np.load(RES_RE1K)
    re4k = np.load(RES_RE4K)
    dec  = np.load(RES_DEC)

    # ---------- Re scaling: time-to-decorrelation vs effective grid ----
    # Map LI(64) and DNS64/128/256 from Re=1000, LI(128) and DNS128/256/512/1024 from Re=4000.
    # X-axis: nominal grid resolution (LI shown at its own grid).
    fig, ax = plt.subplots(figsize=(8, 5))
    # Re=1000 — pick keys present in arrays
    n_T_1k = re1k['corr_LI64'].shape[0]
    save_dt_1k = float(re1k['save_dt'])
    times_1k = np.arange(n_T_1k) * save_dt_1k
    re1k_pts = []
    for grid_, key in [(64, 'corr_DNS64'), (128, 'corr_DNS128'),
                       (256, 'corr_DNS256')]:
        if key in re1k.files:
            re1k_pts.append((grid_, thr(re1k[key], times_1k), 'DNS'))
    re1k_pts.append((64, thr(re1k['corr_LI64'], times_1k), 'LI'))

    # Re=4000
    times_4k = re4k['times']
    re4k_pts = []
    for grid_, key in [(128, 'DNS128_corr'), (256, 'DNS256_corr'),
                       (512, 'DNS512_corr'), (1024, 'DNS1024_corr')]:
        if key in re4k.files:
            re4k_pts.append((grid_, thr(re4k[key], times_4k), 'DNS'))
    re4k_pts.append((128, thr(re4k['LI_corr'], times_4k), 'LI'))

    for (pts, label, marker, color_dns, color_li) in [
        (re1k_pts, 'Re=1000', 'o', 'tab:blue', 'tab:red'),
        (re4k_pts, 'Re=4000', 's', 'tab:green', 'tab:orange')]:
        dns_pts = sorted([(g, t) for g, t, k in pts if k == 'DNS'])
        if dns_pts:
            xs = [p[0] for p in dns_pts]
            ys = [p[1] for p in dns_pts]
            ax.plot(xs, ys, marker=marker, color=color_dns, lw=2, ms=8,
                    label=f'{label} DNS (vs grid)')
        li_pts = [(g, t) for g, t, k in pts if k == 'LI']
        for g, t in li_pts:
            ax.scatter([g], [t], marker='*', s=240, color=color_li,
                       edgecolor='black', zorder=10,
                       label=f'{label} LI({g})')

    ax.set_xscale('log')
    ax.set_xlabel('DNS grid resolution (LI shown at its training grid)', fontsize=12)
    ax.set_ylabel('Time before vorticity corr < 0.95', fontsize=12)
    ax.set_title('Reynolds scaling: LI vs DNS resolution (Kolmogorov flow)',
                 fontsize=13)
    ax.grid(alpha=0.3, which='both')
    ax.legend(fontsize=9, loc='upper left')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 're_scaling.png'), dpi=150)
    plt.close()
    print('Wrote re_scaling.png')

    # ---------- Decaying turbulence spectrum ------------------
    # Plot E(k) at early time (peak) and late time
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    name_map = [('reference', 'k', 'reference (DNS-2048)', 2.5),
                ('LI', 'tab:red', 'LI(64)', 1.8),
                ('DNS64_solver', 'tab:cyan', 'DNS64 (solver)', 1.3),
                ('DNS64', 'tab:blue', 'DNS64 (dataset)', 1.3),
                ('DNS128', 'tab:green', 'DNS128 (dataset)', 1.3),
                ('DNS1024', 'tab:purple', 'DNS1024 (dataset)', 1.3)]
    # Early-time (~ frame 0-5)
    ax = axes[0]
    for key, color, label, lw in name_map:
        spk = f'{key}_spec_k'; spv = f'{key}_spec_early'
        if spk in dec.files and spv in dec.files:
            ax.loglog(dec[spk], dec[spv], color=color, lw=lw, label=label)
    # k^-3 reference slope (2D Kraichnan enstrophy cascade)
    k = np.arange(1, 32)
    ax.loglog(k, 1e-2 * k**-3.0, 'k--', alpha=0.4, label=r'$k^{-3}$ (enstrophy cascade)')
    ax.set(xlabel='k', ylabel='E(k)',
           title='Decaying turbulence: early-time energy spectrum')
    ax.legend(fontsize=8, loc='lower left'); ax.grid(alpha=0.3, which='both')
    # Late time (time-averaged)
    ax = axes[1]
    for key, color, label, lw in name_map:
        spk = f'{key}_spec_k'; spv = f'{key}_spec'
        if spk in dec.files and spv in dec.files:
            ax.loglog(dec[spk], dec[spv], color=color, lw=lw, label=label)
    ax.set(xlabel='k', ylabel='E(k)',
           title='Decaying turbulence: time-avg energy spectrum (late)')
    ax.legend(fontsize=8, loc='lower left'); ax.grid(alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'decaying_turb_spectrum.png'), dpi=150)
    plt.close()
    print('Wrote decaying_turb_spectrum.png')

    # ---------- Compose top-level JSONs --------
    with open(JSON_RE4K) as f:
        re4k_summary = json.load(f)
    with open(JSON_DEC) as f:
        dec_summary  = json.load(f)
    with open(os.path.join(ROOT, 'results_high_re.json'), 'w') as f:
        json.dump({'re_4000': re4k_summary,
                   're_7000': {'status': 'not_completed',
                               'reason': 'in-house 512^2 reference DNS '
                               'energetically unstable (max|u|>20); '
                               'training diverged. See REPORT.'}},
                  f, indent=2)
    with open(os.path.join(ROOT, 'results_decaying.json'), 'w') as f:
        json.dump(dec_summary, f, indent=2)
    print('Wrote results_high_re.json and results_decaying.json')


if __name__ == '__main__':
    main()
