"""LLM-judge the BB-qRAM replication using Argo (free)."""
import json, sys, urllib.request, os
from pathlib import Path

HERE = Path(__file__).parent
scaling = json.loads((HERE / "scaling.json").read_text())
paper_txt = (HERE.parent.parent / "work" / "paper.txt").read_text()

# extract the key paper claims section (abstract + intro + "As a result")
excerpt_head = paper_txt[:2500]
# grab the "exponential reduction" passages
key_phrases = []
for phrase in ["O(log N)", "O(log2 N)", "O(N)", "bucket-brigade", "exponential reduction",
               "log N", "2n - 1", "wait"]:
    if phrase in paper_txt:
        i = paper_txt.find(phrase)
        key_phrases.append(paper_txt[max(0,i-120):i+200])

prompt = f"""You are a research reproduction judge. Score the following independent replication
attempt of the paper arXiv:0708.1879 "Quantum random access memory" by
Giovannetti, Lloyd, Maccone.

--- PAPER (abstract + intro excerpt) ---
{excerpt_head}

--- KEY PASSAGES ---
{'---'.join(key_phrases[:4])}

--- REPLICATION SUMMARY (JSON scaling table) ---
{json.dumps(scaling, indent=2)}

The paper's headline claims are:
(H1) Bucket-brigade (BB) qRAM addresses N=2^n memory cells while actively
     exciting only O(log N) switches per call, vs O(N) for conventional/fanout
     designs.
(H2) BB qRAM implements eq. (1): superposition of addresses -> superposition
     of correlated (address, data) pairs.
(H3) BB memory-array size is O(N) trit nodes.

The replication:
* Built a real Qiskit statevector circuit for n=2 (full-register, addr+trits+bus).
* Verified single-address correctness for every a in [0,N) at n=2 (full-register).
* Verified the eq. (1) superposition-query fidelity == 1.0 at n=2 (full-register).
* Simulated n=2,3,4 in a reduced (addr,bus) subspace (proved equivalent
  because BB routing is a classical permutation on the WAIT-initialised
  protocol subspace); every fidelity == 1.0, every single-address readout
  passes.
* Recorded scaling: BB active switches per call = n = log2 N for
  N in {{4,8,16}}; conventional fanout = N-1; total tree nodes = N-1.

Please judge:
1. Does this replication support headline claims H1, H2, H3? YES/NO/PARTIAL for each.
2. Overall verdict (one of): REPLICATED / PARTIAL / SPOT-CHECK / NO-GO / CONTRADICTED / BLOCKED / FAILED.
3. One-line justification.
4. Key caveats or gaps a reviewer should flag.

Respond in JSON with keys: h1, h2, h3, verdict, one_line, caveats.
"""

body = {
    "model": "argo:gpt-5.4",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.0,
    "max_tokens": 1500,
}
req = urllib.request.Request(
    "http://localhost:44497/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"},
)
try:
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.loads(r.read().decode())
    text = resp["choices"][0]["message"]["content"]
except Exception as e:
    text = f"LLM_JUDGE_ERROR: {e}"

out = {"model": "argo:gpt-5.4", "prompt_len": len(prompt), "response": text}
(HERE / "llm_judge_result.json").write_text(json.dumps(out, indent=2))
print(text)
