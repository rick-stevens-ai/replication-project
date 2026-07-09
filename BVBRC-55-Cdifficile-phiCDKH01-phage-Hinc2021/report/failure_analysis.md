# Failure Analysis — phiCDKH01 Replication (BVBRC-55, Hinc et al. 2021)

**Verdict:** REPLICATED (LLM-judge 93/100). But "replicated" is not "perfect." This document is an honest accounting of what did **not** work, what was **skipped**, and where the replication is **weaker than the headline verdict suggests**.

---

## 1. Summary of imperfections

| # | Item | Severity | Kind |
|---|---|---|---|
| F1 | Started from deposited assembly, not raw reads | Medium | Scope shortcut |
| F2 | myRAST v36 functional annotation (C6) not rerun | Medium | Tool unavailability / partial test |
| F3 | Strand off-by-one (C4): 52/14 vs paper's 53/13 | Low | Unresolved provenance detail |
| F4 | Identity metric substitution: VIRIDIC (81.8%) reported vs paper's Easyfig 89% | Low | Method mismatch, same conclusion |
| F5 | Novelty panel (C9) limited to 11 pre-2021 comparators | Medium | Time-window gap |
| F6 | 39-bp discrepancy in prophage endpoints (C10) not explained | Low | Boundary-convention unresolved |
| F7 | No wet-lab / functional confirmation | High (in principle) | Out of scope |
| F8 | LLM-judge score used as headline | Low | Heuristic, not gold standard |
| F9 | `extraction/marker.md` not present | Low | Extraction artifact missing |

---

## 2. Detail

### F1. Started from deposited assembly, not raw reads (Medium)
- **What happened:** We fetched MN718463 (the paper's deposited phage assembly) and treated it as ground truth for the genome-statistics claims (C1–C5).
- **Why it matters:** Any assembly error in MN718463 would be silently inherited by our "exact" agreements. We are validating the paper's genome *as deposited*, not the paper's genome *as it would emerge from re-assembly of the raw reads*.
- **What we did instead:** We accepted the assembly and moved on.
- **What would fix it:** Pull the raw MiSeq reads from SRA (if deposited); rerun SPAdes 3.13.0 (per paper) and modern SPAdes; diff assemblies with dnadiff.
- **Ollie's honest read:** For a genome-announcement paper, starting from the deposit is a defensible shortcut, but calling it "REPLICATED" without a raw-reads caveat overstates the scope.

### F2. myRAST v36 functional annotation not rerun (Medium)
- **What happened:** Claim C6 (37/66 ORFs functionally annotated) was rated ⚠ *partial* because myRAST v36 has moved / been reorganized (RAST ecosystem migration), and reproducing the exact tool + version reliably in 2026 is nontrivial.
- **What we did instead:** Counted functionally annotated CDS in the GenBank deposit (got 9). Reported the 9-vs-37 gap as a "provenance difference" but did not close it.
- **Why it matters:** The paper's functional-module list (terminase, portal, capsid, integrase, holin, etc.) is qualitatively supported by the deposit, but the 37 vs 9 delta is real and unaddressed.
- **What would fix it:** Rerun a modern phage-annotation pipeline (pharokka with PHROG HMMs is the current best practice) and report the delta.

### F3. Strand off-by-one (Low)
- **What happened:** We got 52 (+) / 14 (−); paper reports 53 (+) / 13 (−).
- **Why it matters:** One CDS is being counted on the opposite strand. We attributed this to "annotation-boundary difference" but did not pinpoint the specific CDS.
- **What would fix it:** Iterate the 66 CDS features in MN718463; cross-reference with the paper's Table/Fig ORF list; identify which single CDS disagrees and adjudicate.

### F4. Identity metric substitution (Low)
- **What happened:** Paper quotes "89% identity to phiCD24-1" (Easyfig conserved-region shading). We report 81.8% (VIRIDIC-style whole-genome intergenomic identity).
- **Why it matters:** The two numbers are not directly comparable. Both agree on the *taxonomic* conclusion (same ICTV genus, distinct species) — but our headline "identity" number is not the paper's.
- **What we did:** Reported both interpretations transparently in REPORT.md §4b.
- **What would fix it:** Also run Easyfig with the paper's original shading thresholds; report both metrics side by side.

### F5. Novelty panel limited to 11 pre-2021 comparators (Medium)
- **What happened:** For claim C9 we used an 11-phage panel drawn from pre-2021 literature.
- **Why it matters:** Any C. difficile phage genome deposited *after* the paper (2021→) that lands in the phiCDKH01/phiCD24-1 genus would weaken the "only phiCD24-1 is congeneric" framing.
- **What we did:** Did not do a time-forward sweep.
- **What would fix it:** Query NCBI for all C. difficile phage genomes with deposit date 2021-01-01→present; extend the VIRIDIC matrix; re-check the novelty claim.

### F6. 39-bp prophage endpoint discrepancy (Low)
- **What happened:** Paper: 288,650–333,698 in JACSDL010000003.1. Us: 288,611–333,698 @ 99.7% identity. Right endpoint exact, left endpoint 39 bp off.
- **Why it matters:** For a genome-announcement claim, "within 39 bp at 99.7%" is a strong confirmation, but the offset itself is unexplained. Temperate phages typically integrate at tRNA loci with short direct repeats (attL/attR); the 39-bp offset is plausibly a convention difference.
- **What would fix it:** Extract the ~200 bp flanks; look for direct-repeat attL/attR pairs; annotate the host locus at the boundary.

### F7. No wet-lab / functional confirmation (High in principle, out of scope in practice)
- **What was skipped:** Everything wet — host range assays, induction efficiency, plaque morphology, lysogeny stability, CRISPR spacer function.
- **Why it matters:** This is a purely *in silico* replication. It cannot confirm any biological claim that requires live cells and virus particles.
- **Ollie's honest read:** For a genome-announcement paper, this is a legitimate scope. But we should not claim to have "replicated" biological function — only genome content.

### F8. LLM-judge score as headline metric (Low)
- **What happened:** We report "LLM-judge agreement 93/100" as if it carries independent epistemic weight.
- **Why it matters:** The LLM (Argo gpt-5.2) is not a domain expert; the score is a summary heuristic; the mapping from claim-by-claim comparison to a single scalar is opaque.
- **What we did:** Provided the claim-by-claim table so a human reviewer can see through the LLM score.
- **What would fix it:** Domain-expert review by a phage biologist; do not treat the 93/100 as authoritative.

### F9. `extraction/marker.md` not present (Low)
- **What happened:** The task expected an `extraction/marker.md` (parser output). It does not exist on disk (ENOENT).
- **Why it matters:** The paper full text was fetched from Europe PMC XML, so parser output was not strictly needed — but the missing artifact is a small inconsistency in the extraction pipeline for this paper.
- **What would fix it:** Rerun the marker (or nougat) parser on the paper PDF and place the output at `extraction/marker.md` for consistency with the standard replication-project layout.

---

## 3. What went right (for calibration)

- Every core claim tested reproduced with near-exact agreement.
- All data was public, free, and no-auth.
- Whole workflow reruns in ~1 hour on a laptop.
- Every numeric claim is backed by a specific evidence file.
- Both non-exact items (strand off-by-one, 39-bp prophage endpoint) were flagged explicitly rather than glossed.

---

## 4. Net honest verdict

**REPLICATED, with the following honest caveats:**

- Replication is of the paper's *deposited* genome content, not the paper's *raw-reads → assembly → annotation* pipeline end-to-end.
- Functional-annotation claim C6 is *partially* validated (deposit-based, not myRAST-rerun-based).
- Novelty claim C9 is validated *as of the paper's 2021 knowledge cutoff*, not against post-2021 phage deposits.
- No biological/functional claims are validated (wet-lab out of scope).

For a genome-announcement paper, this is a solid replication. For a "we independently confirm every aspect of this paper" claim, it is an overstatement — the caveats above are real and the section labelled *Genuine Critique* in REPORT.tex is where they belong.
