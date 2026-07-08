#!/usr/bin/env python3
"""rejudge_all_3judge.py — coherent full re-judge of EVERY replication report.

Reuses the proven judge plumbing from score_unscored_3judge.py but:
  - operates on an EXPLICIT list of REPORT.md relative paths
    (REJUDGE_TARGETS_2026-06-24.txt), so reports at any depth are covered;
  - uses the canonical 3-judge panel gpt-5 / gemini-2.5-pro / claude-opus-4.7;
  - re-scores independently from report substance (ignores author self-scores);
  - checkpoints incrementally to REJUDGE_SCORES_2026-06-24.csv (resume-safe).

Policy: FREE Argo only (localhost:44497, key=stevens), 429-aware, low concurrency.
"""
from __future__ import annotations
import argparse, csv, json, os, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import median
from collections import Counter
import requests

ROOT = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT"))
TARGETS = ROOT / "REJUDGE_TARGETS_2026-06-24.txt"
OUT_CSV = ROOT / "REJUDGE_SCORES_2026-06-24.csv"

ARGO_URL = "http://localhost:44497/v1/chat/completions"
ARGO_KEY = "stevens"
# Canonical coherent panel: one OpenAI, one Google, one Anthropic — all FREE via Argo.
JUDGES = ["argo:gpt-5", "argo:gemini-2.5-pro", "argo:claude-opus-4.7"]

CSV_COLUMNS = [
    "collection","paper_id","verdict","coverage_10","agreement_10",
    "tools_top5","datasets","hardware","repo","judge_note","judge_panel_json","report_path",
]

VALID_VERDICTS = ["REPLICATED","PARTIAL","CONTRADICTED","BLOCKED","SPOT-CHECK","NO-GO","FAILED"]
VERDICT_SEVERITY = {"REPLICATED":0,"PARTIAL":1,"SPOT-CHECK":2,"CONTRADICTED":3,"BLOCKED":3,"NO-GO":4,"FAILED":5}
MAX_REPORT_CHARS = 60_000

RUBRIC = """You are scoring a scientific paper REPLICATION REPORT for a curated cross-disciplinary benchmark.
All reports must be judged on ONE coherent rubric regardless of field (radiation biology, PDEs, genomics, physics, ML).

Return STRICT JSON ONLY (no markdown fences, no prose outside JSON):
{{"coverage_10": <int 0-10>, "agreement_10": <int 0-10>, "verdict": "<REPLICATED|PARTIAL|SPOT-CHECK|CONTRADICTED|BLOCKED|NO-GO|FAILED>", "note": "<1-2 sentences citing concrete report evidence>"}}

COHERENT RUBRIC (apply to the REPORT TEXT below, not your priors):
- coverage_10 = fraction of the paper's primary analyzable units (claims/figures/experiments/datasets) the replication actually ATTEMPTED.
  10=all major units attempted; 8=>=80%; 5=~half; 2=one/few; 0=nothing attempted.
- agreement_10 = of what WAS tested, how well numbers/conclusions MATCH the paper.
  10=exact or within stated tolerance on all tested; 5=mixed; 0=tested items contradict or nothing testable.
- verdict (single coherent ladder):
  - REPLICATED: coverage>=8 AND agreement>=8 (broad scope reproduced and it matches).
  - PARTIAL: meaningful subset reproduced with real agreement, but coverage or agreement gaps remain.
  - SPOT-CHECK: only one/few claims tested (low coverage) but those checked out.
  - CONTRADICTED: a genuine reproduction attempt DISAGREES with the paper's central claim.
  - BLOCKED: reproduction blocked by missing data/code/hardware; little/no actual reproduction performed, but blocker is clearly named.
  - NO-GO: judged not worth/possible to reproduce; no reproduction work done.
  - FAILED: report is a stub/empty/placeholder, OR attempt made and broke down with no usable result.
- note: cite concrete evidence (specific figures reproduced, metrics matched, named blocker artifact).

IGNORE any author self-assigned Coverage/Agreement/Verdict in the report — re-score INDEPENDENTLY from the substantive content.
If the report is essentially empty/template, coverage_10=0 and verdict=FAILED.

PAPER ID: {paper_id}
COLLECTION: {collection}

REPORT TEXT (may be truncated):
---
{report_text}
---
Return ONLY the JSON object."""

TOOL_PATTERNS = ["Python","R ","Julia","C++","Fortran","MATLAB","PyTorch","TensorFlow","JAX",
    "scikit-learn","NumPy","SciPy","pandas","matplotlib","RDKit","Biopython","BLAST","DIAMOND",
    "MMseqs2","MAFFT","Prokka","BUSCO","QUAST","SPAdes","TOPAS","Geant4","MEDRAS","MCNP","OpenMC",
    "Quantum ESPRESSO","VASP","LAMMPS","GROMACS","OpenMM","OpenFOAM","Snakemake","Nextflow","Docker",
    "NetworkX","GraphBLAS","FEniCS","Dedalus","Clawpack","deepxde","emcee","enterprise"]
DATASET_PATTERNS = [r"PRJNA\d+",r"GSE\d+",r"PDB\s?\d[A-Z0-9]{3}",r"UniProt",r"Ensembl",r"RefSeq",
    r"BV-?BRC",r"PATRIC",r"KEGG",r"GenBank",r"ERA5",r"TARGET-?NBL",r"NANOGrav"]
HW_PATTERNS = ["A100","H100","H200","V100","MI250","MI300","PVC","GPU","CPU-only","uicgpu",
    "Aurora","Polaris","Sophia","DGX"]

def extract_light(text):
    out={"tools_top5":"","datasets":"","hardware":""}
    if not text: return out
    low=text.lower()
    t=[]
    for tok in TOOL_PATTERNS:
        if tok.lower() in low and tok not in t: t.append(tok)
        if len(t)>=5: break
    out["tools_top5"]=", ".join(t[:5])
    ds=set()
    for pat in DATASET_PATTERNS:
        for m in re.findall(pat,text): ds.add(m if isinstance(m,str) else " ".join(m))
        if len(ds)>=8: break
    out["datasets"]=", ".join(sorted(ds)[:8])
    hw=[]
    for tok in HW_PATTERNS:
        if tok.lower() in low and tok not in hw: hw.append(tok)
        if len(hw)>=4: break
    out["hardware"]=", ".join(hw)
    return out

def read_report(path, limit=MAX_REPORT_CHARS):
    try: text=Path(path).read_text(encoding="utf-8",errors="replace")
    except Exception as e: return f"[ERROR reading: {e}]"
    if len(text)<=limit: return text
    return text[:int(limit*0.7)]+"\n\n[... middle truncated ...]\n\n"+text[-int(limit*0.3):]

def call_judge(model, paper_id, collection, report_text, max_retries=5):
    prompt=RUBRIC.format(paper_id=paper_id, collection=collection, report_text=report_text)
    headers={"Authorization":f"Bearer {ARGO_KEY}","Content-Type":"application/json"}
    is_gpt5="gpt-5" in model
    payload={"model":model,"messages":[{"role":"user","content":prompt}],
             "max_tokens":4000 if is_gpt5 else 900}
    if not is_gpt5: payload["temperature"]=0
    backoff=4.0; last=None
    for _ in range(max_retries):
        try: r=requests.post(ARGO_URL,headers=headers,json=payload,timeout=200)
        except Exception as e:
            last=f"net:{e}"; time.sleep(backoff); backoff=min(backoff*1.6,30); continue
        if r.status_code==429:
            ra=r.headers.get("Retry-After")
            try: wait=float(ra) if ra else backoff
            except: wait=backoff
            time.sleep(min(wait,60)); backoff=min(backoff*1.6,60); last="429"; continue
        if r.status_code>=500:
            last=f"http:{r.status_code}"; time.sleep(backoff); backoff=min(backoff*1.6,30); continue
        if r.status_code!=200:
            return {"judge":model,"error":f"http:{r.status_code}","body":r.text[:200]}
        try: content=r.json()["choices"][0]["message"]["content"]
        except Exception as e: return {"judge":model,"error":f"resp:{e}"}
        c=content.strip()
        if c.startswith("```"):
            c=re.sub(r"^```[a-zA-Z]*","",c).strip()
            if c.endswith("```"): c=c[:-3].strip()
        try: parsed=json.loads(c)
        except Exception:
            m=re.search(r"\{.*\}",c,re.DOTALL)
            if not m: return {"judge":model,"error":"no_json","raw":content[:300]}
            try: parsed=json.loads(m.group(0))
            except Exception as e: return {"judge":model,"error":f"json:{e}","raw":content[:300]}
        try:
            cov=int(float(parsed.get("coverage_10"))); agr=int(float(parsed.get("agreement_10")))
            verdict=str(parsed.get("verdict","")).upper().strip(); note=str(parsed.get("note","")).strip()
        except Exception as e: return {"judge":model,"error":f"norm:{e}","raw":content[:300]}
        if verdict not in VALID_VERDICTS:
            up=verdict.replace("_","-").replace(" ","-")
            if up in VALID_VERDICTS: verdict=up
            elif "REPLIC" in verdict: verdict="REPLICATED"
            elif "PARTIAL" in verdict: verdict="PARTIAL"
            elif "SPOT" in verdict: verdict="SPOT-CHECK"
            elif "CONTRADICT" in verdict or "REFUT" in verdict: verdict="CONTRADICTED"
            elif "BLOCK" in verdict: verdict="BLOCKED"
            elif "NO" in verdict and "GO" in verdict: verdict="NO-GO"
            else: verdict="FAILED"
        return {"judge":model,"coverage_10":max(0,min(10,cov)),"agreement_10":max(0,min(10,agr)),
                "verdict":verdict,"note":note[:500]}
    return {"judge":model,"error":f"giveup:{last}"}

def aggregate(panel):
    covs=[p["coverage_10"] for p in panel if "coverage_10" in p]
    agrs=[p["agreement_10"] for p in panel if "agreement_10" in p]
    verds=[p["verdict"] for p in panel if "verdict" in p]
    if not covs or not verds: return None,None,None
    cov=int(round(median(covs))); agr=int(round(median(agrs)))
    counts=Counter(verds); top=counts.most_common(); top_n=top[0][1]
    tied=[v for v,n in top if n==top_n]
    verdict=tied[0] if len(tied)==1 else max(tied,key=lambda v:VERDICT_SEVERITY.get(v,99))
    return cov,agr,verdict

def collection_of(rel):
    top=rel.split("/")[0]
    if top.startswith("LUCID-replications"): return "LUCID-100"
    if top.startswith("LUCID-second100"): return "LUCID-second100"
    if top.startswith("PDE-replications"): return "PDE-100"
    if top.startswith("BVBRC"): return "BVBRC-100"
    return "OTHER"

def paper_id(rel):
    parts=rel.split("/")
    if parts[-1]=="REPORT.md": parts=parts[:-1]
    if parts and parts[-1]=="report": parts=parts[:-1]
    return parts[-1] if parts else rel

def score_one(rel):
    path=ROOT/rel
    coll=collection_of(rel); pid=paper_id(rel)
    text=read_report(path)
    base={"collection":coll,"paper_id":pid,"repo":rel,"report_path":rel}
    if not text or len(text.strip())<80:
        light=extract_light(text)
        return {**base,**light,"verdict":"FAILED","coverage_10":0,"agreement_10":0,
                "judge_note":f"empty/stub report ({len(text)} chars)",
                "judge_panel_json":json.dumps({"error":"empty"})}
    panel=[call_judge(j,pid,coll,text) for j in JUDGES]
    cov,agr,verdict=aggregate(panel)
    light=extract_light(text)
    if cov is None:
        return {**base,**light,"verdict":"FAILED","coverage_10":0,"agreement_10":0,
                "judge_note":"all judges errored","judge_panel_json":json.dumps({"panel":panel})}
    composite=" | ".join(f"[{p['judge'].split(':')[-1]}] {p.get('note','')}" for p in panel if "note" in p)
    return {**base,**light,"verdict":verdict,"coverage_10":cov,"agreement_10":agr,
            "judge_note":composite[:1500],"judge_panel_json":json.dumps({"panel":panel})}

_lock=threading.Lock()
def append_row(row):
    with _lock:
        with OUT_CSV.open("a",newline="") as f:
            csv.DictWriter(f,fieldnames=CSV_COLUMNS).writerow({k:row.get(k,"") for k in CSV_COLUMNS})

def load_done():
    if not OUT_CSV.exists(): return set()
    d=set()
    with OUT_CSV.open() as f:
        for row in csv.DictReader(f):
            if row.get("report_path"): d.add(row["report_path"])
    return d

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--concurrency",type=int,default=5)
    ap.add_argument("--limit",type=int,default=0)
    ap.add_argument("--filter",default="",help="only targets whose rel path contains this substring")
    args=ap.parse_args()
    targets=[l.strip() for l in TARGETS.read_text().splitlines() if l.strip() and not l.startswith("#")]
    if args.filter: targets=[t for t in targets if args.filter in t]
    if args.limit: targets=targets[:args.limit]
    if not OUT_CSV.exists() or OUT_CSV.stat().st_size==0:
        with OUT_CSV.open("w",newline="") as f:
            csv.DictWriter(f,fieldnames=CSV_COLUMNS).writeheader()
    done=load_done()
    todo=[t for t in targets if t not in done]
    print(f"[rejudge] targets={len(targets)} done={len(done)} todo={len(todo)}",flush=True)
    t0=time.time(); n=0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs={ex.submit(score_one,t):t for t in todo}
        for fut in as_completed(futs):
            t=futs[fut]
            try: row=fut.result()
            except Exception as e:
                row={"collection":collection_of(t),"paper_id":paper_id(t),"repo":t,"report_path":t,
                     "verdict":"FAILED","coverage_10":0,"agreement_10":0,
                     "judge_note":f"exc:{e}","judge_panel_json":json.dumps({"error":str(e)})}
            append_row(row); n+=1
            print(f"[{n}/{len(todo)}] {row['collection']}/{row['paper_id'][:40]} -> {row['verdict']} cov={row['coverage_10']} agr={row['agreement_10']}",flush=True)
    print(f"[rejudge] done {n} in {(time.time()-t0)/60:.1f} min",flush=True)

if __name__=="__main__":
    main()
