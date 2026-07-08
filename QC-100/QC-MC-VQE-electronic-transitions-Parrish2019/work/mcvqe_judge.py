#!/usr/bin/env python3
"""LLM-judge verdict for the MC-VQE replication. Free Argo endpoint only."""
import json, os, sys, urllib.request

ARGO = "http://localhost:44497/v1/chat/completions"
KEY = os.environ.get("ARGO_API_KEY", "stevens")

def call(model, prompt):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role":"system","content":"You are a meticulous computational-physics replication auditor. Judge ONLY on the evidence given. Output strict JSON."},
            {"role":"user","content": prompt},
        ],
        "temperature": 0.0,
    }).encode()
    req = urllib.request.Request(ARGO, data=body,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"]

def main():
    results = json.load(open(sys.argv[1]))
    prompt = f"""Replication target paper:
Parrish, Hohenstein, McMahon, Martinez, "Quantum Computation of Electronic
Transitions using a Variational Quantum Eigensolver" (MC-VQE), PRL 122, 230401
(2019); arXiv 1901.01234.

The paper's key quantitative claims (all from classical statevector simulation):
- C1: the ab-initio exciton Hamiltonian is isomorphic to a spin-lattice model and
  can be diagonalized (FCI) in the full 2^N Hilbert space.
- C2: single-layer MC-VQE reproduces FCI excitation energies to ~tens of microeV
  (max deviation) for the LH2 ring; low-meV for other cases.
- C3: MC-VQE oscillator strengths deviate <<1% from FCI, while CIS deviates 10%+.
- C4: CIS blue-shifts excitation energies by a few 0.01 eV vs FCI.
- C5: minimizing the state-averaged energy == minimizing the mean of the diagonal
  contracted-Hamiltonian elements (Eq. 6, exact identity via trace).
- C6: ~100 MC-VQE parameters converge in ~14 L-BFGS iterations from a
  zero-entanglement guess (N=18 ring, 108 params).
- C7: for an N=8 linear BChl-a stack CIS is qualitatively wrong while MC-VQE
  matches FCI.

Independent replication results (JSON, from a from-scratch NumPy/SciPy
reimplementation; exact TeraChem monomer data was NOT public so a physically
faithful BChl-a parametrization + dipole/transition-dipole two-body model was
used; the paper's claims are about method accuracy which is geometry-robust):

{json.dumps(results, indent=2)}

Notes on the metrics:
- *_matched_* = errors after matching each MC-VQE/CIS eigenstate to its
  maximum-overlap FCI state, restricted to states with >50% single-excitation
  character (the ansatz subspace). Double-excitation-dominated FCI states are
  outside any singles ansatz and are excluded (a known ansatz limitation, not a
  method failure).
- c5_residual = |state_avg_E - mean_diagonal_contracted_H|.
- n_lbfgs_iters, nparam address C6.

Assess claim-by-claim whether the replication supports each claim. Then give an
overall verdict from EXACTLY this vocabulary: REPLICATED, PARTIAL, SPOT-CHECK,
NO-GO, CONTRADICTED, BLOCKED, FAILED. Also give integer Coverage/10 (how many
testable claims were actually tested) and Agreement/10 (how well the numbers
agree with the paper).

Output strict JSON:
{{"claims": {{"C1": "...", "C2":"...", ...}}, "verdict":"<WORD>",
"coverage":<int>, "agreement":<int>, "justification":"..."}}"""

    for model in ["argo:gpt-5.2", "argo:claude-opus-4.8"]:
        try:
            out = call(model, prompt)
            print(f"===== JUDGE {model} =====")
            print(out)
            open(f"judge_{model.replace(':','_').replace('.','_')}.txt","w").write(out)
            break
        except Exception as e:
            print(f"[{model} failed: {e}]")

if __name__ == "__main__":
    main()
