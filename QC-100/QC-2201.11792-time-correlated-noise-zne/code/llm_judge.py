"""3-judge Argo panel scoring the replication verdict."""
import json, os, sys, urllib.request

ARGO_URL = "http://127.0.0.1:44497/v1/chat/completions"
ARGO_KEY = "stevens"
MODELS = [
    "argo:claude-opus-4.7",
    "argo:gpt-5.2",
    "argo:claude-opus-4.8",
]

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "report", "evidence")

def load(path):
    with open(path) as f:
        return json.load(f)

r_ansatz = load(os.path.join(RESULTS_PATH, "results.json"))
r_ghz = load(os.path.join(RESULTS_PATH, "results_ghz_multiseed.json"))

PROMPT = """You are judging an independent replication of arXiv:2201.11792 "Analyzing the impact of time-correlated noise on zero-noise extrapolation" (Schultz, LaRose, Mari, Quiroz, Shammah, Clader, Zeng, 2022).

The paper's HEADLINE CLAIM:
Zero-Noise Extrapolation (ZNE), a standard quantum error mitigation technique, reduces bias in expectation values under uncorrelated (white/Markovian) noise, but under time-correlated (colored / non-Markovian) noise ZNE leaves substantial residual bias or greatly increased variance because the noise scaling schemes distort the noise spectrum rather than just its amplitude.

The replicator implemented this from scratch using Mitiq + Qiskit Aer with:
- Uncorrelated noise = per-gate depolarizing (Qiskit Aer NoiseModel).
- Time-correlated noise = per-shot random-walk coherent Z drift across gates (low-frequency dominated spectrum, non-Markovian across gates within one shot, resampled across shots). This is a faithful qualitative stand-in for SchWARMA colored dephasing.
- ZNE = Richardson extrapolation with scale factors [1, 3, 5], local (fold_gates_at_random) unitary folding.

EXPERIMENT 1 (single seed, 4-qubit hardware-efficient ansatz, small dynamic range because noiseless P(0000)~0.09):
{ansatz}

EXPERIMENT 2 (multi-seed, 4-qubit GHZ prepare-and-invert circuit, noiseless P(0000)=1.0; 5 independent seeds, means ± stds reported):
{ghz}

Please score:
1) Does the replication USE THE ACTUAL LIBRARIES (Mitiq + Qiskit Aer)? (Yes / No)
2) Does the numerical result QUALITATIVELY REPRODUCE the paper's headline (ZNE effective on uncorrelated, degraded/unreliable on time-correlated)? Explain concretely which numbers support your judgement.
3) Would you assign a verdict of REPLICATED, PARTIAL, SPOT-CHECK, CONTRADICTED, or FAILED? Justify in 3-5 sentences.

Answer strictly in JSON of the form:
{{"used_real_libs": true/false, "reproduces_headline": true/false, "verdict": "REPLICATED"|"PARTIAL"|"SPOT-CHECK"|"CONTRADICTED"|"FAILED", "justification": "..."}}
Do NOT wrap in code fences.
""".format(
    ansatz=json.dumps(r_ansatz, indent=2, default=float),
    ghz=json.dumps(r_ghz, indent=2, default=float),
)


def call(model):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a careful scientific replication reviewer. Output only valid JSON."},
            {"role": "user", "content": PROMPT},
        ],
        "temperature": 0.0,
        "max_tokens": 800,
    }).encode()
    req = urllib.request.Request(ARGO_URL, data=body, headers={
        "Authorization": f"Bearer {ARGO_KEY}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read())
    return payload["choices"][0]["message"]["content"]


out = {}
for m in MODELS:
    try:
        text = call(m)
        parsed = None
        try:
            parsed = json.loads(text)
        except Exception:
            # try to strip anything before/after the first {...}
            i = text.find("{"); j = text.rfind("}")
            if i >= 0 and j > i:
                try:
                    parsed = json.loads(text[i:j+1])
                except Exception:
                    parsed = None
        out[m] = {"raw": text, "parsed": parsed}
        print(f"[{m}] verdict={parsed.get('verdict') if parsed else 'PARSE_FAIL'}")
    except Exception as e:
        out[m] = {"error": str(e)}
        print(f"[{m}] ERROR: {e}")

with open(os.path.join(RESULTS_PATH, "llm_judges.json"), "w") as f:
    json.dump(out, f, indent=2)

verdicts = [v.get("parsed", {}).get("verdict") for v in out.values() if isinstance(v.get("parsed"), dict)]
print("verdicts:", verdicts)
