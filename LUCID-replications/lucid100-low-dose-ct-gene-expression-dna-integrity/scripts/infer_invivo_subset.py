#!/usr/bin/env python3
"""
Infer per-patient in-vivo / ex-vivo labels for Schmid et al. 2025 (IJMS 26:11869).

The paper publishes per-patient differential gene expression (DGE) in Table A1
but does NOT publish which patients belong to the in-vivo (post-CT blood drawn
4-6h after the scan; n=27 per Table 2 or n=28 per abstract) vs ex-vivo
(blood drawn immediately, then incubated; n=33 or n=32) subgroups.

Table 2 publishes the per-gene MEDIAN DGE for each subgroup, rounded to 2 dp.
Given the 60-patient DGE matrix and the 18 target medians (9 genes × 2 groups),
we use simulated annealing over binary partitions to find subset(s) that
reproduce both subgroup medians.

Notes:
  - Abstract says n=28/32; Table 2 says n=27/33. We search both partition sizes.
  - The solution is generally NOT unique — multiple 28-patient subsets reproduce
    the medians to within rounding. We save the best-fit subset and report
    the number of tied subsets, so downstream analyses can be flagged as
    "subject-to-label-ambiguity".

Output: results/invivo_exvivo_labels.json
"""
import csv, random, json, time
from pathlib import Path
import numpy as np

random.seed(20260622); np.random.seed(20260622)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ART = ROOT / 'artifacts'
RES = ROOT / 'results'; RES.mkdir(exist_ok=True)

GENES = ["DDB2","FDXR","POU2AF1","WNT3","BAX","AEN","EDA2R","MIR34AHG","PHLDA3"]
TARGET_IN = {"DDB2":1.09,"FDXR":1.24,"POU2AF1":1.06,"WNT3":0.96,"BAX":1.06,
             "AEN":1.17,"EDA2R":1.57,"MIR34AHG":1.36,"PHLDA3":1.29}
TARGET_EX = {"DDB2":0.73,"FDXR":0.63,"POU2AF1":1.44,"WNT3":0.80,"BAX":0.95,
             "AEN":0.90,"EDA2R":1.41,"MIR34AHG":2.56,"PHLDA3":0.89}

def load():
    rows = list(csv.reader(open(ART/'ijms-26-11869-t0A1.tsv'), delimiter='\t'))
    pat = {}
    for r in rows[3:]:
        if not r or not r[0].strip(): continue
        pid = int(r[0])
        def f(x):
            x = x.strip().replace('\u2212','-')
            return float('nan') if x in ('','-') else float(x)
        vals = [f(r[i+1]) for i in range(9)]
        if any(np.isnan(vals)): continue
        pat[pid] = vals
    return pat

def joint_err(arr, idx, tin, tex):
    mask = np.zeros(len(arr),dtype=bool); mask[idx]=True
    m_in = np.median(arr[mask], axis=0)
    m_ex = np.median(arr[~mask], axis=0)
    return max(np.max(np.abs(m_in-tin)), np.max(np.abs(m_ex-tex)))

def sa(arr, n_in, tin, tex, n_starts=30, n_iters=40000, T0=0.10, T1=0.0005):
    n = arr.shape[0]
    best_err = np.inf; best_set = None; pool=[]
    decay = (T1/T0)**(1.0/n_iters)
    for s in range(n_starts):
        cur = set(random.sample(range(n), n_in))
        ce = joint_err(arr, list(cur), tin, tex)
        T = T0
        for _ in range(n_iters):
            i_out = random.choice(list(cur))
            i_in = random.choice([i for i in range(n) if i not in cur])
            cur.remove(i_out); cur.add(i_in)
            ne = joint_err(arr, list(cur), tin, tex)
            if ne < ce or random.random() < np.exp((ce-ne)/T):
                ce = ne
            else:
                cur.remove(i_in); cur.add(i_out)
            T *= decay
        if ce < best_err - 1e-9:
            best_err, best_set, pool = ce, frozenset(cur), [frozenset(cur)]
        else:
            pool.append(frozenset(cur))
    return best_err, best_set, pool

def main():
    pat = load()
    pids = sorted(pat.keys())
    arr = np.array([pat[p] for p in pids])
    tin = np.array([TARGET_IN[g] for g in GENES])
    tex = np.array([TARGET_EX[g] for g in GENES])
    print(f"Loaded {len(pids)} patients with full gene data.")

    results = {}
    for n_in in (27, 28):
        t0 = time.time()
        print(f"\nJoint SA, n_in={n_in}, 30 starts × 40000 iter ...")
        e, best, pool = sa(arr, n_in, tin, tex)
        print(f"  best err = {e:.4f}  ({time.time()-t0:.1f}s)")
        # count tied
        tied = len({s for s in pool if abs(joint_err(arr,list(s),tin,tex)-e) < 1e-9})
        results[n_in] = (e, best, tied)

    # pick min
    n_in, (e, best, tied) = min(results.items(), key=lambda kv: kv[1][0])
    in_idx = sorted(best); ex_idx = sorted([i for i in range(60) if i not in best])
    mask = np.zeros(60, dtype=bool); mask[in_idx]=True
    m_in = np.median(arr[mask],axis=0); m_ex = np.median(arr[~mask],axis=0)

    out = {
        'method':'joint simulated annealing on Table 2 medians',
        'note':('Abstract says n=28 in-vivo / n=32 ex-vivo; Table 2 says n=27/33. '
                'Both sizes searched; smaller-error winner kept.'),
        'n_in_used':int(n_in), 'n_ex_used':int(60-n_in),
        'max_median_error':float(e),
        'in_vivo_pids':[pids[i] for i in in_idx],
        'ex_vivo_pids':[pids[i] for i in ex_idx],
        'verification':{g:{'target_in':float(tin[i]),'got_in':float(m_in[i]),
                           'target_ex':float(tex[i]),'got_ex':float(m_ex[i])}
                        for i,g in enumerate(GENES)},
        'n_tied_subsets':int(tied),
        'uniqueness': 'UNIQUE' if tied==1 else f'AMBIGUOUS ({tied} tied)',
        'all_results':{str(k):{'max_err':float(v[0]),'tied':int(v[2])}
                       for k,v in results.items()},
    }
    with open(RES/'invivo_exvivo_labels.json','w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {RES/'invivo_exvivo_labels.json'} (n_in={n_in}, err={e:.3f}, tied={tied})")

if __name__ == '__main__':
    main()
