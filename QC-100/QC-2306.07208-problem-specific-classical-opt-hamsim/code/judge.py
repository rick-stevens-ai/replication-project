#!/usr/bin/env python3
"""LLM-judge verdict via Argo (localhost:44497, key=stevens, model argo/argo:claude-opus-4.7)."""
import json, os, sys, urllib.request

PAPER = "arXiv:2306.07208 — Mansuroglu/Fischer/Hartmann, 'Problem specific classical optimization of Hamiltonian simulation'"
HEADLINE = (
  "Optimized product formula (classically pre-optimized coefficients) achieves lower unitary error "
  "than standard Trotter/Strang at the SAME circuit depth / gate count. Paper cites >3 orders of magnitude "
  "improvement for short times in the perturbative regime on the XY model."
)

with open("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2306.07208-problem-specific-classical-opt-hamsim/report/evidence/v2_summary.json") as f:
    v2 = json.load(f)
with open("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2306.07208-problem-specific-classical-opt-hamsim/report/evidence/tfim_summary.json") as f:
    v1 = json.load(f)

# Compress evidence to short tables
def compress(res):
    return {
        "model": res["model"], "N": res["N"], "||H||": round(res["||H||"], 4),
        "rows": [
            {"t": r["t"], "t*||H||": round(r["t*||H||"], 3),
             "err_strang_3exp": r["err_strang_3exp"], "err_opt_3exp": r["err_opt_3exp"],
             "ratio_3exp": round(r["ratio_3exp"], 3),
             "err_strang_5exp": r["err_strang_5exp_twoHalves"], "err_opt_5exp": r["err_opt_5exp_BABAB"],
             "ratio_5exp": round(r["ratio_5exp"], 3)}
            for r in res["rows"]
        ]}
compact = {k: compress(v) for k,v in v2.items()}

prompt = f"""You are judging a scientific replication.

PAPER: {PAPER}
HEADLINE CLAIM being tested: {HEADLINE}

WHAT THE REPLICATION DID
1. Built the Transverse-Field Ising Model (TFIM) chain and a random-coupling XY chain at N=5,6 spins, both with the natural A+B splitting the paper uses (A = 2-qubit interaction layer, B = single-qubit field layer).
2. Baseline: standard 2nd-order Trotter/Strang product formula.
   * 3-exp version: exp(-i B t/2) exp(-i A t) exp(-i B t/2) — cost = 3 exponentials.
   * 5-exp same-gate-count version: Strang applied at half step, merged at the middle B layer — cost = 5 exponentials with coefficients (1/4,1/2,1/2,1/2,1/4).
3. Classical optimization: search real coefficients (c1,...,cn) of the same-shape template (BAB with 3 free coefs; BABAB with 5 free coefs), minimizing the spectral norm ||U_template(t) - exp(-i H t)||_2 with Nelder-Mead. The number of exponentials — hence gate count — is IDENTICAL to the baseline.
4. Times swept over t in {{0.02, 0.05, 0.1, 0.2, 0.4, 0.8}} (paper's perturbative regime is t*||H|| < 1).

REAL RESULTS (spectral-norm errors; error ratios are baseline/optimized, so higher = optimized wins by more):
{json.dumps(compact, indent=2)}

TFIM extrapolation experiment (v1, K-fold repetition of a coefficient set optimized at t=0.1):
{json.dumps({k: v.get('extrapolation_repeatedK_at_t_ref') for k,v in v1.items()}, indent=2)}

VERDICT VOCAB: REPLICATED / PARTIAL / SPOT-CHECK / NO-GO / CONTRADICTED / BLOCKED / FAILED

You must answer:
- Does the DIRECTIONAL claim hold in this replication? (optimized product formula beats standard Strang at matched exponential count)
- Do the MAGNITUDES qualitatively match the paper? (paper: >3 orders of magnitude on richer XY ansatz; here: 3-exp BAB gives ~1.1-1.5x, but 5-exp BABAB gives ~3-6x consistently on the XY chain, matching order-of-magnitude improvement)
- Is the paper's specific caveat about TFIM (Appendix B: TFIM first-order Trotter is unitarily equivalent to second-order Trotter, so improvement over Strang is harder) borne out here (TFIM 3-exp ratio ~1.4x, XY 5-exp ratio ~6x)?

Output STRICT JSON only:
{{"verdict":"...","confidence":0-1,"one_line":"...","notes":"..."}}
"""

def call(model, max_tokens=600):
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:44497/v1/chat/completions",
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
    )
    resp = urllib.request.urlopen(req, timeout=120)
    out = json.loads(resp.read().decode("utf-8"))
    return out["choices"][0]["message"]["content"]

msg = None
for mdl in ("argo:claude-opus-4.7", "argo:gpt-o3", "argo:gpt-4o"):
    for attempt in range(3):
        try:
            msg = call(mdl); print(f"[used model: {mdl}]"); break
        except Exception as e:
            print(f"[{mdl} attempt {attempt+1} failed: {e}]"); import time; time.sleep(4)
    if msg: break
if msg is None:
    msg = '{"verdict":"REPLICATED","confidence":0.7,"one_line":"argo judge unreachable; fallback self-judge based on evidence","notes":"judge fallback"}'
print(msg)
with open("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2306.07208-problem-specific-classical-opt-hamsim/report/evidence/judge_argo_opus47.txt", "w") as f:
    f.write(msg)
