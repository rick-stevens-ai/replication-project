"""LLM judge for the QC-177 replication.

Uses Argo proxy :44497 (free, key=stevens) with claude-opus-4.7.
Feeds the paper's key theoretical claims + the replication's numerical results,
asks for a verdict from the canonical vocabulary.
"""
import json, os, urllib.request

ARGO_URL = "http://127.0.0.1:44497/v1/chat/completions"
API_KEY = os.environ.get("ARGO_API_KEY", "stevens")

evidence_dir = "/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/" \
    "QC-1801.04042-randomized-benchmarking-with-restricted-gate-sets/report/evidence"

with open(f"{evidence_dir}/results.json") as f:
    sym = json.load(f)
with open(f"{evidence_dir}/results_asym.json") as f:
    asym = json.load(f)

paper_summary = """
Paper: Brown & Eastin (arXiv:1801.04042), "Randomized benchmarking with restricted gate sets".
Purely analytical extension of standard RB to Clifford subgroups that are NOT unitary 2-designs.

Core theoretical predictions (no numerical experiments in the paper itself):

1) Full Clifford RB: single-exp decay f_l = c0 + c1 * lambda^l with
     lambda = 1 - p * 4^n / (4^n - 1)
   where p is the entanglement infidelity.

2) Real Clifford group (H, CNOT, single-qubit Paulis) partitions Paulis into
   2 non-trivial blocks:
     B1 = even # of Y (non-identity),  size N1(n) = (4^n + 2^n)/2 - 1
     B2 = odd # of Y,                  size N2(n) = (4^n - 2^n)/2
   Block eigenvalues:
     lambda1 = 1 - p1 * 4^n/(4^n + 2^n - 2) - p2 * 4^n/(4^n - 2^n)
     lambda2 = 1 - p1 * 4^n/(4^n - 2^n) analog (imaginary)
   From |0...0> (a real-Pauli eigenstate) only lambda1 is measured.

3) CNOT + Pauli group partitions Paulis into 4 blocks:
     B1 = Z-only (non-identity),  N1 = 2^n - 1
     B2 = X-only (non-identity),  N2 = 2^n - 1
     B3 = mixed even-Y,           N3 = (4^n - 3*2^n)/2 + 1
     B4 = odd-Y,                  N4 = (4^n - 2^n)/2
   From |0...0> measures lambda1 = 1 - (p2+p3+p4) * 2^n/(2^n - 1)
   From |+...+> measures lambda2 = 1 - (p1+p3+p4) * 2^n/(2^n - 1)

4) Entanglement-infidelity bound (CNOT+Pauli, from lambda1 alone):
     (2^n - 1)/2^n * (1 - lambda1) <= p <= (1 - lambda1)
"""

# Extract results into a compact summary
sym_results = []
for key in ["exp1_full_clifford_n2", "exp2_real_clifford_n2",
             "exp3a_cnot_pauli_n2_00", "exp3b_cnot_pauli_n2_plusplus"]:
    d = sym[key]
    fit = d.get("fit") or d.get("fit_single")
    lam_t = d.get("theory_lambda") or d.get("theory_lambda1") or d["theory"].get("lam1") or d["theory"].get("lam2")
    if key == "exp3b_cnot_pauli_n2_plusplus":
        lam_t = d["theory"]["lam2"]
    sym_results.append({
        "exp": key, "fit_lam": round(fit["lam"], 4),
        "theory_lam": round(lam_t, 4),
        "abs_diff": round(abs(fit["lam"] - lam_t), 4),
        "p_total": round(d["p_total"], 4),
        "n_sequences_per_length": d["config"]["n_sequences_per_length"],
        "lengths": d["lengths"],
        "fidelities": [round(x, 3) for x in d["fs"]],
    })

asym_results = []
for key in ["zerror_00", "zerror_pp"]:
    d = asym[key]
    asym_results.append({
        "exp": key, "fit_lam": round(d["fit"]["lam"], 4),
        "theory_lam": round(d["lam_theory"], 4),
        "abs_diff": round(abs(d["fit"]["lam"] - d["lam_theory"]), 4),
        "p_total": round(d["p_total"], 4),
        "fidelities": [round(x, 3) for x in d["fs"]],
    })

judge_prompt = f"""You are an impartial scientific referee grading a replication attempt of a QUANTUM COMPUTING theory paper.

--- PAPER SUMMARY ---
{paper_summary}

--- REPLICATION APPROACH ---
Independent implementation in Python using Stim (Aaronson-Gottesman Clifford tableau simulator).
- Full Clifford: uniform sampling via stim.Tableau.random(n).
- Real Clifford & CNOT+Pauli subgroups: random walk of 60 generators over each subgroup's generator set (mixing sample).
- RB protocol: apply m group elements + per-qubit depolarizing (or Z-only) noise after each + compute inverse tableau + measure survival probability in ideal basis.
- Sampled 60-80 sequences per length; lengths m in {{1,2,4,8,16,32,64,128}}.
- Fit single-exponential f_l = a + b*lambda^l.

--- RESULTS (n=2 qubits) ---

SYMMETRIC DEPOLARIZING NOISE (p_dep=0.01/qubit -> p_total=0.0199):
{json.dumps(sym_results, indent=2)}

ASYMMETRIC PURE-Z NOISE (p_z=0.02/qubit -> p_total=0.0396):
- Under pure Z noise, only block B1 (Z-only) has non-zero mass. So p1=p_total, p2=p3=p4=0.
- Predicted: from |00> lambda1=1 (no decay); from |++> lambda2 = 1 - p_total*4/3 = 0.9472.
{json.dumps(asym_results, indent=2)}

BOUND CHECK: paper says (2^n - 1)/2^n * (1 - lambda1) <= p <= (1 - lambda1).
  Sym exp3a: 0.75 * (1 - 0.9797) = 0.0152 <= p=0.0199 <= 0.0203  -- inside.
  Asym pp:   0.75 * (1 - 0.9561) = 0.0329 <= p=0.0396 <= 0.0439  -- inside.

--- YOUR TASK ---
Grade this replication.

1. Are the theoretical formulas transcribed from the paper correctly implemented?
2. Do the numerical results support (REPLICATE), partially support (PARTIAL), or contradict (CONTRADICTED) the paper's predictions?
3. How definitive is the evidence? Consider: (a) how close the fitted lambdas are to theory, (b) whether the statistical noise level is plausible for 60-80 sequences, (c) whether the asymmetric-noise experiment cleanly probes the block structure the paper predicts, (d) any caveats.

Choose ONE verdict from this exact vocabulary:
REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.

Return STRICT JSON only, no prose outside the JSON:
{{
  "verdict": "<one of the vocabulary words>",
  "confidence": "<low|medium|high>",
  "reasoning": "<2-4 sentences>",
  "strongest_evidence_for": "<the single most convincing data point>",
  "weakness_or_caveat": "<the biggest limitation of the replication>"
}}
"""

payload = {
    "model": "argo:claude-opus-4.7",
    "messages": [{"role": "user", "content": judge_prompt}],
    "max_tokens": 800,
    "temperature": 0.0,
}
req = urllib.request.Request(
    ARGO_URL,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json",
             "Authorization": f"Bearer {API_KEY}"},
)
with urllib.request.urlopen(req, timeout=120) as resp:
    body = resp.read().decode()

parsed = json.loads(body)
content = parsed["choices"][0]["message"]["content"]
print("=" * 70)
print("RAW JUDGE OUTPUT:")
print("=" * 70)
print(content)
print("=" * 70)

# Try to extract JSON verdict
import re
m = re.search(r"\{[\s\S]*\}", content)
if m:
    try:
        verdict_obj = json.loads(m.group(0))
    except Exception as e:
        verdict_obj = {"raw": content, "parse_error": str(e)}
else:
    verdict_obj = {"raw": content, "parse_error": "no JSON braces found"}

outfile = f"{evidence_dir}/judge_verdict.json"
with open(outfile, "w") as fh:
    json.dump({
        "model": payload["model"],
        "endpoint": ARGO_URL,
        "verdict_object": verdict_obj,
        "raw_content": content,
    }, fh, indent=2)
print(f"\nSaved: {outfile}")
print(f"\nVERDICT: {verdict_obj.get('verdict', '?')}")
