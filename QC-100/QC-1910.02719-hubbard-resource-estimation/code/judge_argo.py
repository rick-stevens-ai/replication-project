"""
LLM-judge (single-model via free Argo endpoint) verdict on the
replication of Cai (arXiv:1910.02719). Free endpoints only.
"""
import json, os, sys, urllib.request

ARGO_URL = "http://127.0.0.1:44497/v1/chat/completions"
ARGO_KEY = "stevens"
MODEL    = "argo:gpt-5.1"

EVIDENCE = os.path.join(os.path.dirname(__file__), "..", "report", "evidence")

def load(name):
    with open(os.path.join(EVIDENCE, name)) as f:
        return json.load(f)

def call(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a careful scientific replication reviewer. Score strictly on evidence. Reply in the requested JSON only."},
            {"role": "user",   "content": prompt},
        ],
        "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(ARGO_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ARGO_KEY}",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())

def main():
    formula   = load("formula_check.json")
    small     = load("hubbard_small_runs.json")
    vqe       = load("hubbard_vqe_runs.json")

    evidence_str = json.dumps({
        "formula_check": formula,
        "hubbard_small_runs": small,
        "hubbard_vqe_runs": vqe,
    }, indent=2)

    prompt = f"""Independent-replication verdict for arXiv:1910.02719 (Cai, "Resource Estimation for Quantum Variational Simulations of the Hubbard Model", 2019).

Paper's headline testable claims we targeted:
  C1 (per-block HVA gate counts, Appendix A2):
     N1q,ha(V) = 4 V^(3/2) + 7 V - 4 sqrt(V)
     N2q,ha(V) = 8 V^(3/2) +   V - 4 sqrt(V)
     with V=25 -> N1q ~ 650, N2q ~ 1000.
  C2 (per-block runtime formula, Appendix A2):
     T = (8 sqrt(V) + 5) tau_1q + (16 sqrt(V) + 2) tau_2q
     with V=25 -> T ~ 45 tau_1q + 80 tau_2q.
  C3 (qubit count): N_qubits = 2 V under Jordan-Wigner.

Evidence gathered (real openfermion + cirq simulation on my own machine, not the paper's numbers):

{evidence_str}

Score STRICTLY on:
  * Is C1 numerically verified from the formulas at V=25? (yes/no, delta)
  * Is C2 numerically verified from the formulas at V=25? (yes/no)
  * Is C3 verified by openfermion Jordan-Wigner on small (2x2, 2x3) instances? (yes/no)
  * Was a real Hubbard ground-state energy computed at small size? (yes/no)

Then output a single overall verdict from this vocabulary:
  REPLICATED   — headline number(s) reproduced within tolerance on real sim
  PARTIAL      — some claims reproduced, others not
  SPOT-CHECK   — code/method verified, small demo, not full claim
  NO-GO        — data/code unavailable
  CONTRADICTED
  BLOCKED
  FAILED

Reply ONLY with JSON of the form:
{{
  "C1_verified": bool, "C1_delta_N1q": number, "C1_delta_N2q": number,
  "C2_verified": bool,
  "C3_verified": bool,
  "vqe_run_end_to_end": bool,
  "verdict": "REPLICATED|PARTIAL|SPOT-CHECK|NO-GO|CONTRADICTED|BLOCKED|FAILED",
  "one_line": "single-sentence summary <= 25 words"
}}
"""
    resp = call(prompt)
    text = resp["choices"][0]["message"]["content"].strip()
    # strip code fences if any
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    verdict = json.loads(text)
    print(json.dumps(verdict, indent=2))
    out = os.path.join(EVIDENCE, "judge_argo.json")
    with open(out, "w") as f:
        json.dump({"model": MODEL, "verdict": verdict, "raw": text}, f, indent=2)
    print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
