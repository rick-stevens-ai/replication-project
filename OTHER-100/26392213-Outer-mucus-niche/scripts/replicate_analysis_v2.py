#!/usr/bin/env python3
"""
Replication analysis for Li et al. 2015 (PMID 26392213)
"The outer mucus layer hosts a distinct intestinal microbial niche"

v2: Fixed demultiplexing — each chip paired with its own mapping file.
    Added per-mouse grouping and location-specific analyses.
    
Key correction: In the paper, "M" = outer mucus layer, "C" = luminal contents.
The inner mucus layer is described as essentially sterile (no bacterial colonization).
So the 16S comparison is: Outer Mucus vs Luminal Contents.
"""

import os
import sys
import gzip
import json
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
import pandas as pd

import skbio
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.ordination import pcoa
from skbio.stats.distance import permanova, anosim

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ============ CONFIG ============
BASE_DIR = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/26392213-Outer-mucus-niche"))
DATA_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "analysis"
FIG_DIR = BASE_DIR / "analysis" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

MIN_READS = 500

# ============ HELPERS ============

def parse_mapping_file(map_path):
    """Parse QIIME-style mapping file."""
    samples = {}
    with open(map_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            parts = line.split('\t')
            sample_id = parts[0]
            barcode = parts[1].strip()
            description = parts[3] if len(parts) > 3 else ''
            samples[barcode] = {
                'sample_id': sample_id,
                'barcode': barcode,
                'description': description
            }
    return samples

def demultiplex_fastq(fastq_path, barcode_map, max_mismatches=0):
    """Demultiplex a barcoded FASTQ file."""
    demuxed = defaultdict(list)
    barcode_lengths = sorted(set(len(b) for b in barcode_map.keys()))
    
    opener = gzip.open if str(fastq_path).endswith('.gz') else open
    total_reads = 0
    assigned_reads = 0
    
    with opener(fastq_path, 'rt') as f:
        while True:
            header = f.readline().strip()
            if not header:
                break
            seq = f.readline().strip()
            plus = f.readline().strip()
            qual = f.readline().strip()
            total_reads += 1
            
            for bc_len in barcode_lengths:
                read_bc = seq[:bc_len]
                if read_bc in barcode_map:
                    info = barcode_map[read_bc]
                    demuxed[info['sample_id']].append(seq[bc_len:])
                    assigned_reads += 1
                    break
            
            if total_reads % 500000 == 0:
                pct = 100*assigned_reads/total_reads if total_reads > 0 else 0
                print(f"  {total_reads:,} reads, {assigned_reads:,} assigned ({pct:.1f}%)")
    
    pct = 100*assigned_reads/total_reads if total_reads > 0 else 0
    print(f"  Total: {total_reads:,} reads, {assigned_reads:,} assigned ({pct:.1f}%)")
    return demuxed

def cluster_sequences(sequences, trunc_len=200):
    """Simple OTU-like clustering by truncating to fixed length."""
    seq_counts = Counter()
    for seq in sequences:
        if len(seq) >= 100:
            key = seq[:trunc_len] if len(seq) >= trunc_len else seq
            seq_counts[key] += 1
    return seq_counts

def classify_sample_spf(sample_id, description):
    """Classify SPF sample into compartment and location."""
    desc = description.lower() if description else ''
    sid = sample_id
    
    # Compartment: M=Mucus (outer), C=Content (luminal)
    if 'colonm' in desc or 'cecumm' in desc or 'ileumm' in desc:
        compartment = 'Outer Mucus'
    elif 'colonc' in desc or 'cecumc' in desc or 'ileumc' in desc:
        compartment = 'Luminal Content'
    elif sid.startswith('CM') or sid.startswith('CeM') or sid.startswith('IlM') or sid.startswith('C3M'):
        compartment = 'Outer Mucus'
    elif sid.startswith('CC') or sid.startswith('CeC') or sid.startswith('IlC'):
        compartment = 'Luminal Content'
    else:
        compartment = 'Unknown'
    
    # Location
    if 'colon' in desc:
        location = 'Colon'
    elif 'cecum' in desc or 'caecum' in desc:
        location = 'Cecum'
    elif 'ileum' in desc:
        location = 'Ileum'
    elif sid.startswith('CC') or sid.startswith('CM'):
        location = 'Colon'
    elif sid.startswith('Ce') or sid.startswith('C3M'):
        location = 'Cecum'
    elif sid.startswith('Il'):
        location = 'Ileum'
    else:
        location = 'Unknown'
    
    # Mouse number (G1-G6)
    if '.G' in sid:
        mouse = sid.split('.G')[-1]
    else:
        mouse = 'Unknown'
    
    return compartment, location, mouse

def classify_sample_dm(sample_id, description):
    """Classify sDMDMm2 sample."""
    desc = description.lower() if description else ''
    
    if 'mucus' in desc:
        compartment = 'Outer Mucus'
    elif 'content' in desc:
        compartment = 'Luminal Content'
    else:
        compartment = 'Unknown'
    
    if 'colon' in desc:
        location = 'Colon'
    elif 'cecum' in desc:
        location = 'Cecum'
    elif 'ileum' in desc:
        location = 'Ileum'
    else:
        location = 'Unknown'
    
    # Mouse group from sample ID (DM1.3, DM4.6, DM8.10, DM6, DM.028, DM10)
    sid = sample_id
    if sid.startswith('DM1.3'):
        mouse = 'DM1-3'
    elif sid.startswith('DM4.6'):
        mouse = 'DM4-6'
    elif sid.startswith('DM8.10'):
        mouse = 'DM8-10'
    elif sid.startswith('DM10'):
        mouse = 'DM10'
    elif sid.startswith('DM6'):
        mouse = 'DM6'
    elif sid.startswith('DM.028'):
        mouse = 'DM028'
    else:
        mouse = 'Unknown'
    
    return compartment, location, mouse

def build_otu_table(all_demuxed):
    """Build OTU table."""
    print("\nBuilding OTU table...")
    all_otus = set()
    sample_otu_counts = {}
    
    for sample_id, sequences in sorted(all_demuxed.items()):
        if len(sequences) < MIN_READS:
            print(f"  Skipping {sample_id}: only {len(sequences)} reads")
            continue
        counts = cluster_sequences(sequences)
        sample_otu_counts[sample_id] = counts
        all_otus.update(counts.keys())
    
    otu_list = sorted(all_otus)
    otu_ids = {seq: f"OTU_{i:04d}" for i, seq in enumerate(otu_list)}
    
    data = {}
    for sid, counts in sample_otu_counts.items():
        data[sid] = [counts.get(seq, 0) for seq in otu_list]
    
    otu_table = pd.DataFrame(data, index=[otu_ids[s] for s in otu_list])
    print(f"  {otu_table.shape[0]} OTUs x {otu_table.shape[1]} samples")
    return otu_table

def run_diversity(otu_table, metadata, dataset_name):
    """Full diversity analysis."""
    print(f"\n{'='*60}")
    print(f"Diversity Analysis: {dataset_name}")
    print(f"{'='*60}")
    
    common = [s for s in otu_table.columns if s in metadata.index]
    otu = otu_table[common]
    meta = metadata.loc[common]
    
    # Filter rare OTUs
    otu = otu[otu.sum(axis=1) >= 2]
    print(f"After filtering: {otu.shape[0]} OTUs, {otu.shape[1]} samples")
    
    matrix = otu.values.T
    sids = list(otu.columns)
    
    # --- Alpha Diversity ---
    print("\n--- Alpha Diversity ---")
    shannon = alpha_diversity('shannon', matrix, ids=sids)
    observed = alpha_diversity('sobs', matrix, ids=sids)
    
    alpha_df = pd.DataFrame({
        'Shannon': shannon,
        'Observed_OTUs': observed,
        'Compartment': meta.loc[sids, 'Compartment'],
        'Location': meta.loc[sids, 'Location'],
        'Mouse': meta.loc[sids, 'Mouse'],
        'Total_Reads': matrix.sum(axis=1)
    })
    
    print("\nAlpha diversity by compartment:")
    for comp in ['Outer Mucus', 'Luminal Content']:
        d = alpha_df[alpha_df['Compartment'] == comp]
        print(f"  {comp}: Shannon = {d['Shannon'].mean():.2f} ± {d['Shannon'].std():.2f}, "
              f"OTUs = {d['Observed_OTUs'].mean():.0f} ± {d['Observed_OTUs'].std():.0f}, "
              f"n = {len(d)}")
    
    print("\nAlpha diversity by location:")
    for loc in ['Colon', 'Cecum', 'Ileum']:
        d = alpha_df[alpha_df['Location'] == loc]
        if len(d) > 0:
            print(f"  {loc}: Shannon = {d['Shannon'].mean():.2f} ± {d['Shannon'].std():.2f}, n = {len(d)}")
    
    alpha_df.to_csv(OUT_DIR / f"{dataset_name}_alpha_diversity_v2.csv")
    
    # Alpha diversity boxplot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, metric in zip(axes, ['Shannon', 'Observed_OTUs']):
        sns.boxplot(data=alpha_df, x='Location', y=metric, hue='Compartment',
                   palette={'Outer Mucus': '#2196F3', 'Luminal Content': '#FF5722'},
                   ax=ax)
        ax.set_title(f'{metric.replace("_", " ")} - {dataset_name}')
        ax.legend(title='Compartment')
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"{dataset_name}_alpha_v2.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # --- Beta Diversity ---
    print("\n--- Beta Diversity ---")
    bc_dm = beta_diversity('braycurtis', matrix, ids=sids)
    bc_pcoa_result = pcoa(bc_dm)
    
    grouping = meta.loc[sids, 'Compartment']
    
    # Overall PERMANOVA
    perm_result = permanova(bc_dm, grouping, permutations=999)
    pval = float(perm_result['p-value'])
    fstat = float(perm_result['test statistic'])
    print(f"\nPERMANOVA (all samples, Bray-Curtis):")
    print(f"  F = {fstat:.4f}, p = {pval:.4f}")
    
    anosim_result = anosim(bc_dm, grouping, permutations=999)
    ar = float(anosim_result['test statistic'])
    ap = float(anosim_result['p-value'])
    print(f"ANOSIM: R = {ar:.4f}, p = {ap:.4f}")
    
    # Location-specific PERMANOVA
    location_results = {}
    for loc in ['Colon', 'Cecum', 'Ileum']:
        loc_sids = [s for s in sids if meta.loc[s, 'Location'] == loc]
        comps = meta.loc[loc_sids, 'Compartment'].unique()
        if len(loc_sids) >= 4 and len(comps) >= 2:
            loc_matrix = matrix[[sids.index(s) for s in loc_sids]]
            loc_dm = beta_diversity('braycurtis', loc_matrix, ids=loc_sids)
            loc_grouping = meta.loc[loc_sids, 'Compartment']
            try:
                loc_perm = permanova(loc_dm, loc_grouping, permutations=999)
                lp = float(loc_perm['p-value'])
                lf = float(loc_perm['test statistic'])
                print(f"PERMANOVA ({loc} only): F = {lf:.4f}, p = {lp:.4f}")
                location_results[loc] = {'F': lf, 'p': lp}
            except Exception as e:
                print(f"PERMANOVA ({loc}): failed — {e}")
    
    # PERMANOVA by location
    loc_grouping = meta.loc[sids, 'Location']
    if len(loc_grouping.unique()) >= 2:
        loc_perm = permanova(bc_dm, loc_grouping, permutations=999)
        print(f"PERMANOVA (by Location): F = {float(loc_perm['test statistic']):.4f}, p = {float(loc_perm['p-value']):.4f}")
    
    # --- PCoA Plot (main figure — replicating Figure 1b) ---
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    coords = bc_pcoa_result.samples
    prop = bc_pcoa_result.proportion_explained
    
    colors = {'Outer Mucus': '#2196F3', 'Luminal Content': '#FF5722'}
    markers = {'Colon': 'o', 'Cecum': 's', 'Ileum': '^'}
    
    for ax_idx, (pc_x, pc_y) in enumerate([(0, 1), (0, 2)]):
        ax = axes[ax_idx]
        for sid in sids:
            if sid in coords.index:
                comp = meta.loc[sid, 'Compartment']
                loc = meta.loc[sid, 'Location']
                x = coords.loc[sid].iloc[pc_x]
                y = coords.loc[sid].iloc[pc_y]
                ax.scatter(x, y, c=colors.get(comp, 'gray'),
                          marker=markers.get(loc, 'D'),
                          s=120, edgecolors='black', linewidth=0.5, zorder=5,
                          alpha=0.8)
        
        for comp, color in colors.items():
            ax.scatter([], [], c=color, marker='o', s=100, label=comp,
                      edgecolors='black', linewidth=0.5)
        for loc, marker in markers.items():
            ax.scatter([], [], c='gray', marker=marker, s=100, label=loc,
                      edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel(f'PC{pc_x+1} ({prop.iloc[pc_x]*100:.1f}%)')
        ax.set_ylabel(f'PC{pc_y+1} ({prop.iloc[pc_y]*100:.1f}%)')
        ax.legend(loc='best', framealpha=0.8, fontsize=9)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    
    axes[0].set_title(f'PCoA (Bray-Curtis) — {dataset_name}\n'
                      f'PERMANOVA F={fstat:.2f}, p={pval:.3f}')
    axes[1].set_title(f'PCoA PC1 vs PC3 — {dataset_name}')
    
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"{dataset_name}_PCoA_v2.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {dataset_name}_PCoA_v2.png")
    
    # --- Heatmap of top OTUs ---
    top_n = 30
    otu_sums = otu.sum(axis=1).sort_values(ascending=False)
    top_otus = otu_sums.head(top_n).index
    
    # Relative abundance
    rel_abund = otu.div(otu.sum(axis=0), axis=1)
    top_rel = rel_abund.loc[top_otus]
    
    # Sort samples by compartment then location
    sort_order = meta.sort_values(['Compartment', 'Location']).index
    sort_order = [s for s in sort_order if s in top_rel.columns]
    top_rel_sorted = top_rel[sort_order]
    
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(top_rel_sorted, cmap='YlOrRd', ax=ax, 
               xticklabels=True, yticklabels=True,
               cbar_kws={'label': 'Relative Abundance'})
    ax.set_title(f'Top {top_n} OTUs — {dataset_name}')
    ax.set_xlabel('Samples')
    ax.set_ylabel('OTUs')
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"{dataset_name}_heatmap_v2.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {dataset_name}_heatmap_v2.png")
    
    return {
        'permanova_F': fstat,
        'permanova_p': pval,
        'anosim_R': ar,
        'anosim_p': ap,
        'location_permanova': location_results,
        'alpha': alpha_df,
        'n_samples': len(sids),
        'n_otus': otu.shape[0],
        'variance_PC1': float(prop.iloc[0]),
        'variance_PC2': float(prop.iloc[1]),
    }

def main():
    print("="*60)
    print("Replication: Li et al. 2015 (PMID 26392213)")
    print("The outer mucus layer hosts a distinct intestinal microbial niche")
    print("v2 — corrected chip-mapping pairing")
    print("="*60)
    
    all_results = {}
    
    # ========== SPF Dataset ==========
    print("\n" + "#"*60)
    print("SPF Dataset — Figure 1")
    print("#"*60)
    
    # Pair each chip with its own mapping file
    spf_pairs = [
        (DATA_DIR / 'SPF_chip_1.fastq.gz', DATA_DIR / 'SPF_map1.txt'),
        (DATA_DIR / 'SPF_chip_2.fastq.gz', DATA_DIR / 'SPF_map2.txt'),
    ]
    
    all_demuxed = defaultdict(list)
    all_info = {}
    
    for fq, mp in spf_pairs:
        bc_map = parse_mapping_file(mp)
        for bc, info in bc_map.items():
            all_info[info['sample_id']] = info
        print(f"\nDemultiplexing {fq.name} with {mp.name}...")
        demuxed = demultiplex_fastq(fq, bc_map)
        for sid, seqs in demuxed.items():
            all_demuxed[sid].extend(seqs)
    
    print(f"\nSPF: {len(all_demuxed)} samples total")
    for sid in sorted(all_demuxed.keys()):
        print(f"  {sid}: {len(all_demuxed[sid]):,} reads — {all_info.get(sid, {}).get('description', '?')}")
    
    otu_table = build_otu_table(all_demuxed)
    
    # Build metadata
    meta_records = []
    for sid in otu_table.columns:
        info = all_info.get(sid, {})
        comp, loc, mouse = classify_sample_spf(sid, info.get('description', ''))
        meta_records.append({'SampleID': sid, 'Compartment': comp, 'Location': loc, 'Mouse': mouse,
                            'Description': info.get('description', ''), 'TotalReads': len(all_demuxed.get(sid, []))})
    
    metadata = pd.DataFrame(meta_records).set_index('SampleID')
    metadata.to_csv(OUT_DIR / 'SPF_metadata_v2.csv')
    
    print(f"\nSample counts:")
    print(metadata.groupby(['Compartment', 'Location']).size())
    
    spf_results = run_diversity(otu_table, metadata, 'SPF')
    all_results['SPF'] = spf_results
    
    # ========== sDMDMm2 Dataset ==========
    print("\n" + "#"*60)
    print("sDMDMm2 Dataset — Supplementary Figure 5")
    print("#"*60)
    
    dm_map = parse_mapping_file(DATA_DIR / 'sDMDMm2_map.txt')
    dm_info = {info['sample_id']: info for info in dm_map.values()}
    
    print(f"\nDemultiplexing sDMDMm2.fastq.gz...")
    dm_demuxed = demultiplex_fastq(DATA_DIR / 'sDMDMm2.fastq.gz', dm_map)
    
    print(f"\nsDMDMm2: {len(dm_demuxed)} samples total")
    for sid in sorted(dm_demuxed.keys()):
        print(f"  {sid}: {len(dm_demuxed[sid]):,} reads — {dm_info.get(sid, {}).get('description', '?')}")
    
    dm_otu = build_otu_table(dm_demuxed)
    
    dm_meta_records = []
    for sid in dm_otu.columns:
        info = dm_info.get(sid, {})
        comp, loc, mouse = classify_sample_dm(sid, info.get('description', ''))
        dm_meta_records.append({'SampleID': sid, 'Compartment': comp, 'Location': loc, 'Mouse': mouse,
                               'Description': info.get('description', ''), 'TotalReads': len(dm_demuxed.get(sid, []))})
    
    dm_metadata = pd.DataFrame(dm_meta_records).set_index('SampleID')
    dm_metadata.to_csv(OUT_DIR / 'sDMDMm2_metadata_v2.csv')
    
    print(f"\nSample counts:")
    print(dm_metadata.groupby(['Compartment', 'Location']).size())
    
    dm_results = run_diversity(dm_otu, dm_metadata, 'sDMDMm2')
    all_results['sDMDMm2'] = dm_results
    
    # ========== SUMMARY ==========
    print("\n" + "="*60)
    print("REPLICATION SUMMARY")
    print("="*60)
    
    for name, r in all_results.items():
        sig = "✓ SIGNIFICANT" if r['permanova_p'] < 0.05 else "✗ NOT SIGNIFICANT"
        print(f"\n{name}:")
        print(f"  Samples: {r['n_samples']}, OTUs: {r['n_otus']}")
        print(f"  PCoA variance: PC1={r['variance_PC1']*100:.1f}%, PC2={r['variance_PC2']*100:.1f}%")
        print(f"  PERMANOVA (Compartment): F = {r['permanova_F']:.4f}, p = {r['permanova_p']:.4f} — {sig}")
        print(f"  ANOSIM: R = {r['anosim_R']:.4f}, p = {r['anosim_p']:.4f}")
        if r.get('location_permanova'):
            for loc, lr in r['location_permanova'].items():
                print(f"  PERMANOVA ({loc} only): F = {lr['F']:.4f}, p = {lr['p']:.4f}")
    
    # Save JSON summary
    json_summary = {}
    for name, r in all_results.items():
        json_summary[name] = {
            'n_samples': r['n_samples'],
            'n_otus': r['n_otus'],
            'PERMANOVA_F': r['permanova_F'],
            'PERMANOVA_p': r['permanova_p'],
            'significant_p005': r['permanova_p'] < 0.05,
            'ANOSIM_R': r['anosim_R'],
            'ANOSIM_p': r['anosim_p'],
            'variance_PC1': r['variance_PC1'],
            'variance_PC2': r['variance_PC2'],
            'location_permanova': r.get('location_permanova', {}),
        }
    
    with open(OUT_DIR / 'replication_summary_v2.json', 'w') as f:
        json.dump(json_summary, f, indent=2)
    
    print(f"\nAll results saved to: {OUT_DIR}")
    print("Done!")

if __name__ == '__main__':
    main()
