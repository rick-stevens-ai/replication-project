# Failure Analysis --- Honest Assessment
_Backfilled 2026-07-05. Read alongside `REPORT.tex` §Critique._

## Verdict framing (up front)
The stored verdict is **REPLICATED**, but that verdict is scoped to the
in-silico slice only: 6 of 22 paper claims verified, 1 partially contradicted,
15 not tested (wet-lab). Calling the paper as a whole "replicated" at 31.8%
claim coverage overstates confidence. A more accurate label is
**"IN-SILICO SLICE REPLICATED; PAPER AS A WHOLE NOT REPLICATED"**.
The verdict is being kept as `REPLICATED` for cross-set consistency (BVBRC set
verdict convention is per-slice), but this document is where the honest
qualifier lives.

## What actually failed (in the paper --- surfaced by the replication)

### F-P1. DyP K279a-only claim contradicted at gene level
- **Paper claim (C4):** "Encapsulating protein DyP-type peroxidase and
  ferritin-like protein oligomers were only detected in K279a."
- **What we found:** The DyP gene (PLfam `PLF_40323_00040048`) is present in
  all four genomes under modern RASTtk. The subsystem call the paper cites
  no longer exists for any of the four.
- **Root cause (candidate):** RAST subsystem ontology reorganisation between
  2018 classic RAST and 2026 RASTtk. Cannot be settled without the 2018 SEED
  subsystem JSON, which is no longer queryable.
- **Residual gap:** Q1 (open questions).

### F-P2. Paper never identifies its own siderophore
- **Paper claim (C18):** "S. maltophilia secreted catechol-type" siderophore
  (Arnow's; "data not shown"). Paper's Discussion cites earlier work claiming
  hydroxamate-type ornibactin for S. maltophilia --- an unresolved internal
  inconsistency.
- **Root cause:** Paper stopped at Arnow's class-level assay; no LC-MS/MS
  identification, no BGC prediction.
- **Residual gap:** Q2.

### F-P3. Mechanism for "transferrin = top iron source" missing
- **Paper claim (C19):** Transferrin gives maximal growth (p<0.001).
- **Contradicting internal evidence in the paper:** the 17-target set
  contains no TbpA/TbpB/LbpA/LbpB homologs. The positive control
  N. meningitidis uses TbpAB/LbpAB and is not comparable.
- **Root cause:** paper never asks how S. maltophilia liberates iron from Tf.
- **Residual gap:** Q4.

### F-P4. Genotype -> virulence linkage never crossed
- **Paper claim (asserted but not tested):** iron-acquisition genes contribute
  to pathogenicity of S. maltophilia. Paper's own concluding sentence: "These
  data need to be further confirmed through several knockout studies."
- **Root cause:** paper is a descriptive genotype/phenotype study, not a
  causal one. No mutants constructed.
- **Residual gap:** Q5.

### F-P5. Environmental n=5 is a weak base for the ecotype claim
- **Paper claims (C8/C9/C17):** clinical isolates >> environmental for gene
  presence, siderophore production, and inducibility.
- **Weakness:** only 5 environmental isolates (LMG*). Claim of ecotype
  difference is very sample-size-fragile.
- **Compounded by:** primer sequences were designed on the 4 in-silico
  genomes; environmental amplification failure could be primer artifact.
- **Residual gap:** Q3.

## What actually failed / was skipped (in the replication)

### F-R1. No independent re-annotation
- **What:** Replication trusts BV-BRC-served RASTtk annotations. No local
  RASTtk/Prokka/Bakta run.
- **Impact:** If BV-BRC has a stale annotation snapshot for any genome, the
  replication silently inherits it. No annotation-date captured in evidence.
- **Fix cost:** medium (few CPU-hours per genome for Bakta). Not blocked.

### F-R2. HmuT ortholog call is soft in R551-3 / JV3
- **What:** PLfam did not resolve HmuT in R551-3 and JV3; fell back to keyword
  search on functional-role text.
- **Impact:** two proteins with same functional label are not necessarily
  orthologs. No reciprocal best-hit BLAST run.
- **Fix cost:** cheap (minutes with DIAMOND). Not done.

### F-R3. Locus-tag mapping validated only by table lookup
- **What:** `SMLT_RS*` -> `Smlt*` mapping used NCBI GFF; not cross-checked by
  amino-acid identity.
- **Impact:** silent propagation of any GFF misannotation.
- **Fix cost:** cheap. Not done.

### F-R4. No siderophore biosynthetic-cluster analysis
- **What:** antiSMASH / PRISM never run on the 4 genomes.
- **Impact:** phenotypic Arnow's-positive result (F-P2) is never given a
  candidate genotype from the replication side either.
- **Fix cost:** small (antiSMASH ~30 min/genome on a laptop).
- **Now tracked as Q2.**

### F-R5. Population-genomic extension not run
- **What:** Testing the 17-target set across the full BV-BRC S. maltophilia
  panel (>200 genomes as of 2026) is one query away.
- **Impact:** F-P5 (n=5 environmental) cannot be resolved without it.
- **Fix cost:** small; single script.
- **Now tracked as Q3.**

### F-R6. Nougat parse is a stub
- **What:** `extraction/nougat.mmd` is a placeholder with sha256 + DOI; no
  actual GPU parse of the paper.
- **Impact:** table extraction quality via Marker fallback is degraded
  (pdftotext, not real Marker).
- **Fix cost:** medium (GPU allocation on uicgpu / Polaris + corpus sweep).
- **Fix path:** whenever the next SCOUT/OSTI Nougat batch runs, drop the real
  .mmd in over the stub.

### F-R7. Marker parse is pdftotext-fallback, not real Marker
- **What:** `extraction/marker.md` is layout-preserving pdftotext.
- **Impact:** Tables 1, 2, 3 lose structure (see marker.md output).
- **Fix cost:** small (`marker_single` on any host with the model cached).
- **Fix path:** same as F-R6.

### F-R8. `data/k279a_iron_subsystems.json` is nearly empty
- **What:** File is only 3 bytes (`{}` or similar).
- **Root cause:** intermediate cache that got clobbered / never populated;
  downstream analysis used `data/iron_subsystems_all.json` instead.
- **Impact:** none on final results; but a code-hygiene issue.
- **Fix cost:** trivial (re-derive from all-genomes JSON by filtering on
  genome_id `522373.48`). Not done here to preserve original artifact set.

## Confidence Assessment

| Component | Confidence | Why |
|-----------|-----------|-----|
| 4-genome roster (C7) | HIGH | Direct accession lookup, no ambiguity. |
| 2 subsystems present (C1--C3) | HIGH | Direct API return; both present in all 4. |
| 17-target roster in K279a (C6) | HIGH | 17/17 mapped SMLT_RS -> Smlt with matching role. |
| Fur in all 4 (C5) | HIGH | Direct annotation, redundant hits. |
| DyP K279a-only (C4) | LOW | Contradicted at gene level; subsystem call gone. |
| Comparative presence 17x4 | MEDIUM | HmuT soft in 2 strains; no RBH check. |
| Wet-lab claims C8--C22 | NIL | Not attempted. Cannot be, from database alone. |
| Paper's overall biological story | LOW-MEDIUM | Untested causal (Q4, Q5); un-resolved siderophore identity (Q2); ecotype claim fragile (Q3). |

## What Would Be Needed to Close the Gaps

1. **A wet-lab collaborator with S. maltophilia culture capability** to touch
   Q1/Q2/Q5 --- the mechanistic questions.
2. **Access to the 2018 classic-RAST SEED subsystem JSON** for these 4 genome
   IDs to settle Q1 non-empirically. If SEEDtk still ships the 2018 subsystem
   snapshot, ~1 day of work.
3. **antiSMASH + primer-coverage scripts** as one-off in-silico extensions to
   settle Q2 (candidate BGC) and Q3 (primer artifact vs biology). Cheap.
4. **Real Marker + Nougat parse of the PDF** via central corpus sweep to
   replace the stubs in `extraction/`.
5. **Reciprocal best-hit BLAST/DIAMOND** across the 4 genomes for the 17
   targets to firm up F-R2 / F-R3 (HmuT + locus-tag mapping softness).
