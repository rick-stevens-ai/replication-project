#!/usr/bin/env python3
"""
Wave-4 LLM-judge: score a replication against paper headline claims via FREE Argo endpoint.
Usage: python3 wave4_llm_judge.py <results.json> <paper_title> <headline_claims_text>
Prints a JSON verdict block. Free endpoints only (localhost:4000 then :44497).
"""
import sys, json, urllib.request

ENDPOINTS = ["http://localhost:4000/v1/chat/completions",
             "http://localhost:44497/v1/chat/completions"]
# opus-4.x is currently returning an upstream parse error through the aggregator (2026-07-19);
# sonnet-4.6 is the working free high-quality Argo model. Falls back to gpt-4o.
MODEL = "argo:claude-sonnet-4.6"
MODEL_FALLBACK = "argo:gpt-4o"

def call(messages):
    last = None
    for model in (MODEL, MODEL_FALLBACK):
        body = json.dumps({"model": model, "messages": messages, "temperature": 0}).encode()
        for url in ENDPOINTS:
            try:
                req = urllib.request.Request(url, data=body,
                      headers={"Content-Type":"application/json","Authorization":"Bearer stevens"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    d = json.loads(r.read())
                    c = d["choices"][0]["message"]["content"]
                    if c and c.strip():
                        return c
            except Exception as e:
                last = e
    raise RuntimeError(f"all endpoints/models failed: {last}")

def main():
    results_path, title, claims_text = sys.argv[1], sys.argv[2], sys.argv[3]
    results = open(results_path).read()
    sys_p = ("You are a rigorous computational-physics replication judge. You compare a "
             "replication's numeric results against a paper's headline claims. Be honest and "
             "quantitative. Output ONLY a JSON object with keys: verdict (one of "
             "'REPLICATED','PARTIAL','FAILED'), coverage (int 0-10, how many claims addressed), "
             "agreement (int 0-10, numeric agreement quality), justification (<=120 words, "
             "cite specific numbers), caveats (<=60 words). No markdown fences.")
    usr = (f"PAPER: {title}\n\nHEADLINE CLAIMS:\n{claims_text}\n\n"
           f"REPLICATION RESULTS (results.json):\n{results}\n\n"
           "Judge whether the replication reproduces the headline claims. Reduced-model / "
           "absolute-unit-normalization mismatches => PARTIAL, not FAILED, if the mechanism/law "
           "is reproduced. Output the JSON verdict only.")
    out = call([{"role":"system","content":sys_p},{"role":"user","content":usr}])
    out = out.strip()
    if out.startswith("```"):
        out = out.split("```")[1].replace("json","",1).strip()
    print(out)

if __name__ == "__main__":
    main()
