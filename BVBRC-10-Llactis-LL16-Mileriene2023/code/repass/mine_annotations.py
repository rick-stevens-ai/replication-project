#!/usr/bin/env python3
"""
Re-pass annotation miner for LL16 Mileriene 2023 replication.
Mines the PGAP GFF3 for previously-skipped or partial claim categories:
  - C14: Adhesion genes (enolase, fibronectin-binding, EPS, TPI, sortase A, ATP synthase)
  - C15: Acid/bile tolerance (ATP synthase, LDH, GlcN-6-P deaminase, CTP synthase, CFA synthase)
  - C16: L- AND D-lactate dehydrogenases
  - C17: Stress (GroES, GroEL, CSP, DnaJ, DnaK, GrpE)
  - C18: Vitamins (thiamine B1, riboflavin B2, pyridoxin B6, biotin B7, folate B9)
  - C20: Tryptophan biosynthesis (trp operon)
  - C22: IS family counts (IS6 ISS1/ISLla, by family)
  - C27: Enzymes (alpha-amylase, lipases, serine protease, DegP/HtrA, xylanase)
  - C28: Lactose utilization operon (lacR-ABCDFEGX)
Writes results/repass/annotation_mining.json incrementally.
"""
import json
import re
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-10-Llactis-LL16-Mileriene2023")
GFF = ROOT / "data/annotated/ncbi_dataset/data/GCF_029912225.1/genomic.gff"
OUT = ROOT / "results/repass/annotation_mining.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


def parse_gff_features():
    """Yield (seqid, type, start, end, strand, attrs_dict) for every feature row."""
    with open(GFF) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 9:
                continue
            seqid, src, ftype, start, end, score, strand, phase, attrs = cols
            adict = {}
            for kv in attrs.split(";"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    adict[k] = v
            yield seqid, ftype, int(start), int(end), strand, adict


def collect_products():
    rows = []
    for seqid, ftype, start, end, strand, attrs in parse_gff_features():
        if ftype not in ("CDS", "tRNA", "rRNA", "ncRNA", "tmRNA", "pseudogene", "gene"):
            continue
        product = attrs.get("product", "")
        gene = attrs.get("gene", "")
        name = attrs.get("Name", "")
        locus = attrs.get("locus_tag", "")
        pseudo = "pseudo=true" in attrs.get("pseudo", "") or attrs.get("pseudo") == "true" or ftype == "pseudogene"
        rows.append({
            "seqid": seqid,
            "type": ftype,
            "start": start,
            "end": end,
            "strand": strand,
            "gene": gene,
            "name": name,
            "product": product,
            "locus_tag": locus,
            "pseudo": pseudo,
        })
    return rows


def search(rows, patterns, types=("CDS",)):
    """Return rows matching any product/gene/name regex; patterns is list of (label, regex)."""
    hits = defaultdict(list)
    compiled = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in patterns]
    for r in rows:
        if r["type"] not in types:
            continue
        haystack = " ".join([r["product"], r["gene"], r["name"]])
        for label, rx in compiled:
            if rx.search(haystack):
                hits[label].append(r)
    return dict(hits)


def main():
    rows = collect_products()
    print(f"Loaded {len(rows)} annotation rows")

    results = {
        "source_gff": str(GFF.relative_to(ROOT)),
        "n_annotation_rows": len(rows),
        "n_cds": sum(1 for r in rows if r["type"] == "CDS"),
        "n_pseudo": sum(1 for r in rows if r["pseudo"]),
        "n_trna": sum(1 for r in rows if r["type"] == "tRNA"),
        "n_rrna": sum(1 for r in rows if r["type"] == "rRNA"),
        "n_tmrna": sum(1 for r in rows if r["type"] == "tmRNA"),
        "n_ncrna": sum(1 for r in rows if r["type"] == "ncRNA"),
        "claims": {},
    }

    # ---- C14 Adhesion ----
    adh = search(rows, [
        ("enolase", r"\benolase\b"),
        ("fibronectin_binding", r"fibronectin"),
        ("eps", r"\b(exopolysaccharide|EPS|epsA|epsB|epsC|epsD|epsE|epsF|epsG|epsH|epsI|epsJ|epsK|epsL|epsM|epsN|epsO|epsP|epsQ|epsR|epsX)\b"),
        ("tpi", r"triosephosphate isomerase|triose-phosphate isomerase|\btpiA?\b"),
        ("sortase_A", r"sortase|\bsrtA\b"),
        ("atp_synthase", r"ATP synthase|\batp[A-Z]\b|F0F1|F1F0"),
        ("eftu", r"elongation factor Tu|\btuf\b"),
        ("lpxtg", r"LPXTG"),
    ])
    results["claims"]["C14_adhesion"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in adh.items()}

    # ---- C15 Acid/bile tolerance ----
    acidbile = search(rows, [
        ("atp_synthase", r"ATP synthase|\batp[A-Z]\b"),
        ("ldh_any", r"lactate dehydrogenase"),
        ("glcn6p_deaminase", r"glucosamine-?6-phosphate deaminase|\bnagB\b"),
        ("ctp_synthase", r"CTP synthase|\bpyrG\b"),
        ("cfa_synthase", r"cyclopropane.*fatty.acyl|cyclopropane-fatty-acyl|\bcfa\b"),
        ("bsh", r"bile salt hydrolase|choloylglycine"),
        ("f0f1", r"F0F1|F1F0"),
    ])
    results["claims"]["C15_acidbile"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in acidbile.items()}

    # ---- C16 L- and D-lactate dehydrogenases ----
    ldh = search(rows, [
        ("L_LDH", r"L-lactate dehydrogenase|\bldh\b|\bldhL\b"),
        ("D_LDH", r"D-lactate dehydrogenase|\bldhD\b"),
        ("any_ldh", r"lactate dehydrogenase"),
    ])
    results["claims"]["C16_LDH"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in ldh.items()}

    # ---- C17 Stress ----
    stress = search(rows, [
        ("groES", r"\bgroES\b|10 kDa chaperonin|co-chaperone GroES|chaperonin GroES"),
        ("groEL", r"\bgroEL\b|60 kDa chaperonin|chaperonin GroEL"),
        ("dnaK", r"\bdnaK\b|molecular chaperone DnaK|Hsp70"),
        ("dnaJ", r"\bdnaJ\b|DnaJ"),
        ("grpE", r"\bgrpE\b|nucleotide exchange factor GrpE"),
        ("csp", r"cold[- ]shock|\bcspA?\b|\bcspB\b|\bcspC\b|\bcspD\b|\bcspE\b"),
        ("clpB", r"\bclpB\b|ATP-dependent chaperone ClpB"),
        ("clpX", r"\bclpX\b"),
        ("clpP", r"\bclpP\b"),
        ("hsp", r"heat shock"),
    ])
    results["claims"]["C17_stress"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in stress.items()}

    # ---- C18 Vitamins ----
    vit = search(rows, [
        ("thiamine_B1", r"thiamine|thiamin|\bthi[A-Z]\b"),
        ("riboflavin_B2", r"riboflavin|\brib[A-Z]\b"),
        ("pyridoxine_B6", r"pyridox|\bpdx[A-Z]\b"),
        ("biotin_B7", r"biotin|\bbio[A-Z]\b"),
        ("folate_B9", r"folate|dihydrofolate|tetrahydrofolate|methylenetetrahydrofolate|folylpolyglutamate"),
        ("cobalamin_B12", r"cobalamin|B12"),
    ])
    results["claims"]["C18_vitamins"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in vit.items()}

    # ---- C20 Tryptophan biosynthesis (serotonin precursor pathway) ----
    trp = search(rows, [
        ("trp_synthase", r"tryptophan synthase|\btrpA\b|\btrpB\b"),
        ("trpC", r"\btrpC\b|indole-3-glycerol"),
        ("trpD", r"\btrpD\b|anthranilate phosphoribosyltransferase"),
        ("trpE", r"\btrpE\b|anthranilate synthase"),
        ("trpF", r"\btrpF\b|N-\(5'-phosphoribosyl\)anthranilate isomerase"),
        ("trpG", r"\btrpG\b"),
        ("trp_general", r"tryptophan|anthranilate"),
        ("aadc", r"aromatic amino acid|aromatic-L-amino-acid decarboxylase|tryptophan decarboxylase|\baadc\b|pyridoxal-dependent decarboxylase"),
    ])
    results["claims"]["C20_tryptophan"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in trp.items()}

    # ---- C22 IS family breakdown ----
    is_hits = defaultdict(int)
    is_examples = defaultdict(list)
    for r in rows:
        m = re.search(r"(IS\d+|ISLla\d*|ISS1|IS-LL\d+)", r["product"])
        if m:
            fam = m.group(1)
            is_hits[fam] += 1
            if len(is_examples[fam]) < 5:
                is_examples[fam].append((r["seqid"], r["product"]))
    results["claims"]["C22_IS_families"] = {k: {"count": v, "examples": is_examples[k]} for k, v in is_hits.items()}

    # ---- C27 Enzymes ----
    enz = search(rows, [
        ("alpha_amylase", r"alpha-?amylase|α-amylase"),
        ("lipase", r"\blipase\b|esterase"),
        ("serine_protease", r"serine protease|serine-type"),
        ("htrA_degP", r"\bhtrA\b|\bDegP\b|HtrA"),
        ("xylanase", r"xylanase|\bxyn[A-Z]\b"),
        ("beta_glucanase", r"glucanase"),
        ("cellulase", r"cellulase"),
        ("protease_any", r"protease|peptidase"),
    ])
    results["claims"]["C27_enzymes"] = {k: ([] if k == "protease_any" else [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v]) for k, v in enz.items()}
    results["claims"]["C27_enzymes"]["protease_any_count"] = len(enz.get("protease_any", []))

    # ---- C28 Lactose utilization (lacR-ABCDFEGX) ----
    lac = search(rows, [
        ("lac_general", r"\blac[A-Z]\b|lactose|galactose"),
        ("lacR", r"\blacR\b"),
        ("lacA", r"\blacA\b"),
        ("lacB", r"\blacB\b"),
        ("lacC", r"\blacC\b"),
        ("lacD", r"\blacD\b"),
        ("lacE", r"\blacE\b"),
        ("lacF", r"\blacF\b"),
        ("lacG", r"\blacG\b"),
        ("lacX", r"\blacX\b"),
        ("pts_lactose", r"PTS.*lactose|lactose-specific"),
        ("beta_gal", r"beta-galactosidase|β-galactosidase|\blacZ\b"),
    ])
    results["claims"]["C28_lactose"] = {k: [(r["seqid"], r["gene"] or r["name"], r["product"], r["locus_tag"]) for r in v] for k, v in lac.items()}

    # Write incrementally
    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print("\nTop-level summary:")
    for k, v in results["claims"].items():
        if isinstance(v, dict):
            sub = {sk: (len(sv) if isinstance(sv, list) else sv) for sk, sv in v.items()}
            print(f"  {k}: {sub}")


if __name__ == "__main__":
    main()
