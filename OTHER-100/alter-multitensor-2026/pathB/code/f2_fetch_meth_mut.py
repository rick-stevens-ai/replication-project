#!/usr/bin/env python3
"""
FRONT 2 fetcher — pull open methylation beta-value files + open MAF mutation
files for TARGET-NBL. Will be used to build the second/third GSVD layers.

Outputs under /data/stevens/alter-pathB/data/target_nbl/:
    files_meth.tsv  files_meth.json   meth/<file_id>.txt    meth_manifest.tsv
    files_maf.tsv   files_maf.json    maf/<file_id>.maf.gz  maf_manifest.tsv
"""
from __future__ import annotations
import json, os, time
from pathlib import Path
import requests

GDC = "https://api.gdc.cancer.gov"
OUT = Path("/data/stevens/alter-pathB/data/target_nbl")
(OUT/"meth").mkdir(parents=True, exist_ok=True)
(OUT/"maf").mkdir(parents=True, exist_ok=True)
LOG = open(OUT/"fetch_f2.log","w")
def log(m): print(m, flush=True); LOG.write(m+"\n"); LOG.flush()

def post(url, payload, retries=3, timeout=180):
    for i in range(retries):
        try:
            r = requests.post(url, json=payload, timeout=timeout); r.raise_for_status(); return r.json()
        except Exception as e:
            log(f"  retry {i+1}: {e}"); time.sleep(2**i)
    raise

def get_bytes(url, retries=3, timeout=600):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=timeout, stream=True); r.raise_for_status()
            buf=b""
            for chunk in r.iter_content(1<<20): buf+=chunk
            return buf
        except Exception as e:
            log(f"  retry {i+1}: {e}"); time.sleep(2**i)
    raise

def fetch_list(data_type, label):
    log(f"== Fetch open {label}")
    payload = {
        "filters": {"op":"and","content":[
            {"op":"in","content":{"field":"cases.project.project_id","value":["TARGET-NBL"]}},
            {"op":"in","content":{"field":"access","value":["open"]}},
            {"op":"in","content":{"field":"data_type","value":[data_type]}},
        ]},
        "fields": "file_id,file_name,file_size,access,data_format,platform,experimental_strategy,analysis.workflow_type,cases.submitter_id,cases.samples.sample_type",
        "format":"JSON","size":5000,
    }
    js = post(f"{GDC}/files", payload)
    hits = js.get("data",{}).get("hits",[])
    log(f"  {label}: {len(hits)} files")
    return hits

def write_tsv(hits, path):
    rows=[]
    for h in hits:
        c = (h.get("cases") or [{}])[0]
        s = ((c.get("samples") or [{}])[0]) if c.get("samples") else {}
        rows.append({
            "file_id": h.get("file_id"),
            "file_name": h.get("file_name"),
            "file_size": h.get("file_size"),
            "format": h.get("data_format"),
            "workflow": (h.get("analysis") or {}).get("workflow_type"),
            "platform": h.get("platform"),
            "case_submitter": c.get("submitter_id"),
            "sample_type": s.get("sample_type"),
        })
    keys = list(rows[0].keys())
    with open(path,"w") as f:
        f.write("\t".join(keys)+"\n")
        for r in rows:
            f.write("\t".join(("" if r[k] is None else str(r[k])) for k in keys)+"\n")
    return rows

def download(hits, subdir, ext_hint=""):
    out_dir = OUT/subdir; out_dir.mkdir(exist_ok=True)
    manifest=[]
    for i,h in enumerate(hits):
        fid = h["file_id"]; fname = h.get("file_name") or fid
        out_path = out_dir / f"{fid}_{fname}"
        if out_path.exists() and out_path.stat().st_size > 0:
            manifest.append((fid, out_path.name, out_path.stat().st_size, "cached")); continue
        try:
            buf = get_bytes(f"{GDC}/data/{fid}")
            out_path.write_bytes(buf)
            manifest.append((fid, out_path.name, len(buf), "ok"))
            if (i+1)%25==0: log(f"  {subdir}: downloaded {i+1}/{len(hits)}")
        except Exception as e:
            manifest.append((fid, fname, 0, f"fail:{e}"))
            log(f"  FAIL {fid}: {e}")
    with open(OUT/f"{subdir}_manifest.tsv","w") as f:
        f.write("file_id\tfile_name\tbytes\tstatus\n")
        for r in manifest: f.write("\t".join(str(x) for x in r)+"\n")
    log(f"  {subdir}: {sum(1 for r in manifest if r[3] in ('ok','cached'))} ok / {len(manifest)}")
    return manifest

def main():
    log(f"== START {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    # Methylation beta values
    meth = fetch_list("Methylation Beta Value", "Methylation Beta Value")
    write_tsv(meth, OUT/"files_meth.tsv")
    (OUT/"files_meth.json").write_text(json.dumps({"hits": meth}, indent=2))
    download(meth, "meth")
    # Masked Somatic Mutation MAFs
    muts = fetch_list("Masked Somatic Mutation", "Masked Somatic Mutation")
    write_tsv(muts, OUT/"files_maf.tsv")
    (OUT/"files_maf.json").write_text(json.dumps({"hits": muts}, indent=2))
    download(muts, "maf")
    log(f"== DONE {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    LOG.close()

if __name__ == "__main__":
    main()
