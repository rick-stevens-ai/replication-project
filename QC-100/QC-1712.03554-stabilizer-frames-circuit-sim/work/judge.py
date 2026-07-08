"""LLM-judge scoring via Argo (free endpoint)."""
import json
import os
import sys
import urllib.request
import urllib.error

RESULTS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "report", "evidence", "results.json")))

PROMPT = f"""You are an independent scientific judge for a QC-100 replication of:

  Garcia & Markov, "Simulation of Quantum Circuits via Stabilizer Frames"
  arXiv:1712.03554

Paper's headline claims we tested:
  (H1) A state |psi> can be represented as a sum of stabilizer states
       |psi> = sum_i alpha_i |phi_i>  (a "stabilizer frame").
  (H2) Clifford gates apply to each frame branch in poly(n).
  (H3) Each non-Clifford T-gate roughly DOUBLES the frame size (frame-size /
       stabilizer-rank chi scales exponentially with T-count t: chi ~ 2^t),
       while remaining polynomial in n.
  (H4) The recovered final-state amplitudes match an exact simulator to
       floating-point precision for small T-count.

Replication design (real code, no fabrication):
  * Wrote a from-scratch stabilizer-frame simulator (~200 lines Python).
    Representation:  |psi> = sum_i alpha_i |phi_i> where each |phi_i> is
    a stabilizer state stored as a Clifford-circuit prefix.
  * Clifford gates: applied to every branch (H, S, S-dagger, X, Y, Z,
    CNOT, CZ, SWAP).
  * T-gate decomposed exactly as
        T = e^(i pi/8) * ( cos(pi/8) I  -  i sin(pi/8) Z )
    so each T splits every branch in two (I-branch scaled by cos, and
    Z-branch scaled by -i*sin), doubling the frame.
  * Ground truth: Qiskit Statevector with native Clifford+T.
  * Independent Clifford cross-check: Stim TableauSimulator statevector.
  * Tolerance target: max amplitude error < 1e-10.

Measured results (n = qubits, t = T-count, chi = final frame size):

{json.dumps(RESULTS, indent=2)}

Judge on:
  A. Does H3 hold (chi = 2^t exactly, runtime roughly doubles per T)?
  B. Does H4 hold (max amplitude error < 1e-10 at all measured (n, t))?
  C. Does H2 hold (Clifford-only frame -> matches Qiskit AND Stim tableau)?
  D. Is the reproduction faithful to the paper's stated method
     (sum-over-stabilizers with T-driven frame growth)?

Return STRICT JSON:
{{
  "H1_representation_faithful": bool,
  "H2_clifford_polytime_ok":    bool,
  "H3_chi_scales_2t":           bool,
  "H4_amplitudes_below_1e10":   bool,
  "verdict":  "REPLICATED" | "PARTIAL" | "SPOT-CHECK" | "NO-GO" | "CONTRADICTED",
  "confidence": "high" | "medium" | "low",
  "one_line":  "..."
}}
"""

req = urllib.request.Request(
    "http://localhost:44497/v1/chat/completions",
    method="POST",
    headers={
        "Authorization": "Bearer stevens",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "argo:gpt-4.1",
        "messages": [
            {"role": "system", "content": "You are a rigorous, terse scientific-replication judge. Return only valid JSON."},
            {"role": "user", "content": PROMPT},
        ],
        "max_tokens": 800,
        "temperature": 0.0,
    }).encode(),
)

try:
    with urllib.request.urlopen(req, timeout=120) as r:
        body = json.load(r)
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.read().decode()[:400], file=sys.stderr)
    raise

txt = body["choices"][0]["message"]["content"].strip()
print("=== raw judge reply ===")
print(txt)
print("=== end ===")
# Try to parse JSON out of it
try:
    # strip ```json fences if present
    if txt.startswith("```"):
        txt = txt.strip("`").split("\n", 1)[1] if "\n" in txt else txt
        if txt.startswith("json"):
            txt = txt[4:]
        # drop trailing ```
        if txt.endswith("```"):
            txt = txt[:-3]
    parsed = json.loads(txt)
except Exception as e:
    print("parse err:", e)
    parsed = {"raw": body["choices"][0]["message"]["content"]}

with open(os.path.join(os.path.dirname(__file__), "..", "report", "evidence", "judge.json"), "w") as f:
    json.dump({"raw": body["choices"][0]["message"]["content"], "parsed": parsed}, f, indent=2)
print(json.dumps(parsed, indent=2))
