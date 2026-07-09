# Failure Analysis — BVBRC-106

Honest analysis of what failed, what was worked around, what remains open, and where the
evidence is weaker than the verdict headline suggests.

## Executive summary

The **REPLICATED** verdict is defensible on the paper's C1–C6 + C8 claims. It is
**silent** on C7 (MAR operon), C9 (PathogenFinder pathogenicity), and C10 (RAST
subsystem gene count 4733) because these were not tested. Two additional structural
weaknesses (ANI-tool mismatch, database-epoch mismatch) mean the numeric agreement is
within tool-drift, not byte-for-byte reproduction. Nothing observed contradicts the paper;
several claims remain untested and should not be scored as replicated.

## Failures during the original run

### F1. Backgrounded fetch script died silently
- **What failed**: First `nohup ... &` invocation of `fetch_assemblies.sh` produced an empty log.
- **Root cause**: `~/env.sh` sourced with `set -eu`; an unset env var expanded to empty
  string; `mkdir ""` failed; the whole backgrounded child died. Because it was backgrounded
  over SSH with no `wait`, the failure was invisible until log inspection.
- **Workaround**: Switched to foreground execution with explicit inline `conda activate`.
- **Residual gap**: none for this paper, but standing lesson — every future WGS wave should
  use `set -u` protection (`${VAR:-}`) OR run with `-x` and capture stderr.

### F2. EB-247T WGS accession failed WGS-DB lookup
- **What failed**: `esearch -db wgs -query FYBI00000000` returned zero hits.
- **Root cause**: `FYBI00000000` is deposited at ENA under a WGS master ID that is not
  indexed in NCBI's WGS DB under that ID (paper submitted to ENA, not NCBI, for that strain).
- **Workaround**: Fell back to `esearch -db assembly -query "Enterobacter bugandensis EB-247"`,
  which resolved to `GCF_900324475.1`.
- **Residual gap**: the WGS-master → GCF equivalence for EB-247T is a strain-name inference,
  not a checksum trace. Directly relevant to open question Q5 (assembly-drift audit).

### F3. Argo `claude-opus-4.8` returned 502
- **What failed**: First judge POST to `argo:claude-opus-4.8` returned HTTP 502.
- **Root cause**: transient Argo backend unavailability (Opus 4.8 model server was flapping
  on the ANL side, as seen elsewhere on 2026-07-05).
- **Workaround**: Fell back to `argo:claude-sonnet-4.6`, which returned a verdict.
- **Residual gap**: verdict was rendered by a smaller model than intended; not re-tried on
  Opus 4.8 once endpoint recovered.

## Weaknesses that are NOT failures but should be called out honestly

### W1. ANI tool mismatch (FastANI vs paper's JSpeciesWS BLAST-ANI)
FastANI is a MashMap-based ANI proxy; JSpeciesWS is BLAST-based. Known to disagree by up to
±0.5% at the species boundary. Our +0.3% delta on MBRL-1077 is exactly this class of drift.
The **topology** replicates cleanly; the **numbers** are not byte-for-byte reproducible.
A stricter replication would use pyani-blastn to numerically reproduce Table 1.

### W2. AMR database epoch mismatch (2026 vs 2018)
AMRFinderPlus DB 2026-03-24.1 has ~8 years of new reference alleles vs the paper's 2018
RAST subsystems + CARD/ResFinder. Any allele-level statement (e.g. "we call blaACT-77
where paper calls generic blaACT") is a database-epoch difference, not biology. Qualitative
family-level agreement (β-lactamase + efflux) is meaningful; allele-level agreement is not
the same claim.

### W3. Claim C7 (MAR operon) not tested
Out of AMRFinderPlus scope (chromosomal regulator, not acquired AMR). Neither confirmed
nor refuted. Explicitly captured in open question Q3.

### W4. Claim C9 (PathogenFinder >79% pathogenicity) not tested
The paper's headline clinical framing pivots on this. Skipping it is a substantive gap.
PathogenFinder v2 is runnable; the omission was a time trade-off. Captured in Q4.

### W5. Claim C10 (RAST subsystem gene count = 4733) not tested
Even Prokka would not reproduce "4733" byte-for-byte because the taxonomy tree has
changed since 2018. This is a legitimate concern with the paper's reporting (single
decimal, no CI), not just with the replication.

### W6. Assembly-provenance chain is inferred, not checksum-traced
Paper accessions → RefSeq GCFs via WGS master / strain name, not via SHA256. If NCBI
re-scaffolded any of the eight assemblies between 2018 and 2026, we would silently be
running on the re-scaffolded version. Captured in Q5.

### W7. No plasmid separation
Paper Table 2 is explicitly plasmid gene content. We did not separate chromosome from
plasmid before AMR calling, so we cannot distinguish chromosomal vs plasmid-borne
β-lactamase/carbapenemase in our re-screen.

### W8. Within-ISS SNP counts not enumerated
The paper's Table S1 reports specific per-strain SNP counts (9/12/15/13/…) after GATK
filtering. Our ANI-based "99.99–100%" agreement is coarser than that per-strain SNP count.
A read-mapping SNP re-derivation is not done. Related to Q2.

### W9. MBRL-1077 is a marginal-species call
ANI 95.3–95.6% AND dDDH 63.9% straddles the modern species cutoff. The paper resolves in
favor of same-species; the paper's own SNP tree contradicts this. We inherit the ambiguity
without resolving it. Q1 targets this directly.

## What would be needed to fully close the replication

To move from "REPLICATED (partial)" to "REPLICATED (comprehensive)":

1. **Rerun ANI with pyani-blastn** on the same 8 GCFs to numerically reproduce paper Table 1
   under the same algorithm class as JSpeciesWS. (~2 h wall on uicgpu.)
2. **Rerun dDDH** via GGDC 3.0 (web submission or local docker) for the same 8 pairs. (~1 h.)
3. **Run PathogenFinder v2** on all 8 assemblies to test C9 directly. (~30 min.)
4. **Targeted marRAB BLAST** to test C7 with intact-operon criteria. (~15 min.)
5. **Prokka re-annotation** of all 8 assemblies + count subsystem-mapped genes to test the
   C10 4733-number under a modern-yet-comparable annotator. (~1 h.)
6. **Assembly-drift audit** (Q5): pull the 2018 INSDC snapshots for the 8 accessions from
   ENA, checksum, rerun FastANI on those, compare with GCF versions. (~2 h.)
7. **Plasmid separation** (Plasmid-finder or MOB-suite) to correctly localize AMR determinants.
8. **Illumina read-mapping SNP count** vs paper Table S1 filtered SNP numbers (Q2). (~2 h.)

Total additional wall-time: ~10 h uicgpu compute + ~4 h agent orchestration.

## Standing lessons

- Any future BVBRC-set replication should include pyani-blastn ANI + PathogenFinder v2 in
  the default script, not as optional extras, since these are the paper's own baselines.
- Verdict headers should distinguish "REPLICATED" from "REPLICATED (partial: C1..Cn tested)"
  to prevent verdict-header inflation.
- Assembly resolution via WGS master ID should record BOTH the paper's original accession
  AND the resolved GCF, and flag any strain-name fallback as an inference chain.
- LLM-judge failures should retry the primary model at least once after a delay, before
  falling back to smaller model, so verdict provenance is stable.
