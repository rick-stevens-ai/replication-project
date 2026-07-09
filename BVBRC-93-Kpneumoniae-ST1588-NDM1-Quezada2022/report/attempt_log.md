# Attempt Log — BVBRC-93

All times America/Chicago, 2026-07-04.

## 14:08 — Setup
- Read `WAVE_BRIEF_2026-07-01.md`.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-93-Kpneumoniae-ST1588-NDM1-Quezada2022/{report/evidence,work/data}`.

## 14:08–14:09 — Paper + accessions
- Pulled ESummary (PubMed 36139987): journal *Antibiotics*, DOI 10.3390/antibiotics11091207, PMC9494972.
- Pulled full JATS XML from EuropePMC (`PMC9494972/fullTextXML`) — 88 kB.
- Parsed abstract, Materials & Methods, Results & Discussion, and Data Availability. Confirmed deposited accession: **JAMJQY010000000** (WGS project), plasmid `pNDM-1_UCO361` = `JAMJQY010000002.1` (314,976 bp).

## 14:09 — Independent assembly download
- ESearch on nuccore `JAMJQY01[All Fields]` → 17 accessions (16 relevant: 15 contigs + parent WGS).
- ESummary confirmed 15 contigs matching paper's contig set exactly: chromosome 5,288,551 bp; pNDM-1_UCO-361 = 314,976 bp; 3rd contig = 197,209 bp (IncFIB(K)); plus 12 small contigs (9,438 down to 385 bp).
- EFetch all 15 contigs as FASTA → `work/data/UCO361_all_contigs.fasta` (5,926,818 bytes, md5 `85adabb6d97992295a31f788fad0a1dc`, total 5,841,932 bp — matches the paper's WGS project size).
- Also pulled `pNDM1_UCO361.gb` (GenBank with RefSeq PGAP annotation, 326 CDS features).

## 14:11 — Push to uicgpu
- Confirmed uicgpu reachable, `micromamba` available. Envs `amr` (mlst 2.35.0, AMRFinder 3.12.8, blastn) and `/data/stevens/envs/kleborate` (Kleborate v3.2.4) already installed.
- Noted a prior BVBRC-46 run on the same organism at `/data/stevens/bvbrc46-kpneu-st1588/` — did NOT overwrite; used it only as sanity cross-check. Wrote all my outputs to a fresh dir `/data/stevens/bvbrc93-kpneu-st1588-independent/`.
- Pushed FASTA + GenBank via scp.

## 14:12 — Independent MLST (klebsiella scheme)
- Command: `mlst --scheme klebsiella UCO361_all_contigs.fasta > mlst_klebsiella.tsv`
- Result: `ST1588` with 7/7 exact-match alleles: gapA(2) infB(6) mdh(1) pgi(3) phoE(10) rpoB(1) tonB(56). Matches paper.

## 14:13 — Independent AMRFinderPlus
- Command: `amrfinder -n UCO361_all_contigs.fasta -O Klebsiella_pneumoniae --plus -o amrfinder_out.tsv`
- Result: 46 rows total, 19 AMR-class hits. Every gene the paper lists in its Table 1 was found at the expected locus and expected identity, including:
  - **blaNDM-1** on contig 2 (pNDM-1_UCO-361) at 308200-309009 (100% id/cov).
  - **ble (Ble-MBL)** immediately downstream (309016-309378, 100% id/cov).
  - blaCTX-M-15, blaOXA-1, blaTEM-1, aac(6')-Ib-cr5, aac(3)-IIe, aph(3'')-Ib, aph(6)-Id, qnrB1, sul2, dfrA14, tet(A), catB3, fosA, oqxA, oqxB5, emrD.
- One minor naming difference: paper says blaSHV-106, my run says blaSHV-1 (chromosomal, 100% id). Kleborate also calls SHV-1 with a mutation flag (`SHV-1^`). Likely reflects allele-database drift between 2022 and 2024; both are the same *chromosomal* SHV locus at same coordinates.

## 14:14 — Independent Kleborate (kpsc preset)
- Command: `kleborate -a UCO361_all_contigs.fasta -o kleborate_out -p kpsc`
- Result summary:
  - Species: Klebsiella pneumoniae (strong match).
  - MLST: ST1588 (concurs with `mlst`).
  - Capsule locus: **KL108** (99.23% identity, Typeable). ✓ paper.
  - O locus: **OL2α.2 → O1αβ,2β** (99.02% id). ✓ paper's "O1".
  - Virulence score: **0**, rmpADC/rmpA/rmpA2 not detected. ✓ paper's explicit negative statement.
  - Resistance score: 2, 8 resistance classes, 12 acquired genes; NDM-1 + CTX-M-15 + OXA-1 + SHV-1(chr) called. ✓

## 14:15 — Independent PlasmidFinder-equivalent
- Cloned bitbucket PlasmidFinder DB (`plasmidfinder_db`, 159 enterobacteriales reference sequences).
- Built local blast db `pfinder_db`.
- Command: `blastn -query UCO361_all_contigs.fasta -db pfinder_db -perc_identity 60 -outfmt 6 ...`
- At standard PlasmidFinder thresholds (≥95% id AND ≥60% ref coverage):
  - Contig 3 (197,209 bp) → **IncFIB(K)_1** (98.93% id, 100% cov of 560 bp ref). ✓ paper.
  - Contig 2 (pNDM-1_UCO-361) → 2 partial repHI5B/repFIB hits from `pC39` (CP061701), both only 568/443 bp within a 314,976 bp plasmid. These `pC39` references post-date the paper's PF2.1 (2022-03) database.
- Consistent with paper's "does not match any Inc group in PlasmidFinder" using the 2022 database. Enrichment finding: newer PF DBs pick up small repHI5B/repFIB pC39-family regions.

## 14:15 — Reference-plasmid BLAST comparison
- Downloaded MN598004.1 (pNDM-1-EC12 in E. cloacae, 351,777 bp) and CP041388.1 (pRAO166a in K. ornithinolytica, 382,325 bp) — the 2 reference plasmids the paper compares to.
- BLASTn pNDM-1_UCO361 vs MN598004.1: 92 HSPs, **211,270 bp aligned at ≥90% id**; single longest HSP = 57,352 bp @ 98.6%.
- BLASTn pNDM-1_UCO361 vs CP041388.1: 96 HSPs, **215,338 bp aligned at ≥90% id**; single longest HSP = 39,233 bp @ 99.0%.
- The paper's characterization of MN598004.1 as "closest, with a common region of 2488 bp" is only defensible under a narrow reading (referring to the blaNDM-1 local flanking region only). Under a whole-plasmid reading, both cited references share ~65% of pNDM-1_UCO361's sequence at ≥90% id — the megaplasmid backbone is not novel, but the specific combination of that backbone with the Tn3000/blaNDM-1 cargo and the pC39-like replicons may be.

## 14:15 — blaNDM-1 genetic environment (paper Figure 1B)
- Parsed the RefSeq PGAP annotation of positions 300000-315000 on pNDM-1_UCO-361.
- Independent confirmation of every landmark feature the paper lists, in the exact expected order:
  - Tn3-like IS3000 family transposase (304754-307771) — paper's "Tn3000/IS3000 upstream" ✓
  - IS30 family transposase (307848-308099) — paper's ΔISAba125 (ISAba125 IS is in the IS30 family) ✓
  - blaNDM-1 (308200-309012) ✓
  - Ble-MBL (309016-309381) — bleMBL ✓
  - Phosphoribosylanthranilate isomerase (309386-310024) — trpF (EC 5.3.1.24) ✓
  - DsbD domain protein — dsdD-family ✓
  - GroES (311594-311884) ✓
  - GroEL/GroL (311940-313205) ✓

## 14:15 — LLM judge (free Argo proxy)
- POST to `http://127.0.0.1:44497/v1/chat/completions` with the full evidence pack and paper's claims.
- Initial attempt with `argo:claude-opus-4.7` returned HTTP 502 (transient upstream). Retried with `argo:gpt-5.1` (still free via Argo proxy, per project rules).
- Response: `{"verdict":"REPLICATED","coverage_frac":0.9,"agreement_frac":0.98,"one_line":"All genomically testable claims are independently reproduced with only minor annotation-label differences and a clarified, but not contradictory, interpretation of megaplasmid novelty."}`

## 14:16 — Wrote report
- REPORT.md, brief.md, artifact_harvest.md, this attempt_log.md.
- Evidence files copied back from uicgpu → `report/evidence/`.

## What worked
- NCBI E-utils gave complete deposited assembly instantly.
- All required tools (mlst, AMRFinder, Kleborate, blastn) already installed on uicgpu in `amr` and `/data/stevens/envs/kleborate` micromamba envs — no build/setup needed.
- RefSeq PGAP annotation on the plasmid contig covered every gene the paper labels in Figure 1B, so no additional Prokka/Bakta run was needed for the local-environment claim.

## What was blocked / not tested
- **C10 (conjugation phenotype at 27°C, frequency 4.3×10⁻⁶):** wet-lab, not reproducible in silico. Only mechanistic prerequisites (traC, IncFIB(K) tra locus, hns) were verified in the assembly.
- **C11 (first NDM-1 K. pneumoniae in Chile, epidemiological):** would require access to the Chilean ISP surveillance registry.
- **PLSDB mash-dist recomputation:** would require the PLSDB v2 sketch (~GBs). BLAST comparison to the specific reference plasmids cited by the paper was performed instead and gives a stronger, direct measurement.

## What surprised me
- The BVBRC-46 prior run on the same organism was ~1 GB of prior work that I could sanity-check against without depending on. All my independent numbers agree with BVBRC-46's independently.
- The paper's "closest plasmid ... 2488 bp common region" statement significantly understates the true whole-plasmid backbone homology. My BLAST finding (~67% of pNDM-1_UCO361 backbone matches pNDM-1-EC12 at ≥90% id) is an honest refinement — the paper's local blaNDM-1 environment observations all hold, but the broader "novel megaplasmid" framing is best interpreted as novel-in-cargo-context, not novel-in-backbone.
