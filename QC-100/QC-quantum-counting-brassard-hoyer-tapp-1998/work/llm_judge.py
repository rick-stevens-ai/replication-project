"""
LLM-judge scoring for the Quantum Counting replication.
Uses Argo free endpoint (localhost:44497, key=stevens).
"""
import json
import os
import subprocess
import sys

DIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/QC-quantum-counting-brassard-hoyer-tapp-1998")


def load_json(p):
    with open(p) as f:
        return json.load(f)


def load_text(p, max_chars=None):
    with open(p) as f:
        t = f.read()
    if max_chars:
        t = t[:max_chars]
    return t


def judge(prompt, model="argo:gpt-5.4", max_tokens=1500):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
    }
    r = subprocess.run(
        [
            "curl", "-sS", "-X", "POST",
            "http://localhost:44497/v1/chat/completions",
            "-H", "Authorization: Bearer stevens",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ],
        capture_output=True, text=True, timeout=180,
    )
    if r.returncode != 0:
        raise RuntimeError(f"curl failed: {r.stderr}")
    try:
        resp = json.loads(r.stdout)
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"bad response: {r.stdout[:2000]} err={e}")


def main():
    sweep = load_json(os.path.join(DIR, "report/evidence/sweep_results.json"))
    verify_log = load_text(os.path.join(DIR, "report/evidence/qiskit_verify_multi.log"))
    paper_txt = load_text(os.path.join(DIR, "work/paper.txt"), max_chars=15000)

    # Extract summary statistics from sweep
    n_total = len(sweep)
    n_within = sum(1 for r in sweep if r["argmax_within_bound"])
    n_success = sum(1 for r in sweep if r["success_prob_ge_8_over_pi2"])

    prompt = f"""You are a rigorous LLM judge evaluating whether a replication faithfully reproduces the core claims of the paper:

  "Quantum Counting" — Brassard, Høyer, Tapp (1998, arXiv:quant-ph/9805082)

The paper's key testable claims are:

  C1. Amplitude amplification generalizes Grover's algorithm to any A with initial success prob a > 0, yielding a Θ(1/√a) quadratic speedup (Theorems 1–3).

  C2. Quantum Counting algorithm Count(F, P): given a Boolean oracle F: {{0,...,N-1}} -> {{0,1}} with t marked items, using P counting qubits, outputs an estimate t̃ of t such that (Theorem 5)
      |t - t̃| < (2π / P) · √(t · N) + (π² / P²) · N
     with probability at least 8/π² ≈ 0.811.

  C3. Corollary 2: with P = c·√N, one gets |t - t̃| < (2π/c)·√t + (π²/c²), i.e. relative-error accuracy scales with c (the "counting-qubit budget").

  C4. Quadratic speedup for heuristic searches (Theorem 4) — mostly a structural claim; not usually reproduced numerically.

The replication being evaluated:

  - Fresh implementation of Count(F,P) in Python + Qiskit (statevector) by an independent agent.
  - Analytic-QPE marginal distribution (over the measured integer f) computed exactly:
       dist(f) = 1/2 P(f | phi_+) + 1/2 P(f | phi_-),
       where phi_+ = theta/pi, phi_- = 1 - theta/pi, sin^2(theta) = t/N,
       and P(f | phi) is the exact QPE Dirichlet-kernel probability.
  - Gate-level Qiskit circuit (H^p on counting, H^n on search, controlled-G^{{2^j}}
    on count_reg[j], then inverse QFT with swaps, measure counting register)
    cross-validated against the analytic distribution to L∞ ≤ 3e-15 across 7 diverse
    (n, t, p) cases (see attached verify log).
  - Sweep over N ∈ {{16, 32, 64}} (n=4,5,6), varying t and counting qubits p ∈ {{3,...,8}}.
  - For each (n, t, p) it records: t̂_argmax, |t - t̂|, the paper's Theorem-5 bound,
    and the exact probability that the measurement falls in the "success" set
    {{ f : |t - N sin²(π f / P)| < bound }} — this is what the paper says should be ≥ 8/π².

Sweep summary:
  - {n_total} (n, t, p) configurations swept.
  - Argmax within Theorem-5 bound: {n_within}/{n_total}.
  - Exact P(within bound) ≥ 8/π²: {n_success}/{n_total}.

Cross-verification (gate-level vs analytic):
{verify_log}

Sample rows from the sweep (first 20 of {n_total}):
{json.dumps(sweep[:20], indent=2)}

The paper text (first ~15k chars) is provided for reference:
====
{paper_txt}
====

Please judge, for each of C1–C3 (skip C4 which is not numerically reproduced), whether the replication:
  (a) tests the claim,
  (b) reproduces it (matches paper's quantitative bounds),
  (c) any caveats.

Then output a JSON block with the following fields (and nothing else at the end):
{{
  "verdict": one of "REPLICATED", "PARTIAL", "SPOT-CHECK", "NO-GO", "CONTRADICTED", "BLOCKED", "FAILED",
  "coverage": float in [0,1]  (fraction of testable claims that the replication actually tested),
  "agreement": float in [0,1] (of the tested claims, fraction reproduced within the paper's stated bounds/probability),
  "per_claim": {{
    "C1": {{ "tested": bool, "reproduced": bool, "note": "..." }},
    "C2": {{ "tested": bool, "reproduced": bool, "note": "..." }},
    "C3": {{ "tested": bool, "reproduced": bool, "note": "..." }}
  }},
  "one_line": "single sentence summary suitable for a WAVE_RESULT line",
  "reasoning": "1-2 paragraphs of judge reasoning"
}}
"""

    print("=== LLM-JUDGE PROMPT LENGTH ===")
    print(len(prompt), "chars")

    out = judge(prompt)
    print("=== LLM-JUDGE RAW OUTPUT ===")
    print(out)

    # save
    with open(os.path.join(DIR, "report/evidence/llm_judge_raw.txt"), "w") as f:
        f.write(out)

    # Try to extract JSON
    import re
    m = re.search(r"\{[\s\S]*\}\s*$", out.strip())
    if m:
        try:
            parsed = json.loads(m.group(0))
            with open(os.path.join(DIR, "report/evidence/llm_judge.json"), "w") as f:
                json.dump(parsed, f, indent=2)
            print("=== PARSED JUDGE JSON ===")
            print(json.dumps(parsed, indent=2))
        except Exception as e:
            print("failed to parse judge JSON:", e)


if __name__ == "__main__":
    main()
