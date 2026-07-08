#!/usr/bin/env python3
"""LLM-judge verdict via Argo free endpoint. No regex scoring."""
import json, os, sys, urllib.request, textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVID = HERE.parent / "report" / "evidence"
results = json.loads((EVID / "results.json").read_text())

PROMPT = textwrap.dedent(f"""
You are an independent scientific-replication judge. A subordinate has produced
a small-instance replication of the paper:

  Craig Gidney, "Stim: a fast stabilizer circuit simulator", arXiv:2103.02202 (2021)

The paper's headline claim is that Stim can (a) analyze a distance-100 rotated
surface code memory circuit (~20k qubits, ~1M measurements) in about 15 seconds
on a 2018 laptop, and (b) then sample full circuit shots at ~1 kHz. Its stated
mechanism is: expensive-once stabilizer-tableau reference sample, then bulk
Pauli-frame sampling with SIMD, giving order-of-magnitude speedups over per-shot
tableau simulation. The paper also positions Stim as the standard fast sampler
that PyMatching decodes for surface-code memory experiments.

The replicator did NOT try the d=100 headline; instead they ran a REAL SMALLER
INSTANCE that tests the same qualitative claims:
 - d=5 rotated surface code memory Z, rounds=5, circuit-level depolarizing noise
 - Correctness at zero noise (no detectors fire, no logical flip)
 - Speed comparison: Stim's bulk Pauli-frame sampler vs a per-shot
   stim.TableauSimulator loop on the SAME circuit
 - Decode with PyMatching, compute logical error rate at 7 noise levels, plus
   distance scaling d=3,5,7 at p=0.005

Actual measured results (real Stim {results['meta']['stim_version']} +
PyMatching {results['meta']['pymatching_version']} on host
{results['meta']['host']}, python {results['meta']['python']}):

CORRECTNESS (d=5, rounds=5, p=0, 200 shots):
{json.dumps(results['correctness'], indent=2)}

SPEED (d=5, rounds=5, p=0.001, same circuit for both samplers):
{json.dumps(results['speed'], indent=2)}

DECODE CURVE (d=5, rounds=5, 20k shots per p, PyMatching MWPM):
{json.dumps(results['decode']['curve'], indent=2)}

DISTANCE SCALING at p=0.005 (20k shots each):
{json.dumps(results['decode_extra'], indent=2)}

Please assess this replication against the paper's claims. Consider:

1. Correctness: at zero noise, are detectors silent and observable unflipped?
   (Confirms the circuit + sampler + decoder pipeline is not broken.)
2. Speed claim: Stim's bulk Pauli-frame sampler should be orders of magnitude
   faster per shot than a per-shot tableau re-simulation of the same circuit.
   (Note: the naive baseline here is itself stim.TableauSimulator, which is
   already a fast Clifford sim; the speedup measured is thus the amortization
   effect only, not Stim-vs-CHP. Judge whether the >~50x measured speedup at
   d=5 is qualitatively consistent with the paper's Pauli-frame amortization
   claim.)
3. Decoder pipeline: does Stim's detector_error_model → PyMatching path
   produce a plausible logical-error curve that increases monotonically with
   noise?
4. Distance scaling: at a p that should be below threshold, does logical
   error rate decrease with distance d?

Choose ONE verdict:
  REPLICATED (headline behaviour reproduced at small scale within tolerance)
  PARTIAL   (some claims reproduced, some not)
  SPOT-CHECK (code/method verified but full claim not tested)
  NO-GO / CONTRADICTED / BLOCKED / FAILED

Respond with a JSON object ONLY (no markdown fences), fields:
{{
  "verdict": "<one of the vocab words>",
  "one_line": "<<=180 char summary>",
  "justification": "<3-6 sentences citing the specific measured numbers>",
  "per_claim": {{
    "correctness": "<pass|fail|na>: <why>",
    "speed": "<pass|fail|partial|na>: <why>",
    "decoder_pipeline": "<pass|fail|partial|na>: <why>",
    "distance_scaling": "<pass|fail|partial|na>: <why>"
  }}
}}
""").strip()

req = urllib.request.Request(
    "http://127.0.0.1:44497/v1/chat/completions",
    method="POST",
    headers={"Authorization": "Bearer stevens", "Content-Type": "application/json"},
    data=json.dumps({
        "model": "argo:gpt-4.1",
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.1,
    }).encode(),
)
with urllib.request.urlopen(req, timeout=120) as r:
    resp = json.loads(r.read())
raw = resp["choices"][0]["message"]["content"]
(EVID / "judge_raw.txt").write_text(raw)
# extract JSON
import re
m = re.search(r"\{.*\}", raw, re.S)
if not m:
    print("no json in judge output", file=sys.stderr)
    print(raw, file=sys.stderr)
    sys.exit(2)
verdict = json.loads(m.group(0))
(EVID / "judge.json").write_text(json.dumps(verdict, indent=2))
print(json.dumps(verdict, indent=2))
