#!/usr/bin/env python3
"""Harvest final re-pass Coverage/Agreement + verdict from every re-passed REPORT.
A dir counts as re-passed if it has REPORT.pass1.md (preserved original) OR PARSER_PROVENANCE.md.
We read the CURRENT REPORT.md (the re-pass) and pull the LAST/explicit re-pass cov/agr/verdict.
"""
import os, re, glob, json, csv, sys

ROOT = "/Users/stevens/Dropbox/REPLICATE-PROJECT"
os.chdir(ROOT)

def find_report(d):
    for c in ("REPORT.md", "report/REPORT.md", "replication/REPORT.md"):
        p = os.path.join(d, c)
        if os.path.isfile(p):
            return p
    # fallback: any REPORT*.md not pass1
    for p in glob.glob(os.path.join(d, "**/REPORT*.md"), recursive=True):
        if ".venv" in p or "pass1" in p.lower():
            continue
        return p
    return None

def extract(text):
    """Return (cov, agr, verdict). Prefer explicit re-pass lines; tolerate 'X -> Y' and 'X/10'."""
    cov = agr = None; verdict = None
    # Coverage: capture a number 0-10; if 'a -> b' or 'a → b', take b (the new value)
    def grab(label):
        # look for 'Label ... N' or 'Label ... a -> b'
        pats = [
            rf"{label}\s*[:=]?\s*\**\s*(\d+)\s*(?:->|→|to)\s*\**(\d+)",   # a -> b
            rf"{label}\s*[:=]?\s*\**\s*(\d+)\s*/\s*10",                    # b/10
            rf"{label}\s*[:=]?\s*\**\s*(\d+)\b",                          # b
        ]
        for pat in pats:
            m = re.search(pat, text, re.I)
            if m:
                return int(m.group(m.lastindex))
        return None
    cov = grab("Coverage")
    agr = grab("Agreement")
    # verdict: 4-tier keywords
    vm = re.search(r"\b(STRONG REPLICATION|REPLICATED[A-Za-z\- ]*|REPRODUCED[A-Za-z\- ]*|PARTIAL[A-Za-z\- ]*|SPOT-CHECK[A-Za-z\- ]*|NO-GO|Tier [ABCD])\b", text)
    if vm:
        verdict = vm.group(1).strip()[:40]
    return cov, agr, verdict

rows = []
seen = set()
markers = set()
for m in glob.glob("**/REPORT.pass1.md", recursive=True) + glob.glob("**/PARSER_PROVENANCE.md", recursive=True):
    if ".venv" in m: continue
    d = os.path.dirname(m)
    d = re.sub(r"/(report|replication)$", "", d)
    markers.add(d)

for d in sorted(markers):
    name = os.path.basename(d)
    if name in seen: continue
    seen.add(name)
    rp = find_report(d)
    if not rp:
        rows.append((name, "?", "?", "NO-REPORT")); continue
    txt = open(rp, errors="ignore").read()
    # restrict to the re-pass section if present (after a 're-pass' / 'pass 2' / 'Executive verdict' heading)
    cov, agr, verdict = extract(txt)
    rows.append((name, cov if cov is not None else "?", agr if agr is not None else "?", verdict or "?"))

print(f"=== Re-passed papers with extracted final scores: {len(rows)} ===\n")
for name, cov, agr, verdict in rows:
    print(f"  cov={str(cov):>2}  agr={str(agr):>2}  {verdict:<32}  {name[:60]}")

# write CSV
out = os.path.join(ROOT, "REPASS_FINAL_SCORES_2026-06-23.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["paper","coverage","agreement","verdict"])
    for r in rows: w.writerow(r)
print(f"\nWrote {out}")
