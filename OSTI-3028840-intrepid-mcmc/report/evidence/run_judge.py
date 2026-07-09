#!/usr/bin/env python3
"""LLM-judge the replication of Intrepid MCMC (OSTI 3028840) using free Argo proxy."""
import json, urllib.request, os, sys

RESULTS = json.load(open(os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/OSTI-3028840-intrepid-mcmc/report/evidence/results.json")))
s = RESULTS["summary"]
betas=['0.0','0.01','0.05','0.1','0.3','0.5','1.0']

# Build compact evidence tables
lines=["TVD median by beta (0.0=CMH baseline):","case | "+" | ".join(betas)]
for c in map(str,range(1,10)):
    r=s[c]['by_beta']
    lines.append(s[c]['name']+" | "+" | ".join(f"{r[b]['tvd_median']:.4f}" for b in betas))
lines.append("\nAcceptance rate by beta:")
lines.append("case | "+" | ".join(betas))
for c in map(str,range(1,10)):
    r=s[c]['by_beta']
    lines.append(s[c]['name']+" | "+" | ".join(f"{r[b]['accrate_mean']:.3f}" for b in betas))
lines.append("\nError-in-mean median CMH(b=0)->Intrepid(b=0.1):")
for c in map(str,range(1,10)):
    r=s[c]['by_beta']
    lines.append(f"{s[c]['name']}: {r['0.0']['errmean_median']:.4f} -> {r['0.1']['errmean_median']:.4f}")
evidence="\n".join(lines)

CLAIMS = """
C1: Intrepid MCMC with beta=0.1 consistently outperforms vanilla CMH (beta=0) on multimodal / disconnected-support targets (lower TVD to the true target).
C2: Even a tiny exploration fraction (beta=0.01) significantly improves convergence for multimodal targets.
C3: CMH gets 'stuck' and fails to find/populate disconnected modes; Intrepid populates all modes (reflected in far lower TVD & error-in-mean for the disconnected 'Circles' cases).
C4: Acceptance rate diminishes only modestly for beta<=0.1, then drops precipitously for beta>=0.3 and collapses at beta=1.0.
C5: Error in the estimated mean converges to near-zero for Intrepid on multimodal targets while CMH produces large errors.
C6: beta=1.0 (pure exploration) is NOT optimal - it wastes samples and worsens TVD vs beta=0.1.
"""

prompt=f"""You are a rigorous, skeptical reproducibility judge for a scientific replication project.

PAPER: "Intrepid MCMC: Metropolis-Hastings with Exploration" (Chakroborty & Shields, INL/JOU-24-82292, DOI 10.1016/j.cma.2025.118402). It proposes a Metropolis-Hastings variant that with probability beta takes an 'Intrepid' exploration step (hyperspherical transform anchored at a fixed point, moving along equal-probability contours of a parent Gaussian) and otherwise a component-wise MH (CMH) step. Benchmarked on 9 analytical 2-D multimodal targets (Section 4.1), sweeping beta, over 100 trials, 100k-sample chains, measuring Total Variation Distance (TVD) to a 50M-sample IID reference, error-in-mean, and acceptance rate.

INDEPENDENT REPLICATION: We reimplemented the algorithm FROM THE EQUATIONS (no public code exists). We reproduced the exact 9 targets (Tables 2-4), exact proposals (Intrepid angular Uniform full-circle, radial Uniform(0.5,2.0); CMH N(x,1) component-wise), anchor at parent mean, identity RTF (radially-symmetric Gaussian parent). We used 30 trials, 100k-sample chains, 10k burn-in, 3M-sample IID rejection references, TVD via 60x60 2D histogram. Compute on an A100 node (CPU numpy). Chains initialized at random valid support points.

PAPER CLAIMS TO ASSESS:
{CLAIMS}

OUR REPRODUCED EVIDENCE:
{evidence}

For EACH claim C1..C6, state whether our independent results SUPPORT / PARTIALLY-SUPPORT / CONTRADICT it, with one sentence of quantitative justification citing the numbers. Then give:
1. An overall verdict from EXACTLY this vocabulary: REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.
2. A 2-3 sentence justification.
Be honest: note that Gumbel-Ring showed ~no improvement and Rosenbrock-Ring/Planes error-in-mean stayed high (heavy-tailed mean), and factor these into whether it's REPLICATED vs PARTIAL.
Return your answer as JSON: {{"per_claim": {{"C1": {{"assessment": "...", "justification": "..."}}, ...}}, "verdict": "...", "justification": "..."}}
"""

def call_argo(model):
    body=json.dumps({"model":model,"messages":[{"role":"user","content":prompt}],
                     "temperature":0.0}).encode()
    req=urllib.request.Request("http://127.0.0.1:44497/v1/chat/completions",data=body,
        headers={"Content-Type":"application/json","Authorization":"Bearer stevens"})
    with urllib.request.urlopen(req,timeout=300) as r:
        return json.load(r)["choices"][0]["message"]["content"]

for model in ["argo:gpt-5.2","argo:claude-opus-4.8","gpt-5.2","claude-opus-4.8"]:
    try:
        print(f"# trying {model}",file=sys.stderr)
        out=call_argo(model)
        print(f"MODEL_USED={model}")
        print(out)
        open(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/OSTI-3028840-intrepid-mcmc/report/evidence/llm_judge_verdict.txt"),"w").write(f"MODEL={model}\n\n"+out)
        break
    except Exception as e:
        print(f"# {model} failed: {e}",file=sys.stderr)
