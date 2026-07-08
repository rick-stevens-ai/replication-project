#!/usr/bin/env python3
"""
FRONT 1 fetcher for TARGET-NBL — pulls public clinical/survival metadata
and the open Gene Expression Quantification (GEQ) files via the GDC API.

Outputs (under /data/stevens/alter-pathB/data/target_nbl/):
    cases.json                 - raw GDC cases payload (size=2000)
    cases_flat.tsv             - one row per case, flattened key fields
    files_geq.json             - raw GDC files payload for open RNA-Seq GEQ
    files_geq.tsv              - one row per file, with case id + workflow
    expression/<file_id>.tsv   - downloaded per-file count tables
    expression_manifest.tsv    - what was downloaded
    fetch_log.txt              - fetch summary
"""
from __future__ import annotations
import json
import os
import sys
import time
import gzip
import hashlib
from pathlib import Path

import requests

GDC = "https://api.gdc.cancer.gov"
OUT = Path("/data/stevens/alter-pathB/data/target_nbl")
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "expression").mkdir(parents=True, exist_ok=True)

LOG = open(OUT / "fetch_log.txt", "w")

def log(msg):
    print(msg, flush=True)
    LOG.write(msg + "\n"); LOG.flush()


def post_json(url, payload, retries=3, timeout=120):
    last = None
    for i in range(retries):
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            log(f"  POST retry {i+1}: {e}")
            time.sleep(2 ** i)
    raise last


def get_bytes(url, retries=3, timeout=300):
    last = None
    for i in range(retries):
        try:
            r = requests.get(url, timeout=timeout, stream=True)
            r.raise_for_status()
            buf = b""
            for chunk in r.iter_content(chunk_size=1 << 20):
                buf += chunk
            return buf
        except Exception as e:
            last = e
            log(f"  GET retry {i+1}: {e}")
            time.sleep(2 ** i)
    raise last


# ---------------------------------------------------------------------------
# 1. Cases — clinical / survival / demographics
# ---------------------------------------------------------------------------
def fetch_cases():
    log("== Fetch TARGET-NBL cases (clinical/survival) ==")
    fields = ",".join([
        "case_id","submitter_id","disease_type","primary_site",
        "demographic.vital_status","demographic.gender","demographic.race",
        "demographic.ethnicity","demographic.year_of_birth",
        "demographic.days_to_death",
        "diagnoses.age_at_diagnosis","diagnoses.tumor_stage","diagnoses.ajcc_pathologic_stage",
        "diagnoses.days_to_death","diagnoses.days_to_last_follow_up",
        "diagnoses.classification_of_tumor","diagnoses.morphology",
        "diagnoses.primary_diagnosis","diagnoses.tissue_or_organ_of_origin",
        # extra annotations that some TARGET-NBL records carry
        "diagnoses.annotations.notes",
    ])
    payload = {
        "filters": {"op":"in","content":{"field":"project.project_id","value":["TARGET-NBL"]}},
        "fields": fields,
        "format":"JSON",
        "size": 2000,
    }
    out = post_json(f"{GDC}/cases", payload)
    n = len(out.get("data",{}).get("hits",[]))
    log(f"  cases hits = {n}")
    (OUT/"cases.json").write_text(json.dumps(out, indent=2))
    # Flatten
    rows = []
    for h in out["data"]["hits"]:
        d = (h.get("diagnoses") or [{}])[0] or {}
        dem = h.get("demographic") or {}
        days_death = d.get("days_to_death") or dem.get("days_to_death")
        days_last = d.get("days_to_last_follow_up")
        vital = dem.get("vital_status")
        # event time: prefer death; else last follow-up
        t = days_death if (vital == "Dead" and days_death is not None) else days_last
        ev = 1 if vital == "Dead" else 0
        rows.append({
            "case_id": h.get("case_id"),
            "submitter_id": h.get("submitter_id"),
            "vital_status": vital,
            "gender": dem.get("gender"),
            "race": dem.get("race"),
            "age_at_diagnosis_days": d.get("age_at_diagnosis"),
            "tumor_stage": d.get("tumor_stage"),
            "ajcc_stage": d.get("ajcc_pathologic_stage"),
            "primary_diagnosis": d.get("primary_diagnosis"),
            "days_to_death": days_death,
            "days_to_last_follow_up": days_last,
            "time_days": t,
            "event": ev,
        })
    # Write TSV
    keys = list(rows[0].keys()) if rows else []
    with open(OUT/"cases_flat.tsv","w") as fh:
        fh.write("\t".join(keys)+"\n")
        for r in rows:
            fh.write("\t".join("" if r[k] is None else str(r[k]) for k in keys)+"\n")
    log(f"  wrote cases_flat.tsv ({len(rows)} rows)")
    # Summary
    have_time = sum(1 for r in rows if r["time_days"] is not None)
    have_event = sum(1 for r in rows if r["event"] == 1)
    log(f"  cases with follow-up time: {have_time}/{len(rows)}; deaths: {have_event}")
    return rows


# ---------------------------------------------------------------------------
# 2. Files — open Gene Expression Quantification
# ---------------------------------------------------------------------------
def fetch_geq_files():
    log("== Fetch open Gene Expression Quantification files ==")
    payload = {
        "filters": {"op":"and","content":[
            {"op":"in","content":{"field":"cases.project.project_id","value":["TARGET-NBL"]}},
            {"op":"in","content":{"field":"data_category","value":["Transcriptome Profiling"]}},
            {"op":"in","content":{"field":"data_type","value":["Gene Expression Quantification"]}},
            {"op":"in","content":{"field":"access","value":["open"]}},
        ]},
        "fields": ",".join([
            "file_id","file_name","file_size","access","experimental_strategy",
            "data_type","data_format","platform",
            "analysis.workflow_type","analysis.workflow_version",
            "cases.case_id","cases.submitter_id",
            "cases.samples.sample_type","cases.samples.submitter_id",
        ]),
        "format":"JSON",
        "size": 5000,
    }
    out = post_json(f"{GDC}/files", payload)
    hits = out.get("data",{}).get("hits",[])
    log(f"  open GEQ files = {len(hits)}")
    (OUT/"files_geq.json").write_text(json.dumps(out, indent=2))
    rows = []
    for h in hits:
        case = (h.get("cases") or [{}])[0]
        sample = ((case.get("samples") or [{}])[0]) if case.get("samples") else {}
        rows.append({
            "file_id": h.get("file_id"),
            "file_name": h.get("file_name"),
            "file_size": h.get("file_size"),
            "workflow_type": (h.get("analysis") or {}).get("workflow_type"),
            "platform": h.get("platform"),
            "case_id": case.get("case_id"),
            "case_submitter": case.get("submitter_id"),
            "sample_type": sample.get("sample_type"),
            "sample_submitter": sample.get("submitter_id"),
        })
    keys = list(rows[0].keys()) if rows else []
    with open(OUT/"files_geq.tsv","w") as fh:
        fh.write("\t".join(keys)+"\n")
        for r in rows:
            fh.write("\t".join("" if r[k] is None else str(r[k]) for k in keys)+"\n")
    log(f"  wrote files_geq.tsv ({len(rows)} rows)")
    # Workflow type breakdown
    from collections import Counter
    wf = Counter(r["workflow_type"] for r in rows)
    log(f"  workflow_type histogram: {dict(wf)}")
    st = Counter(r["sample_type"] for r in rows)
    log(f"  sample_type histogram: {dict(st)}")
    return rows


# ---------------------------------------------------------------------------
# 3. Download each open GEQ file
# ---------------------------------------------------------------------------
def download_geq(rows):
    log("== Download open GEQ files ==")
    manifest = []
    for i, r in enumerate(rows):
        fid = r["file_id"]
        out_path = OUT / "expression" / f"{fid}.tsv"
        if out_path.exists() and out_path.stat().st_size > 0:
            manifest.append((fid, r["case_submitter"], r["sample_type"], out_path.stat().st_size, "cached"))
            continue
        url = f"{GDC}/data/{fid}"
        try:
            buf = get_bytes(url)
            # GDC returns either gzipped TSV or plain TSV
            if buf[:2] == b"\x1f\x8b":
                try:
                    buf = gzip.decompress(buf)
                except Exception:
                    pass
            out_path.write_bytes(buf)
            manifest.append((fid, r["case_submitter"], r["sample_type"], len(buf), "ok"))
            if (i+1) % 25 == 0:
                log(f"  downloaded {i+1}/{len(rows)} ({fid} -> {len(buf)} bytes)")
        except Exception as e:
            log(f"  FAIL {fid}: {e}")
            manifest.append((fid, r["case_submitter"], r["sample_type"], 0, f"fail:{e}"))
    with open(OUT/"expression_manifest.tsv","w") as fh:
        fh.write("file_id\tcase_submitter\tsample_type\tbytes\tstatus\n")
        for row in manifest:
            fh.write("\t".join(str(x) for x in row) + "\n")
    log(f"  wrote expression_manifest.tsv ({len(manifest)} rows)")
    return manifest


# ---------------------------------------------------------------------------
# 4. Try to recover MYCN status / INSS stage / risk from clinical XML/TSV
#    GDC TARGET clinical TSV downloads carry stage + risk + MYCN status.
# ---------------------------------------------------------------------------
def fetch_clinical_supplement():
    log("== Fetch clinical-supplement files (BCR XML / TSV) ==")
    payload = {
        "filters": {"op":"and","content":[
            {"op":"in","content":{"field":"cases.project.project_id","value":["TARGET-NBL"]}},
            {"op":"in","content":{"field":"data_category","value":["Clinical"]}},
            {"op":"in","content":{"field":"access","value":["open"]}},
        ]},
        "fields": "file_id,file_name,file_size,data_format,data_type,cases.submitter_id,cases.case_id",
        "format":"JSON",
        "size": 5000,
    }
    out = post_json(f"{GDC}/files", payload)
    hits = out.get("data",{}).get("hits",[])
    log(f"  open Clinical files = {len(hits)}")
    (OUT/"files_clinical.json").write_text(json.dumps(out, indent=2))
    # Download all (these are small XML/TSV)
    cdir = OUT/"clinical"; cdir.mkdir(exist_ok=True)
    rows=[]
    for h in hits:
        fid = h["file_id"]; fname = h.get("file_name") or fid
        out_path = cdir / f"{fid}_{fname}"
        if out_path.exists() and out_path.stat().st_size > 0:
            rows.append((fid, fname, out_path.stat().st_size, "cached"))
            continue
        try:
            buf = get_bytes(f"{GDC}/data/{fid}")
            out_path.write_bytes(buf)
            rows.append((fid, fname, len(buf), "ok"))
        except Exception as e:
            rows.append((fid, fname, 0, f"fail:{e}"))
    with open(OUT/"clinical_manifest.tsv","w") as fh:
        fh.write("file_id\tfile_name\tbytes\tstatus\n")
        for r in rows: fh.write("\t".join(str(x) for x in r)+"\n")
    log(f"  wrote clinical_manifest.tsv ({len(rows)} rows)")
    return rows


def main():
    log(f"== START {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    cases = fetch_cases()
    geq = fetch_geq_files()
    download_geq(geq)
    fetch_clinical_supplement()
    log(f"== DONE {time.strftime('%Y-%m-%d %H:%M:%S')} ==")
    LOG.close()


if __name__ == "__main__":
    main()
