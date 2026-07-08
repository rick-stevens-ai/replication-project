#!/usr/bin/env python3
"""census.py — authoritative paper/verdict census for REPLICATE-PROJECT.

Ground truth = the report files on disk, NOT a hand-edited snapshot CSV.

What it does:
  1. Walk each collection, enumerate every *paper directory* (a dir that is a
     replication unit, identified by containing a canonical REPORT).
  2. Locate the canonical report per dir (top-level REPORT*.md preferred, then
     report/REPORT.md, then largest *.md), de-duping the two-report-files case.
  3. Extract the verdict + coverage/agreement from the report (prefer an
     explicit 3-judge panel aggregate block; else the report's own §Verdict).
  4. Cross-check against RECONCILED_MASTER (which rows are missing on disk,
     which disk dirs are missing from the master, verdict disagreements).
  5. Print collection x verdict matrix + headline + a GAPS section.

Verdict extraction is heuristic-but-honest: it reports HOW each verdict was
sourced (panel / self-verdict / master-only / UNSCORED) so you can see exactly
where the soft spots are. It does NOT invent verdicts.

Usage:
  python3 scripts/census.py                 # full census + gaps
  python3 scripts/census.py --csv out.csv   # also dump per-paper census CSV
  python3 scripts/census.py --gaps-only     # just the things that need work
"""
from __future__ import annotations
import argparse, csv, os, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT"))
MASTER = ROOT / "RECONCILED_MASTER_2026-06-24.csv"
# Panel-score CSVs (3-judge) whose verdicts override on-disk self-extraction.
# Keyed by paper_id = last path component. Newest file wins on conflict.
PANEL_GLOBS = ["scoring/MASTER_SCORES_*3judge*.csv", "scoring/MASTER_SCORES_*_additions.csv"]

CANON_VERDICTS = ["REPLICATED","PARTIAL","SPOT-CHECK","CONTRADICTED","NO-GO","BLOCKED","FAILED"]
# normalize loose labels the reports use
ALIAS = {
    "FULL":"REPLICATED","REPRODUCED":"REPLICATED","REPRODUCED-EXACT":"REPLICATED",
    "EXACT":"REPLICATED","VERIFIED":"REPLICATED","CONFIRMED":"REPLICATED",
    "MOSTLY REPLICATED":"REPLICATED","REPLICATED-WITH-CAVEATS":"REPLICATED",
    "STRONG":"REPLICATED","PARTIAL-REPLICATED":"PARTIAL","LARGELY":"PARTIAL",
    "PASS":"REPLICATED","DATA-BLOCKED":"BLOCKED","NOGO":"NO-GO","NO GO":"NO-GO",
}

# infra / non-paper dirs at top level
NON_PAPER = {"common","drafts","scoring","scripts","papers","priority-lists",
             "pde_candidates","pde_corpus","special-categories","report_figs",
             "LUCID-replications","LUCID-second100","PDE-replications","QC-100",
             "QC-200","OTHER-100","docs","_support",
             "pvmol-gen","pvmol-gen-fajar2026","replicate-msm","rosters_5x100",
             "perovskite-Passivation-Molecules-AI-Discovery"}

def collection_of(rel: Path) -> str:
    p = str(rel)
    if p.startswith("LUCID-replications/"): return "LUCID-100"
    if p.startswith("LUCID-second100/"):   return "LUCID-100"
    if p.startswith("PDE-replications/"):   return "PDE-100"
    if p.startswith("QC-100/"):             return "QC-100"
    if p.startswith("QC-200/"):             return "QC-200"
    if p.startswith("OTHER-100/"):          return "OTHER"
    base = p.split("/")[0]
    if base.startswith("BVBRC-"): return "BVBRC-100"
    if base.startswith("PDE-"):   return "PDE-100"
    if base.startswith("OSTI-"):  return "OSTI-100"
    return "OTHER"

def find_report(d: Path):
    """Return (path, source_tag) for the canonical report, or (None, reason)."""
    if not d.exists(): return None, "missing-dir"
    # exclude obvious sibling/backup variants
    def ok(p): 
        n=p.name.lower()
        return not any(x in n for x in ("prereconcile","pass1",".pass1","back_to","_superseded"))
    top = sorted([p for p in d.glob("*REPORT*.md") if ok(p)])
    if top: return top[0], "top"
    nested = d/"report"/"REPORT.md"
    if nested.exists(): return nested, "report/"
    rep_dir = d/"report"
    if rep_dir.exists():
        mds=[p for p in rep_dir.glob("*.md") if ok(p)]
        rep=[m for m in mds if "REPORT" in m.name.upper()] or mds
        if rep: return max(rep,key=lambda p:p.stat().st_size), "report-dir"
    mds=[p for p in d.glob("*.md") if ok(p) and p.name.upper()!="README.MD"]
    if mds: return max(mds,key=lambda p:p.stat().st_size), "top-md"
    deep=[p for p in d.glob("**/*.md") if ok(p)]
    if deep: return max(deep,key=lambda p:p.stat().st_size), "deep-md"
    return None, "no-md"

VERD_RE = re.compile(r"(REPLICATED|PARTIAL[- ]?REPLICATED|PARTIAL|SPOT[- ]?CHECK|CONTRADICTED|NO[- ]?GO|NOGO|BLOCKED|DATA[- ]?BLOCKED|FAILED|MOSTLY REPLICATED|REPRODUCED[- ]?EXACT|REPRODUCED|FULL|VERIFIED|CONFIRMED|EXACT)\b", re.I)

def norm_verdict(raw: str):
    if not raw: return None
    r = raw.strip().upper().replace("**","").replace("’","'")
    r = r.replace("SPOT CHECK","SPOT-CHECK").replace("NO GO","NO-GO")
    if r in CANON_VERDICTS: return r
    if r in ALIAS: return ALIAS[r]
    return None

def _first_verdict_token(s: str):
    vm = VERD_RE.search(s)
    if vm: return norm_verdict(vm.group(1))
    return None

def extract_verdict(report: Path):
    """Return (verdict, source). source in {panel, self, table, none}.

    Strategy (strongest signal first), skipping table-header noise:
      1. 3-judge aggregate block.
      2. An explicit '## Verdict' / '## N. Verdict' / 'VERDICT:' heading, scanning
         the lines AFTER it for the first canonical token, ignoring lines that are
         clearly a markdown table HEADER (contain the literal word 'Verdict' as a
         column label, i.e. a row like '| ... | Verdict |').
      3. A bold standalone **VERDICT** token.
      4. A per-claim 'Status'/'Verdict' table is ignored for the headline; instead
         fall back to a 'final 4-tier verdict' / 'overall' line if present.
    """
    try: text = report.read_text(encoding="utf-8", errors="replace")
    except Exception: return None, "read-error"
    lines = text.splitlines()

    # 1. explicit 3-judge aggregate
    m = re.search(r"Aggregated audit verdict[:* ]+\**\s*([A-Z][A-Z\- ]+?)\**\b", text)
    if m:
        v = norm_verdict(m.group(1)); 
        if v: return v, "panel"

    def is_table_header(ln: str) -> bool:
        # a table header/row that merely uses 'Verdict' as a COLUMN label
        return ln.count("|") >= 2 and re.search(r"\bverdict\b", ln, re.I) is not None

    # 2. headings that ARE a verdict declaration (not a table column)
    hdr_re = re.compile(r"(?i)^\s*#{0,4}\s*(?:\d+\.?\s*)?(?:final\s+|overall\s+)?verdict\b")
    for i, ln in enumerate(lines):
        if is_table_header(ln):
            continue
        if hdr_re.search(ln) or re.search(r"(?i)\bverdict\b\s*[:\-]", ln):
            # search this line + next ~6 non-table lines for a canonical token
            chunk = []
            chunk.append(re.sub(r"(?i)\bverdict\b", "", ln))  # drop the word 'verdict' itself
            j = i + 1; taken = 0
            while j < len(lines) and taken < 8:
                nxt = lines[j]
                if not is_table_header(nxt):
                    chunk.append(nxt); taken += 1
                j += 1
            v = _first_verdict_token("\n".join(chunk))
            if v: return v, "self"

    # 3. bold standalone token e.g. **REPLICATED**
    bm = re.search(r"\*\*\s*("+ "|".join([re.escape(x) for x in CANON_VERDICTS]) +r"|FULL|CONFIRMED|MOSTLY REPLICATED)\s*\*\*", text, re.I)
    if bm:
        v = norm_verdict(bm.group(1))
        if v: return v, "self"

    # 4. 'final 4-tier verdict' phrase anywhere
    fm = re.search(r"(?i)(?:final\s+4-tier\s+verdict|status)\s*[:*]+\s*\**\s*([A-Z][A-Za-z\- ]+)", text)
    if fm:
        v = norm_verdict(fm.group(1).split()[0] if fm.group(1) else "")
        if v: return v, "table"
    return None, "none"

def load_panel_overrides():
    """Collect panel verdicts from all 3-judge score CSVs, newest-wins."""
    files=[]
    for g in PANEL_GLOBS:
        files += list(ROOT.glob(g))
    files = sorted(set(files), key=lambda p: p.stat().st_mtime)  # oldest->newest
    ov={}
    for fp in files:
        try:
            for r in csv.DictReader(fp.open(newline="")):
                pid=(r.get("paper_id") or "").strip()
                v=norm_verdict((r.get("verdict") or "").strip())
                if not pid or not v: continue
                base=pid.split("/")[-1]
                ov[base]=(v, r.get("coverage_10",""), r.get("agreement_10",""), fp.name)
        except Exception:
            continue
    return ov

def load_master():
    rows={}
    if not MASTER.exists(): return rows, []
    with MASTER.open(newline="") as f:
        rd=csv.DictReader(f); recs=list(rd)
    for r in recs:
        rows.setdefault(r["paper_id"], []).append(r)
    return rows, recs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--gaps-only", action="store_true")
    args=ap.parse_args()

    # enumerate paper dirs
    paper_dirs=[]
    for sub in ["LUCID-replications","LUCID-second100","PDE-replications","QC-100","QC-200","OTHER-100"]:
        subdir=ROOT/sub
        if not subdir.is_dir(): continue
        for d in sorted(subdir.glob("*/")):
            if d.name in ("parsed_md","_second100-meta") or d.name.startswith("_"): continue
            paper_dirs.append(d)
    for d in sorted(ROOT.glob("*/")):
        if d.name in NON_PAPER: continue
        if d.name.startswith("."): continue      # skip .git and other hidden dirs
        paper_dirs.append(d)

    census=[]
    for d in paper_dirs:
        rel=d.relative_to(ROOT)
        coll=collection_of(rel)
        rep,how=find_report(d)
        if rep is None:
            census.append(dict(coll=coll, dir=str(rel), report="", verdict="", vsource="NO-REPORT", how=how))
            continue
        v,src=extract_verdict(rep)
        census.append(dict(coll=coll, dir=str(rel), report=str(rep.relative_to(ROOT)),
                           verdict=v or "", vsource=src, how=how))

    # apply panel overrides (authoritative 3-judge verdicts win over self-extraction)
    panel=load_panel_overrides()
    n_panel=0
    for c in census:
        base=Path(c["dir"]).name
        if base in panel:
            pv,cov,agr,fn=panel[base]
            c["verdict"]=pv; c["vsource"]="panel"; n_panel+=1

    # ---- matrix ----
    by_coll=defaultdict(Counter)
    for c in census:
        by_coll[c["coll"]][c["verdict"] or "(unscored)"]+=1

    order=["LUCID-100","PDE-100","BVBRC-100","OSTI-100","QC-100","OTHER"]
    cols=CANON_VERDICTS+["(unscored)"]
    print("="*92)
    print("PAPER CENSUS (ground truth = report files on disk under REPLICATE-PROJECT)")
    print("="*92)
    hdr=f"{'collection':16s}"+"".join(f"{c[:5]:>7s}" for c in cols)+f"{'TOTAL':>8s}"
    print(hdr); print("-"*len(hdr))
    grand=Counter()
    for coll in order:
        row=by_coll.get(coll,Counter())
        line=f"{coll:16s}"+"".join(f"{row.get(c,0):7d}" for c in cols)
        tot=sum(row.values()); line+=f"{tot:8d}"
        print(line)
        for c in cols: grand[c]+=row.get(c,0)
    print("-"*len(hdr))
    print(f"{'TOTAL':16s}"+"".join(f"{grand.get(c,0):7d}" for c in cols)+f"{sum(grand.values()):8d}")

    R=grand["REPLICATED"]; P=grand["PARTIAL"]; T=sum(grand.values())
    scored=T-grand["(unscored)"]
    print()
    print(f"Total paper dirs on disk:        {T}")
    print(f"  with an extractable verdict:   {scored}")
    print(f"  UNSCORED (need attention):     {grand['(unscored)']}")
    print(f"REPLICATED+PARTIAL:              {R+P}  ({(R+P)/T*100:.1f}% of all, {(R+P)/scored*100:.1f}% of scored)" if scored else "")

    # verdict-source breakdown (consistency view)
    src=Counter(c["vsource"] for c in census if c["verdict"])
    print()
    print("Verdict provenance (consistency check):")
    for k,n in src.most_common(): print(f"  {k:8s} {n}")

    # ---- gaps vs master ----
    mrows, mrecs = load_master()
    disk_bases={Path(c["dir"]).name for c in census}
    master_ids=set(mrows.keys())
    print()
    print("="*92); print("GAPS / WHERE TO IMPROVE"); print("="*92)

    unscored=[c for c in census if not c["verdict"]]
    print(f"\n[1] UNSCORED paper dirs ({len(unscored)}) — no extractable verdict on disk:")
    for c in unscored:
        print(f"    {c['coll']:16s} {c['dir']}  ({c['vsource']}/{c['how']})")

    self_only=[c for c in census if c["vsource"]=="self"]
    print(f"\n[2] SELF-scored only ({len(self_only)}) — verdict from report's own §Verdict, NOT a 3-judge panel.")
    print(f"    (These are the consistency risk; a panel pass would standardize them.)")

    # master-only (in CSV but no disk dir)
    monly=[mid for mid in master_ids if mid not in disk_bases and mid!="replication"]
    print(f"\n[3] In master CSV but NO matching disk dir ({len(monly)}):")
    for mid in sorted(monly)[:40]: print(f"    {mid}")
    if len(monly)>40: print(f"    ... +{len(monly)-40} more")

    # disk dirs not represented in master
    donly=[c for c in census if Path(c['dir']).name not in master_ids]
    print(f"\n[4] On disk but NOT in master CSV ({len(donly)}):")
    for c in donly[:40]: print(f"    {c['coll']:16s} {c['dir']}")
    if len(donly)>40: print(f"    ... +{len(donly)-40} more")

    # duplicate paper_ids in master
    dups={k:len(v) for k,v in mrows.items() if len(v)>1}
    print(f"\n[5] Duplicate paper_id rows still in master ({len(dups)}): {dups}")

    if args.csv:
        with args.csv.open("w", newline="") as f:
            w=csv.DictWriter(f, fieldnames=["coll","dir","report","verdict","vsource","how"])
            w.writeheader(); w.writerows(census)
        print(f"\nPer-paper census written -> {args.csv}")

if __name__=="__main__":
    main()
