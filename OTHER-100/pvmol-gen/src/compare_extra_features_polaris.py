#!/usr/bin/env python3
"""
Compare PyTorch SMILES-X classifier with different extra feature sets.
Polaris version — imports smilesx from ~/pvmol-gen/smilesx.
"""

import os
import sys
import json
import logging
import time

import numpy as np
import pandas as pd

from smilesx.train import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)


FEATURE_CONFIGS = {
    'no_features': {
        'cols': [],
        'dense_depth': 0,
        'desc': 'No extra features (SMILES only)',
    },
    'paper_2feat': {
        'cols': ['ha_num', 'o_num'],
        'dense_depth': 2,
        'desc': 'Paper 2 features (ha_num, o_num)',
    },
    'enriched_8feat': {
        'cols': ['ha_num', 'o_num', 'n_num', 's_num', 'hbd_num', 'TPSA', 'MolLogP', 'NumRotatableBonds'],
        'dense_depth': 3,
        'desc': 'Enriched 8 features',
    },
}


def run_comparison(data_path, outdir, device=None):
    df = pd.read_csv(data_path)
    desc_cols = ['ha_num', 'o_num', 'n_num', 's_num', 'hbd_num', 'TPSA', 'MolLogP', 'NumRotatableBonds']
    df = df.dropna(subset=[c for c in desc_cols if c in df.columns]).reset_index(drop=True)
    
    logger.info(f"Data: {len(df)} molecules, {df['bin_class'].sum():.0f} positive, "
                f"{(1-df['bin_class']).sum():.0f} negative")
    
    results = {}
    
    for config_name, cfg in FEATURE_CONFIGS.items():
        logger.info(f"\n{'='*70}")
        logger.info(f"  CONFIG: {config_name} — {cfg['desc']}")
        logger.info(f"  Features: {cfg['cols'] or 'None'}")
        logger.info(f"{'='*70}")
        
        run_outdir = os.path.join(outdir, config_name)
        os.makedirs(run_outdir, exist_ok=True)
        
        t0 = time.time()
        
        clf = SmilesXClassifier(
            data=df,
            smiles_col='smiles',
            label_col='bin_class',
            extra_feature_cols=cfg['cols'] if cfg['cols'] else None,
            embed_dim=512,
            lstm_units=128,
            tdense_units=128,
            dense_depth=cfg['dense_depth'],
            dropout=0.3,
            lr=1e-4,
            weight_decay=1e-4,
            batch_size=16,
            n_epochs=100,
            patience=25,
            class_weight=True,
            outdir=run_outdir,
            device=device,
            seed=42,
        )
        
        cv_result = clf.cross_validate(n_folds=5, augment=True)
        elapsed = time.time() - t0
        
        results[config_name] = {
            'desc': cfg['desc'],
            'n_features': len(cfg['cols']),
            'features': cfg['cols'],
            'dense_depth': cfg['dense_depth'],
            'mean_f1': cv_result.mean_f1,
            'std_f1': cv_result.std_f1,
            'mean_auc': cv_result.mean_auc,
            'std_auc': cv_result.std_auc,
            'elapsed_sec': elapsed,
            'folds': [
                {
                    'fold': f.fold,
                    'f1': f.f1,
                    'auc_roc': f.auc_roc,
                    'auc_pr': f.auc_pr,
                    'accuracy': f.accuracy,
                    'precision': f.precision,
                    'recall': f.recall,
                    'threshold': f.threshold,
                }
                for f in cv_result.folds
            ],
        }
        
        logger.info(f"  → F1={cv_result.mean_f1:.4f}±{cv_result.std_f1:.4f}  "
                     f"AUC={cv_result.mean_auc:.4f}±{cv_result.std_auc:.4f}  "
                     f"({elapsed:.0f}s)")
    
    # Comparison table
    print(f"\n{'='*80}")
    print(f"  COMPARISON SUMMARY")
    print(f"{'='*80}")
    print(f"  {'Config':<20s} {'#Feat':>5s} {'F1':>12s} {'AUC-ROC':>14s} {'Time':>8s}")
    print(f"  {'-'*20} {'-'*5} {'-'*12} {'-'*14} {'-'*8}")
    
    for name, r in results.items():
        print(f"  {name:<20s} {r['n_features']:>5d} "
              f"{r['mean_f1']:.4f}±{r['std_f1']:.4f} "
              f"{r['mean_auc']:.4f}±{r['std_auc']:.4f} "
              f"{r['elapsed_sec']:>6.0f}s")
    
    print(f"  {'-'*20} {'-'*5} {'-'*12} {'-'*14} {'-'*8}")
    print(f"  Paper target:              0.80          0.88")
    print(f"{'='*80}")
    
    summary_path = os.path.join(outdir, 'comparison_results.json')
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"\nFull results saved to {summary_path}")
    
    return results


if __name__ == '__main__':
    os.chdir('/home/stevens/pvmol-gen')
    run_comparison(
        data_path='data/T0_enriched.csv',
        outdir='results/feature_comparison',
        device='cuda',
    )
