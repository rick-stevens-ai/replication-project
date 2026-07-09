#!/usr/bin/env python3
"""LLM-judge scoring of the Gmunu replication.  Uses the Argo proxy (free).

Reads the summary evidence JSONs plus a compact statement of what the paper claims,
sends to the Argo LLM, and asks it to (1) score claim-by-claim agreement and
(2) recommend a verdict in the project vocabulary."""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ARGO = "http://127.0.0.1:44497/v1/chat/completions"
API_KEY = "stevens"
MODEL = os.environ.get("ARGO_MODEL", "argo:gpt-5")

def load(name):
    p = os.path.join(HERE, name)
    with open(p) as f:
        return json.load(f)

grid = load("grid_independence_summary.json")
order = load("order_of_accuracy.json")
fas = load("fas_nonlinear_summary.json")
pwc = load("pwc_restriction_summary.json")

paper_claims = """
The paper Cheong, Lin & Li (2020) 'Gmunu' (arXiv:2001.05723) presents an
axisymmetric general-relativistic hydrodynamics code with a nonlinear cell-
centred multigrid solver for the extended conformally-flat (xCFC) approximation
of the Einstein field equations.  The core numerical claims we intended to
independently reproduce (with a tight, hardware-appropriate scope) are:

C1  The multigrid algorithm as described (FAS V-cycle with red-black
    Gauss-Seidel smoother, nu_pre = nu_post = 15, piecewise-constant
    restriction, bilinear prolongation) yields textbook grid-independent
    convergence for elliptic problems.
C2  A deep V-cycle (V6) reaches the prescribed residual tolerance in tens of
    iterations from a flat initial guess (paper Fig 11: ~37 iterations for the
    highly non-spherical BU8 model at 640x64).
C3  A single-grid Gauss-Seidel (V1) requires O(10^5) iterations to reach the
    same tolerance and is orders of magnitude slower than V6 in equivalent
    fine-grid work.
C4  Convergence rate increases (monotonically) with V-cycle depth and then
    saturates once the coarse level is coarse enough.
C5  Second-order spatial accuracy (paper Sec 7.4) on smooth solutions.
C6  The FAS formulation genuinely handles nonlinearity, not just linear
    elliptic problems.
C7  The choice of restriction (piecewise-constant vs full-weighting) does not
    change the qualitative convergence story: the paper's exact stencil works
    too.

The full GRHD stack (WENO/MP5 reconstruction, HLLE Riemann, EoS, XNS initial
data, spherical (r,theta) grid, coupled 5-eq xCFC solve, BU8 mode-frequency
recovery, metric-solver amortization tests) is out of scope for this
python-only spot-check.
"""

evidence_summary = f"""
Evidence produced by this replication (all under report/evidence/):

1. Linear V-cycle spot-check (mg_poisson_spotcheck.py) — earlier run, 129x129
   grid, V1..V7 depths, 50 cycles max: V1 stagnates at ~2e-6 reduction in
   50 sweeps; V2 converges in 21 cycles; V3-V7 converge in 5-6 cycles.

2. Grid-independence (mg_grid_independence.py, summary below):
{json.dumps(grid, indent=2)}

3. Order-of-accuracy (mg_order_of_accuracy.py):
{json.dumps(order, indent=2)}

4. FAS nonlinear V-cycle for -Delta u + u^3 = f (mg_fas_nonlinear.py):
{json.dumps(fas, indent=2)}

5. Piecewise-constant restriction, cell-centred (mg_pwc_restriction.py):
{json.dumps(pwc, indent=2)}
"""

prompt = f"""You are the scoring judge for an independent-replication project.
You do NOT use regex or keyword matching; use your reasoning.  You never
inflate — only claim reproduction when the numeric evidence supports it.

The candidate paper and testable claims we asked to reproduce:
---
{paper_claims}
---

Actual independent-replication evidence:
---
{evidence_summary}
---

Please:
(A) For each claim C1..C7 above, give a one-line verdict from
    {{reproduced, partially_reproduced, consistent_but_not_definitive,
      not_tested, contradicted}} and one sentence citing the numeric evidence.
(B) Recommend an overall verdict from the project vocabulary:
    REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.
(C) In one paragraph, justify the verdict, honestly noting what was NOT
    reproduced (full xCFC nonlinear solve on a spherical grid, hydrodynamics,
    BU8 mode frequencies) and what WAS (the multigrid convergence mechanism
    itself in both linear and FAS-nonlinear form, grid-independence,
    second-order accuracy, single-grid vs deep V-cycle gap, and the paper's
    exact restriction stencil).

Return your answer as strict JSON with keys:
  \"per_claim\": [ {{\"id\":\"C1\",\"verdict\":\"...\",\"note\":\"...\"}}, ... ],
  \"overall_verdict\": \"PARTIAL\" (or whichever),
  \"justification\": \"...\"
"""

body = json.dumps({
    "model": MODEL,
    "messages": [
        {"role": "system", "content":
         "You are a numerical-PDE scoring judge for a replication project. "
         "Return valid JSON only.  Do not add commentary outside the JSON."},
        {"role": "user", "content": prompt},
    ],
}).encode()

req = urllib.request.Request(
    ARGO, data=body,
    headers={"Content-Type": "application/json",
             "Authorization": f"Bearer {API_KEY}"},
)
try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read().decode()
except urllib.error.HTTPError as e:
    sys.stderr.write(f"HTTP {e.code}: {e.read().decode()[:400]}\n")
    sys.exit(1)
except urllib.error.URLError as e:
    sys.stderr.write(f"URL error: {e}\n"); sys.exit(1)

try:
    parsed = json.loads(raw)
    content = parsed["choices"][0]["message"]["content"]
except Exception:
    content = raw

# Persist raw and (if valid JSON) parsed.
with open(os.path.join(HERE, "llm_judge_raw.json"), "w") as f:
    f.write(raw)
print("---- JUDGE RESPONSE ----")
print(content)
# Try to json.loads the content and save cleanly
try:
    obj = json.loads(content)
    with open(os.path.join(HERE, "llm_judge.json"), "w") as f:
        json.dump({"model": MODEL, "judgement": obj}, f, indent=2)
    print("\nWrote llm_judge.json")
except Exception as e:
    # Try to salvage: find outer braces
    a = content.find("{")
    b = content.rfind("}")
    if a >= 0 and b > a:
        try:
            obj = json.loads(content[a:b+1])
            with open(os.path.join(HERE, "llm_judge.json"), "w") as f:
                json.dump({"model": MODEL, "judgement": obj}, f, indent=2)
            print("\nWrote llm_judge.json (salvaged)")
        except Exception as e2:
            print(f"[warn] could not parse judge JSON: {e2}")
    else:
        print(f"[warn] could not parse judge JSON: {e}")
