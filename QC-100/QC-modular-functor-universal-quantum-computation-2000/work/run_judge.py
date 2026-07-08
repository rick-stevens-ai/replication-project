#!/usr/bin/env python3
"""Call the free LiteLLM aggregator at cherryrd:4000 with Argo Opus 4.7 to
produce an LLM-judge verdict on the replication."""
import json, os, sys, subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

SYS_PROMPT = """You are an expert judge for a scientific-paper replication project.
You will be given a JSON summary of an independent numerical replication of a
theory paper on topological quantum computation:
  Freedman, Kitaev, Larsen, Wang (2000), "A modular functor which is universal for
  quantum computation", arXiv:quant-ph/0001108.

The paper's concrete testable content (what a numerical replication can check):
  C1  Hilbert-space dimensions of the SU(2)-Chern-Simons modular functor at r=5 on
       n-punctured disks with all punctures labeled 1:
         dim V_3^1 = 2, dim V_3^3 = 1, dim V_6^0 = 5, dim V_6^2 = 8   (paper Eq. 4)
  C2  The Jones-representation braid generators rho_lambda(sigma_i) are unitary
       for the (2,5)-Young diagrams lambda = [2,1], [3,3], [4,2].
  C3  The braid group and Temperley-Lieb algebra relations hold
       (sigma_i sigma_{i+1} sigma_i = sigma_{i+1} sigma_i sigma_{i+1};
        e_i e_{i+1} e_i = beta^{-1} e_i; commutativity for |i-j|>=2; etc.)
  C4  Every generator rho(sigma_i) has spectrum exactly {-1, q} with q = exp(2 pi i / 5).
  C5  For lambda = [4,2] the multiplicities are 3 (for -1) and 5 (for q) - Theorem 3.1(iv).
  C6  Density theorem (Theorem 4.1): the closure of rho(B_6) contains SU(5) x SU(8) - this is
       the substance of universality. A finite-sample numerical *check* of density is: (a)
       random braid words spread over SU(N)/center (not confined to a finite subgroup); and
       (b) explicit target-gate approximation improves with braid length.
  C7  Paper prints an explicit matrix for rho_{[2,1]}(sigma_2) in Section 3. Sanity-check.

Judge the following:
 1. Which claims are testable numerically at all (mark testable/not-testable).
 2. Which testable claims were reproduced (mark PASS/FAIL/PARTIAL).
 3. Overall verdict from the canonical vocabulary:
    REPLICATED  - core testable claims independently reproduced on real data.
    PARTIAL     - some claims reproduced, some out of reach.
    SPOT-CHECK  - data-availability + method plausibility verified, no full rerun.
    NO-GO / CONTRADICTED / BLOCKED / FAILED.
 4. A one-line summary <= 15 words.
 5. Coverage percent 0-100 (what fraction of the paper's testable content did this
    replication cover).
 6. Agreement percent 0-100 (of what was tested, how well does the numerical output
    agree with the paper).

BE CRITICAL. Ignore claims about full universality-for-BQP (that is a theorem, not
a numerically testable claim; the replication can only test the *ingredients* it uses).
The density theorem itself is not fully numerically provable, but empirical spread
of random braids and target-gate approximation are ingredients that would fail if
the density theorem were wrong.

Return STRICT JSON with keys:
  {"verdict": "...", "one_line": "...", "coverage_pct": <int>, "agreement_pct": <int>,
   "per_claim": [{"id": "C1", "testable": true, "status": "PASS", "note": "..."}, ...],
   "reasoning": "..." (2-4 paragraphs)}
"""

evidence = json.dumps(json.load(open("judge_input.json")), indent=2)
user_msg = f"Evidence JSON:\n\n{evidence}\n\nJudge this replication."

body = {
    "model": "argo:gpt-5.1",
    "messages": [
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user",   "content": user_msg},
    ],
    "temperature": 0.0,
    "max_tokens": 3000,
}
data = json.dumps(body)
out = subprocess.run(
    ["curl", "-sS", "-m", "180", "-X", "POST",
     "http://<tailnet-aggregator>:4000/v1/chat/completions",
     "-H", "Authorization: Bearer stevens",
     "-H", "Content-Type: application/json",
     "-d", data],
    capture_output=True, text=True, timeout=200,
)
if out.returncode != 0 or not out.stdout.strip():
    print("curl rc=", out.returncode, file=sys.stderr)
    print(out.stderr, file=sys.stderr)
    sys.exit(1)
payload = json.loads(out.stdout)

open("judge_response.json", "w").write(json.dumps(payload, indent=2))
content = payload["choices"][0]["message"]["content"]
open("judge_verdict.txt", "w").write(content)
print(content)
