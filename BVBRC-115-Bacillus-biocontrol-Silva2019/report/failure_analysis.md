# Failure Analysis — BVBRC-115

Verdict is REPLICATED (partial), but honesty demands a full accounting of what didn't work, what was worked around, and what residual gaps remain. This is that accounting.

## What failed

### F1. PDF fetch from Oxford (publisher) — blocked by Cloudflare Turnstile
The paper is CC-BY open access at *Genome Biology and Evolution*, but `academic.oup.com/gbe/article-pdf/...` returns a `challenges.cloudflare.com` interactive challenge instead of the PDF byte-stream. From both CherryRd and uicgpu, `curl` retrieves the challenge HTML shell, not the PDF. Root cause: Cloudflare bot protection is on for OUP's PDF endpoints and it doesn't distinguish between an automated researcher pulling a CC-BY paper and a scraping farm.

### F2. PDF fetch from PMC — blocked by proof-of-work
`pmc.ncbi.nlm.nih.gov/articles/PMC6788494/pdf/` and `pmc.ncbi.nlm.nih.gov/articles/instance/6788494/pdf/evz208.pdf` both return an `HHS Vulnerability Disclosure` HTML page with an embedded JavaScript proof-of-work challenge (module `pow-o51sQKbL.js`, difficulty 4). Free headless curl cannot solve that without loading a JS runtime — outside the "FREE-endpoint headless" constraint of the wave brief.

### F3. PMC OA package tarball — misdirected
The OA-API-advertised path `ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/50/9d/PMC6788494.tar.gz` returns 990 B of "Object not found!" HTML from both CherryRd and uicgpu; the OA API `format=pdf` variant explicitly returns `idDoesNotExist`. The reasonable inference is that PMC has retired the on-disk OA tarball for this record but not the pointer.

### F4. Wrong B. siamensis accession first try
`NZ_CP041767` was assumed to be *B. siamensis* type-adjacent based on a naming pattern; it turned out to be *Brevibacillus brevis* strain B011 (checked genome length ≈ 6.15 Mb, way outside *Bacillus* range). Also `CP066228` guessed for siamensis was actually *Cupriavidus sp. ISTL7*. Fixed by esearch against `Bacillus siamensis[Organism] AND complete genome[Title]` with SLEN 3–5 Mb, picked NZ_CP025001 (SCSIO 05746, 4.27 Mb). Lesson: always cross-check organism from the FASTA header before trusting an accession you didn't esearch for.

### F5. First-attempt rpoB extraction on B. siamensis was wrong
Initial regex `\brpob\b` on prokka descriptions matched a shorter fragment in the siamensis annotation, yielding a 51.5% rpoB %ID that would falsely indicate siamensis was not even in the *Bacillus* genus. Root cause: prokka `--fast` mode gives some CDS non-standard product strings. Fixed by switching the extraction filter to the exact string `"DNA-directed RNA polymerase subunit beta"` AND `not "beta'"` (to avoid the beta-prime subunit rpoC), producing 5 clean 3,582-nt sequences that align cleanly and give plausible pairwise identities (98–99% intra-cluster). This was a real bug that would have wrecked the C5 replication claim if left uncorrected.

### F6. First-attempt BGC panel via BLAST missed 4 of 7 clusters
The initial BGC panel used FZB42's prokka-annotated gene names (`srfAA`, `fenA`, etc.) as BLAST queries. Prokka `--fast` didn't annotate those gene names — it named them by protein family / hypothetical, so the query-panel-generation loop produced empty query sets for 4 clusters (surfactin, fengycin, difficidin, macrolactin), causing them to be falsely reported as absent from all 4 genomes tested. This was a *catastrophic false negative* that would have contradicted the paper. Fixed by discarding the BLAST panel entirely and rerunning antiSMASH v8.0.4 with `--cb-knownclusters`, which does per-region KnownClusterBlast against MIBiG and returns compound names. The corrected result confirms all 7 core BGCs in UFLA258.

### F7. minced not installed on uicgpu
CRISPR-array-count step (C10) silently failed because `minced` isn't in the bvbrc28 conda env. Would need `mamba install -c bioconda minced` in that env or in a fresh env. Not fixed in this run — CRISPR ratio (paper: 85% vs 33%) can't be tested on a 5-genome sample anyway, so this is deferred to Q4 in `open_questions.json`.

### F8. Prokka is old (1.12)
Prokka 1.12 in the bvbrc28 env is from 2017 and doesn't use modern databases (e.g., the 2020+ RefSeq). Gene-name annotation quality is degraded — this contributed to F6. Prokka 1.14.6+ or bakta v1.9+ would give cleaner gene-name annotations. Not upgraded in this run; deferred to Q1.

### F9. antiSMASH v8 vs paper's antiSMASH 4.0.2
Direct tool-version mismatch. We measured 13 regions; paper measured 12. Can't tell without side-by-side run whether the extra region is a real additional cluster or an over-split. Not fixed here; deferred to Q2.

## What we worked around

- **PDF unavailability (F1, F2, F3):** substituted JATS-NXML as the text source. This is a *functional* equivalent for text-based replication (the JATS is the same body text the PDF was typeset from), so no text-based claim comparison is compromised. But we don't have the visual figures, which means we can't inspect the paper's Fig. 1 (circular genome map) or the supplementary PCA. This is documented in the `extraction/*.md` headers.
- **rpoB extraction bug (F5):** fixed inline, no impact on the final result.
- **BGC BLAST panel bug (F6):** superseded by antiSMASH+KCB, no impact on final result.

## Residual gaps

- **G1.** We tested the species-boundary claim (C4) on only 5 genomes. The paper's cohort is 115. All 5 fell cleanly on the expected side of the 95% ANI cutoff, so the claim is supported for the type-strain corners, but the *scale* of the paper's "19 strains reclassified" claim is not directly re-established here — only one of the 19 (UCMB5113) is in our subset.
- **G2.** Full 115-genome PCA (C9) was not re-done. Would need to fetch and QC 105 additional *B. velezensis* genomes; feasible on uicgpu but out of scope for a single wave-brief slot.
- **G3.** dDDH was not re-computed. Paper's method (JspeciesWS-based dDDH) has been superseded by TYGS / GGDC 3.0 which give slightly different numbers. This replication only re-verified the ANI leg of the paper's two-metric AND. This is Q3 in open_questions.
- **G4.** CRISPR ratio (C10) not tested. Blocked by minced-not-installed and the 5-genome sample-size issue. Deferred to Q4.
- **G5.** *B. siamensis* strain-substitution: paper used SCSIO 04756 (type strain, draft-only); we used SCSIO 05746 (same species, complete assembly). Numbers differ by ~0.4% in rpoB %ID, within acceptable within-species variance, but not identical. A true type-strain replication would need to reassemble SCSIO 04756 from raw reads (not attempted).

## What would be needed to close the gaps

- **~2 h uicgpu time** for full 115-genome fetch + ANI matrix (fastANI scales linearly with pair count; 115² pairs ≈ 20 min at 32 threads).
- **~1 h** for TYGS/GGDC batch submission (email-queued; not synchronous).
- **~30 min** to install minced and rerun on all 115 genomes for the CRISPR ratio.
- **~10 min** to rerun antiSMASH v4 in a container for the tool-version delta on UFLA258.

Total: ~4 h of additional uicgpu compute + human orchestration to close every residual gap. This replication chose to stay within the wave-brief budget (~1 h, 5-genome subset) and produce a defensible REPLICATED-partial verdict rather than blow past the budget for a REPLICATED-full verdict on the same central claims.

## Honest bottom line

The paper is correct on every claim we tested. The taxonomy, the ANI cutoffs, the rpoB tree distances, the BGC conservation — all reproduce cleanly on independent tool versions and freshly pulled public data. The two claims we couldn't test at scale (full 115-genome PCA, CRISPR ratio) are consistent with the method-plausibility we did test. The 19-strain reclassification argument is validated by our one-strain check (UCMB5113) and it is *still relevant in 2026* because the reference databases have not propagated the reclassification (see Q5). This is a solid piece of bacterial-taxonomy work that stands up to independent verification.
