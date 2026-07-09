#!/usr/bin/env python3
"""Rebuild RECONCILED_MASTER from the census ground-truth CSV.

- Census (scripts/census.py --csv CENSUS_*.csv) is disk-truth.
- Drop admin/infra/dup dirs (no real paper).
- Keep canonical schema so downstream report tooling still reads it.
- Pull coverage_10/agreement_10 from the newest 3-judge panel CSV when present,
  else leave blank (self-scored rows have verdict but no panel numbers).
"""
import csv, glob, os, re, sys
from collections import defaultdict

ROOT = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT")
CENSUS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "CENSUS_2026-07-03.csv")
OUT = os.path.join(ROOT, "RECONCILED_MASTER_2026-06-24.csv")

CANON = ["REPLICATED","PARTIAL","SPOT-CHECK","CONTRADICTED","NO-GO","BLOCKED","FAILED"]

# dirs that are not real papers
SKIP_SUBSTR = ["_LUCID100_ADMIN","_LUCID100_WAVE1_LAUNCH","_harvest","_missing_data_hunt",
               "_second100-meta",".git","/memory","roary_out","_WAVE_DUP","QC-100$",
               "OTHER,QC-100","report-dir-only"]
SKIP_EXACT = {"OTHER::.git","OTHER::memory","OTHER::roary_out","OTHER::QC-100",
              "OTHER::_WAVE_DUPES_2026-07-01","OTHER::_WAVE_DUPS"}

def is_skip(coll, d):
    key = f"{coll}::{d}"
    if key in SKIP_EXACT: return True
    base = os.path.basename(d.rstrip("/"))
    if base.startswith("_"): return True
    if d in (".git","memory","roary_out","QC-100"): return True
    if base in ("_harvest","_missing_data_hunt","_second100-meta"): return True
    return False

# --- load newest panel CSV for coverage/agreement numbers ---
panel = {}  # normalized paper key -> (cov, agr, verdict)
panel_files = sorted(glob.glob(os.path.join(ROOT,"scoring","MASTER_SCORES_*3judge*.csv")))
def keyify(s):
    return re.sub(r"[^a-z0-9]","", (s or "").lower())
for pf in panel_files:
    try:
        for r in csv.DictReader(open(pf)):
            pid = r.get("paper_id") or r.get("dir") or r.get("paper") or ""
            cov = r.get("coverage_10") or r.get("coverage") or r.get("median_coverage") or ""
            agr = r.get("agreement_10") or r.get("agreement") or r.get("median_agreement") or ""
            vd  = r.get("verdict_canon") or r.get("verdict") or ""
            if pid:
                panel[keyify(pid)] = (cov, agr, vd)
    except Exception as e:
        print(f"  warn: {pf}: {e}", file=sys.stderr)

rows_out = []
counts = defaultdict(lambda: defaultdict(int))
for r in csv.DictReader(open(CENSUS)):
    coll, d, verdict, vsource = r["coll"], r["dir"], r["verdict"].strip().upper(), r["vsource"]
    if is_skip(coll, d):
        continue
    if not verdict:
        # unscored but a real dir -> keep as (unscored) row so gaps stay visible
        verdict = ""
    # canonicalize
    if verdict and verdict not in CANON:
        m = {"FULL":"REPLICATED","CONFIRMED":"REPLICATED","EXACT":"REPLICATED","MOSTLY":"REPLICATED",
             "DATA-BLOCKED":"BLOCKED"}
        verdict = m.get(verdict, verdict)
    pid = os.path.basename(d.rstrip("/"))
    k = keyify(pid)
    cov = agr = ""
    if k in panel:
        cov, agr, pv = panel[k]
        if pv and vsource != "panel":
            vsource = "panel"
    rows_out.append({
        "collection": coll,
        "paper_id": pid,
        "verdict_canon": verdict,
        "coverage_10": cov,
        "agreement_10": agr,
        "verdict_raw": verdict,
        "flag_noncanon_verdict": "0",
        "flag_no_score": "1" if not cov else "0",
        "rel": d,
        "vsource": vsource,
    })
    counts[coll][verdict or "(unscored)"] += 1

# backup then write
import shutil, datetime
if os.path.exists(OUT):
    bak = OUT + ".bak-pre-rebuild-" + datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    shutil.copy2(OUT, bak)
    print(f"backup -> {os.path.basename(bak)}")

cols = ["collection","paper_id","verdict_canon","coverage_10","agreement_10",
        "verdict_raw","flag_noncanon_verdict","flag_no_score","rel","vsource"]
with open(OUT,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in sorted(rows_out, key=lambda x:(x["collection"],x["paper_id"])):
        w.writerow(r)

print(f"\nwrote {len(rows_out)} rows -> {os.path.basename(OUT)}\n")
gt=gs=0
print(f"{'SET':14} {'total':>6} {'solid':>6}  breakdown")
for c in sorted(counts):
    tot=sum(counts[c].values()); solid=counts[c].get("REPLICATED",0)+counts[c].get("PARTIAL",0)
    gt+=tot; gs+=solid
    bd=", ".join(f"{k}:{n}" for k,n in sorted(counts[c].items(),key=lambda x:-x[1]))
    print(f"{c:14} {tot:>6} {solid:>6}  {bd}")
print(f"{'TOTAL':14} {gt:>6} {gs:>6}")
