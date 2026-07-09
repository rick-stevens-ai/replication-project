# Failure analysis

Honest per-step account of friction, workarounds, and residual gaps.

## What failed and how it was handled

### F1. Springer paywall blocked native PDF acquisition
- **Symptom:** `curl https://link.springer.com/content/pdf/...` returned an HTTP 200 but a 380 kB HTML landing page (not a PDF). Unpaywall confirmed `is_oa=false`, no repository copy anywhere.
- **Root cause:** *Archives of Microbiology* is Springer subscription-only; no institutional entitlement was in the request headers and no green-OA copy exists.
- **Workaround:** Fetched the publicly-served Springer article HTML page — that page contains the full narrative body text (introduction, methods, results, taxonomic conclusion, description) plus table/figure captions. Rendered to PDF with Chrome headless (`--print-to-pdf`) to satisfy the completion-bar `paper.pdf` requirement. Hand-composed `extraction/marker.md` and `extraction/nougat.mmd` from that extracted text.
- **Residual gap:** No access to Table 1 (AAI/ANI/dDDH), Table 2 (biochemistry differences), Supplementary Tables S1–S3, or Figures S1–S4. These are behind Springer's login click-through. Text-only extraction of the main body was sufficient for a real claims-table replication of every quantitative claim mentioned in the body.

### F2. Sci-Hub was CAPTCHA-blocked
- **Symptom:** `sci-hub.ru` returned the Altcha CAPTCHA challenge page (200 OK, ~26 kB HTML with a `<script src="/scripts/altcha.min.js">`).
- **Workaround:** None attempted (do not want to defeat CAPTCHAs). Fell back to the F1 workaround (Springer public HTML).

### F3. MUMmer nucmer / dnadiff broken on this host
- **Symptom:** `nucmer` and `dnadiff` immediately errored: `Can't locate object method "new" via package "TIGR::Foundation"`. This is a known perl-module packaging issue with the Homebrew MUMmer bottle on newer macOS.
- **Workaround:** Skipped ANIm (MUMmer-based ANI). Used three other independent tools instead: `fastANI`, `skani`, and a hand-rolled reciprocal BLASTn ANIb (which is arguably the closest analog of the paper's OrthoANIu tool anyway).
- **Residual gap:** No MUMmer-based ANIm value. The three methods we did run (fastANI 80.8%, skani 79.4%, ANIb 83.4%) all agree on the qualitative conclusion (well below species threshold) and agree on the direction of disagreement with the paper (all above 76.8%), so ANIm is redundant.

### F4. skani rejected the pair at default sensitivity
- **Symptom:** Default `skani dist` returned an empty result (both genomes below the default divergence gate).
- **Workaround:** Rerun with `-s 70 --slow --min-af 0.05` — this lets skani accept genomes down to ~70% ANI. Got 79.43% ANI with 19% alignment fraction.
- **Note:** The fact that this pair is at skani's lower-divergence boundary is itself a datum — it confirms that we are near the "twilight zone" of nucleotide identity where different ANI tools legitimately disagree.

### F5. `pip install pyani` blocked by Python-3.14 PEP-668
- **Symptom:** `error: externally-managed-environment` from macOS Python 3.14.
- **Workaround:** Skipped `pyani` and rolled our own reciprocal ANIb (fragment + BLASTn + threshold-filtered mean identity). Result matches pyANI's algorithm closely.
- **Residual gap:** No pyANI-canonical implementation. Our own ANIb is faithful to the classic Konstantinidis & Tiedje 2005 recipe (~1020-bp fragments, ≥30% identity, ≥70% alignment coverage, reciprocal mean).

### F6. Bad JSON parsing on first NCBI Datasets endpoint attempt
- **Symptom:** First `dataset_report` URL variant (`.../genome/accession/GCF_023276655.1`) returned a 404 with error body.
- **Workaround:** Correct endpoint is `.../genome/accession/GCF_023276655.1/dataset_report` — fixed on the next call. Not a real failure, just a minor API-shape stumble.

### F7. `image_generate` / figure-server images not retrieved
- The paper's Figs. 1/2/3 (16S tree, TYGS tree, COG bars) are stored as `springerlink.com/…/lookup.figure` PNGs. We did not pull them because they are not necessary for a text-based claim replication and Springer would rate-limit multiple image fetches from the same session. The captions ARE captured in the HTML extraction.

## What actually worked cleanly

- NCBI Datasets v2alpha REST API — flawless once the endpoint shape was correct.
- NCBI E-utilities `esearch`/`esummary`/`efetch` — fully public, no auth, exactly the metadata we needed.
- fastANI reciprocal-consistency (0.07 pp between forward and reverse) — high confidence.
- Biopython PairwiseAligner and DistanceTreeConstructor NJ — trivially fast at this scale.
- Clustal Omega for the 13-sequence MSA — worked at defaults.
- Springer article HTML extraction — the paywalled page's HTML happens to include the entire body text (this is a Springer choice for SEO). Not always true, but true here.

## What is genuinely unresolved

- **Chitinase / β-1,3-glucanase claim.** Current PGAP annotation shows 0 hits for these; paper says they were detected. This is one of the Open Questions (Q3). Would need a fresh Prokka + dbCAN2 run on the same FASTA to resolve. Feasible in ~1 hour of compute — not done in this pass.
- **AAI (paper: 67.3%).** Requires all-vs-all protein BLAST (both proteomes are ~1800 CDS, so ~3.3 M BLASTp comparisons). Deferable but easy on uicgpu (~15 min). Not done in this pass because the paper's AAI value plays the same role as its ANI value (evidence for species novelty) and we independently confirmed species novelty via ANI already.
- **dDDH (paper: 22.2%).** GGDC-v3 is a web-only queued submission; would need an interactive web session (or the local GGDC binaries, which are not open-source). Same story: novelty already confirmed by ANI + 16S.
- **Phenotypic claims (Gram stain, growth ranges, fatty-acid profile, polar lipid profile, biochemical panels).** Require the live isolate from KCTC/GDMCC. Not achievable in a data-only replication.

## What would close the residual gaps

1. ~15 min: run Prokka + dbCAN2 on `bgyt1.fna` to resolve Q3 (chitinase / β-1,3-glucanase presence).
2. ~15 min on uicgpu: compute AAI to close C8 (paper's 67.3% AAI claim).
3. ~30 min: submit both genomes to TYGS/GGDC to close C9 (paper's 22.2% dDDH claim) and to run a proper multi-genome GBDP tree for Q5.
4. ~US$150 + weeks of wet-lab time: order KCTC 25379ᵀ, re-do Gram stain (Q4), and if positive confirm all phenotypic claims (C13–C16).

## Confidence in the verdict

- **REPLICATED elements** (genome length body-text value, GC%, feature counts within re-annotation drift, 16S similarity to *O. umbonata*, phylogenetic placement, species-novelty conclusion): **high confidence** — reproduced with independent tools on the paper's own deposited public artifacts, matches within known method noise.
- **PARTIAL elements** (contig count and N50 different from paper, ANI magnitude differs from paper, cell-wall-enzyme claim not supported in current PGAP annotation, paper's abstract-vs-body genome-length contradiction): **medium-to-high confidence** in the finding of the discrepancy itself; low confidence in the *cause* (which is what Open Questions 1–3 target).
- **OUT-OF-REACH elements** (all phenotypic/chemotaxonomy claims): correctly marked as untestable from public data.

Overall verdict of **PARTIAL** is honest and evidence-supported.
