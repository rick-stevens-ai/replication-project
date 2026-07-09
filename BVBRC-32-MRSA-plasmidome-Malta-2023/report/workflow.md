# Workflow — BVBRC-32 Replication

Independent re-analysis of Al-Trad et al. 2023 (*Antibiotics* 12(4):733,
DOI 10.3390/antibiotics12040733) — MRSA plasmidome from HSNZ, Kuala
Terengganu, Malaysia.

**Host:** CherryRd (local BLAST+; NCBI Datasets v2; CGE reference DBs).
**Date:** 2026-07-01.
**Verdict:** PARTIAL replication (LLM-judge `argo:gpt-5.2`).

> **Naming caveat.** Ledger tag is `-Malta-2023` but the paper is Malaysia,
> not Malta. Confirmed via CrossRef DOI and PMID 37107095. Directory name
> retained; all analysis on the correct paper.

## Stage 1 — Paper identification & scope
- Resolve DOI → CrossRef → confirm journal, authors, year.
- Fetch OA PDF (PMC10135026, CC BY).
- Extract paper's stated inputs: 79 sequenced + 15 previously published =
  94 total MRSA; BioProject `PRJNA722830`.
- Define replication scope: plasmid replicon typing, plasmid-borne AMR,
  biocide (qacA/B), mecA universality. **Explicitly excluded:**
  heavy-metal operon curation, SNP phylogeny, spa/ST typing.

## Stage 2 — Data retrieval
- Tool: NCBI `datasets` v2 CLI.
- Query: BioProject `PRJNA722830` → all GCA assemblies.
- Delivered: **88 GCA assemblies** (72.8 MB FASTA-only, genome level).
- Delta vs paper: 88 recovered vs 94 cited (79 sequenced + 15 external).
  The 15 external genomes (AOCQ/ANPO/AMRB/AMRC/AMRD/AMRE00000000 +
  PRJNA503680) were **not** pulled. All percentages are relative to 88.

## Stage 3 — Reference databases
- **CGE PlasmidFinder Gram-positive DB** (RepA_N, RepL, Rep1, Rep2, Rep3,
  Rep_trans, NT_Rep, Inc18). Pulled fresh from CGE.
- **CGE ResFinder DB** (`all.fsa`, full allele set).
- **CGE DisinFinder DB** (qac family).
- No custom heavy-metal DB assembled.

## Stage 4 — Replicon typing
- Per-assembly `blastn` vs PlasmidFinder Gram-positive DB.
- Thresholds: **≥80% identity, ≥60% coverage** (CGE PlasmidFinder defaults).
- Redundant hits collapsed to distinct **replicon loci** by contig-overlap
  clustering (loci on the same contig sharing overlap = one locus).
- `rep→superfamily` mapping per PlasmidFinder nomenclature; `repUS18` →
  PriCT_1.
- Output: 279 replicon loci across 88 genomes (paper: 189 curated plasmid
  molecules).

## Stage 5 — AMR gene detection
- Per-assembly `blastn` vs ResFinder DB.
- Thresholds: **≥90% id, ≥60% cov**; best hit per gene per genome.
- Output: mecA 88/88; blaZ 87/88; erm(C) 67; tet(K) 5; tet(L) 3;
  aadD 2; mupA 1; erm(B) 1; lnu 1; cat 3; aac(6′)-aph(2″) 23.
- Manual exclusion: the full Enterobacterales **blaTEM** allele family
  cross-hit (n=1 each) in a single genome — flagged as raw-allele-DB
  artifact, excluded from plasmid-AMR tally.

## Stage 6 — Biocide detection
- Per-assembly `blastn` vs DisinFinder (qac) DB, 80/60.
- Output: qacA/qacB in 5 genomes, all plasmid-borne.

## Stage 7 — Plasmid-vs-chromosome assignment
- Rule: an AMR/biocide hit is **plasmid-borne** iff its contig also
  carries a detected PlasmidFinder replicase.
- Coarse but reproducible; the paper's alternative (curated plasmid
  molecules) requires manual PCR-guided gap closure not achievable from
  public draft contigs.
- Output: erm(C) 66/67 plasmid; blaZ 17/87 plasmid; qacA/B 5/5 plasmid.

## Stage 8 — Claim mapping
- Manual extraction of quantitative claims from the paper into an 11-row
  claim table (C1–C11).
- Match each to a replication statistic; assign per-claim verdict.
- Verdicts: 8× VERIFIED / VERIFIED (exact), 2× PARTIAL, 1× NOT TESTED.

## Stage 9 — LLM judge
- Model: `argo:gpt-5.2` (opus-4.8 proxy returned 502; documented in
  REPORT.md).
- Input: paper abstract + methods excerpt + replication claim table.
- Output: per-claim assessment + overall verdict **PARTIAL REPLICATION**.
- Stored in `judge_verdict.md`.

## Stage 10 — Reporting
- `REPORT.md` — canonical human-readable report (source of truth for the
  other artifacts).
- `REPORT.tex` — LaTeX rendering with dedicated Genuine Critique section.
- `open_questions.json` — 5 truly open questions grounded in REPORT.md.
- `workflow.md` — this file.
- `artifacts_summary.md` — file-by-file artifact inventory.
- `failure_analysis.md` — honest accounting of what did not reproduce
  and why.

## Reproducibility notes
- All CGE reference DBs are public and versioned. Any drift in
  PlasmidFinder allele coverage between the paper's original run and this
  replication is a plausible source of the extra Inc18 signal.
- The BLASTn thresholds used here (**80/60** replicon, **90/60** AMR,
  **80/60** biocide) are CGE web-service defaults. Any change to these
  will shift absolute counts.
- The `plasmid-borne = shared-contig-with-replicase` rule is stricter
  than a proximity-graph rule and looser than a closed-molecule rule;
  documenting it explicitly for downstream re-use.
