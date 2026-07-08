"""Generate all figures for the v2 report."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/results'
FIG = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/report/figs'
os.makedirs(FIG, exist_ok=True)


def fig_ks():
    try:
        d = np.load(f'{OUT}/ks/rollout.npz')
        h = json.load(open(f'{OUT}/ks/history.json'))
        m = json.load(open(f'{OUT}/ks/metrics.json'))
    except Exception as e:
        print("KS figures skipped:", e); return

    # Training curve
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    ax[0].semilogy([x['data'] for x in h], label='data loss')
    ax[0].semilogy([x['pen'] for x in h], label='penalty', alpha=0.7)
    ax[0].set_xlabel('iteration'); ax[0].set_ylabel('loss'); ax[0].legend()
    ax[0].set_title('KS training')
    ax[1].plot([x['mu'] for x in h])
    ax[1].set_yscale('log'); ax[1].set_xlabel('iteration'); ax[1].set_ylabel(r'$\mu$')
    ax[1].set_title(r'KS penalty schedule')
    fig.tight_layout(); fig.savefig(f'{FIG}/ks_training.png', dpi=150); plt.close(fig)

    # Hovmöller: truth vs prediction (short rollout)
    pred = d['pred_short']; truth = d['truth_short']; t = d['t_short']
    n = min(len(t), len(truth), len(pred))
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True, sharey=True)
    vmax = max(abs(truth).max(), 3)
    im = axes[0].imshow(truth[:n].T, aspect='auto', origin='lower',
                        extent=[0, t[n-1], 0, 22], cmap='RdBu_r',
                        vmin=-vmax, vmax=vmax)
    axes[0].set_title('KS ground truth (ETDRK4/BDF reference)')
    axes[0].set_ylabel('x')
    axes[1].imshow(pred[:n].T, aspect='auto', origin='lower',
                   extent=[0, t[n-1], 0, 22], cmap='RdBu_r',
                   vmin=-vmax, vmax=vmax)
    axes[1].set_title('MP-NODE prediction')
    axes[1].set_ylabel('x')
    err = truth[:n] - pred[:n]
    axes[2].imshow(err.T, aspect='auto', origin='lower',
                   extent=[0, t[n-1], 0, 22], cmap='RdBu_r',
                   vmin=-vmax/2, vmax=vmax/2)
    axes[2].set_title('Difference (truth − prediction)')
    axes[2].set_xlabel('t'); axes[2].set_ylabel('x')
    fig.tight_layout()
    fig.savefig(f'{FIG}/ks_hovmoller.png', dpi=150); plt.close(fig)

    # RMSE vs time
    fig, ax = plt.subplots(figsize=(6, 3.2))
    rmse = d['rmse_t']
    u_std = m['u_std_truth']
    ax.plot(t[:len(rmse)], rmse / u_std, lw=2)
    ax.axhline(1.0, color='k', ls='--', alpha=0.5, label='NRMSE=1 (saturated)')
    ax.axhline(0.5, color='r', ls=':', alpha=0.5, label='NRMSE=0.5 (horizon)')
    ax.axvline(22, color='g', ls=':', alpha=0.5, label=r'$\tau_L$')
    ax.set_xlabel('t'); ax.set_ylabel('NRMSE'); ax.legend(fontsize=8)
    ax.set_title(f'KS forecast skill  (horizon={m["forecast_horizon_lyap"]:.2f} $\\tau_L$)')
    fig.tight_layout(); fig.savefig(f'{FIG}/ks_rmse.png', dpi=150); plt.close(fig)

    # Attractor PDF: joint PDF of u and u_x
    dx = 22.0 / truth.shape[1]
    truth_long = d['truth_long']; pred_long = d['pred_long']
    ux_t = np.gradient(truth_long, dx, axis=1)
    ux_p = np.gradient(pred_long, dx, axis=1)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].hist2d(truth_long.flatten(), ux_t.flatten(), bins=80,
                   cmap='viridis', density=True)
    axes[0].set_title('Truth: joint PDF $(u, \\partial_x u)$')
    axes[0].set_xlabel('u'); axes[0].set_ylabel(r'$u_x$')
    axes[1].hist2d(pred_long.flatten(), ux_p.flatten(), bins=80,
                   cmap='viridis', density=True,
                   range=[[truth_long.min(), truth_long.max()],
                          [ux_t.min(), ux_t.max()]])
    axes[1].set_title('MP-NODE: joint PDF $(u, \\partial_x u)$')
    axes[1].set_xlabel('u'); axes[1].set_ylabel(r'$u_x$')
    fig.tight_layout(); fig.savefig(f'{FIG}/ks_attractor.png', dpi=150); plt.close(fig)


def fig_kol():
    try:
        d = np.load(f'{OUT}/kolmogorov/rollout.npz')
        h = json.load(open(f'{OUT}/kolmogorov/history.json'))
        m = json.load(open(f'{OUT}/kolmogorov/metrics.json'))
    except Exception as e:
        print("KOL figures skipped:", e); return

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    ax[0].semilogy([x['data'] for x in h], label='data')
    ax[0].semilogy([x['pen'] for x in h], label='pen', alpha=0.7)
    ax[0].set_xlabel('it'); ax[0].set_ylabel('loss'); ax[0].legend()
    ax[0].set_title('Kolmogorov training')
    ax[1].plot(m['correlation_per_step'])
    ax[1].set_xlabel('rollout step'); ax[1].set_ylabel('correlation')
    ax[1].set_title('Corr vs DNS')
    ax[1].set_ylim([-0.2, 1.05])
    ax[1].axhline(0.5, color='r', ls=':')
    fig.tight_layout(); fig.savefig(f'{FIG}/kol_training.png', dpi=150); plt.close(fig)

    # Vorticity snapshots
    u_true = d['u_true']; u_pred = d['u_pred']
    # compute vorticity: dv/dx - du/dy
    def vort(u):
        v = u[1]; ux = u[0]
        dv_dx = np.gradient(v, axis=-1)
        du_dy = np.gradient(ux, axis=-2)
        return dv_dx - du_dy
    steps = [0, 5, 10, 20, 40]
    fig, axes = plt.subplots(2, len(steps), figsize=(2.2*len(steps), 4.5))
    for j, s in enumerate(steps):
        if s >= u_true.shape[0]: continue
        vt = vort(u_true[s]); vp = vort(u_pred[s])
        vmax = max(abs(vt).max(), abs(vp).max())
        axes[0, j].imshow(vt, cmap='RdBu_r', vmin=-vmax, vmax=vmax)
        axes[0, j].set_title(f'Truth t={s}'); axes[0, j].axis('off')
        axes[1, j].imshow(vp, cmap='RdBu_r', vmin=-vmax, vmax=vmax)
        axes[1, j].set_title(f'MP-NODE t={s}'); axes[1, j].axis('off')
    fig.tight_layout(); fig.savefig(f'{FIG}/kol_vorticity.png', dpi=150); plt.close(fig)

    # Spectrum
    kbins = d['kbins']; Ek_t = d['Ek_true']; Ek_p = d['Ek_pred']
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.loglog(kbins, Ek_t, 'k-', lw=2, label='Truth (DNS)')
    ax.loglog(kbins, Ek_p, 'r--', lw=2, label='MP-NODE')
    ax.set_xlabel(r'$|k|$'); ax.set_ylabel(r'$E(k)$')
    ax.set_title('Kolmogorov energy spectrum')
    ax.legend()
    fig.tight_layout(); fig.savefig(f'{FIG}/kol_spectrum.png', dpi=150); plt.close(fig)


def fig_era5():
    try:
        d = np.load(f'{OUT}/era5/rollout.npz')
        m = json.load(open(f'{OUT}/era5/metrics.json'))
    except Exception as e:
        print("ERA5 figures skipped:", e); return

    fig, ax = plt.subplots(figsize=(6, 3.5))
    rmse_m = d['rmse_model'].mean(axis=0)
    rmse_p = d['rmse_pers'].mean(axis=0)
    rmse_c = d['rmse_clim'].mean(axis=0)
    ax.plot(rmse_m, 'b-', label='MP-NODE')
    ax.plot(rmse_p, 'k--', label='Persistence')
    ax.plot(rmse_c, 'g-.', label='Climatology')
    ax.set_xlabel('forecast step'); ax.set_ylabel('RMSE (normalized)')
    lbl = 'ERA5 (synthetic proxy)' if not m.get('is_real_data', False) else 'ERA5'
    ax.set_title(f'{lbl} forecast skill')
    ax.legend()
    fig.tight_layout(); fig.savefig(f'{FIG}/era5_rmse.png', dpi=150); plt.close(fig)


if __name__ == '__main__':
    fig_ks(); fig_kol(); fig_era5()
    print("Figures written to", FIG)
