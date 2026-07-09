import json, urllib.request
prompt = """You are a strict scientific-replication judge. A subagent independently reimplemented the CORE mechanism of a paper and ran a reduced-compute test. Score honestly.

PAPER (OSTI 2866316, Wang/Wong/Ruan/Goswami 2026): "Causality-Respecting Adaptive Refinement for PINNs." Core contribution = causality-training for PINNs (Eqs 9-11: temporal residual slabs weighted by omega_k = exp(-eps * sum_{m<k} Lr(t_m)), eps=10) + residual-based adaptive refinement (RBAR), applied to a phase-field Allen-Cahn equation. Paper benchmarks against COMSOL FEM (proprietary) and reports mainly qualitative/figure-based accuracy gains from RBAR+causality vs vanilla PINN; central claim: vanilla PINNs converge to LOW training loss but WRONG Allen-Cahn solutions ('erroneous convergence'), and causality+RBAR fixes this.

REPLICATION performed:
- Correctly implemented causality weighting (Eqs 9-11, eps=10) in PyTorch; verified weights active (later time-slabs down-weighted, wmin->0).
- Tested on the CANONICAL 1D Allen-Cahn PINN benchmark (u_t = 1e-4 u_xx +5u -5u^3, u(0,x)=x^2 cos(pi x), periodic BC) -- the exact testbed from the causality method's origin paper (ref [18], Wang-Sankaran-Perdikaris 2022) -- because COMSOL phase-field data is unavailable. Ground truth = independent Fourier spectral (IMEX) solver.
- Reduced compute: 4-layer 128-wide tanh MLP, 12000 Adam iters each, 64 time-slabs x 200 spatial pts, soft IC/BC.

RESULTS (global relative-L2 vs spectral reference):
- Vanilla PINN: 0.692 (training loss converged to ~1e-2 yet solution 69% wrong)
- Causal PINN (eps=10): 0.861
- Per-time: BOTH accurate early (t<0.1, err 1-6%) and degrade to ~100% error by t=1.

KEY OBSERVATIONS:
1. REPRODUCED the paper's motivating pathology: low training loss + wrong solution (vanilla converged to 1e-2 loss but 69% L2 error).
2. REPRODUCED the qualitative error-growth structure (accurate early times, degrading late).
3. Did NOT reproduce the improvement claim: causal alone (no RBAR, reduced iters, soft BC, no Fourier features) did not beat vanilla; both fail at this compute budget. The origin causality papers use ~200k-300k iters, hard BC constraints, and Fourier features to succeed; RBAR (the paper's second half) was not implemented.

Give: (a) coverage of testable claims, (b) which claims reproduced vs not, (c) a single verdict from {REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED}, (d) 2-sentence justification. Be honest that the improvement claim was NOT reproduced but the failure-mode claim WAS."""
body = json.dumps({"model":"gpt-5.2","messages":[{"role":"user","content":prompt}],"temperature":0.2}).encode()
req = urllib.request.Request("http://127.0.0.1:44497/v1/chat/completions", data=body, headers={"Content-Type":"application/json","Authorization":"Bearer stevens"})
r = json.loads(urllib.request.urlopen(req, timeout=180).read())
print(r["choices"][0]["message"]["content"])
