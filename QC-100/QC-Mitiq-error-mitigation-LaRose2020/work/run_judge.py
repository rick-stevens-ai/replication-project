import json, urllib.request
prompt = open("judge_prompt.txt").read()
for model in ["argo:claude-opus-4.8", "gpt-5.2", "gpt-4o", "argo:gpt-4o"]:
    body = json.dumps({"model": model,
        "messages": [{"role": "user", "content": prompt}], "temperature": 0.0}).encode()
    req = urllib.request.Request("http://localhost:44497/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer stevens"})
    try:
        r = urllib.request.urlopen(req, timeout=120)
        d = json.load(r)
        txt = d["choices"][0]["message"]["content"]
        print(f"=== JUDGE MODEL: {model} ===\n")
        print(txt)
        open("evidence_llm_judge.txt", "w").write(f"JUDGE MODEL: {model}\n\n{txt}\n")
        break
    except Exception as e:
        err = e.read().decode()[:300] if hasattr(e, "read") else str(e)[:300]
        print(f"[{model} failed] {err}\n")
