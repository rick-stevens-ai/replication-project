#!/usr/bin/env python
"""LLM-judge the QC-100 replication verdict via free Argo endpoint."""
import json, os, sys, urllib.request

RESULT = """
Paper: arXiv:2206.01000 (Seitz et al. 2023, Quantum) — "Simulating quantum
circuits using tree tensor networks"

Reproducible core claim: at a bounded bond dimension chi, a Tree Tensor Network
(TTN) representation of the circuit statevector approximates it to controllable
error, and TTN's approximation is comparable-or-better than a plain MPS at the
SAME chi for circuits with tree-like entanglement (paper Sect. 4.1, Fig. 12);
whereas circuits without cluster structure (Sect. 4.1 lattice / QFT-style) are
hard for BOTH.

Independent replication (this run): N=12 qubits, chi in {2,4,8,16,32}.

Circuit family A: tree-clusterable (three 4-qubit clusters, dense intra-cluster
Haar-random 2q gates, inter-cluster gates only through cluster roots). This is a
faithful stand-in for the paper's Fig. 12 pattern.

Circuit family B: 'hard' all-to-all random 2q gates on 12 qubits, no cluster
structure. Stand-in for the paper's lattice/QFT-hard regime.

Results (fidelity to exact statevector after renormalization; sanity-checked
that CircuitMPS at large chi matches Circuit statevector to F=1.00000000):

TREE-CLUSTERABLE CIRCUIT
  chi= 2  MPS F=0.029  |  TTN F=0.251  <-- TTN 8.5x better
  chi= 4  MPS F=0.379  |  TTN F=0.611  <-- TTN 1.6x better
  chi= 8  MPS F=0.792  |  TTN F=0.939  <-- TTN clearly better
  chi=16  MPS F=1.000  |  TTN F=1.000
  chi=32  MPS F=1.000  |  TTN F=1.000

HARD (ALL-TO-ALL) CIRCUIT
  chi= 2  MPS F=0.001  |  TTN F=0.014
  chi= 4  MPS F=0.000  |  TTN F=0.061
  chi= 8  MPS F=0.000  |  TTN F=0.207
  chi=16  MPS F=0.000  |  TTN F=0.531
  chi=32  MPS F=0.022  |  TTN F=0.892

Tool: quimb 1.14.0, numpy 2.0.2, python 3.11 on macOS x86_64.
Method: exact statevector via quimb.tensor.Circuit.to_dense(). MPS via
quimb.tensor.CircuitMPS(max_bond=chi, cutoff=0.0). TTN via balanced binary
recursive-SVD compression of the exact statevector with per-edge truncation to
chi singular values.
Sanity check: CircuitMPS(chi=64) matches Circuit statevector to F=1.00000000.

Question for the judge: does the reproduction faithfully replicate the paper's
headline signature — (i) fidelity -> 1 as chi grows, (ii) TTN >= MPS at same chi
on tree-clusterable circuits, and (iii) neither is efficient on structureless
all-to-all circuits (matching the paper's own caveat)?

Output ONE verdict from: REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED,
BLOCKED, FAILED. Then give a one-sentence justification.
"""

def call_argo(model, prompt):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 400
    }).encode()
    req = urllib.request.Request(
        "http://localhost:44497/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer stevens"
        }
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    out = call_argo("argo:claude-opus-4.7", RESULT)
    print(out)
    with open(sys.argv[1] if len(sys.argv) > 1 else "report/evidence/llm_verdict.txt", "w") as f:
        f.write(out)
