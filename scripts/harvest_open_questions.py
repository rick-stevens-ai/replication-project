#!/usr/bin/env python3
"""Harvest every report/open_questions.json into a master corpus JSONL.
Run periodically; idempotent (rewrites the master from scratch each run)."""
import os, glob, json

BASE = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT")
OUT = os.path.join(BASE, "OPEN_QUESTIONS_CORPUS.jsonl")

def find_oq_files():
    pats = [
        os.path.join(BASE, "QC-100", "*", "report", "open_questions.json"),
        os.path.join(BASE, "QC-200", "*", "report", "open_questions.json"),
        os.path.join(BASE, "LUCID-replications", "*", "report", "open_questions.json"),
        os.path.join(BASE, "PDE-*", "report", "open_questions.json"),
        os.path.join(BASE, "BVBRC-*", "report", "open_questions.json"),
        os.path.join(BASE, "OSTI-*", "report", "open_questions.json"),
        # also any nested location
        os.path.join(BASE, "**", "open_questions.json"),
    ]
    seen = set(); files = []
    for p in pats:
        for f in glob.glob(p, recursive=True):
            rf = os.path.realpath(f)
            if rf in seen: continue
            seen.add(rf); files.append(f)
    return files

def set_of(path):
    rel = os.path.relpath(path, BASE)
    top = rel.split(os.sep)[0]
    for s in ("QC-100","QC-200"):
        if top == s: return s
    if top == "LUCID-replications": return "LUCID"
    for s in ("PDE","BVBRC","OSTI"):
        if top.startswith(s): return s
    return top

def dir_of(path):
    # dir containing report/
    d = os.path.dirname(path)
    if os.path.basename(d) == "report":
        d = os.path.dirname(d)
    return os.path.basename(d)

n_files = n_q = 0
with open(OUT, "w") as out:
    for f in find_oq_files():
        try:
            data = json.load(open(f))
        except Exception as e:
            continue
        if not isinstance(data, list):
            data = data.get("questions", []) if isinstance(data, dict) else []
        setn = set_of(f); dirn = dir_of(f)
        n_files += 1
        for i, q in enumerate(data, 1):
            if isinstance(q, str):
                q = {"q": q}
            rec = {"set": setn, "dir": dirn, "qn": i,
                   "q": q.get("q") or q.get("question") or "",
                   "basis": q.get("basis") or "",
                   "next_steps": q.get("next_steps") or q.get("nextSteps") or ""}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_q += 1
print(f"harvested {n_q} questions from {n_files} files -> {OUT}")
