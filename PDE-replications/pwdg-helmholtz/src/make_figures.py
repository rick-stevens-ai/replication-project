"""Generate publication-quality figures for PWDG Helmholtz replication."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os

plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

base = os.path.dirname(os.path.dirname(__file__))
results_dir = os.path.join(base, 'results')
fig_dir = os.path.join(base, 'figures')
os.makedirs(fig_dir, exist_ok=True)

with open(os.path.join(results_dir, 'full_study.json')) as f:
    data = json.load(f)


# ================================================================
# Figure 1: p-convergence for different wavenumbers
# ================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
markers = ['o', 's', '^', 'D']

for idx, k in enumerate([1.0, 2.0, 4.0, 8.0]):
    key = f'pw_k{k}'
    if key not in data:
        continue
    d = data[key]
    p = np.array(d['p'])
    L2 = np.array(d['L2'])
    DG = np.array(d['DG'])
    
    # Only plot where convergence is real (before conditioning floor)
    valid = L2 > 0
    
    ax1.semilogy(p[valid], L2[valid], f'-{markers[idx]}', color=colors[idx],
                label=f'k = {int(k)}', markersize=6, linewidth=1.5)
    ax2.semilogy(p[valid], DG[valid], f'-{markers[idx]}', color=colors[idx],
                label=f'k = {int(k)}', markersize=6, linewidth=1.5)

# Reference line: exp(-σp)
p_ref = np.linspace(3, 14, 50)
for ax, label in [(ax1, 'L² error'), (ax2, 'DG error')]:
    ref = 0.5 * np.exp(-1.4 * p_ref)
    ax.semilogy(p_ref, ref, 'k--', alpha=0.3, linewidth=1, label=r'$\sim e^{-1.4p}$')
    ax.set_xlabel('Number of plane wave directions $p$')
    ax.set_ylabel(label)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xlim(2.5, 16.5)

ax1.set_title('L² Error')
ax2.set_title('DG Skeleton Error')

fig.suptitle('PWDG $p$-Convergence — 2D Helmholtz, Unit Square (32 elements)\n'
            'Plane wave solution, Trefftz-DG least-squares formulation',
            fontsize=13, y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig1_p_convergence.png'))
plt.close()
print("Saved fig1_p_convergence.png")


# ================================================================
# Figure 2: Convergence rates
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5.5))

for idx, k in enumerate([1.0, 2.0, 4.0, 8.0]):
    key = f'pw_k{k}'
    if key not in data:
        continue
    d = data[key]
    p = np.array(d['p'])
    L2 = np.array(d['L2'])
    
    # Compute pointwise rates
    rates = []
    p_mid = []
    for i in range(len(p)-1):
        if L2[i] > 1e-14 and L2[i+1] > 1e-14 and L2[i+1] < L2[i]:
            r = -(np.log(L2[i+1]) - np.log(L2[i])) / (p[i+1] - p[i])
            rates.append(r)
            p_mid.append(0.5*(p[i]+p[i+1]))
    
    if rates:
        ax.plot(p_mid, rates, f'-{markers[idx]}', color=colors[idx],
               label=f'k = {int(k)}', markersize=6, linewidth=1.5)

ax.set_xlabel('$p$ (midpoint)')
ax.set_ylabel('Convergence rate $\\sigma$')
ax.set_title('Estimated exponential rate: $e_p \\sim C\\,e^{-\\sigma p}$')
ax.legend()
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_ylim(bottom=0)

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig2_convergence_rates.png'))
plt.close()
print("Saved fig2_convergence_rates.png")


# ================================================================
# Figure 3: Effect of mesh resolution
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5.5))

mesh_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
mesh_markers = ['o', 's', '^', 'D', 'v']

for idx, n in enumerate([2, 3, 4, 6, 8]):
    key = f'mesh_n{n}'
    if key not in data:
        continue
    d = data[key]
    p = np.array(d['p'])
    L2 = np.array(d['L2'])
    h = d['h']
    
    valid = L2 > 1e-13
    ax.semilogy(p[valid], L2[valid], f'-{mesh_markers[idx]}', 
               color=mesh_colors[idx],
               label=f'$h$ = {h:.3f} ({d["n_elements"]} elem)',
               markersize=5, linewidth=1.5)

ax.set_xlabel('Number of plane wave directions $p$')
ax.set_ylabel('L² error')
ax.set_title('Effect of mesh resolution ($k=4$, plane wave)')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig3_mesh_effect.png'))
plt.close()
print("Saved fig3_mesh_effect.png")


# ================================================================
# Figure 4: h-convergence for fixed p
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5.5))

for idx, p_val in enumerate([6, 8, 10]):
    key = f'hconv_p{p_val}'
    if key not in data:
        continue
    d = data[key]
    h = np.array(d['h'])
    L2 = np.array(d['L2'])
    
    ax.loglog(h, L2, f'-{markers[idx]}', color=colors[idx],
             label=f'$p = {p_val}$', markersize=6, linewidth=1.5)

# Reference slopes
h_ref = np.array([0.1, 0.5])
for order, style in [(2, '--'), (3, ':')]:
    ref = 0.01 * (h_ref/0.1)**order
    ax.loglog(h_ref, ref, style, color='gray', alpha=0.5, 
             label=f'$O(h^{order})$')

ax.set_xlabel('Mesh size $h$')
ax.set_ylabel('L² error')
ax.set_title('$h$-convergence ($k=4$, plane wave)')
ax.legend()
ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig4_h_convergence.png'))
plt.close()
print("Saved fig4_h_convergence.png")


# ================================================================
# Figure 5: Circular wave (Hankel function)
# ================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

for idx, k in enumerate([2.0, 4.0]):
    key = f'hankel_k{k}'
    if key not in data:
        continue
    d = data[key]
    p = np.array(d['p'])
    L2 = np.array(d['L2'])
    DG = np.array(d['DG'])
    
    valid = L2 > 0
    ax1.semilogy(p[valid], L2[valid], f'-{markers[idx]}', color=colors[idx],
                label=f'k = {int(k)}', markersize=6, linewidth=1.5)
    ax2.semilogy(p[valid], DG[valid], f'-{markers[idx]}', color=colors[idx],
                label=f'k = {int(k)}', markersize=6, linewidth=1.5)

for ax, label in [(ax1, 'L² error'), (ax2, 'DG error')]:
    ax.set_xlabel('Number of plane wave directions $p$')
    ax.set_ylabel(label)
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

ax1.set_title('L² Error')
ax2.set_title('DG Skeleton Error')

fig.suptitle('PWDG $p$-Convergence — Circular Wave (Hankel $H_0^{(1)}$)\n'
            'Source at $(-0.5, -0.5)$, unit square, 32 elements',
            fontsize=13, y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig5_hankel_convergence.png'))
plt.close()
print("Saved fig5_hankel_convergence.png")


# ================================================================
# Figure 6: Condition number growth
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5.5))

for idx, k in enumerate([1.0, 2.0, 4.0, 8.0]):
    key = f'pw_k{k}'
    if key not in data:
        continue
    d = data[key]
    p = np.array(d['p'])
    cond = np.array(d['cond'])
    
    ax.semilogy(p, cond, f'-{markers[idx]}', color=colors[idx],
               label=f'k = {int(k)}', markersize=6, linewidth=1.5)

ax.axhline(y=1e15, color='red', linestyle='--', alpha=0.5, label='Double precision limit')
ax.set_xlabel('Number of plane wave directions $p$')
ax.set_ylabel('Condition number $\\kappa(A)$')
ax.set_title('System conditioning vs $p$')
ax.legend()
ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig6_conditioning.png'))
plt.close()
print("Saved fig6_conditioning.png")


# ================================================================
# Summary figure: key result
# ================================================================
fig, ax = plt.subplots(figsize=(9, 6))

# Main result: k=4 on 32-element mesh
d = data['pw_k4.0']
p = np.array(d['p'])
L2 = np.array(d['L2'])

valid = L2 > 1e-13
ax.semilogy(p[valid], L2[valid], '-o', color='#1f77b4', 
           markersize=8, linewidth=2, label='PWDG (Trefftz-DG LS)')

# Fit exponential in convergence range
p_fit = p[valid & (p <= 14)]
L2_fit = L2[valid & (p <= 14)]
if len(p_fit) >= 3:
    c = np.polyfit(p_fit, np.log(L2_fit), 1)
    rate = -c[0]
    p_ref = np.linspace(3, 15, 50)
    ax.semilogy(p_ref, np.exp(c[1]) * np.exp(-rate * p_ref), '--',
               color='red', linewidth=1.5, alpha=0.7,
               label=f'Best fit: $e^{{-{rate:.2f}p}}$')

ax.set_xlabel('Number of plane wave directions $p$', fontsize=14)
ax.set_ylabel('Relative L² error', fontsize=14)
ax.set_title('Exponential $p$-Convergence of PWDG\n'
            '$k=4$, unit square, 32 elements, plane wave solution',
            fontsize=14)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(2.5, 15.5)

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'fig_summary.png'))
plt.close()
print("Saved fig_summary.png")

print("\nAll figures generated!")
