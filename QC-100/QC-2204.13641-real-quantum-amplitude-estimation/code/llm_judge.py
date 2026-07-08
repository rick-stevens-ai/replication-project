"""LLM-judge verdict via Argo (localhost:44497, key=stevens, model claude-opus-4.7).
Reads results.json, sends it plus a checklist to the judge, saves verdict."""
import json, os, sys
from pathlib import Path
import urllib.request, urllib.error

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "report" / "evidence" / "results.json"
OUT = ROOT / "report" / "evidence" / "judge_verdict.json"

with open(RESULTS) as f:
    results = json.load(f)

# Compact summary
summary = {
    "config": results["config"],
    "rqae_by_eps": [{"eps": r["eps_target_true"], "a": r["a_true"],
                     "rmse": r["rmse"], "mean_N_q": r["mean_n_oracle"],
                     "coverage": r["coverage_within_eps"]} for r in results["rqae"]],
    "classical_by_eps": [{"eps": r["eps_target_true"], "a": r["a_true"],
                          "rmse": r["rmse"], "mean_N_q": r["mean_n_oracle"]}
                         for r in results["classical"]],
    "scaling_fit": results["scaling_fit"],
    "headline": results["headline"],
}

paper_claims = """
PAPER: Manzano et al. "Real Quantum Amplitude Estimation" arXiv:2204.13641

Headline claims to verify:
  C1. RQAE achieves quadratic speedup over unamplified sampling:
      N_oracle scales as ~1/eps for RQAE vs ~1/eps^2 classical
      (Fig. 6, Sec. 3.2 empirical performance).
  C2. Confidence-interval coverage: P(|a_hat - a| <= eps) >= 1-gamma = 0.95.
  C3. RMSE(a_hat) stays within the target precision eps.
"""

prompt = f"""You are a strict scientific replication judge. Evaluate whether the
attached numerical results REPLICATE the headline claims of the paper.

{paper_claims}

RESULTS (real Qiskit-Aer shot-based simulation, this replication):
{json.dumps(summary, indent=2)}

For each claim, decide REPLICATED / PARTIAL / NOT REPLICATED, cite the specific
numbers, and give a one-sentence justification.

Then give an overall verdict from this fixed vocabulary:
  REPLICATED | PARTIAL | SPOT-CHECK | NO-GO | CONTRADICTED | BLOCKED | FAILED

Reply ONLY as a compact JSON object with keys:
  claim_C1_verdict, claim_C1_reason,
  claim_C2_verdict, claim_C2_reason,
  claim_C3_verdict, claim_C3_reason,
  overall_verdict, overall_reason, one_line_summary
"""

body = json.dumps({
    "model": "argo:claude-opus-4.7",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 800,
}).encode()

req = urllib.request.Request(
    "http://localhost:44497/v1/chat/completions",
    data=body,
    headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode()
except urllib.error.HTTPError as e:
    raw = e.read().decode()
    print("HTTPError:", e.code, raw[:500])
    sys.exit(1)

parsed = json.loads(raw)
text = parsed["choices"][0]["message"]["content"].strip()

# Try to parse the JSON blob out of the text
def extract_json(s):
    start = s.find("{")
    end = s.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(s[start:end+1])
        except json.JSONDecodeError:
            pass
    return {"raw": s}

verdict = extract_json(text)
verdict["_model"] = "argo:claude-opus-4.7"
verdict["_endpoint"] = "http://localhost:44497/v1"

with open(OUT, "w") as f:
    json.dump(verdict, f, indent=2)

print(json.dumps(verdict, indent=2))
