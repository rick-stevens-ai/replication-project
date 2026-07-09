#!/usr/bin/env python3
"""
reconcile_reports.py — Scan every REPORT.md in REPLICATE-PROJECT, extract its
verdict + Coverage/10 + Agreement/10 from whatever format it currently uses,
map verdict synonyms onto the canonical AUDIT_PROTOCOL vocabulary, and emit a
single reconciled master table + an exceptions report.

Canonical schema (AUDIT_PROTOCOL.md):
  verdict ∈ {REPLICATED, PARTIAL, CONTRADICTED, BLOCKED, SPOT-CHECK, NO-GO, FAILED}
  coverage_10 : float 0..10
  agreement_10: float 0..10

This is an EXTRACTION + CLASSIFICATION pass (no LLM judging here — it harvests
the scores already written into each report). Reports with no parseable score or
a non-canonical verdict are flagged for a follow-up judging/normalization pass.
"""
import os, re, csv, json, sys, glob

ROOT = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT")

CANON = {"REPLICATED","PARTIAL","CONTRADICTED","BLOCKED","SPOT-CHECK","NO-GO","FAILED"}

# verdict synonyms -> canonical
SYN = {
    "REPRODUCED": "REPLICATED",
    "STRONG REPLICATION": "REPLICATED",
    "STRONGLY REPLICATED": "REPLICATED",
    "FULLY REPLICATED": "REPLICATED",
    "MODEL-LEVEL REPLICATED": "REPLICATED",
    "REPLICATED (MODEL-LEVEL)": "REPLICATED",
    "PARTIALLY REPLICATED": "PARTIAL",
    "PARTIAL REPLICATION": "PARTIAL",
    "PARTIAL VALIDATION": "PARTIAL",
    "SPOT CHECK": "SPOT-CHECK",
    "SPOTCHECK": "SPOT-CHECK",
    "SPOT-CHECK ONLY": "SPOT-CHECK",
    "NOGO": "NO-GO",
    "NO GO": "NO-GO",
    "DATA-BLOCKED": "BLOCKED",
    "DATA BLOCKED": "BLOCKED",
    "BLOCKED (DATA)": "BLOCKED",
    "REFUTED": "CONTRADICTED",
    "DISAGREES": "CONTRADICTED",
    "FAIL": "FAILED",
}

VERDICT_TOKEN = re.compile(
    r"REPLICATED|REPRODUCED|PARTIALLY REPLICATED|PARTIAL VALIDATION|PARTIAL REPLICATION|"
    r"PARTIAL|CONTRADICTED|REFUTED|BLOCKED|DATA-BLOCKED|SPOT[- ]?CHECK(?:\s+ONLY)?|"
    r"NO[- ]?GO|FAILED|STRONG REPLICATION", re.I)

# Coverage X / 10  and Agreement Y / 10  (tolerant of bold, spaces, fractions)
COV = re.compile(r"coverage[:\s*]*\**\s*([0-9]{1,2}(?:\.[0-9]+)?)\s*/\s*1?0?\b", re.I)
AGR = re.compile(r"agreement[:\s*]*\**\s*([0-9]{1,2}(?:\.[0-9]+)?)\s*/\s*1?0?\b", re.I)
# also catch "Coverage 12 / 13" style (renormalize to /10)
COV_FRAC = re.compile(r"coverage[:\s*]*\**\s*([0-9]{1,2}(?:\.[0-9]+)?)\s*/\s*([0-9]{1,2})\b", re.I)
AGR_FRAC = re.compile(r"agreement[:\s*]*\**\s*([0-9]{1,2}(?:\.[0-9]+)?)\s*/\s*([0-9]{1,2})\b", re.I)

def collection_of(rel):
    top = rel.split(os.sep)[0]
    if top.startswith("LUCID-replications"): return "LUCID-100"
    if top.startswith("LUCID-second100"): return "LUCID-second100"
    if top.startswith("PDE-replications"): return "PDE-100"
    if top.startswith("BVBRC"): return "BVBRC-100"
    return "OTHER"

def paper_id(rel):
    parts = rel.split(os.sep)
    # strip trailing /report/REPORT.md or /REPORT.md
    if parts[-1] == "REPORT.md":
        parts = parts[:-1]
    if parts and parts[-1] == "report":
        parts = parts[:-1]
    return parts[-1] if parts else rel

def canon_verdict(raw):
    if not raw: return None, raw
    u = raw.upper().strip()
    u = re.sub(r"\s+", " ", u)
    if u in CANON: return u, raw
    if u in SYN: return SYN[u], raw
    # token-normalize spot-check / no-go spacing
    u2 = u.replace("SPOT CHECK","SPOT-CHECK").replace("SPOTCHECK","SPOT-CHECK")
    u2 = u2.replace("NO GO","NO-GO").replace("NOGO","NO-GO")
    if u2 in CANON: return u2, raw
    if u2 in SYN: return SYN[u2], raw
    return None, raw  # non-canonical -> flag

def extract_verdict(text):
    """Find the verdict near a Verdict/TL;DR header, else first strong token."""
    # 1) explicit "Overall verdict:" / "Verdict:" lines
    for pat in [r"overall verdict[:\s]+\**([A-Za-z \-]+?)\**\s*(?:\.|\n|<br|\|)",
                r"\bverdict[:\s]+\**([A-Za-z \-]+?)\**\s*(?:\.|\n|<br|\||→)"]:
        m = re.search(pat, text, re.I)
        if m:
            tok = VERDICT_TOKEN.search(m.group(1))
            if tok: return tok.group(0)
            return m.group(1).strip()
    # 2) a "## ... Verdict" header then the next strong token within 400 chars
    m = re.search(r"#+\s*[0-9.]*\s*(?:TL;DR.*?)?verdict", text, re.I)
    if m:
        window = text[m.end(): m.end()+500]
        tok = VERDICT_TOKEN.search(window)
        if tok: return tok.group(0)
    # 3) "X → Y" transition (take final)
    m = re.search(r"(" + VERDICT_TOKEN.pattern + r")\s*→\s*(" + VERDICT_TOKEN.pattern + r")", text, re.I)
    if m: return m.group(2)
    # 4) first strong token anywhere
    tok = VERDICT_TOKEN.search(text)
    return tok.group(0) if tok else None

def extract_scores(text):
    cov = agr = None
    m = COV.search(text)
    if m: cov = float(m.group(1))
    m = AGR.search(text)
    if m: agr = float(m.group(1))
    # fraction renormalization if denominator != 10 and !=0
    if cov is None:
        m = COV_FRAC.search(text)
        if m and m.group(2) not in ("0",):
            cov = round(float(m.group(1))/float(m.group(2))*10, 1)
    if agr is None:
        m = AGR_FRAC.search(text)
        if m and m.group(2) not in ("0",):
            agr = round(float(m.group(1))/float(m.group(2))*10, 1)
    # clamp
    if cov is not None: cov = max(0.0, min(10.0, cov))
    if agr is not None: agr = max(0.0, min(10.0, agr))
    return cov, agr

def main():
    reports = []
    for path in glob.glob(os.path.join(ROOT, "**", "REPORT.md"), recursive=True):
        rel = os.path.relpath(path, ROOT)
        if rel.startswith("repass") or "/repass" in rel:  # scratch dirs
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            reports.append(dict(rel=rel, err=str(e)))
            continue
        rawv = extract_verdict(text)
        cv, rawv2 = canon_verdict(rawv)
        cov, agr = extract_scores(text)
        reports.append(dict(
            paper_id=paper_id(rel),
            collection=collection_of(rel),
            rel=rel,
            verdict_canon=cv or "",
            verdict_raw=(rawv or "").strip(),
            coverage_10=cov if cov is not None else "",
            agreement_10=agr if agr is not None else "",
            flag_noncanon_verdict=(cv is None),
            flag_no_score=(cov is None or agr is None),
        ))

    reports.sort(key=lambda r: (r.get("collection",""), r.get("paper_id","")))

    out_csv = os.path.join(ROOT, "RECONCILED_MASTER_2026-06-24.csv")
    cols = ["collection","paper_id","verdict_canon","coverage_10","agreement_10",
            "verdict_raw","flag_noncanon_verdict","flag_no_score","rel"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in reports:
            w.writerow({k: r.get(k,"") for k in cols})

    # exceptions
    exc = [r for r in reports if r.get("flag_noncanon_verdict") or r.get("flag_no_score")]
    with open(os.path.join(ROOT, "RECONCILE_EXCEPTIONS_2026-06-24.md"), "w") as f:
        f.write("# Reconciliation Exceptions — 2026-06-24\n\n")
        f.write(f"Total reports scanned: **{len(reports)}**\n")
        f.write(f"Needing follow-up (non-canonical verdict OR missing score): **{len(exc)}**\n\n")
        f.write("| collection | paper_id | verdict_raw | cov | agr | issue |\n|---|---|---|---|---|---|\n")
        for r in exc:
            issue = []
            if r.get("flag_noncanon_verdict"): issue.append("verdict")
            if r.get("flag_no_score"): issue.append("score")
            f.write(f"| {r['collection']} | {r['paper_id']} | {r.get('verdict_raw','')} | "
                    f"{r.get('coverage_10','')} | {r.get('agreement_10','')} | {'+'.join(issue)} |\n")

    # summary to stdout
    from collections import Counter
    by_coll = Counter(r["collection"] for r in reports if "collection" in r)
    by_verd = Counter(r["verdict_canon"] or "UNRESOLVED" for r in reports if "collection" in r)
    print(f"Scanned {len(reports)} reports")
    print("By collection:", dict(by_coll))
    print("By canonical verdict:", dict(by_verd))
    print(f"Exceptions (verdict or score): {len(exc)}")
    print(f"Wrote: {out_csv}")
    print(f"Wrote: RECONCILE_EXCEPTIONS_2026-06-24.md")

if __name__ == "__main__":
    main()
