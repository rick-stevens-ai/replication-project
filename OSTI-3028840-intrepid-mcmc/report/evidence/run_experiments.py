#!/usr/bin/env python3
"""
Reproduce Intrepid MCMC Section 4.1 key claims on the 9 analytical multimodal 2D targets.
Metrics per paper: Total Variation Distance (TVD) vs IID rejection-sampled reference,
error-in-mean (l2 of chain-mean minus true-mean / sqrt(trace(cov))), acceptance rate.
Sweep beta in {0, 0.01, 0.05, 0.1, 0.3, 0.5, 1.0}. 100 (reduced) trials.
"""
import numpy as np, json, time, sys
from concurrent.futures import ProcessPoolExecutor
from intrepid import CASES, run_chain, rejection_sample, tvd

BETAS = [0.0, 0.01, 0.05, 0.1, 0.3, 0.5, 1.0]
N_TRIALS = int(sys.argv[1]) if len(sys.argv)>1 else 40
CHAIN_LEN = int(sys.argv[2]) if len(sys.argv)>2 else 100000
BURN = 10000
N_IID = 3_000_000
BINS = 60

# generous bounds per case (from paper contour plots)
BOUNDS = {
 1: ((-6,6),(-6,6)),
 2: ((-6,6),(-6,6)),
 3: ((-6,6),(-6,6)),
 4: ((-4,8),(-4,8)),
 5: ((-4,8),(-4,8)),
 6: ((-4,8),(-4,8)),
 7: ((-6,6),(-5,15)),
 8: ((-6,6),(-5,15)),
 9: ((-6,6),(-5,15)),
}

def approx_pmax(case_id, bounds):
    from intrepid import CASES
    name,pi_fn=CASES[case_id]
    (xlo,xhi),(ylo,yhi)=bounds
    gx=np.linspace(xlo,xhi,1000); gy=np.linspace(ylo,yhi,1000)
    X,Y=np.meshgrid(gx,gy)
    pts=np.stack([X.ravel(),Y.ravel()],axis=1)
    return float(pi_fn(pts).max())*1.5

def build_reference(case_id):
    b=BOUNDS[case_id]
    pmax=approx_pmax(case_id,b)
    ref = rejection_sample(case_id, N_IID, 999+case_id, b, pmax)
    true_mean = ref.mean(0)
    true_cov = np.cov(ref.T)
    return ref, true_mean, true_cov, b

def trial(args):
    case_id, beta, seed, ref_hist_bounds, true_mean, tr_cov_sqrt, ref_samples_small = args
    samples, ar = run_chain(case_id, beta, CHAIN_LEN, BURN, seed)
    t = tvd(samples, ref_samples_small, BINS, ref_hist_bounds)
    err_mean = np.linalg.norm(samples.mean(0)-true_mean)/tr_cov_sqrt
    return (case_id, beta, seed, t, err_mean, ar)

def main():
    results=[]
    summary={}
    for case_id in range(1,10):
        name,_=CASES[case_id]
        t0=time.time()
        ref, true_mean, true_cov, b = build_reference(case_id)
        tr_cov_sqrt = np.sqrt(np.trace(true_cov))
        rng_bounds=[list(b[0]),list(b[1])]
        # use a subset of iid for TVD histogram reference (same for all)
        ref_small = ref[:500000]
        tasks=[]
        for beta in BETAS:
            for k in range(N_TRIALS):
                tasks.append((case_id,beta,1000+k, rng_bounds, true_mean, tr_cov_sqrt, ref_small))
        with ProcessPoolExecutor(max_workers=32) as ex:
            for r in ex.map(trial, tasks):
                results.append(r)
        # summarize
        summary[case_id]={"name":name,"n_ref":len(ref),"true_mean":true_mean.tolist(),
                          "tr_cov_sqrt":float(tr_cov_sqrt),"by_beta":{}}
        for beta in BETAS:
            rr=[x for x in results if x[0]==case_id and x[1]==beta]
            tvds=np.array([x[3] for x in rr]); errs=np.array([x[4] for x in rr]); ars=np.array([x[5] for x in rr])
            n_fail=int(np.isnan(tvds).sum())
            summary[case_id]["by_beta"][str(beta)]={
                "tvd_median":float(np.nanmedian(tvds)),"tvd_mean":float(np.nanmean(tvds)),"tvd_std":float(np.nanstd(tvds)),
                "errmean_median":float(np.nanmedian(errs)),"errmean_mean":float(np.nanmean(errs)),
                "accrate_mean":float(ars.mean()),"n_fail_no_mode":n_fail,"n_trials":len(tvds)}
        print(f"case {case_id} {name}: done in {time.time()-t0:.1f}s  "
              f"TVD(b=0)={summary[case_id]['by_beta']['0.0']['tvd_median']:.4f} "
              f"TVD(b=0.1)={summary[case_id]['by_beta']['0.1']['tvd_median']:.4f}", flush=True)
    json.dump({"config":{"n_trials":N_TRIALS,"chain_len":CHAIN_LEN,"burn":BURN,"n_iid":N_IID,"bins":BINS,"betas":BETAS},
               "summary":summary},
              open("results.json","w"), indent=2)
    print("WROTE results.json")

if __name__=="__main__":
    main()
