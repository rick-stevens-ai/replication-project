# Workflow & effort — BVBRC-130

## Narrative

The paper is a species-announcement paper backed by a deposited PacBio single-chromosome assembly (CP124620). The most efficient replication route is:

1. **Ground truth = the deposited FASTA + feature table**, not the raw PacBio reads. All the paper's numeric claims (length, GC, contig count, gene count) are properties of the deposited assembly itself.
2. **Species-boundary check via modern ANI** (skani) against the closest publicly-available *Stenotrophomonas* references. This substitutes for the paper's TYGS/dDDH pipeline with a well-established equivalent (ANI 95 % ≈ dDDH 70 %).
3. **16S negative control** via BLAST — the paper's key methodological point (16S is not species-resolving in *Stenotrophomonas*) is directly testable.

Total wall-clock: **~8 minutes**, entirely from a laptop shell + free NCBI/F1000 endpoints. No heavy compute was necessary; `ssh uicgpu` was not invoked because the ANI job finished in ~50 ms locally.

## Tools & versions

| Tool | Version | Role |
|------|---------|------|
| `curl` | macOS system | HTTP fetches (PDF, EUtils, BLAST download) |
| `pdftotext` | Poppler `/usr/local/bin/pdftotext` | PDF → text for grep + Marker fallback |
| `python3` | system | FASTA parser, feature-table parser, JSON output |
| `blastn` | NCBI BLAST+ (mbedtls 3.6.5) | Remote 16S BLAST vs `nt` |
| `skani` | learned-ANI mode | Whole-genome ANI (triangle mode) |
| `shasum` | macOS system | Artifact fingerprints |

Standard library only for the Python scripts; no venv needed.

## Data endpoints (all FREE)

- **NCBI EUtils** — esummary, efetch, elink (no auth, gentle rate).
- **F1000Research** — public PDF at `/articles/12-1373/v3/pdf`.
- **NCBI BLAST** — `blastn -remote`.

## Free-endpoint LLM use

The numeric/taxonomic checks (C1–C7) require zero LLM inference — they are direct fingerprint comparisons. No LLM judge was invoked because the ground truth is byte-level identical to derivations from the deposited data. The narrative report writing was done inside the OpenClaw agent turn (Argo Opus 4.7 via `localhost:44497`), no paid endpoint touched.

## Enumerated steps (with commands)

```sh
# 1. Metadata
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=38021406&retmode=json"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=38021406&rettype=abstract&retmode=text" > work/abstract.txt

# 2. Paper PDF (PMC fell back to F1000 direct)
curl -sL "https://f1000research.com/articles/12-1373/v3/pdf" -o paper.pdf
pdftotext -layout paper.pdf work/paper.txt

# 3. Assembly + feature table
curl -s "…efetch…db=nuccore&id=CP124620&rettype=fasta" -o work/CP124620.fasta
curl -s "…efetch…db=nuccore&id=CP124620&rettype=ft"    -o work/CP124620.features.txt

# 4. Length + GC + N-count (Python one-liner over the FASTA)
python3 …  # see report

# 5. Assembly metadata via elink → assembly esummary
curl -s "…elink…dbfrom=nuccore&db=assembly&id=CP124620&retmode=json"
curl -s "…esummary…db=assembly&id=16697841&retmode=json"

# 6. Annotation counts
python3 parse_feature_table.py > report/evidence/genome_stats.json  # inline in the notebook-style Python

# 7. 16S BLAST (novelty methodology check)
blastn -query 16S_1.fasta -db nt -remote -entrez_query "Stenotrophomonas[Organism]" \
       -max_target_seqs 8 -outfmt "6 sacc sscinames pident length evalue"

# 8. Reference-genome fetches for ANI
for acc in CP118898 OZ345833; do
    curl -s "…efetch…db=nuccore&id=$acc&rettype=fasta" -o work/$acc.fasta
done

# 9. ANI triangle
skani triangle CP124620.fasta CP118898.fasta OZ345833.fasta -t 4 --sparse > work/skani_ani.tsv
```

## Effort estimate

- **Wall-clock:** ~8 min end-to-end (metadata → verdict).
- **Human/agent turns:** ~15 shell exec calls, 6 file writes.
- **LOC written:** ~120 lines of shell + inline Python (parser + stats scripts).
- **Compute:** ≈50 ms skani, ~30 s BLAST-remote, dominated by NCBI RTT.
- **Bytes downloaded:** ~14.6 MB (paper 1.5 MB, three FASTAs 13 MB, feature table 1 MB, misc JSON ~10 KB).
- **Bytes derived:** ~80 KB of tables, JSONs, and text outputs (evidence).
