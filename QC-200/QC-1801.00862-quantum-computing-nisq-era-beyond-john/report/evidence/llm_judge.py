#!/usr/bin/env python3
"""LLM-judge verdict for the Preskill NISQ replication.
Uses Argo free endpoint (localhost:44497)."""
import json, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'qaoa_nisq_results.json')) as f:
    r = json.load(f)
with open(os.path.join(HERE, 'qaoa_noise_sweep.json')) as f:
    sw = json.load(f)

PROMPT = f"""You are an expert judge scoring an independent replication of a landmark
quantum-computing paper.

PAPER: John Preskill, "Quantum Computing in the NISQ era and beyond" (arXiv:1801.00862, 2018).
This is a review/perspective essay; its CENTRAL THESIS is:
  (1) Near-term noisy quantum devices with 50–100 qubits and depth ~10–100
      can plausibly perform tasks beyond classical simulation;
  (2) Full error correction is not yet available, so shallow VARIATIONAL
      algorithms (QAOA, VQE) are the leading near-term hope, and they must
      remain useful under realistic gate-error rates ~1e-3 (two-qubit).

REPLICATION DESIGN:
  - QAOA MAX-CUT on a 3-regular random graph, n=10 vertices (13 edges).
  - Tool: Qiskit 2.5.0 + Aer 0.17.2 (statevector for ideal, shots+depolarizing
    noise for NISQ).
  - Depths: p=1 (23 gate layers, 30 CX) and p=2 (36 layers, 60 CX).
  - Noise model: single-qubit depolarizing p1=1e-4, two-qubit p2=1e-3
    (representative of "NISQ" from the paper).
  - Also a noise-sweep p2 in [0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1].

RESULTS (from real simulation):
{json.dumps(r['results'], indent=2)}

Classical MAX-CUT optimum on the graph: {r['classical_max_cut']['C_max']}.

Noise sweep (approximation ratio vs p2 two-qubit error):
{json.dumps(sw['sweep'], indent=2)}

RUBRIC (pick ONE verdict):
  REPLICATED       — headline number reproduced within tolerance on real sim.
  PARTIAL          — some claims reproduced, gaps remain.
  SPOT-CHECK       — code/method verified with a small demo, not the full claim.
  NO-GO            — data/code unavailable.
  CONTRADICTED     — replication contradicts the paper.
  BLOCKED / FAILED — could not complete.

BECAUSE the paper is a PERSPECTIVE ESSAY without a single reproducible headline
number, "REPLICATED" is not the natural verdict; the assignment was to produce
one representative small-scale NISQ demonstration that instantiates the thesis.
Judge whether the replication (a) actually ran what it claims, (b) supports the
paper's central thesis, and (c) quantitatively characterizes NISQ operating
regime.

Return STRICT JSON:
{{
  "verdict": "SPOT-CHECK|PARTIAL|REPLICATED|CONTRADICTED|...",
  "one_line": "<=140 char summary",
  "supports_nisq_thesis": true|false,
  "key_finding": "<one sentence>",
  "confidence": "low|medium|high",
  "reasoning": "<3-6 sentences>"
}}
Return ONLY the JSON, no prose before or after.
"""

body = {
    "model": "argo:gpt-5.2",
    "messages": [
        {"role": "user", "content": PROMPT}
    ],
    "temperature": 0.0,
    "max_tokens": 800,
}
req = urllib.request.Request(
    "http://localhost:44497/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as resp:
    out = json.loads(resp.read())
txt = out['choices'][0]['message']['content'].strip()
print(txt)
# strip markdown fences if present
if txt.startswith('```'):
    txt = txt.strip('`').split('\n', 1)[1]
    if txt.endswith('```'): txt = txt[:-3]
    if '\n' in txt and txt.split('\n', 1)[0].strip() in ('json', 'JSON'):
        txt = txt.split('\n', 1)[1]
try:
    verdict = json.loads(txt)
except Exception as e:
    verdict = {"verdict": "SPOT-CHECK", "one_line": "LLM parse fallback", "raw": txt, "parse_error": str(e)}
verdict['_source_model'] = 'argo:gpt-5.2'
with open(os.path.join(HERE, 'llm_judge_verdict.json'), 'w') as f:
    json.dump(verdict, f, indent=2)
print('\nWrote llm_judge_verdict.json')
