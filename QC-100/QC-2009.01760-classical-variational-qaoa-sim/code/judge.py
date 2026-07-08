"""Argo LLM-judge for the QC-100 replication verdict.

Free endpoint: http://localhost:44497/v1  key=stevens (per QC wave brief).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

ARGO_URL = "http://127.0.0.1:44497/v1/chat/completions"
ARGO_KEY = os.environ.get("ARGO_API_KEY", "stevens")

RUBRIC = """You are a research-replication judge for the QC-100 project (independent
replications of quantum-computing papers).

Verdict vocabulary:
- REPLICATED: the paper's headline number reproduced within tolerance on real
  simulation.
- PARTIAL: some claims reproduced but not the full headline.
- SPOT-CHECK: method / code verified with a small demo; not the full claim.
- NO-GO: data/code unavailable, replication could not proceed.
- CONTRADICTED: reproduction attempted and clearly disagrees with the paper.
- BLOCKED / FAILED: environment or tooling failed.

Given the paper summary, the claims tested, the numerical evidence, and the
tolerance criteria, output STRICT JSON of the form:
{
  "verdict": "<one of the labels above>",
  "confidence_0to1": <float>,
  "one_line": "<<= 200 char summary>",
  "justification": "<3-6 sentence explanation citing the numbers>"
}
Do not output anything except the JSON object.
"""


def call_argo(system: str, user: str, model: str = "argo:claude-opus-4.7") -> str:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        ARGO_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ARGO_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        payload = json.loads(r.read().decode())
    return payload["choices"][0]["message"]["content"].strip()


def main() -> None:
    context_path = sys.argv[1] if len(sys.argv) > 1 else "context_for_judge.md"
    with open(context_path) as f:
        context = f.read()

    user = f"""Below is the replication evidence bundle for arXiv:2009.01760
"Classical variational simulation of the Quantum Approximate Optimization
Algorithm" (Medvidović & Carleo, 2020/21).

Please issue a verdict.

--- EVIDENCE BUNDLE ---

{context}
"""

    verdicts = []
    for model in ["argo:gpt-5.2", "argo:claude-opus-4.6", "argo:gemini-2.5-pro"]:
        try:
            print(f"[judge] calling {model} ...", flush=True)
            raw = call_argo(RUBRIC, user, model=model)
            # extract JSON
            start = raw.find("{")
            end = raw.rfind("}")
            if start >= 0 and end > start:
                obj = json.loads(raw[start : end + 1])
            else:
                obj = {"verdict": "PARSE_ERROR", "raw": raw}
            obj["judge_model"] = model
            verdicts.append(obj)
            print(json.dumps(obj, indent=2))
        except Exception as e:
            print(f"[judge] {model} error: {e}")
            verdicts.append({"judge_model": model, "error": str(e)})

    with open("judge_results.json", "w") as f:
        json.dump(verdicts, f, indent=2)
    print(f"\n[judge] wrote judge_results.json with {len(verdicts)} verdicts")


if __name__ == "__main__":
    main()
