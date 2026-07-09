#!/usr/bin/env python3
"""Statistical smoke check on Table 3 chemopotentiation data.

Replicates paper-style claims, e.g.:
  * mean SF2 in HRS+ (0.29) vs HRS- (0.25) fibroblasts (paper Results §2.1).
  * Whether SF after LDFR 4x0.5 Gy differs significantly from SF after a single 2 Gy
    (paper Results: 'similar to that after 2 Gy').
  * Whether CPL+LDFR and PTX+LDFR enhancement is independent of HRS status
    (paper: no chemopotentiation effect of HRS).

Uses paired Wilcoxon and Mann-Whitney U; threshold p<0.05 per paper.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent.parent
T1 = HERE / 'artifacts' / 'table1_singledose_SF.csv'
T3 = HERE / 'artifacts' / 'table3_chemopotentiation.csv'


def load_t3():
    by = {}
    with T3.open() as f:
        for r in csv.DictReader(f):
            pid = int(r['patient_id'])
            d = by.setdefault(pid, {'hrs': r['hrs_status']})
            try:
                d[r['condition']] = float(r['SF_mean']) if r['SF_mean'] not in ('', None) else None
            except ValueError:
                d[r['condition']] = None
    return by


def main():
    t3 = load_t3()
    pids_hrs = [p for p, v in t3.items() if v['hrs'] == 'HRS']
    pids_non = [p for p, v in t3.items() if v['hrs'] == 'NON']
    sf2_hrs = np.array([t3[p]['2Gy'] for p in pids_hrs if t3[p].get('2Gy') is not None])
    sf2_non = np.array([t3[p]['2Gy'] for p in pids_non if t3[p].get('2Gy') is not None])
    sf4x05_hrs = np.array([t3[p]['4x0.5Gy'] for p in pids_hrs if t3[p].get('4x0.5Gy') is not None])
    sf4x05_non = np.array([t3[p]['4x0.5Gy'] for p in pids_non if t3[p].get('4x0.5Gy') is not None])
    print(f'HRS+ patients with SF2: {len(sf2_hrs)} mean={sf2_hrs.mean():.3f} (paper: 0.29)')
    print(f'HRS- patients with SF2: {len(sf2_non)} mean={sf2_non.mean():.3f} (paper: 0.25)')
    print(f'HRS+ patients with SF(4x0.5): {len(sf4x05_hrs)} mean={sf4x05_hrs.mean():.3f}')
    print(f'HRS- patients with SF(4x0.5): {len(sf4x05_non)} mean={sf4x05_non.mean():.3f}')

    # Test 1: SF2 HRS+ vs HRS- (Mann-Whitney U)
    u, p = stats.mannwhitneyu(sf2_hrs, sf2_non, alternative='two-sided')
    print(f'\nMW U-test SF2 HRS+ vs HRS-: U={u:.2f} p={p:.4f} '
          f'({ "different" if p<0.05 else "no significant difference" })')

    # Test 2: paired SF(4x0.5Gy) vs SF(2Gy) across all patients with both
    pairs = [(t3[p].get('2Gy'), t3[p].get('4x0.5Gy')) for p in t3]
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    a = np.array([x[0] for x in pairs]); b = np.array([x[1] for x in pairs])
    w, p = stats.wilcoxon(a, b)
    print(f'\nPaired Wilcoxon SF(2Gy) vs SF(4x0.5Gy), n={len(pairs)}: W={w:.2f} p={p:.4f} '
          f'(paper: "similar to that after 2 Gy")  → diff means {a.mean():.3f} vs {b.mean():.3f}')

    # Test 3: enhancement ratio by HRS status
    # Enhancement ER_CPL_LDFR = (CPL+4x0.5) / (CPL * 4x0.5) (Webb-type ratio, normalized)
    def er(p, drug, rad):
        d = t3[p]
        try:
            num = d.get(f'{drug}+{rad}'); den = d.get(drug) * d.get(rad) if d.get(drug) and d.get(rad) else None
        except TypeError:
            return None
        if num is None or den is None or den == 0:
            return None
        return num / den

    for drug in ('CPL', 'PTX'):
        for rad in ('2Gy', '4x0.5Gy'):
            er_hrs = [er(p, drug, rad) for p in pids_hrs]
            er_non = [er(p, drug, rad) for p in pids_non]
            er_hrs = np.array([x for x in er_hrs if x is not None])
            er_non = np.array([x for x in er_non if x is not None])
            if len(er_hrs) < 2 or len(er_non) < 2:
                continue
            u, p = stats.mannwhitneyu(er_hrs, er_non, alternative='two-sided')
            print(f'MW U-test ER({drug}+{rad}) HRS+ (n={len(er_hrs)}, mean={er_hrs.mean():.3f}) '
                  f'vs HRS- (n={len(er_non)}, mean={er_non.mean():.3f}): U={u:.2f} p={p:.4f}')

    print('\nPaper-consistency expectations:')
    print('  - SF2 HRS+ vs HRS- means should be ~0.29 vs ~0.25 (not necessarily significant per paper)')
    print('  - Paired test of 4x0.5 vs 2 Gy should be NOT significant (paper: similar to 2 Gy)')
    print('  - ER(CPL+rad) and ER(PTX+rad) by HRS status should be NOT significantly different '
          '(paper: HRS has no effect on chemopotentiation)')


if __name__ == '__main__':
    sys.exit(main())
