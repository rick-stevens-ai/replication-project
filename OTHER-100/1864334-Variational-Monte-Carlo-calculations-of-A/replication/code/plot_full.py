"""Plot energy convergence + final energies for the full-Hamiltonian runs."""
import json, os
import numpy as np
import matplotlib.pyplot as plt

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/results'
OUT = DIR + '/figs'
os.makedirs(OUT, exist_ok=True)

systems = [('3H', -8.482), ('3He', -7.718), ('4He', -28.296)]

# ---------- (a) convergence curves ----------
fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=False)
for ax, (lab, exp) in zip(axs, systems):
    for tag, color, name in [('full','C0','V_NN+V_3N'),
                              ('no3n','C2','V_NN only')]:
        path = f'{DIR}/{tag}/full_{lab}_history.json'
        if not os.path.exists(path): continue
        h = json.load(open(path))
        ax.plot(h['iter'], h['E_clip'], color=color, lw=1.0, label=name, alpha=0.85)
    ax.axhline(exp, color='k', ls='--', lw=1, label=f'Exp {exp:.2f}')
    ax.set_title(f'{lab}'); ax.set_xlabel('iter'); ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc='lower right')
axs[0].set_ylabel('E_VMC (MeV)')
plt.tight_layout()
plt.savefig(f'{OUT}/full_convergence.png', dpi=140)
print(f'wrote {OUT}/full_convergence.png')

# ---------- (b) final energy bar chart with V_3N ablation ----------
fig, ax = plt.subplots(figsize=(7,4.2))
labels, base, full, exp = [], [], [], []
for lab, e in systems:
    labels.append(lab)
    exp.append(e)
    base.append(json.load(open(f'{DIR}/no3n/full_{lab}_summary.json'))['E_final'])
    full.append(json.load(open(f'{DIR}/full/full_{lab}_summary.json'))['E_final'])
x = np.arange(len(labels)); w=0.27
ax.bar(x-w, base, w, color='C2', label='V_NN only (Minnesota)')
ax.bar(x,   full, w, color='C0', label='V_NN + V_3N (UIX-inspired)')
ax.bar(x+w, exp,  w, color='k',  alpha=0.6, label='Experiment')
for xi,(b,f,e) in enumerate(zip(base,full,exp)):
    ax.text(xi-w, b+0.3, f'{b:.2f}', ha='center', fontsize=8)
    ax.text(xi,   f+0.3, f'{f:.2f}', ha='center', fontsize=8)
    ax.text(xi+w, e+0.3, f'{e:.2f}', ha='center', fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel('Ground-state energy (MeV)')
ax.set_title('Light-nucleus binding: ablation of 3-body force')
ax.legend(); ax.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUT}/full_ablation.png', dpi=140)
print(f'wrote {OUT}/full_ablation.png')

# ---------- (c) component breakdown for 4He ----------
fig, ax = plt.subplots(figsize=(6,4))
for tag, color, name in [('no3n','C2','V_NN only'), ('full','C0','full V_NN+V_3N')]:
    h = json.load(open(f'{DIR}/{tag}/full_4He_history.json'))
    ax.plot(h['iter'], h['T'],    color=color, lw=1.0, ls='-',  label=f'T  ({name})')
    ax.plot(h['iter'], h['V_NN'], color=color, lw=1.0, ls='--', label=f'V_NN ({name})')
    ax.plot(h['iter'], h['V_3N'], color=color, lw=1.0, ls=':',  label=f'V_3N ({name})')
ax.set_xlabel('iter'); ax.set_ylabel('Energy component (MeV)')
ax.set_title('⁴He component evolution'); ax.grid(alpha=0.3)
ax.legend(fontsize=7, ncol=2, loc='center right')
plt.tight_layout()
plt.savefig(f'{OUT}/full_components_4He.png', dpi=140)
print(f'wrote {OUT}/full_components_4He.png')
