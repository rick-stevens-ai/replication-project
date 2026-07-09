# Failure analysis — BVBRC-81

Where this replication almost went wrong, where it worked around a genuine
obstacle, and where it deliberately did not attempt something the paper did.
Documented so future replicators of BV-BRC Nanopore-assembly workflows can
skip the same rakes.

---

## 1. What actually failed

### 1.1 MDPI PDF fetch (Akamai block)
- **What.** Direct `curl` / `wget` of the paper PDF from `mdpi.com` was
  blocked by MDPI's Akamai layer with a challenge page, from both CherryRd
  and uicgpu. This is an ongoing MDPI anti-scraping posture, not a one-off.
- **Impact.** Could not visually inspect figures (circular genome maps,
  TYGS tree).
- **Workaround.** Used the Europe PMC full-text XML mirror
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10609609/fullTextXML`)
  which is unrestricted and returned complete text + tables (200,906 B).
- **Residual risk.** Figures unread; low probability of hidden numeric
  claims not present in the text or tables. Accepted.

### 1.2 Two LLM judges returned HTTP 502
- **What.** `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both returned
  HTTP 502 from the Argo proxy (`:44497`) during the judge run on 2026-07-03.
- **Impact.** Only 3 judges instead of the intended 5-way panel.
- **Workaround.** Proceeded with 3 (gpt-4o, gpt-5, gemini-2.5-pro). The
  panel is still an odd number and returned a clear 2:1 majority verdict.
- **Residual risk.** Low. Opus judges were not expected to swing the
  verdict; Argo Opus availability is a known intermittent issue.

## 2. What almost failed (early-warning notes)

### 2.1 tRNA off-by-one between Prokka and paper
- Prokka found 71 tRNAs; paper reports 72.
- **Not a failure** — PGAP re-annotation returns 72, matching the paper.
  The discrepancy is a Prokka-vs-tRNAscan-SE cutoff artifact, not a genome
  problem. Flagged only because a naïve reader might over-interpret it.

### 2.2 CARD raw hit `dfrE` at 67.6% coverage
- Abricate + CARD returned a single raw hit (dfrE, dihydrofolate reductase,
  67.6% cov / 75.5% id). Under Abricate defaults (`--mincov 80 --minid 80`)
  this fails the filter, matching the paper's zero-AMR call.
- **Not a failure** — the filter is doing its job. Flagged so a future
  replicator does not report this as an "AMR gene present" if they lower
  the thresholds without justification.

### 2.3 VFDB `clfA`/`clfB` fragments 12–33% coverage
- Same pattern as 2.2. Sub-threshold sequence similarity to *Staphylococcus
  aureus* fibrinogen-binding surface proteins. All fail the 80%/80% filter.
  These are conserved-domain fragments, not real virulence factors in a
  *Lactiplantibacillus*.

### 2.4 CDS-count divergence (~25% across three annotation runs)
- This is the single largest observed disagreement between our replication
  and the paper. See REPORT.md §4.2 and REPORT.tex §Genuine critique.
- **Not chased to root cause** — deliberately, because doing so would
  require recovering the PGAP binary + database snapshot from the paper's
  submission date, which is not archived.

## 3. What was deliberately not attempted

### 3.1 BAGEL4 (bacteriocin core-peptide labels)
- Web server only; not installed locally.
- **Consequence.** The bacteriocin cluster (C11) is confirmed
  positionally and by machinery genes (AgrA/LagD/LcnD), not by direct
  PlnE/F/K labels. A stricter replication would install BAGEL4 (Docker
  image available).

### 3.2 CRISPRCasFinder
- Web server only. The paper reports a CRISPR array at chromosome
  1,306,053–1,306,616 (evidence level 4). Not independently re-typed here.

### 3.3 dbCAN3 (CAZyme survey)
- Web server only. Not independently re-run.

### 3.4 Wet-lab phenotype panels
- Acid tolerance, bile tolerance, osmotic tolerance, oxidative stress,
  adhesion assays, BIOLOG PM sugar utilization, antibiotic disc diffusion:
  all require the actual PU3 strain in an anaerobic lab. Not attempted.
- **Consequence.** The verdict "REPLICATED" covers genomic + comparative
  claims only. Phenotype claims are recorded as "not evaluated", not as
  "replicated".

### 3.5 Nanopore raw-read reassembly
- The paper's assembly was verified from the deposited final genome, not
  by re-running Flye/Racon/Medaka on raw MinION reads.
- We did check for raw-read availability under BioProject PRJNA946199;
  in the current archive the raw reads path is not straightforward to
  reproduce without additional metadata from the depositors.
- **Consequence.** We cannot say whether an independent re-assembly from
  the same raw reads with a newer Flye would yield the same 3.18 Mb
  chromosome + 9 plasmids. This is a known limitation of
  "assembly-from-final-deposit" replication style.

### 3.6 Hybrid short-read polishing
- No Illumina data exists for PU3 (Nanopore-only paper). We did not
  attempt to generate any. See `open_questions.json` OQ1.

## 4. Lessons learned (durable, for future BV-BRC Nanopore replications)

1. **Always try Europe PMC XML before MDPI PDF.** MDPI's Akamai layer is
   a recurring block. Europe PMC has the full text and is unrestricted.
2. **PGAP snapshot dates matter.** Any bacterial genome paper's CDS count
   is snapshot-dependent. Report all three: paper's number, current PGAP
   number, and Prokka number. Do not treat a ~25% CDS delta as a
   contradiction — it is baseline pipeline variance.
3. **Abricate defaults (80% cov, 80% id) are the right filter.** Report
   raw hits + passing hits separately; the paper is using the filter, so
   you must too, or you are not comparing like with like.
4. **Structural RNA counts (rRNA, tRNA) are the most pipeline-stable
   comparison and should be the primary annotation cross-check.** They
   almost always agree exactly across Prokka, PGAP, and BV-BRC.
5. **BAGEL4, CRISPRCasFinder, dbCAN3 are web-only.** Plan around this —
   either install Docker images ahead of time or accept the machinery-only
   / positional confirmation as sufficient for a genomic replication.
6. **A 3-way LLM judge (odd number, mixed families: gpt-4o + gpt-5 +
   gemini) is a robust cheap cross-check** and typically returns a clear
   majority. Anthropic judges via Argo have intermittent 502s; do not
   assume a full 5-way panel will always land.
