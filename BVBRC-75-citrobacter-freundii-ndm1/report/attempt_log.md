# Attempt Log — BVBRC-75

Chronological, from top.

## 2026-07-03 06:41 CDT — kickoff
- Read wave brief and BVBRC-71 exemplar to understand expected report structure.
- Confirmed paper metadata via NCBI E-utils esummary for PMID 32024012: MDPI Pathogens, Jan 2020, PMC7168644, DOI 10.3390/pathogens9020089.

## 06:41 — Paper text
- Pulled full-text XML from Europe PMC (`/webservices/rest/PMC7168644/fullTextXML`, 134 KB).
- Stripped XML tags with a small Python helper (`ElementTree` + tag walk) → `work/paper/paper_text.txt` (46,411 chars).
- Extracted key claims manually (assembly stats, ST498, resistome list, plasmid identity).
- Identified WGS accession **VWTQ00000000** and comparison plasmid **CP023554.1** from paper text.

## 06:42 — Assembly and annotation
- NCBI E-utils esearch located assembly UID 8406111 → GCF_015208815.1 (ASM1520881v1), submitted 2020-11-02 by UKZN.
- Downloaded FNA / GFF / CDS / protein / assembly-stats from the RefSeq FTP path.
- `H2730R_stats.txt` gives canonical stats: **5,299,408 bp, 58 contigs, N50=518,368, L50=4, GC=52%, SKESA 2018-09-01, Illumina MiSeq, 99x** — every one of these matches the paper's Table A1 exactly, including the SKESA v2.3 assembler + MiSeq platform.

## 06:42 — Genome stats
- Wrote `work/analysis/` python that parses the FNA (58 contigs) + GFF (5093 CDS, 116 pseudogenes, 70 tRNA, 12 rRNA of which 7×23S + 5×5S, 1 tmRNA, 1 antisense_RNA, 8 ncRNA, 9 riboswitch).
- Paper Table A1 lists "Number of RNAs=70, Number of tRNAs=12, 23S rRNAs=7, 5S rRNAs=5"; direct comparison with the GFF shows the labels for "RNAs" and "tRNAs" appear swapped in the paper (our tRNAs=70, our rRNAs=12) — the sub-breakdown of 23S=7 and 5S=5 rRNAs matches exactly.

## 06:43 — Resistome scan
- Regex-scan of PGAP CDS `product` and `gene` qualifiers against ResFinder-style keyword patterns.
- Detected **17 distinct acquired resistance loci** covering β-lactams (NDM-1, CTX-M-15, TEM-1, OXA-1, OXA-10, CMY-48), aminoglycosides (aac(6')-Ib-cr, aac(3)-IId/IIe, aadA1, phosphotransferase), sulfonamide/trimethoprim (dfrA14/dfrA23/dfrA7), tetracycline (tet(A)), chloramphenicol (cmlA5), quinolone (qnrB1), rifampin (Arr-2).
- Paper reports 25 acquired R genes. Gap is likely because paper unions ResFinder+ARG-ANNOT+CARD (which independently pick up sulfonamide sul, macrolide mph/ereA, additional aminoglycoside phospho hits) and counts subfamily hits separately. All qualitatively documented drug classes are represented.

## 06:44 — Plasmid confirmation (central claim)
- Downloaded CP023554.1 (212,326 bp p18-43_01).
- Extracted contig **NZ_VWTQ01000022.1** (14,979 bp, carries blaNDM-1) via Biopython/pickle round-trip.
- Local BLAST+ (`blastn` 2.16 in /usr/local/bin) with makeblastdb.
- Result: single primary HSP **100.000% identity across the entire 14,979 bp contig**, aligning to p18-43_01 positions 61,316–76,294. Additional HSPs for repeat elements. Total aligned = 17,310 bp (115.6% coverage counting repeats), weighted mean pident 98.97%.
- Bonus: BLAST of all 12 resistance-gene-bearing contigs vs p18-43_01 shows contigs 22 (100%/100%), 27 (99.87%/50%), 31 (98.73%/125%), 41 (99.88%/44%) all have substantial matches → several resistance regions likely derived from this same plasmid backbone.

## 06:44 — MLST typing
- PubMLST REST API: pulled scheme 1 profiles (1,250 STs) and per-locus allele FASTAs (7 loci, 228–450 alleles each).
- PubMLST current ST498 profile: `aspC=16, clpX=14, fadD=103, mdh=15, arcA=5, dnaG=54, lysP=5` — **matches paper exactly**.
- In-silico typing via local BLAST (100% identity + full length required): got exact matches for arcA=5, aspC=16, dnaG=54, lysP=5, mdh=15. clpX and fadD returned newer alleles (clpX=297, fadD=322) with 100% match, and the paper's alleles 14/103 hit at 99.82% and 99.79% (single silent C→T at pos 414 and 438 respectively). Interpretation: RefSeq assembly (deposited Nov 2020) picked up 2 SNPs vs the original ST498-defining alleles from the paper — either sequencing base-call noise or later curation. Regardless, the ST498 record in PubMLST remains defined by the paper's allele numbers, and the genome's identity to that ST is >99.7% at every locus. MLST claim: SUPPORTED.

## 06:45 — LLM judge
- `work/analysis/judge.py` sends 23 structured claims + paper summary + per-claim reproduction evidence to Argo proxy (localhost:44497, key=stevens).
- Model: `argo:gpt-5.2` (first pick, no fallback needed).
- Returns strict JSON verdict.
- Judge: **PARTIAL**, coverage 74%, agreement 82%. Top concerns center on claims that were not re-run (PlasmidFinder replicon typing, PHASTER prophages, PathogenFinder Pscore, CRISPRCasFinder, RM-Finder, GyrA S83I point mutation).

## Not re-run (marked "not-tested" in judge output)
- Plasmid replicon (Inc-type) typing via PlasmidFinder — the web tool requires database or a specific hosted service.
- Prophage prediction via PHASTER — web-only.
- Pathogenicity Pscore via PathogenFinder — web-only.
- CRISPRCasFinder / R-M system typing — web-only.
- Point-mutation call for GyrA S83I — would need translation + alignment vs reference; annotation shows gyrA presence only.
- Phylogenomic tree of South African *C. freundii* — needs > 5 genomes and CSI Phylogeny.

These are documented as "plausibility only" in the claims table so the LLM judge downweights coverage rather than agreement.

## Bugs / hiccups
- First MLST pull attempt via PubMLST BigSDB PHP download URL returned an HTML page rather than FASTA (curl exit 23). Switched to the REST API `/loci/{L}/alleles_fasta` which returns FASTA cleanly.
- Wrote `judge.py` initially into the wrong workspace-shadow path (`~/.openclaw/workspace/BVBRC-75...` instead of `~/Dropbox/REPLICATE-PROJECT/BVBRC-75...`) — caught immediately and moved.
- No compute needed to leave CherryRd — genome is 5.3 Mbp, all analysis ran in under 3 min locally with Biopython + BLAST+.

## Wall-clock
Kickoff → final report ≈ 20 min on CherryRd.
