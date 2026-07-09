# Failure analysis — BVBRC-77 · proGenomes3

An honest catalog of what did NOT work, what was skipped, and what should not
be over-read from a PARTIAL verdict.

## 1. The paper's exact v3 numbers cannot be re-verified

**Symptom:** every `proGenomes3_*.tab.bz2` URL enumerated from the current
download page returns **HTTP 404**. 6/6 candidate v3 URLs → 404 on both
2026-07-03 and 2026-07-04.

**Consequence:** the paper's headline claims
- **C1** (907,388 HQ genomes) and
- **C3** (41,171 specI clusters)

cannot be evaluated as literal snapshot claims from the paper's own cited
URL. Every quantitative check in this replication is against the **pg4**
successor (1,891,267 / 32,887), which uses a **different clustering
methodology** (pure ANI vs specI).

**Mitigation used:** verified the *class* of claim on the served successor
files and documented the direction and magnitude of the v3→pg4 delta with
cross-checks against a disjoint QC-excluded roster. This is supportive but
does not equal snapshot-faithful replication.

**Cannot be mitigated without:** the pg maintainers reposting v3 tarballs, or
a mirror surfacing (Zenodo, ENA, etc.).

## 2. Silent v3→v4 backend swap is undocumented

**Symptom:** the download page HTML still advertises `proGenomes3_*`
filenames that no longer exist. Users following the paper get 404s with no
version banner and no changelog.

**Consequence:** a naive user will conclude "the resource is offline" rather
than "the resource silently upgraded". This is a real reproducibility hazard
for any longitudinal analysis. It is arguably the most important operational
finding of this replication.

**Mitigation used:** documented as a first-class finding in REPORT.md, §4.1
and §4.2.

**Recommended fix (out of our scope):** the maintainers should either (a)
repost v3 tarballs under a versioned URL, or (b) update the download-page
HTML to reflect pg4 filenames and post a machine-readable version manifest
plus per-release DOI.

## 3. CheckM QC gate does NOT independently reproduce at 100%

**Symptom:** 79.3% (65/82) of slice-100 genomes with both fields reported
pass the paper's stated "completeness > 90% AND contamination < 5%" gate
under NCBI's independent CheckM re-run. Three concrete failures documented:

- `GCA_004295585.1` (*Cohnella abietis*): completeness 90.9%, **contamination 14.2%**
- `GCA_000521215.1` (*Labrenzia sp.*): completeness 86.9%, **contamination 18.6%**
- `GCA_002631185.1` (*Teichococcus rhizosphaerae*): completeness **74.9%**, contamination 12.5%

**Consequence:** if read literally, this is 21% of representatives failing
the paper's own QC gate.

**Caveat / mitigation:** NCBI's CheckM is CheckM1 with the standard 43-marker
lineage-specific set. pg4's internal QC is likely CheckM2 (ML-based, same
authors, distinct tool, different numbers on the same genomes) with
pg-specific marker choices. This tool-version mismatch is a plausible
explanation for the entire discrepancy.

**Not mitigated:** we did NOT re-run CheckM2 + GUNC with pg's exact marker
set on the slice. That test was out of budget. Anyone citing the 79.3%
number should NOT read it as "pg fails 21% of its own QC gate"; and anyone
citing the 0/32,887 structural check should NOT read it as "biological QC
gate independently verified" — the structural check only shows internal
consistency (reps are not on their own excluded list), not gate
calibration.

## 4. eggNOG functional annotation (C6) was NOT tested

**Symptom:** claim C6 (consistent functional annotation via eggNOG-mapper) was
explicitly skipped as out-of-budget. The 1.5 GB `pg4_eggnog_representatives`
file was not downloaded and no eggNOG-mapper re-run was performed.

**Consequence:** one of the paper's four headline consistency claims
(taxonomy + functional annotation + MGE + BGC) has zero independent
evidence in this replication. Nor were MGE or BGC annotations touched.

**Not mitigated.** This is the single largest scope gap. See
`open_questions.json` Q3 and Q4 for a follow-up plan.

## 5. Slice-100 species-level taxonomy agreement is low

**Symptom:** slice-100 vs NCBI shows only 42.9% species-name agreement
(genus agreement 71.4%).

**Consequence:** at first glance this looks like a failure of the paper's
"consistent taxonomy" claim.

**Caveat / mitigation:** the mismatches are dominated by known, deliberate
GTDB reclassifications (e.g. *Brucella tianjinense* in GTDB = *Falsochrobactrum
tianjinense* in NCBI; *Halopseudomonas excrementavium* vs *H. bauzanensis*).
The paper claims consistency *within* the pg system (specifically that pg's
GTDB labels are the GTDB labels), not agreement with NCBI's Linnaean
taxonomy. GTDB is designed to diverge from NCBI at roughly half of species.
The 90.01% GTDB-consensus coverage at DB scale is the stronger measurement
of the paper's actual claim.

**Not a failure of pg — a failure of the naïve NCBI-agreement metric.**

## 6. LLM judge Opus-4.7 returned 502 in both runs

**Symptom:** `argo:claude-opus-4.7` returned 502 Bad Gateway from the Argo
proxy in both v1 and v2 judge invocations. The unanimous "3/3 PARTIAL" is
really 3/4 with one endpoint unreachable.

**Consequence:** the majority vote is unanimous among reporting judges but
not truly quadruple-vote. Argo proxy availability is not under our control.

**Mitigation:** noted in REPORT.md §5.2; three-of-three from the other
frontier models is still a strong-enough signal for a PARTIAL verdict, but
should not be described as "4/4 unanimous".

## 7. LLM judges are not independent of the evidence pack

**Symptom:** all three reporting judges converged on PARTIAL after being fed
an evidence pack that itself framed the situation as partial (v3 files 404,
successor reproduces class of claims, one claim untested, one claim
tool-caveated).

**Consequence:** the unanimous PARTIAL is corroborative, not orthogonal
evidence. LLM judges tend to converge on the framing they are given.

**Not mitigated.** This is a general limitation of LLM-judged replication.
Treat the judge output as an internally consistent summary, not as ground
truth.

## 8. Compute + endpoint scope limits

- Only used free endpoints (EuropePMC, NCBI eUtils, NCBI Datasets v2alpha,
  progenomes.embl.de, free Argo proxy). No paid APIs; no GPU jobs; no
  Polaris/Aurora time. This bounds what could be re-run in-scope.
- Local CherryRd, Python 3.13 stdlib only. No CheckM2, no GUNC, no
  eggNOG-mapper, no antiSMASH, no CARD-RGI, no VFDB — any of which would
  require heavier tooling and would meaningfully strengthen the replication
  but were out of budget.

## Bottom line

**PARTIAL is the honest verdict, and it is genuinely partial.** The paper's
resource is real, healthy, and internally well-structured on its live
successor. The paper's specific v3 snapshot is 404. One headline claim was
untested (eggNOG). One QC re-check disagreed at the 21% level under a
tool-version caveat. The v3→v4 silent swap is the most reproducibility-
consequential finding for the community.

Do NOT read PARTIAL as "close to REPLICATED". It means: real resource, real
successor, real cross-checks, real known limitations, and one substantive
un-tested claim.
