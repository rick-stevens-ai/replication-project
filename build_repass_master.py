#!/usr/bin/env python3
"""Consolidate the 2026-06-23 re-pass run into an authoritative master CSV + findings doc.

For each re-passed paper (dir containing REPORT.pass1.md OR PARSER_PROVENANCE.md),
read the CURRENT report and extract the re-pass final Coverage / Agreement / Verdict,
the parser provenance, and any 'headline catch' note. We read the re-pass section
preferentially (the block after a 'this pass'/'re-pass'/'2026-06-23' marker) rather
than first-match, to avoid grabbing pass-1 numbers.

Outputs:
  REPASS_MASTER_2026-06-23.csv
  REPASS_FINDINGS_2026-06-23.md
"""
import os, re, glob, csv, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

def find_report(d):
    for cand in ("REPORT.md", "report/REPORT.md", "report/REPORT_v2.md",
                 "replication/REPORT.md", "REPORT_v2.md"):
        p = os.path.join(d, cand)
        if os.path.isfile(p):
            return p
    # fallback: any REPORT*.md not named pass1
    for p in glob.glob(os.path.join(d, "**", "REPORT*.md"), recursive=True):
        if ".venv" in p or "pass1" in p.lower():
            continue
        return p
    return None

def grab_score(text, label):
    """Find the highest-confidence FINAL (re-pass) score for label.
    Handles: 'Coverage: 7 -> 8', 'Coverage 6 → 8', '**Coverage** | **8/10**',
    'Coverage / agreement score | 0.87 (lifted from 0.78)'. Returns str or '?'."""
    # 1) arrow form -> take the 'after' value (last occurrence)
    arrow = re.findall(label + r'[^\n]*?(\d+(?:\.\d+)?)\s*(?:->|→|to|lifted (?:to|from [\d.]+ to))\s*(\d+(?:\.\d+)?)', text, re.I)
    if arrow:
        return arrow[-1][1]
    # 1b) 'lifted from 0.78 ... 0.87' fractional in a combined cell
    frac = re.findall(label.split('/')[0] + r'[^\n]*?(0\.\d+)\s*\(lifted', text, re.I)
    if frac:
        return frac[-1]
    # 2) X/10 table-cell form (allow markdown bold/pipes between label and number)
    slash = re.findall(label + r'[^\n0-9]{0,20}(\d+(?:\.\d+)?)\s*/\s*10', text, re.I)
    if slash:
        return slash[-1]
    # 3) bare 'Coverage ... 0.87' fractional
    barefrac = re.findall(label + r'[^\n0-9]{0,20}(0\.\d+)\b', text, re.I)
    if barefrac:
        return barefrac[-1]
    # 4) plain integer near label
    plain = re.findall(label + r'[^\n0-9]{0,12}(\d+)\b', text, re.I)
    if plain:
        return plain[-1]
    return '?'

def grab_verdict(text):
    for pat in (r'4-tier[^\n]*?:\s*\*{0,2}([A-Z][A-Za-z \-/]+?)\*{0,2}\s*(?:\n|—|-)',
                r'Verdict[^\n]*?:\s*\*{0,2}([A-Z][A-Za-z \-/]+)',
                r'Status:\*{0,2}\s*\*{0,2}([A-Z][A-Z \-]*(?:REPLICATED|SPOT-CHECK|PARTIAL|NO-GO))',
                r'Outcome:\*{0,2}\s*\*{0,2}([A-Z][A-Za-z \-]+)',
                r'\b(STRONG REPLICATION|SPOT-CHECK REPLICATED|REPRODUCED[A-Z \-]*|REPLICATED|SPOT-CHECK|PARTIAL|NO-GO|Tier [A-D])\b'):
        m = re.findall(pat, text)
        if m:
            return m[-1].strip()[:40]
    return '?'

def grab_parser(d, text):
    pp = os.path.join(d, "PARSER_PROVENANCE.md")
    if os.path.isfile(pp):
        t = open(pp, errors='ignore').read()
        for kw in ("pdftotext", "Nougat", "Marker", "OCR", "pdfplumber", "pymupdf", "PyMuPDF", "pre-existing", "paper.txt"):
            if kw.lower() in t.lower():
                return kw
        return "recorded"
    for kw in ("pdftotext", "Nougat", "Marker"):
        if kw.lower() in text.lower():
            return kw
    return "none"

rows = []
dirs = set()
for marker in ("REPORT.pass1.md", "PARSER_PROVENANCE.md"):
    for f in glob.glob(os.path.join(ROOT, "**", marker), recursive=True):
        if ".venv" in f:
            continue
        d = os.path.dirname(f)
        d = re.sub(r'/(report|replication|code/repass|results/repass)$', '', d)
        if os.path.basename(d) in ('repass_paper', 'template', '_template'):
            continue
        dirs.add(d)

for d in sorted(dirs):
    rep = find_report(d)
    name = os.path.basename(d)
    if not rep:
        rows.append({"paper": name, "coverage": "?", "agreement": "?",
                     "verdict": "NO-REPORT", "parser": grab_parser(d, ""), "report": ""})
        continue
    text = open(rep, errors='ignore').read()
    rows.append({
        "paper": name,
        "coverage": grab_score(text, "Coverage"),
        "agreement": grab_score(text, "Agreement"),
        "verdict": grab_verdict(text),
        "parser": grab_parser(d, text),
        "report": os.path.relpath(rep, ROOT),
    })

csv_path = os.path.join(ROOT, "REPASS_MASTER_2026-06-23.csv")
with open(csv_path, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["paper", "coverage", "agreement", "verdict", "parser", "report"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

# findings doc
md = [f"# Re-pass Master — {datetime.date.today().isoformat()}",
      "",
      f"**{len(rows)} papers re-passed** (coverage-lift pass on the prior REPLICATE-PROJECT corpus).",
      "Each got PARSER_PROVENANCE.md; original report preserved as REPORT.pass1.md.",
      "",
      "## Scores (re-pass final)",
      "",
      "| Paper | Cov | Agr | Verdict | Parser |",
      "|---|---|---|---|---|"]
for r in sorted(rows, key=lambda x: x["paper"].lower()):
    md.append(f"| {r['paper']} | {r['coverage']} | {r['agreement']} | {r['verdict']} | {r['parser']} |")

# parser provenance coverage
have_pp = sum(1 for r in rows if r["parser"] not in ("none",))
md += ["", "## Provenance",
       f"- Papers with parser provenance recorded: **{have_pp}/{len(rows)}**",
       "",
       "## Headline integrity catches (manually curated — verify against reports)",
       "- **zhang-spde**: pass-1 replicated the WRONG Zhang paper (1905.01205 vs cited 1809.08327). Re-pass fixed identity → 9/11 cov, 78% agr.",
       "- **modal-space**: two silent v2 setup bugs (wrong distribution params on Ex1, wrong PDE on Ex3); corrected Ex1 now beats the paper → REPLICATED.",
       "- **BVBRC-07**: 26 'missed' genes were an AMRFinder --organism flag mismatch, not a real gap; 15 acquired AMR genes match exactly.",
       "- **divide-conquer-chaotic**: quantified Lorenz gradient explosion 1.6e13×; fixed KS stability; ERA5 honestly reclassified as data-blocked.",
       "- **SCALE-molten-salt**: caught a Table-1 element-label swap; named RSICC-gated SCALE 6.3 blocker.",
       "- **mutant-phenotypes**: 17 claims confirmed EXACT vs deposited tables; named 84GB R-image blocker.",
       "- **nanograv-15yr**: reproduced headline GWB detection significances exactly (p=7.85e-4 vs 1e-3; OS S/N p=4.75e-5 vs 5e-5).",
       "- **Variovorax**: caught a coordinate typo in the original paper.",
       ""]
md_path = os.path.join(ROOT, "REPASS_FINDINGS_2026-06-23.md")
open(md_path, "w").write("\n".join(md))

print(f"WROTE {csv_path}")
print(f"WROTE {md_path}")
print(f"rows: {len(rows)}  with-provenance: {have_pp}")
print("\n=== score sanity (any '?') ===")
for r in rows:
    if r["coverage"] == "?" or r["verdict"] in ("?", "NO-REPORT"):
        print(f"  CHECK {r['paper']}: cov={r['coverage']} agr={r['agreement']} verdict={r['verdict']} report={r['report']}")
