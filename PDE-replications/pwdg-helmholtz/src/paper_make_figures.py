"""
Generate paper-faithful figures from results/paper_*.json.

Matches the panels of Hiptmair-Moiola-Perugia 2011 §4 as closely as our LS
Trefftz-DG solver allows.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
RES = os.path.abspath(os.path.join(HERE, '..', 'results'))
FIG = os.path.abspath(os.path.join(HERE, '..', 'figures'))
os.makedirs(FIG, exist_ok=True)


def load(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)


def fig_42():
    d = load('paper_fig42_regular.json')
    rows = d['rows']
    p  = np.array([r['p'] for r in rows])
    l2 = np.array([r['L2_omega'] for r in rows])
    h1 = np.array([r['brokenH1'] for r in rows])
    jp = np.array([r['jumpL2'] for r in rows])
    pr = np.array([r['proj_L2'] for r in rows])

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, y, lab in zip(axes, [l2, h1, jp], ['$L^2$ error', 'broken $H^1$ seminorm', '$L^2$ jumps on skeleton']):
        ax.semilogy(p, y, 'o-', lw=2, label='Trefftz-DG-LS')
        if lab.startswith('$L^2$ error'):
            ax.semilogy(p, pr, 's--', lw=1.5, label='proj. $L^2$')
        ax.set_xlabel('# local plane wave basis functions $p$')
        ax.set_ylabel(lab)
        ax.set_title(lab)
        ax.grid(True, which='both', alpha=0.3)
        ax.legend()
    fig.suptitle('Paper Fig. 4.2 — Regular solution $u=J_1(\\omega r)\\cos\\theta$, $\\omega=10$, 8-tri mesh', fontsize=12)
    fig.tight_layout()
    out = os.path.join(FIG, 'paper_fig42_regular.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"saved {out}")


def fig_43_45():
    d = load('paper_fig43_45_singular.json')
    cases = d['cases']
    fig, axes = plt.subplots(3, 2, figsize=(11, 12))
    for ci, (xi_key, xilab) in enumerate(zip(['xi_0.6667', 'xi_1.5000'], ['$\\xi=2/3$', '$\\xi=3/2$'])):
        c = cases[xi_key]
        rows = c['rows']
        plp = np.array([r['p_over_log_p'] for r in rows])
        l2  = np.array([r['L2_omega'] for r in rows])
        h1  = np.array([r['brokenH1'] for r in rows])
        jp  = np.array([r['jumpL2'] for r in rows])
        pr  = np.array([r['proj_L2'] for r in rows])
        for ri, (y, ylab, yname) in enumerate([(l2, '$L^2$ error', 'L2_omega'),
                                                (h1, 'broken $H^1$ seminorm', 'brokenH1'),
                                                (jp, '$L^2$ jumps', 'jumpL2')]):
            ax = axes[ri, ci]
            ax.loglog(plp, y, 'o-', lw=2, label='Trefftz-DG-LS')
            if ri == 0:
                ax.loglog(plp, pr, 's--', lw=1.5, label='proj. $L^2$')
            slope = c.get(f'algebraic_slope_{yname}')
            if slope is not None:
                # overlay a reference line through (plp[mid], y[mid])
                mid = len(plp)//2
                yref = y[mid] * (plp/plp[mid])**slope
                ax.loglog(plp, yref, ':', color='gray', alpha=0.7,
                          label=f'fit slope {slope:.2f}')
            ax.set_xlabel('$p/\\log p$')
            ax.set_ylabel(ylab)
            ax.set_title(f'{xilab}: {ylab}')
            ax.grid(True, which='both', alpha=0.3)
            ax.legend()
    fig.suptitle('Paper Fig. 4.3-4.5 — Singular solutions, $\\omega=10$, 8-tri mesh', fontsize=12)
    fig.tight_layout()
    out = os.path.join(FIG, 'paper_fig43_45_singular.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"saved {out}")


def fig_46():
    d = load('paper_fig46_omega_sweep.json')
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    colors = plt.cm.viridis(np.linspace(0, 0.85, 5))
    # left: regular xi=1, L2 vs p
    cases = d['cases']['regular_xi_1']['rows_by_omega']
    for c, key in zip(colors, ['omega_0.25', 'omega_1.0', 'omega_4.0', 'omega_16.0', 'omega_64.0']):
        rows = cases[key]
        p = np.array([r['p'] for r in rows])
        e = np.array([r['L2_omega'] for r in rows])
        om = key.split('_')[1]
        axes[0].semilogy(p, e, 'o-', color=c, lw=1.8, label=f'$\\omega={om}$')
    axes[0].set_xlabel('$p$')
    axes[0].set_ylabel('$L^2$ error')
    axes[0].set_title('regular $\\xi=1$ (paper Fig 4.6 left)')
    axes[0].grid(True, which='both', alpha=0.3)
    axes[0].legend()

    # right: singular xi=2/3, L2 vs p/log p (loglog)
    cases = d['cases']['singular_xi_2_3']['rows_by_omega']
    for c, key in zip(colors, ['omega_0.25', 'omega_1.0', 'omega_4.0', 'omega_16.0', 'omega_64.0']):
        rows = cases[key]
        plp = np.array([r['p_over_log_p'] for r in rows])
        e = np.array([r['L2_omega'] for r in rows])
        om = key.split('_')[1]
        axes[1].loglog(plp, e, 'o-', color=c, lw=1.8, label=f'$\\omega={om}$')
    axes[1].set_xlabel('$p/\\log p$')
    axes[1].set_ylabel('$L^2$ error')
    axes[1].set_title('singular $\\xi=2/3$ (paper Fig 4.6 right)')
    axes[1].grid(True, which='both', alpha=0.3)
    axes[1].legend()
    fig.tight_layout()
    out = os.path.join(FIG, 'paper_fig46_omega_sweep.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"saved {out}")


def fig_conditioning():
    d = load('paper_conditioning.json')
    rows = [r for r in d['rows'] if 'cond_A' in r]
    p = np.array([r['p'] for r in rows])
    cn = np.array([r['cond_A'] for r in rows])
    er = np.array([r['L2_omega'] for r in rows])
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.semilogy(p, cn, 'o-', color='tab:red', lw=2, label='cond($A$)')
    ax1.set_xlabel('$p$')
    ax1.set_ylabel('condition number', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.grid(True, which='both', alpha=0.3)
    ax2 = ax1.twinx()
    ax2.semilogy(p, er, 's--', color='tab:blue', lw=2, label='$L^2$ error')
    ax2.set_ylabel('$L^2$ error', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title('Conditioning growth (paper §4 final paragraph)')
    fig.tight_layout()
    out = os.path.join(FIG, 'paper_conditioning.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"saved {out}")


if __name__ == '__main__':
    fig_42()
    fig_43_45()
    fig_46()
    fig_conditioning()
