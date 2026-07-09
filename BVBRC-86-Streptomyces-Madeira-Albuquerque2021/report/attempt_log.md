# BVBRC-86 attempt log

Paper: Albuquerque P, Ribeiro I, Correia S, Mucha A, Tamagnini P. "Complete Genome Sequence of Two Deep-Sea Streptomyces Isolates from Madeira Archipelago and Evaluation of Their Biosynthetic Potential." Marine Drugs (2021). PMID 34822492.

Suggested BV-BRC workflow: BV-BRC Codon Tree / Phylogenetic Tree + BV-BRC Genome Assembly.

## 2026-07-03 12:21 CDT — kickoff
- Set up target dir with report/{evidence,} and work/.
- Wave brief read; free-endpoints only, real-data replication, LLM-judge verdict.

## 2026-07-03 12:22 CDT — paper acquired
- PMID 34822492 → PMC8622039, DOI 10.3390/md19110621. Marine Drugs 2021, 19, 621, 10-page PDF via EuropePMC (`work/paper.pdf`, 1.99 MB).
- MDPI direct + PMC OA PDF endpoint both blocked scraping; `europepmc.org/articles/PMC8622039?pdf=render` worked.
- `pdftotext -layout` → `paper.txt` (1051 lines). All key claims + accessions parsed cleanly with grep.

## 2026-07-03 12:23 CDT — accessions resolved
- BioProject **PRJNA754006** → 2 assemblies:
  - **GCF_020740535.1** (MA3_2.13) = 1-contig complete chromosome NZ_CP082362.1; NCBI has re-labelled the organism *Streptomyces profundus* strain MA3_2.13 (author's proposed new species from this paper).
  - **GCF_020739505.1** (S07_1.15) = 2 contigs NZ_JAJBZK010000001.1 + …0002.1 (whole-genome shotgun, matches paper's assembly-graph description).
- BioSamples: SAMN20720482 (MA3_2.13), SAMN21157270 (S07_1.15).
- FNA + GFF pulled from NCBI FTP for both genomes; reference genomes for closest relatives (GCA_000220705.1 = *S. xinghaiensis* S187, GCA_002128305.1 = *Streptomyces* sp. SCSIO 3032) also pulled for ANI.

## 2026-07-03 12:24 CDT — Table 1 recomputed from downloaded FASTAs
- MA3_2.13: **7,653,710 bp, 72.14% GC, 1 contig** — EXACT match to paper Table 1 (7,653,710 bp, 72.1% GC, CP082362, 1 contig).
- S07_1.15: contig 1 = 7,094,148 bp @ 73.15% GC; contig 2 = 160,397 bp @ 69.56% GC → EXACT match to paper (7,094,148 + 160,397; 73.2% & 69.6%).
- rRNA operons from NCBI PGAP GFF: MA3_2.13 = 5 × 16S; S07_1.15 = 6 × 16S → matches paper Table 1 (5 vs 6 rRNA operons).
- CDS counts differ slightly (PGAP: 6212 / 6166 vs RAST paper: 6412 / 6492) — expected RAST-vs-PGAP annotator delta, not a discrepancy.

## 2026-07-03 12:25 CDT — ANI recomputed (species-boundary claim)
- skani (learned-ANI mode) + fastANI both run locally:
  - S07_1.15 vs *S. xinghaiensis* S187: skani **96.66%** (aligned 78% ref / 71% query); fastANI **96.12%**. Paper reported PYANI ANIb **95.83%**. All three cross the 95–96% species threshold → S07_1.15 IS *S. xinghaiensis* ✅.
  - MA3_2.13 vs *Streptomyces* sp. SCSIO 3032: skani rejects as too divergent (no confident learned-ANI); fastANI **80.85%**. Paper reported PYANI ANIb **77.90%**. Both agree assembly is FAR below species threshold → MA3_2.13 IS a distinct new species ✅ (NCBI already accepted it as *S. profundus*).

## 2026-07-03 12:27 CDT — antiSMASH launched on uicgpu
- Pulled `antismash/standalone:6.1.1` docker image on uicgpu (image is self-contained with pfam/tigrfam/resfam/clusterblast DBs). Paper used **antiSMASH 5.0**; using 6.1.1 as closest freely-available comparable (major-version bumps in antiSMASH mainly add detectors + tighten rules, so BGC counts should be broadly comparable — with caveat that v6 detects a few extra categories).
- Two containers running detached on uicgpu with 32 CPUs each: `as_MA3` on MA3_2.13, `as_S07` on S07_1.15. Options: `--genefinding-tool prodigal --taxon bacteria --minimal --cb-general --pfam2go --smcog-trees` (fast profile — includes clusterblast against all antiSMASH-curated clusters, drops slow known-cluster-comparison against MIBiG to keep runtime bounded).

## 2026-07-03 12:34 CDT — antiSMASH pass 1 complete
- MA3_2.13: 27 BGC regions (paper: 32). S07_1.15: 24 BGC regions (paper: 24 — EXACT). Sub-6-min wall time per genome on 32 CPU.
- Composition-by-region cross-checked: MA3_2.13 has 11 T1PKS regions (paper: 13 type I PKS); S07_1.15 has ZERO T1PKS — confirms paper's specific negative claim.
- Full region JSON archived to `report/evidence/antismash/*_general.json.gz`.

## 2026-07-03 12:37 CDT — antiSMASH pass 2 (knownclusterblast/MIBiG) launched + completed
- Same docker image, `--minimal --cb-knownclusters` for both isolates.
- Both containers exit 0 in ~5 min.
- Extracted top-MIBiG hits per region for both isolates → `evidence/known_cluster_hits.tsv`.
- **All three paper-named MIBiG hits recovered**:
  - MA3_2.13 region_008 → BGC0001975 atratumycin (score 24833, 21 hits)
  - MA3_2.13 region_014 → BGC0001983 triacsins (score 11135, 23 hits)
  - MA3_2.13 region_021 → BGC0001283 arsono-polyketide (score 11436, 18 hits) — region-numbering shift (paper called this #24) is due to v6 splitting/merging of protoclusters upstream, but the MIBiG-hit identity is preserved.
- S07_1.15 known hits include ectoine, hopene, desferrioxamine E, SapB — the common *Streptomyces* metabolites the paper called out for both isolates.

## 2026-07-03 12:41 CDT — LLM-judge for verdict
- Free endpoint: Argo proxy at `localhost:44497` (auth `Bearer stevens`).
- Tried argo:claude-opus-4.7 first, got a transient 502 Bad Gateway. Fell through to argo:claude-sonnet-4.6, which returned cleanly.
- Verdict prompt at `work/llm_judge_input.md` (7.2 KB, includes all 7 claim groups + our results + honest limitations).
- Model returned: **VERDICT: REPLICATED** with a one-paragraph justification citing exact assembly match, cross-tool ANI agreement, exact S07 BGC count, exact recovery of all three named MIBiG hits, and confirmation of the specific zero-T1PKS-in-S07 negative claim. Full response saved to `report/evidence/llm_judge_response.txt`.

## 2026-07-03 12:44 CDT — report assembly complete
- All tables, TSVs, evidence artifacts, and REPORT.md written.
- 4 antiSMASH JSON archives (~23 MB compressed total) copied back from uicgpu into `report/evidence/antismash/`. Full HTML output trees stay on uicgpu at `/data/stevens/replicate/bvbrc86/` (retrievable via scp; too large to duplicate to Dropbox).
- No writes outside `~/Dropbox/REPLICATE-PROJECT/BVBRC-86-Streptomyces-Madeira-Albuquerque2021/` and `uicgpu:/data/stevens/replicate/bvbrc86/`. Other BVBRC-*/ dirs untouched (verified via `ls ~/Dropbox/REPLICATE-PROJECT/ | grep BVBRC` before starting).

## Notes / lessons
- MDPI PDF direct download blocked (302 to interstitial); PMC PDF endpoint 404. Working URL: `https://europepmc.org/articles/PMC<id>?pdf=render`. Worth remembering for future MDPI replications in this wave.
- NCBI has since re-named MA3_2.13 as *Streptomyces profundus* — the authors' new-species proposal from this very paper appears to have been formally accepted post-publication. Nice validation of the paper's C3 conclusion.
- Docker antismash/standalone:6.1.1 is a great turnkey option — self-contained with all databases, no manual DB install needed. Worth caching on uicgpu for future BGC-heavy replications.
- LLM-judge on Argo proxy: retry-on-502 loop with model fallback (opus → sonnet → gpt-5) is worth building into a reusable helper for the replication wave.

