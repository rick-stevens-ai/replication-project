"""Plot convergence & local-energy histograms for deuteron and (optionally) He-4."""
import json, os, sys, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), '..', 'results')
OUT = os.path.join(os.path.dirname(__file__), '..', 'report', 'figs')
os.makedirs(OUT, exist_ok=True)

def plot_convergence(system, target, label):
    path = os.path.join(RES, f'{system}_history.json')
    if not os.path.exists(path): return
    with open(path) as f: H = json.load(f)
    its = [h['it'] for h in H]
    E   = np.array([h['E'] for h in H])
    Ec  = np.array([h['E_clip'] for h in H])
    sd  = np.array([h['std'] for h in H])
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(its, E,  alpha=0.35, color='C0', lw=0.8, label='$\\langle E_L \\rangle$ (raw)')
    ax.plot(its, Ec, color='C0',  lw=1.4, label='$\\langle E_L \\rangle$ (clipped)')
    ax.fill_between(its, Ec-sd, Ec+sd, color='C0', alpha=0.2)
    ax.axhline(target, color='r', ls='--', lw=1, label=f'target: {target:+.3f} MeV')
    ax.set_xlabel('optimization iteration')
    ax.set_ylabel('energy  [MeV]')
    ax.set_title(f'VMC convergence: {label}')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f'{system}_convergence.pdf'))
    fig.savefig(os.path.join(OUT, f'{system}_convergence.png'), dpi=150)
    plt.close(fig)
    print('wrote', system, 'convergence')

def plot_hist(system, target, label):
    path = os.path.join(RES, f'{system}_final_EL.npy')
    if not os.path.exists(path): return
    EL = np.load(path)
    # trim 1% tails for visualisation
    lo, hi = np.quantile(EL, [0.005, 0.995])
    keep = EL[(EL>=lo)&(EL<=hi)]
    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(keep, bins=120, density=True, alpha=0.7, color='C1')
    ax.axvline(float(EL.mean()), color='C0', lw=2,
               label=f'$\\langle E_L\\rangle={EL.mean():.3f}$ MeV')
    ax.axvline(target, color='r', ls='--', lw=1.5, label=f'reference {target:+.3f}')
    ax.set_xlabel('local energy $E_L$  [MeV]')
    ax.set_ylabel('density')
    ax.set_title(f'Local-energy distribution (final eval): {label}  '
                 f'(N={EL.size})')
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f'{system}_local_energy_hist.pdf'))
    fig.savefig(os.path.join(OUT, f'{system}_local_energy_hist.png'), dpi=150)
    plt.close(fig)
    print('wrote', system, 'hist')

if __name__ == '__main__':
    plot_convergence('deuteron', -2.2246, 'Deuteron (Minnesota triplet)')
    plot_hist      ('deuteron', -2.2246, 'Deuteron')
    plot_convergence('he4',     -28.296, '$^4$He (Minnesota central, even-state avg)')
    plot_hist      ('he4',     -28.296, '$^4$He')
