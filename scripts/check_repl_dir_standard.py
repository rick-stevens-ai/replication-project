#!/usr/bin/env python3
"""Audit each replication dir against the 8-artifact standard (Rick 2026-07-05).

Usage:
  check_repl_dir_standard.py                 # audit all sets, print per-set summary
  check_repl_dir_standard.py --missing       # also list per-dir missing items
  check_repl_dir_standard.py --set QC-100    # one set
  check_repl_dir_standard.py --csv OUT.csv   # write per-dir CSV
"""
import os, glob, csv, argparse, re
from collections import defaultdict

BASE = os.path.expanduser(os.environ.get("REPLICATE_BASE", "~/Dropbox/REPLICATE-PROJECT"))

# Container sets (dir-of-dirs) vs flat prefix sets (top-level SET-* dirs)
CONTAINERS = {"QC-100": "QC-100", "QC-200": "QC-200", "LUCID": "LUCID-replications",
              "OTHER": "OTHER-100"}
FLAT_PREFIXES = {"PDE": "PDE-", "BVBRC": "BVBRC-", "OSTI": "OSTI-", "TEXTURE": "TEXTURE-"}

def big(f, n=1500):
    try: return os.path.getsize(f) >= n
    except OSError: return False

def any_glob(d, pats, minsize=1500):
    for p in pats:
        for f in glob.glob(os.path.join(d, p), recursive=True):
            if big(f, minsize): return f
    return None

def check_dir(d):
    """Return dict item->path-or-None for the 8 artifacts."""
    r = {}
    # 1 PDF
    r["1_pdf"] = any_glob(d, ["paper.pdf", "*.pdf", "work/*.pdf", "**/*.pdf"], 3000)
    # 2 Marker .md (exclude report/brief md)
    marker = None
    for f in glob.glob(os.path.join(d, "**", "*.md"), recursive=True):
        b = os.path.basename(f).lower()
        if b in ("report.md","brief.md","attempt_log.md","artifact_harvest.md","readme.md",
                 "workflow.md","artifacts_summary.md","failure_analysis.md","open_questions.md"):
            continue
        if big(f, 1500): marker = f; break
    r["2_marker_md"] = marker
    # 3 Nougat .mmd
    r["3_nougat_mmd"] = any_glob(d, ["**/*.mmd"], 1000)
    # 4 LaTeX report
    r["4_report_tex"] = any_glob(d, ["report/REPORT.tex","**/REPORT.tex","**/*.tex"], 1000)
    # 5 open questions
    r["5_open_questions"] = any_glob(d, ["report/open_questions.json","**/open_questions.json"], 100)
    # 6 workflow
    r["6_workflow"] = any_glob(d, ["report/workflow.md","**/workflow.md"], 300)
    # 7 artifacts summary
    r["7_artifacts_summary"] = any_glob(d, ["report/artifacts_summary.md","**/artifacts_summary.md"], 200)
    # 8 failure analysis
    r["8_failure_analysis"] = any_glob(d, ["report/failure_analysis.md","**/failure_analysis.md"], 200)
    return r

def gather_dirs(only=None):
    groups = defaultdict(list)
    for key, cont in CONTAINERS.items():
        if only and key != only: continue
        p = os.path.join(BASE, cont)
        if os.path.isdir(p):
            for d in glob.glob(os.path.join(p, "*")):
                if os.path.isdir(d) and not os.path.basename(d).startswith("_"):
                    groups[key].append(d)
    for key, pref in FLAT_PREFIXES.items():
        if only and key != only: continue
        for d in glob.glob(os.path.join(BASE, pref + "*")):
            if os.path.isdir(d) and not os.path.basename(d).startswith("_"):
                groups[key].append(d)
    return groups

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--set", dest="only")
    ap.add_argument("--csv")
    a = ap.parse_args()
    groups = gather_dirs(a.only)
    ITEMS = ["1_pdf","2_marker_md","3_nougat_mmd","4_report_tex","5_open_questions",
             "6_workflow","7_artifacts_summary","8_failure_analysis"]
    rows = []
    print("8-artifact standard audit (Rick 2026-07-05)\n"+"="*70)
    gtot = defaultdict(int); gn = 0
    for key in ("QC-100","QC-200","LUCID","PDE","BVBRC","OSTI","TEXTURE","OTHER"):
        subs = groups.get(key, [])
        if not subs: continue
        counts = defaultdict(int); complete = 0
        for d in subs:
            r = check_dir(d)
            present = {k: bool(v) for k, v in r.items()}
            for k, ok in present.items():
                if ok: counts[k] += 1; gtot[k] += 1
            if all(present.values()): complete += 1
            rows.append((key, os.path.basename(d), present))
            if a.missing:
                miss = [k for k in ITEMS if not present[k]]
                if miss: print(f"   [{key}] {os.path.basename(d)[:44]:44s} missing: {','.join(x.split('_')[0] for x in miss)}")
        n = len(subs); gn += n
        print(f"\n{key}: {n} dirs | ALL-8 complete: {complete}/{n}")
        for k in ITEMS:
            print(f"    {k:20s} {counts[k]:3d}/{n}")
    print("\n"+"="*70+f"\nTOTAL dirs: {gn}")
    for k in ITEMS:
        print(f"  {k:20s} {gtot[k]:3d}/{gn}")
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["set","dir"]+ITEMS)
            for key, name, present in rows:
                w.writerow([key, name]+[int(present[k]) for k in ITEMS])
        print("wrote", a.csv)

if __name__ == "__main__":
    main()
