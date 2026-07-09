"""Build all figures from saved results."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIGDIR = '../figures'
RESDIR = '../results'
os.makedirs(FIGDIR, exist_ok=True)


def fig_landau_efield():
    with open(f'{RESDIR}/landau_results.json') as f:
        r = json.load(f)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    t = np.array(r['full']['t'])
    sE_full = np.sqrt(2.0 * np.array(r['full']['E_energy']))
    ax.semilogy(t, sE_full, 'k-', lw=2, label=f"full grid (wall {r['full']['wall_sec']:.1f}s)")

    colors = ['C1', 'C2', 'C3', 'C4']
    for c, rk in zip(colors, [2, 4, 8, 16]):
        key = f'lr_r{rk}'
        if key not in r: continue
        sE = np.sqrt(2.0 * np.array(r[key]['E_energy']))
        ax.semilogy(np.array(r[key]['t']), sE, '--', color=c,
                    label=f"DLR r={rk} ({r[key]['wall_sec']:.1f}s)")
    # analytic damping rate line
    gamma = 0.1533
    ax.semilogy(t, 0.05 * np.exp(-gamma * t), 'k:', alpha=0.5,
                label=f'analytic exp(-{gamma}t)')
    ax.set_xlabel('time t')
    ax.set_ylabel(r'$\sqrt{2 \mathcal{E}_E(t)}$  (electric field amplitude)')
    ax.set_title('Linear Landau damping: full grid vs DLR (rank r), α=0.01, k=0.5')
    ax.legend(loc='lower left', fontsize=9)
    ax.grid(True, which='both', ls=':')
    ax.set_ylim(1e-9, 1e-1)
    plt.tight_layout()
    fig.savefig(f'{FIGDIR}/landau_E_envelope.png', dpi=130)
    fig.savefig(f'{FIGDIR}/landau_E_envelope.pdf')
    print(f'wrote {FIGDIR}/landau_E_envelope.png')
    plt.close(fig)


def fig_twostream_efield():
    with open(f'{RESDIR}/twostream_results.json') as f:
        r = json.load(f)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    t = np.array(r['full']['t'])
    sE_full = np.sqrt(2.0 * np.array(r['full']['E_energy']))
    ax.semilogy(t, sE_full, 'k-', lw=2, label=f"full grid (wall {r['full']['wall_sec']:.1f}s)")

    colors = ['C1', 'C2', 'C3', 'C4']
    for c, rk in zip(colors, [4, 8, 16, 32]):
        key = f'lr_r{rk}'
        if key not in r: continue
        sE = np.sqrt(2.0 * np.array(r[key]['E_energy']))
        ax.semilogy(np.array(r[key]['t']), sE, '--', color=c,
                    label=f"DLR r={rk} ({r[key]['wall_sec']:.1f}s)")
    ax.set_xlabel('time t')
    ax.set_ylabel(r'$\sqrt{2 \mathcal{E}_E(t)}$  (electric field amplitude)')
    ax.set_title('Two-stream instability: full grid vs DLR (rank r), α=0.05, k=0.5, v₀=2.4')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, which='both', ls=':')
    plt.tight_layout()
    fig.savefig(f'{FIGDIR}/twostream_E.png', dpi=130)
    fig.savefig(f'{FIGDIR}/twostream_E.pdf')
    print(f'wrote {FIGDIR}/twostream_E.png')
    plt.close(fig)


def fig_rank_error_cost():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    # Landau
    with open(f'{RESDIR}/landau_results.json') as f:
        rL = json.load(f)
    ranks = [2, 4, 8, 16]
    errsL = [rL[f'lr_r{r}']['final_distribution_L2_error'] for r in ranks]
    wallsL = [rL[f'lr_r{r}']['wall_sec'] for r in ranks]
    axes[0].loglog(ranks, errsL, 'o-', label='DLR final ||Δf||')
    axes[0].axhline(1.2e-3, color='gray', ls=':', label='noise floor ~ truncation')
    axes[0].set_xlabel('rank r')
    axes[0].set_ylabel(r'$\|f_{\rm full}(T) - f_{\rm DLR}(T)\|_{L^2}$')
    axes[0].set_title('Landau: distribution error vs rank')
    axes[0].grid(True, which='both', ls=':')
    axes[0].legend()

    # Two-stream
    with open(f'{RESDIR}/twostream_results.json') as f:
        rT = json.load(f)
    ranks_t = [4, 8, 16, 32]
    errsT = [rT[f'lr_r{r}']['final_distribution_L2_error'] for r in ranks_t]
    wallsT = [rT[f'lr_r{r}']['wall_sec'] for r in ranks_t]
    axes[1].loglog(ranks_t, errsT, 's-', color='C3', label='DLR final ||Δf||')
    # Reference 1/r line
    axes[1].loglog(ranks_t, 0.15 / np.array(ranks_t)**2, 'k:', alpha=0.5, label=r'$\propto r^{-2}$')
    axes[1].set_xlabel('rank r')
    axes[1].set_ylabel(r'$\|f_{\rm full}(T) - f_{\rm DLR}(T)\|_{L^2}$')
    axes[1].set_title('Two-stream: distribution error vs rank')
    axes[1].grid(True, which='both', ls=':')
    axes[1].legend()

    plt.tight_layout()
    fig.savefig(f'{FIGDIR}/rank_error.png', dpi=130)
    fig.savefig(f'{FIGDIR}/rank_error.pdf')
    print(f'wrote {FIGDIR}/rank_error.png')
    plt.close(fig)


def fig_phase_space():
    f_full = np.load(f'{RESDIR}/twostream_f_final_full.npy')
    f_lr4 = np.load(f'{RESDIR}/twostream_f_final_r4.npy')
    f_lr16 = np.load(f'{RESDIR}/twostream_f_final_r16.npy')

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    extent = [0, 4*np.pi, -8, 8]
    vmin = min(f_full.min(), f_lr4.min(), f_lr16.min())
    vmax = max(f_full.max(), f_lr4.max(), f_lr16.max())
    for ax, f, t in zip(axes, [f_full, f_lr4, f_lr16],
                        ['Full grid', 'DLR r=4', 'DLR r=16']):
        im = ax.imshow(f.T, origin='lower', aspect='auto', extent=extent,
                       cmap='turbo', vmin=vmin, vmax=vmax)
        ax.set_xlabel('x')
        ax.set_ylabel('v')
        ax.set_title(f'{t}, t=40 (two-stream)')
    fig.colorbar(im, ax=axes, shrink=0.85, label='f(x,v)')
    fig.savefig(f'{FIGDIR}/twostream_phase_space.png', dpi=130, bbox_inches='tight')
    print(f'wrote {FIGDIR}/twostream_phase_space.png')
    plt.close(fig)


def fig_conservation():
    with open(f'{RESDIR}/landau_results.json') as f:
        rL = json.load(f)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    t = np.array(rL['full']['t'])
    axes[0].plot(t, np.abs(np.array(rL['full']['mass']) - rL['full']['mass'][0]),
                 'k-', label='full grid')
    for rk in [2, 4, 8, 16]:
        t_r = np.array(rL[f'lr_r{rk}']['t'])
        m_r = np.array(rL[f'lr_r{rk}']['mass'])
        axes[0].plot(t_r, np.abs(m_r - m_r[0]), '--', label=f'DLR r={rk}')
    axes[0].set_xlabel('t'); axes[0].set_ylabel('|mass(t) - mass(0)|')
    axes[0].set_yscale('log')
    axes[0].set_title('Landau: mass conservation')
    axes[0].grid(True, ls=':'); axes[0].legend(fontsize=9)

    # Total energy: KE + E_e
    e_full = np.array(rL['full']['kinetic_energy']) + np.array(rL['full']['E_energy'])
    axes[1].plot(t, np.abs(e_full - e_full[0]) / e_full[0], 'k-', label='full grid')
    for rk in [2, 4, 8, 16]:
        t_r = np.array(rL[f'lr_r{rk}']['t'])
        e_r = np.array(rL[f'lr_r{rk}']['kinetic_energy']) + np.array(rL[f'lr_r{rk}']['E_energy'])
        axes[1].plot(t_r, np.abs(e_r - e_r[0]) / e_r[0], '--', label=f'DLR r={rk}')
    axes[1].set_xlabel('t'); axes[1].set_ylabel('|E_total(t) - E(0)| / E(0)')
    axes[1].set_yscale('log')
    axes[1].set_title('Landau: relative total-energy drift')
    axes[1].grid(True, ls=':'); axes[1].legend(fontsize=9)

    plt.tight_layout()
    fig.savefig(f'{FIGDIR}/conservation.png', dpi=130)
    print(f'wrote {FIGDIR}/conservation.png')
    plt.close(fig)


if __name__ == '__main__':
    fig_landau_efield()
    fig_twostream_efield()
    fig_rank_error_cost()
    fig_phase_space()
    fig_conservation()
