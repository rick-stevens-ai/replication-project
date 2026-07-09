# Attempt Log — BVBRC-71 (Ms. mobilis Shm1)

Session: agent:main:subagent:e36e5c33-ca51-44f5-8ae1-0020ec3a4712
Executor: Ollie (subagent), 2026-07-03 00:07 – 00:20 CDT

## Timeline

**T+0** Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Confirmed free-endpoints-only rule, LLM-judge requirement, no-overwrite policy.

**T+1** Confirmed no prior `BVBRC-71-*` directory exists. Created `~/Dropbox/REPLICATE-PROJECT/BVBRC-71-methylospira-mobilis/{report/evidence,work}/`.

**T+2** Fetched PubMed abstract for PMID 31835835 via NCBI E-utils from uicgpu. Confirmed authors, journal, and key qualitative claims (4.7 Mbp, >4800 CDS, pMMO/sMMO, Mo-Fe + V-Fe nitrogenases, expanded chemotaxis, IS load).

**T+3** Attempted to fetch full PDF from MDPI (`https://www.mdpi.com/2076-2607/7/12/683/pdf`) — blocked with 403 Access Denied even with a browser UA. Attempted PMC direct PDF and PMC OA package (`ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/8b/e5/PMC6956133.tar.gz`) — 404. Succeeded with Europe PMC full-text XML (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6956133/fullTextXML`, 162 KB). Extracted plain text.

**T+4** Grepped extracted text for accession numbers and quantitative claims. Found:
- Ms. mobilis Shm1 genome accession: **CP044205** (deposited DDBJ/NCBI/EMBL)
- Comparator: Mc. capsulatus Bath, **AE017282.2**
- Quantitative claims: 4.7 Mbp single contig, G+C 54 mol%, 3 rRNA operons, 49 tRNA, 4858 CDS (RAST); 16S identity vs Bath = 94.06 %; >200 IS elements; 2 CRISPR loci

**T+5** Downloaded both GenBank flat files with `gbwithparts` from NCBI E-utils on uicgpu:
- CP044205.gb: 10.6 MB
- AE017282.gb: 7.2 MB

**T+6** Ran `genome_stats.py` (Biopython) on both. Confirmed:
- Shm1: 4,703,534 bp (matches 4.7 Mbp), GC 54.05 % (matches 54 mol%), 3+3+3 rRNA (matches 3 operons), 48 tRNA (paper: 49), 4214 CDS (paper: 4858 RAST — see analysis note), 171 pseudogenes.
- Bath: 3,304,561 bp (matches 3.3 Mbp), GC 63.58 % (matches 63.6 mol%), 2+2+2 rRNA (matches 2 operons), 46 tRNA, 2960 CDS.

**T+7** Ran `gene_products_scan.py` — regex/keyword scan over CDS `product`, `gene`, `note` qualifiers for methanotrophy pathway genes. First pass showed many "0" hits for pmo/mmo in Shm1; investigation revealed submitter annotation uses generic "methane monooxygenase" and "methane monooxygenase/ammonia monooxygenase subunit A/B/C" product strings rather than pmoA/B/C gene names.

**T+8** Re-scanned Shm1 by broader product-string keywords. Confirmed:
- pMMO cluster at F6R98_01470–01480 ("methane monooxygenase/ammonia monooxygenase subunit A/B/C")
- sMMO cluster at F6R98_10895–10905 ("soluble methane monooxygenase-binding protein MmoD" + 4 additional MMO CDS)
- Methanol dehydrogenase F6R98_08170 (generic product label)
- nifH/D/K annotated with gene names (1/2/2 copies); vnfD explicitly annotated at F6R98_01760, plus "vanadium nitrogenase" at F6R98_01835
- CRISPR type I-E with cas1/2/3, casA/B, cas7e/5e/6e — matches paper's "cas array" claim
- 44 flagellar CDS, 52 chemotaxis CDS (vs 2 MCP hits in Bath — dramatic asymmetry confirmed)
- 194 transposase-family CDS (paper: >200)

**T+9** Extracted 16S rRNA sequences from both genomes, ran Biopython global PairwiseAligner. Result: **93.89 % identity over ungapped positions** (Shm1 1538 bp vs Bath 1473 bp; matches=1383, mismatches=90, gaps=65). Paper reports 94.06 %. Within tool tolerance (different aligners: paper likely used SILVA / EzBioCloud alignment).

**T+10** Wrote 21-claim verification table (`evidence/claim_verification.md`).

**T+11** Transferred all evidence from uicgpu back to CherryRd (Dropbox) via scp.

**T+12** Ran LLM-judge scoring via Argo proxy (localhost:44497). First tried `argo:claude-opus-4.7` — 502 Bad Gateway on payloads with `max_tokens=2500`. Retried with `argo:gpt-5.2` (also free via Argo) — succeeded first try. Judge returned:
- verdict: **PARTIAL**
- coverage_pct: 100
- agreement_pct: 86
- 17/21 claims marked `agrees=true`, 4/21 flagged (C4 tRNA off-by-1, C5 CDS count pipeline mismatch, C12 MDH substring-based, C16 IS 194<200)

**T+13** LLM judge output stored at `evidence/llm_judge_verdict.json`. Wrote REPORT.md, brief.md, artifact_harvest.md.

## What worked
- Europe PMC full-text XML (open API, no auth) as fallback when MDPI + PMC PDF were blocked
- NCBI E-utils `gbwithparts` for full annotated GenBank flat files
- Biopython for both feature counts and pairwise 16S alignment (no external BLAST needed)
- Broadening gene-name search to product/note strings after seeing NCBI/PGAP uses different naming than paper

## What didn't work
- MDPI PDF download from either host (Akamai edge blocks non-browser UA)
- `argo:claude-opus-4.7` with `max_tokens >= 2500` — 502 gateway error (reproducible); Argo evidently has an unpublished cap. Falling back to gpt-5.2 worked cleanly.

## Not attempted (out of scope for a genome-announcement replication)
- Full RAST re-annotation via BV-BRC web workflow (would take ~1 h wallclock and add no new evidence beyond what CDS count discrepancy already tells us)
- Phylogenomic reconstruction on 120 single-copy proteins (paper Fig. 3) — treated as a downstream analysis, not a core claim
- Formal ANI (only 16S rRNA identity was tested)
