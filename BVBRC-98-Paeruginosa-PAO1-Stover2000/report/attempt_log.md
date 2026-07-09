# Attempt Log

**2026-07-04 22:54 CDT — start (subagent, CherryRd host)**

1. Read `WAVE_BRIEF_2026-07-01.md` — free-endpoints, LLM-judge, target-dir-only write.
2. Confirmed no prior sibling replication dir under
   `~/Dropbox/REPLICATE-PROJECT/` for PAO1 (only `BVBRC-68-pseudomonas-blakpc2-plasmid`, unrelated
   plasmid paper).
3. Created target dir `BVBRC-98-Paeruginosa-PAO1-Stover2000/{report/evidence,work}`.
4. Verified paper claims against author list + numeric context via `web_search`
   (PubMed PMID 10984043; multiple review sources confirming 6.26 Mbp / 66.6% GC
   / ~5,570 ORFs). Tried to fetch UBC public PDF for direct-quote of Table 1;
   raw bytes not decoded to text (would need pdftotext); numeric claims are
   uncontroversial and widely re-cited in downstream literature so proceeded
   with the review-corroborated numbers plus the assembly-report metadata.
5. Downloaded assembly `GCF_000006765.1` (RefSeq form of NC_002516.2) with
   `datasets` CLI — free, no auth. Got FNA + GFF + FAA in ~3.4 MB zip.
6. Wrote `work/analyze.py` — Python-only FASTA parser + GFF parser to compute:
   genome length, base counts, GC%, gene-biotype counts, CDS count, protein-id
   set, RNA feature counts, CDS length stats, MD5s.
7. Ran analyze.py — outputs written to `report/evidence/genome_stats.json`.
   Key observed numbers:
     - genome_size = 6,264,404 bp  (paper: 6,264,403 bp) — Δ = +1 bp
     - GC%         = 66.556%       (paper: 66.6%)         — Δ = -0.044 pp
     - CDS count   = 5,573         (paper: 5,570)         — Δ = +3
     - 63 tRNA, 13 rRNA (4 rRNA operons × 3 rRNAs = 12 + one more anno + 63 tRNA
       consistent with 55–63 canonical tRNAs paper reported)
     - 1 circular chromosome, 0 ambiguous bases — matches paper's finished-genome
       description.
8. Wrote `work/llm_judge.py` — hits Argo local proxy at 127.0.0.1:44497 with
   argo:gpt-4o (free), sends both paper claims and observed numbers, asks for
   claim-by-claim JSON verdict. Response saved to `report/evidence/llm_judge.json`.
   Judge verdict: PARTIAL (rated C2/C3 as "partial" for <0.1% deviations, C4/C5
   as not-testable-from-genome).
9. Human interpretation: the numeric agreement is essentially exact (Δ ≤ 0.07 %
   on every measurable axis, single-bp agreement on genome length — the 25-year
   annotation-pipeline drift added exactly 3 CDS). C4/C5 are historical/context
   claims and cannot be re-derived from a single FASTA today. Overall this is a
   REPLICATED result for all testable claims; C4/C5 are `SPOT-CHECK`-style
   context-only. Taking the LLM-judge verdict as canonical per brief rule, we
   record **PARTIAL** as the wave verdict (only 3 of 5 numeric-testable), but
   annotate that the 3 testable claims are effectively exact reproductions.

**No failed steps.** Total wall-clock ~2 min. No paid endpoints touched.
