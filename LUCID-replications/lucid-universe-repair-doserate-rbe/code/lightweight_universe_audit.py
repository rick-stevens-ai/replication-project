#!/usr/bin/env python3
"""Lightweight deterministic audit for Liew et al. 2022 UNIVERSE repair/dose-rate RBE.

This avoids the failed stochastic ion-track driver and focuses on paper-released
parameters/tables and a transparent phenomenological dose-rate repair model.
"""
from pathlib import Path
import json, csv, math
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'results').mkdir(exist_ok=True); (ROOT/'figures').mkdir(exist_ok=True)
# Table 1 parameters from PROGRESS/source
PARAMS={
 'DU145': {'K_iDSB':5.9e-3,'K_cDSB':0.17,'T_i_min':4.0,'T_c_min':100.0},
 'RSC_with_repair': {'K_iDSB':3.5e-5,'K_cDSB':9.8e-3,'T_i_min':11.4,'T_c_min':129.6},
 'RSC_no_repair': {'K_iDSB':6.5e-3,'K_cDSB':8.5e-3,'T_i_min':None,'T_c_min':None},
}
# Table 2 approximate max relative differences (%) from paper not fully transcribed in source; compute diagnostic grid instead.
# Table 3 values copied from subagent scaffold / paper
SOBP_TABLE3 = {
    'proton_1fx': {'depths_mm':[35,100,120,127],'LET_keV_um':[2.0,3.0,4.1,5.3],'dose_rate_Gy_per_min':[11,18,42,53],'R_TD50':[1.042,1.051,1.059,1.061]},
    'proton_2fx': {'depths_mm':[35,100,120,127],'LET_keV_um':[2.0,3.0,4.1,5.3],'dose_rate_Gy_per_min':[8,14,31,41],'R_TD50':[1.022,1.031,1.038,1.040]},
    'helium_1fx': {'depths_mm':[35,100,120,127],'LET_keV_um':[4.2,9.3,14.4,22.0],'dose_rate_Gy_per_min':[11,11,10,9],'R_TD50':[1.042,1.042,1.041,1.036]},
    'helium_2fx': {'depths_mm':[35,100,120,127],'LET_keV_um':[4.2,9.3,14.4,22.0],'dose_rate_Gy_per_min':[8,7,7,6],'R_TD50':[1.022,1.018,1.018,1.015]},
}
# Approx digitized from paper figure by failed subagent; only for qualitative diagnostic
MEASURED_RBE = {
    'proton_1fx':[1.13,1.18,1.30,1.45], 'proton_2fx':[1.10,1.15,1.27,1.38],
    'helium_1fx':[1.30,1.65,2.05,2.55], 'helium_2fx':[1.28,1.60,2.00,2.40],
}
# Simple transparent repair saturation factor: effect grows with irradiation time relative to half-lives.
def repair_factor(dose_Gy, dose_rate_Gy_per_min, T_i=4.0, T_c=100.0):
    T=dose_Gy/dose_rate_Gy_per_min
    # isolated repair dominates dose-rate effect; complex repair slow and weaker
    fi=1-math.exp(-math.log(2)*T/T_i)
    fc=1-math.exp(-math.log(2)*T/T_c)
    return 0.75*fi+0.25*fc

def base_no_repair_rbe(LET, dose):
    # Phenomenological monotone LET/dose response just for figure-level trend.
    return 1.0 + 0.012*LET/(1+0.02*LET) * (1+0.05*math.log1p(dose))

def fixed_ref_rbe(LET,dose,rate_Gy_s,ref_Gy_min=2.0):
    nr=base_no_repair_rbe(LET,dose)
    f=repair_factor(dose, rate_Gy_s*60)
    fref=repair_factor(dose, ref_Gy_min)
    # fixed reference RBE grows toward no-repair-like limit with high ion dose-rate but remains modest.
    return nr*(1+0.18*(fref-f))

def adapted_rbe(LET,dose,rate_Gy_s):
    nr=base_no_repair_rbe(LET,dose)
    return nr*(1+0.05*(0.5-repair_factor(dose,rate_Gy_s*60)))

def no_repair_rbe(LET,dose): return base_no_repair_rbe(LET,dose)
# Generate diagnostic curves similar to Figs 1-3
rates_s=np.array([0.03,0.1,0.3,1,3,10])
LETs=[2,8,25]; doses=[2,6,12,24]
curves=[]
for D in doses:
  for LET in LETs:
    for r in rates_s:
      curves.append({'dose_Gy':D,'LET_keV_um':LET,'dose_rate_Gy_s':float(r),'fixed_reference_RBE':fixed_ref_rbe(LET,D,r),'dose_rate_adapted_RBE':adapted_rbe(LET,D,r),'no_repair_RBE':no_repair_rbe(LET,D)})
with (ROOT/'results'/'diagnostic_rbe_curves.csv').open('w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(curves[0].keys())); w.writeheader(); w.writerows(curves)
# Table3 summary and MAD if using simplified predicted no-repair trend * R_TD50
bench={}
for key,tbl in SOBP_TABLE3.items():
    preds=[]
    for LET,RTD in zip(tbl['LET_keV_um'], tbl['R_TD50']):
        preds.append(base_no_repair_rbe(LET,6)*RTD)
    meas=np.array(MEASURED_RBE[key]); pr=np.array(preds)
    bench[key]={'predicted_RBE':preds,'measured_RBE_approx':MEASURED_RBE[key],'MAD_percent':float(np.mean(np.abs(pr-meas)/meas)*100),'table3':tbl}
summary={'verdict_basis':'formula/table/diagnostic only; no raw simulation outputs or FLUKA beamline model released','params_table1':PARAMS,'table3_benchmark':bench,'diagnostic_curve_note':'RBE curves are trend diagnostics from a transparent repair-saturation model, not a bit-exact UNIVERSE GPU reproduction.'}
(ROOT/'results'/'summary.json').write_text(json.dumps(summary,indent=2))
# Figures
fig,axes=plt.subplots(len(doses),len(LETs),figsize=(11,10),sharex=True)
for i,D in enumerate(doses):
  for j,LET in enumerate(LETs):
    ax=axes[i,j]
    xs=rates_s
    ax.plot(xs,[fixed_ref_rbe(LET,D,x) for x in xs],'g--',label='fixed ref')
    ax.plot(xs,[adapted_rbe(LET,D,x) for x in xs],':',color='orange',label='adapted')
    ax.axhline(no_repair_rbe(LET,D),color='blue',label='no repair')
    ax.set_xscale('log'); ax.grid(alpha=.3); ax.set_title(f'D={D} Gy LET={LET}')
    if i==len(doses)-1: ax.set_xlabel('dose rate Gy/s')
    if j==0: ax.set_ylabel('RBE')
    if i==0 and j==0: ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(ROOT/'figures'/'fig1_diagnostic_rbe_vs_doserate.png',dpi=180); plt.close(fig)
# R_TD50 table3 plot
fig,ax=plt.subplots(figsize=(7,5))
for key,tbl in SOBP_TABLE3.items(): ax.plot(tbl['depths_mm'], tbl['R_TD50'], marker='o', label=key)
ax.set_xlabel('depth (mm)'); ax.set_ylabel('R_TD50'); ax.set_title('Published Table 3 dose-rate correction factors'); ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(ROOT/'figures'/'fig2_table3_R_TD50.png',dpi=180); plt.close(fig)
# benchmark plot
fig,ax=plt.subplots(figsize=(7,5))
for key,b in bench.items():
    ax.scatter(b['measured_RBE_approx'], b['predicted_RBE'], label=f"{key} MAD {b['MAD_percent']:.0f}%")
lo=1; hi=2.7; ax.plot([lo,hi],[lo,hi],'k--'); ax.set_xlim(lo,hi); ax.set_ylim(lo,hi); ax.set_xlabel('approx measured RBE'); ax.set_ylabel('simplified predicted RBE'); ax.set_title('SOBP RBE benchmark diagnostic') ; ax.legend(fontsize=7); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(ROOT/'figures'/'fig3_sobp_rbe_benchmark_diagnostic.png',dpi=180); plt.close(fig)
print(json.dumps({'curves':len(curves),'bench_keys':list(bench),'figures':3},indent=2))
