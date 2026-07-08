#!/usr/bin/env python3
"""
FRONT 3 fetcher — pull TCGA-GBM open data for the independent
generalizability test: clinical/survival + RNA-Seq STAR Counts +
Gene-Level Copy Number Variation + Masked Somatic Mutations.

GBM has a well-known molecular biomarker (MGMT methylation,
IDH1/2 mutation) that we will use as the standard-of-care comparator.

Outputs under /data/stevens/alter-pathB/data/tcga_gbm/:
    cases.json   cases_flat.tsv
    files_rna.tsv   files_cnv.tsv  files_meth.tsv   files_clinical.tsv
    rna/<file_id>.tsv       (STAR Counts per case)
    cnv/<file_id>.tsv       (Gene Level Copy Number)
    meth/<file_id>.txt      (Methylation Beta Value)
    clinical/<file_id>.xml  (BCR Clinical XML)
"""
from __future__ import annotations
import json, os, time
from pathlib import Path
import requests

GDC = "https://api.gdc.cancer.gov"
PROJECT = "TCGA-GBM"
OUT = Path("/data/stevens/alter-pathB/data/tcga_gbm")
for sub in ("rna","cnv","meth","clinical"):
    (OUT/sub).mkdir(parents=True, exist_ok=True)
LOG = open(OUT/"fetch_log.txt","w")
def log(m): print(m, flush=True); LOG.write(m+"\n"); LOG.flush()

def post(url, payload, retries=3, timeout=180):
    last=None
    for i in range(retries):
        try:
            r=requests.post(url,json=payload,timeout=timeout); r.raise_for_status(); return r.json()
        except Exception as e:
            last=e; log(f"  retry {i+1}: {e}"); time.sleep(2**i)
    raise last

def get_bytes(url, retries=3, timeout=600):
    last=None
    for i in range(retries):
        try:
            r=requests.get(url,timeout=timeout,stream=True); r.raise_for_status()
            buf=b""
            for chunk in r.iter_content(1<<20): buf+=chunk
            return buf
        except Exception as e:
            last=e; log(f"  retry {i+1}: {e}"); time.sleep(2**i)
    raise last

def fetch_cases():
    log(f"== Fetch {PROJECT} cases (clinical/survival) ==")
    fields = ",".join([
        "case_id","submitter_id","disease_type",
        "demographic.vital_status","demographic.gender","demographic.race",
        "demographic.days_to_death","demographic.age_at_index",
        "diagnoses.age_at_diagnosis","diagnoses.tumor_grade",
        "diagnoses.ajcc_pathologic_stage",
        "diagnoses.days_to_death","diagnoses.days_to_last_follow_up",
        "diagnoses.primary_diagnosis","diagnoses.treatments.treatment_type",
    ])
    payload = {"filters":{"op":"in","content":{"field":"project.project_id","value":[PROJECT]}},
               "fields":fields,"format":"JSON","size":2000}
    js = post(f"{GDC}/cases", payload)
    hits = js.get("data",{}).get("hits",[])
    log(f"  cases: {len(hits)}")
    (OUT/"cases.json").write_text(json.dumps(js, indent=2))
    rows=[]
    for h in hits:
        d = (h.get("diagnoses") or [{}])[0] or {}
        dem = h.get("demographic") or {}
        days_d = d.get("days_to_death") or dem.get("days_to_death")
        days_l = d.get("days_to_last_follow_up")
        vital = dem.get("vital_status")
        t = days_d if (vital=="Dead" and days_d is not None) else days_l
        ev = 1 if vital=="Dead" else 0
        rows.append({
            "case_id":h.get("case_id"),
            "submitter_id":h.get("submitter_id"),
            "vital_status":vital,
            "gender":dem.get("gender"),
            "race":dem.get("race"),
            "age_at_diagnosis_days":d.get("age_at_diagnosis"),
            "tumor_grade":d.get("tumor_grade"),
            "stage":d.get("ajcc_pathologic_stage"),
            "primary_diagnosis":d.get("primary_diagnosis"),
            "days_to_death":days_d,
            "days_to_last_follow_up":days_l,
            "time_days":t,
            "event":ev,
        })
    keys=list(rows[0].keys())
    with open(OUT/"cases_flat.tsv","w") as f:
        f.write("\t".join(keys)+"\n")
        for r in rows: f.write("\t".join("" if r[k] is None else str(r[k]) for k in keys)+"\n")
    have_t=sum(1 for r in rows if r["time_days"] is not None)
    have_e=sum(1 for r in rows if r["event"]==1)
    log(f"  with follow-up time: {have_t}; deaths: {have_e}")
    return rows

def fetch_files_kind(data_type, label):
    payload = {"filters":{"op":"and","content":[
        {"op":"in","content":{"field":"cases.project.project_id","value":[PROJECT]}},
        {"op":"in","content":{"field":"access","value":["open"]}},
        {"op":"in","content":{"field":"data_type","value":[data_type]}},
    ]},
    "fields":"file_id,file_name,file_size,data_format,data_type,access,experimental_strategy,platform,analysis.workflow_type,cases.case_id,cases.submitter_id,cases.samples.sample_type",
    "format":"JSON","size":5000}
    js = post(f"{GDC}/files", payload)
    hits = js.get("data",{}).get("hits",[])
    log(f"  {label}: {len(hits)} files")
    rows=[]
    for h in hits:
        c=(h.get("cases") or [{}])[0]
        s=((c.get("samples") or [{}])[0]) if c.get("samples") else {}
        rows.append({"file_id":h["file_id"],"file_name":h.get("file_name"),
                     "file_size":h.get("file_size"),
                     "workflow":(h.get("analysis") or {}).get("workflow_type"),
                     "platform":h.get("platform"),
                     "case_submitter":c.get("submitter_id"),
                     "sample_type":s.get("sample_type")})
    return hits, rows

def write_tsv(rows, path):
    if not rows: return
    keys=list(rows[0].keys())
    with open(path,"w") as f:
        f.write("\t".join(keys)+"\n")
        for r in rows: f.write("\t".join("" if r[k] is None else str(r[k]) for k in keys)+"\n")

def download(rows, subdir, prefer_primary=True):
    out_dir = OUT/subdir
    # If many files per patient, prefer Primary Tumor, then de-dup by patient
    pool = rows[:]
    if prefer_primary:
        prim = [r for r in pool if r.get("sample_type")=="Primary Tumor"]
        if prim: pool = prim
    seen=set(); dedup=[]
    for r in sorted(pool, key=lambda x: x["file_id"]):
        if r["case_submitter"] in seen: continue
        seen.add(r["case_submitter"]); dedup.append(r)
    log(f"  {subdir}: {len(dedup)} files to download (one per patient)")
    manifest=[]
    for i,r in enumerate(dedup):
        fid=r["file_id"]; fname=r.get("file_name") or fid
        out_path = out_dir / f"{fid}_{fname}"
        if out_path.exists() and out_path.stat().st_size>0:
            manifest.append((fid, r["case_submitter"], r.get("sample_type"), out_path.stat().st_size, "cached")); continue
        try:
            buf=get_bytes(f"{GDC}/data/{fid}")
            out_path.write_bytes(buf)
            manifest.append((fid, r["case_submitter"], r.get("sample_type"), len(buf), "ok"))
            if (i+1)%25==0: log(f"  {subdir}: {i+1}/{len(dedup)}")
        except Exception as e:
            manifest.append((fid, r["case_submitter"], r.get("sample_type"), 0, f"fail:{e}"))
    with open(OUT/f"{subdir}_manifest.tsv","w") as f:
        f.write("file_id\tcase_submitter\tsample_type\tbytes\tstatus\n")
        for r in manifest: f.write("\t".join(str(x) for x in r)+"\n")
    log(f"  {subdir}: {sum(1 for x in manifest if x[4] in ('ok','cached'))}/{len(manifest)} downloaded")
    return manifest

def main():
    log(f"== START {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    fetch_cases()
    # RNA-Seq STAR Counts
    h, rows = fetch_files_kind("Gene Expression Quantification","RNA STAR Counts")
    write_tsv(rows, OUT/"files_rna.tsv"); download(rows, "rna")
    # Gene-level CNV
    h, rows = fetch_files_kind("Gene Level Copy Number","Gene Level CNV")
    write_tsv(rows, OUT/"files_cnv.tsv"); download(rows, "cnv")
    # Methylation beta
    h, rows = fetch_files_kind("Methylation Beta Value","Methylation Beta")
    write_tsv(rows, OUT/"files_meth.tsv"); download(rows, "meth")
    # Clinical supplement
    h, rows = fetch_files_kind("Clinical Supplement","Clinical Supplement")
    write_tsv(rows, OUT/"files_clinical.tsv"); download(rows, "clinical", prefer_primary=False)
    log(f"== DONE {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    LOG.close()

if __name__ == "__main__":
    main()
