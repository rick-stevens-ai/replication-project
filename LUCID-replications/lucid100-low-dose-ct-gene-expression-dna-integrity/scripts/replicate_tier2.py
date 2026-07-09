#!/usr/bin/env python3
"""
Tier-2 replication for Schmid et al. 2025 (IJMS 26:11869).

Uses the inferred in-vivo/ex-vivo subset (results/invivo_exvivo_labels.json,
produced by scripts/infer_invivo_subset.py) to reproduce:
  G5  in-vivo upregulation of DDB2, FDXR, AEN, PHLDA3
  G6  WNT3 in-vivo NS (p=0.302)
  G7  POU2AF1 in-vivo borderline (p=0.049)
  G8  in-vivo vs ex-vivo difference for all genes except WNT3
  G11 in-vivo OLS DGE~DLP: AEN, FDXR, DDB2, PHLDA3 p<0.0001
  G12 in-vivo r² ≈ 0.66 (AEN), 0.56 (FDXR)
  G13 in-vivo BAX r²=0.15 p=0.043; EDA2R r²=0.14 p=0.055
  G14 ex-vivo regressions ~3× weaker
  G15 EDA2R ex-vivo regression stronger (p<0.0001)
  G16 in-vivo DLP-stratified (<500 vs >=500 mGy*cm)

Also re-runs the paired DSB analysis (D3) and writes results/tier2_results.json
plus dose-response figures into figures/.

CPU-only, no external dependencies beyond numpy/scipy/matplotlib.
"""
import os, sys, csv, json
from pathlib import Path
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ART = ROOT / 'artifacts'
RES = ROOT / 'results'; RES.mkdir(exist_ok=True)
FIG = ROOT / 'figures'; FIG.mkdir(exist_ok=True)

GENES = ["DDB2","FDXR","POU2AF1","WNT3","BAX","AEN","EDA2R","MIR34AHG","PHLDA3"]

def load_a1():
    rows = list(csv.reader(open(ART/'ijms-26-11869-t0A1.tsv'), delimiter='\t'))
    d = {}
    for r in rows[3:]:
        if not r or not r[0].strip(): continue
        pid = int(r[0])
        def f(x):
            x = x.strip().replace('\u2212','-')
            return float('nan') if x in ('','-') else float(x)
        vals = [f(r[i+1]) for i in range(9)]
        dlp = f(r[10]) if len(r)>10 else float('nan')
        eff = f(r[11]) if len(r)>11 else float('nan')
        d[pid] = {'genes':vals,'DLP':dlp,'eff':eff}
    return d

def load_a2():
    rows = list(csv.reader(open(ART/'ijms-26-11869-t0A2.tsv'), delimiter='\t'))
    out = []
    for r in rows[2:]:
        if not r or not r[0].strip(): continue
        def f(x):
            x = x.strip().replace('\u2212','-')
            return float('nan') if x in ('','-') else float(x)
        out.append({'pid':int(r[0]),'pre':f(r[1]),'post':f(r[2]),'rif':f(r[3]),
                    'DLP':f(r[4]),'eff':f(r[5])})
    return out

def main():
    a1 = load_a1()
    a2 = load_a2()
    labels = json.loads((RES/'invivo_exvivo_labels.json').read_text())
    in_pids = set(labels['in_vivo_pids'])
    ex_pids = set(labels['ex_vivo_pids'])
    print(f"In-vivo n={len(in_pids)}  Ex-vivo n={len(ex_pids)}  (per inferred labels)")

    pids_full = sorted([p for p in a1 if not any(np.isnan(a1[p]['genes']))])
    in_idx = [pids_full.index(p) for p in sorted(in_pids)]
    ex_idx = [pids_full.index(p) for p in sorted(ex_pids)]
    arr = np.array([a1[p]['genes'] for p in pids_full])
    dlp = np.array([a1[p]['DLP'] for p in pids_full])

    results = {'in_vivo_n':len(in_idx), 'ex_vivo_n':len(ex_idx),
               'label_max_median_error':labels['max_median_error'],
               'label_uniqueness':labels['uniqueness']}

    # ---- 1. In-vivo per-gene one-sample test (log2 vs 0) ----
    print("\n=== G5/G6/G7: In-vivo per-gene tests (log2 DGE vs 0) ===")
    g_in = {}
    for i,g in enumerate(GENES):
        v = arr[in_idx, i]
        log2v = np.log2(v)
        t, p_t = stats.ttest_1samp(log2v, 0.0)
        try:
            wstat, p_w = stats.wilcoxon(log2v)
        except ValueError:
            wstat, p_w = float('nan'), float('nan')
        med = float(np.median(v))
        g_in[g] = {'n':len(v),'median':med,'mean_log2':float(np.mean(log2v)),
                   't':float(t),'p_ttest':float(p_t),'p_wilcoxon':float(p_w)}
        print(f"  {g:10s} n={len(v):2d} median={med:6.3f}  log2 mean={np.mean(log2v):+.3f}  "
              f"t-p={p_t:.4g}  wilcox-p={p_w:.4g}")
    results['in_vivo_tests'] = g_in

    # ---- 2. Ex-vivo per-gene one-sample test (mirror) ----
    print("\n=== Ex-vivo per-gene tests ===")
    g_ex = {}
    for i,g in enumerate(GENES):
        v = arr[ex_idx, i]
        log2v = np.log2(v)
        t, p_t = stats.ttest_1samp(log2v, 0.0)
        try:
            wstat, p_w = stats.wilcoxon(log2v)
        except ValueError:
            wstat, p_w = float('nan'), float('nan')
        med = float(np.median(v))
        g_ex[g] = {'n':len(v),'median':med,'mean_log2':float(np.mean(log2v)),
                   't':float(t),'p_ttest':float(p_t),'p_wilcoxon':float(p_w)}
        print(f"  {g:10s} n={len(v):2d} median={med:6.3f}  log2 mean={np.mean(log2v):+.3f}  "
              f"t-p={p_t:.4g}  wilcox-p={p_w:.4g}")
    results['ex_vivo_tests'] = g_ex

    # ---- 3. In-vivo vs ex-vivo Mann-Whitney (G8) ----
    print("\n=== G8: In-vivo vs Ex-vivo comparison (Mann-Whitney U) ===")
    cmp_ = {}
    for i,g in enumerate(GENES):
        u, p = stats.mannwhitneyu(arr[in_idx,i], arr[ex_idx,i], alternative='two-sided')
        cmp_[g] = {'U':float(u),'p':float(p)}
        print(f"  {g:10s}  U={u:6.1f}  p={p:.4g}")
    results['invivo_vs_exvivo'] = cmp_

    # ---- 4. In-vivo dose-response OLS (G11-G13) ----
    print("\n=== G11-G13: In-vivo dose-response (OLS DGE ~ DLP) ===")
    reg_in = {}
    dlp_in = dlp[in_idx]
    for i,g in enumerate(GENES):
        y = arr[in_idx,i]
        m = stats.linregress(dlp_in, y)
        reg_in[g] = {'r2':float(m.rvalue**2),'p':float(m.pvalue),
                     'slope':float(m.slope),'intercept':float(m.intercept)}
        print(f"  {g:10s}  r²={m.rvalue**2:.3f}  p={m.pvalue:.4g}  slope={m.slope:+.5f}")
    results['regression_in_vivo'] = reg_in

    print("\n=== G14/G15: Ex-vivo dose-response (OLS DGE ~ DLP) ===")
    reg_ex = {}
    dlp_ex = dlp[ex_idx]
    for i,g in enumerate(GENES):
        y = arr[ex_idx,i]
        m = stats.linregress(dlp_ex, y)
        reg_ex[g] = {'r2':float(m.rvalue**2),'p':float(m.pvalue),
                     'slope':float(m.slope),'intercept':float(m.intercept)}
        print(f"  {g:10s}  r²={m.rvalue**2:.3f}  p={m.pvalue:.4g}  slope={m.slope:+.5f}")
    results['regression_ex_vivo'] = reg_ex

    # ---- 5. G14 verification: FDXR ratio of r² (in/ex) ----
    fdxr_ratio = reg_in['FDXR']['r2'] / max(reg_ex['FDXR']['r2'], 1e-9)
    print(f"\n  FDXR in-vivo/ex-vivo r² ratio = {fdxr_ratio:.2f}  (paper says ~3.2×)")
    results['fdxr_invivo_exvivo_r2_ratio'] = float(fdxr_ratio)

    # ---- 6. G16: in-vivo DLP-stratified (<500 vs >=500) ----
    print("\n=== G16: In-vivo DLP-stratified (<500 vs >=500 mGy·cm) Mann-Whitney ===")
    low = [j for j in in_idx if dlp[j] < 500]
    high = [j for j in in_idx if dlp[j] >= 500]
    print(f"  Low n={len(low)}  High n={len(high)}")
    strat = {'n_low':len(low),'n_high':len(high)}
    for i,g in enumerate(GENES):
        u, p = stats.mannwhitneyu(arr[low,i], arr[high,i], alternative='two-sided')
        ml, mh = float(np.median(arr[low,i])), float(np.median(arr[high,i]))
        strat[g] = {'median_low':ml,'median_high':mh,'U':float(u),'p':float(p)}
        print(f"  {g:10s}  med_low={ml:5.3f}  med_high={mh:5.3f}  U={u:6.1f}  p={p:.4g}")
    results['dlp_stratified_in_vivo'] = strat

    # ---- 7. D3 re-analysis (paired DSB) ----
    print("\n=== D3: Paired DSB re-analysis (γ-H2AX post vs pre, n=12) ===")
    pre = np.array([r['pre'] for r in a2])
    post = np.array([r['post'] for r in a2])
    rif = np.array([r['rif'] for r in a2])
    dlp_g = np.array([r['DLP'] for r in a2])

    p_mw = stats.mannwhitneyu(pre, post, alternative='two-sided').pvalue
    p_paired_t = stats.ttest_rel(post, pre).pvalue
    p_wilcox = stats.wilcoxon(rif).pvalue
    p_signtest = stats.binomtest(int((rif > 0).sum()), len(rif), 0.5).pvalue
    print(f"  Mann-Whitney U (independent, INCORRECT for paired design): p={p_mw:.4f}  [paper: 0.37]")
    print(f"  Paired t-test (correct):                                   p={p_paired_t:.4f}")
    print(f"  Wilcoxon signed-rank (paired):                             p={p_wilcox:.4f}")
    print(f"  Sign test:                                                 p={p_signtest:.4f}")
    rif_pos = int((rif > 0).sum()); rif_neg = int((rif < 0).sum()); rif_zero = int((rif==0).sum())
    print(f"  RIF sign distribution: {rif_pos} positive, {rif_neg} negative, {rif_zero} zero (n=12)")
    results['dsb_paired_reanalysis'] = {
        'n':len(pre),
        'mean_pre':float(np.mean(pre)),'sd_pre':float(np.std(pre,ddof=0)),
        'mean_post':float(np.mean(post)),'sd_post':float(np.std(post,ddof=0)),
        'mean_rif':float(np.mean(rif)),'sd_rif':float(np.std(rif,ddof=0)),
        'p_mann_whitney_independent':float(p_mw),
        'p_paired_t':float(p_paired_t),
        'p_wilcoxon_signed_rank':float(p_wilcox),
        'p_sign_test':float(p_signtest),
        'rif_pos':rif_pos,'rif_neg':rif_neg,'rif_zero':rif_zero,
    }

    # ---- 8. Dose-RIF regression (extra) ----
    m = stats.linregress(dlp_g, rif)
    print(f"\n  RIF ~ DLP regression (n=12): r²={m.rvalue**2:.3f}  p={m.pvalue:.4f}")
    results['rif_dlp_regression'] = {'r2':float(m.rvalue**2),'p':float(m.pvalue),
                                     'slope':float(m.slope),'intercept':float(m.intercept)}

    # ---- 9. Pathway-level test: DNA-damage-repair (DDR) gene set ----
    # Group genes by canonical function:
    #   DDR/p53 response: DDB2, FDXR, AEN, BAX, PHLDA3
    #   Other transcriptomic markers: EDA2R, MIR34AHG (p53 targets), WNT3, POU2AF1
    # Pathway test: combined-cohort one-sample t on mean(log2 DDR DGE) vs 0
    print("\n=== Pathway test: p53-driven DDR gene set (DDB2/FDXR/AEN/BAX/PHLDA3) ===")
    ddr = ["DDB2","FDXR","AEN","BAX","PHLDA3"]
    ddr_idx = [GENES.index(x) for x in ddr]
    for label, sel in [('combined', list(range(60))), ('in_vivo', in_idx), ('ex_vivo', ex_idx)]:
        sub = arr[sel][:,ddr_idx]
        # per-patient log2 mean across 5 DDR genes
        per_pt = np.mean(np.log2(sub), axis=1)
        t,p = stats.ttest_1samp(per_pt, 0.0)
        print(f"  {label:10s} n={len(sel):2d}  mean log2(DDR) = {np.mean(per_pt):+.3f}  "
              f"t-p={p:.4g}  median DDR = {np.median(per_pt):+.3f}")
        results.setdefault('ddr_pathway_test',{})[label] = {
            'n':len(sel),'mean_log2':float(np.mean(per_pt)),
            'median_log2':float(np.median(per_pt)),
            't':float(t),'p':float(p),'genes':ddr}

    # Same for p53-target up-set including EDA2R + MIR34AHG (p53-regulated)
    print("\n=== Pathway test: extended p53-target up-set (DDB2/FDXR/AEN/PHLDA3/EDA2R/MIR34AHG) ===")
    p53 = ["DDB2","FDXR","AEN","PHLDA3","EDA2R","MIR34AHG"]
    p53_idx = [GENES.index(x) for x in p53]
    for label, sel in [('combined', list(range(60))), ('in_vivo', in_idx), ('ex_vivo', ex_idx)]:
        sub = arr[sel][:,p53_idx]
        per_pt = np.mean(np.log2(sub), axis=1)
        t,p = stats.ttest_1samp(per_pt, 0.0)
        print(f"  {label:10s} n={len(sel):2d}  mean log2(p53-up) = {np.mean(per_pt):+.3f}  t-p={p:.4g}")
        results.setdefault('p53_uppathway_test',{})[label] = {
            'n':len(sel),'mean_log2':float(np.mean(per_pt)),
            't':float(t),'p':float(p),'genes':p53}

    # ---- 10. Save results ----
    with open(RES/'tier2_results.json','w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {RES/'tier2_results.json'}")

    # ---- 11. Make figures (matplotlib) ----
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping figures")
        return

    # Figure: in-vivo dose-response panels for top genes
    plot_genes = ['AEN','FDXR','DDB2','PHLDA3','BAX','EDA2R']
    fig, axes = plt.subplots(2,3, figsize=(12,7))
    for ax, g in zip(axes.flat, plot_genes):
        i = GENES.index(g)
        x = dlp[in_idx]; y = arr[in_idx,i]
        ax.scatter(x, y, s=22, c='steelblue', label=f'in vivo n={len(in_idx)}')
        x2 = dlp[ex_idx]; y2 = arr[ex_idx,i]
        ax.scatter(x2, y2, s=18, c='tomato', marker='x', alpha=0.7, label=f'ex vivo n={len(ex_idx)}')
        m_in = stats.linregress(x,y); m_ex = stats.linregress(x2,y2)
        xx = np.linspace(0, max(np.max(x),np.max(x2))*1.05, 100)
        ax.plot(xx, m_in.intercept+m_in.slope*xx, 'b-', lw=1.5)
        ax.plot(xx, m_ex.intercept+m_ex.slope*xx, 'r--', lw=1.2)
        ax.set_title(f"{g}  in r²={m_in.rvalue**2:.2f} p={m_in.pvalue:.2g}\n"
                     f"      ex r²={m_ex.rvalue**2:.2f} p={m_ex.pvalue:.2g}",
                     fontsize=9)
        ax.set_xlabel('DLP [mGy·cm]'); ax.set_ylabel('DGE')
        ax.axhline(1.0, color='grey', lw=0.5, ls=':')
        ax.legend(fontsize=7, loc='best')
    plt.tight_layout()
    plt.savefig(FIG/'dose_response_in_ex_vivo.png', dpi=150)
    print(f"Saved {FIG/'dose_response_in_ex_vivo.png'}")

    # Figure: pre/post DSB paired
    fig, ax = plt.subplots(figsize=(6,5))
    for i in range(len(pre)):
        ax.plot([0,1],[pre[i],post[i]], 'k-', alpha=0.4)
    ax.scatter([0]*len(pre), pre, s=50, c='steelblue', label='pre')
    ax.scatter([1]*len(post), post, s=50, c='tomato', label='post')
    ax.set_xticks([0,1]); ax.set_xticklabels(['pre-CT','post-CT'])
    ax.set_ylabel('γ-H2AX + 53BP1 foci/cell')
    ax.set_title(f'Paired DSB foci (n={len(pre)})\n'
                 f'paired-t p={p_paired_t:.3f}  signed-rank p={p_wilcox:.3f}  '
                 f'(paper used independent-sample test, p=0.37)',
                 fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIG/'dsb_paired.png', dpi=150)
    print(f"Saved {FIG/'dsb_paired.png'}")

    print("\nTier-2 reproduction complete.")

if __name__ == '__main__':
    main()
