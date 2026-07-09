# Failure Analysis — BVBRC-78 (Pradal 2023, vB_EfaH_163)

Honest catalogue of what did not work, what is blocked, and where the replication is weaker than a single-number verdict suggests. Verdict: **PARTIAL** (not REPLICATED) — this document explains why.

## 1. Blocked-by-missing-data (the two claims driving the PARTIAL verdict)

### 1.1 C-9 — Long direct terminal repeats via PhageTerm (BLOCKED)
- **What the paper claims:** vB_EfaH_163 uses direct-terminal-repeat (DTR) packaging, inferred with PhageTerm.
- **Why we could not test:** PhageTerm is a read-mapping algorithm — it infers packaging strategy from read-end pile-ups on the assembled contig. It requires the raw sequencing reads. The authors deposited only the assembled contig (`CAJDKA010000002.1`), not the reads.
- **Consequence:** an accessible-in-principle computational claim is not independently verifiable from public data.
- **Recovery options:** (a) request reads from corresponding author; (b) re-sequence a strain aliquot if obtainable; (c) infer packaging heuristically from terminase-large-subunit family (Herelleviridae terminases are typically pac/headful, so DTR would be unusual for the family and worth confirming). None of these were pursued in this replication.

### 1.2 C-13 — VR-13 host carries the van cluster (BLOCKED)
- **What the paper claims / implies:** the therapeutic model rests on VR-13 being a bona-fide vanR (vancomycin-resistant) E. faecium clinical isolate, i.e. carrying a functional van cluster.
- **Why we could not test:** the host isolate genome was not deposited. Phenotypic vancomycin MIC is reported in the paper but the genotype cannot be independently confirmed by BLASTing a vanA/vanB/vanD/vanN reference against the host assembly.
- **Consequence:** the therapeutic story's foundation (VR-13 = clinically-relevant VRE) has to be taken on the authors' word.
- **Recovery options:** (a) request the host isolate genome from corresponding author; (b) if the strain is deposited with a culture collection, re-sequence.

## 2. Tool-level failures and workarounds

### 2.1 MAFFT segfault on Homebrew macOS build
- **Symptom:** `mafft` crashed with SIGSEGV on the 6-protein MCP input.
- **Impact:** could not produce a proper MSA-based ML tree for C-7.
- **Workaround:** switched to BioPython `PairwiseAligner` (global; match +1, mismatch 0, gap open -1, gap extend -0.5) all-vs-all + UPGMA on (1 − pid) distances.
- **Cost:** topology reproduces paper Fig 4 (Schiekvirus core with MDA2 as Kochikohdavirus outlier), but branch lengths from UPGMA on pairwise-global distances should not be over-interpreted. A proper ML tree with bootstraps was not produced.
- **Fix for next time:** use a different MAFFT build (bioconda) or switch to muscle5 / mafft-linsi via container.

### 2.2 Argo opus endpoints returned HTTP 502
- **Symptom:** `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both returned HTTP 502 during the LLM-judge sweep.
- **Impact:** the pre-registered 6-judge panel dropped to 4 responsive judges.
- **Workaround:** substituted `argo:claude-sonnet-4.6` and `argo:gpt-5.4` to maintain 4 diverse responsive judges (2× GPT family, 1× Gemini, 1× Claude).
- **Cost:** panel composition deviates from pre-registration, though diversity is preserved.
- **Fix for next time:** either retry opus with backoff or accept the sonnet + gpt-5.4 panel as the canonical panel going forward.

## 3. Method-level weaknesses (would tighten the verdict if fixed)

### 3.1 ORF caller mismatch (C-3)
- **What we did:** Prodigal in meta mode → 183 ORFs.
- **What the paper did:** RAST + PATRIC + manual BLAST curation → 186 ORFs.
- **Why our number is lower:** curated pipelines find short ORFs, frameshifted ORFs, and overlapping ORFs that Prodigal-meta misses; conversely Prodigal can over-call in intergenic regions on phage genomes with unusual codon usage.
- **Charity in our verdict:** we called this AGREE ±2%. A stricter reviewer might call it UNVERIFIED-BY-INDEPENDENT-METHOD.
- **Fix for next time:** run Pharokka (phage-specific pipeline: PHANOTATE + tRNAscan-SE + MMseqs2 vs PHROG) which is designed to match curated phage annotations.

### 3.2 BLASTn %identity drift (C-8)
- **What we found:** iF6 96.5%, EFP01 95.7%, EfV12-phi1 94.1%, EFDG1 93.8% — systematic ~2 pp below paper's ~98%.
- **Cause:** metric-definition difference. We used weighted-average %id across all HSPs from megablast; the paper likely used VIRIDIC or pyani ANIm which average differently and can round up to ~98%.
- **Consequence:** looks like data-quality issue but is actually a metric-definition issue. Direction and ordering agree.
- **Fix for next time:** run VIRIDIC (or pyani ANIm) as a second metric to distinguish "our method reads lower" from "the underlying identity is lower".

### 3.3 Lysogeny screen used curated integrase set, not HMMs (C-6)
- **What we did:** BLASTp against a 7-protein curated reference (λ, φ80, P22 int + cIs, Sa3int, L54a).
- **Limitation:** a genuine integrase from an unusual family (e.g. serine-recombinase / large-serine-integrase / tyrosine-integrase variants not present in the curated set) could escape.
- **Positive control:** the same screen against Siphoviridae outgroup NC_031260 returned 1 integrase hit as expected, so the pipeline is functional; the negative result on vB_EfaH_163 is meaningful within the sensitivity of the reference set.
- **Fix for next time:** run PHASTER/PHASTEST HMMs and/or the full VOG lysogeny catalogue for a more sensitive screen.

### 3.4 No sensitivity analysis on the BLASTn metric
- Only one identity metric was reported. A proper replication would compute at least two (weighted-HSP + VIRIDIC or ANIm) and report both.

## 4. Scope-level gaps (not failures, but honest boundaries)

### 4.1 Wet-lab claims are not tested
- C-10 (host range 51%, 16 VRE), C-11 (burst size 155 PFU, latent 60 min), C-12 (Galleria mortality reduction) are all wet-lab and outside computational-replication scope. Nothing was attempted; nothing should be inferred from silence.

### 4.2 Therapeutic claim is not adjudicated
- The paper's headline is a therapeutic result (mortality reduction in Galleria). This replication adjudicates the genomic substrate under that result but not the result itself. A reader interested in phage therapy for VRE should treat our PARTIAL verdict as "the genomic characterization holds up; the therapeutic claim is not our jurisdiction".

### 4.3 Panel composition of the host-range assay is not known
- Even taking C-10 at face value, "51% of E. faecium" is not stratified by clonal complex, MLST, or van allele. Whether coverage is dense inside CC17 (the clinically dominant lineage) or patchy is decisive for translational relevance and cannot be inferred from the paper.

## 5. Was any claim contradicted?
No. Every accessible-in-principle claim tested (C-1..C-8) agreed with the paper. C-3 and C-8 had explainable numerical drift, not contradiction. The PARTIAL verdict is entirely driven by C-9 and C-13 being blocked by missing deposited data, not by any disagreement.

## 6. If we had one more day, what would we do?
1. Re-run C-3 with Pharokka to check whether curated phage-specific annotation closes the 183-vs-186 gap.
2. Run VIRIDIC on the phage + 5 Herelleviridae comparators to produce a proper ANI matrix and close the ~2 pp BLASTn drift with a matched metric.
3. Email corresponding author (Fernández, IPLA-CSIC) requesting raw reads for PhageTerm (C-9) and the VR-13 host genome for van-cluster confirmation (C-13). Even if the answer is no, the request should be logged.
4. Rerun the judge panel with backoff on the opus endpoints to obtain the full 6-judge pre-registered panel.

None of these would change the PARTIAL → REPLICATED boundary on their own (that boundary is set by data-sharing, not by our methods), but items 1–2 would tighten the numeric agreement, item 3 could unblock the boundary itself, and item 4 would deliver the pre-registered panel.
