import json, urllib.request, os

claims_and_results = r"""
PAPER: "Kolmogorov-Arnold Wavefunctions" (Bedaque, Cigliano, Kumar, Paul, Rajawat;
arXiv:2506.02171 / OSTI 3007459). Variational Monte Carlo (VMC) with a bosonic
Kolmogorov-Arnold Network (KAN) wavefunction ansatz for 1D many-boson systems,
compared to feed-forward MLP ansatz.

CLAIMS (independently tested):
C1 (method correctness): The solvable model (Eq.6, sigma=-mwg/2) has exact ground
   energy E0 = N w/2 - m g^2 N(N^2-1)/24 (Eq.7). The VMC local-energy estimator
   (kinetic via autodiff of log-psi + potential) applied to the EXACT wavefunction
   (Eq.8) should give E0 with zero variance (zero-variance principle).
C2 (non-interacting sanity): KAN VMC on the delta+harmonic model (Eq.12) at g=0
   should give E = N/2 exactly for any N.
C3 (interacting accuracy, N=2): KAN VMC energy for Eq.12 should match the Busch et al.
   analytic N=2 result across coupling g.
C4 (E(g) shape): E(g) rises monotonically from N/2 (g=0) toward the Tonks-Girardeau
   limit N^2/2 (g->inf) (paper Fig.6 shape).
C5 (efficiency, HEADLINE): KAN ansatz needs far fewer parameters than MLP, and is
   ~10x cheaper in FLOPs/walltime at matched accuracy.
C6 (knot refinement): the knot-doubling refinement scheme (insert knots, keep the
   curve) allows scaling ansatz expressivity mid-training.

INDEPENDENT-REPLICATION RESULTS (real reimplementation from equations; no paper code):
- C1: smooth local energy of the EXACT wavefunction = E0 to machine precision with
  ZERO variance for N=2 (0.9375), N=4 (1.3750), N=8 (-1.2500). PASS (rigorous).
- C2: KAN VMC g=0 gives E = 1.0 (N=2), 1.5 (N=3), 2.0 (N=4), relerr ~1e-6, zero
  variance. PASS (exact).
- C3/C4: The delta term was reintroduced as a Gaussian-regulated delta (width eps)
  giving the repulsion needed to bound the energy for smooth trial wavefunctions.
  Busch analytic reference reproduced exactly (g=0.5:1.307, g=1:1.487, g=2:1.674,
  g->inf:2.0). KAN VMC results were SEED- and EPS-dependent: some runs hit near-exact
  (N=2 g=2.0: E=1.682 vs Busch 1.674, relerr 0.5%), but many runs overshot or were
  unstable (N=2 g=0.5: E=1.79 vs 1.307; N=2 g=4.0: E=2.49, above the TG limit 2.0
  -> unphysical/collapsed). eps->0 extrapolation was non-monotonic and did not yield
  a clean value (extrap 2.19 vs Busch 1.487). So the interacting energies are
  QUALITATIVELY reproduced and occasionally quantitatively accurate, but NOT robustly.
- C5 (headline 10x): KAN used 2.9x FEWER parameters than MLP (408 vs 1186) at matched
  problem -> the "fewer parameters" part is confirmed. But in OUR reimplementation the
  KAN was SLOWER in walltime and less accurate than the MLP for the interacting case,
  so the ~10x walltime/FLOP efficiency claim was NOT confirmed (our KAN VMC tuning is
  weaker than our MLP; the paper's optimized implementation may differ).
- C6: knot-doubling refinement implemented (RBF-spline least-squares match) and used
  during training without destabilizing the run. Structurally reproduced.

KNOWN LIMITATIONS of the replication:
- No paper code/data package (method-only reimplementation from the equations).
- The naive piecewise-quadratic spline caused derivative-spike variational collapse;
  fixed by switching to smooth Gaussian-RBF line-functions (a faithful "smooth
  line-function" choice, but not bit-identical to the paper's quadratic splines).
- Delta interaction handled by Gaussian regularization; introduces eps-dependence not
  present in the paper's (presumably cusp-analytic) treatment.
- Interacting-case VMC not robustly converged across seeds; no full FLOP profiling.

Given all this, produce a JSON verdict object:
{"coverage": <0-1>, "agreement": <0-1>, "verdict": "<REPLICATED|PARTIAL|SPOT-CHECK|NO-GO|CONTRADICTED|FAILED>", "rationale": "<2-4 sentences>"}
coverage = fraction of testable claims independently exercised; agreement = degree the
reproduced results agree with the paper where tested. Be strict and fair.
"""

payload = {
    "model": "argo:gpt-5.2",
    "messages": [
        {"role": "system", "content": "You are a strict, fair scientific replication judge. Output ONLY a JSON object."},
        {"role": "user", "content": claims_and_results},
    ],
    "temperature": 0.0,
}

def call(model):
    payload["model"] = model
    req = urllib.request.Request(
        "http://localhost:44497/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())

for model in ["argo:gpt-5.2", "argo:claude-opus-4.8"]:
    try:
        resp = call(model)
        content = resp["choices"][0]["message"]["content"]
        print(f"=== JUDGE MODEL: {model} ===")
        print(content)
        json.dump({"model": model, "raw": content}, open("llm_judge_verdict.json", "w"), indent=2)
        break
    except Exception as e:
        print(f"model {model} failed: {e}")
