#!/usr/bin/env python3
"""
03_kegg_crosscheck.py — Re-pass:
  - Confirm KEGG organism code `vaa` resolves to Variovorax sp. PAMC 28711.
  - Confirm map vaa00500 exists and is named "Starch and sucrose metabolism".
  - Map all paper-EC numbers to their KEGG KO and check
    `link/vaa/ko:KXXXXX` to see which genes KEGG assigns in this organism.
  - Independently re-test TreX (K02438 / K01214) which was NOT checked in
    pass-1.

Output: results/repass/kegg_crosscheck.json
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "repass" / "kegg_crosscheck.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

EC_TO_KO = {
    "OtsA":     ("2.4.1.15",  ["K00697"]),
    "OtsB":     ("3.1.3.12",  ["K01087"]),
    "TreY":     ("5.4.99.15", ["K06044"]),  # paper says X for vaa
    "TreZ":     ("3.2.1.141", ["K01236"]),
    "TreS":     ("5.4.99.16", ["K05343"]),
    "TreF":     ("3.2.1.28",  ["K01194"]),
    "TreP":     ("2.4.1.64",  ["K00691", "K05349"]),
    "TreT":     ("2.4.1.245", ["K13057"]),
    "TreX":     ("3.2.1.68",  ["K02438", "K01214"]),  # NEW
    # Glycogen biosynthesis
    "GlgC":     ("2.7.7.27",  ["K00975"]),
    "GlgA":     ("2.4.1.21",  ["K00703"]),
    "GlgB":     ("2.4.1.18",  ["K00700"]),
    "GlgP":     ("2.4.1.1",   ["K00688"]),
    "MalQ":     ("2.4.1.25",  ["K00705"]),
}


def kget(path: str) -> str:
    url = f"https://rest.kegg.jp/{path}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> None:
    out: dict = {"endpoint": "https://rest.kegg.jp", "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}

    # 1. Organism code resolves (`list/organism` was deprecated; use info/vaa)
    try:
        out["organism_vaa_info"] = kget("info/vaa").strip().splitlines()[:10]
    except Exception as e:
        out["organism_vaa_info"] = f"ERROR: {e}"

    # 2. Pathway map vaa00500
    try:
        raw = kget("get/vaa00500")
        first_lines = "\n".join(raw.splitlines()[:6])
        out["vaa00500_header"] = first_lines
    except Exception as e:
        out["vaa00500_header"] = f"ERROR: {e}"

    # 3. List number of pathway maps for vaa
    try:
        raw = kget("list/pathway/vaa")
        out["n_vaa_pathway_maps"] = len([ln for ln in raw.splitlines() if ln.strip()])
    except Exception as e:
        out["n_vaa_pathway_maps"] = f"ERROR: {e}"

    # 4. List number of modules for vaa
    try:
        raw = kget("list/module/vaa")
        out["n_vaa_modules"] = len([ln for ln in raw.splitlines() if ln.strip()])
    except Exception as e:
        out["n_vaa_modules"] = f"ERROR: {e}"

    # 5. Total genes in vaa
    try:
        raw = kget("list/vaa")
        out["n_vaa_genes"] = len([ln for ln in raw.splitlines() if ln.strip()])
    except Exception as e:
        out["n_vaa_genes"] = f"ERROR: {e}"

    # 6. Per-KO genes assigned in vaa
    ko_links = {}
    for name, (ec, kos) in EC_TO_KO.items():
        ko_links[name] = {"EC": ec, "KOs": kos, "vaa_genes_per_KO": {}}
        for ko in kos:
            try:
                raw = kget(f"link/vaa/ko:{ko}")
                genes = []
                for ln in raw.splitlines():
                    ln = ln.strip()
                    if not ln:
                        continue
                    parts = ln.split("\t")
                    if len(parts) == 2:
                        # KEGG returns "ko:KXXXXX\tvaa:GENEID"
                        genes.append(parts[1])
                ko_links[name]["vaa_genes_per_KO"][ko] = genes
            except Exception as e:
                ko_links[name]["vaa_genes_per_KO"][ko] = f"ERROR: {e}"
            time.sleep(0.1)  # be polite

    out["enzyme_KO_to_vaa_gene_links"] = ko_links

    OUT.write_text(json.dumps(out, indent=2))
    print(f"Wrote {OUT}")
    print("Organism info(vaa):")
    print("  " + "\n  ".join(out.get("organism_vaa_info", [])) if isinstance(out.get("organism_vaa_info"), list) else f"  {out['organism_vaa_info']}")
    print(f"vaa pathway maps: {out['n_vaa_pathway_maps']}")
    print(f"vaa modules: {out['n_vaa_modules']}")
    print(f"vaa total genes: {out['n_vaa_genes']}")
    print("--- vaa00500 header ---")
    print(out["vaa00500_header"])
    print("--- per-enzyme KO links in vaa ---")
    for name, info in ko_links.items():
        ec = info["EC"]
        per_ko = info["vaa_genes_per_KO"]
        summary = "; ".join(
            f"{ko}={genes if isinstance(genes,str) else (','.join(genes) or 'NONE')}"
            for ko, genes in per_ko.items()
        )
        print(f"  {name:6s} EC {ec:<10s}  {summary}")


if __name__ == "__main__":
    main()
