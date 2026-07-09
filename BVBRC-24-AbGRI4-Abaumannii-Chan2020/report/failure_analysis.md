# Failure & Limitation Analysis — BVBRC-24 (AbGRI4 / *A. baumannii* / Chan 2020)

The verdict is **REPLICATED**, but "replicated" is never "everything worked flawlessly". This
document catalogues the concrete failures, near-failures, and self-imposed limitations of this
replication, so downstream readers know exactly which parts of the paper's story this project does
and does not underwrite.

---

## 1. Actual failures encountered

### 1.1 PlasmidFinder returned zero hits across all six genomes
- **Symptom.** `data/abricate/plasmidfinder.tsv` is essentially empty (header + no data rows,
  122 bytes on disk).
- **Root cause.** The PlasmidFinder database is developed and curated for *Enterobacteriaceae*
  replicon typing. *Acinetobacter* plasmid replicons (Rep_3, RepAci-family, etc.) are not
  represented, so absence of hits is a **database-scope artefact**, not biological evidence that
  the isolates lack plasmids.
- **Impact on verdict.** None. The core AbGRI4 claim is about gene content and lineage, not
  plasmid replicon typing. The paper itself does not hinge on PlasmidFinder-catchable replicons.
- **Fix if this ever needed to be resolved.** Substitute an *Acinetobacter*-aware caller: MOB-suite
  for mobility typing, or a dedicated *Acinetobacter* rep-type DB (e.g. from Bertini *et al.*).
  Tracked in `open_questions.json` OQ2.

### 1.2 Prior backfill attempt token-exhausted at ~3m19s
- **Symptom.** A first pass at generating this exact set of report items ingested ~466K input
  tokens from raw sequence files (`work/*.fna`, `work/*.gb`) before it could finish writing.
- **Root cause.** No context-diet policy. The agent read genomes into context to "look at the
  evidence" instead of trusting the summary tables (`data/abricate/ncbi.tsv`, `REPORT.md`).
- **Impact on verdict.** None (verdict is written elsewhere), but it wasted a full run and delayed
  the backfill by one turn.
- **Fix applied.** This second pass runs under a **hard context-diet rule**: only `REPORT.md`,
  small `report/` subfiles, and small evidence TSVs may be read; no FASTA / GenBank files. Budget
  ≤ 100K tokens.

## 2. Self-imposed scope limitations (design decisions, not failures)

Each is a deliberate choice, and each carries a residual risk that the reader should know about.

### 2.1 Did not re-run de novo assembly
- **What was skipped.** Unicycler on raw Illumina + ONT reads for the four ABUH isolates.
- **Why.** All four assemblies are already finished (complete chromosome + closed plasmids) in
  RefSeq. Re-running Unicycler would burn substantial compute for a byte-identical (or
  near-identical) result on already-finished genomes.
- **Residual risk.** RefSeq curation may differ from the paper's exact deposited assembly. Small
  differences (masking, N-runs) cannot be ruled out without md5 verification against the paper's
  deposited FASTA. In practice, gene-content calls at ~90 % coverage / ~90 % identity are
  insensitive to this level of noise.

### 2.2 Did not re-run RAxML phylogeny or Gubbins recombination filtering
- **What was skipped.** The global-context phylogeny of *A. baumannii* IC lineages and its
  recombination-filtered variant.
- **Why.** These concern the phylogenetic / phylogeographic framing of AbGRI4, not the AbGRI4
  gene-content core claim. The paper's titular contribution is the definition and per-isolate
  assignment of the island, which is what this replication was designed to adjudicate.
- **Residual risk.** The paper's phylogenetic / dispersal claims (which IC2 sub-clade the ABUH
  strains belong to, when AbGRI4 was acquired in the tree, etc.) are **not adjudicated** by this
  replication. A downstream user who cares about those claims must consider them unverified here.

### 2.3 Did not re-run susceptibility (MIC) testing
- **What was skipped.** Any wet-lab or laboratory susceptibility measurement.
- **Why.** Out of scope for a computational replication.
- **Residual risk.** Genotype-to-phenotype concordance is asserted only where the paper itself
  asserts it. If any reported MIC is discordant with the genotype we recovered, we would not
  detect that here.

### 2.4 Did not perform structural / synteny analysis of the AbGRI4 island
- **What was skipped.** Base-pair-level extraction of the AbGRI4 integron, `intI1` + `attC`
  cassette architecture, insertion-site TSDs, IS flanking, and pairwise alignment of the island
  region across the three AbGRI4⁺ isolates.
- **Why.** ABRicate presence/absence is sufficient to verify the paper's gene-content claim, and
  structural annotation adds substantial complexity for marginal gain relative to the core claim.
- **Residual risk.** We verified *presence* of the AbGRI4 gene triad, not *identity of the island
  as a single mobile element*. It is formally possible (though unlikely) that the three
  AbGRI4⁺ isolates carry independently-acquired class-1 integrons with the same cassette in
  different genomic contexts — see `open_questions.json` OQ5.

### 2.5 Did not orthogonally test AbGRI4 *novelty*
- **What was skipped.** A systematic search of public *A. baumannii* genomes for the AbGRI4
  cassette + integron + insertion-site combination.
- **Why.** Novelty is a claim about the *reference set* (all previously described RIs), not
  about the four ABUH genomes; verifying it would require a project of comparable scope to the
  original paper.
- **Residual risk.** If a prior study had described the same island under a different name, this
  replication would not detect that. Tracked in `open_questions.json` OQ1.

## 3. Independent-judge risk

- **Single judge.** The independent LLM judge was run once (gpt-5.2), returning
  coverage 9/10, agreement 9/10, no contradicted claim.
- **Failure mode.** A single-judge run means the meta-verdict inherits the failure modes of that
  one model (e.g. specific hallucination patterns, DB cutoff timing).
- **Mitigation.** For higher-stakes claims, a two-model judge (gpt-5.2 + Claude-Opus-4.8 via Argo,
  both free endpoints) would harden the meta-verdict. Not done here to keep the replication
  low-cost; would be straightforward to add.

## 4. What would flip the verdict?

The verdict of **REPLICATED** would need to be revised if any of the following were shown:

1. The AbGRI4 marker triad (`aadB` + `aadA2` + `sul1`) is **absent** from any of ABUH763 / 793 / 796
   in the current RefSeq assemblies, **or** is **present** in ABUH773. Neither is the case in
   `data/abricate/ncbi.tsv`.
2. The Pasteur MLST call for any of the four ABUH isolates is **not ST2**. All four typed as
   ST2 in the rerun.
3. A previously published *A. baumannii* resistance island is shown to be sequence-identical to
   AbGRI4 (which would demote "novel" to "reobserved"). Not tested here — see OQ1.

If any of the above later proves true, this project's verdict should be revisited.

## 5. Bottom line

Failures encountered were limited to (i) a database-scope artefact (PlasmidFinder) and (ii) an
agent-runtime failure (context bloat on a prior backfill attempt), neither of which touches the
verdict. Self-imposed scope limits are enumerated above and cross-referenced to concrete
follow-up work in `open_questions.json`. Every claim the replication was designed to adjudicate is
verified against independent evidence; every claim it was not designed to adjudicate is explicitly
excluded here.
