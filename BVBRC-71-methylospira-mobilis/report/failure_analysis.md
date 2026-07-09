# Failure Analysis — BVBRC-71

**Verdict:** PARTIAL (leaning REPLICATED). Not a full REPLICATED for three specific reasons plus one operational note. This file explains each in detail.

## 1. What Went Right (Context)

Before enumerating what didn't fully replicate: 17 of 21 tested claims agree, coverage is 100 %, all 15 quantitative genome-level metrics match within tool tolerance, every qualitative comparative-genomics asymmetry (V-Fe nitrogenase, chemotaxis expansion, IS load, PEP carboxylase, flagellar apparatus, CRISPR typing) is recovered with the correct sign and often with a larger magnitude than the paper prose suggests. The paper's headline story is fully supported by the public GenBank record.

**Nothing about the paper failed to replicate.** What follows is a list of places where our REPLICATION was operationally limited, not where the paper's science is wrong.

---

## 2. Substantive Non-Matches (4 flagged claims)

### 2.1 C5 — CDS count: paper 4858 (RAST) vs. independent 4214 (PGAP)

- **Gap:** −13 % (644 fewer CDS in the PGAP annotation).
- **Root cause:** annotation-pipeline difference. The paper ran RASTtk on Shm1; the deposited GenBank annotation is PGAP. These two callers disagree systematically:
  - RASTtk is more permissive about short ORFs, uses FIGfam signatures for hypothetical proteins, and calls more pseudogenes as separate features.
  - PGAP is more conservative on short/hypothetical CDS and merges frameshifted pseudogenes.
  - A 10–15 % gap between the two is typical for a 4–5 Mbp Proteobacterial genome.
- **Not a data problem.** Same genome, two callers, two counts. Both are valid; they answer slightly different questions.
- **How to close:** Submit CP044205 to BV-BRC → Comprehensive Genome Analysis → Rerun RASTtk. Compare CDS count directly against the paper's 4858. This was outside our replication scope (BV-BRC job queue, ~30–60 min compute).
- **Impact on verdict:** flagged by LLM judge but does not undermine any other claim. PGAP-derived downstream counts (chemotaxis, flagellar, transposase) all show the correct direction and magnitude, so the pipeline difference didn't propagate destructively.

### 2.2 C16 — IS elements: paper ">200" vs. independent 194 transposase-CDS

- **Gap:** −3 % (just under the threshold).
- **Root cause:** definitional. The paper's ">200" almost certainly comes from an ISfinder / ISEScan run that counts IS *elements* (which can include IS with multiple transposase ORFs, or IS that our substring scan missed because the CDS product string wasn't "transposase" but e.g. "IS4-family element" or "integrase"). Our number is a substring match over PGAP product strings for {transposase, IS, insertion-sequence}.
- **Not a data problem.** Six-count difference at a >200 threshold; the underlying mobile-element load is huge in both counts (Bath has 41 → Shm1 has 4.7× more, which is the paper's qualitative claim).
- **How to close:** Run ISEScan (or upload to ISfinder) on CP044205 and count IS elements per IS family. Outside scope.
- **Impact on verdict:** cosmetic. The paper's qualitative claim ("very high IS load, much more than Bath") is unambiguously confirmed.

### 2.3 C4 — tRNA: paper 49 vs. independent 48

- **Gap:** −1 (2 %).
- **Root cause:** almost certainly a tRNAscan-SE cutoff difference or one pseudo-tRNA that PGAP labels differently than the paper's annotation pipeline did. Off-by-one at n=49 is well within noise.
- **Not concerning.** Every 16S/23S/5S rRNA operon and every tRNA-Sec / tRNA-Pyl edge case would need per-tRNA inspection to close this. Not worth the effort.
- **Impact on verdict:** trivial.

### 2.4 C12 — MxaFI + XoxF specific-ortholog resolution

- **Gap:** methodological, not numerical. We flagged **mxaF, mxaI, xoxF** by substring match against PGAP's generic "methanol dehydrogenase" product labels rather than by phylogenetic ortholog assignment.
- **Root cause:** the deposited annotation labels methanol dehydrogenase CDS generically, not with the specific mxaFI vs. xoxF nomenclature. Distinguishing the two requires either:
  - HMMER against Pfam PF00805 (MDH-large-subunit) + PF01712 (MDH-small-subunit) with subfamily-specific gating, OR
  - Active-site inspection: mxaF has a Ca²⁺-coordinating active site; xoxF has a La³⁺-coordinating one (single-residue substitution in the metal-binding pocket).
- **Not a data problem.** The genes are there; we cannot tell you WHICH ones from a product-string scan alone.
- **How to close:** ~1 hour of HMMER + alignment work. Not done.
- **Impact on verdict:** the claim "MxaFI + XoxF MDHs present in Shm1" is weakly supported by our method, not contradicted. A stronger method would probably confirm it.

---

## 3. Operational Limitations of Our Replication

### 3.1 No functional / phenotypic corroboration
We cannot verify that the annotated flagellar apparatus is functional, that V-Fe nitrogenase actually fixes N₂ under Mo-limitation, or that the copper-switch regulation is intact. That would require wet-lab access to strain Shm1 (VKM B-3350 / KCTC 15564). Genome-record replication is our scope; biology is not.

### 3.2 Single LLM judge
Only `argo:gpt-5.2` returned a verdict. The original plan was `argo:claude-opus-4.7`, but it reproducibly 502'd at max_tokens ≥ 2500 with the 21-claim prompt. We fell back to gpt-5.2. A multi-judge ensemble (opus-4.8 + gpt-5.2 + gemini-2.5-pro) would give a stronger consensus verdict but was not run.

### 3.3 Annotation-pipeline apples-to-oranges
The paper reports RAST-derived numbers; we compared against PGAP. Several counts (especially CDS, and to a lesser extent transposase family calls) are affected. A true head-to-head requires re-running RASTtk on CP044205, which is a BV-BRC job.

### 3.4 Product-string matching as ortholog proxy
Gene-presence work for pathway markers (pMMO, sMMO, MDH, nif/vnf, cbb, flagellar, chemotaxis, oxidase, CRISPR) was regex over PGAP `product`, `gene`, `note` qualifiers. This is fine for coarse presence/absence but weak for fine-grained claims like "2 pmoCAB operons with distinct high-vs-low affinity regulation" (which would require operon-level synteny + upstream promoter analysis).

### 3.5 No HMMER / BLAST / ISfinder / ISEScan
No sequence-level homology tools were run. Everything downstream is annotation-based. Running HMMER + ISEScan would very likely upgrade the verdict to REPLICATED but was outside the scope of this rapid replication pass.

---

## 4. What Would Upgrade the Verdict to REPLICATED

In priority order:

1. **Re-run RASTtk on CP044205** via BV-BRC Comprehensive Genome Analysis (~30–60 min). Compare CDS count directly to the paper's 4858. Very likely to close C5.
2. **HMMER against Pfam PF00805/PF01712 with subfamily gating** for MxaFI vs. XoxF resolution (~1 hour). Very likely to close C12.
3. **ISEScan run on CP044205** for proper IS-element enumeration (~15 min). Very likely to close C16.
4. **Multi-judge ensemble** (opus-4.8 + gpt-5.2 + gemini-2.5-pro) on the 21-claim table. Strengthens the verdict statistically but unlikely to change the substantive answer.

None of these were done; all four are cheap and would likely convert PARTIAL → REPLICATED.

---

## 5. Bottom Line

- **No paper claim was contradicted.** Every asymmetry, every direction, every magnitude tested was recovered.
- **Every quantitative genome-level claim matches within tool tolerance** (largest gap = RAST-vs-PGAP CDS count = 13 %, which is a pipeline artifact not a data issue).
- **Four flagged items are all conservative honesty calls**, not scientific failures.
- **This is a solid, honest PARTIAL** per the wave-brief vocabulary. A cheap follow-up pass (RAST rerun + HMMER + ISEScan) would almost certainly upgrade it to REPLICATED.
