#!/usr/bin/env python3
"""write_verdict.py — append a canonical, re-extractable Verdict line to a report.

Usage:
  python3 scripts/write_verdict.py --report <path> --verdict REPLICATED \
      --coverage 8 --agreement 7 --rationale "one-line justification"

Canonical verdicts: REPLICATED, PARTIAL, SPOT-CHECK, CONTRADICTED, NO-GO, BLOCKED, FAILED

Writes (idempotently) a block the census extractor will pick up:

  ## Verdict
  **Verdict: <V>** (Coverage <c>/10, Agreement <a>/10) — <rationale>
  <!-- census-verdict: <V> assigned 2026-07-08 by LLM judge (Argo Opus) -->

For .md reports it appends markdown; for .tex reports it inserts a
\\section{Verdict} block before \\end{document} (or appends if none).
It refuses to add a second census-verdict block (idempotent).
"""
import argparse, datetime, sys
from pathlib import Path

CANON = {"REPLICATED","PARTIAL","SPOT-CHECK","CONTRADICTED","NO-GO","BLOCKED","FAILED"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--coverage", default="")
    ap.add_argument("--agreement", default="")
    ap.add_argument("--rationale", default="")
    a=ap.parse_args()
    v=a.verdict.strip().upper().replace(" ","-")
    if v=="NOGO": v="NO-GO"
    if v not in CANON:
        print(f"ERROR: '{a.verdict}' not canonical {sorted(CANON)}", file=sys.stderr); sys.exit(2)
    p=Path(a.report)
    if not p.exists():
        print(f"ERROR: no such report {p}", file=sys.stderr); sys.exit(2)
    text=p.read_text(encoding="utf-8", errors="replace")
    if "census-verdict:" in text:
        print(f"SKIP (already has census-verdict): {p}"); return
    date=datetime.date.today().isoformat()
    cov=f"Coverage {a.coverage}/10, " if a.coverage else ""
    agr=f"Agreement {a.agreement}/10" if a.agreement else ""
    meta=(cov+agr).strip().strip(",")
    meta=f" ({meta})" if meta else ""
    rat=f" — {a.rationale}" if a.rationale else ""
    if p.suffix.lower()==".tex":
        block=(f"\n\\section{{Verdict}}\n"
               f"\\textbf{{Verdict: {v}}}{meta}.{rat}\n"
               f"% census-verdict: {v} assigned {date} by LLM judge (Argo Opus)\n")
        if "\\end{document}" in text:
            text=text.replace("\\end{document}", block+"\n\\end{document}", 1)
        else:
            text=text+block
    else:
        block=(f"\n\n## Verdict\n\n"
               f"**Verdict: {v}**{meta}.{rat}\n\n"
               f"<!-- census-verdict: {v} assigned {date} by LLM judge (Argo Opus) -->\n")
        text=text+block
    p.write_text(text, encoding="utf-8")
    print(f"WROTE Verdict: {v} -> {p}")

if __name__=="__main__":
    main()
