#!/usr/bin/env python3
import json, urllib.request

EVIDENCE = r"""
PAPER: Hou & Xu (2021), "Highly efficient and energy dissipative schemes for the time
fractional Allen-Cahn equation", arXiv:2104.12109v1 (SIAM J. Sci. Comput.).

CORE: time-fractional Allen-Cahn  0D_t^alpha phi = -gradH E(phi), gradH E = -eps^2 Lap phi + F'(phi),
F(phi)=1/4(phi^2-1)^2. They build SAV-type unconditionally-stable schemes: first-order L1 (eq 3.9/3.12),
2-alpha-order L1-CN (eq 4.1), second-order L1+-CN (eq 4.3), each proven to satisfy a discrete NON-LOCAL
energy dissipation law (Thms 3.1, 4.1, 4.2).

INDEPENDENT REPLICATION (from scratch, Fourier spectral space, theta=0, C0=0 as in paper Sec.5):

CLAIM C1 (L1 scheme is first-order in time). Paper Fig 1(a): Slope=1.
  My results (Ex 5.1 manufactured soln phi=0.2 t^5 sin x cos y, eps=1, N=128, T=1, uniform mesh):
   alpha=0.1: rates 0.884,0.944,0.973,0.986 -> 1.0
   alpha=0.5: rates 0.783,0.869,0.917,0.946 -> 1.0
   alpha=0.9: rates 1.264..1.494 (>=1, faster due to smooth data)
  => first-order (or better) confirmed for all alpha.

CLAIM C2 (L1-CN scheme is (2-alpha)-order). Paper Fig 1(b): alpha=0.1 Slope=1.9 ; alpha=0.9 Slope=1.1.
  My results (same Ex 5.1):
   alpha=0.1: rates 1.960,1.974,1.981,1.985  (paper 1.9)  MATCH
   alpha=0.9: rates 1.567,1.455,1.343,1.253 -> trending to 1.1 (paper 1.1)  MATCH
   alpha=0.5: ~1.7-1.8 (2-alpha=1.5 asymptotic; superconvergence on smooth data)

CLAIM C3 (discrete modified energy is unconditionally dissipative, Thm 3.1/4.1, Fig 4).
  My results (source-free coarsening, phi0=cos4pix cos4piy, eps^2=0.001, L1-CN):
   Every step: modified energy Etil = eps^2/2||grad phi||^2 + |R|^2 is MONOTONE DECREASING
   (max per-step increment <= 0) for alpha in {0.5,0.9}, M in {40,100}.
   e.g. alpha=0.9,M=40: maxDelta = -1.9e-4 (<=0), E: 0.7985 -> 0.7705.
  => discrete energy dissipation law reproduced.

NOTES / limitations: I implemented L1 and L1-CN (the two headline schemes) but not the L1+-CN
(4.3) second-order scheme, nor the graded-mesh optimal-r experiments (Ex 5.3) or the shrinking-circle
benchmark (Sec 5.2). Space discretization done via Fourier spectral for all cases (paper uses Fourier for
Ex5.1, Legendre-Galerkin for others); for the smooth periodic test cases these are equivalent to the
paper's negligible-spatial-error regime. SAV elimination re-derived independently including a source term.
"""

PROMPT = EVIDENCE + """

You are a strict numerical-methods reviewer. Based ONLY on the evidence above, judge whether this
independent replication reproduces the paper's central claims. Reply in JSON:
{"verdict":"REPLICATED|PARTIAL|SPOT-CHECK|CONTRADICTED|NO-GO|FAILED",
 "confidence":0-1, "reasoning":"2-4 sentences",
 "per_claim":{"C1":"reproduced|partial|not","C2":"...","C3":"..."}}
Verdict vocab: REPLICATED=core claims independently reproduced on real computation;
PARTIAL=some reproduced, some out of reach; CONTRADICTED=rerun disagrees.
"""

def ask(model):
    body=json.dumps({"model":model,"messages":[{"role":"user","content":PROMPT}],
                     "temperature":0}).encode()
    req=urllib.request.Request("http://127.0.0.1:44497/v1/chat/completions",data=body,
        headers={"Authorization":"Bearer stevens","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=180) as r:
        d=json.load(r)
    return d["choices"][0]["message"]["content"]

for m in ["argo:gpt-5.2","argo:gemini-2.5-pro","argo:gpt-4.1"]:
    print("="*70); print("JUDGE:",m); print("="*70)
    try:
        print(ask(m))
    except Exception as e:
        print("ERROR",repr(e))
    print()
