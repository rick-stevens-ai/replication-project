#!/usr/bin/env python
"""3-judge Argo LLM panel scoring for the replication verdict."""
import os, json, requests, textwrap

REPORT = open(os.path.join(os.path.dirname(__file__), "../report/REPORT.md")).read()
EVID = open(os.path.join(os.path.dirname(__file__), "../report/evidence/qsvm_final.json")).read()

JUDGES = [
    ("argo:gpt-5.2",           "Judge A (GPT-5.2)"),
    ("argo:claude-opus-4.8",   "Judge B (Claude Opus 4.8)"),
    ("argo:gemini-2.5-pro",    "Judge C (Gemini 2.5 Pro)"),
]

PROMPT = """You are an independent scientific-replication judge for a small quantum-computing paper reproduction. You will be given:
  (A) the replication REPORT.md
  (B) the underlying evidence JSON.

Your job:
  1. Read both.
  2. Score the replication using EXACTLY this vocabulary:
     REPLICATED | PARTIAL | SPOT-CHECK | NO-GO | CONTRADICTED | BLOCKED | FAILED
  3. Give one short paragraph justifying your verdict.
  4. Comment on: (a) is the simulation real (not fabricated), (b) is the substitution (SUSY-for-ttH) reasonable, (c) is the AUC comparison honest.

Output STRICTLY as JSON:
{"verdict": "...", "confidence_1_to_5": N, "justification": "...", "sim_is_real": true/false, "substitution_reasonable": true/false, "auc_comparison_honest": true/false}

--- (A) REPORT.md ---
""" + REPORT + "\n\n--- (B) evidence/qsvm_final.json ---\n" + EVID

URL = "http://127.0.0.1:44497/v1/chat/completions"
HEADERS = {"Authorization": "Bearer stevens", "Content-Type": "application/json"}

results = []
for model, name in JUDGES:
    print(f"\n=== {name} ({model}) ===")
    body = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.2,
        "max_tokens": 800,
    }
    try:
        r = requests.post(URL, headers=HEADERS, json=body, timeout=180)
        r.raise_for_status()
        j = r.json()
        txt = j["choices"][0]["message"]["content"]
        print(txt)
        results.append({"judge": name, "model": model, "response": txt})
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({"judge": name, "model": model, "error": str(e)})

out = os.path.join(os.path.dirname(__file__), "../report/evidence/judge_panel.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n[SAVED] {out}")
