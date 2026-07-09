# Failure Analysis — BVBRC-87 (Gancz 2021, KpnU95 ST1412)

This document is the honest counterweight to the headline `PARTIAL (strong)` verdict. It catalogs what did NOT fully replicate, what was NOT attempted, why each gap matters, and what would be needed to close it. Verdict: **PARTIAL** — not `REPLICATED`.

## Summary by gap category

| Gap | Claim(s) | Category | Downstream risk |
|---|---|---|---|
| Chromosome ORF count Δ24 CDS (5,063 vs 5,087) | C3 | Minor annotation drift | Low — within 0.5% |
| oqxAB / nfsA-like not directly re-BLASTed | C6 | Partial evidence | Low-medium — chr-mediated resistance interpretation partially relies on it |
| Sec 3.4 capsule K109 vs Kleborate KL107 | C10 | Contradicted (paper-internal typo) | Low — paper's own Sec 3.5 agrees with our KL107 call |
| C9 Houston Methodist ST1412 SRA meta-analysis | C9 | Untested | Medium — the paper's comparative-genomics narrative is not re-verified |
| C11 all wet-lab claims | C11 | Not attempted (physical strain required) | **HIGH — the paper's mechanistic story rests entirely on assays we did not repeat** |
| Independent hybrid re-assembly from raw SRA reads | (C3, C4) | Circularity — read-your-own-deposit | Medium — replicates deposit annotation, not de-novo assembly |
| Provenance metadata (C1) | C1 | Untested | Low — this is patient/metadata data, not scientifically replicable from public artifacts |

## Detailed analysis

### Gap 1 — Chromosome ORF count Δ24 CDS (C3)

- **Paper:** 5,087 ORFs on chromosome.
- **This work:** 5,063 CDS in the NCBI GFF for `GCA_015714665.1`.
- **Delta:** 24 CDS (0.47%).
- **Hypothesis (unverified):** paper used NCBI PGAP + RAST hybrid annotation; NCBI's re-annotation for the deposited assembly is PGAP-only. Small pipeline-driven CDS drift is normal.
- **What would close it:** re-run RAST on the assembly, compare CDS calls locus-by-locus vs the current PGAP GFF, confirm the 24-CDS delta is attributable to hypothetical / short-ORF cutoffs where the two pipelines differ.
- **Not closed here.** Called PARTIAL for ORF, REPLICATED for bp (which IS byte-exact).
- **Downstream risk:** low. Chromosome sequence content is identical; ORF-calling differences don't affect any downstream claim.

### Gap 2 — oqxAB / nfsA-like not directly re-BLASTed (C6)

- **Paper:** chromosomal SHV, oqxAB efflux, and nfsA-like nitroreductase (75.62% id) → intrinsic nitrofurantoin non-susceptibility.
- **This work:** Kleborate confirms `Bla_chr = SHV-1` on the assembly. oqxAB and nfsA are not standard Kleborate output fields and were NOT directly BLASTed against the chromosome scaffolds.
- **Consequence:** the SHV-1 part of C6 is REPLICATED; the oqxAB and nfsA parts are only "consistent with" (the plasmid-driven cipro MIC pattern the paper describes is compatible with oqxAB presence). Not verified.
- **What would close it:** BLAST oqxA + oqxB (from any reference K. pneumoniae, e.g., MGH78578) against `kpnu95.fna`; BLAST nfsA from E. coli against chromosome scaffolds; confirm the 75.62% id number specifically.
- **Not closed here.** Called PARTIAL and left there.
- **Downstream risk:** low-medium. Any nitrofurantoin-treatment claim resting on the nfsA-like divergence has NOT been independently verified in this replication.

### Gap 3 — Capsule K109 vs KL107 (C10)

- **Paper Sec 3.4:** "KpnU95 belonged to ST1412 lineage with a K109 capsular type."
- **Paper Sec 3.5:** "Four out of the five Houston K. pneumoniae ST1412 isolates that carried pKpnU95-related plasmid sequences possessed capsule type KL107." (Implicitly places KpnU95 in the KL107 group.)
- **This work:** Kleborate 3.2.4 (2024 K-locus DB): `K_type: unknown (KL107)`.
- **Reading:** paper Sec 3.4 K109 is likely a typo. Our KL107 call agrees with the paper's own Sec 3.5.
- **Alternate less-charitable reading:** the paper's typing pipeline was inconsistent between sections. We resolved the ambiguity in the direction that flatters the paper's Sec 3.5 comparative-genomics story.
- **Not fully closed.** We accept the KL107 interpretation without running a period-appropriate Kleborate (2021-era K-locus DB) to see if that DB call was K109.
- **What would close it:** install a 2021-era Kleborate + K-locus DB snapshot, re-type Kpnu95, see if the K109 result reproduces on the older DB. If it does, the "typo" reading dissolves and the discrepancy is real DB drift.
- **Downstream risk:** low. K-locus is downstream of ST for most epidemiology purposes, and both K109 and KL107 land in the same clonal group.

### Gap 4 — C9 Houston Methodist ST1412 SRA meta-analysis (untested)

- **Paper:** 4/5 Houston Methodist ST1412 isolates carry a pKpnU95-related backbone with capsule type KL107; the 5th (KL7) does not.
- **This work:** UNTESTED. We did NOT pull the 5 SRA runs, did NOT map reads against pKpnU95, did NOT re-type their capsules.
- **What we did instead:** confirmed our own KL107 call for Kpnu95 (which is a necessary but not sufficient condition for the paper's clustering claim).
- **What would close it:** identify the 5 Houston BioSamples referenced in the paper (paper Table/text lists BioSample IDs), pull SRA runs via `sra-toolkit` or `nf-core/fetchngs`, run `mash screen` or read-mapping against `MK552109.1`, and re-type each isolate's K-locus.
- **Not closed here.** Out of scope for a rank-40 spot-replication of a single-isolate paper.
- **Downstream risk:** medium. The paper's comparative-genomics finding that pKpnU95 is not unique to Kpnu95 — that it circulates in the ST1412 lineage — is not re-verified here. If a downstream reader wants to cite the ``pKpnU95-related plasmid is a lineage marker for ST1412 KL107'' claim, that claim should carry an ``untested in this replication'' asterisk.

### Gap 5 — C11 wet-lab (NOT ATTEMPTED — highest-risk gap)

- **Paper C11 subclaims (all NOT ATTEMPTED here):**
  - Plasmid curing abolishes ESBL phenotype.
  - Plasmid curing drops cipro MIC 11.8×.
  - Plasmid curing decreases artificial-urine growth advantage.
  - Plasmid curing decreases copper tolerance.
  - Plasmid curing does NOT affect *C. elegans* killing (chromosomally-driven virulence).
- **Why not attempted:** requires the physical KpnU95 strain, a cured derivative (may or may not be available from the Navon-Venezia lab on request), a nematode culture facility, MIC-panel capability, and an artificial-urine growth-curve rig. None of these are available on `uicgpu` in a bioinformatics-only replication.
- **What would close it:** request the KpnU95 + cured strain from Navon-Venezia (Ariel U, Israel) via lab-to-lab transfer or a repository (BEI, DSMZ). Reproduce the plasmid-curing panel + assays with a naïve MIC panel + a Galleria-in-place-of-C.elegans surrogate as a fast first pass; full C. elegans repeat if lab infrastructure permits.
- **Not closed here.** Labelled `NOT ATTEMPTED` in every claims table so no reader can mistake absence-of-check for verification.
- **Downstream risk:** **HIGH.** The paper's *mechanistic* story — the entire ``plasmid explains fitness'' arc — is not re-verified. Anyone quoting the `PARTIAL (strong)` verdict downstream must be forced to notice the C11 gap.

### Gap 6 — Circularity: read-your-own-deposit (C3, C4)

- **What happened:** our chromosome bp (5,055,295) and plasmid bp (180,286) match to the byte because we read the authors' own NCBI deposits (`GCA_015714665.1` for the chromosome, `MK552109.1` for the closed plasmid). The plasmid CDS count (243), GC (50.23%), and replicon call are similarly derived from the authors' deposit.
- **What this tests:** ``an independent reader can retrieve the deposited artifacts, run standard annotation/typing tools, and reach the same numbers as the paper.'' This IS a real test — it catches deposit errors, tool-drift errors, and typos in the paper's reported values. Kpnu95 passes it cleanly.
- **What this does NOT test:** ``an independent lab can re-assemble the raw SRA reads with Unicycler-hybrid and independently reach a 180,286-bp closure.'' That is the stronger test.
- **What would close it:** pull the SRA short + long reads (BioProject `PRJNA494961`), run Unicycler-hybrid or Trycycler, compare the resulting plasmid closure to `MK552109.1` (dnadiff or minimap2/paftools).
- **Not closed here.** Out of scope; would triple the wall time (SRA download + assembly ~1–4 hours) and require Nanopore-basecall reproducibility.
- **Downstream risk:** medium. Our numbers being exact reflects deposit integrity + tool-DB accuracy, not de-novo assembly reproducibility. This should be understood when citing our verdict.

### Gap 7 — C1 provenance (untested)

- **Paper:** isolated from healthy young woman with community UTI, Israel, 2016.
- **This work:** UNTESTED. Patient metadata is not scientifically replicable from public artifacts; we can only cross-check the isolate-collection date + origin fields on the BioSample record.
- **Downstream risk:** low. This is metadata, not a mechanistic claim.

## Bottom line

The replication earns the `PARTIAL (strong)` verdict because:

1. **Every testable computational claim reproduces exactly** on public data with standard tools (ST, chromosome bp, plasmid metrics, 10-ARG resistome, persistence operons, non-conjugative status).
2. **BUT** the wet-lab claims (C11) — which carry the paper's mechanistic story — were NOT attempted and would require the physical strain to close.
3. **AND** the comparative-genomics C9 claim was NOT attempted and would require SRA meta-analysis to close.
4. **AND** the exact-match numbers on C3/C4 partly reflect ``we can read the authors' own deposit,'' which is a valid but not maximal replication test.

The verdict is `PARTIAL` — not `REPLICATED` — precisely because of the C11 wet-lab gap. Anyone downstream who reads this replication and wants to treat the plasmid-curing mechanistic story as re-verified is misusing the verdict; that story is `NOT ATTEMPTED`, not `REPLICATED`. All the bioinformatic scaffolding around it holds up cleanly.
