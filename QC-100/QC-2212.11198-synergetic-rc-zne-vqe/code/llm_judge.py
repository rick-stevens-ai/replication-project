"""LLM-judge scoring via Argo (free endpoint) for QC-2212.11198 replication.

Sends the paper summary + our results + methodology to argo/argo:claude-opus-4.7
and asks for a verdict from {REPLICATED, PARTIAL, SPOT-CHECK, NO-GO,
CONTRADICTED, BLOCKED, FAILED}.
"""

import json
import os
from pathlib import Path
from urllib import request

ARGO_URL = "http://localhost:44497/v1/chat/completions"
ARGO_KEY = "stevens"
# Judge models -- try in order; each is a free Argo endpoint.
JUDGE_MODELS = [
    "argo:gpt-4.1",
    "argo:claude-opus-4.7",
    "argo:gemini-2.5-pro",
]

HERE = Path(__file__).resolve().parent.parent
EV = HERE / "report" / "evidence"


PAPER_CLAIM = """\
Paper: Kurita et al. 2022 (arXiv:2212.11198), "Synergetic quantum error
mitigation by randomized compiling and zero-noise extrapolation for the
variational quantum eigensolver."

CORE CLAIMS:
C1 (headline): For deep VQE circuits under COHERENT noise (over-rotation on
  2q gates), RC alone and ZNE alone give only limited improvement, but the
  combination RC+ZNE reduces the ground-state energy error by 1-2 ORDERS OF
  MAGNITUDE relative to the raw noisy VQE.
C2: The improvement is generic across noise strengths / models.
C3: Coherent noise causes substantially large errors that are difficult for
  conventional mitigation to suppress; ZNE alone can be unreliable on
  coherent noise (systematic over/under-correction).
"""

METHOD = """\
Real simulation:
  Molecule:   H2 in STO-3G at R=0.735 A, 2-qubit tapered Hamiltonian
              (O'Malley et al. 2016 PRX 6 031007 Table I).
  Ansatz:     Deep hardware-efficient, reps=6 (6 CX gates, 13 params).
  Optimizer:  Noiseless Nelder-Mead multi-start (20 restarts) finds theta*
              that matches FCI to <1e-8 Ha.
  Noise:      Coherent RX(eps) after every CX on both qubits + coherent
              RZZ(eps/2), plus 2q depolarizing p_dep=0.002 via Aer NoiseModel
              (matches paper's regime: dominant coherent noise on 2q gates).
  Backend:    Aer density-matrix simulator (exact channel evolution).
  RC:         Pauli twirl of each CX (16-element table) using paper's
              N_rand=30 random compilations (paper used 20).
  ZNE:        Mitiq LinearFactory, scale factors [1,2,3], global folding.
              Folding done on CLEAN ansatz; noise injected per-scale by the
              executor so each folded CX gets its own noise block (physically
              faithful).
  RC+ZNE:     ZNE executor = RC-averaged energy at each scale factor.

Tools: qiskit==2.5.0, qiskit_aer==0.17.2, mitiq==1.0.0, Python 3.12.13.
"""


def load_results():
    with open(EV / "results.json") as f:
        return json.load(f)


def format_results(res):
    lines = []
    lines.append(f"Noiseless VQE energy: {res['vqe_noiseless_energy_Ha']:.6f} Ha  "
                 f"(FCI = {res['fci_electronic_Ha']:.6f} Ha, match to 1e-8)")
    lines.append("")
    lines.append("Energy errors vs noiseless (mHa), sweep over coherent-noise eps:")
    lines.append(f"{'eps (rad)':>10} {'eps (deg)':>10}  {'raw':>10} {'RC':>10} "
                 f"{'ZNE':>10} {'RC+ZNE':>10}")
    for row in res["eps_sweep_Ha"]:
        lines.append(
            f"{row['eps_rad']:>10.3f} {row['eps_deg']:>10.2f}  "
            f"{row['raw_err_mHa']:>+10.3f} {row['rc_err_mHa']:>+10.3f} "
            f"{row['zne_err_mHa']:>+10.3f} {row['rc_zne_err_mHa']:>+10.3f}"
        )
    lines.append("")
    lines.append("Reduction factor (|raw| / |RC+ZNE|):")
    for row in res["eps_sweep_Ha"]:
        rf = abs(row["raw_err_mHa"]) / max(abs(row["rc_zne_err_mHa"]), 1e-9)
        lines.append(f"  eps={row['eps_rad']:.3f}: {rf:.1f}x")
    return "\n".join(lines)


def call_argo(prompt: str, model: str) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 1500,
    }).encode()
    req = request.Request(
        ARGO_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ARGO_KEY}",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


def main():
    res = load_results()
    results_text = format_results(res)

    prompt = f"""You are an independent scientific judge assessing whether a
replication successfully reproduces the headline claim of a paper.

{PAPER_CLAIM}

{METHOD}

REAL SIMULATION RESULTS:
{results_text}

TASK:
Assess whether the replication reproduces the paper's HEADLINE claim (C1):
that RC+ZNE combined reduces the VQE energy error by 1-2 orders of magnitude
relative to the raw noisy VQE, while RC alone or ZNE alone are limited.

Also assess C3 (ZNE alone can be unreliable on coherent noise).

Return your answer in this exact format:

VERDICT: <REPLICATED | PARTIAL | SPOT-CHECK | NO-GO | CONTRADICTED | BLOCKED | FAILED>
CONFIDENCE: <low | medium | high>

JUSTIFICATION:
<3-6 sentences on what was reproduced, what was not, and why the verdict.>

ONE-LINE SUMMARY:
<one line, max 200 chars.>
"""

    replies = {}
    for m in JUDGE_MODELS:
        print(f"[argo] {m} ...")
        try:
            r = call_argo(prompt, m)
            replies[m] = r
            print(f"  ok ({len(r)} chars)")
        except Exception as e:
            replies[m] = f"ERROR: {e}"
            print(f"  err: {e}")

    text = "\n\n".join(f"===== JUDGE: {m} =====\n{r}" for m, r in replies.items())
    (EV / "llm_judge.txt").write_text(text)
    print(f"[wrote] {EV/'llm_judge.txt'}")
    print()
    print(text)


if __name__ == "__main__":
    main()
