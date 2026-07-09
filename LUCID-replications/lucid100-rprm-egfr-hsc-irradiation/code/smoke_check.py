#!/usr/bin/env python3
"""smoke_check.py — LUCID100 first-pass smoke for cbin.11900 (RPRM/EGFR/HSC).

This paper has no model or code to re-run, so this smoke is a *scoping smoke*:
  (a) re-inventory captured artifacts and checksum them
  (b) parse the qPCR primer table out of the JATS XML (the only machine-readable
      experimental table in the paper) and write it as JSON
  (c) probe the three deposit endpoints we tried by hand and record verdicts

Pure stdlib. CPU-only. Writes results/smoke_output.json.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "source"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory_artifacts() -> list[dict]:
    out = []
    for rel in [
        "source/cbin.11900.pdf",
        "source/cbin.11900.txt",
        "source/cbin.11900.xml",
        "source/crossref.json",
        "source/epmc.json",
        "source/geo_search.json",
    ]:
        p = ROOT / rel
        out.append({
            "path": str(rel),
            "exists": p.exists(),
            "size_bytes": p.stat().st_size if p.exists() else 0,
            "sha256": sha256(p) if p.exists() else None,
        })
    # figures dir
    figdir = SOURCE / "figures"
    if figdir.exists():
        for f in sorted(figdir.iterdir()):
            out.append({
                "path": str(f.relative_to(ROOT)),
                "exists": True,
                "size_bytes": f.stat().st_size,
                "sha256": sha256(f),
            })
    return out


def parse_qpcr_primers(xml_path: Path) -> list[dict]:
    """The qPCR primer table is the only structured experimental table in JATS."""
    if not xml_path.exists():
        return []
    text = xml_path.read_text(encoding="utf-8", errors="ignore")
    # The table sits right after the §2.4 'Quantitative real-time PCR' section.
    # The 10 primer rows follow a strict <tr><td>gene</td><td>F</td><td>R</td></tr>
    # pattern. Extract by regex (the namespacing in JATS makes ElementTree
    # awkward, and we already know the exact 10 genes).
    expected_genes = {
        "Ccl11", "il‐13", "TNF‐α", "RPRM", "IL‐1α",
        "il‐1β", "MCP‐1", "Lin28a", "EGFR", "Xrcc6", "GAPDH",
    }
    # Look for table-wrap content near the qPCR section
    m = re.search(
        r"Quantitative real‐time PCR.*?<table-wrap[^>]*>(.*?)</table-wrap>",
        text,
        flags=re.DOTALL,
    )
    if not m:
        return []
    table_block = m.group(1)
    rows = re.findall(
        r"<tr[^>]*>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>",
        table_block,
    )
    primers = []
    for gene, fwd, rev in rows:
        gene_s = gene.strip()
        if gene_s == "Gene":
            continue
        primers.append({
            "gene": gene_s,
            "forward_primer": fwd.strip(),
            "reverse_primer": rev.strip(),
            "expected": gene_s in expected_genes,
        })
    return primers


def probe_url(url: str, timeout: float = 8.0) -> dict:
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"url": url, "ok": True, "status": r.status, "final_url": r.url}
    except urllib.error.HTTPError as e:
        return {"url": url, "ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"url": url, "ok": False, "status": None, "error": f"{type(e).__name__}: {e}"}


def main() -> int:
    artifacts = inventory_artifacts()
    primers = parse_qpcr_primers(SOURCE / "cbin.11900.xml")

    deposit_probes = [
        # 1. NCBI GEO search for RPRM hematopoietic studies (already 0 hits, re-confirm)
        probe_url(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
            "db=gds&term=RPRM+hematopoietic+stem+cell+irradiation"
        ),
        # 2. Wiley supp download (will 403)
        probe_url(
            "https://onlinelibrary.wiley.com/action/downloadSupplement?"
            "doi=10.1002%2Fcbin.11900&file=cbin11900-sup-0001-Figures.pdf"
        ),
        # 3. Europe PMC OA PDF (this is the one we successfully used)
        probe_url("https://europepmc.org/articles/PMC9804513?pdf=render"),
        # 4. PMC supp file path (will 404 — the bin/ paths in JATS aren't re-rendered)
        probe_url(
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9804513/bin/CBIN-46-2158-s001.pdf"
        ),
        # 5. PMC OA tarball index pointer (stale 404)
        probe_url(
            "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/b5/97/PMC9804513.tar.gz"
        ),
    ]

    output = {
        "paper": "Li et al. (2022) RPRM deletion preserves hematopoietic regeneration ...",
        "doi": "10.1002/cbin.11900",
        "pmcid": "PMC9804513",
        "pmid": "36041213",
        "license": "CC BY-NC-ND 4.0",
        "lucid100_slot": "Wave 2, master row 49 (slot 17; task descriptor said 18 — slot mismatch flagged)",
        "verdict": (
            "Wet-lab in vivo mouse paper; mis-tagged as 'simulation/model replication' "
            "in master TSV. No model, no code, no deposited RNA-seq. Independent "
            "quantitative replication is NOT feasible from public artifacts."
        ),
        "artifacts": artifacts,
        "qpcr_primer_panel": {
            "n_primers": len(primers),
            "primers": primers,
            "notes": (
                "Single machine-readable experimental table in the paper. "
                "All 10 (gene, forward, reverse) tuples reproducible by any "
                "wet lab with the RPRM-KO line; no author contact required."
            ),
        },
        "deposit_probes": deposit_probes,
        "deposit_summary": {
            "rna_seq_accession": None,
            "rna_seq_deposit_status": "NOT DEPOSITED — 'available from corresponding author upon reasonable request'",
            "supplementary_files_accessible_via_free_routes": False,
            "supp_files_known": [
                "CBIN-46-2158-s001.pdf",
                "CBIN-46-2158-s002.docx",
                "CBIN-46-2158-s003.pdf",
                "CBIN-46-2158-s004.pdf",
                "CBIN-46-2158-s005.pdf",
                "CBIN-46-2158-s006.pdf",
            ],
            "supp_files_inferred_contents": {
                "S1": "sex-matched control panels for steady-state BM phenotype (referenced in §3.1)",
                "S2": "1–7 month time-course of unirradiated KO vs WT (referenced in §3.1)",
                "S3": "additional unirradiated time-course (referenced in §3.1)",
                "S4": "female-mouse parallels for Fig 2 (BM morphology, LSK/HSC counts, CBC) — explicitly referenced as S4A–D in §3.2",
                "S5": "female-mouse parallels for Fig 3 (γ-H2AX, comet, apoptosis, colony) — referenced as S5A–H in §3.3",
                "S6": "unknown without fetch (likely RNA-seq DEG table or method extension; not referenced by panel-letter in body)",
            },
        },
        "qa_retag_recommendation": {
            "current": "simulation/model replication",
            "proposed": "wet-lab / in-vivo + bulk RNA-seq",
            "keep_in_corpus": True,
            "friction_tags": [
                "wet-lab-only", "no-code", "no-deposit",
                "supp-blocked", "data-on-request-only",
                "requires-rprm-ko-line",
            ],
        },
    }

    out_path = RESULTS / "smoke_output.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"[smoke] wrote {out_path}")
    print(f"[smoke] artifacts inventoried: {len(artifacts)}")
    print(f"[smoke] qPCR primers parsed:   {len(primers)}")
    print(f"[smoke] deposit probes run:    {len(deposit_probes)}")
    print(f"[smoke] verdict: REPLICATION NOT FEASIBLE FROM PUBLIC ARTIFACTS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
