# BVBRC-113 — Workflow

**Paper:** Nakazono et al. 2022, PLoS ONE, doi:10.1371/journal.pone.0258283
**Date executed:** 2026-07-05
**Host:** CherryRd
**Environment:** Python 3.14.6 venv, Biopython 1.87, NCBI BLAST+ (blastp, makeblastdb), NCBI E-utilities
**LLM judge:** Argo proxy at `127.0.0.1:44497` (Bearer stevens), model `argo:claude-sonnet-4.6` (free)
**Verdict:** PARTIAL, 74/100

---

## Stage 0 — Scope decision

- 8 in-silico testable claims (C1–C8) were extracted from the paper's Tables 2–3 and Figures 2–3.
- Wet-lab claims (bacteriocin purification, MS, plasmid curing, MW2 braRS assays, M. luteus co-culture, spectrum panels) declared explicitly out of scope: they require the actual KSE56 / KSE650 strains and are NOT TESTED here.

## Stage 1 — Paper acquisition

```
esummary -db pubmed -id 35041663           # -> PMCID PMC8765612, DOI 10.1371/journal.pone.0258283
efetch  -db pmc     -id PMC8765612 -format xml > work/paper.xml     # 225,843 B
```

## Stage 2 — Sequence acquisition

For each accession in `{OK031036, OK031035, KP702950, X62386, U77778}`:

```
efetch -db nuccore -id <ACC> -format gb    > work/sequences/<ACC>.gb
efetch -db nuccore -id <ACC> -format fasta > work/sequences/<ACC>.fasta
```

- `OK031036` — pEpi56 (KSE56, 64,386 bp, circular)
- `OK031035` — pNuk650 (KSE650, 26,160 bp, circular)
- `KP702950` — pIVK45 comparator (21,840 bp)
- `X62386`   — Tü3298 epidermin reference
- `U77778`   — nukacin locus reference (context)

## Stage 3 — Structural verification (`work/analyze_plasmids.py`)

1. Parse each GenBank with Biopython `SeqIO.read`.
2. Record `len(record.seq)`, `record.annotations['topology']`, count of `CDS` features, count of `gene` features, organism.
3. For pEpi56, extract every CDS whose `gene` qualifier matches `epi*`.
4. For pNuk650, extract every CDS whose `gene` qualifier matches `nuk*`.
5. Serialize → `report/evidence/plasmid_summary.json`.

## Stage 4 — Bacteriocin identity (`work/bacteriocin_align.py`)

1. Locate `epiA` CDS on `OK031036` (KSE56) and `X62386` (Tü3298); extract nt + translated aa.
2. Locate `nukA` CDS on `OK031035` (KSE650) and `KP702950` (IVK45); extract nt + translated aa.
3. Since both loci had identical CDS lengths, direct position-by-position mismatch counting (no alignment needed):
   - `nt_mm = sum(a != b for a, b in zip(nt1, nt2))`
   - `aa_mm = sum(a != b for a, b in zip(aa1, aa2))`
4. Mature-peptide comparison over the terminal 27 aa (nukacin IVK45 mature is 27 aa).
5. Serialize → `report/evidence/bacteriocin_alignment.json`.

## Stage 5 — Comparative ORF-delta (`work/compare_plasmids.py`)

1. Extract all 29 pNuk650 CDS protein sequences → `proteins_pNuk650.faa`.
2. Extract all 17 pIVK45 CDS protein sequences → `proteins_pIVK45.faa`.
3. `makeblastdb -in proteins_pIVK45.faa -dbtype prot -out ivk45_db`
4. `blastp -query proteins_pNuk650.faa -db ivk45_db -evalue 1e-5 -max_target_seqs 1 -outfmt 6`
5. Ortholog rule: `pident >= 30% AND qcov >= 50%`. Non-ortholog pNuk650 CDS counted.
6. Serialize → `report/evidence/pNuk650_vs_pIVK45_blast.json`.

## Stage 6 — LLM judge (`work/llm_judge.py`)

1. Bundle the three JSON evidence blobs with a numbered claims table (C1–C8).
2. POST to `http://127.0.0.1:44497/v1/chat/completions` with `Authorization: Bearer stevens`.
3. First tried `argo:claude-opus-4.7` and `argo:claude-opus-4.8` — both returned HTTP 502 on the ~30 kB payload.
4. Fell back to `argo:claude-sonnet-4.6` — completed cleanly.
5. Save raw response → `report/evidence/llm_judge_verdict.txt`.

## Stage 7 — Report assembly

- Markdown REPORT.md hand-written from the deterministic evidence JSONs + judge verdict.
- LaTeX REPORT.tex mirrored from REPORT.md with an added GENUINE CRITIQUE section.
- Failure analysis and open questions distilled post-hoc.

---

## Total wall time

≈ 30 s (fetch + analyze + BLAST + judge, excluding paper download).

## Reproducibility snippet

```bash
cd work
python3 -m venv .venv && source .venv/bin/activate
pip install biopython
python analyze_plasmids.py
python bacteriocin_align.py
python compare_plasmids.py
python llm_judge.py
```
