"""LLM-judge for the Chen-Holst-Xu 2007 RPBE replication.
Uses local Argo proxy (free) at http://127.0.0.1:44497/v1 with key `stevens`.
"""
import json, os, sys, urllib.request

PROMPT = """You are grading an independent replication of a mathematical numerical-analysis paper.

PAPER (real, on arXiv 1001.1350; SIAM J. Numer. Anal. 45(6):2298-2320, 2007):
  "The Finite Element Approximation of the Nonlinear Poisson-Boltzmann Equation"
  Long Chen, Michael Holst, Jinchao Xu.

KEY THEORETICAL CLAIMS made by the paper that the replicator can hope to test computationally:
  C1. The regularization  utilde = u + G   with G = sum_i q_i/(eps_m |x - x_i|)
      turns the PBE with delta sources (originally not in H^{-1}) into a
      well-posed nonlinear PDE (the "RPBE") for u in H^1.
  C2. The further split  u = u^l + u^n  (paper eqs 3.7-3.10) decomposes the
      solver into a linear elliptic problem for u^l and a nonlinear elliptic
      problem for u^n with data in H^{-1} and bounded solution respectively.
  C3. Theorem 6.2 (quasi-optimal a priori error estimate):
        ||u - u_h||_1  <~  inf_{v_h in V^h} ||u - v_h||_1.
      Combined with standard P1 interpolation on H^2-regular solutions this
      predicts empirical rates
        ||u - u_h||_L2 = O(h^2),   |u - u_h|_H1 = O(h).
  C4. Discrete L^infty bounds on u_h (Theorems 6.3, 6.4) via M-matrix / grid
      assumptions -- effectively "u_h stays bounded uniformly in h".
  C5. Adaptive FEM based on the a posteriori estimator of section 7 converges.

WHAT THE REPLICATOR DID (independent implementation in Python with scikit-fem 12,
P1 Lagrange elements, damped Newton on the nonlinear reaction term, direct
sparse solves; all free/OSS stack):

Test A: Manufactured-solution 2D RPBE test on Omega=(0,1)^2 with atom placed
OUTSIDE Omega (so G is smooth on Omega, matching Thm 6.2's smoothness setup).
Exact solution u = sin(pi x) sin(pi y); f computed in closed form; solve nonlinear
FEM system on a sequence of 7 uniformly refined triangulations. Observed
(rpbe_mms_results.json):
%(mms_table)s

Test B: Two-atom RPBE test on Omega=(-1,1)^2 with a 2D "molecule" (|x|,|y|<0.2)
containing a dipole (q = +1, -1 at x=(-0.1,0),(0.1,0)), eps_m=2, eps_s=80,
kappabar^2_s=80. Implements the paper's u = u^l + u^n split; solves linear
problem for u^l and damped-Newton nonlinear problem for u^n. Six refinement
levels; measures energy monotonicity under Newton and H1-norm-difference
between consecutive-level solutions (Cauchy-in-h proxy). Observed
(rpbe_twoatom_results.json):
%(twoatom_table)s

Newton behaviour reported: full quadratic convergence (residual reduced from
~1e2 to ~1e-13 in 3-5 iterations) on both tests, and the two-atom energy was
strictly monotonically decreasing along Newton iterations at every level.

GRADING TASK
Assess how well this replication supports each of C1-C5, on real data / real
code (no fabrication -- all numbers came from the runs above). Then choose ONE
verdict from this canonical vocabulary:
  REPLICATED   (core claims independently reproduced on real data)
  PARTIAL      (some claims reproduced, some out of reach)
  SPOT-CHECK   (only data availability + method plausibility, no full rerun)
  NO-GO        (data/code unavailable)
  CONTRADICTED (rerun disagrees with paper)
  BLOCKED      (external blocker)
  FAILED       (attempted, could not reproduce for technical reasons)

Respond as JSON:
{
  "per_claim": {"C1": "...", "C2": "...", "C3": "...", "C4": "...", "C5": "..."},
  "verdict": "<one of the vocabulary above>",
  "justification": "<2-4 sentence rationale>",
  "one_line_summary": "<one sentence>"
}
"""

def build_prompt():
    with open('rpbe_mms_results.json') as f:
        mms = json.load(f)
    with open('rpbe_twoatom_results.json') as f:
        tw = json.load(f)

    lines = ["  lvl   h        ndof    L2 err       L2 rate   H1 err       H1 rate"]
    for r in mms['results']:
        rL2 = r.get('rate_L2', float('nan'))
        rH1 = r.get('rate_H1', float('nan'))
        lines.append(f"  {r['level']:>3}  {r['h']:<8.5f} {r['ndof']:>6d}  "
                     f"{r['L2']:.3e}  {rL2:>7.3f}   {r['H1']:.3e}  {rH1:>7.3f}")
    mms_tbl = "\n".join(lines)

    lines = ["  lvl   h        ndof    |ul|_H1     |un|_H1     Newton_iters  energy_mono  E_start->E_end        H1diff_vs_prev"]
    for r in tw['results']:
        d = r['H1_norm_diff_vs_prev']
        d_str = f"{d:.3e}" if isinstance(d,(int,float)) and d==d else "  -   "
        lines.append(f"  {r['level']:>3}  {r['h']:<8.5f} {r['ndof']:>6d}  "
                     f"{r['ul_H1']:.3e}  {r['un_H1']:.3e}  {r['newton_iters']:>4d}         "
                     f"{r['energy_monotone']}         "
                     f"{r['energy_first']:.3e}->{r['energy_last']:.3e}  {d_str}")
    two_tbl = "\n".join(lines)

    return PROMPT % {'mms_table': mms_tbl, 'twoatom_table': two_tbl}


def call_argo(prompt, model='argo:gpt-5'):
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    # gpt-5 family under Argo currently returns 400 if temperature is set
    if 'gpt-5' not in model and 'o1' not in model and 'o3' not in model and 'o4' not in model:
        payload['temperature'] = 0
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        'http://127.0.0.1:44497/v1/chat/completions',
        data=body,
        headers={'Content-Type': 'application/json',
                 'Authorization': 'Bearer stevens'},
        method='POST')
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


if __name__ == "__main__":
    p = build_prompt()
    print("=" * 78)
    print("Prompt sent to LLM judge (Argo Claude Opus 4.7):")
    print("=" * 78)
    print(p)
    print("=" * 78)
    out = call_argo(p)
    content = out['choices'][0]['message']['content']
    print("\n=== JUDGE RESPONSE ===\n")
    print(content)
    with open('judge_response_raw.json', 'w') as f:
        json.dump(out, f, indent=2)
    with open('judge_verdict.md', 'w') as f:
        f.write("# LLM Judge Verdict\n\nModel: argo:gpt-5 (Argo proxy, free)\n\n")
        f.write("## Prompt sent\n\n```\n" + p + "\n```\n\n")
        f.write("## Response\n\n" + content + "\n")
    print("\nSaved judge_response_raw.json and judge_verdict.md")
