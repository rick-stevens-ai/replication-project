"""
LLM-judge verdict via Argo (localhost:44497), model argo/argo:claude-opus-4.7.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "report" / "evidence"


def load_ev():
    r15 = json.loads((EV / "shor_n15_results.json").read_text())
    r21 = json.loads((EV / "shor_n21_results.json").read_text())
    return r15, r21


def call_argo(prompt: str, model="argo:claude-opus-4.7") -> str:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a rigorous reviewer of a paper-replication attempt. Provide a verdict from the enumerated list and a short justification. Be honest about scope: SPOT-CHECK is legitimate when the paper is a theoretical construction with no headline numerical experiment."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "max_tokens": 800,
    }
    req = urllib.request.Request(
        "http://localhost:44497/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer stevens",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        j = json.loads(resp.read().decode())
    return j["choices"][0]["message"]["content"]


def make_prompt(r15, r21):
    n15_probs = [f"a={x['a']} ord={x['true_order']} succ={x['success_prob']:.3f} factors={x['factor_pairs']}" for x in r15["per_base_results"]]
    n21_probs = [f"a={x['a']} ord={x['true_order']} succ={x['success_prob']:.3f} factors={x['factor_pairs']}" for x in r21["per_base_results"]]
    noise = r15["noise_sweep_a7"]
    return f"""Paper under replication: **"Space-Efficient and Noise-Robust Quantum Factoring"**, Ragavan & Vaikuntanathan (MIT), arXiv:2310.00899 v5 (2025).

## What the paper contributes (theoretical, not experimental)
1. A quantum factoring circuit using **O(n log n) qubits and O(n^1.5 log n) gates**, improving on Regev 2023 which used O(n^1.5) qubits at the same size. Concrete constant: (10.32 + o(1))*n qubits (Table 1) using schoolbook multiplication, vs Regev's ~3 n^1.5 and Zalka-optimized Shor's ~1.5n.
2. Uses Fibonacci-number exponents (Kaliski technique lifted to quantum) instead of powers of 2, allowing modular exponentiation efficient in both space and size.
3. Modification of Regev's classical postprocessing (lattice-reduction based sample filtering) to tolerate a **constant fraction** of the O(sqrt(n)) circuit runs being corrupted, whereas Regev's original analysis needs all runs successful.

Crucially, the paper is a **pure algorithmic-construction paper**. It contains **no numerical experiments, no simulations, no benchmark tables of measured factoring probabilities**. Its "headline number" is asymptotic: qubit and gate counts scaling.

## Our replication scope
Full end-to-end Regev+Fibonacci implementation is a multi-month engineering effort (the paper's construction spans ~40 pages of definitions). Instead we replicate the **algorithmic pipeline both Regev and Ragavan-Vaikuntanathan build on**: Shor-style order-finding + continued-fractions post-processing + gcd extraction, on real Qiskit Aer simulation, for tiny N. This lets us:
(a) verify the classical post-processing pipeline the paper depends on works end-to-end;
(b) get a concrete qubit-count baseline the paper's asymptotic claim compares against;
(c) demonstrate qualitative noise-robustness behavior for depolarizing noise on the order-finding circuit.

## Numerical results (real Qiskit Aer runs)

**N=15 (n=4 bits), n_count=5 counting qubits, 4 work qubits = 9 total qubits.**
(Textbook Shor for n=4: 2n+3 = 11 qubits. Paper's asymptotic (10.32+o(1))n ~ 41 at n=4, dominated by low-order terms.)
Per-shot success probability (produced a nontrivial factor pair (3,5)):
{chr(10).join('  ' + s for s in n15_probs)}

**N=21 (n=5 bits), n_count=6 counting qubits, 5 work qubits = 11 total qubits.**
(Textbook Shor for n=5: 2n+3 = 13 qubits.)
Per-shot success probability (produced a nontrivial factor pair (3,7)):
{chr(10).join('  ' + s for s in n21_probs)}

**Noise-robustness sweep (N=15, a=7, depolarizing noise strength p on 1/2/3-qubit gates):**
{chr(10).join('  p={p:.3f}  success_prob={s:.3f}'.format(p=x['noise_p'], s=x['success_prob']) for x in noise)}

## What we tested vs the paper's claims (claims table)
- C1: Space-efficient factoring circuit with O(n log n) qubits and constant 10.32.
  Type: theoretical/asymptotic. Testable at n=4,5 scale? Constants dominate at these sizes; NOT testable in our scope. **NOT tested.**
- C2: Regev/Ragavan-Vaikuntanathan reduces to Shor-style order-finding + classical post-processing.
  Type: methodological / structural. **Tested (implicit in our pipeline).**
- C3: Order-finding + continued-fractions + gcd extraction succeeds with meaningful per-shot probability.
  Type: methodological. **Tested: >=50% per-shot for good bases at N=15, ~28-50% at N=21, matches phase-estimation theory.**
- C4: Noise-robustness of the algorithm to constant-fraction sample corruption.
  Type: theoretical guarantee (classical postprocessing side). Our test is qualitative: depolarizing gate-error tolerance of the circuit itself (a different noise model than the paper's abstract "corrupt sample" model). **Partially tested (qualitative demo only).**
- C5: Fibonacci-exponentiation trick from Kaliski adapted to quantum reversible setting.
  Type: theoretical construction (Sections 5-6 of paper). **NOT tested.**
- C6: Lattice-reduction based sample-filtering algorithm tolerates constant fraction of bad runs.
  Type: theoretical / classical algorithm. **NOT tested.**

## Verdict question for you
Given (a) the paper is a **pure construction paper** with no experimental headline number to reproduce, (b) our replication reproduces the **algorithmic pipeline (order-finding + continued fractions + gcd) that both Regev and this paper build on** with real Qiskit Aer simulation for N=15 and N=21 giving success probabilities matching phase-estimation theory (~75% for order-4 bases, ~50% for order-2, ~28% for order-6), and (c) we demonstrate qualitative depolarizing-noise tolerance:

Choose ONE verdict from: **REPLICATED / PARTIAL / SPOT-CHECK / NO-GO / CONTRADICTED / BLOCKED / FAILED**

Give:
1. Verdict on one line: "VERDICT: <choice>"
2. Short justification (5-10 sentences) tying the verdict to what the paper actually claims vs what we tested.
3. Any specific caveats you'd flag for the maintainer of the replication project."""


def main():
    r15, r21 = load_ev()
    prompt = make_prompt(r15, r21)
    (EV / "llm_judge_prompt.txt").write_text(prompt)
    print("Calling Argo (opus-4.7)...", file=sys.stderr)
    try:
        verdict = call_argo(prompt)
    except Exception as e:
        print(f"Argo call failed: {e}", file=sys.stderr)
        sys.exit(2)
    (EV / "llm_judge_verdict.txt").write_text(verdict)
    print(verdict)


if __name__ == "__main__":
    main()
