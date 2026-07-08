#!/usr/bin/env python3
"""apply_canonical_headers.py — prepend the canonical Verdict block to every
REPORT.md using the coherent 3-judge scores in REJUDGE_SCORES_2026-06-24.csv.

For each report:
  1. Back up original to REPORT.prereconcile.md (once; never overwrite a backup).
  2. Strip any prior canonical block we inserted (idempotent re-runs).
  3. Prepend a standardized block:

       <!-- CANONICAL-RECONCILE v1 2026-06-24 -->
       # <existing H1 title if present, else paper_id>

       ## Canonical Verdict
       | Field | Value |
       |---|---|
       | Verdict | <X> |
       | Coverage | C/10 |
       | Agreement | A/10 |
       | Scoring method | 3-judge LLM panel (argo gpt-5 / gemini-2.5-pro / claude-opus-4.7), median + majority |
       | Reproducibility blocker | <named blocker or "none / fully reproduced"> |
       | Reconciled | 2026-06-24 |

       _Per-judge panel: gpt-5 cov/agr/verdict ; gemini ... ; opus ..._
       <!-- /CANONICAL-RECONCILE -->

       <original body follows, with its leading H1 removed to avoid dupes>

Idempotent: detects the marker and replaces the block instead of stacking.
"""
import csv, json, os, re, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT"))
SCORES = ROOT / "REJUDGE_SCORES_2026-06-24.csv"
MARK_START = "<!-- CANONICAL-RECONCILE v1 2026-06-24 -->"
MARK_END = "<!-- /CANONICAL-RECONCILE -->"

def panel_line(panel_json):
    try:
        panel = json.loads(panel_json).get("panel", [])
    except Exception:
        return ""
    bits = []
    for p in panel:
        j = p.get("judge","?").split(":")[-1]
        if "coverage_10" in p:
            bits.append(f"{j} {p['coverage_10']}/{p['agreement_10']}·{p.get('verdict','?')}")
        else:
            bits.append(f"{j} ERR({p.get('error','')})")
    return " ; ".join(bits)

def infer_blocker(note, verdict):
    # Prefer an explicit blocker phrase from the judges' notes.
    m = re.search(r"(blocked? by|missing|not deposited|not archived|requires|needs)\s+[^.|]{4,90}", note, re.I)
    if m:
        return m.group(0).strip().rstrip(".,")
    if verdict in ("REPLICATED",):
        return "none / fully reproduced"
    if verdict in ("BLOCKED","NO-GO"):
        return "see report — reproduction blocked (named in body)"
    return "see report body"

def strip_existing_block(text):
    if MARK_START in text and MARK_END in text:
        pre, rest = text.split(MARK_START, 1)
        _, post = rest.split(MARK_END, 1)
        return (pre + post).lstrip("\n")
    return text

def extract_h1(body):
    m = re.match(r"\s*#\s+(.+)", body)
    if m:
        title = m.group(1).strip()
        body_wo = body[m.end():].lstrip("\n")
        return title, body_wo
    return None, body

def build_block(row, h1):
    title = h1 or row["paper_id"]
    blocker = infer_blocker(row.get("judge_note",""), row["verdict"])
    pl = panel_line(row.get("judge_panel_json",""))
    return f"""{MARK_START}
# {title}

## Canonical Verdict
| Field | Value |
|---|---|
| Paper | `{row['paper_id']}` |
| Collection | {row['collection']} |
| **Verdict** | **{row['verdict']}** |
| Coverage | {row['coverage_10']}/10 |
| Agreement | {row['agreement_10']}/10 |
| Scoring method | 3-judge LLM panel (argo gpt-5 / gemini-2.5-pro / claude-opus-4.7), median + majority verdict |
| Reproducibility blocker (6/22 rule) | {blocker} |
| Reconciled | 2026-06-24 |

_Per-judge panel: {pl}_

_Judges' notes: {row.get('judge_note','')[:600]}_
{MARK_END}

"""

def main():
    apply = "--apply" in sys.argv
    rows = list(csv.DictReader(open(SCORES)))
    changed = 0; skipped = 0
    for row in rows:
        rel = row.get("report_path") or row.get("repo")
        path = ROOT / rel
        if not path.exists():
            print("MISSING:", rel); skipped += 1; continue
        orig = path.read_text(encoding="utf-8", errors="replace")
        # backup once
        bak = path.with_name("REPORT.prereconcile.md")
        if not bak.exists():
            if apply:
                bak.write_text(orig, encoding="utf-8")
        # remove any existing canonical block, then take the body
        body = strip_existing_block(orig)
        h1, body_wo = extract_h1(body)
        block = build_block(row, h1)
        new = block + body_wo
        if apply:
            path.write_text(new, encoding="utf-8")
        changed += 1
    print(f"{'APPLIED' if apply else 'DRY-RUN'}: {changed} reports headered, {skipped} missing")
    if not apply:
        print("Re-run with --apply to write (backs up each as REPORT.prereconcile.md).")

if __name__ == "__main__":
    main()
