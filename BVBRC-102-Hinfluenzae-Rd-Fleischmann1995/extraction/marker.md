# Marker extraction — pending

**Paper:** Fleischmann R. D. et al. (1995). "Whole-genome random sequencing and assembly of *Haemophilus influenzae* Rd." *Science* **269**(5223):496–512. doi:10.1126/science.7542800. PMID 7542800.

**Status:** PENDING — paper.pdf could not be obtained.

**Reason:** Unpaywall lookup (2026-07-05) for DOI `10.1126/science.7542800` returned
`is_oa: false, oa_status: closed, best_oa_location: null, has_repository_copy: false`.
No open-access copy exists in any repository (no PMC record for this 1995 Science article;
Science/AAAS content from 1995 remains paywalled and no author manuscript was self-archived).
BACKFILL rule caps PDF fetch at 90 s and forbids paid endpoints — moved on.

**How to fill later:**
1. Institutional Science subscription: fetch PDF, drop as `paper.pdf`, then run Marker
   (`marker_single paper.pdf --out extraction/marker.md`) on a CPU host.
2. Interlibrary loan / Argonne Research Library retrieval of the scanned PDF.
3. Optionally digitize from a hard-copy Science 1995 volume (JGI/Argonne stacks).

**Non-blocker for this replication:** The paper's numerical claims (chromosome length, G+C, CDS/tRNA/rRNA counts, operon count, topology) are extensively re-tabulated in secondary sources (GenBank flatfile header for L42023 → NC_000907.1, RefSeq record notes, the paper's abstract, the Fleischmann Wikipedia summary, and the BV-BRC genome page for genome_id 71421.1). All quantitative comparisons in this replication were made against the paper's abstract / Table 1 values that are widely re-quoted verbatim across all of those sources; the numeric backbone of the replication does not depend on having the PDF in hand.
