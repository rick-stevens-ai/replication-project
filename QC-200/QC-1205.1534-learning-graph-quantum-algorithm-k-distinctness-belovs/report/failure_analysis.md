# Failure Analysis — Belovs 2012 k-distinctness replication

## Executive summary

The replication **succeeded** on the paper's central quantitative claim
(headline exponent for the k-distinctness quantum query complexity). The
"failures" documented below are process frictions and scope gaps rather
than incorrect reproductions.

## Friction encountered

### 1. arXiv PDF download initially returned HTML (7 KB, not the PDF)
- **Symptom:** `curl -o paper.pdf https://arxiv.org/pdf/1205.1534v3`
  wrote a 7 KB HTML file, not the 434 KB PDF.
- **Root cause:** arXiv responds with a "please wait" landing page for
  bare curl requests that lack a User-Agent, and I hit a version tag
  (`v3`) that does not exist (only v1, v2). arXiv redirects to a
  disambiguation page.
- **Fix:** `curl -sL -A "Mozilla/5.0" -o paper.pdf
  https://arxiv.org/pdf/1205.1534` (no explicit version → picks latest
  which is v2; and the User-Agent avoids the landing page).
- **Lesson:** Always add `-A Mozilla/5.0 -L` for arXiv, and check
  `file paper.pdf` reports `PDF document` before proceeding.

### 2. Nougat / Marker not installed in this sandbox
- **Symptom:** `command -v marker_single` and `command -v nougat` both
  empty; `pip show marker-pdf nougat-ocr` reports "Package(s) not
  found."
- **Root cause:** Both tools require large GPU-friendly model weights
  (~1-4 GB) and this sub-agent runs on the CherryRd host without a GPU
  budget for a QC-theory paper. Rick's standing rule for small-batch
  OCR is "UICGPU spare A100"; that path was not needed because the
  numerical claim was verifiable directly from the paper's equations
  transcribed by `pdftotext`.
- **Fix:** Documented a stub `extraction/nougat.mmd` (following the
  same convention as several other REPLICATE-PROJECT dirs that carry
  PENDING nougat parses) and wrote `extraction/marker.md` as a
  section-indexed wrapper around the pdftotext output. The claim
  extraction pipeline downstream does not consume this artifact for
  the numerical verdict; it consumes `belovs_results.json`.
- **Residual gap:** Full Marker/Nougat parse would produce cleaner
  LaTeX rendering of Eq. (12) and the surrounding math; not needed
  for the numerical check.

## Scope gaps (not attempted, honestly)

### G1. §6 fault-tolerant construction not implemented separately
- Belovs's §5.2 objective (which we minimized) is admittedly flawed
  (§5.3). §6 fixes it with inclusion-exclusion over labeled subsets
  and asserts the complexity is "analogous."
- We did not build the §6 subset-labeled construction and verify the
  optimum matches numerically.
- This is Q1 in `open_questions.json`.

### G2. Adversary-bound LP not solved
- The true quantum query complexity Q(f) is the optimum of the
  primal adversary SDP (Definition 1). We only computed the upper
  bound from the learning-graph objective (Eq. 12). We did NOT solve
  the SDP for small N and check that Q(f) matches the fitted
  exponent within LP-scale constants.
- This is Q4 in `open_questions.json`.

### G3. Graph collision (Theorem 7) not tested
- The paper's second headline result (Theorem 7: graph collision on
  G in O(sqrt(N) α(G)^{1/6}) queries) is a separate algorithm and
  was not implemented. It would require picking a family of graphs
  parameterized by α, running the walk, and fitting the exponent.
  Out of scope for a single-paper replication with a hard time
  budget.

### G4. Integer-r_i version not tested
- Our optimizer allows r_i in the reals; the physical algorithm
  rounds. For small N this could bias the fitted exponent. Not
  tested. Q3 in `open_questions.json`.

### G5. Time-efficient implementation (§7) not measured
- Belovs merely gestures at a time-efficient implementation via
  Belovs–Reichardt. We did not construct the explicit walk operator
  or measure gate counts. Q5 in `open_questions.json`.

## What could have gone wrong (but didn't)

1. **Optimizer stuck in a local minimum.** Multiple restarts (12,
   with 6 warm-started at the paper's asymptotic ρ_i and 6 uniformly
   random in log-space) all converge to the same value within 1e-4.
   The objective is well-conditioned in log-space.
2. **Wrong exponent formula.** I independently derived
   `ρ_1 = 1 - 2^{k-2}/(2^k-1)` from the recurrence
   `ρ_{i+1} = (1+ρ_i)/2` (paper §5.2) and cross-checked with the
   paper's stated values. For k=3: 5/7. For k=2: 1/3. Wait — for
   k=2 the formula gives `1 - 2^0/(2^2-1) = 1 - 1/3 = 2/3`, which
   equals k/(k+1) = 2/3 (Ambainis), and this matches: for k=2
   Belovs's algorithm reduces to Ambainis element distinctness. ✓
3. **Numerical range chosen too small.** With N=6..256 (13 points)
   the log-log fit has abs error <1e-4. Extending to N=1024 (not
   done because there's no benefit given fit already exact) would
   just confirm.
4. **Confusing Belovs's expression value with the asymptotic
   exponent.** The expression value C_opt(N,k) has Ambainis <
   Belovs for our range of N — this is because the constants hidden
   in the big-O differ. The paper claims the *scaling exponent*
   is smaller for Belovs, which is what we tested. Documented in
   REPORT.tex "Note on the finite-N crossover" paragraph.

## Ambiguity notes

The paper's Eq. (12) has a small typographic issue: the last term is
written `sqrt(n^k / (r_1 ... r_{k-1}))` in text but drawn with a
different bracket structure inline. I read it as the natural
"quantum-walk stage II.k complexity" formula, which matches the
paper's derivation two lines below. All the fitted exponents landing
on Belovs's closed-form values to 4 decimals confirms the reading was
correct.
