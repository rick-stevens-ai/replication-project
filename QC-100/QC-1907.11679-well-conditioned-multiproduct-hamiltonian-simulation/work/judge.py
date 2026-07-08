"""LLM-judge over the Argo free proxy: given the paper claims and our numerical
evidence, ask for a verdict from the canonical vocabulary."""

import json
import os
import urllib.request
from pathlib import Path

evidence_dir = Path(__file__).parent.parent / "report" / "evidence"
slopes = json.loads((evidence_dir / "03_slopes.json").read_text())
bench = json.loads((evidence_dir / "02_benchmark_N4_t1.json").read_text())

# Compact evidence summary
def fmt_rows(rows):
    lines = []
    for r in rows:
        s = r["slope_fit"]
        s_str = "n/a (hit FP floor)" if s is None or (isinstance(s, float) and s != s) else f"{s:+.2f}"
        lines.append(f"  {r['method']:22s} 2m={r['order_2m']:>2}  ||a||_1={r['cond_a_1']:6.3f}  ||k||_1={r['k_1']:>3}  fit_slope={s_str}  min_err={r['min_err']:.2e}")
    return "\n".join(lines)

evidence_text = f"""
Independent replication of arXiv:1907.11679 (Low, Kliuchnikov, Wiebe 2019,
"Well-conditioned multiproduct Hamiltonian simulation").

Setup: 1D Heisenberg model H = sum_j (X_j X_{{j+1}} + Y_j Y_{{j+1}} + Z_j Z_{{j+1}})
on N=4 spins with periodic boundary conditions, evolved for time t=1.0 (||H||_2 = 8.0).
Compared exact matrix-exponential to product-formula and multiproduct approximations,
computed operator-norm error at increasing step counts r = 1..200.

Coefficient constructions tested:
  - Chin (arithmetic k_j = j, Eq. 5): closed-form, ill-conditioned.
  - Chebyshev-based closed-form (Eqs. 8-9): well-conditioned real exponents.
  - Rounded integer (Eq. 10): the paper's Theorem-1 explicit construction.
  - Paper's Appendix A tabulated integer coefficients (m=2..6, transcribed
    verbatim from the PDF, values entered as exact Fractions).

Numerical results (t=1.0, N=4):
{fmt_rows(slopes["rows"])}

Key numerical findings:
 (F1) Cancellation conditions Va = e_1 solved to machine precision (max residual
      < 1e-15) for every construction and every order.
 (F2) Empirical global-error slope in the clean regime (before FP floor) matches
      the theoretical prediction of -(2m) to within roughly +/-5% for all
      integrator orders 2m=2..12. For example:
        U4 (2m=4)                slope -3.84 vs expected -4
        Chin m=3 (2m=6)          slope -6.13 vs expected -6
        Chin m=5 (2m=10)         slope -10.39 vs expected -10
        Paper table m=5 (2m=10)  slope -10.39 vs expected -10
        Paper table m=6 (2m=12)  slope -11.45 vs expected -12
 (F3) Condition number ||a||_1 scaling (main claim of Theorem 1):
        Chin:                 1.42 -> 3.13 -> 6.21 -> 12.69 -> 26.44  (exp growth)
        Paper Appendix A:     1.67 -> 1.33 -> 1.40 -> 1.37 -> 1.53    (bounded ~O(log m))
        Rounded integer:      1.25 -> 1.59 -> 1.95 -> 1.66 -> 1.81    (bounded)
      Chin's ||a||_1 approximately doubles per unit m (consistent with e^Omega(m));
      the well-conditioned constructions are numerically indistinguishable from a
      logarithmic upper bound over the tested range.
 (F4) The Appendix A tabulated coefficients (which we entered as exact Fractions
      from the paper PDF) satisfy the cancellation equations to machine precision.
      This directly verifies that the coefficient tables published in the paper
      are correct.
 (F5) Both the closed-form Chebyshev construction and the rounded-integer variant
      independently reproduce the well-conditioning; both are non-trivial: the
      Chebyshev construction uses cot(pi(2j-1)/4m) coefficients and sin^{-2}(...)
      exponents (Eqs. 8-9); the rounded-integer version uses ceil(K * k'_j) with
      the smallest K that yields unique integers.

Not tested (out of local-simulation scope):
 (X1) The full quantum-circuit implementation via LCU / oblivious amplitude
      amplification (paper's Sec. "Hamiltonian simulation in the worst-case").
      We simulate classically by taking the literal linear combination of
      operators, which is what the LCU circuit implements on average.
 (X2) The commutator-dependent bound of Theorem 3.
 (X3) Larger system-size scaling (Fig. 2 middle/right panels used N up to ~50);
      classical simulation cost is exponential in N so we cap at N=4-6.

Given the above, choose ONE verdict from this fixed vocabulary:
  REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.

Definitions:
  REPLICATED = core claims independently reproduced on real data / with real code
  PARTIAL    = some claims reproduced, some out of reach
  SPOT-CHECK = availability & plausibility verified, no full rerun
  CONTRADICTED = rerun disagrees with paper
  BLOCKED / FAILED = external blocker / technical failure

Return JSON: {{"verdict": "...", "confidence": 0-1, "justification": "one paragraph",
"one_line_summary": "at most 20 words"}}.
"""

payload = {
    "model": "argo:gpt-5",
    "messages": [
        {"role": "system", "content": "You are a rigorous replication-verdict judge. Reply with JSON only."},
        {"role": "user", "content": evidence_text},
    ],
    "max_tokens": 4000,
}

req = urllib.request.Request(
    "http://127.0.0.1:44497/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer stevens",
    },
)

with urllib.request.urlopen(req, timeout=180) as resp:
    body = resp.read().decode()

print(body)
Path(evidence_dir / "04_judge_raw.json").write_text(body)

# Extract JSON verdict from content
import re
data = json.loads(body)
content = data["choices"][0]["message"]["content"]
print("\n=== Judge content ===")
print(content)

# Try to parse embedded JSON
m = re.search(r"\{.*\}", content, re.S)
if m:
    verdict_obj = json.loads(m.group(0))
    Path(evidence_dir / "05_judge_verdict.json").write_text(json.dumps(verdict_obj, indent=2))
    print("\n=== Parsed verdict ===")
    print(json.dumps(verdict_obj, indent=2))
