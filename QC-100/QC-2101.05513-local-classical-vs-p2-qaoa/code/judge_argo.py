#!/usr/bin/env python
"""
3-judge Argo panel for the QC-100 QAOA replication report.
"""
import json, os, sys, time
import urllib.request

REPORT = open("report/REPORT.md").read()

RUBRIC = """You are an expert reviewer scoring an INDEPENDENT REPLICATION of a
published paper.  The paper is Marwaha 2021 (arXiv:2101.05513): "Local classical
MAX-CUT algorithm outperforms p=2 QAOA on high-girth regular graphs".

Please assess the attached REPORT.md and output a single verdict from this set:
  REPLICATED / PARTIAL / SPOT-CHECK / NO-GO / CONTRADICTED / BLOCKED / FAILED

Also give:
  * a 1-line justification (no more than 20 words)
  * a numeric confidence 0-100
  * any specific concerns

Output MUST be valid JSON with keys: verdict, one_line, confidence, concerns.
No prose outside the JSON.

REPORT.md contents follow between the markers.
--- BEGIN REPORT ---
""" + REPORT + """
--- END REPORT ---
"""

def call_argo(model, prompt):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        "http://localhost:44497/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer stevens",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def extract_json(text):
    # find first {...} block
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                return text[start:i + 1]
    return text


judges = [
    "argo:claude-sonnet-4.6",
    "argo:gpt-5.2",
    "argo:gemini-2.5-pro",
]

results = []
def call_with_retry(j, prompt, tries=3):
    last_err = None
    for k in range(tries):
        try:
            return call_argo(j, prompt)
        except Exception as e:
            last_err = e
            print(f"    retry {k+1}/{tries}: {e}")
            time.sleep(3 * (k + 1))
    raise last_err

for j in judges:
    print(f"[judge] calling {j}...")
    t0 = time.time()
    try:
        resp = call_with_retry(j, RUBRIC)
        content = resp["choices"][0]["message"]["content"]
        js = extract_json(content)
        try:
            parsed = json.loads(js)
        except Exception:
            parsed = {"raw": content, "parse_error": True}
        parsed["_judge_model"] = j
        parsed["_latency_sec"] = time.time() - t0
        results.append(parsed)
        print(f"  {j}: verdict={parsed.get('verdict')} conf={parsed.get('confidence')} in {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"  {j}: ERROR {e}")
        results.append({"_judge_model": j, "error": str(e)})

os.makedirs("report/evidence", exist_ok=True)
with open("report/evidence/judges.json", "w") as f:
    json.dump(results, f, indent=2)

# Majority verdict
from collections import Counter
verdicts = [r.get("verdict") for r in results if r.get("verdict")]
maj = Counter(verdicts).most_common(1)
print()
print(f"Panel verdicts: {verdicts}")
if maj:
    print(f"Majority: {maj[0][0]} ({maj[0][1]}/{len(judges)})")
