# Failure Analysis — BVBRC-01-CRKP-Zhang2022

Honest post-mortem on what failed, what was worked around, what remains a residual gap, and
what would be required to close each gap. Also contains the honest critique of evidence
strength (Rick's 2026-07-05 explicit requirement: no rubber-stamping).

Verdict remained **REPLICATED** across the backfill, but the verdict applies to
descriptive epidemiology and the KL47→KL64 finding — NOT to the paper's proposed
mechanism (wzc recombination, C18) nor its phylogenetic clade architecture (C20).

## Explicit failures (things that didn't work as intended)

### F1. Claim C12 (blood as predominant sample source, 31.09%) — NOT TESTED
- **Failure:** Could not replicate the paper's basic descriptive claim about sample-source
  distribution.
- **Root cause:** BV-BRC's `body_sample_site` metadata field is empty for 92% of K. pneumoniae
  records. This is a database-side missing-data problem, not a code failure.
- **Workaround:** None available at BV-BRC layer.
- **Residual gap:** The paper's whole inclusion criterion (8 specific human sample sources)
  cannot be applied to our 2026 pull; hence 955 ST11 CRKP vs paper's 386.
- **To close:** Scrape isolation-source from NCBI BioSample for each genome accession via
  Entrez efetch (see Open Question Q3 next_steps). Estimated ~4 h wall-clock for 955 records
  with NCBI rate limits.

### F2. Claim C18 (wzc CD1-VR2-CD2 ~303bp longer in KL64) — NOT TESTED
- **Failure:** The paper's proposed causal mechanism for the KL47→KL64 transition was
  never actually tested in the replication.
- **Root cause:** Kleborate labels a K-locus by mapping short reads to reference cps
  cassettes; it does not report a length measurement of the wzc VR2 insertion. Testing C18
  requires targeted BLASTn alignment of wzc between representative KL47 and KL64 assemblies.
- **Workaround:** We noted the paper's claim in the report and marked it NOT TESTED. We did
  NOT try to gloss over this by proxying with a K-locus-count difference (which would be
  circular reasoning).
- **Residual gap:** The largest single mechanistic claim of the paper is unverified here.
- **To close:** Extract wzc CDS regions from ~20 KL47 and ~20 KL64 assemblies (already on
  uicgpu), run BLASTn against a K. pneumoniae wzc reference (e.g., from NC_016845.1),
  measure CD1-VR2-CD2 span, and compute the KL64-minus-KL47 length delta. Expected wall-clock
  ~2 h. Also see Open Question Q1.

### F3. Claim C20 (9 phylogenetic clades) — TESTED AS PROXY ONLY
- **Failure:** Real phylogenetic replication (Roary + IQ-TREE/RAxML-ng) was not run;
  substituted with a 27-way ST+K-locus co-occurrence table.
- **Root cause:** Time budget in Phase 2 (~1 h wall-clock for Kleborate) did not include the
  ~12 h wall-clock a Roary+IQ-TREE run would need on 955 assemblies.
- **Workaround:** We reported "27 ST+KL combinations" as PARTIAL and were explicit in the
  report that this is not a phylogenetic tree.
- **Residual gap:** Cannot confirm or refute the "9 clades" number; cannot distinguish
  clonal expansion from repeated conversion of KL47→KL64 (Open Question Q1).
- **To close:** Standard Roary → snp-sites → IQ-TREE pipeline on uicgpu. Roughly 12 h
  wall-clock, 200–500 GB RAM (fits on uicgpu 2 TB). Also see Open Question Q1.

### F4. Claim C17 (35 differentially carried virulence genes, p<0.05) — MISLABELED AS PARTIAL
- **Failure:** We reported C17 as PARTIAL on the strength of Kleborate locus-level agreement,
  but Kleborate does NOT enumerate individual VFDB genes and cannot produce a 35-gene count.
- **Root cause:** Tool substitution — we swapped Abricate+VFDB (paper's approach) for
  Kleborate virulence modules (our approach) without noting the granularity mismatch.
- **Workaround:** None applied at the time; called out here in retrospect.
- **Residual gap:** The 35 count itself is untested; only the direction (KL64 > KL47 on
  hypervirulence loci) is verified.
- **To close:** Run Abricate v1.0+ with VFDB v2024 on the 955 assemblies (~30 min wall-clock
  on uicgpu), do per-gene Fisher's exact tests, count how many reach p<0.05.

### F5. Tool version drift (Kleborate v2.x → v3.2.4) — NOT AUDITED
- **Failure:** We used Kleborate v3.2.4; the paper used v2.x. Kaptive database has been
  rebuilt in v3. Some K-locus classifications may differ between versions.
- **Root cause:** No side-by-side v2 vs v3 audit was performed.
- **Workaround:** Acknowledged as a caveat in the discussion.
- **Residual gap:** C13 (51 vs 19 serotypes) may be partly a v2→v3 taxonomic re-lumping
  artifact rather than a real reduction in diversity.
- **To close:** Install Kleborate v2.x in a parallel conda env; run on a random 100-genome
  subsample; compute K-locus concordance rate. ~1 h wall-clock.

### F6. Statistical significance testing — NOT COMPUTED
- **Failure:** The paper reports χ² and Fisher's exact p-values throughout Tables 2 and 3.
  We reported percentages and percentage-point differences but no p-values.
- **Root cause:** Scope-choice — we prioritized coverage (18/20 claims tested) over
  inferential rigor.
- **Workaround:** None; effects are large enough that most would be highly significant
  (e.g., rmpA 29.1% vs 2.3% on n=218/n=413 is essentially certain).
- **Residual gap:** Statement "KL64 vscore = 2.06 vs KL47 = 1.80" lacks a p-value; a
  reviewer would ask for one.
- **To close:** ~1 h of Python + scipy.stats work over `analysis/kleborate/kleborate_results_all.tsv`.

### F7. PDF fetch — first three URL patterns failed
- **Failure:** MDPI `/pdf/` URL returns HTTP 403 Access Denied via Edge; `/pdf?version=...`
  also 403; the article-page URL returned HTML not PDF.
- **Root cause:** MDPI edge blocks non-browser User-Agent + certain URL patterns.
- **Workaround:** Fourth attempt via `https://res.mdpi.com/d_attachment/genes/genes-13-01624/article_deploy/genes-13-01624.pdf`
  succeeded (1.52 MB, 10 pages, PDF v1.7). Standing lesson for future MDPI fetches: skip
  `/pdf/` and go straight to `res.mdpi.com/d_attachment/...`.
- **Residual gap:** None.

### F8. Central Marker/Nougat corpus miss
- **Failure:** sha256 `a5b493...53df` not found in the SCOUT/OSTI corpus manifests on Eagle.
- **Root cause:** Never parsed centrally.
- **Workaround:** pdftotext -layout for marker.md; nougat.mmd stub with sha256 recorded for
  later corpus sweep.
- **Residual gap:** No Nougat mathematical/table extraction available (though this paper
  has no equations and only handful of simple tables, so the loss is minimal).
- **To close:** Add sha256 to the next Polaris/Eagle Nougat batch.

## Honest critique of evidence strength (per Rick's 2026-07-05 requirement)

The Phase 1+2 REPORT.md is written in a broadly celebratory tone: "central novel finding
strongly verified", "unambiguously replicated", "18/20 tested = 90%". A more sober read of
the same evidence is:

1. **The signal is real, but the mechanism is asserted, not tested.** The KL47→KL64
   epidemiological transition (C14) is genuinely reproduced with high confidence — same
   direction, same crossover year (2016), same virulence-loci enrichment pattern. But the
   *mechanistic* story the paper tells (wzc CD1-VR2-CD2 recombination causes the transition
   via serotype-switch, C18) was neither tested by us nor experimentally demonstrated by the
   paper itself (the paper explicitly lists this as a limitation). Calling the replication
   REPLICATED for the epidemiology is correct; the reader should not conclude that the
   mechanism has been replicated.

2. **Selection bias is under-controlled on both sides.** The paper's 386-genome set is a
   selection from PATRIC 2022 with an 8-sample-source filter that we cannot recreate. Our
   955-genome set is a superset with 92% missing sample-source metadata. Neither dataset is
   a random probability sample of the world's ST11 CRKP; both are convenience samples of
   what got sequenced and deposited. Any absolute-fraction claim (blood at 31.09%, KL64 at
   47.06%) must be read with this caveat. Our replication should have made this louder.

3. **Database growth is a real confounder, not just a numerical inconvenience.** BV-BRC
   grew ~2.5× for ST11 CRKP between the paper's 2022 snapshot and our 2026 pull. If the
   new submissions are systematically biased toward large Chinese KL64 outbreak studies (a
   plausible but untested hypothesis), then our KL64 proportions are inflated in a
   direction that makes the paper look more right than it should. We papered over this by
   calling absolute-count differences "partial (database growth)" but a more rigorous
   framing is "we cannot separate database-growth from a real trend without a
   pre-2022-only counterfactual" (see Open Question Q5).

4. **Tool substitutions were not audited.** Kleborate v3 vs v2 (F5) and Kleborate virulence
   modules vs Abricate+VFDB (F4) are both meaningful methodological differences that could
   independently produce percentage-level shifts in the numbers. We used the newer/simpler
   tool and reported directional agreement; we did not verify that the two tool chains
   produce equivalent results on the paper's exact 386-genome set.

5. **Phylogeny is missing entirely (F3).** The paper's Figures 3–5 and Section 3.4 are the
   most computationally demanding parts of the paper. We tested them via a shortcut
   (ST+KL co-occurrence, 27 combinations) that a phylogeneticist would not accept as a
   substitute for a real tree. The "9 phylogenetic clades" claim is essentially untested.

6. **Statistical claims are asserted from percentages, not tested (F6).** No p-values were
   computed on our side. The paper's specific numeric claims (e.g., "χ² = 47.497,
   p < 0.001 for rmpA" from Table 3) were not independently verified.

## What this replication IS good evidence for
- The paper's descriptive epidemiology (year, country, carbapenemase distribution) is
  reproducible on 2026 BV-BRC data.
- The KL47→KL64 transition is real, has the right crossover year, and is not an artifact
  of the paper's inclusion criteria — it holds on a 2.5× larger dataset without the
  sample-source filter.
- The direction (KL64 > KL47 on hypervirulence loci: rmpA, clb, iuc) is real and
  reproducible with an independent tool chain.

## What this replication IS NOT good evidence for
- That wzc CD1-VR2-CD2 recombination causes the KL47→KL64 transition (C18 untested).
- That ST11 CRKP breaks into exactly 9 phylogenetic clades (C20 proxy only).
- That 35 individual VFDB virulence genes are differentially carried at p<0.05 (C17 tested
  at locus, not gene, level).
- That the trend has held or reversed post-2020 (only n=14 for 2020, no post-2020 data).
- That the effect is not driven by Chinese hospital-network founder effects (never
  stratified by country).

## Suggested downgrade if the reader wants a strict verdict
- **Epidemiology + KL47→KL64 crossover:** REPLICATED (strong).
- **Virulence-locus differential (KL64 > KL47):** REPLICATED (strong, direction only).
- **Individual-gene virulence differences (C17):** PARTIAL at best.
- **wzc mechanism (C18):** NOT REPLICATED (never tested).
- **Phylogenetic architecture (C20):** NOT REPLICATED (proxied only).
- Overall verdict remains REPLICATED because 18/20 claims were tested and the paper's
  central novel claim (KL47→KL64) is verified — but the reader should not extend that
  verdict to the mechanistic (C18) or phylogenetic (C20) portions.
