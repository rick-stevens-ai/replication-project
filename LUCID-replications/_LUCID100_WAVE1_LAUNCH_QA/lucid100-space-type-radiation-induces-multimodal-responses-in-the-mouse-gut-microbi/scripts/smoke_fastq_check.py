#!/usr/bin/env python3
"""
Smoke test: verify a downloaded FASTQ pair against ENA metadata and check that
reads look like 16S V4 amplicons (F515/R806 primers expected from the methods).

Usage:
    smoke_fastq_check.py [RUN_ACCESSION]   # default SRR5210762 (smallest)
"""
import csv, gzip, hashlib, os, sys, pathlib, collections

SLOT = pathlib.Path(__file__).resolve().parents[1]
FRP  = SLOT / "harvest" / "ena_filereport.tsv"

def main():
    acc = sys.argv[1] if len(sys.argv) > 1 else "SRR5210762"
    with open(FRP) as f:
        rows = {r["run_accession"]: r for r in csv.DictReader(f, delimiter="\t")}
    if acc not in rows:
        sys.exit(f"Run {acc} not in {FRP}")
    r = rows[acc]
    print(f"Run: {acc}  Sample: {r['sample_accession']}  Title: {r['sample_title']}")
    print(f"Strategy: {r['library_strategy']} | Source: {r['library_source']} | "
          f"Layout: {r['library_layout']} | Platform: {r['instrument_platform']}/{r['instrument_model']}")
    print(f"Expected reads: {r['read_count']}  bases: {r['base_count']}")

    urls = r["fastq_ftp"].split(";")
    md5s = r["fastq_md5"].split(";")
    smoke = SLOT / "data" / "smoke"
    ok = True
    for url, md5 in zip(urls, md5s):
        name = url.rsplit("/", 1)[-1]
        path = smoke / name
        if not path.exists():
            print(f"  [MISS] {name} — run fetch_all_fastq.sh")
            ok = False; continue
        h = hashlib.md5()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        got = h.hexdigest()
        status = "OK " if got == md5 else "BAD"
        print(f"  [{status}] {name}  md5={got}  expected={md5}")
        if got != md5: ok = False
    if not ok:
        sys.exit(1)

    # Count reads in R1 + look for V4 primer signature
    r1 = smoke / urls[0].rsplit("/", 1)[-1]
    n = 0; head_kmers = collections.Counter()
    with gzip.open(r1, "rt") as f:
        while True:
            hdr = f.readline()
            if not hdr: break
            seq  = f.readline().rstrip()
            plus = f.readline()
            qual = f.readline()
            n += 1
            head_kmers[seq[:5]] += 1
    print(f"Counted reads in R1: {n}  (matches ENA: {n == int(r['read_count'])})")
    print(f"Most common 5-mer at read start (V4 expected ~TACGT): "
          f"{head_kmers.most_common(3)}")
    print("Smoke test PASS." if n == int(r['read_count']) else "Smoke test FAIL.")

if __name__ == "__main__":
    main()
