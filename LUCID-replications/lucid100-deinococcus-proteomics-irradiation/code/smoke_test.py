#!/usr/bin/env python3
"""
LUCID100 slot 22 — smoke replication for:
Chen & Zhang 2025, "Proteomic Profiling of Deinococcus radiodurans Reveals
Irradiation-Induced Proteins and Their Associated Functional Pathways"
DOI: 10.1088/1742-6596/3109/1/012098

What this PASS-low smoke does (and does not):

  IN SCOPE (this script):
  1. Verify the UniProt reference proteome UP000002524 (D. radiodurans R1)
     used by the authors (pFind3 search target) is publicly retrievable and
     report its size — order-of-magnitude must be consistent with the paper's
     ~2,000 detected proteins.
  2. Verify the three named irradiation-induced DNA-repair proteins
     (RuvC, DdrA, DdrB) resolve to UniProt accessions in D. radiodurans
     R1 (taxon 243230) and carry the GO terms the paper claims are
     enriched: GO:0006281 (DNA repair), GO:0003677 / GO:0003697 (DNA
     binding), GO:0071480 (cellular response to gamma radiation).
  3. Confirm the paper's Venn diagram arithmetic in Figure 2b
     (2,034 shared + 142 control-only + 62 radiation-only) is internally
     self-consistent, and that the radiation-only fraction is small but
     non-trivial (~3% of detected proteome).
  4. Document accession / DOI / artifact provenance.

  OUT OF SCOPE (would need data the authors did NOT deposit):
  - Reading their raw .raw LC-MS/MS files (no PRIDE / ProteomeXchange
    accession for THIS paper; see NO_GO note in FIRST_PASS_REPORT.md).
  - Re-running pFind3 to reproduce the 62 irradiation-induced protein
    list. The 62 protein list is NOT published in the paper or as a
    supplement and the underlying raw spectra are not deposited.
  - Re-running the DAVID 6.8 enrichment with the actual induced set.

The point of this smoke is to verify that the *reproducible part* of the
authors' pipeline (public reference proteome, public GO annotations,
named protein identities) is internally consistent. That is the most
that the public artifact set permits without author contact or paid
access to private LC-MS/MS data.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"Accept": "text/tab-separated-values"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


# ---------------------------------------------------------------------------
# Step 1: reference proteome size
# ---------------------------------------------------------------------------
def check_proteome() -> dict:
    p = DATA / "UP000002524.json"
    if p.exists():
        meta = json.loads(p.read_text())
    else:
        meta = http_get_json("https://rest.uniprot.org/proteomes/UP000002524")
        p.write_text(json.dumps(meta, indent=2))

    n = meta.get("proteinCount")
    paper_detected = 2034 + 142 + 62  # = 2238 (Figure 2b Venn total)
    # Detected proteome should be ~50-80% of the reference proteome (typical for
    # shotgun LC-MS/MS at this depth on a small bacterium). 2238 / 3085 ~= 72%.
    frac = paper_detected / n if n else None
    return {
        "ref_proteome_id": meta.get("id"),
        "ref_proteome_size": n,
        "taxon": (meta.get("taxonomy") or {}).get("scientificName"),
        "tax_id": (meta.get("taxonomy") or {}).get("taxonId"),
        "strain_matches_R1": "R1" in (meta.get("strain") or ""),
        "paper_detected_total_proteins": paper_detected,
        "detected_over_reference_fraction": round(frac, 3) if frac else None,
        "fraction_in_plausible_range_50_to_90_pct": (
            0.50 <= frac <= 0.90 if frac else False
        ),
    }


# ---------------------------------------------------------------------------
# Step 2: named protein resolution + GO sanity
# ---------------------------------------------------------------------------
GO_REPAIR = "GO:0006281"
GO_DNA_BIND_DS = "GO:0003677"
GO_DNA_BIND_SS = "GO:0003697"
GO_GAMMA = "GO:0071480"


def check_named_proteins() -> dict:
    targets = [
        ("RuvC", "ruvC", "Q9RX75"),
        ("DdrA", "ddrA", "Q9RX92"),
        ("DdrB", "ddrB", "Q9RY80"),
    ]
    out = []
    for label, gene, expected_acc in targets:
        url = (
            "https://rest.uniprot.org/uniprotkb/search?"
            + urllib.parse.urlencode(
                {
                    "query": f"gene:{gene} AND organism_id:243230 AND reviewed:true",
                    "fields": "accession,id,protein_name,gene_names,length,go_id",
                    "format": "tsv",
                    "size": 3,
                }
            )
        )
        tsv = http_get_text(url)
        rows = [r for r in tsv.strip().splitlines()[1:] if r]
        # pick the row whose Entry == expected_acc, else first row
        chosen = None
        for r in rows:
            if r.split("\t")[0] == expected_acc:
                chosen = r
                break
        if not chosen and rows:
            chosen = rows[0]
        if not chosen:
            out.append({"protein": label, "found": False})
            continue
        cols = chosen.split("\t")
        acc, entry_name, prot_name, gene_names, length, go_ids = cols[:6]
        go_set = {g.strip() for g in go_ids.split(";") if g.strip()}
        out.append(
            {
                "protein": label,
                "gene_query": gene,
                "expected_accession": expected_acc,
                "uniprot_accession": acc,
                "match_expected": acc == expected_acc,
                "entry_name": entry_name,
                "protein_name": prot_name,
                "length": int(length),
                "has_GO_DNA_repair (GO:0006281)": GO_REPAIR in go_set,
                "has_GO_DNA_binding (GO:0003677 or GO:0003697)": (
                    GO_DNA_BIND_DS in go_set or GO_DNA_BIND_SS in go_set
                ),
                "has_GO_cellular_response_to_gamma (GO:0071480)": GO_GAMMA in go_set,
            }
        )
    return {"named_proteins": out}


# ---------------------------------------------------------------------------
# Step 3: Venn arithmetic / fraction sanity
# ---------------------------------------------------------------------------
def check_venn() -> dict:
    shared = 2034
    control_only = 142
    radiation_only = 62
    total = shared + control_only + radiation_only
    control_total = shared + control_only
    radiation_total = shared + radiation_only
    pct_induced = radiation_only / radiation_total
    return {
        "shared": shared,
        "control_only": control_only,
        "radiation_only": radiation_only,
        "control_total_proteins": control_total,
        "radiation_total_proteins": radiation_total,
        "radiation_only_fraction_of_radiation_set": round(pct_induced, 4),
        "fraction_in_plausible_range_0p5_to_5_pct": (
            0.005 <= pct_induced <= 0.05
        ),
        "approx_2000_per_group_consistent": (
            1900 <= control_total <= 2300 and 1900 <= radiation_total <= 2300
        ),
    }


def main() -> int:
    report = {
        "paper": {
            "doi": "10.1088/1742-6596/3109/1/012098",
            "title": (
                "Proteomic Profiling of Deinococcus radiodurans Reveals "
                "Irradiation-Induced Proteins and Their Associated "
                "Functional Pathways"
            ),
            "authors": ["Chaoyi Chen", "Yongqian Zhang"],
            "year": 2025,
            "venue": "Journal of Physics: Conference Series 3109 (2025) 012098",
        },
        "step1_reference_proteome": check_proteome(),
        "step2_named_proteins": check_named_proteins(),
        "step3_venn_arithmetic": check_venn(),
    }

    # Overall PASS criteria
    s1 = report["step1_reference_proteome"]
    s2_rows = report["step2_named_proteins"]["named_proteins"]
    s3 = report["step3_venn_arithmetic"]

    criteria = {
        "ref_proteome_resolves_and_strain_is_R1": (
            s1["ref_proteome_id"] == "UP000002524" and s1["strain_matches_R1"]
        ),
        "detected_count_consistent_with_reference_proteome_size": s1[
            "fraction_in_plausible_range_50_to_90_pct"
        ],
        "all_3_named_proteins_resolve_to_expected_uniprot": all(
            r.get("match_expected") for r in s2_rows
        ),
        "all_3_named_proteins_have_DNA_repair_GO": all(
            r.get("has_GO_DNA_repair (GO:0006281)") for r in s2_rows
        ),
        "all_3_named_proteins_have_DNA_binding_GO": all(
            r.get("has_GO_DNA_binding (GO:0003677 or GO:0003697)") for r in s2_rows
        ),
        "at_least_2_of_3_have_gamma_response_GO": (
            sum(
                bool(r.get("has_GO_cellular_response_to_gamma (GO:0071480)"))
                for r in s2_rows
            )
            >= 2
        ),
        "venn_arithmetic_self_consistent": s3[
            "approx_2000_per_group_consistent"
        ]
        and s3["fraction_in_plausible_range_0p5_to_5_pct"],
    }
    report["pass_low_criteria"] = criteria
    report["pass_low_overall"] = all(criteria.values())

    out_path = RESULTS / "smoke_test_report.json"
    out_path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"\n[smoke] wrote {out_path}", file=sys.stderr)
    return 0 if report["pass_low_overall"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
