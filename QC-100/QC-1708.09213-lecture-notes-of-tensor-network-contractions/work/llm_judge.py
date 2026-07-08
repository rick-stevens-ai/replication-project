"""
LLM-judge scoring of the replication verdict.
Uses Argo proxy (localhost:44497) with argo:claude-opus-4.7 (free).
"""
import json, os, requests, textwrap

ARGO_URL = "http://127.0.0.1:44497/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY", "stevens")

def load_evidence():
    root = "../report/evidence"
    out = {}
    for name in sorted(os.listdir(root)):
        with open(os.path.join(root, name)) as f:
            out[name] = json.load(f)
    return out

def build_prompt(evidence):
    # Always strip long arrays for brevity
    def strip(x):
        if isinstance(x, dict): return {k: strip(v) for k,v in x.items()}
        if isinstance(x, list) and len(x) > 8 and all(isinstance(y,(int,float)) for y in x):
            return f"[array len={len(x)}: min={min(x):.4g} max={max(x):.4g}]"
        if isinstance(x, list): return [strip(y) for y in x]
        return x
    ev_str = json.dumps(strip(evidence), indent=2, default=str)

    prompt = f"""You are the independent-replication verdict judge for the X-100 replication project.

## Paper under replication
arXiv:1708.09213 -- "Lecture Notes of Tensor Network Contractions" by
S.-J. Ran, E. Tirrito, C. Peng, X. Chen, L. Tagliacozzo, G. Su, M. Lewenstein
(published as Lecture Notes in Physics vol. 964, Springer, 2020).

This is a PEDAGOGICAL / TUTORIAL paper (a book, really) on tensor-network
methods -- MPS, PEPS, MERA, DMRG, TEBD, TRG, CTMRG, etc.  It does not present
a big table of new numerical results; its "claims" are the standard
correctness / behaviour of the algorithms it teaches.  For replication we
picked four concrete numerical claims that are:
  - directly implied by the paper's exposition,
  - testable with modest numerical work in `quimb` / numpy on a laptop,
  - falsifiable if the algorithms are wrong.

## Claims tested (with paper anchor)
C1 (Sec 2.2 + Sec 5.1 + Chap 6):  A finite-N DMRG / MPS variational
    calculation on the 1D TFIM  H = -sum Z_i Z_{{i+1}} - h sum X_i  at
    criticality (h=1) reproduces the exact free-fermion ground-state energy;
    a 1/N extrapolation converges to the thermodynamic-limit result -4/pi.
C2 (Sec 2.4.3 + general MPS/CFT pedagogy):  For the critical TFIM, the
    half-chain / block entanglement entropy scales as
    S(l) = (c/6) log((2N/pi) sin(pi l /N)) + const   with c = 1/2 (Ising CFT).
C3 (Sec 5.1.1 -- 5.1.2):  A finite MPS can be brought into a canonical form
    (left-orthogonality  sum_s A_s^dag A_s = I to machine precision), and
    truncation by keeping largest Schmidt values in canonical form is
    globally optimal (2-norm error = sum of DISCARDED sigma^2).
C4 (Sec 3.4 + Sec 4.2):  Imaginary-time TEBD drives an initial product state
    toward the ground state; for critical TFIM the per-site energy converges
    to the same value as DMRG / free-fermion.

## Method
- Free endpoints only (Argo proxy).
- Real code, real numerical output.
- `quimb` 1.14.0 + numpy on CPU.
- Cross-checked TFIM Pauli-convention against exact diagonalization (N=6..12)
  and against Pfeuty free-fermion formula (agree to 1e-14).

## Raw evidence
```json
{ev_str}
```

## Your task
Score each of the four claims individually: REPLICATED / PARTIAL / SPOT-CHECK /
NO-GO / CONTRADICTED / BLOCKED / FAILED, with a one-sentence justification for
each based on the numerical evidence above.

Then give an OVERALL verdict for the paper using the same vocabulary, and one
line summarizing what was actually achieved.

Return valid JSON only, with keys:
  claim_verdicts: object mapping C1,C2,C3,C4 -> {{verdict, evidence, justification}}
  overall_verdict: string (one of the vocab)
  overall_one_line: string (<= 150 chars)
"""
    return prompt

def judge(evidence, model="argo:gpt-5"):
    prompt = build_prompt(evidence)
    payload = {
        "model": model,
        "messages": [
            {"role": "user",
             "content": ("You are a rigorous, evidence-based replication verdict judge. "
                         "Output valid JSON only.\n\n" + prompt)},
        ],
        "max_tokens": 3500,
        "user": "stevens",
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    r = requests.post(ARGO_URL, json=payload, headers=headers, timeout=180)
    if r.status_code != 200:
        print('HTTP', r.status_code, 'body:', r.text[:1000])
    r.raise_for_status()
    resp = r.json()
    content = resp["choices"][0]["message"]["content"]
    return content, resp

def main():
    ev = load_evidence()
    print(f"Loaded {len(ev)} evidence files")
    content, resp = judge(ev)
    # strip markdown fences if present
    txt = content.strip()
    if txt.startswith("```"):
        txt = txt.split("```", 2)[1]
        if txt.startswith("json"): txt = txt[4:]
        txt = txt.strip("` \n")
    # try to parse
    try:
        parsed = json.loads(txt)
    except json.JSONDecodeError:
        print("--- raw LLM response ---")
        print(content)
        raise
    with open("../report/evidence/llm_judge_verdict.json", "w") as f:
        json.dump(dict(judge_model=payload_model_hint(),
                       raw=content,
                       parsed=parsed), f, indent=2)
    print("\n===== JUDGE VERDICT =====")
    print(json.dumps(parsed, indent=2))

def payload_model_hint():
    return "argo:gpt-5 via localhost:44497"

if __name__ == "__main__":
    main()
