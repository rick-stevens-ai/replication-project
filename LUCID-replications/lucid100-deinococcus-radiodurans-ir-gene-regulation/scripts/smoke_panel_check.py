#!/usr/bin/env python3
"""
LUCID100 smoke replication for Wang et al. 2019 (Gene, DOI 10.1016/j.gene.2019.144008)
"Gene regulation for the extreme resistance to ionizing radiation of Deinococcus radiodurans"

Source paper type: REVIEW (no primary data, no supplements, paywalled Elsevier).
Replication strategy: panel cross-check against public IR-responsive D. deserti
transcriptome (GSE95658; closest available IrrE/DdrO RDR-regulon dataset) and
sRNA dataset (GSE64952; D. radiodurans R1, sham vs 15 kGy).

Smoke checks (4):
  1. GSE95658 RD42 (DeltaIrrE) diff-exp table loads with expected schema/row count
  2. GSE95658 RD62 (DeltaDdrO) diff-exp table loads with expected schema/row count
  3. Wang 2019's named regulator panel (IrrE, DdrO, DdrA-D, PprA, RecA, RecFOQR,
     UvrABCD, GyrA, PolA, SSB) is detectable in the GSE95658 D. deserti orthologs
  4. GSE64952 sRNA table loads and shows differential sham vs 15 kGy IR counts
     for sRNAs the review highlights (Dsr/PprS family)
"""
from __future__ import annotations
import csv, gzip, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ART = HERE / "artifacts"

# Panel of regulators / DDR/RDR-regulon members named in Wang 2019 review
WANG2019_PANEL = {
    # Master regulators / regulon controllers
    "irrE", "ddrO", "ddrI",
    # PprI / PprM / PprA axis (PprI is IrrE; review uses both names)
    "pprI", "pprM", "pprA",
    # Ddr radiation-induced family (named in review)
    "ddrA", "ddrB", "ddrC", "ddrD",
    # Core DNA repair (UvrABC NER, RecA-family HR, polA, gyrA, ssb)
    "recA", "recF", "recO", "recQ", "recR", "recX",
    "uvrA", "uvrB", "uvrC", "uvrD",
    "gyrA", "polA", "ssb",
}

def check_diffexp(path: Path, label: str) -> dict:
    """Load a GSE95658 differential expression table and return summary stats."""
    res = {"label": label, "path": str(path), "ok": False}
    if not path.exists():
        res["error"] = "missing file"
        return res
    rows = 0
    hits = {}
    with path.open() as fh:
        # First line is condition label, second is header
        _condition = fh.readline().rstrip("\n")
        header_line = fh.readline().rstrip("\n").split("\t")
        # Expected columns from inspection: Label, Type, Name, Product, Begin, End, Length, Frame, foldChange, log2FoldChange, pval, padj
        try:
            i_name = header_line.index("Name")
            i_log2 = header_line.index("log2FoldChange")
            i_padj = header_line.index("padj")
        except ValueError as exc:
            res["error"] = f"header missing column: {exc}"
            return res
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= max(i_name, i_log2, i_padj):
                continue
            rows += 1
            gene = parts[i_name].strip()
            # Normalize both sides to lowercase for robust comparison
            gene_key = gene.lower()
            panel_lc = {g.lower() for g in WANG2019_PANEL}
            if gene and gene != "NULL" and gene_key in panel_lc:
                # keep most extreme |log2FC| per gene name (paralogs on plasmids)
                try:
                    log2 = float(parts[i_log2])
                except ValueError:
                    log2 = float("nan")
                try:
                    padj = float(parts[i_padj])
                except ValueError:
                    padj = float("nan")
                prev = hits.get(gene_key)
                if prev is None or abs(log2) > abs(prev["log2FC"]):
                    hits[gene_key] = {"locus": parts[0], "log2FC": log2, "padj": padj, "gene_name_in_file": gene}
    res["row_count"] = rows
    res["panel_total"] = len(WANG2019_PANEL)
    res["panel_hits"] = len(hits)
    res["panel_hit_genes"] = sorted(hits.keys())
    res["panel_missing"] = sorted({g.lower() for g in WANG2019_PANEL} - set(hits.keys()))
    res["panel_detail"] = hits
    res["ok"] = rows > 3000 and len(hits) >= 15
    return res

def check_sRNA(path: Path) -> dict:
    """Load GSE64952 sRNA processed table and verify sham vs 15 kGy structure."""
    res = {"label": "GSE64952_sRNA", "path": str(path), "ok": False}
    if not path.exists():
        res["error"] = "missing file"
        return res
    rows = []
    with path.open() as fh:
        header = fh.readline().rstrip("\n").split("\t")
        # Strip trailing whitespace from column names (header has weird spacing)
        header = [h.strip() for h in header]
        idx_name = header.index("Name of small RNA")
        idx_sham_raw = header.index("Read counts under sham irradiation")
        # Use loose match for 15kGy raw col
        idx_ir_raw = next(i for i,h in enumerate(header) if "15kGy" in h and "Read count" in h and "Normalized" not in h)
        idx_sham_norm = next(i for i,h in enumerate(header) if "sham" in h and "Normalized" in h)
        idx_ir_norm   = next(i for i,h in enumerate(header) if "15kGy" in h and "Normalized" in h)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= idx_ir_norm: continue
            try:
                rows.append({
                    "name": parts[idx_name].strip(),
                    "sham_raw": int(parts[idx_sham_raw]),
                    "ir_raw": int(parts[idx_ir_raw]),
                    "sham_norm": float(parts[idx_sham_norm]),
                    "ir_norm": float(parts[idx_ir_norm]),
                })
            except (ValueError, IndexError):
                continue
    res["row_count"] = len(rows)
    # Wang 2019 sRNA / Dsr family (Dsr1, Dsr2=PprS, Dsr3, etc.); confirm Dsr2 present
    by_name = {r["name"]: r for r in rows}
    dsr2 = by_name.get("Dsr2")
    res["dsr2_present"] = dsr2 is not None
    res["dsr2_record"] = dsr2
    # Compute fold change (ir_norm / sham_norm) for Dsr family
    dsr_changes = {}
    for r in rows:
        if r["name"].startswith("Dsr"):
            sham, ir = r["sham_norm"], r["ir_norm"]
            fc = (ir / sham) if sham > 0 else None
            dsr_changes[r["name"]] = {"sham_norm": sham, "ir_norm": ir, "fc_ir_vs_sham": fc}
    res["dsr_family_changes"] = dsr_changes
    # Count Dsrs with >=2x change either direction (review describes IR-responsive sRNAs)
    responsive = [n for n,v in dsr_changes.items() if v["fc_ir_vs_sham"] is not None
                  and (v["fc_ir_vs_sham"] >= 2 or v["fc_ir_vs_sham"] <= 0.5)]
    res["dsr_2x_responsive"] = responsive
    res["ok"] = (len(rows) >= 25 and dsr2 is not None and len(responsive) >= 3)
    return res

def main() -> int:
    report = {"paper_doi": "10.1016/j.gene.2019.144008",
              "paper_type": "review",
              "datasets_used": ["GSE95658 (D. deserti, IrrE/DdrO regulon)",
                                "GSE64952 (D. radiodurans R1, sham vs 15 kGy sRNAs)"],
              "checks": {}}

    report["checks"]["c1_GSE95658_RD42_irrE"] = check_diffexp(
        ART / "GSE95658_diffexp_RD42.txt", "RD42 (DeltaIrrE) vs WT after IR")
    report["checks"]["c2_GSE95658_RD62_ddrO"] = check_diffexp(
        ART / "GSE95658_diffexp_RD62.txt", "RD62 (DeltaDdrO) vs WT after IR")
    report["checks"]["c3_panel_overlap"] = {
        "wang2019_panel_size": len(WANG2019_PANEL),
        "panel_genes": sorted(WANG2019_PANEL),
        "RD42_panel_hits": report["checks"]["c1_GSE95658_RD42_irrE"].get("panel_hits", 0),
        "RD42_panel_hit_genes": report["checks"]["c1_GSE95658_RD42_irrE"].get("panel_hit_genes", []),
        "RD42_panel_missing": report["checks"]["c1_GSE95658_RD42_irrE"].get("panel_missing", []),
        "ok": report["checks"]["c1_GSE95658_RD42_irrE"].get("panel_hits", 0) >= 15,
    }
    report["checks"]["c4_GSE64952_sRNA"] = check_sRNA(ART / "GSE64952_processed.txt")

    n_ok = sum(1 for c in report["checks"].values() if c.get("ok"))
    n_total = len(report["checks"])
    report["summary"] = {"checks_passed": n_ok, "checks_total": n_total,
                         "verdict": "PASS-low" if n_ok == n_total else
                                    ("PARTIAL" if n_ok >= n_total/2 else "FAIL")}

    out = ART / "smoke_panel_results.json"
    out.write_text(json.dumps(report, indent=2, default=str))

    # Human-readable summary
    print(f"=== Smoke replication for DOI {report['paper_doi']} ===")
    print(f"Paper type: {report['paper_type']} (no primary data, no supplements)")
    print(f"Surrogate datasets: {', '.join(report['datasets_used'])}")
    print()
    for name, chk in report["checks"].items():
        flag = "PASS" if chk.get("ok") else "FAIL"
        extra = ""
        if "row_count" in chk:
            extra += f" rows={chk['row_count']}"
        if "panel_hits" in chk:
            extra += f" panel_hits={chk['panel_hits']}/{chk.get('panel_total','?')}"
        if name == "c4_GSE64952_sRNA":
            extra += f" Dsr2={chk.get('dsr2_present')} responsive_Dsrs={len(chk.get('dsr_2x_responsive',[]))}"
        print(f"  [{flag}] {name}: {chk.get('label','')}{extra}")
    print()
    print(f"OVERALL: {n_ok}/{n_total} -> {report['summary']['verdict']}")
    print(f"Detailed JSON: {out}")
    return 0 if n_ok == n_total else 1

if __name__ == "__main__":
    sys.exit(main())
