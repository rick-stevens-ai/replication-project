#!/usr/bin/env python3
"""
04_bvbrc_metadata.py — Re-pass:
  Pull genome-level metadata from BV-BRC for genome 1795631.3 to ground
  the paper's implicit claims that PAMC28711 is:
    - cold-adapted lichen-associated Antarctic bacterium (Background §1)
    - a complete genome with one chromosome
    - originally described as opine-utilizing (Ref [3] Han et al. 2016)
  and the explicit numeric claim:
    - "NZ_CP014517.1" + complete genome.

Output: results/repass/bvbrc_metadata.json
"""
from __future__ import annotations

import csv
import io
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "repass" / "bvbrc_metadata.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

FIELDS = [
    "genome_name", "host_name", "isolation_source", "isolation_country",
    "isolation_site", "geographic_location", "collection_date",
    "gc_content", "genome_length", "patric_cds", "refseq_cds",
    "strain", "segments", "plasmids", "chromosomes",
    "completion_date", "genome_status", "completeness",
    "rrna", "trna", "ncrna", "biosample_accession", "assembly_accession",
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/repass"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> None:
    select = "select(" + ",".join(FIELDS) + ")"
    url = (
        "https://www.bv-brc.org/api/genome/?genome_id=1795631.3&"
        + select + "&http_accept=text/csv"
    )
    raw = fetch(url)
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows:
        raise SystemExit(f"No rows from BV-BRC URL {url}\n{raw}")
    g = rows[0]

    out = {
        "endpoint": "https://www.bv-brc.org/api/genome",
        "genome_id": "1795631.3",
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "metadata": g,
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"Wrote {OUT}")
    for k, v in g.items():
        print(f"  {k:24s} = {v!r}")


if __name__ == "__main__":
    main()
