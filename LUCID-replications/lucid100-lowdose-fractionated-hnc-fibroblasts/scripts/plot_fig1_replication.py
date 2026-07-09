#!/usr/bin/env python3
"""Replicate paper Figure 1 (LQ vs IR fits to HRS+ patient dose-response curves).
Outputs artifacts/fig1_replication.png.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent.parent
CSV = HERE / 'artifacts' / 'table1_singledose_SF.csv'
OUT = HERE / 'artifacts' / 'fig1_replication.png'


def lq_logsf(d, a, b):
    return -a * d - b * d * d


def ir_logsf(d, ar, as_, dc, b):
    return -ar * (1 + (as_ / ar - 1) * np.exp(-d / dc)) * d - b * d * d


def load_t1():
    by = {}
    with CSV.open() as f:
        for r in csv.DictReader(f):
            pid = int(r['patient_id'])
            d = by.setdefault(pid, {'doses': [], 'SF': [], 'SEM': [], 'hrs': r['hrs_status']})
            d['doses'].append(float(r['dose_Gy']))
            d['SF'].append(float(r['SF_mean']))
            d['SEM'].append(float(r['SF_sem']))
    return by


def main():
    data = load_t1()
    hrs_pids = sorted([p for p, v in data.items() if v['hrs'] == 'HRS'])
    fig, axes = plt.subplots(2, 3, figsize=(13, 8), constrained_layout=True)
    dgrid = np.linspace(0.01, 4.0, 400)
    for ax, pid in zip(axes.flat, hrs_pids):
        v = data[pid]
        d = np.array(v['doses']); sf = np.array(v['SF']); sem = np.array(v['SEM'])
        order = np.argsort(d); d, sf, sem = d[order], sf[order], sem[order]
        sigma = np.maximum(sem, 1e-3) / np.maximum(sf, 1e-3)
        popt_lq, _ = curve_fit(lq_logsf, d, np.log(sf), sigma=sigma, p0=[0.5, 0.05],
                               bounds=([0, 0], [5, 1]), maxfev=20000)
        popt_ir, _ = curve_fit(ir_logsf, d, np.log(sf), sigma=sigma,
                               p0=[popt_lq[0], 2.0, 0.3, popt_lq[1]],
                               bounds=([0, 0, 0.01, 0], [5, 50, 5, 1]), maxfev=40000)
        ax.errorbar(d, sf, yerr=sem, fmt='o', color='k', label='data', capsize=2, ms=5)
        ax.plot(dgrid, np.exp(lq_logsf(dgrid, *popt_lq)), 'k--', label='LQ fit')
        ax.plot(dgrid, np.exp(ir_logsf(dgrid, *popt_ir)), 'r-', label='IR fit')
        ax.set_yscale('log')
        ax.set_xlim(0, 4.1)
        ax.set_ylim(0.01, 1.2)
        ax.set_title(f'HFIB{pid} (HRS+)')
        ax.set_xlabel('Dose (Gy)')
        ax.set_ylabel('Surviving fraction')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=8, loc='lower left')
    fig.suptitle('Replicated Figure 1: LQ vs IR (induced-repair) fits to HRS-positive HNSCC fibroblasts\n'
                 'Source: doi:10.3390/ijms27062525 Table 1; refit using paper Eqs (1)–(2)')
    fig.savefig(OUT, dpi=140)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
