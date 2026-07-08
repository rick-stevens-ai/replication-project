"""LLM-judge scoring via Argo free endpoint (Claude Opus 4.7).

Reads the replication evidence (numeric_results.json + monotonicity check) and asks the model
to score coverage/agreement/verdict for Grover (quant-ph/0503205).
"""
import json
import os
import sys
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
EVIDENCE = BASE / "report" / "evidence"

numeric = json.loads((EVIDENCE / "numeric_results.json").read_text())
monotone_txt = (EVIDENCE / "monotonicity_check.txt").read_text()

paper_summary = """
Paper: Lov Grover, "A different kind of quantum search", arXiv:quant-ph/0503205 (2005).

Key claims:
  C1. Replacing selective phase inversions (phase pi) in Grover with phase shifts of pi/3
      converts the algorithm into a fixed-point search that converges MONOTONICALLY
      toward the target state (no overshoot), in contrast to standard Grover which
      oscillates.
  C2. If ||U_ts||^2 = 1 - epsilon (base success probability), then the single application
      of the transformation  U R_s U^dag R_t U  yields P(target) = 1 - epsilon^3.
  C3. The recursion  U_{m+1} = U_m R_s U_m^dag R_t U_m  yields
        ||U_{m,ts}||^2 = 1 - epsilon^(3^m),
      i.e. the failure probability collapses triple-exponentially in m.
  C4. For a database of size N=16 (uniform superposition, one marked element),
      standard Grover's success probability oscillates as a function of iteration k;
      the pi/3 recursion is monotone.
""".strip()

evidence_summary = f"""
Replication (independent, numpy statevector, N=16, M=1 marked, target index 5):

Base probability P0 = |U_ts|^2 = {numeric['base_probability_P0']:.6f}
Base epsilon      = 1 - P0    = {numeric['base_epsilon']:.6f}

Standard Grover P(target) vs iteration k = 0..12:
{numeric['standard_grover_probs']}
Max success = {numeric['standard_grover_max_prob']:.6f} at k = {numeric['standard_grover_argmax_iter']}
(Clear oscillation: rises to ~0.96 at k=3, drops to ~0.02 at k=6, rises to 0.99 at k=9, ...)

pi/3 recursion levels m = 0..4:
"""
for r in numeric["pi3_recursion"]:
    evidence_summary += (
        f"  m={r['m']}  q(U-calls)={r['queries_U_calls']:4d}  "
        f"P_measured={r['P_target_measured']:.10f}  "
        f"P_theory(1 - eps^(3^m))={r['P_target_theoretical']:.10f}  "
        f"|err|={r['abs_error']:.2e}\n"
    )

evidence_summary += "\nMonotonicity check:\n" + monotone_txt

prompt = f"""You are an expert quantum-information reviewer acting as a strict but fair replication judge.

PAPER UNDER REPLICATION:
{paper_summary}

REPLICATION EVIDENCE PRODUCED IN THIS RUN:
{evidence_summary}

Your task: score the replication against the paper's claims C1-C4.

Return a strict JSON object with these fields (no prose outside JSON):
{{
  "claim_scores": {{
    "C1": {{"tested": true|false, "reproduced": true|false, "comment": "..."}},
    "C2": {{"tested": true|false, "reproduced": true|false, "comment": "..."}},
    "C3": {{"tested": true|false, "reproduced": true|false, "comment": "..."}},
    "C4": {{"tested": true|false, "reproduced": true|false, "comment": "..."}}
  }},
  "coverage_fraction": <fraction of the paper's testable claims that this run tested, 0..1>,
  "agreement_fraction": <of tested claims, fraction reproduced, 0..1>,
  "verdict": "REPLICATED" | "PARTIAL" | "SPOT-CHECK" | "NO-GO" | "CONTRADICTED" | "BLOCKED" | "FAILED",
  "one_line": "<=140-char summary suitable for WAVE_RESULT",
  "justification": "3-6 sentence justification citing specific numbers"
}}
Guidance: REPLICATED means core testable claims independently reproduced on real (or in this case, independently simulated) evidence to within reasonable numerical tolerance. Be honest, not inflationary."""

url = "http://127.0.0.1:44497/v1/chat/completions"
body = json.dumps({
    "model": "argo:gpt-4o",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.0,
    "max_tokens": 1500,
}).encode()

req = urllib.request.Request(
    url,
    data=body,
    headers={
        "Authorization": "Bearer stevens",
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode()
except Exception as e:
    print(f"LLM call failed: {e}", file=sys.stderr)
    sys.exit(2)

data = json.loads(raw)
content = data["choices"][0]["message"]["content"]

# Find the JSON block
import re
m = re.search(r"\{.*\}", content, re.DOTALL)
if not m:
    print("No JSON found in LLM response:", file=sys.stderr)
    print(content, file=sys.stderr)
    sys.exit(3)
try:
    verdict_json = json.loads(m.group(0))
except json.JSONDecodeError as e:
    # try to fix trailing prose
    print(f"Failed to parse LLM JSON: {e}", file=sys.stderr)
    print(content, file=sys.stderr)
    sys.exit(4)

out = EVIDENCE / "llm_judge.json"
out.write_text(json.dumps({
    "model": "argo:gpt-4o",
    "endpoint": url,
    "raw_response": content,
    "parsed": verdict_json,
}, indent=2))
print(json.dumps(verdict_json, indent=2))
print(f"\n[save] LLM judge -> {out}")
