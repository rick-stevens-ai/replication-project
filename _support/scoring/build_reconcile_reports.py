#!/usr/bin/env python3
"""build_reconcile_reports.py — produce the canonical reconciled master CSV +
a top-level RECONCILIATION_REPORT and one per-collection report from the
coherent 3-judge scores.
"""
import csv, os, json
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean

ROOT = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT"))
SCORES = ROOT / "REJUDGE_SCORES_2026-06-24.csv"
DATE = "2026-06-24"
VERDICT_ORDER = ["REPLICATED","PARTIAL","SPOT-CHECK","CONTRADICTED","BLOCKED","NO-GO","FAILED"]

def fnum(x):
    try: return float(x)
    except: return None

def main():
    rows = list(csv.DictReader(open(SCORES)))
    # canonical master CSV (clean column set)
    cols = ["collection","paper_id","verdict","coverage_10","agreement_10","tools_top5","datasets","hardware","repo"]
    with open(ROOT / f"RECONCILED_MASTER_{DATE}.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for r in sorted(rows,key=lambda x:(x["collection"],x["paper_id"])):
            w.writerow({k:r.get(k,"") for k in cols})

    by_coll=defaultdict(list)
    for r in rows: by_coll[r["collection"]].append(r)

    def dist(rs):
        c=Counter(r["verdict"] for r in rs)
        return {v:c.get(v,0) for v in VERDICT_ORDER if c.get(v,0)}
    def stats(rs):
        cov=[fnum(r["coverage_10"]) for r in rs if fnum(r["coverage_10"]) is not None]
        agr=[fnum(r["agreement_10"]) for r in rs if fnum(r["agreement_10"]) is not None]
        return (round(mean(cov),2) if cov else 0, round(mean(agr),2) if agr else 0)

    # top-level report
    lines=[f"# Replication Project — Reconciliation Report ({DATE})","",
           "All replication REPORT.md files re-judged on a single coherent rubric by a 3-judge LLM panel",
           "(argo gpt-5 / gemini-2.5-pro / claude-opus-4.7, free Argo only; median scores, majority verdict,",
           "conservative tiebreak). Author self-scores were ignored; each report was re-scored independently.","",
           f"**Total reports reconciled:** {len(rows)}","",
           "## Canonical scoring scheme","",
           "- **Verdict ladder:** REPLICATED → PARTIAL → SPOT-CHECK → CONTRADICTED → BLOCKED → NO-GO → FAILED",
           "- **Coverage /10:** fraction of the paper's analyzable units attempted",
           "- **Agreement /10:** match between reproduced and reported results, on what was tested",
           "- Every report now carries a `## Canonical Verdict` block (original preserved as `REPORT.prereconcile.md`).","",
           "## Corpus verdict distribution",""]
    d=dist(rows); tot=len(rows)
    lines.append("| Verdict | N | % |")
    lines.append("|---|---|---|")
    for v in VERDICT_ORDER:
        n=d.get(v,0)
        if n: lines.append(f"| {v} | {n} | {100*n/tot:.1f}% |")
    cov,agr=stats(rows)
    lines += ["", f"**Mean coverage:** {cov}/10  ·  **Mean agreement:** {agr}/10","",
              "## By collection","",
              "| Collection | N | Mean Cov | Mean Agr | Distribution |","|---|---|---|---|---|"]
    for coll in sorted(by_coll):
        rs=by_coll[coll]; c,a=stats(rs)
        dd=", ".join(f"{k} {v}" for k,v in dist(rs).items())
        lines.append(f"| {coll} | {len(rs)} | {c} | {a} | {dd} |")
    lines += ["","## Artifacts","",
              f"- `RECONCILED_MASTER_{DATE}.csv` — unified score table",
              f"- `REJUDGE_SCORES_{DATE}.csv` — full 3-judge panel detail (per-judge JSON)",
              f"- `scoring/rejudge_all_3judge.py` — judging tool",
              f"- `scoring/apply_canonical_headers.py` — header normalizer",
              f"- per-collection reports: `RECONCILE_<COLLECTION>_{DATE}.md`",""]
    (ROOT / f"RECONCILIATION_REPORT_{DATE}.md").write_text("\n".join(lines))

    # per-collection reports
    for coll in sorted(by_coll):
        rs=sorted(by_coll[coll],key=lambda r:(VERDICT_ORDER.index(r["verdict"]) if r["verdict"] in VERDICT_ORDER else 99, -(fnum(r["coverage_10"]) or 0)))
        c,a=stats(rs)
        L=[f"# Reconciliation — {coll} ({DATE})","",
           f"{len(rs)} reports · mean coverage {c}/10 · mean agreement {a}/10","",
           "| Verdict | Cov | Agr | Paper |","|---|---|---|---|"]
        for r in rs:
            L.append(f"| {r['verdict']} | {r['coverage_10']} | {r['agreement_10']} | `{r['paper_id']}` |")
        L+=["","## Verdict distribution",""]
        for k,v in dist(rs).items(): L.append(f"- {k}: {v}")
        safe=coll.replace("/","_")
        (ROOT / f"RECONCILE_{safe}_{DATE}.md").write_text("\n".join(L))

    print(f"Wrote RECONCILIATION_REPORT_{DATE}.md + {len(by_coll)} per-collection reports + RECONCILED_MASTER_{DATE}.csv")
    print("Verdict dist:", dict(Counter(r['verdict'] for r in rows)))

if __name__=="__main__":
    main()
