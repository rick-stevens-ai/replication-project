#!/usr/bin/env python3
"""Extract CDS translations from each Genbank file using a tolerant regex parser
(the supplementary GBK files have malformed LOCUS lines that crash Biopython 1.x)."""
import re
import json
from pathlib import Path

GBK_DIR = Path("data/genbank/Genbank_files")
OUT_DIR = Path("data/proteins")
OUT_DIR.mkdir(parents=True, exist_ok=True)

STRAINS = {
    "PAC_4875":  "Propionibacterium_acidipropionici_ATCC_4875.gbk",
    "PAC_55737": "Propionibacterium_acidipropionici_55737.gbk",
    "PSHE":      "Propionibacterium_freudenreichii_subsp._shermanii_CIRM-BIA1.gbk",
    "PAVI":      "Propionibacterium_avidum_44067.gbk",
    "PACN":      "Propionibacterium_acnes_6609.gbk",
    "PPRO":      "Propionibacterium_propionicum_F0230a.gbk",
}

def parse_gbk_cds(path):
    """Yield (locus_tag_or_id, aa_seq) tuples for each CDS that has /translation=..."""
    text = path.read_text()
    # Split into features. A feature starts at column 5 with a feature-name token.
    # We'll find every "     CDS " (5 spaces, then feature name) block.
    # The block ends at the next feature key (col 5 non-space) or the section keyword
    # (column 0 non-space like CONTIG, ORIGIN, //, etc.)
    feat_re = re.compile(r"^ {5}([A-Za-z_]+)\s+([^\n]+)", re.M)
    matches = list(feat_re.finditer(text))
    cds_idx = 0
    for i, m in enumerate(matches):
        feat_name = m.group(1)
        if feat_name != "CDS":
            continue
        cds_idx += 1
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[start:end]
        # extract /translation="..."
        tr_m = re.search(r'/translation="([^"]*)"', block, re.S)
        if not tr_m:
            continue
        aa = re.sub(r'\s+', '', tr_m.group(1))
        # try locus_tag, gene, protein_id, fallback to index
        locus = re.search(r'/locus_tag="([^"]+)"', block)
        gene  = re.search(r'/gene="([^"]+)"', block)
        pid   = re.search(r'/protein_id="([^"]+)"', block)
        for c in (locus, gene, pid):
            if c:
                raw_id = c.group(1)
                break
        else:
            raw_id = f"cds{cds_idx}"
        yield raw_id, aa


def main():
    stats = {}
    combined = OUT_DIR / "all_proteins.faa"
    with combined.open("w") as out_all:
        for tag, fname in STRAINS.items():
            gbk = GBK_DIR / fname
            per_strain = OUT_DIR / f"{tag}.faa"
            n = 0
            seen = set()
            with per_strain.open("w") as fout:
                for raw_id, aa in parse_gbk_cds(gbk):
                    safe = re.sub(r'[^A-Za-z0-9_.\-]', '_', raw_id)
                    # ensure uniqueness inside strain
                    base = safe
                    k = 1
                    while safe in seen:
                        k += 1
                        safe = f"{base}_{k}"
                    seen.add(safe)
                    seq_id = f"{tag}|{safe}"
                    fout.write(f">{seq_id}\n{aa}\n")
                    out_all.write(f">{seq_id}\n{aa}\n")
                    n += 1
            stats[tag] = {"file": fname, "n_cds_with_translation": n}
            print(f"{tag:10s} {n:6d} proteins  -> {per_strain}", flush=True)

    (OUT_DIR / "extract_stats.json").write_text(json.dumps(stats, indent=2))
    total = sum(s["n_cds_with_translation"] for s in stats.values())
    print(f"\nCombined: {combined}  total = {total}")

if __name__ == "__main__":
    main()
