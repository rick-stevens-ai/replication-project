# BVBRC-111 — Failure analysis

Honest catalogue of every place the replication is weaker than a naïve read of the REPORT.md verdict (`REPLICATED, 92`) would suggest. Written 2026-07-05 as part of the 8-artifact backfill.

## Category A — Things that failed and were worked around

### A1. Paper PDF could not be fetched non-interactively

- **What failed.** Three open-access endpoints all refused a headless fetch inside the 60–90 s cap:
  - OUP publisher PDF (`academic.oup.com/jac/article-pdf/77/7/1851/44373670/dkac115.pdf`) → HTML anti-bot challenge page instead of PDF bytes.
  - Europe PMC render endpoint → HTTP/2 `STREAM_CLOSED`.
  - NCBI PMC per-article gate (`pmc.ncbi.nlm.nih.gov/articles/PMC9244215/pdf/dkac115.pdf`) → 1.8 KB "Preparing to download" HTML gate page rather than PDF bytes.
- **Root cause.** All three endpoints have some form of interactive-only fetch gate (bot detection, JS-issued cookie, or referer/session check).
- **Workaround.** Wrote `extraction/marker.md` as a pending stub with full identification metadata (DOI, PMID, PMCID, S2 paperId) and explicit fill instructions for a later interactive-session sweep. Wrote `extraction/nougat.mmd` as a pending-GPU-parse stub. Grounded the replication in the paper's abstract + the authors' own GenBank submission metadata for CP090606.1 + CP080453–456 (which encodes the AbaR28 / Tn2006 / Tn7 / Tn7+ / gyrA / marR annotations directly in the feature table).
- **Residual gap.** Body text of the paper (Methods, discussion, supplementary) was not consulted during this pass. Any nuance that lives only in the paper's prose is invisible to us.

### A2. Paper not present in central Eagle Marker/Nougat corpus

- **What failed.** grep for `MRSN 56` / `dkac115` / `Harmer` across `/eagle/projects/AuroraGPT/stevens/scout_corpus/md/` (520 files) returned zero hits. Same for `/eagle/projects/AuroraGPT/stevens/osti_marker/md/`.
- **Root cause.** The paper is not (yet) in the central corpus; corpus is focused on the OSTI + scout target sets, and this JAC paper was not in either.
- **Workaround.** See A1 (stub + abstract-grounded replication).
- **Next step to close.** After PDF is materialized interactively, queue via the central Nougat pipeline; sha256 becomes the filename in `/eagle/projects/AuroraGPT/stevens/scout_corpus/mmd/`.

### A3. Oxford MLST returned "-" (novel combination)

- **What failed.** `mlst --scheme abaumannii` returned `-` because `Oxf_gdhB` resolved as 4/182 (mixed allele call).
- **Root cause.** pubMLST database drift since the paper's 2022 typing. `gdhB` in *A. baumannii* is notoriously polymorphic and has had allele-numbering churn.
- **Workaround.** Focused on the Pasteur scheme (which the paper leads with anyway); Pasteur returned exact ST1 with all 7 alleles matching.
- **Residual gap.** We did not manually reconcile the current `gdhB` alleles to those in force in 2022. If a reviewer specifically wants ST231Ox confirmed we would need to freeze the pubMLST snapshot at ~mid-2022.

### A4. Tn7+ span 21.7 kb vs paper's 22,852 bp

- **What failed.** Our reported ~21.7 kb Tn7+ block does not exactly reproduce the paper's 22,852 bp figure.
- **Root cause.** We did not lock the paper's exact left/right boundary features and measure between the same coordinates in our own annotation. We used the outermost feature boundaries we could see in the GBFF (glmS-adjacent TnsA → IS*Aba1* right flank) and reported the span between them.
- **Workaround.** Called out explicitly in the report as "same order of magnitude, boundary-definition difference".
- **Residual gap.** ~1.1 kb (5%) discrepancy is unexplained. Either (a) our boundary features are 1–2 CDSs short of the paper's, or (b) the paper's boundaries include an IS element on one side that we assigned outside the Tn7+ module. A disciplined follow-up would obtain the paper's exact coordinates from a supplementary table and reconcile.

## Category B — Things we did not attempt (declared out of scope, but real gaps)

### B1. Did not re-assemble from raw reads

- We replicated against the finished assembly GCA_021484925.1, not against the MinION+MiSeq reads that produced it.
- Every downstream claim depends on the base-pair correctness of the finished assembly.
- Not attempted because: (i) requires ~50 GB read data, (ii) requires Unicycler v0.4.0 + modern hybrid stacks, (iii) not the paper's contribution (the paper's contribution is the annotation of the finished sequence, not the assembly method).
- But: this means we cannot rule out that the paper's Tn7+ / two-Tn7-copies / plasmid-boundary claims are assembly artefacts. See Q4 in `open_questions.json`.

### B2. Did not test the transcriptional half of C7

- Paper's C7 has two halves: (i) structural (IS*Aba1* inserted upstream of *marR*, MarR pseudogene) and (ii) transcriptional (constitutive *marA* expression from an IS*Aba1*-internal promoter).
- We reproduced half (i) cleanly. Half (ii) requires RNAseq / reporter assays / 5′ TSS mapping, none of which we ran.
- The paper's headline mechanistic novelty rides on half (ii); we scored the claim as MATCH-structural rather than MATCH, and the failure_analysis is: we are validating a structural prerequisite, not a mechanism.

### B3. Did not independently re-annotate (Prokka/Bakta)

- Used NCBI PGAP as shipped in the GCA_021484925.1 GBFF for every feature call, including pseudogene calls for MarR-family regulators and *parC*.
- PGAP releases update and its HMMs change. A different PGAP release could re-label some CDSs — especially the pseudogene calls that C7 leans on.
- A more rigorous replication would run Prokka or Bakta as an independent second annotator and confirm the AbaR28 walk / Tn7 machinery / IS*Aba1*–marR juxtaposition / MarR-frameshift call all reproduce under an alternative annotator.

### B4. Did not stress-test AMR call thresholds

- Used `--minid 90 --mincov 80` for all AMR databases.
- Did not re-run at `--minid 98 --mincov 95` to check whether any AMR calls are borderline hits.
- Marginal alleles (variant *aadA1*, promoter mutants of *bla*<sub>OXA-23</sub>) would not be flagged under the permissive threshold.

### B5. Did not verify Tn2006 / Tn7 target-site duplications

- Both Tn2006 and Tn7 have signature target-site duplications (TSDs) of characteristic length.
- We confirmed positional flanking of *bla*<sub>OXA-23</sub> by IS*Aba1* on both sides, and TnsA/D/E adjacency for Tn7 clusters, but did not extract the flanking sequences and check for the expected TSDs.
- A more thorough replication would confirm TSDs to distinguish "canonical Tn2006/Tn7 in the correct configuration" from "just some elements in the neighbourhood".

### B6. Did not survey generality of Tn7+

- Tn7+ is claimed as novel. Novel means "not seen before in the surveyed corpus". We did not survey any other genomes to check whether Tn7+ is unique to MRSN 56 or has spread. See Q3 in `open_questions.json`.

## Category C — Systemic critique of evidence strength

### C1. Two LLM judges are not two independent replications

- Both judges consumed *the same structured dossier that we wrote*. They can only score what we chose to put in front of them.
- Getting 88 and 95 out of two LLMs reading our own evidence brief is one replication scored twice, not two replications.
- Improvement: build an "adversarial" dossier that intentionally hides some of our confirmations to see whether the LLM judges catch the omission.

### C2. This replication is structurally biased toward success

- The paper describes features the authors could see directly in the finished sequence. Re-running the annotation against that same sequence is almost guaranteed to succeed for those features.
- The right null hypothesis for a probing replication is not "can we see what the authors saw in *their* genome?" but "can we see the same pattern in *other* genomes?" We did not do the latter (see B6 / Q3).

### C3. Score inflation risk

- The score of 92 lands in the "REPLICATED" band. But nearly all of the score is driven by structural/positional matches on features the authors extracted from the very sequence we re-analyzed. The one truly mechanistic claim (C7 transcriptional half) is untested.
- A more honest scoring rubric would down-weight structural-match-on-same-sequence claims and up-weight tested-mechanism claims. Under such a rubric this replication would probably score in the 70s.

### C4. No wet-lab loop

- No isolate was cultured, no MIC was measured, no RNA was extracted. This is an entirely in-silico replication against public sequence.
- That is the correct scope for a BV-BRC-style replication of a bioinformatic paper, but should not be over-read as "we independently confirmed the phenotype".

## Category D — Backfill-specific gaps (2026-07-05)

### D1. `paper.pdf` still not on disk after backfill fetch attempt

- If the backfill fetch attempt (executed after all 5 report items were written) also failed, a `paper.pdf.MISSING.md` marker will be present alongside this file. The stubs in `extraction/marker.md` and `extraction/nougat.mmd` capture the fill instructions for a later interactive sweep.

### D2. `report/REPORT.pdf` may not exist

- The backfill attempted a `pdflatex` compile of `REPORT.tex` if the binary was on PATH. Absence of `REPORT.pdf` in the dir means `pdflatex` was not available in the subagent's PATH; the `.tex` source is authoritative and can be compiled later.

## Residual open items → converted to Open Questions

Every non-trivial gap above has been converted into one of the 5 heavy-duty items in `open_questions.json`:

- A1/A2 (paper text access) → operational, handled by fill instructions in stubs.
- A4 (Tn7+ span) → subsumed by Q4 (assembly reproducibility).
- B1 (raw-read assembly) → **Q4**.
- B2 (C7 transcriptional half) → **Q1**.
- B3 (independent annotator) → operational follow-up.
- B4 (threshold stress-test) → operational follow-up.
- B5 (TSD verification) → operational follow-up.
- B6 (Tn7+ dissemination survey) → **Q3**.
- Extra: multiple MarR-family loci disentanglement → **Q2**.
- Extra: novel-route fitness vs classical route → **Q5**.
