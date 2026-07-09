#!/usr/bin/env python3
"""LLM-judge scoring via Argo proxy (free)."""
import json, os, sys, urllib.request

REPORT = open('/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-69-acinetobacter-abgri4/report/REPORT.md').read()

RUBRIC = """
You are an independent scientific-replication auditor. Read the REPORT below,
which describes an attempt to independently reproduce the core claims of a
published paper on real public data.

Score each of the following on a strict 0–5 scale (0 = missing/fabricated,
1 = minimal, 3 = adequate, 5 = exceptional and verified). Give a single JSON
object as your final output, no prose after.

Fields:
- claim_coverage:  Do the tested claims cover the paper's main findings?
- data_provenance: Are data sources real, cited by accession, and free?
- method_soundness: Are the methods appropriate for testing each claim?
- evidence_strength: Is the numeric/genomic evidence strong (identities, coverages, coordinates)?
- reproducibility: Could a third party rerun this from the report + scripts?
- verdict_alignment: Does the declared verdict match the evidence given? (5=fully supported, 1=overstated, 0=fabricated)
- overall_reliability: your bottom-line 0-5.

Also emit:
- verdict_recommended: one of {REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED}
- notes: <= 3 short bullet points on any concerns
- best_line: single-sentence summary suitable for the wave result line.

Return ONLY the JSON object.
"""

payload = {
    "model": "argo:gpt-5",
    "messages": [
        {"role": "system", "content": "You are an evidence-driven scientific auditor. Output only valid JSON."},
        {"role": "user", "content": RUBRIC + "\n\n---REPORT---\n\n" + REPORT}
    ],
    # gpt-5 rejects non-default temperature; leave it off.
}

req = urllib.request.Request(
    "http://localhost:44497/v1/chat/completions",
    data=json.dumps(payload).encode('utf-8'),
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer stevens",
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=180) as resp:
    data = json.loads(resp.read())

content = data['choices'][0]['message']['content'].strip()
# Try to parse — strip markdown fences if present
if content.startswith('```'):
    content = content.split('```', 2)[1]
    if content.startswith('json'):
        content = content[4:]
    content = content.strip().rstrip('`').strip()
try:
    parsed = json.loads(content)
except Exception as e:
    print("Could not JSON-parse LLM output; raw follows:", file=sys.stderr)
    print(content)
    sys.exit(1)

out = {
    "judge_model": "argo:gpt-5",
    "judge_endpoint": "http://localhost:44497/v1 (Argo, free)",
    "scores": parsed,
    "raw_model_response": data,
}
outfile = '/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-69-acinetobacter-abgri4/report/evidence/llm_judge.json'
os.makedirs(os.path.dirname(outfile), exist_ok=True)
with open(outfile, 'w') as fh:
    json.dump(out, fh, indent=2)
print(json.dumps(parsed, indent=2))
