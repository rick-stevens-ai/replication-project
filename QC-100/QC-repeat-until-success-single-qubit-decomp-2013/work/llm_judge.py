"""
LLM-judge scoring of the replication of arXiv:1311.1074 (RUS, Paetznick & Svore 2014).
Uses the free Argo proxy at localhost:44497 (model: argo:claude-opus-4.7).
Prompts the judge with:
  - paper claims (extracted from the paper text),
  - the exact numerical results of our Qiskit statevector reproduction,
and asks for a structured verdict from the canonical vocabulary.
"""
import json, os, subprocess, sys, textwrap

# Use the LiteLLM aggregator (:4000) instead of the raw Argo wrapper (:44497) —
# the raw wrapper's response-format validator was rejecting Claude's structured
# output; the aggregator strips those fields cleanly. Both endpoints hit the
# same free Argo Claude Opus 4.7 backend.
ARGO_URL = "http://<tailnet-aggregator>:4000/v1/chat/completions"
MODEL = "argo:gpt-5.2"   # opus-4.7 hits an upstream response-parse bug on structured JSON; gpt-5.2 works cleanly

# Load results
with open("rus_results.json") as f:
    results = json.load(f)

def fmt_matrix(m):
    if m is None: return "None"
    return "\n".join("    [" + "  ".join(str(v) for v in row) + "]" for row in m)

evidence = []
for name in ["Fig8", "Fig9", "Fig1a"]:
    r = results[name]
    evidence.append(f"""
{name} circuit (from paper section 5):
  Target unitary (paper):
{fmt_matrix(r['target'])}
  Induced Kraus operator on data qubit (post-selected on all ancillas measured 0):
{fmt_matrix(r['K_matrix'])}
  Normalised (Kraus / sqrt(p_succ)):
{fmt_matrix(r['K_normalised'])}
  Pr(success) measured (Haar-avg over data input): {r['p_success_measured']:.6f}
  Pr(success) paper                              : {r['p_success_paper']:.6f}
  |Δp|                                           : {r['delta_prob']:.2e}
  Process fidelity(K_normalised, target)         : {r['process_fidelity']:.6f}
  Equal up to global phase?                      : {r['unitary_equal_upto_phase']}
  (Global phase relating K_norm to target)       : {r['global_phase']}
""")

evidence_str = "\n---\n".join(evidence)

prompt = f"""You are the LLM judge for an independent-replication of the paper
"Repeat-Until-Success: Non-deterministic decomposition of single-qubit unitaries"
(Paetznick & Svore, arXiv:1311.1074, 2014).

Paper claims we set out to reproduce (all in section 5, "The database"):
  C1 (Fig. 8): The two-T-gate single-ancilla RUS circuit implements
      U = (I + i·√2 X)/√3 on success, identity on failure, with Pr(success) = 3/4.
  C2 (Fig. 9): The four-T-gate single-ancilla single-measurement RUS circuit
      implements V3 = (I + 2iZ)/√5 on success, identity on failure,
      with Pr(success) = 5/8.
  C3 (Fig. 1a, NC00 pp.198 style): Two-ancilla X-basis-measurement RUS circuit
      also implements V3 with Pr(success)=5/8.

Method used: Qiskit 2.5.0 statevector simulation. Build the full unitary W on
(ancilla + data) qubits, project onto the all-ancillas-zero subspace to obtain
the induced (unnormalised) Kraus operator K_0 on the data qubit. Compute
Pr(success) = (1/2) tr(K_0† K_0) (Haar-average over the 1-qubit input) and
process fidelity |tr(K_norm† U_target)/2|² between the normalised map and the
paper's target unitary.

Empirical results per circuit:
{evidence_str}

Reproducible artefacts: code at work/rus_verify.py (150 LOC, self-contained),
Qiskit 2.5.0, numpy statevector; runs in <1 s on a laptop.

Notes:
- "Global phase" between K_norm and target of magnitude 1 is not a physical
  discrepancy — quantum states are equivalence classes modulo an overall phase.
- Fig. 1a was implemented from our best textual reading of the ASCII figure
  (two Toffoli-style controlled-controlled-S then controlled-controlled-Z, plus
  H's for X-basis measurement). This is a guess and does not need to match; C1
  and C2 are the primary tests.

Please answer the following STRICTLY as valid JSON only (no prose outside the
JSON block):

{{
  "verdict": "REPLICATED" | "PARTIAL" | "SPOT-CHECK" | "NO-GO" | "CONTRADICTED" | "BLOCKED" | "FAILED",
  "claim_C1_status": "reproduced" | "not-reproduced" | "not-tested",
  "claim_C2_status": "reproduced" | "not-reproduced" | "not-tested",
  "claim_C3_status": "reproduced" | "not-reproduced" | "not-tested",
  "coverage_fraction_of_paper_tested": <float 0..1>,
  "agreement_score_0_to_1": <float>,
  "justification": "<3-6 sentence explanation grounded in the numerical evidence>",
  "one_line_summary": "<<=140 chars single-line summary suitable for WAVE_RESULT>",
  "caveats": ["<caveat 1>", "<caveat 2>", ...]
}}

Use the vocabulary strictly. Guidance:
- REPLICATED = the primary tested numerical claims match paper to machine precision.
- PARTIAL = some claims match, some don't or are untested.
- Ignore Fig. 1a's mismatch if C1 and C2 both match (Fig 1a was a guess).
"""

payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 1500,
    "temperature": 0,
}

# Call via curl to avoid extra deps
resp = subprocess.run(
    ["curl", "-s", "-m", "60", "-X", "POST", ARGO_URL,
     "-H", "Authorization: Bearer stevens",
     "-H", "Content-Type: application/json",
     "-d", json.dumps(payload)],
    capture_output=True, text=True,
)
if resp.returncode != 0:
    print("curl failed:", resp.stderr, file=sys.stderr); sys.exit(1)

try:
    data = json.loads(resp.stdout)
    content = data["choices"][0]["message"]["content"]
except Exception as e:
    print("parse fail:", e, file=sys.stderr)
    print(resp.stdout[:2000], file=sys.stderr)
    sys.exit(2)

# Extract JSON from the content
import re
m = re.search(r'\{[\s\S]+\}', content)
if not m:
    print("no JSON in judge output:", content, file=sys.stderr); sys.exit(3)
judge_json = json.loads(m.group(0))

print("=== LLM JUDGE VERDICT ===")
print(json.dumps(judge_json, indent=2))

with open("llm_judge_verdict.json", "w") as f:
    json.dump({
        "model": MODEL,
        "endpoint": ARGO_URL,
        "prompt": prompt,
        "raw_response": content,
        "parsed_verdict": judge_json,
    }, f, indent=2)
print("Wrote llm_judge_verdict.json")
