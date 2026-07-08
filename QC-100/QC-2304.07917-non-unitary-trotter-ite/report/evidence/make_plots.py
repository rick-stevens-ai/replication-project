#!/usr/bin/env python3
"""Reproduce Figures 7 & 8 of arXiv:2304.07917 side-by-side using our ITE data."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def load(path):
    with open(path) as f:
        return json.load(f)

def main():
    tim = load('ite_tim_result.json')
    hub = load('ite_hubbard_result.json')

    for name, res, out_png in [
        ('4-site TIM (J=0.5, h=0.1, PBC, dτ=0.1)', tim, 'fig7_tim.png'),
        ('2-site Hubbard (t=-0.1, U=0.1, OBC, dτ=0.1)', hub, 'fig8_hubbard.png'),
    ]:
        hist = res['history']
        E0 = res.get('E0_exact') or res.get('E0_exact_ED')
        steps = [r['step'] for r in hist]
        E    = [r['E']    for r in hist]
        dE   = [abs(r['E_minus_E0']) if 'E_minus_E0' in r else abs(r['dE']) for r in hist]
        pcum = [r['p_success_cumulative'] if 'p_success_cumulative' in r else r['p_cum'] for r in hist]

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
        # Left: <E> vs step, with exact E0 dashed
        axes[0].plot(steps, E, 'k.-', label='Trotterised PITE (statevector)')
        axes[0].axhline(E0, color='r', linestyle='--', label=f'exact E$_0$ = {E0:.5f}')
        axes[0].set_xlabel('Trotter step')
        axes[0].set_ylabel(r'$\langle E \rangle$')
        axes[0].set_title('Energy estimate')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        # Middle: |<E>-E0| vs step, log y
        axes[1].plot(steps, dE, 'k.-')
        axes[1].set_yscale('log')
        axes[1].set_xlabel('Trotter step')
        axes[1].set_ylabel(r'$|\langle E \rangle - E_0|$')
        axes[1].set_title('Convergence to ground state')
        axes[1].grid(True, alpha=0.3, which='both')
        # Right: cumulative post-selection probability vs step, log y
        axes[2].plot(steps, pcum, 'k.-')
        axes[2].set_yscale('log')
        axes[2].set_xlabel('Trotter step')
        axes[2].set_ylabel('cumulative post-selection prob')
        axes[2].set_title('Success probability')
        axes[2].grid(True, alpha=0.3, which='both')
        fig.suptitle(name)
        fig.tight_layout()
        fig.savefig(out_png, dpi=120)
        plt.close(fig)
        print(f"wrote {out_png}")

if __name__ == '__main__':
    main()
