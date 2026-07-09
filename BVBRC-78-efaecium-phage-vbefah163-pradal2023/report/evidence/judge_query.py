#!/usr/bin/env python3
"""Query 3 Argo judges with the replication summary and collect verdicts."""
import json, urllib.request, sys, pathlib

payload_text = pathlib.Path(__file__).parent.joinpath("judge_input.md").read_text()

JUDGES = [
    "argo:claude-sonnet-4.6",
    "argo:gpt-5.4",
]

SYSTEM = ("You are an independent-replication judge for a scientific paper reproducibility "
          "project. Score the replication using ONLY the evidence provided, using the vocabulary: "
          "REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED. "
          "'Solid' = REPLICATED or PARTIAL. Do not inflate.")

results = {}
for model in JUDGES:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": payload_text},
        ],
        "temperature": 0.1,
        "max_tokens": 1200,
    }
    req = urllib.request.Request(
        "http://127.0.0.1:44497/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer stevens", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read().decode())
        txt = resp["choices"][0]["message"]["content"]
        results[model] = txt
        print(f"\n===== {model} =====\n{txt}\n", flush=True)
    except Exception as e:
        results[model] = f"ERROR: {e}"
        print(f"\n===== {model} FAILED =====\n{e}\n", flush=True)

out = pathlib.Path(__file__).parent.joinpath("judge_verdicts_j3.json")
out.write_text(json.dumps(results, indent=2))
print(f"\nSaved to {out}")
