#!/usr/bin/env python3
"""
Full replication pipeline for Hyun et al. 2020.
Builds pan-genome feature matrices and runs SVM-RSE for all organisms.
"""

import os
import sys
import json
import hashlib
import time
import numpy as np
from collections import defaultdict, Counter
from scipy import sparse
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (accuracy_score, matthews_corrcoef,
                              precision_score, recall_score, roc_auc_score)
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Paper parameters
CDHIT_IDENTITY = 0.8
CDHIT_WORD = 5
CORE_THRESHOLD = 10   # Missing in <=10 genomes = core
N_SVMS = 500          # Paper: 500 SVMs
GENOME_FRAC = 0.8     # Paper: 80% of genomes
FEATURE_FRAC = 0.5    # Paper: 50% of features
N_FOLDS = 5           # Paper: 5-fold CV


# ========== CLUSTER PARSING ==========

def parse_cdhit_clusters(clstr_file):
    """Parse CD-Hit .clstr file. Returns dict: cluster_id -> list of members."""
    clusters = {}
    current = None
    with open(clstr_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>Cluster'):
                current = int(line.split()[1])
                clusters[current] = []
            elif current is not None and '>' in line:
                parts = line.split('>')
                if len(parts) < 2:
                    continue
                after_gt = parts[1]
                seq_id = after_gt.split('...')[0].strip()
                
                # Extract genome ID from PATRIC feature ID
                genome_id = extract_genome_id(seq_id)
                is_rep = line.rstrip().endswith('*')
                
                clusters[current].append({
                    'seq_id': seq_id,
                    'genome_id': genome_id,
                    'is_rep': is_rep,
                })
    return clusters


def extract_genome_id(seq_id):
    """Extract genome ID from a PATRIC feature ID like fig|1280.15931.peg.2071|..."""
    if 'fig|' in seq_id:
        inner = seq_id.split('fig|')[1]
        # Remove trailing pipe-delimited fields
        inner = inner.split('|')[0]
        for sep in ['.peg.', '.rna.', '.repeat.', '.CDS.', '.trna.']:
            if sep in inner:
                return inner.split(sep)[0]
        return inner
    return 'unknown'


# ========== PROTEIN LOADING ==========

def load_protein_sequences(protein_dir, genome_ids):
    """Load all protein sequences from per-genome FASTA files.
    Returns dict: seq_id -> (genome_id, amino_acid_sequence)
    """
    sequences = {}
    loaded = 0
    missing = 0
    
    for gid in genome_ids:
        fpath = os.path.join(protein_dir, f'{gid}.faa')
        if not os.path.exists(fpath):
            missing += 1
            continue
        
        current_id = None
        current_seq = []
        
        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_id and current_seq:
                        sequences[current_id] = (gid, ''.join(current_seq))
                        loaded += 1
                    # Parse: >fig|1280.15931.peg.2071|C3B39_10435| Description
                    header = line[1:].strip()
                    # Use full ID including all pipe-delimited parts up to space
                    full_id = header.split()[0].rstrip('|')
                    # Also store a short version for matching
                    current_id = full_id
                    current_seq = []
                else:
                    current_seq.append(line)
        
        if current_id and current_seq:
            sequences[current_id] = (gid, ''.join(current_seq))
            loaded += 1
    
    print(f"  Loaded {loaded} protein sequences from {len(genome_ids)-missing}/{len(genome_ids)} genomes")
    if missing > 0:
        print(f"  ({missing} genome files not found)")
    return sequences


def build_seq_id_lookup(sequences, clusters):
    """Build a lookup from CD-Hit seq_ids to our loaded seq_ids.
    
    CD-Hit might use slightly different ID formats. We try:
    1. Exact match
    2. Match by removing trailing pipe-delimited fields
    3. Match using just fig|GENOME.peg.N format
    """
    # Build index of our loaded IDs
    # Keys in sequences dict are full header IDs
    seq_keys = set(sequences.keys())
    
    # Also build an index by short form: fig|GENOME.peg.N
    short_to_full = {}
    for full_id in seq_keys:
        parts = full_id.split('|')
        if len(parts) >= 2 and parts[0] == 'fig':
            short = f"fig|{parts[1]}"
            short_to_full[short] = full_id
    
    lookup = {}
    all_cdhit_ids = set()
    for cid, members in clusters.items():
        for m in members:
            sid = m['seq_id']
            all_cdhit_ids.add(sid)
            
            if sid in seq_keys:
                lookup[sid] = sid
            else:
                # Try stripping to just fig|GENOME.peg.N
                parts = sid.split('|')
                if len(parts) >= 2 and parts[0] == 'fig':
                    short = f"fig|{parts[1]}"
                    if short in short_to_full:
                        lookup[sid] = short_to_full[short]
                    elif short in seq_keys:
                        lookup[sid] = short
    
    print(f"  Matched {len(lookup)}/{len(all_cdhit_ids)} cluster member IDs to sequences")
    return lookup


# ========== FEATURE MATRIX ==========

def build_feature_matrix(clusters, genome_ids, sequences, seq_lookup):
    """Build binary feature matrix following the paper's approach:
    - Core genes (missing ≤10): allele-level features (each unique AA seq = one feature)
    - Accessory genes: binary presence/absence
    - Unique genes (present ≤10): excluded
    """
    n_genomes = len(genome_ids)
    genome_idx = {gid: i for i, gid in enumerate(genome_ids)}
    
    feature_names = []
    feature_types = []
    feature_data = []  # list of (set of genome indices)
    
    stats = {'core': 0, 'accessory': 0, 'unique': 0, 'core_alleles': 0}
    
    for cid in sorted(clusters.keys()):
        members = clusters[cid]
        genomes_in_cluster = set(m['genome_id'] for m in members if m['genome_id'] in genome_idx)
        n_present = len(genomes_in_cluster)
        n_missing = n_genomes - n_present
        
        if n_missing <= CORE_THRESHOLD:
            # CORE gene: allele-level features
            stats['core'] += 1
            
            # Group by unique amino acid sequence
            allele_genomes = defaultdict(set)
            for m in members:
                gid = m['genome_id']
                if gid not in genome_idx:
                    continue
                our_id = seq_lookup.get(m['seq_id'])
                if our_id and our_id in sequences:
                    seq = sequences[our_id][1]
                    # Hash the sequence for grouping
                    seq_hash = hashlib.md5(seq.encode()).hexdigest()[:16]
                    allele_genomes[seq_hash].add(gid)
            
            for ai, (shash, gids) in enumerate(allele_genomes.items()):
                feature_names.append(f"core{cid}_allele{ai}")
                feature_types.append('core_allele')
                feature_data.append({genome_idx[g] for g in gids if g in genome_idx})
                stats['core_alleles'] += 1
        
        elif n_present <= CORE_THRESHOLD:
            # UNIQUE gene: skip
            stats['unique'] += 1
        
        else:
            # ACCESSORY gene: presence/absence
            stats['accessory'] += 1
            feature_names.append(f"acc{cid}")
            feature_types.append('accessory')
            feature_data.append({genome_idx[g] for g in genomes_in_cluster})
    
    # Build sparse matrix
    rows, cols, vals = [], [], []
    for j, gset in enumerate(feature_data):
        for gi in gset:
            rows.append(gi)
            cols.append(j)
            vals.append(1)
    
    n_features = len(feature_names)
    X = sparse.csr_matrix((vals, (rows, cols)),
                          shape=(n_genomes, n_features), dtype=np.float32)
    
    print(f"  Core genes: {stats['core']} ({stats['core_alleles']} alleles)")
    print(f"  Accessory genes: {stats['accessory']}")
    print(f"  Unique genes: {stats['unique']} (excluded)")
    print(f"  Total features: {n_features}")
    print(f"  Matrix shape: {X.shape}, nnz: {X.nnz}")
    
    return X, feature_names, feature_types, stats


# ========== AMR LABELS ==========

def load_amr_labels(amr_file, genome_ids, antibiotic):
    """Load AMR phenotype labels for a specific antibiotic.
    Returns (y, mask) where y is 0=S, 1=R/I, and mask indicates valid labels.
    """
    with open(amr_file) as f:
        records = json.load(f)
    
    # Collect phenotypes per genome
    gid_pheno = {}
    for rec in records:
        abx = rec.get('antibiotic', '').lower().strip()
        if abx != antibiotic.lower().strip():
            continue
        
        gid = str(rec.get('genome_id', ''))
        pheno = rec.get('resistant_phenotype', '').strip()
        
        if pheno == 'Resistant' or pheno == 'Intermediate':
            gid_pheno[gid] = 1  # R/I overrides S
        elif pheno == 'Susceptible' and gid not in gid_pheno:
            gid_pheno[gid] = 0
    
    y = np.full(len(genome_ids), -1, dtype=int)
    for i, gid in enumerate(genome_ids):
        if gid in gid_pheno:
            y[i] = gid_pheno[gid]
    
    mask = y >= 0
    return y, mask


# ========== SVM-RSE ==========

def train_svm_rse(X, y, n_svms=N_SVMS, seed=42):
    """Train SVM-RSE ensemble and return averaged feature weights.
    
    Paper: 500 SVMs, each using 80% of genomes and 50% of features.
    SVM: LinearSVC with L1 penalty, squared hinge loss, class_weight='balanced'.
    """
    rng = np.random.RandomState(seed)
    n_samples, n_features = X.shape
    
    # Work with dense for subsetting efficiency
    X_dense = X.toarray() if sparse.issparse(X) else X
    
    weight_sum = np.zeros(n_features)
    weight_count = np.zeros(n_features)
    trained = 0
    
    for i in range(n_svms):
        # Random subspace: 80% genomes, 50% features
        n_s = max(10, int(n_samples * GENOME_FRAC))
        n_f = max(10, int(n_features * FEATURE_FRAC))
        
        s_idx = rng.choice(n_samples, n_s, replace=False)
        f_idx = rng.choice(n_features, n_f, replace=False)
        
        X_sub = X_dense[np.ix_(s_idx, f_idx)]
        y_sub = y[s_idx]
        
        # Need both classes
        if len(np.unique(y_sub)) < 2:
            continue
        
        try:
            svm = LinearSVC(
                penalty='l1', loss='squared_hinge', dual=False,
                class_weight='balanced', max_iter=10000,
                random_state=i, C=1.0
            )
            svm.fit(X_sub, y_sub)
            
            w = svm.coef_[0]
            weight_sum[f_idx] += w
            weight_count[f_idx] += 1
            trained += 1
        except Exception:
            continue
        
        if (i + 1) % 100 == 0:
            print(f"    Trained {i+1}/{n_svms} ({trained} successful)")
            sys.stdout.flush()
    
    # Average weights
    mask = weight_count > 0
    avg_weights = np.zeros(n_features)
    avg_weights[mask] = weight_sum[mask] / weight_count[mask]
    
    print(f"    Final: {trained}/{n_svms} SVMs converged")
    return avg_weights


def cv_evaluate(X, y, n_folds=N_FOLDS, n_svms_per_fold=100, seed=42):
    """5-fold stratified CV with SVM-RSE ensemble.
    
    Uses fewer SVMs per fold for speed (100 vs 500).
    """
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    
    metrics = {k: [] for k in ['accuracy', 'mcc', 'precision', 'recall', 'auroc']}
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        rng = np.random.RandomState(seed + fold * 1000)
        
        if sparse.issparse(X):
            X_train = X[train_idx].toarray()
            X_test = X[test_idx].toarray()
        else:
            X_train = X[train_idx]
            X_test = X[test_idx]
        
        y_train = y[train_idx]
        y_test = y[test_idx]
        
        n_train, n_feat = X_train.shape
        
        # Ensemble predictions
        decision_sum = np.zeros(len(test_idx))
        vote_counts = np.zeros((len(test_idx), 2))
        n_valid = 0
        
        for i in range(n_svms_per_fold):
            n_s = max(10, int(n_train * GENOME_FRAC))
            n_f = max(10, int(n_feat * FEATURE_FRAC))
            
            s_idx = rng.choice(n_train, n_s, replace=False)
            f_idx = rng.choice(n_feat, n_f, replace=False)
            
            X_tr_s = X_train[np.ix_(s_idx, f_idx)]
            y_tr_s = y_train[s_idx]
            
            if len(np.unique(y_tr_s)) < 2:
                continue
            
            try:
                svm = LinearSVC(
                    penalty='l1', loss='squared_hinge', dual=False,
                    class_weight='balanced', max_iter=10000,
                    random_state=i, C=1.0
                )
                svm.fit(X_tr_s, y_tr_s)
                
                X_te_s = X_test[:, f_idx]
                preds = svm.predict(X_te_s)
                dv = svm.decision_function(X_te_s)
                
                for j, (p, d) in enumerate(zip(preds, dv)):
                    vote_counts[j, int(p)] += 1
                    decision_sum[j] += d
                n_valid += 1
            except Exception:
                continue
        
        if n_valid == 0:
            print(f"    Fold {fold+1}: No valid SVMs!")
            continue
        
        y_pred = np.argmax(vote_counts, axis=1)
        avg_decision = decision_sum / n_valid
        
        acc = accuracy_score(y_test, y_pred)
        mcc = matthews_corrcoef(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        
        try:
            auc = roc_auc_score(y_test, avg_decision)
        except ValueError:
            auc = 0.5
        
        metrics['accuracy'].append(acc)
        metrics['mcc'].append(mcc)
        metrics['precision'].append(prec)
        metrics['recall'].append(rec)
        metrics['auroc'].append(auc)
        
        print(f"    Fold {fold+1}: acc={acc:.3f} mcc={mcc:.3f} "
              f"prec={prec:.3f} rec={rec:.3f} auc={auc:.3f} "
              f"[R={sum(y_test==1)}, S={sum(y_test==0)}, svms={n_valid}]")
        sys.stdout.flush()
    
    return {k: (float(np.mean(v)), float(np.std(v))) for k, v in metrics.items() if v}


# ========== MAIN PIPELINE ==========

def run_organism(org_key, org_name, genome_ids_file, amr_file, protein_dir,
                 clstr_file, antibiotics):
    """Run full pipeline for one organism."""
    
    print(f"\n{'#'*70}")
    print(f"# {org_name}")
    print(f"{'#'*70}")
    
    # Load genome IDs
    with open(genome_ids_file) as f:
        genome_ids = [l.strip() for l in f if l.strip()]
    
    # Filter to genomes with protein data
    genome_ids = [gid for gid in genome_ids
                  if os.path.exists(os.path.join(protein_dir, f'{gid}.faa'))
                  and os.path.getsize(os.path.join(protein_dir, f'{gid}.faa')) > 100]
    
    print(f"\nGenomes with protein data: {len(genome_ids)}")
    
    if not os.path.exists(clstr_file):
        print(f"ERROR: CD-HIT cluster file not found: {clstr_file}")
        return None
    
    # 1. Parse clusters
    print("\n--- Parsing CD-HIT clusters ---")
    clusters = parse_cdhit_clusters(clstr_file)
    print(f"  Total clusters: {len(clusters)}")
    
    # 2. Load protein sequences
    print("\n--- Loading protein sequences ---")
    sequences = load_protein_sequences(protein_dir, genome_ids)
    
    # 3. Build sequence ID lookup
    print("\n--- Building ID lookup ---")
    seq_lookup = build_seq_id_lookup(sequences, clusters)
    
    # 4. Build feature matrix
    print("\n--- Building feature matrix ---")
    X, feature_names, feature_types, gene_stats = build_feature_matrix(
        clusters, genome_ids, sequences, seq_lookup
    )
    
    # 5. Run ML for each antibiotic
    all_results = {}
    
    for antibiotic in antibiotics:
        print(f"\n{'='*60}")
        print(f"{org_name} vs {antibiotic}")
        print(f"{'='*60}")
        
        y, mask = load_amr_labels(amr_file, genome_ids, antibiotic)
        n_labeled = mask.sum()
        n_r = (y[mask] == 1).sum()
        n_s = (y[mask] == 0).sum()
        
        print(f"  Labeled genomes: {n_labeled} (R={n_r}, S={n_s})")
        
        if n_labeled < 20 or min(n_r, n_s) < 5:
            print(f"  SKIPPING — insufficient data")
            continue
        
        X_case = X[mask]
        y_case = y[mask]
        
        # Remove zero-variance features for this subset
        feat_var = np.array(X_case.sum(axis=0)).flatten()
        nonzero = (feat_var > 0) & (feat_var < n_labeled)
        X_case = X_case[:, nonzero]
        active_names = [feature_names[i] for i, nz in enumerate(nonzero) if nz]
        print(f"  Active features: {X_case.shape[1]} (removed {sum(~nonzero)} constant)")
        
        # Train full SVM-RSE for feature ranking
        print("\n  --- Training SVM-RSE (500 SVMs) ---")
        t0 = time.time()
        weights = train_svm_rse(X_case, y_case, n_svms=500)
        dt = time.time() - t0
        print(f"    Time: {dt:.1f}s")
        
        # Top 50 features
        top_idx = np.argsort(np.abs(weights))[::-1][:50]
        print(f"\n  Top 10 features (by |weight|):")
        for rank, idx in enumerate(top_idx[:10]):
            print(f"    {rank+1}. {active_names[idx]} (w={weights[idx]:.4f})")
        
        # 5-fold CV
        print(f"\n  --- 5-fold Cross Validation (100 SVMs/fold) ---")
        t0 = time.time()
        cv_results = cv_evaluate(X_case, y_case, n_folds=5, n_svms_per_fold=100)
        dt = time.time() - t0
        print(f"    CV time: {dt:.1f}s")
        
        print(f"\n  Results:")
        for metric, (mean, std) in cv_results.items():
            print(f"    {metric}: {mean:.3f} ± {std:.3f}")
        
        all_results[antibiotic] = {
            'n_genomes': int(n_labeled),
            'n_resistant': int(n_r),
            'n_susceptible': int(n_s),
            'n_features': int(X_case.shape[1]),
            'cv_metrics': cv_results,
            'top_50': [
                {'rank': r+1, 'feature': active_names[idx], 'weight': float(weights[idx])}
                for r, idx in enumerate(top_idx)
            ]
        }
    
    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_file = os.path.join(RESULTS_DIR, f'{org_key}_results.json')
    with open(out_file, 'w') as f:
        json.dump({
            'organism': org_name,
            'n_genomes': len(genome_ids),
            'gene_stats': gene_stats,
            'antibiotics': all_results
        }, f, indent=2)
    
    print(f"\n  Results saved: {out_file}")
    return all_results


def main():
    # === S. aureus ===
    sa_results = run_organism(
        org_key='S_aureus',
        org_name='Staphylococcus aureus',
        genome_ids_file=os.path.join(DATA_DIR, 'sa_genome_ids.txt'),
        amr_file=os.path.join(DATA_DIR, 'S_aureus_amr_raw.json'),
        protein_dir=os.path.join(DATA_DIR, 'S_aureus_proteins'),
        clstr_file=os.path.join(RESULTS_DIR, 'S_aureus_cdhit.clstr'),
        antibiotics=[
            'ciprofloxacin', 'clindamycin', 'erythromycin',
            'gentamicin', 'tetracycline', 'trimethoprim/sulfamethoxazole'
        ]
    )
    
    # === P. aeruginosa ===
    pa_clstr = os.path.join(RESULTS_DIR, 'P_aeruginosa_cdhit.clstr')
    if os.path.exists(pa_clstr):
        pa_results = run_organism(
            org_key='P_aeruginosa',
            org_name='Pseudomonas aeruginosa',
            genome_ids_file=os.path.join(DATA_DIR, 'pa_genome_ids.txt'),
            amr_file=os.path.join(DATA_DIR, 'P_aeruginosa_amr_raw.json'),
            protein_dir=os.path.join(DATA_DIR, 'P_aeruginosa_proteins'),
            clstr_file=pa_clstr,
            antibiotics=['amikacin', 'ceftazidime', 'levofloxacin', 'meropenem']
        )
    else:
        print(f"\nP. aeruginosa: Cluster file not found, skipping.")
        pa_results = None
    
    # === E. coli ===
    ec_clstr = os.path.join(RESULTS_DIR, 'E_coli_cdhit.clstr')
    if os.path.exists(ec_clstr):
        ec_results = run_organism(
            org_key='E_coli',
            org_name='Escherichia coli',
            genome_ids_file=os.path.join(DATA_DIR, 'ec_genome_ids.txt'),
            amr_file=os.path.join(DATA_DIR, 'E_coli_amr_raw.json'),
            protein_dir=os.path.join(DATA_DIR, 'E_coli_proteins'),
            clstr_file=ec_clstr,
            antibiotics=[
                'amoxicillin/clavulanic acid', 'ceftazidime', 'ciprofloxacin',
                'gentamicin', 'imipenem', 'trimethoprim'
            ]
        )
    else:
        print(f"\nE. coli: Cluster file not found, skipping.")
        ec_results = None
    
    print(f"\n\n{'#'*70}")
    print("# PIPELINE COMPLETE")
    print(f"{'#'*70}")


if __name__ == '__main__':
    main()
