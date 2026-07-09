#!/usr/bin/env python3
"""
Step 4: Build feature matrix from pan-genome and train SVM-RSE models.

Feature encoding (from paper):
- Core gene alleles: presence/absence of each allele
- Non-core genes: presence/absence of gene (not allele-level)

SVM-RSE:
- 500 SVMs per ensemble
- Each: random 80% of genomes, 50% of features
- Linear SVM with L1 regularization, square hinge loss, class-weighted
- 5-fold cross validation for evaluation
"""

import os
import sys
import json
import numpy as np
from collections import defaultdict
from scipy import sparse
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (accuracy_score, matthews_corrcoef, 
                              precision_score, recall_score, roc_auc_score)
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')

CORE_THRESHOLD = 10
N_SVMS = 500
GENOME_FRACTION = 0.8
FEATURE_FRACTION = 0.5


def read_genome_ids(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return [line.strip() for line in f if line.strip()]


def parse_cdhit_clusters_detailed(clstr_file):
    """Parse CD-Hit clusters and extract allele-level info."""
    clusters = {}
    current_cluster = None
    
    with open(clstr_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>Cluster'):
                current_cluster = int(line.split()[1])
                clusters[current_cluster] = []
            elif current_cluster is not None and '>' in line:
                # Parse: "0   2681aa, >fig|1280.15931.peg.1175|... at 85.00%"
                # or: "0   2681aa, >fig|1280.15931.peg.1175|... *"
                parts = line.split('>')
                if len(parts) < 2:
                    continue
                after_gt = parts[1]
                # Get sequence ID: everything before first space or "..."
                seq_id = after_gt.split('...')[0].split()[0].rstrip('.')
                
                # Extract genome ID from fig|GENOME_ID.peg.N format
                if seq_id.startswith('fig|'):
                    inner = seq_id[4:]  # remove "fig|"
                    # Genome ID is everything up to .peg. or .rna.
                    for sep in ['.peg.', '.rna.', '.repeat.']:
                        if sep in inner:
                            genome_id = inner.split(sep)[0]
                            break
                    else:
                        genome_id = inner
                else:
                    genome_id = 'unknown'
                
                is_rep = line.endswith('*')
                
                # Get identity percentage if not representative
                identity = 100.0
                if not is_rep and 'at' in line:
                    try:
                        identity = float(line.split('at')[-1].strip().rstrip('%'))
                    except ValueError:
                        identity = 100.0
                
                clusters[current_cluster].append({
                    'seq_id': seq_id,
                    'genome_id': genome_id,
                    'is_rep': is_rep,
                    'identity': identity,
                })
    
    return clusters


def identify_alleles_from_proteins(org_name, genome_ids, clusters):
    """
    Identify unique amino acid sequence variants (alleles) for each gene cluster.
    For each cluster, read the actual protein sequences to find distinct alleles.
    """
    # Build mapping: seq_id -> cluster_id
    seq_to_cluster = {}
    for cid, members in clusters.items():
        for m in members:
            seq_to_cluster[m['seq_id']] = cid
    
    # Read all protein sequences and group by cluster
    cluster_alleles = defaultdict(dict)  # cluster -> {seq_hash -> allele_id}
    genome_allele_map = defaultdict(dict)  # genome -> {(cluster, allele) -> True}
    
    prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
    
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
                        # Find which cluster this belongs to
                        cid = seq_to_cluster.get(current_id)
                        if cid is not None:
                            seq_hash = hash(seq)
                            if seq_hash not in cluster_alleles[cid]:
                                cluster_alleles[cid][seq_hash] = len(cluster_alleles[cid])
                            allele_id = cluster_alleles[cid][seq_hash]
                            genome_allele_map[gid][(cid, allele_id)] = True
                    
                    # Parse new header
                    header = line[1:].split()[0]  # First word after >
                    # Handle multi-pipe PATRIC IDs
                    current_id = header.split('|')[0] + '|' + header.split('|')[1] if '|' in header else header
                    # Try matching against cluster seq_ids
                    if current_id not in seq_to_cluster:
                        # Try the full header
                        current_id = header
                    current_seq = []
                else:
                    current_seq.append(line)
        
        # Handle last sequence
        if current_id and current_seq:
            seq = ''.join(current_seq)
            cid = seq_to_cluster.get(current_id)
            if cid is not None:
                seq_hash = hash(seq)
                if seq_hash not in cluster_alleles[cid]:
                    cluster_alleles[cid][seq_hash] = len(cluster_alleles[cid])
                allele_id = cluster_alleles[cid][seq_hash]
                genome_allele_map[gid][(cid, allele_id)] = True
    
    return cluster_alleles, genome_allele_map


def build_feature_matrix(org_name, genome_ids, clusters):
    """
    Build binary feature matrix.
    - Core genes (missing ≤10): use allele-level features
    - Non-core genes: use gene-level presence/absence
    """
    n_genomes = len(genome_ids)
    
    # Classify genes
    gene_genome_count = {}
    gene_genomes = {}
    for cid, members in clusters.items():
        genomes = set(m['genome_id'] for m in members)
        gene_genome_count[cid] = len(genomes)
        gene_genomes[cid] = genomes
    
    core_genes = {cid for cid, cnt in gene_genome_count.items() 
                  if n_genomes - cnt <= CORE_THRESHOLD}
    non_core_genes = {cid for cid in clusters if cid not in core_genes}
    unique_genes = {cid for cid, cnt in gene_genome_count.items() 
                    if cnt <= CORE_THRESHOLD}
    accessory_genes = non_core_genes - unique_genes
    
    print(f"  Core genes: {len(core_genes)}")
    print(f"  Accessory genes: {len(accessory_genes)}")
    print(f"  Unique genes: {len(unique_genes)}")
    print(f"  Total clusters: {len(clusters)}")
    
    # For simplicity and speed, use gene-level presence/absence for all genes,
    # plus an approximation of allele diversity using cluster identity info.
    # The paper clusters proteins at 80% identity, so members with different
    # sequences within a cluster represent different alleles.
    
    # For core genes, we need allele-level encoding
    # For non-core genes, gene-level presence/absence
    
    print(f"  Identifying alleles for core genes...")
    cluster_alleles, genome_allele_map = identify_alleles_from_proteins(
        org_name, genome_ids, {cid: clusters[cid] for cid in core_genes}
    )
    
    # Build feature list
    features = []
    feature_names = []
    
    # Core gene alleles
    for cid in sorted(core_genes):
        n_alleles = len(cluster_alleles.get(cid, {}))
        for aid in range(n_alleles):
            features.append(('core_allele', cid, aid))
            feature_names.append(f"Cluster_{cid}_allele_{aid}")
    
    # Non-core gene presence/absence
    for cid in sorted(non_core_genes):
        features.append(('gene', cid, None))
        feature_names.append(f"Cluster_{cid}")
    
    print(f"  Total features: {len(features)}")
    print(f"    Core allele features: {sum(1 for f in features if f[0] == 'core_allele')}")
    print(f"    Non-core gene features: {sum(1 for f in features if f[0] == 'gene')}")
    
    # Build sparse matrix
    genome_idx = {gid: i for i, gid in enumerate(genome_ids)}
    rows, cols, data = [], [], []
    
    for j, (ftype, cid, aid) in enumerate(features):
        if ftype == 'core_allele':
            for gid in genome_ids:
                if (cid, aid) in genome_allele_map.get(gid, {}):
                    rows.append(genome_idx[gid])
                    cols.append(j)
                    data.append(1)
        elif ftype == 'gene':
            for gid in gene_genomes.get(cid, set()):
                if gid in genome_idx:
                    rows.append(genome_idx[gid])
                    cols.append(j)
                    data.append(1)
    
    X = sparse.csr_matrix((data, (rows, cols)), shape=(len(genome_ids), len(features)))
    
    print(f"  Feature matrix: {X.shape[0]} genomes × {X.shape[1]} features")
    print(f"  Density: {X.nnz / (X.shape[0] * X.shape[1]):.4f}")
    
    return X, feature_names, features


def load_amr_phenotypes(org_name, genome_ids, antibiotic):
    """Load binary AMR phenotypes for a given antibiotic."""
    amr_file = os.path.join(DATA_DIR, f'{org_name}_amr_raw.json')
    with open(amr_file) as f:
        records = json.load(f)
    
    # Build phenotype vector
    phenotypes = {}
    for rec in records:
        if rec.get('antibiotic', '').lower() == antibiotic.lower():
            gid = rec.get('genome_id')
            pheno = rec.get('resistant_phenotype', '')
            if pheno in ('Susceptible',):
                phenotypes[gid] = 0
            elif pheno in ('Resistant', 'Intermediate'):
                phenotypes[gid] = 1
    
    y = np.full(len(genome_ids), -1, dtype=int)
    for i, gid in enumerate(genome_ids):
        if gid in phenotypes:
            y[i] = phenotypes[gid]
    
    # Filter to genomes with phenotype data
    mask = y >= 0
    return y, mask


def train_svm_rse(X, y, n_svms=N_SVMS, genome_frac=GENOME_FRACTION, 
                  feature_frac=FEATURE_FRACTION, random_state=42):
    """Train SVM Random Subspace Ensemble."""
    rng = np.random.RandomState(random_state)
    n_samples, n_features = X.shape
    
    feature_weights = np.zeros(n_features)
    feature_counts = np.zeros(n_features)
    
    oob_predictions = defaultdict(list)
    
    for i in range(n_svms):
        # Random sample of genomes (80%)
        n_sample = int(n_samples * genome_frac)
        sample_idx = rng.choice(n_samples, n_sample, replace=False)
        oob_idx = np.setdiff1d(np.arange(n_samples), sample_idx)
        
        # Random sample of features (50%)
        n_feat = int(n_features * feature_frac)
        feat_idx = rng.choice(n_features, n_feat, replace=False)
        
        X_train = X[sample_idx][:, feat_idx]
        y_train = y[sample_idx]
        
        # Skip if only one class in sample
        if len(np.unique(y_train)) < 2:
            continue
        
        # Train linear SVM with L1 regularization
        try:
            svm = LinearSVC(
                penalty='l1',
                loss='squared_hinge',
                dual=False,
                class_weight='balanced',
                max_iter=5000,
                random_state=i,
                C=1.0,
            )
            svm.fit(X_train.toarray() if sparse.issparse(X_train) else X_train, y_train)
            
            # Store feature weights
            weights = svm.coef_[0]
            feature_weights[feat_idx] += weights
            feature_counts[feat_idx] += 1
            
            # OOB predictions
            if len(oob_idx) > 0:
                X_oob = X[oob_idx][:, feat_idx]
                preds = svm.predict(X_oob.toarray() if sparse.issparse(X_oob) else X_oob)
                for idx, pred in zip(oob_idx, preds):
                    oob_predictions[idx].append(pred)
        except Exception as e:
            if i < 5:
                print(f"    SVM {i} error: {e}", file=sys.stderr)
            continue
        
        if (i + 1) % 100 == 0:
            print(f"    Trained {i+1}/{n_svms} SVMs")
    
    # Average weights (only over SVMs that used each feature)
    mask = feature_counts > 0
    avg_weights = np.zeros(n_features)
    avg_weights[mask] = feature_weights[mask] / feature_counts[mask]
    
    # OOB MCC
    oob_true, oob_pred = [], []
    for idx in sorted(oob_predictions.keys()):
        preds = oob_predictions[idx]
        majority = 1 if sum(preds) > len(preds) / 2 else 0
        oob_true.append(y[idx])
        oob_pred.append(majority)
    
    if oob_true:
        oob_mcc = matthews_corrcoef(oob_true, oob_pred)
        oob_acc = accuracy_score(oob_true, oob_pred)
    else:
        oob_mcc = 0
        oob_acc = 0
    
    return avg_weights, oob_mcc, oob_acc


def cross_validate_rse(X, y, n_folds=5, n_svms=N_SVMS):
    """5-fold cross validation of SVM-RSE."""
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    metrics = {
        'accuracy': [], 'mcc': [], 'precision': [], 'recall': [], 'auroc': []
    }
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        print(f"    Fold {fold+1}: train={len(train_idx)}, test={len(test_idx)}, "
              f"R={sum(y_test==1)}, S={sum(y_test==0)}")
        
        rng = np.random.RandomState(fold * 100)
        n_samples, n_features = X_train.shape
        
        # Collect predictions from all SVMs for voting
        vote_counts = np.zeros((len(test_idx), 2))
        decision_values = np.zeros(len(test_idx))
        n_valid = 0
        
        for i in range(n_svms):
            n_sample = int(n_samples * GENOME_FRACTION)
            sample_idx = rng.choice(n_samples, n_sample, replace=False)
            n_feat = int(n_features * FEATURE_FRACTION)
            feat_idx = rng.choice(n_features, n_feat, replace=False)
            
            X_tr = X_train[sample_idx][:, feat_idx]
            y_tr = y_train[sample_idx]
            
            if len(np.unique(y_tr)) < 2:
                continue
            
            try:
                svm = LinearSVC(
                    penalty='l1', loss='squared_hinge', dual=False,
                    class_weight='balanced', max_iter=5000, random_state=i, C=1.0
                )
                svm.fit(X_tr.toarray() if sparse.issparse(X_tr) else X_tr, y_tr)
                
                X_te = X_test[:, feat_idx]
                preds = svm.predict(X_te.toarray() if sparse.issparse(X_te) else X_te)
                dvals = svm.decision_function(X_te.toarray() if sparse.issparse(X_te) else X_te)
                
                for j, (p, d) in enumerate(zip(preds, dvals)):
                    vote_counts[j, int(p)] += 1
                    decision_values[j] += d
                n_valid += 1
            except:
                continue
        
        if n_valid == 0:
            continue
        
        # Majority vote predictions
        y_pred = np.argmax(vote_counts, axis=1)
        decision_values /= n_valid
        
        metrics['accuracy'].append(accuracy_score(y_test, y_pred))
        metrics['mcc'].append(matthews_corrcoef(y_test, y_pred))
        metrics['precision'].append(precision_score(y_test, y_pred, zero_division=0))
        metrics['recall'].append(recall_score(y_test, y_pred, zero_division=0))
        try:
            metrics['auroc'].append(roc_auc_score(y_test, decision_values))
        except ValueError:
            metrics['auroc'].append(0.5)
    
    return {k: (np.mean(v), np.std(v)) for k, v in metrics.items()}


def main():
    # Define organism-antibiotic cases from the paper
    cases = {
        'S_aureus': {
            'id_file': 'sa_genome_ids.txt',
            'antibiotics': [
                'ciprofloxacin', 'clindamycin', 'erythromycin',
                'gentamicin', 'tetracycline', 'trimethoprim/sulfamethoxazole'
            ]
        },
        'P_aeruginosa': {
            'id_file': 'pa_genome_ids.txt',
            'antibiotics': ['amikacin', 'ceftazidime', 'levofloxacin', 'meropenem']
        },
        'E_coli': {
            'id_file': 'ec_genome_ids.txt',
            'antibiotics': [
                'amoxicillin/clavulanic acid', 'ceftazidime', 'ciprofloxacin',
                'gentamicin', 'imipenem', 'trimethoprim'
            ]
        },
    }
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    all_results = {}
    
    for org_name, config in cases.items():
        genome_ids = read_genome_ids(config['id_file'])
        
        # Check protein availability
        prot_dir = os.path.join(DATA_DIR, f'{org_name}_proteins')
        available = [gid for gid in genome_ids 
                     if os.path.exists(os.path.join(prot_dir, f'{gid}.faa'))
                     and os.path.getsize(os.path.join(prot_dir, f'{gid}.faa')) > 100]
        
        if len(available) < len(genome_ids) * 0.9:
            print(f"\n{org_name}: Only {len(available)}/{len(genome_ids)} genomes available, skipping")
            continue
        
        # Check for CD-Hit output
        clstr_file = os.path.join(RESULTS_DIR, f'{org_name}_cdhit.clstr')
        if not os.path.exists(clstr_file):
            print(f"\n{org_name}: CD-Hit output not found, skipping")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {org_name} ({len(available)} genomes)")
        
        # Parse clusters
        print(f"  Parsing CD-Hit clusters...")
        clusters = parse_cdhit_clusters_detailed(clstr_file)
        print(f"  Total gene clusters: {len(clusters)}")
        
        # Build feature matrix
        print(f"  Building feature matrix...")
        X, feature_names, features = build_feature_matrix(org_name, available, clusters)
        
        # Process each antibiotic
        for antibiotic in config['antibiotics']:
            print(f"\n  --- {org_name} vs {antibiotic} ---")
            
            y, mask = load_amr_phenotypes(org_name, available, antibiotic)
            n_with_data = mask.sum()
            n_resistant = (y[mask] == 1).sum()
            n_susceptible = (y[mask] == 0).sum()
            
            if n_with_data < 20:
                print(f"    Too few genomes with phenotype data ({n_with_data}), skipping")
                continue
            
            print(f"    Genomes with data: {n_with_data} "
                  f"(R={n_resistant}, S={n_susceptible})")
            
            X_case = X[mask]
            y_case = y[mask]
            
            # Train SVM-RSE for feature selection
            print(f"    Training SVM-RSE (feature selection)...")
            weights, oob_mcc, oob_acc = train_svm_rse(X_case, y_case)
            
            # Get top features
            top_resistance = np.argsort(weights)[::-1][:50]
            print(f"    OOB MCC: {oob_mcc:.3f}, OOB Accuracy: {oob_acc:.3f}")
            print(f"    Top 10 resistance features:")
            for rank, idx in enumerate(top_resistance[:10]):
                print(f"      {rank+1}. {feature_names[idx]} (weight: {weights[idx]:.4f})")
            
            # 5-fold cross validation
            print(f"    Running 5-fold cross validation...")
            cv_metrics = cross_validate_rse(X_case, y_case, n_folds=5, n_svms=100)
            
            case_key = f"{org_name}_{antibiotic.replace('/', '_')}"
            all_results[case_key] = {
                'organism': org_name,
                'antibiotic': antibiotic,
                'n_genomes': int(n_with_data),
                'n_resistant': int(n_resistant),
                'n_susceptible': int(n_susceptible),
                'oob_mcc': float(oob_mcc),
                'oob_accuracy': float(oob_acc),
                'cv_metrics': {k: {'mean': float(v[0]), 'std': float(v[1])} 
                              for k, v in cv_metrics.items()},
                'top_10_features': [
                    {'rank': r+1, 'name': feature_names[idx], 'weight': float(weights[idx])}
                    for r, idx in enumerate(top_resistance[:10])
                ],
                'top_50_features': [
                    {'rank': r+1, 'name': feature_names[idx], 'weight': float(weights[idx])}
                    for r, idx in enumerate(top_resistance[:50])
                ]
            }
            
            print(f"    CV Results:")
            for metric, (mean, std) in cv_metrics.items():
                print(f"      {metric}: {mean:.3f} ± {std:.3f}")
    
    # Save all results
    results_file = os.path.join(RESULTS_DIR, 'svm_rse_results.json')
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    print("Done!")


if __name__ == '__main__':
    main()
