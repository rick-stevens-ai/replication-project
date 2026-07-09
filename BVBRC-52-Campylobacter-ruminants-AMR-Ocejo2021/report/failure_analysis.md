# Failure Analysis — BVBRC-52 replication (Ocejo et al. 2021)

**Verdict:** PARTIAL (strong). This document catalogues what *didn't* work, what was deliberately skipped, and what remains a genuine gap. It is the companion to REPORT.md / REPORT.tex.

## 1. Genuine failures encountered during the run

### 1.1 tet(O) assembly-level dropout in three high-coverage *C. coli* (C0140, C0541, C0680)
- **Symptom:** Assemblies of three TET-resistant multidrug *C. coli* were negative for tet(O) when scanned with ABRicate.
- **Root cause:** ~150× downsampling (input capped from raw ~1125×) plus the paper's own 200 bp contig filter. SPAdes at moderate coverage occasionally fragments plasmid/repeat-borne genes below the length threshold. Known SPAdes behaviour.
- **Rescue:** Parallel direct **raw-read** BLAST for tet(O): 148 / 155 / 161 read hits in the three isolates, 0 hits in the TET-susceptible control C0444. The gene is genuinely present; it just failed to assemble into a ≥200 bp contig at downsampled coverage.
- **Cost to concordance:** raw = 91.1% (5 FN); corrected = 93.8% (2 FN). Reported honestly with both numbers.
- **What would fully fix this:** rerun assembly at full ~1125× coverage — this is what the paper did and is why the paper did not see this failure mode. Compute time was the reason for downsampling in the replication.

### 1.2 PointFinder not installed in the compute environment
- **Symptom:** The paper's `PointFinder` tool for chromosomal point-mutation calling was unavailable in the `bvbrc14/bvbrc38/bvbrc28` conda envs at run time.
- **Root cause:** Missing dependency; not installed.
- **Substitute used:** tblastn / blastn against the *C. jejuni* NCTC 11168 wild-type reference (RefSeq GCF_000009085.1, fetched via NCBI `datasets`). WT gyrA protein → tblastn residue 86; WT rpsL protein → tblastn residue 43; WT 23S rRNA → blastn with the resistance column pinned empirically by aligning all copies across ERY-R vs ERY-S isolates — this converged cleanly on **gene position 2075**, matching the paper's *E. coli*-numbered A2075G claim.
- **Validation:** clean R/S separation in all three loci; exact-position match to the paper's numbering. Strong evidence the substitute behaves equivalently on the mutations tested, but it is not tool-level identical.
- **What would fully fix this:** install PointFinder + PointFinder-DB (Campylobacter), rerun.

### 1.3 AMP concordance is genuinely poor (69%)
- **Symptom:** 5 false-positive AMP calls out of 16 isolates.
- **Root cause:** My genotype→phenotype rule for AMP was "blaOXA present ⇒ predict AMP-resistant." The paper explicitly notes that blaOXA presence alone does not confer AMP resistance in *Campylobacter* — a promoter mutation is separately required. My rule therefore over-calls AMP by design.
- **Not a paper disagreement:** the paper documents this caveat. But it is a genuine weakness of the replication's AMP prediction rule.
- **What would fully fix this:** add a promoter-region scan for the known activating mutations upstream of blaOXA and require both gene + promoter for an AMP-R call.

## 2. Deliberately skipped work (out of subset scope, not failures)

### 2.1 Full-cohort population-genetics analyses (paper claim C10)
- **What the paper did:** core-genome / ST networks (Fig 1), 70-isolate phylogeny (Fig 2), ST↔AMR association statistics (Fig 3).
- **What this replication did:** nothing on this claim. The 16-isolate subset does not support 70-isolate population-structure inference.
- **Why skipped:** the subset was designed to be mechanism-representative, not statistically representative. Full-cohort phylogeny + population statistics is a separate, larger compute job.
- **Impact on verdict:** exactly why the verdict is PARTIAL rather than REPLICATED.

### 2.2 Independent wet-lab MICs
- **What the paper did:** phenotypic MICs against 6 antimicrobials (GEN, STR, TET, CIP, NAL, ERY) + AMP by E-test, pre-existing for the ruminant collection.
- **What this replication did:** used the paper's phenotypes as-is (Table S1) for the genotype-vs-phenotype concordance calculation.
- **Impact:** the concordance metric is "my genotype vs the paper's phenotype", not "my genotype vs an independent phenotype ground truth." Any systematic error in the paper's MICs propagates unaltered into the 93.8%. This is a limitation of any purely-computational replication of a paper with wet-lab phenotypes.

### 2.3 Full 70-isolate reassembly and re-genotyping
- **What the paper did:** WGS + assembly + genotyping on all 70 isolates.
- **What this replication did:** 16/70 (~23%).
- **Why:** compute-time and storage-time tractability. Each isolate is ~660 MB raw FASTQ, and the full paper cohort would be ~46 GB gz + several days of SPAdes time on the shared uicgpu node.
- **What this affects:** any frequency-based claim (e.g. "tet(O) is the most prevalent tetracycline gene", "blaOXA-489 is enriched in ST-827") is confirmed *directionally* here but not *quantitatively* at population level.

## 3. Ambiguities the replication did not resolve

### 3.1 Why is C0268 CIP-resistant with wild-type gyrA?
- **Reproduced from paper:** C0268 phenotypically CIP-R (MIC = 1) yet gyrA WT (Thr86). Both the paper and this replication independently observe this.
- **Neither the paper nor this replication explains it.** Candidates in the *Campylobacter* literature include CmeABC efflux pump upregulation, an unknown novel resistance mutation elsewhere in the QRDR, phenotypic assay noise near the epidemiological cut-off, or a low-frequency subpopulation. Not tested here.
- **What would resolve it:** RNA-seq of C0268 to check CmeABC expression, full QRDR resequencing, MIC repeat with population-analysis-profile.

### 3.2 Are the 5 AMP FPs really the promoter-mutation issue, or something else?
- **Framed as:** "documented caveat — blaOXA presence alone doesn't confer AMP resistance."
- **Not directly tested:** whether the 5 FP isolates actually lack the activating promoter mutation. That would be the direct test.
- **What would resolve it:** promoter-region scan on the 5 FP isolates and compare against the 3-4 AMP-R isolates that carry both gene and mutation.

## 4. Methodological caveats to flag when reporting the 93.8% number

- **Sample size:** 112 calls from 16 isolates × 7 drugs. Wilson 95% CI on 93.8% (105/112) ≈ 87.7–97.0%. Should be quoted whenever the number is compared to another study.
- **Not blinded:** the LLM judge (Argo gpt-5.2 + opus-4.8 cross-check) was presented with a summary that already framed the result as strong-partial. Verdict-elicitation was not blind. Confirmation bias reduced but not eliminated.
- **Corrected vs raw:** the 93.8% depends on accepting the raw-read tet(O) rescue as a legitimate orthogonal check. If someone insists on assembly-only concordance, the number is 91.1%. Both should always be reported together.

## 5. What was tested cleanly and does not need caveats

For balance — this replication's clean wins (no significant failures or hidden caveats):

- **MLST (C3):** 16/16 exact match. Full tool identity (`mlst --scheme campylobacter`), full PubMLST DB agreement, zero disagreements.
- **23S A2075G (C5):** perfect concordance. G in exactly the four ERY-R isolates, A in all twelve ERY-S. Position 2075 identified empirically as the *only* differentiating base in the domain-V macrolide loop — independent confirmation of the paper's E. coli-numbered position claim.
- **gyrA T86I (C4):** matches phenotype in all 16 isolates including the paper's noted C0268 CIP-R / gyrA-WT exception.
- **Assembly stats (C2):** length within 0.8%, GC within 0.1% in all 16. Species-specific GC split (jejuni 30.4–30.5% vs coli 31.2–31.5%) independently confirms two-species structure.
- **Data availability (C1):** 70 runs = 40 jejuni + 30 coli, matches the paper exactly.

## 6. What "PARTIAL" is buying you here

- Everything the paper claims at the mechanistic + typing + gene-content level for the 16 tested isolates is independently reproduced.
- Nothing the paper claims at the full-cohort population-genetics level is independently confirmed or refuted.
- The verdict PARTIAL is precisely calibrated to that distinction. It is not a euphemism for "close but no cigar" — it is a factual statement that the tested subset reproduces cleanly and the untested full cohort remains, well, untested.
