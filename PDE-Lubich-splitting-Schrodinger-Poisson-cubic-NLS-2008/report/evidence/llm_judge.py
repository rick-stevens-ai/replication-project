"""
LLM-judge for the Lubich (2008) replication.  Uses Argo (free) at localhost:44497.
Model: argo/argo:claude-opus-4.8 (default) via OpenAI-compat /v1/chat/completions.
"""
import json, os, sys, urllib.request

RESULTS = json.load(open(os.path.join(os.path.dirname(__file__), "convergence_results.json")))

paper_claims = """\
Lubich (2008), Math. Comp. 77(264):2141-2153.  Theorems 2.1 and 7.1.

Theorem 2.1 (Schrödinger-Poisson, 3D whole space, H^4-regular solution).
For the Strang split-step scheme (eq. (1.4) of the paper):
    ||psi_n - psi(t_n)||_{H^1} <= C(m3,T) * tau
    ||psi_n - psi(t_n)||_{L^2} <= C(m4,T) * tau^2
The paper explicitly states the argument extends to periodic BC and lower
space dimension.

Theorem 7.1 (cubic nonlinear Schrödinger, sign +/-|psi|^2, H^4-regular solution).
For the same Strang split-step scheme:
    ||psi_n - psi(t_n)||_{H^2} <= C(m4,T) * tau
    ||psi_n - psi(t_n)||_{L^2} <= C(m4,T) * tau^2

Additional intrinsic property: the scheme is a composition of two unitary flows
in L^2, so ||psi_n||_{L^2} = ||psi_0||_{L^2} exactly (up to floating-point).

The paper contains NO numerical experiments (pure theory paper, 13 pages).
"""

replication_summary = f"""\
Independent replication (1D periodic domain [0, 2*pi], N={RESULTS['grid']['N']} Fourier modes,
final time T=1.0, smooth initial data, reference = Strang splitting at tau_ref=1/32000):

For each problem, five step sizes tau were tested: 1/50, 1/100, 1/200, 1/400, 1/800.
The numerical convergence orders were estimated from consecutive tau-halvings.

Cubic NLS (defocusing, sign=-1):
  L2 orders across pairs: {['%.3f'%o for o in RESULTS['cubic_NLS_defocusing']['orders_L2']]}
  H2 orders across pairs: {['%.3f'%o for o in RESULTS['cubic_NLS_defocusing']['orders_Hm']]}
  L2 mass drift: max |dM|/M = {max(RESULTS['cubic_NLS_defocusing']['mass_drift']):.2e}

Cubic NLS (focusing, sign=+1):
  L2 orders: {['%.3f'%o for o in RESULTS['cubic_NLS_focusing']['orders_L2']]}
  H2 orders: {['%.3f'%o for o in RESULTS['cubic_NLS_focusing']['orders_Hm']]}
  L2 mass drift: max |dM|/M = {max(RESULTS['cubic_NLS_focusing']['mass_drift']):.2e}

Schrödinger-Poisson (sign = +|psi|^2):
  L2 orders: {['%.3f'%o for o in RESULTS['SP_plus']['orders_L2']]}
  H1 orders: {['%.3f'%o for o in RESULTS['SP_plus']['orders_Hm']]}
  L2 mass drift: max |dM|/M = {max(RESULTS['SP_plus']['mass_drift']):.2e}

Schrödinger-Poisson (sign = -|psi|^2):
  L2 orders: {['%.3f'%o for o in RESULTS['SP_minus']['orders_L2']]}
  H1 orders: {['%.3f'%o for o in RESULTS['SP_minus']['orders_Hm']]}
  L2 mass drift: max |dM|/M = {max(RESULTS['SP_minus']['mass_drift']):.2e}

Additional sanity check performed prior to the sweep:
- Free-Schrödinger step applied to a pure plane wave psi = exp(i*3*x) with
  V=0, tau=0.01, T=1.0 gives L2 error 4.4e-14 vs. the exact solution
  exp(i*3*x - i*9*t)  ->  scheme reduces to the exact linear propagator
  to machine precision, confirming correct implementation of the kinetic step.
"""

prompt = f"""You are a rigorous scientific replication judge.  You will decide whether the
independent replication below faithfully reproduces the mathematical claims of the paper.

PAPER CLAIMS:
{paper_claims}

INDEPENDENT REPLICATION:
{replication_summary}

Please decide:

1. Does the replication numerically confirm Theorem 2.1's second-order L^2
   convergence for Schrödinger-Poisson?  Cite the observed numbers.
2. Does the replication numerically confirm Theorem 7.1's second-order L^2
   convergence for cubic NLS?  Cite the observed numbers.
3. Does the L^2 conservation observed match the theoretical unitarity property?
4. What about the H^m estimates (theorem: O(tau), observed: what)?  Is the
   observation consistent with the theorem (theorem gives an upper bound)?
5. Note that the paper analyzes 3D whole-space, but explicitly states the
   arguments extend to periodic BC and lower dimension.  Is a 1D periodic
   test a legitimate check of the theorems?  Why?

Then output a JSON block on its own with:
{{
  "verdict": one of "REPLICATED", "PARTIAL", "CONTRADICTED", "SPOT-CHECK",
  "core_claims_reproduced": true/false,
  "notes": "<one to three sentence justification>",
  "one_line_summary": "<<= 25 words>"
}}
"""

def call_argo(prompt: str, model: str = "argo:claude-sonnet-4.6") -> str:
    # argo:claude-opus-4.8 was returning 502 Bad Gateway at run time (upstream flake);
    # falling back to argo:claude-sonnet-4.6 (also free, Argo proxy).
    url = "http://127.0.0.1:44497/v1/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a careful scientific replication judge. Be precise and quantitative."},
            {"role": "user",   "content": prompt},
        ],
        "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": "Bearer stevens", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    return resp["choices"][0]["message"]["content"]

out = call_argo(prompt)
print(out)
with open(os.path.join(os.path.dirname(__file__), "llm_judge_output.md"), "w") as f:
    f.write("# LLM-judge output (model: argo:claude-sonnet-4.6 via Argo proxy)\n\n")
    f.write(out)
