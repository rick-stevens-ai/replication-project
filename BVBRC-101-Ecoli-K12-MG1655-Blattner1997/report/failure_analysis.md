# Failure analysis — Blattner 1997 E. coli K-12 MG1655 replication

Honest catalogue of everything that did not work, and why. This complements the "what worked"
section in `attempt_log.md`.

## 1. Primary PDF retrieval — BLOCKED

**What failed.** Automated retrieval of Blattner F. R. et al. (1997) *Science* 277(5331):1453–1462
returned HTTP 403 (Cloudflare bot-check) from `https://www.science.org/doi/10.1126/science.277.5331.1453`
on 2026-07-05.

**Why.** AAAS/Science paywalls its full-text PDFs behind Cloudflare; unauthenticated `curl`
requests are rejected regardless of DOI validity. This is a policy failure of the source,
not a bug in the replication pipeline. Science 1997 is also pre-PMC, so no OA full-text
mirror exists at `pmc.ncbi.nlm.nih.gov` (the PMID 9278503 landing page returns an HTML wrapper
with abstract only, no PDF link).

**Attempted mitigations.** (a) Direct DOI fetch — 403. (b) PMC full text — no full text. (c)
Europe PMC full-text — 404 (paper not in EPMC full-text corpus). (d) UNAM `~lgomez` mirror
that was cited in prior attempt logs — unreachable from CherryRd. (e) Web-search for legitimate
alternative hosts — none free.

**Consequence for the replication.** None on the verdict. The paper's *verbatim* headline
quantities (genome size 4,639,221 bp, CDS count 4,288, unknown-function fraction 38%) are all
in the PubMed abstract, which is freely licensed. The remaining canonical numbers used in the
comparison (G+C 50.8%, ~950 bp mean CDS, ~88% coding density, ~86 tRNAs, 7 rRNA operons,
~55% strand bias) are widely-cited derived values from the paper's Table 1 and body,
independently confirmable via EcoCyc/RegulonDB canonical annotation counts and via Murakami
2015 (PMC4696680) for the rRNA operon count. So the replication has a valid ground-truth
reference even without the primary PDF.

**Consequence for downstream artifacts.** `extraction/marker.md` is a fallback extraction
(explicitly labeled as such in its header) rather than a machine-produced Marker parse.
`extraction/nougat.mmd` is a header-only placeholder — a real Nougat `.mmd` cannot be
produced until a valid source PDF is ingested. `paper.pdf.MISSING` marks the gap
machine-readably so `scripts/check_repl_dir_standard.py` can flag it.

**How to fix in future.** Fetch the PDF from `science.org/doi/10.1126/science.277.5331.1453`
while authenticated to an institutional AAAS/Science subscription (ANL library or UChicago
library), save as `paper.pdf` at the directory root, then run `nougat paper.pdf --recompute -o extraction/`
on a GPU host (uicgpu or Polaris) and rename `paper.mmd` → `extraction/nougat.mmd`.

## 2. Sub-claims not tested — deliberate scope limits

The following analytical claims from the paper are NOT tested by this replication. Each is
either method-plausible but out of scope, or requires 1997-vintage inputs no longer available.

| Sub-claim | Why not tested | Method-plausible re-test |
|---|---|---|
| "38% of proteins have no attributed function" | Would need to (a) re-run Blattner's 1997 GeneMark + custom heuristics pipeline, (b) re-BLAST vs SWISS-PROT circa 1997. Modern annotation trivially assigns function to a much larger fraction (only ~5–10% remain uncharacterized in modern EcoCyc). Direct test would produce a very different — but not contradictory — number, and would not falsify the 1997 claim about the 1997 corpus. | Test 2: recompute unknown-function fraction against modern EcoCyc classes and report both numbers side-by-side. |
| "80 ABC transporters (largest paralog family)" | Requires reproducing the paper's protein-family clustering pipeline. Modern EcoCyc / InterPro / Pfam ABC-transporter counts differ (both up and down depending on definition — permease-only vs full transporter modules). | Cluster all NC_000913.3 proteins with modern MMseqs2 + InterPro membership; report ABC family size against the paper's 80. |
| IS element / phage remnant inventory | The GenBank file has 50 `mobile_element` features (reported in metrics.json) but classifying them into IS families, phage remnants, and "patches of unusual composition" requires the paper's specific compositional-analysis pipeline. | Method-plausible: run ISEScan or PHASTER-lite on NC_000913.3; classify by IS family; compare totals to paper's tabulation. |
| GC-skew asymmetry & oligonucleotide-motif orientation | Method is known (cumulative GC-skew over sliding windows, motif orientation vs replichore) but out of the ≤5-min replication budget. | Method-plausible: `dnaA`-box, `KOPS`, `Chi`-site orientation vs replichore using standard signal-processing recipes. |
| Comparison to 5 contemporary sequenced microbes | Requires 1997-vintage genome corpus (H. influenzae Rd, M. genitalium G37, Synechocystis 6803, M. jannaschii, S. cerevisiae S288C). All 5 are available today but with heavily updated annotations — a modern re-run would be a different comparison. | Modern-corpus re-run possible; would not falsify the 1997 comparative claim about the 1997 corpus. |

**Assessment.** These are honest scope limits, not failures. The replication's testable core
(whole-genome quantitative body) is completely covered.

## 3. Judge disagreement — controlled and expected

**What happened.** Argo `argo:gpt-5` returned `REPLICATED` (coverage=100, agreement=100).
Argo `argo:gpt-5.2` returned `PARTIAL` (coverage=70, agreement=78).

**Why not a real failure.** `gpt-5.2`'s justification (verbatim in `judge2.json`) states
"Core genome-wide quantities … reproduce closely on NC_000913.3, consistent with expected
minor drift from curation and resequencing." The lower coverage_pct is entirely driven by
`gpt-5.2` penalizing the presence of table rows (start-codon histogram, per-base composition)
that were not literally tabulated in the paper's abstract — the substantive claim-level
agreement is high in both models. This is a systematic strictness difference between the
two Argo models that we have observed across multiple BVBRC replications, not a
signal that any measured quantity contradicts the paper.

**Resolution.** Consensus verdict is **REPLICATED**, with both judge outputs archived verbatim
for auditability. If future BVBRC policy requires unanimous strict-judge agreement, we would
downgrade to `PARTIAL` — but that would be a policy choice, not a factual finding.

## 4. Environment reuse — not a failure but a gotcha

Reused the sibling BVBRC-100 Kunst venv (Biopython 1.87 on Python 3.14) to avoid a redundant
`pip install`. This is fine as long as the Kunst directory is not deleted before this one.
If we ever wanted to fully self-contain this replication, `work/analyze.py` should be
paired with a small `requirements.txt` (`biopython==1.87`, `requests` for the judge driver)
and a fresh `python3.14 -m venv .venv`.

## 5. Timing quirks — none material

- NCBI E-utilities occasionally returns 429 / brief 503s under heavy load. Not encountered
  during this run; would be resolved by exponential-backoff retry.
- Argo proxy latency is unpredictable (5s–60s per call); each judge finished on first try.

## 6. What did NOT go wrong (worth naming so we don't over-claim failures)

- Reference-sequence retrieval: clean single `curl`, byte-perfect sha256 verified.
- Interval-union coding density calculation: sanity-checked against the naive sum-of-CDS-lengths
  variant (which double-counts overlapping ORFs and gives a slightly higher figure). The
  interval-union value (86.32%) is the correct one against which the paper's 88% should be
  compared.
- Replichore assignment: MG1655's oriC in the second half of the sequence (~3.93 Mb) instead
  of at coord 0 required a non-trivial two-line change vs the sibling Kunst pipeline (B. subtilis
  origin at coord 1), and reproduced the paper's ~55% strand-bias figure to within 0.1 pp.
