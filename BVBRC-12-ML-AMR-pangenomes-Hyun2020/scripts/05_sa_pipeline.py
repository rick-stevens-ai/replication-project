#!/usr/bin/env python3
"""
Complete pipeline for S. aureus: pan-genome features → SVM-RSE → evaluation.
Optimized single-organism version for the full replication.
"""

import os
import sys
import json
import hashlib
import numpy as np
from collections import defaultdict
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

CORE_THRESHOLD = 10
N_SVMS = 500
GENOME_FRAC = 0.8
FEATURE_FRAC = 0.5


def parse_clusters(clstr_file):
    """Parse CD-Hit cluster file."""
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
                seq_id = after_gt.split('...')[0].split()[0].rstrip('.')
                
                if 'fig|' in seq_id:
                    inner = seq_id.replace('fig|', '')
                    genome_id = None
                    for sep in ['.peg.', '.rna.', '.repeat.']:
                        if sep in inner:
                            genome_id = inner.split(sep)[0]
                            break
                    if genome_id is None:
                        genome_id = inner
                else:
                    genome_id = 'unknown'
                
                clusters[current].append({
                    'seq_id': seq_id,
                    'genome_id': genome_id,
                })
    return clusters


def load_protein_sequences(org_name, genome_ids):
    """Load all protein sequences indexed by PATRIC ID."""
    prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
    sequences = {}  # seq_id -> (genome_id, seq)
    
    for gid in genome_ids:
        fpath = os.path.join(prot_dir, f'{gid}.faa')
        if not os.path.exists(fpath):
            continue
        
        current_id = None
        current_seq = []
        
        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_id and current_seq:
                        seq = ''.join(current_seq)
                        sequences[current_id] = (gid, seq)
                    
                    # Parse header: >fig|GENOME.peg.N|LOCUS| description
                    header = line[1:]
                    parts = header.split('|')
                    if len(parts) >= 2:
                        current_id = f"fig|{parts[1]}"
                    else:
                        current_id = header.split()[0]
                    current_seq = []
                else:
                    current_seq.append(line)
        
        if current_id and current_seq:
            seq = ''.join(current_seq)
            sequences[current_id] = (gid, seq)
    
    return sequences


def build_feature_matrix(clusters, genome_ids, sequences, n_genomes):
    """Build binary feature matrix with allele-level core genes."""
    
    # Map seq_id from cluster to sequence
    # Build a lookup from CD-Hit seq_ids to our loaded seq_ids
    # CD-Hit uses: fig|1280.15931.peg.2071|C3B39_10435
    # Our keys: fig|1280.15931.peg.2071
    cdhit_to_our = {}
    for cdhit_id_full in [m['seq_id'] for c in clusters.values() for m in c]:
        # Try exact match first
        if cdhit_id_full in sequences:
            cdhit_to_our[cdhit_id_full] = cdhit_id_full
        else:
            # CD-Hit ID might be: fig|1280.15931.peg.2071|C3B39_10435
            # Our ID is: fig|1280.15931.peg.2071
            parts = cdhit_id_full.split('|')
            if len(parts) >= 2:
                short_id = f"fig|{parts[1]}"
                if short_id in sequences:
                    cdhit_to_our[cdhit_id_full] = short_id
    
    print(f"  Mapped {len(cdhit_to_our)}/{sum(len(c) for c in clusters.values())} "
          f"cluster members to sequences")
    
    # Classify clusters and identify alleles
    genome_idx = {gid: i for i, gid in enumerate(genome_ids)}
    
    feature_list = []  # (name, type)
    feature_data = []  # list of sets of genome indices that have this feature
    
    core_genes = 0
    acc_genes = 0
    unique_genes = 0
    total_alleles = 0
    
    for cid, members in sorted(clusters.items()):
        genomes_present = set(m['genome_id'] for m in members if m['genome_id'] in genome_idx)
        n_present = len(genomes_present)
        n_missing = n_genomes - n_present
        
        if n_missing <= CORE_THRESHOLD:
            # Core gene: allele-level features
            core_genes += 1
            
            # Group members by unique amino acid sequence
            allele_genomes = defaultdict(set)  # seq_hash -> set of genome_ids
            for m in members:
                gid = m['genome_id']
                if gid not in genome_idx:
                    continue
                our_id = cdhit_to_our.get(m['seq_id'])
                if our_id and our_id in sequences:
                    seq = sequences[our_id][1]
                    seq_hash = hashlib.md5(seq.encode()).hexdigest()[:16]
                    allele_genomes[seq_hash].add(gid)
                else:
                    # Can't find sequence — use genome presence as fallback
                    allele_genomes['_unknown_' + gid].add(gid)
            
            for allele_idx, (seq_hash, gids) in enumerate(allele_genomes.items()):
                if seq_hash.startswith('_unknown_'):
                    continue
                feature_list.append((f"C{cid}_a{allele_idx}", 'core_allele'))
                genome_set = {genome_idx[g] for g in gids if g in genome_idx}
                feature_data.append(genome_set)
                total_alleles += 1
        
        elif n_present <= CORE_THRESHOLD:
            # Unique gene: skip (too rare)
            unique_genes += 1
        
        else:
            # Accessory gene: gene-level presence/absence
            acc_genes += 1
            feature_list.append((f"C{cid}", 'accessory'))
            genome_set = {genome_idx[g] for g in genomes_present}
            feature_data.append(genome_set)
    
    print(f"  Core genes: {core_genes} ({total_alleles} alleles)")
    print(f"  Accessory genes: {acc_genes}")
    print(f"  Unique genes: {unique_genes} (excluded)")
    print(f"  Total features: {len(feature_list)}")
    
    # Build sparse matrix
    rows, cols, vals = [], [], []
    for j, gset in enumerate(feature_data):
        for gi in gset:
            rows.append(gi)
            cols.append(j)
            vals.append(1)
    
    X = sparse.csr_matrix((vals, (rows, cols)),
                          shape=(len(genome_ids), len(feature_list)),
                          dtype=np.int8)
    
    feature_names = [f[0] for f in feature_list]
    feature_types = [f[1] for f in feature_list]
    
    return X, feature_names, feature_types


def load_amr_phenotypes(org_name, genome_ids, antibiotic):
    """Load AMR phenotypes, binarized as 0=S, 1=R/I."""
    amr_file = os.path.join(DATA_DIR, f'{org_name}_amr_raw.json')
    with open(amr_file) as f:
        records = json.load(f)
    
    phenotypes = {}
    for rec in records:
        if rec.get('antibiotic', '').lower() == antibiotic.lower():
            gid = rec.get('genome_id')
            pheno = rec.get('resistant_phenotype', '')
            if pheno == 'Susceptible':
                if gid not in phenotypes:  # Don't overwrite R with S
                    phenotypes[gid] = 0
            elif pheno in ('Resistant', 'Intermediate'):
                phenotypes[gid] = 1
    
    y = np.full(len(genome_ids), -1, dtype=int)
    for i, gid in enumerate(genome_ids):
        if gid in phenotypes:
            y[i] = phenotypes[gid]
    
    mask = y >= 0
    return y, mask


def train_svm_rse(X, y, n_svms=N_SVMS, seed=42):
    """Train SVM-RSE and return feature weights."""
    rng = np.random.RandomState(seed)
    n_samples, n_features = X.shape
    
    weights = np.zeros(n_features)
    counts = np.zeros(n_features)
    trained = 0
    
    X_dense = X.toarray()
    
    for i in range(n_svms):
        n_s = int(n_samples * GENOME_FRAC)
        s_idx = rng.choice(n_samples, n_s, replace=False)
        n_f = int(n_features * FEATURE_FRAC)
        f_idx = rng.choice(n_features, n_f, replace=False)
        
        X_tr = X_dense[np.ix_(s_idx, f_idx)]
        y_tr = y[s_idx]
        
        if len(np.unique(y_tr)) < 2:
            continue
        
        try:
            svm = LinearSVC(
                penalty='l1', loss='squared_hinge', dual=False,
                class_weight='balanced', max_iter=10000, random_state=i, C=1.0
            )
            svm.fit(X_tr, y_tr)
            w = svm.coef_[0]
            weights[f_idx] += w
            counts[f_idx] += 1
            trained += 1
        except Exception as e:
            continue
        
        if (i + 1) % 100 == 0:
            print(f"    Trained {i+1}/{n_svms} SVMs ({trained} successful)")
            sys.stdout.flush()
    
    mask = counts > 0
    avg_w = np.zeros(n_features)
    avg_w[mask] = weights[mask] / counts[mask]
    
    print(f"    Total trained: {trained}/{n_svms}")
    return avg_w


def cv_evaluate(X, y, n_folds=5, n_svms_per_fold=100, seed=42):
    """5-fold cross validation."""
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    
    results = {'accuracy': [], 'mcc': [], 'precision': [], 'recall': [], 'auroc': []}
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        rng = np.random.RandomState(seed + fold * 1000)
        X_tr_full = X[train_idx].toarray()
        y_tr = y[train_idx]
        X_te_full = X[test_idx].toarray()
        y_te = y[test_idx]
        
        n_train, n_feat = X_tr_full.shape
        votes = np.zeros((len(test_idx), 2))
        dvals = np.zeros(len(test_idx))
        n_valid = 0
        
        for i in range(n_svms_per_fold):
            n_s = int(n_train * GENOME_FRAC)
            s_idx = rng.choice(n_train, n_s, replace=False)
            n_f = int(n_feat * FEATURE_FRAC)
            f_idx = rng.choice(n_feat, n_f, replace=False)
            
            X_tr_s = X_tr_full[np.ix_(s_idx, f_idx)]
            y_tr_s = y_tr[s_idx]
            
            if len(np.unique(y_tr_s)) < 2:
                continue
            
            try:
                svm = LinearSVC(
                    penalty='l1', loss='squared_hinge', dual=False,
                    class_weight='balanced', max_iter=10000, random_state=i, C=1.0
                )
                svm.fit(X_tr_s, y_tr_s)
                
                X_te_s = X_te_full[:, f_idx]
                preds = svm.predict(X_te_s)
                dv = svm.decision_function(X_te_s)
                
                for j, (p, d) in enumerate(zip(preds, dv)):
                    votes[j, int(p)] += 1
                    dvals[j] += d
                n_valid += 1
            except:
                continue
        
        if n_valid == 0:
            print(f"    Fold {fold+1}: No valid SVMs!")
            continue
        
        y_pred = np.argmax(votes, axis=1)
        dvals /= n_valid
        
        acc = accuracy_score(y_te, y_pred)
        mcc = matthews_corrcoef(y_te, y_pred)
        prec = precision_score(y_te, y_pred, zero_division=0)
        rec = recall_score(y_te, y_pred, zero_division=0)
        try:
            auc = roc_auc_score(y_te, dvals)
        except ValueError:
            auc = 0.5
        
        results['accuracy'].append(acc)
        results['mcc'].append(mcc)
        results['precision'].append(prec)
        results['recall'].append(rec)
        results['auroc'].append(auc)
        
        print(f"    Fold {fold+1}: acc={acc:.3f}, mcc={mcc:.3f}, "
              f"prec={prec:.3f}, rec={rec:.3f}, auroc={auc:.3f} "
              f"(R={sum(y_te==1)}, S={sum(y_te==0)}, svms={n_valid})")
        sys.stdout.flush()
    
    return {k: (float(np.mean(v)), float(np.std(v))) for k, v in results.items()}


def main():
    org_name = 'S_aureus'
    
    # Antibiotics from paper
    antibiotics = [
        'ciprofloxacin', 'clindamycin', 'erythromycin',
        'gentamicin', 'tetracycline', 'trimethoprim/sulfamethoxazole'
    ]
    
    genome_ids_file = os.path.join(DATA_DIR, 'sa_genome_ids.txt')
    with open(genome_ids_file) as f:
        genome_ids = [l.strip() for l in f if l.strip()]
    
    # Filter to available genomes
    prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
    genome_ids = [gid for gid in genome_ids 
                  if os.path.exists(os.path.join(prot_dir, f'{gid}.faa'))
                  and os.path.getsize(os.path.join(prot_dir, f'{gid}.faa')) > 100]
    
    print(f"S. aureus: {len(genome_ids)} genomes with protein data")
    
    # Parse CD-Hit clusters
    print("Parsing CD-Hit clusters...")
    clusters = parse_clusters(os.path.join(RESULTS_DIR, 'S_aureus_cdhit.clstr'))
    print(f"  Total clusters: {len(clusters)}")
    
    # Load protein sequences
    print("Loading protein sequences...")
    sequences = load_protein_sequences(org_name, genome_ids)
    print(f"  Total sequences loaded: {len(sequences)}")
    
    # Build feature matrix
    print("Building feature matrix...")
    X, feature_names, feature_types = build_feature_matrix(
        clusters, genome_ids, sequences, len(genome_ids)
    )
    print(f"  Matrix shape: {X.shape}")
    
    # Process each antibiotic
    all_results = {}
    
    for antibiotic in antibiotics:
        print(f"\n{'='*60}")
        print(f"S. aureus vs {antibiotic}")
        print('='*60)
        
        y, mask = load_amr_phenotypes(org_name, genome_ids, antibiotic)
        n_data = mask.sum()
        n_r = (y[mask] == 1).sum()
        n_s = (y[mask] == 0).sum()
        
        if n_data < 20 or min(n_r, n_s) < 5:
            print(f"  Insufficient data: {n_data} genomes (R={n_r}, S={n_s}), skipping")
            continue
        
        print(f"  Genomes: {n_data} (R={n_r}, S={n_s})")
        
        X_case = X[mask]
        y_case = y[mask]
        
        # Train SVM-RSE for feature ranking
        print("  Training SVM-RSE...")
        weights = train_svm_rse(X_case, y_case, n_svms=500)
        
        # Top resistance features
        top_idx = np.argsort(weights)[::-1][:50]
        print(f"\n  Top 10 resistance-associated features:")
        for rank, idx in enumerate(top_idx[:10]):
            print(f"    {rank+1}. {feature_names[idx]} (w={weights[idx]:.4f})")
        
        # 5-fold CV (use fewer SVMs per fold for speed)
        print(f"\n  5-fold cross validation (100 SVMs/fold)...")
        cv_res = cv_evaluate(X_case, y_case, n_folds=5, n_svms_per_fold=100)
        
        print(f"\n  CV Summary:")
        for metric, (mean, std) in cv_res.items():
            print(f"    {metric}: {mean:.3f} ± {std:.3f}")
        
        all_results[antibiotic] = {
            'n_genomes': int(n_data),
            'n_resistant': int(n_r),
            'n_susceptible': int(n_s),
            'cv_metrics': cv_res,
            'top_50_features': [
                {'rank': r+1, 'name': feature_names[idx], 'weight': float(weights[idx])}
                for r, idx in enumerate(top_idx)
            ]
        }
    
    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, 'S_aureus_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n\nAll results saved!")


if __name__ == '__main__':
    main()
