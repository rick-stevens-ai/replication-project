# Marker parse — PENDING

**Status:** pending central corpus parse.

**Paper:**
- Harmer CJ, Lebreton F, Stam J, McGann PT, Hall RM. "Complete genome of the extensively
  antibiotic-resistant GC1 *Acinetobacter baumannii* isolate MRSN 56 reveals a novel route to
  fluoroquinolone resistance." *J Antimicrob Chemother* 77(7):1851-1855, 2022.
- **DOI:** 10.1093/jac/dkac115
- **PMID:** 35403193
- **PMCID:** PMC9244215
- **Semantic Scholar paperId:** b43c132b5dd2c5d3b00089bc784354c3c1f7302e

**Why pending.** During the 2026-07-05 backfill pass we did NOT successfully materialize a raw
PDF within the 90 s fetch cap:
- Publisher PDF at `https://academic.oup.com/jac/article-pdf/77/7/1851/44373670/dkac115.pdf` returned
  an HTML challenge page rather than PDF bytes when fetched non-interactively (OUP anti-bot).
- Europe PMC render endpoint returned an HTTP/2 STREAM_CLOSED error.
- The NCBI PMC per-article gate at `pmc.ncbi.nlm.nih.gov/articles/PMC9244215/pdf/dkac115.pdf`
  returned a 1.8 KB "Preparing to download" HTML gate page rather than PDF bytes.
- The paper is NOT present in the central Eagle Marker corpus at
  `/eagle/projects/AuroraGPT/stevens/scout_corpus/md/` (grep for `MRSN 56 | dkac115 | Harmer` on
  all 520 files returned no match). Not present in `/eagle/projects/AuroraGPT/stevens/osti_marker/md/`
  either.

**Fill instructions for a later sweep.**
1. Manually download `dkac115.pdf` from the OUP link above OR from PMC9244215 (open access, CC-BY)
   in an interactive browser session.
2. Place at `<dir>/paper.pdf`.
3. Run `marker_single paper.pdf --output_dir extraction/ --output_format markdown` and rename to
   `extraction/marker.md`.
4. Delete this pending stub.

**What replaces this file for the replication.** The replication team re-read the paper via
(a) the NCBI PubMed abstract (fetched 2026-07-05 via eutils `esummary` for PMID 35403193),
(b) the paper's own GenBank submission metadata for chromosome CP090606.1 + plasmids
CP080453..CP080456 (which encodes the authors' claimed AbaR28 / Tn2006 / Tn7 / Tn7+ / gyrA /
marR annotations directly in the GenBank feature table), and (c) the paper's per-claim
predictions transcribed into `report/REPORT.tex` and `report/REPORT.md`. All 7 core claims in
this replication are stated verbatim from the paper's abstract + featured novel-mechanism text.
