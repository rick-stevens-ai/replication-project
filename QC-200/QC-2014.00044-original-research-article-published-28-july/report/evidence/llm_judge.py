#!/usr/bin/env python3
"""LLM-judge verdict via Argo (localhost:44497, key=stevens, FREE).

Judges whether the reproduction faithfully tests the paper's central claim and
whether the observed numerical results support the claim.
"""
import json
import os
import sys
import urllib.request

# Prefer the litellm aggregator on cherryrd:4000 (has full Argo model set),
# falling back to the raw Argo wrapper on :44497.
ARGO_URLS = [
    "http://localhost:4000/v1/chat/completions",
    "http://<tailnet-aggregator>:4000/v1/chat/completions",
    "http://localhost:44497/v1/chat/completions",
]

paper_title = "Fourier-transforming with quantum annealers (Hen 2014, Frontiers in Physics 2:44)"
paper_claim = """
The paper introduces three adiabatic Hamiltonians that are claimed to reproduce
the Hadamard, controlled-phase-shift, and CNOT gates using an ancilla qubit that
ends in |1> at theta_f = pi. Specifically:
- Eq. (3) with Eqs. (4)-(5): adiabatic Hadamard, target = Eq. (8)
- Eq. (10): adiabatic controlled-phase-shift(phi), target = Eq. (11)
- Eq. (12): adiabatic CNOT, target = Eq. (13)
The paper concludes: "these 'adiabatic gates' may be used in a sequence to
construct the algorithm of Quantum Fourier Transform" with "no additional
complexity cost or resource overhead."
"""

reproduction = """
An independent statevector simulation was implemented using numpy + scipy.expm
(no Trotter approximation between slices; midpoint-rule schedule at N=2000-3000
time slices; theta_f=pi; T=20-25 in natural units so T*gap >> 1 for the paper's
stated constant gap = 2). The three adiabatic Hamiltonians were written LITERALLY
as printed in the paper (Eqs. 3-5, 10, 12). Fidelity was measured two ways:
  (a) full 2- or 3-qubit fidelity against (Gate|psi_data>) ⊗ |1>_aux
  (b) post-selecting on aux=|1>, then computing fidelity of the renormalized
      data register vs Gate|psi_data> ("fid_proj")

Key numerical outcomes (all fid <= 1.0):

Controlled-phase-shift (5 values of phi from pi/8 to 3pi/4, random 2-qubit input):
  fid_full = 0.999973  fid_proj|aux=1 = 1.000000  P(aux=1) = 0.999973
  (identical across ALL 5 phi values — this IS the paper's claim reproduced.)

CNOT (4 computational-basis inputs + 5 random 2-qubit states):
  fid_full = 0.999973  fid_proj|aux=1 = 1.000000  P(aux=1) = 0.999973
  (identical across ALL 9 inputs — this IS the paper's claim reproduced.)

Adiabatic Hadamard (5 random single-qubit input states, aux starts in |0>):
  trial 0: fid_full=0.223  fid_proj|aux=1=0.225  P(aux=1)=0.995
  trial 1: fid_full=0.049  fid_proj|aux=1=0.049  P(aux=1)=0.995
  trial 2: fid_full=0.092  fid_proj|aux=1=0.092  P(aux=1)=0.995
  trial 3: fid_full=0.522  fid_proj|aux=1=0.525  P(aux=1)=0.995
  trial 4: fid_full=0.196  fid_proj|aux=1=0.197  P(aux=1)=0.995
  Convergence sweep (N=50..5000): fidelity plateau ~0.293 (Trotter-independent).

Additional check: composing IDEAL H, CP-shift, CNOT (which the adiabatic gates
are claimed to equal) into the standard 3-qubit QFT circuit reproduces the
textbook QFT_3 matrix at fidelity 1.000000. So the *composition scheme* the
paper proposes is correct — the anomaly is isolated to whether the printed
Hadamard Hamiltonian (Eq. 3 with Eqs. 4-5) implements the intended target.

Four sign-convention variants of the Hadamard Hamiltonian were also tested
(swapping subspaces, flipping the sign of the sigma_y term, flipping sigma_x)
and NONE achieved fid > ~0.6 across all four random inputs. The aux qubit
still ended in |1> at ~99.5% for every variant.
"""

judge_prompt = f"""You are an expert quantum-computing referee judging an independent
replication. Score honestly.

Paper: {paper_title}

Paper claim:
{paper_claim}

Independent replication:
{reproduction}

Please answer, in JSON with keys "verdict", "confidence", "justification":
1. verdict — one of: REPLICATED, PARTIAL, SPOT-CHECK, CONTRADICTED, NO-GO, FAILED.
   Definitions per project standard:
   - REPLICATED = headline claim reproduced within tolerance on a real sim
   - PARTIAL    = some claims reproduced, not all
   - SPOT-CHECK = code/method verified, small demo, not full claim
   - CONTRADICTED = a claim was tested and found FALSE
   - NO-GO      = data/code unavailable to test
   - FAILED     = infrastructure/setup blocked the test
2. confidence — 0.0..1.0
3. justification — 3-6 sentences, cite the fidelity numbers

Return ONLY the JSON, nothing else.
"""

body = {
    "model": "argo:gpt-5.2",
    "messages": [
        {"role": "system", "content": "You are a rigorous quantum-computing referee. Return valid JSON only."},
        {"role": "user", "content": judge_prompt},
    ],
    "temperature": 0.0,
}

last_err = None
for url in ARGO_URLS:
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode()
        print(f"=== Raw response from {url} ===")
        print(raw[:2000])
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
        print("\n=== Judge content ===")
        print(content)
        with open("llm_judge_response.json", "w") as f:
            json.dump({"endpoint": url, "prompt": judge_prompt, "response_raw": raw, "response_content": content}, f, indent=2)
        print("\nSaved to llm_judge_response.json")
        break
    except Exception as e:
        print(f"[{url}] failed: {e}", file=sys.stderr)
        last_err = e
else:
    print(f"All Argo endpoints failed. Last error: {last_err}", file=sys.stderr)
    sys.exit(1)
