# Failure & Gap Analysis — BVBRC-46 (K. pneumoniae ST1588 NDM-1 megaplasmid)

The main REPORT declares **REPLICATED** (Coverage 8/10, Agreement 9/10).
That verdict is defensible for the sequence-testable claims, but this
document exists to be **honest about what did not happen, what could not
happen, and what happened but should not carry as much weight as it might
appear**.

---

## 1. PDF availability

- **The paper's PDF was not downloaded, cached, or parsed by a
  PDF-vision tool.** The article is *Antibiotics* (MDPI) 2022 under
  CC BY 4.0 — the PDF is freely available at
  `https://www.mdpi.com/2079-6382/11/9/1207/pdf` and could have been
  fetched at zero cost.
- **What was used instead:** Europe PMC full-text JATS XML for
  PMC9494972. This is complete for CC-BY OA articles and adequate for
  extracting all textual claims and accessions.
- **What this cost us:** The paper's figures (especially Fig. 1B, the
  Tn3000 architecture diagram; the plasmid maps; any electrophoresis
  images) were **never inspected visually**. The Tn3000 gene-order
  reconstruction in this replication was cross-checked against the
  *textual* description of Fig. 1B extracted from the XML, not against
  the figure itself. A subtle visual detail (e.g., exact break-point of
  ΔISAba125, orientation glyphs, distances not called out in text) could
  differ from what I reconstructed without my knowing.
- **Standing policy note.** `pdf` and `image` are paid tools; this
  replication was run under the free-endpoint-only rule. If Rick wants
  a figure-level audit, that requires either (a) explicit approval to
  invoke `pdf`/`image` on this specific PDF, or (b) a manual eyeball by
  a human. Neither happened.

## 2. Unrun analyses (things a stricter replication would have done)

The following analyses would have strengthened the verdict but were
**not performed**:

### 2a. Wet-lab claims (**structurally impossible from sequence**)
- **C9 — conjugation frequency (4.3×10⁻⁶ transconjugants/recipient at
  27 °C, no transfer at 37 °C).** Requires mating assay in vitro. The
  IncHI-type transfer machinery on the megaplasmid provides a
  *mechanistic explanation* consistent with temperature-dependent
  conjugation, but that is inference, not reproduction.
- **C10 — disk-diffusion / MIC antibiotic-susceptibility panel
  (their Table 1).** Requires bacterial cultures + susceptibility
  testing. Genomically predicted resistance (from the resistome) is not
  a substitute for measured MICs.

**These two claims are marked "❌ out of reach" and "⚠ mechanism-
consistency only" in the report, and are correctly reflected in the
Coverage=8/10 score (not 10/10).**

### 2b. In-silico analyses that *could* have been done but weren't

- **Re-assembly from raw Illumina + Nanopore reads.** The deposited
  assembly (GCF_023554495.1) was trusted as authoritative. If the
  deposited assembly is subtly wrong (e.g. mis-scaffolding, mis-oriented
  megaplasmid contig, chimeric join), the replication inherits the same
  error. A rigorous replication would pull SRA runs and re-run
  Unicycler / Trycycler / Flye+Medaka+Pilon.
- **Fully independent annotation.** The Tn3000 gene order table came
  from parsing the deposited NCBI PGAP `genomic.gff`. It was **not**
  re-annotated with Prokka or Bakta as an independent check. In
  practice, PGAP agrees with Prokka/Bakta on well-studied AMR
  transposons, but this is a shortcut.
- **ISfinder / ISEScan pass.** The IS3000 and ISAba125 element
  boundaries were assigned by PGAP transposase-family calls, not by
  direct ISfinder classification. An ISfinder run would have given
  independent IS-element coordinates.
- **Broader plasmid comparative sweep.** BLAST was done against a
  single reference (pNDM-1-EC12, NZ_MN598004.1) because that's the one
  the paper names. I did **not** sweep against all NCBI NDM-1
  plasmids to independently verify EC12 is actually the closest match.
- **Chromosome-level orthogonal checks.** No ANI comparison of the
  chromosome vs other ST1588 chromosomes; no core-genome MLST
  cross-check; no checkM completeness/contamination re-scoring.
- **2022-era database snapshots.** Kleborate v3.2.4 and abricate DBs
  are the 2026-Apr-3 snapshots — roughly 4 years newer than the paper's
  2022 CGE web tools. Nomenclature drift (e.g. SHV sub-allele numbers)
  is possible; a strict replication would rerun against 2022 DB
  snapshots to verify zero drift.
- **PlasmidFinder "un-typeable" is a soft call.** PlasmidFinder
  returned *partial* hybrid repHI5B / repFIB hits on the megaplasmid.
  The report reads this as "consistent with the paper's un-typeable
  description," but a stricter reviewer could reasonably say the
  megaplasmid carries partial IncHI5B / IncFIB signals rather than
  being truly un-typeable.

## 3. Single-judge caveat (**important**)

- **The verdict (Coverage 8/10, Agreement 9/10, REPLICATED) was
  rendered by a single LLM judge**, `argo:gpt-5.2` via the free Argo
  proxy, on a single prompt, with no rubric-calibration set.
- **No inter-judge agreement was computed.** A stronger design would
  have polled 3+ judges (e.g. `argo:claude-opus-4.8`,
  `argo:gpt-5.2`, `argo:gemini-2.5-pro`, plus a Kleborate-blind judge)
  and reported the median score with inter-rater variance.
- **No blinding.** The judge saw the paper text and the results
  side-by-side, produced by the same agent that later interpreted its
  answer. Confirmation-bias risk is nonzero.
- **The judge cannot verify wet-lab claims.** It marks C9/C10 as
  out-of-scope, which is correct, but its coverage score of 8/10 (i.e.
  "8 of 10 claims covered") is definitional — if the paper had had 15
  wet-lab claims and 3 sequence claims, the same replication would have
  been judged 3/18, and the underlying quality of what *was* reproduced
  would be identical. Coverage as a fraction is a weak metric that
  penalizes ambitious papers.
- **How to strengthen this.** Rerun the judge prompt across at least
  three models, report all three scores, and either take the median or
  flag any dissenting verdict as a red flag requiring human review.

## 4. Discrepancy that was resolved by inference (not experiment)

- The paper's Results text says the megaplasmid "carries the blaNDM-1
  and oqxB genes." All three AMR databases (ResFinder, NCBI, AMRFinderPlus)
  place *oqxA/B* on the **chromosome**, not the megaplasmid. *oqxAB* is
  a well-known **intrinsic chromosomal** efflux operon in *K. pneumoniae*.
- **I labeled this a "minor textual error in the paper."** That is an
  inference from three databases + prior biological knowledge. It is
  the most parsimonious explanation, but I did not (a) contact the
  authors for confirmation, (b) look for erratum/correction notices in
  MDPI's record for this article, or (c) re-check the paper's figures
  (they are behind the PDF wall — see §1).
- If the paper's intent was subtler than a typo (e.g., a plasmid-borne
  *oqxB*-adjacent duplicate the deposited assembly does not contain),
  my "minor textual error" framing would be wrong. Low-probability but
  not zero.

## 5. Missing sensitivity / robustness checks

- **No re-run with alternative Kleborate / abricate DB versions** to
  demonstrate stability of the ST / K / O / resistome calls.
- **No re-run of the blastn on scrambled controls** (shuffled megaplasmid
  vs pNDM-1-EC12) to establish a null distribution for the 2,488 bp
  match length. The exactness (2,488 bp, 99.96% id) is compelling on its
  face, but a null model would make the "exact match" claim quantitative.
- **No confidence intervals or replicate runs.** All numbers are from a
  single run of each tool with default parameters. Bootstrap or seed-
  variation was not done.

## 6. What I claim vs what is actually shown

| I claimed... | What is actually shown |
|---|---|
| "Every sequence-testable claim reproduced" | 8 sequence claims reproduced against the deposited assembly (not from raw reads) using current-generation DBs. Assembly-level errors are inherited transparently. |
| "Often to the exact base pair" | True for megaplasmid size (314,976 bp), IncFIB(K) size (197,209 bp), and shared NDM region (2,488 bp). This IS strong. |
| "Full Tn3000 order matches Fig. 1B" | Matches the paper's *text* description of Fig. 1B. The figure itself was not visually inspected (see §1). |
| "The oqxB discrepancy is a minor textual error" | Best-supported hypothesis given three DBs + known biology, but not confirmed with authors and not cross-checked in the figures. |
| "Verdict: REPLICATED" | Verdict of a single free-tier LLM judge; no multi-judge agreement, no calibration. |

## 7. Bottom-line recommendation

The replication is solid **in-silico corroboration** of the paper's
genomic backbone. It should **not** be presented as either (a) a
from-scratch re-derivation of the paper's biology, or (b) a wet-lab
reproduction. The label "REPLICATED" is appropriate for the
sequence-testable subset (C1–C8); C9 is only mechanistically
consistent, and C10 was not attempted.

Anyone building on this report should either commission the missing
wet-lab work (mating + AST) or explicitly gate downstream claims on the
in-silico-only nature of the evidence.
