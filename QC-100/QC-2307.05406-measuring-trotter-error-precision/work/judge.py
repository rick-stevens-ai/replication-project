"""LLM-judge scoring via Argo (free, key=stevens, model=argo/argo:claude-opus-4.7)."""
import json, os, sys, urllib.request, urllib.error, time, textwrap

REPORT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "report", "REPORT.md")).read()

# Argo proxy speaks the OpenAI /v1/chat/completions API
URL = "http://127.0.0.1:44497/v1/chat/completions"
MODEL = os.environ.get("JUDGE_MODEL", "argo:claude-opus-4.7")
KEY = os.environ.get("ARGO_API_KEY", "stevens")

SYS = ("You are a senior computational quantum-simulation reviewer. "
       "You will read a REPLICATION REPORT of a real published paper on measuring Trotter error "
       "(arXiv:2307.05406, Ikeda/Kono/Fujii 2024). You will assess whether the reproduction is: "
       "(a) methodologically sound (correct Hamiltonian, correct T2 / T4 formulas, correct estimator "
       "eta^(24), correct adaptive-step rule), "
       "(b) evidence-backed (real numerical simulation, not fabricated), "
       "(c) whether the assigned verdict is well-justified. "
       "Reply as JSON only with fields: verdict_assessment ('AGREE'|'DOWNGRADE'|'UPGRADE'), "
       "confidence (0-1), main_evidence (short), weaknesses (short), suggested_verdict.")

USER = ("Report follows. Assess it independently:\n\n---\n" + REPORT +
        "\n\n---\nWhat verdict would YOU assign, and do you agree with REPLICATED for the two central "
        "methodological claims (estimator tracks truth; adaptive step meets tolerance)?  Reply JSON only.")

payload = {"model": MODEL,
           "messages": [{"role":"system","content":SYS},
                        {"role":"user","content":USER}],
           "temperature": 0,
           "max_tokens": 700}

req = urllib.request.Request(URL,
                             data=json.dumps(payload).encode("utf-8"),
                             headers={"Content-Type":"application/json",
                                      "Authorization": f"Bearer {KEY}"})
try:
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode()
    dt = time.time() - t0
except urllib.error.HTTPError as e:
    print("HTTPError", e.code, e.read().decode()[:400])
    sys.exit(2)
except Exception as e:
    print("ERR", type(e).__name__, e)
    sys.exit(3)

j = json.loads(raw)
msg = j["choices"][0]["message"]["content"]
print(f"=== JUDGE ({MODEL})  {dt:.1f}s ===")
print(msg)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "report", "evidence", "llm_judge.json"), "w") as f:
    json.dump({"model": MODEL, "seconds": dt, "raw_response": msg}, f, indent=2)
