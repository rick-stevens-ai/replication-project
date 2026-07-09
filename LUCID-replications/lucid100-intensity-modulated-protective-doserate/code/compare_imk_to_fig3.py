#!/usr/bin/env python3
"""
Compare full-IMK model predictions to digitized Fig 3 data points.

Fig 3 was digitized programmatically by color-detecting symbols in the published
PNG (figures/Fig3.png from Springer Nature). Calibration:
  Panel A (AGO1522): cols 49-266 = dose 0-8 Gy; rows 30-257 = survival 1 - 1e-4 (log)
  Panel B (DU145):   cols 339-556 = dose 0-10 Gy; same y-axis

The color masks pick up both the discrete data symbols AND the model fit lines.
We therefore filter to clusters that look like symbols: size 8-30 px, and
deduplicated to one point per nominal-dose region (round to nearest 0.5 Gy).
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from imk_full import survival_IMK

ROOT = os.path.join(os.path.dirname(__file__), '..')

# Load digitized points
with open(os.path.join(ROOT, 'results', 'fig3_digitized.json')) as f:
    dig = json.load(f)


def filter_data_points(pts, min_size=8, max_size=30):
    """Keep only point-shaped clusters (rough symbol size)."""
    return [p for p in pts if min_size <= p['size'] <= max_size]

def dedupe_by_dose(pts, bin_width=0.5):
    """Group by rounded dose bin and keep median-survival point in each."""
    bins = {}
    for p in pts:
        b = round(p['dose'] / bin_width) * bin_width
        bins.setdefault(b, []).append(p)
    out = []
    for b, lst in sorted(bins.items()):
        lst.sort(key=lambda x: x['surv'])
        med = lst[len(lst)//2]
        out.append(med)
    return out


def compare(cell, panel_key):
    panel = dig[panel_key]
    print(f'\n=== {cell} (panel {panel_key}) — full IMK vs digitized Fig 3 ===')
    print(f'{"Condition":<14} {"Dose(Gy)":>10} {"S_data":>12} {"S_IMK":>12} {"S_IMK/S_data":>14} {"|log10 ratio|":>16}')

    # Color → field mapping
    color_to_field = {
        'blue_MF_inField' : 'MF_inField',
        'red_MF_outField' : 'MF_outField',
        'green_UF'        : 'UF',
    }
    summary = {}
    for color, field in color_to_field.items():
        raw = panel.get(color, [])
        # filter to plausible data points
        if color == 'red_MF_outField':
            # red model FIT curve also picks up red mask in long thin strands;
            # real data points are at lower doses (D < 0.5 Gy typical for OF)
            pts = filter_data_points(raw, min_size=10, max_size=30)
            pts = [p for p in pts if p['dose'] <= 0.6]  # OF cells received only scatter
        else:
            pts = filter_data_points(raw, min_size=8, max_size=30)
        pts = dedupe_by_dose(pts, bin_width=0.7)

        ratios = []
        for p in pts:
            D = p['dose']
            S_data = p['surv']
            if field == 'MF_outField':
                # Use D=delivered IF dose for the model; scatter dose to OF cell ~0.05 Gy typ
                S_imk, _, _ = survival_IMK(cell, 'MF_outField', D, scatter_OF=0.05)
                # but data point dose is the scatter dose D_OF; can use D as scatter directly
                # Use the OF-cell scatter dose as the cluster's x-axis position
                S_imk, _, _ = survival_IMK(cell, 'MF_outField', D, scatter_OF=D)
                # No — paper x-axis for OF cells is the SCATTER dose they actually received,
                # while IF cells received the full prescribed dose. So D_IF unknown for OF data.
                # Approximate: paper Fig 3 plots OF survival at the OF dose ~0.1-0.3 Gy,
                # with corresponding IF dose 0-10 Gy unknown per point.
                # Use D_IF = average prescribed dose for which OF was measured at this scatter level.
                # For this comparison, use D_IF=4 Gy (mid-range single-dose experiments).
                S_imk, _, _ = survival_IMK(cell, 'MF_outField', 4.0, scatter_OF=D)
            else:
                S_imk, _, _ = survival_IMK(cell, field, D)
            ratio = S_imk / S_data if S_data > 0 else float('inf')
            logr = abs(math.log10(ratio)) if ratio > 0 else float('inf')
            ratios.append(logr)
            print(f'{field:<14} {D:>10.2f} {S_data:>12.4g} {S_imk:>12.4g} {ratio:>14.3g} {logr:>16.3f}')
        if ratios:
            summary[field] = {
                'n_points': len(ratios),
                'mean_abs_log10_ratio': round(sum(ratios)/len(ratios), 3),
                'max_abs_log10_ratio' : round(max(ratios), 3),
            }
    return summary


def main():
    print('Full-IMK vs digitized Fig 3 comparison')
    print('=' * 70)
    s_ago = compare('AGO1522', 'A_AGO1522')
    s_du  = compare('DU145',   'B_DU145')

    out = {
        'AGO1522_quality': s_ago,
        'DU145_quality':   s_du,
        'notes': [
            'mean_abs_log10_ratio < 0.3 means model within ~factor of 2 of data',
            'mean_abs_log10_ratio < 0.5 means model within ~factor of 3',
            'OF (out-of-field) points are compared with assumed D_IF=4Gy because Fig3 OF points',
            ' do not carry their D_IF label; this introduces a known systematic.',
        ],
    }
    out_path = os.path.join(ROOT, 'results', 'imk_vs_fig3_comparison.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nWrote: {out_path}')


if __name__ == '__main__':
    main()
