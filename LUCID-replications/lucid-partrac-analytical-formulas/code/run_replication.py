#!/usr/bin/env python3
from pathlib import Path
import json, math, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import matplotlib.pyplot as plt
from parameters import PARAMS, ION_ORDER
from formulas import sb_ssb_yield, dsb_yield

ROOT = Path(__file__).resolve().parents[1]
( ROOT/'results').mkdir(exist_ok=True)
( ROOT/'figures').mkdir(exist_ok=True)
LET = np.logspace(np.log10(0.5), np.log10(500), 300)

def f(dc, eff, ion, let=LET):
    params = PARAMS[dc][eff][ion]
    return (sb_ssb_yield if dc in ('SB','SSB') else dsb_yield)(let, *params)

summary = {'paper':'Kundrat et al. 2020 Scientific Reports 10:15775','doi':'10.1038/s41598-020-72857-z','task_doi_mismatch':'10.3390/cancers11020205 points to a different Cancers review','checks':{}}
# checks from prose
checks=[]
# low LET values at 0.5
for dc, expected in [('SB',170),('SSB',156),('DSB',6.8),('DSB_clusters',0.07),('DSB_sites',6.8)]:
    val=float(f(dc,'total','H',np.array([0.5]))[0])
    checks.append({'claim':f'{dc} total low-LET p1 baseline', 'computed_at_LET_0.5':val, 'expected_approx':expected, 'rel_error_vs_p1':abs(val-expected)/expected if expected else None})
# direct/indirect low LET
for dc, expected_direct, expected_indirect in [('SB',64,106),('SSB',60,102),('DSB',2.8,2.2),('DSB_clusters',0.018,0.004),('DSB_sites',2.8,2.2)]:
    checks.append({'claim':f'{dc} direct low-LET p1 baseline','computed_at_LET_0.5':float(f(dc,'direct','H',np.array([0.5]))[0]),'expected_approx':expected_direct})
    checks.append({'claim':f'{dc} indirect low-LET p1 baseline','computed_at_LET_0.5':float(f(dc,'indirect','H',np.array([0.5]))[0]),'expected_approx':expected_indirect})
# DSB sites peak 100-200, approx 15
peaks=[]
for ion in ION_ORDER:
    y=f('DSB_sites','total',ion)
    i=int(np.nanargmax(y))
    peaks.append({'ion':ion,'peak_LET':float(LET[i]),'peak_yield':float(y[i]),'low_LET_yield':float(y[0]),'RBE_peak_vs_lowLET_H':float(y[i]/f('DSB_sites','total','H',np.array([0.5]))[0])})
summary['checks']['low_let_and_headline'] = checks
summary['checks']['dsb_site_peaks'] = peaks
summary['aggregate'] = {
    'DSB_sites_peak_range': [min(p['peak_yield'] for p in peaks), max(p['peak_yield'] for p in peaks)],
    'DSB_sites_peak_LET_range': [min(p['peak_LET'] for p in peaks), max(p['peak_LET'] for p in peaks)],
    'H_DSB_yield_LET_0p5': float(f('DSB','total','H',np.array([0.5]))[0]),
    'H_DSB_yield_LET_50': float(f('DSB','total','H',np.array([50]))[0]),
    'H_DSB_sites_peak': next(p for p in peaks if p['ion']=='H'),
}
(ROOT/'results'/'summary.json').write_text(json.dumps(summary, indent=2))
# CSV grid for selected classes total/direct/indirect
import csv
with (ROOT/'results'/'yield_grid.csv').open('w', newline='') as out:
    w=csv.writer(out)
    w.writerow(['LET_keV_um','damage_class','effect','ion','yield_Gy_inv_Gbp_inv'])
    for let in np.logspace(np.log10(0.5), np.log10(500), 80):
        for dc in ['SB','SSB','DSB','DSB_clusters','DSB_sites']:
            for eff in ['total','direct','indirect']:
                for ion in ION_ORDER:
                    w.writerow([let, dc, eff, ion, float(f(dc,eff,ion,np.array([let]))[0])])
# raw excerpts
src=(ROOT/'source-paper.md').read_text(errors='ignore')
ex=[]
for marker in ['The simulated LET-dependent yields of SB and SSB','The simulated LET-dependent yields of DSB','The low-LET yields','The fits reproduced','The effectiveness in the induction of DSB sites peaks']:
    idx=src.find(marker)
    if idx>=0: ex.append(src[max(0,idx-500):idx+1500])
(ROOT/'results'/'table_excerpts.txt').write_text('\n\n--- EXCERPT ---\n\n'.join(ex))
# figures
def plot_class(dc, fname, title):
    fig, ax = plt.subplots(figsize=(8,5))
    for ion in ION_ORDER:
        ax.plot(LET, f(dc,'total',ion), label=ion)
    ax.set_xscale('log'); ax.set_xlabel('LET (keV/µm)'); ax.set_ylabel('Yield (Gy$^{-1}$ Gbp$^{-1}$)'); ax.set_title(title); ax.grid(True, alpha=.3); ax.legend(ncol=3, fontsize=8)
    fig.tight_layout(); fig.savefig(ROOT/'figures'/fname, dpi=180); plt.close(fig)
plot_class('SB','fig1_sb_total_yields.png','Eq. 1 reproduction: total strand breaks')
plot_class('DSB','fig2_dsb_total_yields.png','Eq. 2 reproduction: total double-strand breaks')
plot_class('DSB_sites','fig3_dsb_sites_total_yields.png','Eq. 2 reproduction: total DSB sites / RBE-like peak')
# direct indirect total for H/C/Ne DSB sites
fig, ax = plt.subplots(figsize=(8,5))
for ion in ['H','C','Ne']:
    for eff,ls in [('total','-'),('direct','--'),('indirect',':')]:
        ax.plot(LET, f('DSB_sites',eff,ion), ls=ls, label=f'{ion} {eff}')
ax.set_xscale('log'); ax.set_xlabel('LET (keV/µm)'); ax.set_ylabel('Yield'); ax.set_title('DSB sites: total/direct/indirect for H, C, Ne'); ax.grid(True, alpha=.3); ax.legend(fontsize=8,ncol=2)
fig.tight_layout(); fig.savefig(ROOT/'figures'/'fig4_dsb_sites_effect_components.png', dpi=180); plt.close(fig)
print(json.dumps(summary['aggregate'], indent=2))
