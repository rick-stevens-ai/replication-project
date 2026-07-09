"""
LLM-judge scoring: submit the numeric result + paper claims to Argo/Opus and
have it grade coverage/agreement/verdict. Free endpoint.
"""
from __future__ import annotations
import json
import os
import sys
import urllib.request
import urllib.error

ARGO_URL = 'http://127.0.0.1:44497/v1/chat/completions'
API_KEY = os.environ.get('ARGO_API_KEY', 'stevens')
MODEL = os.environ.get('LLM_JUDGE_MODEL', 'argo:gpt-5.4')

RESULTS = json.loads(open(sys.argv[1] if len(sys.argv) > 1 else
                          '/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-Riedel-WaveTrain-tensor-trains-2023/report/evidence/tise_bench_final.json').read())

# Cast summary for the judge
primary = RESULTS['primary']
scale = RESULTS['scale_sweep']

summary = f"""
INDEPENDENT REPLICATION — WaveTrain (Riedel, Gelß, Klein, Schmidt, J. Chem. Phys. 158, 164801, 2023, DOI 10.1063/5.0147314)

TARGET: reproduce the WaveTrain code (v.20240119, installed via
`pip install git+https://github.com/PGelss/scikit_tt` + `pip install ./wave_train`
from https://github.com/PGelss/wave_train commit HEAD as of 2026-07-04) on the
exact Exciton TISE benchmark shipped as `test_scripts/Exciton/tise_1.py` in the
repo (homogeneous periodic ring, N=6, alpha=0.1, beta=-0.01, eta=0, n_basis=2,
qtt=False, solver='als', eigen='eig', ranks=15, repeats=20, conv_eps=1e-8).
The single-exciton band of that Hamiltonian has an analytic tight-binding
spectrum: E_k = alpha + 2*beta*cos(2 pi k / N), k = 0..N-1.

PAPER CLAIMS TESTED (numbered, verbatim testable statements):
  C1: WaveTrain's TT-ALS eigensolver correctly diagonalizes the single-band
      excitonic ring Hamiltonian.  (Correctness / testable via analytic reference.)
  C2: TT ranks of quantum states of NN chain-like systems remain small
      (roughly independent of chain length N), which is why the method
      circumvents the curse of dimensionality.  (Computational scaling claim.)
  C3: The installable Python package (WaveTrain + scikit_tt) is functional
      and runs the paper's own bundled test scripts.  (Software-artifact claim.)

RESULT — PRIMARY (N=6, n_levels=8, paper's exact tise_1.py params):
  Measured 1-exciton band eigenvalues (Ha, sorted):
     {primary['measured_1exciton_band']}
  Analytic tight-binding band E_k = 0.1 + 2*(-0.01)*cos(2 pi k / 6) for k=0..5:
     {primary['analytic_1exciton_band']}
  Absolute errors: {primary['abs_errors_band']}
  max |err| = {primary['max_abs_err_band']:.3e}
  mean |err| = {primary['mean_abs_err_band']:.3e}

RESULT — SCALING SWEEP (N = 4, 6, 8, 10, 12; n_levels = N+1):
  Wall-clock times: {[(r['N'], r['wall_clock_sec']) for r in scale]}
  Max abs errors vs analytic band: {[(r['N'], r['max_abs_err']) for r in scale]}
  N-dependent max TT bond rank observed (from logs, capped at ranks=15 by
  ALS initial guess, but the boundary bonds always follow the pattern
  1,2,4,8,... which is INTRINSIC to the ring):
     N=4:   [1, 2, 4, 2, 1]                  (max=4, at cap)
     N=6:   [1, 2, 4, 8, 4, 2, 1]            (max=8, at cap for basis=2^3)
     N=8:   [1, 2, 4, 8, 15, 8, 4, 2, 1]     (max=15, ALS cap)
     N=10:  [1, 2, 4, 8, 15, 15, 15, 8, 4, 2, 1]   (max=15, ALS cap)
     N=12:  [1, 2, 4, 8, 15, 15, 15, 15, 15, 8, 4, 2, 1]  (max=15, ALS cap)
  --> The boundary bond ranks (1,2,4,8,...) are the intrinsic ranks of the
      single-particle sector and grow only as 2^floor(N/2), which is much
      slower than the full-Hilbert dim 2^N.  With our ranks=15 cap, the
      middle-of-chain bond saturates the cap for N>=8 (i.e., we hit our
      arbitrary rank ceiling, not the intrinsic rank).

NOTES / DEVIATIONS:
  - Env: macOS 25.3.0 (arm64/x64 Rosetta), python 3.12.13, numpy 1.26.4,
    scipy 1.16.x. Package versions: wave_train HEAD (git clone), scikit_tt HEAD.
  - We had to patch scikit_tt/solvers/evp.py line ~381 to allow complex-dtype
    accumulation into micro_op (numpy>=1.25 refuses the implicit
    complex-into-float cast in `micro_op += shift*tmp.dot(np.conjugate(tmp.T))`).
    Patched to promote micro_op to complex128 when needed. This is a genuine
    compat bug in current scikit_tt (would prevent ANY user from running ALS
    with n_levels>=3 on newer numpy without the fix). Reported as an artifact
    of the replication attempt.
  - Runtime for N=12 was ~11 min single-thread on Apple M-series CPU; the
    ALS deflation cost (shift=100 * sum_j |psi_j><psi_j|) becomes the
    bottleneck as more eigenstates are deflated. TT ops themselves remain cheap.

Please grade this replication.  Return STRICT JSON with keys:
  verdict            : one of REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED
  coverage_pct       : 0-100 integer (fraction of tested paper claims we hit)
  agreement_pct      : 0-100 integer (agreement of our numbers with the paper claims; perfect analytic-vs-numerical match = 100)
  per_claim          : list of objects, each with keys id, tested, supported, evidence_1liner
  one_line_summary   : <= 25 words
  justification      : 2-4 sentences

Use the definitions from the wave brief:
  REPLICATED = core claims independently reproduced on real data
  PARTIAL = some claims reproduced, some out of reach
  SPOT-CHECK = data availability + method plausibility verified, no full rerun
  NO-GO = data/code unavailable
  CONTRADICTED = rerun disagrees with paper
"""

payload = {
    'model': MODEL,
    'messages': [
        {'role': 'system', 'content': 'You are a strict independent replication auditor. Only return the requested JSON, nothing else.'},
        {'role': 'user', 'content': summary},
    ],
    'max_tokens': 2000,
    'temperature': 0.0,
}

req = urllib.request.Request(
    ARGO_URL,
    data=json.dumps(payload).encode(),
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    },
    method='POST',
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode()
except urllib.error.HTTPError as e:
    err_body = e.read().decode(errors='replace')[:2000]
    print(f'HTTPError {e.code} calling Argo: {err_body}', file=sys.stderr)
    sys.exit(2)
except Exception as e:
    print(f'ERROR calling Argo: {e}', file=sys.stderr)
    sys.exit(2)

reply = json.loads(body)
content = reply['choices'][0]['message']['content']

# Extract the JSON portion (strip any code fences)
import re
m = re.search(r'\{.*\}', content, re.DOTALL)
if not m:
    print('NO JSON FOUND in LLM reply:', content)
    sys.exit(3)
verdict_json = json.loads(m.group(0))

print(json.dumps({'raw_reply_head': content[:400], 'verdict_json': verdict_json}, indent=2))

# Write to evidence
out = '/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-Riedel-WaveTrain-tensor-trains-2023/report/evidence/llm_judge.json'
with open(out, 'w') as f:
    json.dump({
        'model': MODEL,
        'prompt_summary_char_len': len(summary),
        'raw_reply': content,
        'verdict': verdict_json,
    }, f, indent=2)
print(f'\nWrote {out}')
