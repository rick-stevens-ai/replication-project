#!/usr/bin/env python3
from pathlib import Path
import re, json, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/extracted'
( ROOT/'results').mkdir(exist_ok=True); (ROOT/'figures').mkdir(exist_ok=True)
files=sorted(DATA.glob('*.parquet'))
rows=[]
for p in files:
    m=re.match(r'080322_dataframe_zstack0_(.+)_([^_]+)\.parquet', p.name)
    microscope=m.group(1) if m else 'unknown'
    mag=m.group(2).replace('x','') if m else 'unknown'
    df=pd.read_parquet(p)
    # Basic comparisons. Slice actual corresponds visible slice; cell actual whole-cell truth.
    for counted in ['DSBCountedBreaks','H2AXCountedBreaks']:
        for truth in ['ActualBreaksSlice','ActualBreaksCell']:
            rel=(df[counted]-df[truth])/df[truth].replace(0,np.nan)
            absrel=rel.abs()
            rows.append({
                'file':p.name,'microscope':microscope,'magnification':mag,'n':int(len(df)),
                'counted':counted,'truth':truth,
                'mean_counted':float(df[counted].mean()),'mean_truth':float(df[truth].mean()),
                'mean_bias_fraction':float(rel.mean()),'median_bias_fraction':float(rel.median()),
                'mean_abs_error_fraction':float(absrel.mean()),'median_abs_error_fraction':float(absrel.median()),
                'r':float(df[[counted,truth]].corr().iloc[0,1])
            })
summary=pd.DataFrame(rows)
summary.to_csv(ROOT/'results'/'cached_dataset_error_summary.csv', index=False)
# Aggregate useful paper-level stats: compare DSB counted to actual visible slice, and H2AX to actual visible slice.
agg=summary[summary.truth.eq('ActualBreaksSlice')].groupby(['counted']).agg(
    mean_abs_error_fraction=('mean_abs_error_fraction','mean'),
    min_abs_error_fraction=('mean_abs_error_fraction','min'),
    max_abs_error_fraction=('mean_abs_error_fraction','max'),
    mean_corr=('r','mean'),
    n_datasets=('file','count')
).reset_index()
# Per microscope/mag for DSB vs slice
sel=summary[(summary.counted=='DSBCountedBreaks') & (summary.truth=='ActualBreaksSlice')].copy()
sel['mag_num']=pd.to_numeric(sel['magnification'], errors='coerce')
summary_json={
    'n_parquet_files':len(files),
    'total_rows_per_file_min':int(min(pd.read_parquet(f).shape[0] for f in files)) if files else 0,
    'total_rows_per_file_max':int(max(pd.read_parquet(f).shape[0] for f in files)) if files else 0,
    'aggregate_truth_slice':agg.to_dict(orient='records'),
    'best_DSB_vs_slice':sel.sort_values('mean_abs_error_fraction').head(5).to_dict(orient='records'),
    'worst_DSB_vs_slice':sel.sort_values('mean_abs_error_fraction', ascending=False).head(5).to_dict(orient='records'),
    'artifact_note':'This audit uses cached public PyFoci parquet/count datasets; it does not rerun numba image-processing pipeline.'
}
(ROOT/'results'/'summary.json').write_text(json.dumps(summary_json, indent=2))
# Figures
plt.figure(figsize=(10,5))
plot=sel.sort_values(['microscope','mag_num'])
labels=[f"{r.microscope}\n{r.magnification}x" for _,r in plot.iterrows()]
plt.bar(range(len(plot)), plot['mean_abs_error_fraction']*100)
plt.xticks(range(len(plot)), labels, rotation=70, ha='right', fontsize=7)
plt.ylabel('Mean absolute error vs visible actual breaks (%)')
plt.title('PyFoci cached datasets: DSB counted-break error by microscope/magnification')
plt.tight_layout(); plt.savefig(ROOT/'figures'/'fig1_dsb_error_by_microscope.png', dpi=180); plt.close()
# Scatter sample for representative best/mid/worst
reps=[]
if len(sel):
    reps=[sel.sort_values('mean_abs_error_fraction').iloc[0], sel.iloc[len(sel)//2], sel.sort_values('mean_abs_error_fraction', ascending=False).iloc[0]]
fig, axes=plt.subplots(1, len(reps), figsize=(5*len(reps),4), squeeze=False)
for ax, (_,r) in zip(axes[0], [(None,x) for x in reps]):
    df=pd.read_parquet(DATA/r['file'])
    sample=df.sample(min(2500,len(df)), random_state=1)
    ax.scatter(sample['ActualBreaksSlice'], sample['DSBCountedBreaks'], s=4, alpha=.25)
    lo=min(sample['ActualBreaksSlice'].min(), sample['DSBCountedBreaks'].min()); hi=max(sample['ActualBreaksSlice'].max(), sample['DSBCountedBreaks'].max())
    ax.plot([lo,hi],[lo,hi],'r--',lw=1)
    ax.set_title(f"{r['microscope']} {r['magnification']}x\nMAE {r['mean_abs_error_fraction']*100:.1f}% r={r['r']:.2f}")
    ax.set_xlabel('Actual breaks in slice'); ax.set_ylabel('DSB counted breaks')
fig.tight_layout(); fig.savefig(ROOT/'figures'/'fig2_counted_vs_actual_scatter.png', dpi=180); plt.close(fig)
# H2AX vs DSB comparison
comp=summary[summary.truth.eq('ActualBreaksSlice')].pivot_table(index=['file','microscope','magnification'], columns='counted', values='mean_abs_error_fraction').reset_index()
plt.figure(figsize=(6,5))
plt.scatter(comp['DSBCountedBreaks']*100, comp['H2AXCountedBreaks']*100)
mx=max(comp['DSBCountedBreaks'].max(), comp['H2AXCountedBreaks'].max())*100
plt.plot([0,mx],[0,mx],'r--'); plt.xlabel('DSB counted MAE (%)'); plt.ylabel('H2AX counted MAE (%)'); plt.title('Marker/counting method error comparison')
plt.tight_layout(); plt.savefig(ROOT/'figures'/'fig3_h2ax_vs_dsb_error.png', dpi=180); plt.close()
print(json.dumps(summary_json, indent=2)[:4000])
