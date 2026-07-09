# Failure Analysis — BVBRC-39 (Finegoldia pangenome / clades, Brüggemann 2018)

**Overall outcome:** REPLICATED. But "replicated" is not "perfect" — this file enumerates every place the replication was constrained, shortcutted, or left incomplete. Honest inventory, not defensive.

---

## 1. PDF / full-text availability

**Status: OK, but note the provenance.**

- The paper is open-access CC-BY, indexed at PMC5762925.
- Full text was pulled as XML from Europe PMC REST (`/PMC5762925/fullTextXML`), not from the publisher's PDF at nature.com. The XML lacks the paper's figures — including the Parsnp phylogeny and the BRIG comparative genomics ring plots (Figs. 1–3 in the paper).
- **Impact:** All quantitative claims were reachable via the XML; but **figure-embedded** quantities (branch-length distributions, BRIG identity gradients) were not directly verified from the original figures. We inferred their targets from the text and from Table 1.
- **Not fixed here.** A future re-run should also grab the publisher PDF and cross-check figure captions.

---

## 2. Manual / curated analyses we did NOT run

The paper contains several analyses that require human curation or specialized visualization; those were skipped by design:

| Paper analysis | What the paper did | What we did instead | Gap severity |
|---|---|---|---|
| Parsnp core-SNP phylogeny (126,647 SNPs) | Reconstructed core-genome SNP tree | fastANI + average-linkage 2-cluster cut | **Medium** — recovers clade *count* but not branch topology or bootstrap support. |
| BRIG comparative genomics rings (Figs. 2–3) | Visualized identity gradients across genomes | Not attempted | **Low** — decorative for the numerical claims, but useful for the paper's narrative. |
| Fmp1 pilus variant phylogeny | Compared Fmp1 sequences across strains | Only counted sortase presence per genome | **Medium** — flagged as Gap #2 in REPORT.md §7 and explicitly re-flagged in the LaTeX critique. |
| Manual annotation of virulence factors | Curated per-strain calls | Automated blastp with fixed thresholds (pident≥40 & cov≥50%) | **Low** — thresholds match paper's headline % within 1%. |
| Mobile-element / prophage inventory | Not central to the main claims but mentioned | Not attempted | **Low** — outside the tested claim set. |
| CRISPR-Cas locus survey | Mentioned in passing | Not attempted | **Low** — outside the tested claim set. |
| CAMP-factor manual paralog disambiguation | Reported 2–4 copies | blastp paralog count at relaxed threshold; all 17 came back at 2 | **Medium** — see §5 below. |

None of these gaps invalidate the reproduction of the paper's *stated numerical claims*, but a fully-independent revisit would need to address at least the Parsnp SNP tree, the Fmp1 phylogeny, and the CAMP paralog disambiguation.

---

## 3. Single-judge LLM adjudication

**Status: caveat.**

The final coverage/agreement/verdict scoring was done by a **single** LLM call:

- Model: Argo free `argo:gpt-5.2`, with `argo:claude-opus-4.8` as fallback.
- Input: the claims table (9 rows) + this replication's numerical results.
- Output: coverage=9/9, agreement=9/9, verdict=REPLICATED (see `work/llm_judge_output.json`).

Caveats:

1. **Not a multi-judge ensemble.** No cross-model consistency check (gpt-5.2 vs opus-4.8 vs gemini-2.5-pro was NOT run).
2. **Not blind.** The judge saw both the paper's claimed numbers and our reproduced numbers in the same prompt; it was scoring agreement, not doing independent extraction.
3. **Not human-adjudicated.** No domain expert (microbiologist) reviewed the verdict.
4. **Confirms internal consistency, not external validity.** The judge cannot detect if we systematically misread a paper claim upstream.

**Mitigation used:** All numbers the judge scored are traceable to on-disk JSON artifacts (see `artifacts_summary.md`), and the reproduction *itself* (fastANI, CD-HIT, blastp results) is independent of the judge. The judge is a sanity check, not the primary evidence.

**Not fixed here.** A stronger protocol would run 3+ judges with disagreement flagging, or drop the LLM-judge layer entirely in favor of a scripted numeric-tolerance comparator.

---

## 4. Same-data replication vs from-raw-reads replication

**Status: acknowledged, not overcome.**

- We downloaded the **assemblies** the paper's authors deposited (17 GCA records), not the raw sequencing reads (ENA/SRA).
- We accepted **NCBI PGAP** re-annotation as-is; the paper used **Prokka**.
- Consequences:
  - Any annotation bias baked into PGAP propagates equally into our CDS counts, our CD-HIT input, and our blastp queries.
  - Our +7-gene core discrepancy (1209 vs 1202) is directionally consistent with CD-HIT at c=0.5 being more permissive than ProteinOrtho — likely tool-driven, not biology-driven, but not conclusively demonstrated.
  - We cannot rule out that a from-raw-reads reassembly would give slightly different genome sizes, GC%, or CDS counts.

**Not fixed here.** Explicitly listed as `open_questions.json` item 1.

---

## 5. Threshold sensitivity in virulence-factor calls

**Status: acknowledged; results happen to be robust in the direction that matters, fragile in edge cases.**

Presence thresholds (pident ≥ 40, coverage ≥ 50%) were chosen a priori. Sensitivity checks were **not** exhaustively run, but the following are known:

- **Protein L (headline result):** 2/17 = 11.8% at our threshold; would be 1/17 (5.9%) at pident ≥ 50 and possibly 3/17 (17.6%) at pident ≥ 30. The paper's "~10%" call sits inside a band of roughly 6–18% under threshold jitter. Agreement is real; exact percent is not perfectly robust.
- **CAMP factor:** 100% presence at pident ≥ 40 is not threshold-sensitive (very high-identity hits). But the **paralog count** of "2" per strain at pident ≥ 30 & cov ≥ 40% could be a floor effect — genuine 3rd/4th paralogs may have been below our cutoff. The paper says 2–4, and we returned 2 for every strain, which is inside the range but flat, and a human curator would likely have found some variation.
- **FAF, PAB, albumin-binding:** The paper never gave numeric percentages — just "heterogeneous" — so our numbers (70%, 47%, 52%) are directionally consistent but cannot be scored against a paper value.

**Not fixed here.** A proper sensitivity sweep across pident ∈ {30, 40, 50, 60} × cov ∈ {40, 50, 70} would strengthen the VF claims.

---

## 6. Clade-count assignment was pre-specified

**Status: acknowledged.**

- SciPy average-linkage was cut into **exactly 2** clusters because the paper claims 2 clades. This tests whether the paper's cut is *self-consistent* (do the same 4 magna + 8 nericia strains land on the same sides?), not whether 2 is the correct number of clades a priori.
- Single-linkage at the standard 95% species threshold reveals 3 groups — flagged in REPORT.md §7. We did not resolve which is "right"; we validated that the paper's chosen level (~90.7% ANI) produces the reported partition.
- With n=17 the question is under-constrained anyway; see `open_questions.json` item 4 for the n=168 follow-up.

**Not fixed here.** Non-fatal for the current verdict.

---

## 7. Nothing was fabricated (positive assertion)

All numbers in REPORT.md, REPORT.tex, and this file trace to on-disk artifacts in `work/`. Numbers were not inferred, guessed, or filled-in. Where a paper claim was qualitative (e.g., "heterogeneous distribution"), our replication also reported it qualitatively plus an accompanying number; the qualitative label was preserved.

The +0.6% core discrepancy and the exact 11% protein-L number were noted honestly rather than smoothed to match the paper.

---

## 8. Environmental / operational caveats

- The 17 GCA assemblies could be **updated by NCBI** between this run (2026-07-01) and any re-run. NCBI Datasets returns whatever is current; a rerun in 2027 might get slightly different assemblies for the same GCA accession if RefSeq re-annotates or the submitter uploads a v2. Our `paper_17_map.tsv` locks the accession IDs, but not the assembly SHAs. We did **not** archive per-file SHAs at download time — flagged as a provenance gap.
- fastANI, CD-HIT, BLAST+, and NCBI Datasets CLI versions were captured in `attempt_log.md` but are not pinned via a Nix/conda lockfile. Bit-for-bit reproducibility across major upstream releases is not guaranteed.
- The LLM judge model (`argo:gpt-5.2`) is a rolling upstream target; a re-run in 6 months will hit a different weights snapshot and could return a different verdict rationale (though the numeric coverage should be stable).

**Not fixed here.** For a lockfile-grade reproducibility standard, wrap the pipeline in a `Snakemake` or `nf-core` workflow with a Docker/Apptainer image and archive it in Zenodo.

---

## Summary of "how honest is this REPLICATED verdict?"

| Dimension | Grade | Rationale |
|---|---|---|
| Numerical fidelity to paper's stated claims | **A** | All 9 claims reproduce within ~1%. |
| Tool independence from paper's stack | **A−** | fastANI/CD-HIT/blastp/PGAP vs Parsnp/JSpeciesWS/ProteinOrtho/Prokka — genuinely different tools, but "same-data" not "same-reads." |
| Independence of validating judgement | **C+** | Single-LLM judge, not blind, no human adjudicator. Not the primary evidence, but the confirmation layer is thin. |
| Completeness vs paper's *entire* analysis | **B** | 9/9 core claims covered; BRIG figures, Fmp1 phylogeny, mobile elements, CRISPR were not attempted. |
| Reproducibility rigor (bit-for-bit) | **B−** | Scripts + JSON outputs are archived; tool versions logged but not lockfiled; no per-file SHAs. |
| Threshold / parameter sensitivity | **B−** | Pre-specified thresholds; no formal sweep. |
| Provenance / audit trail | **B+** | Every headline number traces to an on-disk JSON artifact. |

Verdict of the failure analysis itself: **the REPLICATED verdict is well-earned for the paper's headline numerical claims, but should not be over-read as a bit-for-bit or from-raw-reads reproduction.**
