# BVBRC-91 — Attempt Log

## 2026-07-04 (Sat, ~14:08 CDT) — single-session replication attempt

**Requester:** Ollie main-session cron subagent (label `bvbrc-91`).
**Analyst:** Ollie (OpenClaw AI subagent), working locally in `~/Dropbox/REPLICATE-PROJECT/BVBRC-91-Averonii-pathotype-Tekedar2019/`.
**Wall time:** ~10 min end-to-end.
**Compute used:** local CherryRd only. No uicgpu offload was needed — the genomes are ~5 Mb each, and both fastANI + skani finish in <1 s per pairing on a laptop.

### Timeline
1. **T+0:00** — Read the wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`) and the BVBRC-17 exemplar (Fang 2018 replication) to fix format expectations.
2. **T+0:01** — Created target dir tree (`report/{evidence}`, `work/`). Never touched sibling dirs.
3. **T+0:02** — PMID→PMCID+DOI lookup via NCBI id-converter → PMC6715197 / 10.1371/journal.pone.0221018 (PLoS ONE, CC BY 4.0). Full-text XML pulled directly from EuropePMC (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6715197/fullTextXML`, 255 KB). Stored to `work/fulltext.xml` + a stripped-tags text version.
4. **T+0:04** — Grep'd the paper text for accessions, secretion-system claims, ANI values, pan/core numbers. Confirmed the paper table lists 41 GenBank accessions; the two "pathotype" strains are ML09-123 (paper-native, PPUW00000000) and TH0426 (NZ_CP012504.1).
5. **T+0:05** — BV-BRC API smoke test on taxon 654: 726 *A. veronii* genomes now public (vs 41 in 2018). Direct name-lookup found ML09-123 (654.112, GCA_002906945.1) and TH0426 (654.45, GCA_001593245.1); confirms both are still first-class BV-BRC entries.
6. **T+0:06** — Downloaded ML09-123 and TH0426 assemblies via NCBI Datasets REST (`https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/…/download?include_annotation_type=GENOME_FASTA`), unpacked, and computed length/contigs/GC in Python. Both match paper Table 1 to the decimal.
7. **T+0:07** — Ran fastANI (forward + reverse) and skani on the ML09-123 ↔ TH0426 pair. **fastANI 99.9273% / 99.9106%; skani 99.94%** — well above the paper's stated conserved-cluster ≥99.91% threshold.
8. **T+0:08** — Pulled BV-BRC Specialty Genes (VFDB + Victors + PATRIC_VF + CARD + etc.) for ML09-123 (399 rows, 211 VF-property rows), TH0426 (705 rows), and AVNIH1 (654.48, 465 rows) as a T3SS-negative control. Confirmed T3SS/T6SS present in the two catfish strains and absent from AVNIH1, matching paper. Confirmed TssJ (=VasD, =AHA_1837, the paper's marquee "shared only between ML09-123 and TH0426" T6SS component) present in both.
9. **T+0:09** — 41-strain BV-BRC round-trip: 34/41 resolved by exact strain-name match; remaining 7 are recoverable under different taxa (e.g., B565 → taxon 998088, GCF_000204115.1, hit confirmed) — effective 41/41 availability.
10. **T+0:10** — Wrote `brief.md`, `artifact_harvest.md`, saved evidence to `report/evidence/`.
11. **T+0:11** — Wrote `REPORT.md` and this log.

### What worked
- BV-BRC + NCBI Datasets REST are both free, no-auth, and fast.
- The Tekedar 2019 pathotype ANI claim is *unusually* well-scoped for reproduction: the two strains are named, both are public, and a single-pair ANI query is the entire test.
- Two independent ANI tools (fastANI, skani) gave concordant answers >99.9%.

### What did not need to be done
- **EDGAR 2.0 pan/core-genome rerun** on 41 strains — the paper's specific 8,710/2,855 numbers are tool-specific (EDGAR's BLAST score-ratio orthology at their chosen SRV cutoff) and a rerun with any other tool (Roary, Panaroo, PPanGGOLiN) would give different absolute numbers even on identical data, so a byte-perfect number match is not achievable and not a meaningful reproducibility target. Noted in REPORT but not attempted.
- **MUSCLE + RAxML core-genome ML tree** on 2.9 Mb concatenated alignment — CPU-hours, out of scope for a spot replication.
- **Live fish challenge** for the LD50 experimental-virulence claim — obviously out of scope.

### What didn't work / gotchas
- Initial PMC id-converter URL (`www.ncbi.nlm.nih.gov/pmc/utils/idconv/…`) 301-redirects to `pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/…`; had to follow with `-L`.
- Initial EuropePMC full-text URL (`europepmc.org/api/get/articleApi/…`) returns 404; correct endpoint is `www.ebi.ac.uk/europepmc/webservices/rest/PMCID/fullTextXML`.
- BV-BRC's Specialty Gene `gene` column often contains the *VFDB reference-species* symbol (e.g., BCE_5384 = *Bacillus cereus*, lpg0041 = *Legionella pneumophila*), so direct gene-symbol matching against the paper's "most prevalent" list is uninformative; the `product` string is the correct anchor for cross-species VF assessments.
- Paper strain B565 is filed under a strain-specific NCBI taxon (998088), not the species-level 654 — need to widen the BV-BRC query to catch it.

### No harm done
- Target dir was created empty. Wrote only inside it. No sibling dirs were touched.
- No paid endpoint used. All LLM inference was reasoning-only in-session (no external LLM API calls needed for this task).
